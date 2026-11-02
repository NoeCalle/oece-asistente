"""Plan de lectura documental por experiencia; no evalúa presencia ni cumplimiento."""
from .comun import ROOT,dentro,leer,sha
from .evaluacion import seleccionar

REGISTRO=ROOT/'rules/requisitos-ampliaciones.v1.5.json'


def verificar(registry=None):
    """Comprueba todos los pasajes literales y fuentes del registro contra originales."""
    from pypdf import PdfReader
    from .biblioteca import fuentes
    registry=registry or leer(REGISTRO);manifest={s['name']:s for s in fuentes()};pdfs={};count=0
    refs=[s for r in registry['requisitos'] for s in r['fuentes']]
    refs += [a['fuente'] for a in registry['alertas_exclusion']]+registry['remisiones']
    for ref in refs:
        source=manifest.get(ref['archivo'])
        if source is None or source['sha256']!=ref['sha256'] or source['source_url']!=ref['url']:raise ValueError('Fuente del requisito fuera del manifiesto')
        if ref['archivo'] not in pdfs:
            path=dentro(ROOT,source['local_path'])
            if sha(path.read_bytes())!=source['sha256']:raise ValueError('Original de requisitos alterado')
            pdfs[ref['archivo']]=PdfReader(path)
        pdf=pdfs[ref['archivo']];page=ref['pagina_pdf']
        if type(page) is not int or not 1<=page<=len(pdf.pages):raise ValueError('Página del requisito inválida')
        if 'cita' in ref:
            if not ref['cita'] or ref['cita'] not in (pdf.pages[page-1].extract_text() or ''):raise ValueError('Cita del requisito no contenida en el original')
            count+=1
    return {'originales':len(pdfs),'referencias':len(refs),'citas_literales':count,'alcance':'integridad_y_procedencia_no_aplicabilidad_juridica'}


def planificar(config):
    registry=leer(REGISTRO);route=seleccionar(config);procedure=config['procedimiento']
    catalog=[r for r in registry['requisitos'] if r['procedimiento']==procedure]
    result={'version':registry['version'],'sha256_registro':sha(REGISTRO.read_bytes()),'procedimiento':procedure,
            'alcance':registry['alcance'],'es_evaluacion_de_cumplimiento':False,
            'estado':'plan_de_revision' if catalog else 'fuera_cobertura','catalogo':catalog,'tareas':[],
            'alertas_exclusion':registry['alertas_exclusion'] if catalog else [],'pendientes':list(route['preguntas']),
            'limites':registry['pendientes'],'vigencia':'no_determinable'}
    if not catalog:return result
    for record in catalog:
        if record['ambito']=='expediente':result['tareas'].append({'id':record['id'],'requisito_id':record['id'],'experiencia':None,'seleccion_documental':'aplica','revision':'pendiente_interpretacion'})
    if not route['experiencias']:result['pendientes'].append('Identificar experiencias que sustentan ampliación/aumento; no se inventa una experiencia ni se presume ausencia de documentos.')
    for exp in route['experiencias']:
        origin=exp.get('origen');sub=exp.get('subcontrato')
        if sub is not None and type(sub) is not bool:raise ValueError('subcontrato debe ser booleano o null')
        if sub is True and (procedure=='ampliacion_consultores' or origin!='peru_ley'):
            result['pendientes'].append('Experiencia '+exp['id']+': delimitar subcontrato, autorización y exclusiones 9.2.9; no trasladar la lista 3.3 de obras públicas peruanas a otra rama.')
        for record in catalog:
            if record['ambito']!='experiencia':continue
            if origin in ('peru_ley','peru_fuera_ley','extranjero') and record['origen']!=origin:continue
            state='aplica' if origin==record['origen'] else 'no_determinable'
            if record['subcontrato'] is not None:
                if sub is not None and sub!=record['subcontrato']:continue
                if sub is None:state='no_determinable'
            result['tareas'].append({'id':record['id']+'/'+exp['id'],'requisito_id':record['id'],'experiencia':exp['id'],
                                     'seleccion_documental':state,'revision':'pendiente_interpretacion'})
        if procedure=='aumento_cmc' and origin=='peru_ley' and sub is None:
            result['pendientes'].append('Experiencia '+exp['id']+': precisar si es contrato directo o subcontrato para elegir 3.1.i o 3.3; no acumular ambas listas.')
    # La selección es documental, no habilitación temporal de un requisito.
    from .tupa import consultar
    result['estado_temporal']=consultar(config)['estado_temporal']
    result['pendientes']=list(dict.fromkeys(result['pendientes']))
    return result
