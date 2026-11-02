"""Recuperación de fichas TUPA candidatas; sin dictamen temporal ni nuevos requisitos."""
from datetime import date
import re

from .comun import ROOT,dentro,leer,sha

REGISTRO=ROOT/'normativa/indice-tupa.v0.1.json'
VALORES={'procedimiento':('ampliacion_consultores','aumento_cmc','inscripcion','actualizacion','reconsideracion'),
         'tipo_registro':('bienes','servicios','consultor','ejecutor'),'tipo_persona':('natural','juridica'),
         'origen_proveedor':('nacional','extranjero'),'domicilio':('domiciliado','no_domiciliado'),
         'tipo_tramite':('inscripcion','reinscripcion')}


def consultar(ficha,codigo=None,pagina=None):
    if not isinstance(ficha,dict):raise ValueError('Ficha de expediente inválida')
    for key,values in VALORES.items():
        if ficha.get(key) is not None and ficha[key] not in values:raise ValueError('Valor no admitido: '+key)
    if not ficha.get('procedimiento'):raise ValueError('Procedimiento requerido')
    if codigo is not None and (not isinstance(codigo,str) or not re.fullmatch('PA[0-9A-Z]{8}',codigo)):raise ValueError('Código TUPA inválido')
    if pagina is not None and (type(pagina) is not int or not codigo):raise ValueError('Página entera requiere código TUPA')
    registry=leer(REGISTRO)
    candidates=[f for f in registry['fichas'] if f['procedimiento']==ficha['procedimiento'] and
                all(ficha.get(key) is None or ficha[key] in values for key,values in f['condiciones'].items())]
    missing=sorted({key for f in candidates for key in f['condiciones'] if ficha.get(key) is None})
    alerts=['Fichas candidatas por datos declarados: no prueba de cumplimiento ni de vigencia. No acumular requisitos de ramas alternativas.']
    if ficha['procedimiento']=='inscripcion' and ficha.get('tipo_tramite') is None:alerts.append('Falta distinguir inscripción/reinscripción antes de interpretar requisitos de experiencia.')
    if ficha.get('origen_proveedor')=='nacional' and ficha.get('domicilio')=='no_domiciliado':
        candidates=[];alerts.append('Combinación nacional/no domiciliado: requiere delimitar régimen, sin asignación automática.')
    if not candidates:alerts.append('Sin ficha indexada para esta selección. Actualización se contrasta con directiva 9.6; reconsideración requiere identificar el trámite del acto impugnado. No inventar código TUPA.')
    value=ficha.get('fecha_solicitud');temporal='fecha_no_documentada'
    if value is not None:
        if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):raise ValueError('Fecha ISO inválida')
        try:cut=date.fromisoformat(value)
        except ValueError:raise ValueError('Fecha ISO inválida')
        if cut<date.fromisoformat(registry['publicacion_acto']['fecha']):temporal='requiere_version_historica'
        elif cut>date.fromisoformat(registry['corte_documental']):temporal='requiere_actualizar_fuentes'
        else:temporal='dentro_corte_documental_sin_resolver_vigencia'
    result={'version_indice':registry['version'],'sha256_indice':sha(REGISTRO.read_bytes()),'fuente':registry['fuente'],
            'corte_documental':registry['corte_documental'],'estado_temporal':temporal,'aplicabilidad_juridica':'no_determinable',
            'campos_faltantes':missing,'alertas':alerts,'fichas_candidatas':candidates,'alcance':registry['alcance']}
    if codigo is not None:
        item=next((f for f in candidates if f['codigo']==codigo),None)
        if item is None:raise ValueError('Código no pertenece a las fichas candidatas; revisar datos y consultar índice')
        source=registry['fuente']
        from .biblioteca import fuentes
        official=next((s for s in fuentes() if s['name']==source['name']),None)
        if not official or any(source[k]!=official[k] for k in ('sha256','source_url','local_path','instrument_id')):raise ValueError('Fuente fuera del manifiesto')
        path=dentro(ROOT,source['local_path'])
        if sha(path.read_bytes())!=source['sha256']:raise ValueError('Original TUPA alterado')
        page=pagina if pagina is not None else item['paginas'][0]['pagina_pdf']
        expected=next((p for p in item['paginas'] if p['pagina_pdf']==page),None)
        if expected is None:raise ValueError('Página fuera de la ficha seleccionada')
        from pypdf import PdfReader
        text=PdfReader(path).pages[page-1].extract_text() or ''
        if sha(text.encode('utf-8'))!=expected['sha256_texto']:raise ValueError('Extracción cambió; reconstruir y revisar índice TUPA')
        result['pagina']={'codigo':codigo,'ubicacion':'pagina:'+str(page),'texto':text,'sha256_texto':expected['sha256_texto'],
                          'advertencia':'Página completa; el orden extraído puede mezclar descripción y requisitos. Cotejar el PDF.'}
    return result
