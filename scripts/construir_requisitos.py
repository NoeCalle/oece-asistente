"""Segmenta requisitos expresos de dos fichas, sobre originales identificados."""
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.biblioteca import fuentes
from oece.comun import dentro,guardar,sha


def entre(text,inicio,fin):
    start=text.index(inicio);end=text.index(fin,start+len(inicio)) if fin else len(text)
    return text[start:end].strip()


def construir():
    from pypdf import PdfReader
    sources={s['name']:s for s in fuentes()}
    names=['tupa-modificacion-2026-073.pdf','reglamento-consolidado-2026-01-09.pdf',
           '6682380-directiva-de-procedimientos-y-tramites-ante-el-registro-nacional-de-proveedores.pdf']
    expected=['d3ab3f6b87f7b5706177c8a7f6df8bd202a0f3878c686f23a5047d5264834b7e',
              '0ebe95b3e05661b80f73c060d6e6ce8dd17621ce34af9277c688dd67e5d99830',
              'a1f62195f04cf69640b64b1f3478a27fa7f994852490a42913c40ff666890847']
    pdfs={}
    for name,digest in zip(names,expected):
        source=sources[name];path=dentro(ROOT,source['local_path'])
        if source['sha256']!=digest or sha(path.read_bytes())!=digest:raise ValueError('Revisar mapa: original distinto '+name)
        pdfs[name]=PdfReader(path)
    def ref(name,page,disposition,quote=None):
        s=sources[name];r={'archivo':name,'url':s['source_url'],'sha256':s['sha256'],'pagina_pdf':page,'disposicion':disposition}
        if quote is not None:
            if quote not in (pdfs[name].pages[page-1].extract_text() or ''):raise ValueError('Cita fuera del original')
            r['cita']=quote
        return r
    records=[]
    for procedure,prefix,page,article,code in [('ampliacion_consultores','AC',31,'381.4','PA42003A92'),('aumento_cmc','CMC',28,'381.5','PA42009D33')]:
        text=pdfs[names[0]].pages[page-1].extract_text() or ''
        requirements=entre(text,'1.- Solicitud','Notas:')
        def add(identifier,title,quote,origin=None,subcontract=None,number='',orient=(),alternatives=None):
            article_page=210 if prefix=='AC' or number=='1' else 212 if number=='3.3.e' else 211
            records.append({'id':prefix+'-'+identifier,'procedimiento':procedure,'codigo_tupa':code,
                            'titulo':title,'ambito':'experiencia' if origin else 'expediente',
                            'origen':origin,'subcontrato':subcontract,'hechos_orientativos':list(orient),
                            'fuentes':[ref(names[0],page,code+' requisito '+number,quote),ref(names[1],article_page,article+'.'+number)],
                            'alternativas_documentales':alternatives or [],'revision_humana':None,'apta_para_reglas':False})
        add('R01','Solicitud presentada mediante formulario',entre(requirements,'1.-','2.-'),number='1',orient=['solicitud_presentada'])
        add('R02','Número de recibo y fecha de pago',entre(requirements,'2.-','3.-'),number='2',orient=['recibo_numero','pago_fecha'])
        law=entre(requirements,'i. En el marco','ii. Fuera del marco')
        law=law[law.index('a)'):].strip()
        add('L-a','Constancia u otro documento de la entidad con los datos exigidos',law,'peru_ley',False if prefix=='CMC' else None,'3.1.i.a',
            ['documento_entidad','datos_constancia_completos'])
        private=entre(requirements,'ii. Fuera del marco','3.2 ')
        titles=['Contrato','Documento del contratante con los datos exigidos','Aprobación/viabilidad/conformidad según el objeto y autoridad competente' if prefix=='AC' else 'Conformidad de obra por autoridad competente u órgano técnico cuando corresponda',
                'Descripción de obra y actividades del consultor' if prefix=='AC' else 'Facturas o boletas cuya suma equivalga al monto final',
                'Comprobantes de pago cuya suma equivalga al monto final']
        fields=['contrato','datos_contratante','aprobacion_viabilidad_conformidad' if prefix=='AC' else 'conformidad_obra',
                'descripcion_actividades' if prefix=='AC' else 'comprobantes_equivalentes','comprobantes_equivalentes']
        letters='abcde' if prefix=='AC' else 'abcd'
        for i,letter in enumerate(letters):
            quote=entre(private,letter+')',letters[i+1]+')' if i+1<len(letters) else None)
            add('P-'+letter,titles[i],quote,'peru_fuera_ley',None,'3.1.ii.'+letter,[fields[i]])
        foreign=entre(requirements,'3.2 ','3.3 ' if prefix=='CMC' else None)
        for letter,title,field,next_marker in [('a','Contrato de la experiencia extranjera','contrato','b)'),('b','Documento extranjero del contratante con los datos exigidos','datos_extranjero_completos',None)]:
            add('E-'+letter,title,entre(foreign,letter+')',next_marker),'extranjero',None,'3.2.'+letter,
                [field,'conformidad_viabilidad'] if prefix=='AC' and letter=='b' else [field])
        if prefix=='CMC':
            sub=entre(requirements,'3.3 ',None)
            titles=['Contrato principal o referencias admitidas cuando está registrado en la plataforma',
                    'Autorización de la entidad para celebrar el subcontrato','Subcontrato',
                    'Documento del contratista principal con los datos exigidos','Facturas cuya suma equivalga al monto final']
            for i,letter in enumerate('abcde'):
                alt=[{'via':'copia_contrato_principal','verificar':'Copia del contrato de ejecución de obra'},
                     {'via':'referencia_registro_plataforma','verificar':'Registro efectivo del contrato; número, nomenclatura del procedimiento y entidad en la solicitud'}] if letter=='a' else []
                add('S-'+letter,titles[i],entre(sub,letter+')','abcde'[i+1]+')' if i<4 else None),'peru_ley',True,'3.3.'+letter,
                    ['subcontrato_autorizado'] if letter=='b' else ['documentacion_subcontrato_completa'],alt)
    exclusions=[]
    for page,letters,start,end in [(11,'ab','9.2.9 ',None),(12,'cdefghij','c) ','9.3 AUMENTO')]:
        text=pdfs[names[2]].pages[page-1].extract_text() or ''
        section=entre(text,start,end)
        for i,letter in enumerate(letters):
            quote=entre(section,letter+')',letters[i+1]+')' if i+1<len(letters) else None)
            exclusions.append({'id':'EX-'+letter,'caracter':'alerta_de_analisis_no_documento_adicional','fuente':ref(names[2],page,'9.2.9.'+letter,quote)})
    return {'version':'1.5.0','fecha':'2026-11-01','autor':'asistente_ia','corte_normativo':'2026-10-31',
            'alcance':'Plan documental de 24 requisitos expresos y diez alertas; no acredita cumplimiento ni vigencia y no sustituye condiciones del artículo 25, régimen ni excepciones.',
            'requisitos':records,'alertas_exclusion':exclusions,
            'remisiones':[ref(names[2],12,'9.3.1–9.3.3')],
            'pendientes':['Cadena temporal y eficacia por disposición','Delimitar categoría (a), objeto y autoridad competente del caso',
                          'Reorganización societaria: cotejar excepciones del artículo 25.7 modificado, sin rechazo automático',
                          'Ramas de inscripción, actualización y reconsideración no segmentadas aquí']}


if __name__=='__main__':
    import logging,json
    logging.getLogger('pypdf').setLevel(logging.ERROR)
    result=construir();guardar(ROOT/'rules/requisitos-ampliaciones.v1.5.json',result)
    print(json.dumps({'requisitos':len(result['requisitos']),'alertas':len(result['alertas_exclusion'])}))
