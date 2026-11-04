"""Plan trazable de los cinco trámites, con verificación de originales y recortes."""
from functools import lru_cache
from io import BytesIO
import json

from .comun import ROOT,data_dir,leer,ruta_original,sha,bytes_json
from .evaluacion import seleccionar
from . import requisitos as anterior

REGISTRO=ROOT/'rules/requisitos.v1.6.json'
DATOS_LEGALES={'condicion_sunat','nombres','domicilio_fiscal','profesion','representacion','denominacion_social',
               'estructura_societaria','domiciliada_a_no_domiciliada','no_domiciliada_a_domiciliada'}


@lru_cache(maxsize=2)
def _citas(serialized,contents):
    from pypdf import PdfReader
    import pdfplumber
    from .lectura import leer_documento
    registry=json.loads(serialized);raws=dict(contents);pdfs={};cropped={};words={};texts={};count=0
    refs=[s for r in registry['requisitos'] for s in r['fuentes']]+[r['fuente'] for r in registry['alertas_exclusion']]+registry['remisiones']
    for ref in refs:
        name=ref['archivo'];raw=raws[name]
        if name.endswith('.docx'):
            if name not in words:
                from .biblioteca import fuentes
                path=ruta_original(next(s['local_path'] for s in fuentes() if s['name']==name))
                words[name]={b['ubicacion']:b['texto'] for b in leer_documento(path,data_dir()/'catalogo-lecturas',False)['fragmentos']}
                if sha(path.read_bytes())!=ref['sha256']:raise ValueError('Anexo cambió durante la lectura')
            text=words[name].get(ref.get('ubicacion'),'')
        else:
            number=ref.get('pagina_pdf')
            if type(number) is not int or number<1:raise ValueError('Página inválida del plan')
            if ref.get('metodo')=='pdfplumber_recorte':
                if name not in cropped:cropped[name]=pdfplumber.open(BytesIO(raw))
                bbox=ref.get('bbox')
                if not isinstance(bbox,list) or len(bbox)!=4 or any(type(x) not in (int,float) for x in bbox):raise ValueError('Recorte inválido')
                if number>len(cropped[name].pages):raise ValueError('Página fuera de rango')
                key=(name,number,tuple(bbox))
                if key not in texts:texts[key]=cropped[name].pages[number-1].crop(tuple(bbox)).extract_text() or ''
                text=texts[key]
            else:
                if name not in pdfs:pdfs[name]=PdfReader(BytesIO(raw))
                if number>len(pdfs[name].pages):raise ValueError('Página fuera de rango')
                if 'cita' not in ref:continue
                key=(name,number)
                if key not in texts:texts[key]=pdfs[name].pages[number-1].extract_text() or ''
                text=texts[key]
        if 'cita' in ref:
            if not isinstance(ref['cita'],str) or not ref['cita'].strip() or ref['cita'] not in text:raise ValueError('Cita no contenida en la ubicación del plan')
            count+=1
    for pdf in cropped.values():pdf.close()
    return {'originales':len(contents),'referencias':len(refs),'citas_literales':count,
            'alcance':'procedencia_y_segmentacion_no_cumplimiento_ni_vigencia'}


def verificar(registry=None):
    from .biblioteca import fuentes
    registry=leer(REGISTRO) if registry is None else registry;manifest={s['name']:s for s in fuentes()};originals={}
    refs=[s for r in registry['requisitos'] for s in r['fuentes']]+[r['fuente'] for r in registry['alertas_exclusion']]+registry['remisiones']
    for ref in refs:
        name=ref.get('archivo');s=manifest.get(name)
        if s is None or ref.get('sha256')!=s['sha256'] or ref.get('url')!=s['source_url']:raise ValueError('Fuente fuera del manifiesto')
        if name not in originals:
            raw=ruta_original(s['local_path']).read_bytes()
            if sha(raw)!=s['sha256']:raise ValueError('Original del plan alterado')
            originals[name]=raw
    # Se cotejan los bytes en cada llamada. Solo se reutiliza el cotejo textual de contenido idéntico.
    return dict(_citas(bytes_json(registry),tuple(sorted(originals.items()))))


def planificar(config):
    route=seleccionar(config);registry=leer(REGISTRO);procedure=config['procedimiento']
    if procedure in ('ampliacion_consultores','aumento_cmc'):
        result=anterior.planificar(config,registry=registry)
        result.update(version=registry['version'],sha256_registro=sha(REGISTRO.read_bytes()),limites=registry['pendientes'])
        return result
    catalog=[r for r in registry['requisitos'] if r['procedimiento']==procedure]
    tasks=[];pending=list(route['preguntas']);codes=None
    from .tupa import consultar
    tupa=consultar(config)
    if procedure=='inscripcion':
        codes={f['codigo'] for f in tupa['fichas_candidatas']}
        catalog=[r for r in catalog if r['codigo_tupa'] in codes]
        pending.extend(tupa['alertas'])
    datos=config.get('datos_actualizados')
    if datos is not None and (not isinstance(datos,list) or not datos or any(not isinstance(d,str) or d not in DATOS_LEGALES for d in datos) or len(set(datos))!=len(datos)):
        raise ValueError('Precisar datos_actualizados con identificadores admitidos')
    for r in catalog:
        conditions=r.get('condiciones',{});state='aplica';extra={}
        if any(config.get(k) is not None and config[k] not in v for k,v in conditions.items()):continue
        if any(config.get(k) is None for k in conditions):state='no_determinable'
        if codes is not None and len(codes)!=1:state='no_determinable'
        if r.get('supuesto')=='representacion':
            if config.get('tipo_persona')=='natural' and config.get('actua_por_representante') is False:continue
            if config.get('tipo_persona')!='juridica' and config.get('actua_por_representante') is not True:state='no_determinable'
        if 'dato_actualizado' in r:
            if datos is None:state='no_determinable'
            elif r['dato_actualizado'] not in datos:continue
            column=2 if config.get('origen_proveedor')=='nacional' else 3 if config.get('origen_proveedor')=='extranjero' and config.get('domicilio')=='domiciliado' else 4 if config.get('origen_proveedor')=='extranjero' and config.get('domicilio')=='no_domiciliado' else None
            chosen=next((c for c in r['columnas'] if c['columna']==column),None)
            extra={'columna_fuente':column,'localizadores_a_cotejar':chosen['localizadores'] if chosen else []}
            if not chosen or chosen['sin_texto']:
                state='no_determinable';pending.append(r['id']+': no inferir documentos de una columna sin texto o sin seleccionar; cotejar la tabla y la excepción aplicable.')
        if r['id']=='AU-9.6.6':
            if datos is not None and 'estructura_societaria' not in datos:continue
            if datos is None:state='no_determinable'
        tasks.append({'id':r['id'],'requisito_id':r['id'],'experiencia':None,'seleccion_documental':state,'revision':'pendiente_interpretacion',**extra})
    if procedure=='actualizacion' and config.get('clase_actualizacion')=='legal' and datos is None:pending.append('Identificar los datos legales que variaron para seleccionar los supuestos del Anexo 5; no exigir toda la tabla.')
    if procedure=='inscripcion' and config.get('tipo_tramite') not in ('inscripcion','reinscripcion'):pending.append('Distinguir inscripción de reinscripción en los incisos de experiencia.')
    if procedure=='reconsideracion':pending.append('Identificar acto, notificación eficaz, nueva prueba/única instancia y calendario aplicable; el plan no decide estos hechos.')
    return {'version':registry['version'],'sha256_registro':sha(REGISTRO.read_bytes()),'procedimiento':procedure,
            'alcance':registry['alcance'],'es_evaluacion_de_cumplimiento':False,'estado':'plan_de_revision',
            'catalogo':catalog,'tareas':tasks,'alertas_exclusion':registry['alertas_exclusion'] if procedure=='inscripcion' and config.get('tipo_registro') in ('consultor','ejecutor') else [],
            'pendientes':list(dict.fromkeys(pending)),'limites':registry['pendientes'],'vigencia':'no_determinable','estado_temporal':tupa['estado_temporal']}
