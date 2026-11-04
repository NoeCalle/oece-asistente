"""Construye el catálogo de preparación de los cinco trámites desde originales."""
from pathlib import Path
import copy
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.biblioteca import fuentes
from oece.comun import data_dir,guardar,leer,ruta_original,sha
from oece.lectura import leer_documento


def construir():
    import pdfplumber
    from pypdf import PdfReader
    from docx import Document
    from docx.table import Table
    result=copy.deepcopy(leer(ROOT/'rules/requisitos-ampliaciones.v1.5.json'))
    result.update(version='1.6.0',alcance='Preparación documental de cinco trámites. Cada unidad requiere interpretación y evidencia; no acredita cumplimiento ni vigencia.')
    by_name={s['name']:s for s in fuentes()};verified={};pdfs={}
    def source(name):
        s=by_name[name]
        if name not in verified:
            path=ruta_original(s['local_path'])
            if sha(path.read_bytes())!=s['sha256']:raise ValueError('Original alterado: '+name)
            verified[name]=path
        return s
    def ref(name,page=None,quote=None,**extras):
        s=source(name);r={'archivo':name,'url':s['source_url'],'sha256':s['sha256'],**extras}
        if page is not None:r['pagina_pdf']=page
        if quote is not None:r['cita']=quote
        return r
    def page(name,n):
        source(name)
        if name not in pdfs:pdfs[name]=PdfReader(verified[name])
        return pdfs[name].pages[n-1].extract_text() or ''
    def add(rid,title,procedure,refs,conditions=None,**extras):
        result['requisitos'].append({'id':rid,'titulo':title,'procedimiento':procedure,'ambito':'expediente',
            'fuentes':refs,'condiciones':conditions or {},'hechos_orientativos':[],
            'revision_humana':None,'apta_para_reglas':False,'caracter':'unidad_de_revision',**extras})
    # Recortes físicos del bloque Requisitos evitan mezclar la descripción que pypdf reordena.
    tupa='tupa-modificacion-2026-073.pdf';source(tupa)
    with pdfplumber.open(verified[tupa]) as pdf:
        for ficha in leer(ROOT/'normativa/indice-tupa.v0.1.json')['fichas']:
            if ficha['procedimiento']!='inscripcion':continue
            first=ficha['paginas'][0]['pagina_pdf'];items=[];current=None
            for loc in ficha['paginas']:
                number=loc['pagina_pdf'];p=pdf.pages[number-1];words=p.extract_words()
                req=next((w for w in words if w['text']=='Requisitos'),None)
                note=next((w for w in words if w['text']=='Notas:'),None)
                if number>first and not note:raise ValueError('Revisar continuación de requisitos '+ficha['codigo'])
                if number==first and not req:raise ValueError('Bloque Requisitos no localizado')
                bbox=[60,req['bottom']+5 if req else 75,552,note['top']-1 if note else p.height-30]
                text=p.crop(tuple(bbox)).extract_text() or ''
                markers=list(re.finditer(r'(?m)^([0-9]+)\.\-\s',text))
                spans=[(0,markers[0].start(),None)] if markers and markers[0].start() else []
                spans += [(m.start(),markers[i+1].start() if i+1<len(markers) else len(text),int(m[1])) for i,m in enumerate(markers)]
                if not markers:spans=[(0,len(text),None)]
                for start,end,num in spans:
                    quote=text[start:end].strip()
                    if not quote:continue
                    if num is not None:
                        current={'numero':num,'fuentes':[],'titulo':re.sub(r'\s+',' ',quote).split('.',1)[-1].strip().lstrip('- ')[:180]};items.append(current)
                    if current is None:raise ValueError('Continuación sin requisito')
                    current['fuentes'].append(ref(tupa,number,quote,metodo='pdfplumber_recorte',bbox=bbox,disposicion=ficha['codigo']+' requisito '+str(current['numero'])))
                if note:break
            if [r['numero'] for r in items]!=list(range(1,len(items)+1)):raise ValueError('Numeración incompleta '+ficha['codigo'])
            for item in items:
                add('IN-'+ficha['codigo']+'-'+str(item['numero']),item['titulo'],'inscripcion',item['fuentes'],
                    codigo_tupa=ficha['codigo'],condiciones=ficha['condiciones'],subsupuestos='Leer todos los incisos: inscripción/reinscripción, experiencia, finanzas y excepciones se delimitan con los datos del caso. No exigirlos acumulativamente.')
    directiva='6682380-directiva-de-procedimientos-y-tramites-ante-el-registro-nacional-de-proveedores.pdf'
    d13=page(directiva,13);d14=page(directiva,14);d15=page(directiva,15);d16=page(directiva,16)
    def cut(text,start,end=None):
        a=text.index(start);return text[a:text.index(end,a+len(start)) if end else len(text)].strip()
    for number,end in [('9.6.1','9.6.2'),('9.6.2','9.6.3'),('9.6.3','9.6.4'),('9.6.4','Actualización de Información Legal'),('9.6.5','9.6.6')]:
        cond={'clase_actualizacion':['legal']} if number=='9.6.5' else {'documentos_extranjeros':[True]} if number in ('9.6.2','9.6.3') else {'documentos_extranjeros':[True],'documentos_en_espanol':[False]} if number=='9.6.4' else {}
        add('AU-'+number,'Actualización: '+number,'actualizacion',[ref(directiva,13,cut(d13,number,end),disposicion=number)],cond,
            supuesto='representacion' if number=='9.6.1' else None)
    add('AU-9.6.6','Distribución accionaria y alternativas documentales','actualizacion',
        [ref(directiva,13,cut(d13,'9.6.6'),disposicion='9.6.6'),ref(directiva,14,cut(d14,'general de accionistas','Actualización de Información Financiera'),disposicion='9.6.6 continuación')],
        {'clase_actualizacion':['legal'],'tipo_persona':['juridica']},subsupuestos='Tipo societario, acciones cotizadas, país que no expide instrumentos y facultades del declarante; alternativas, no lista acumulativa.')
    head=cut(d14,'9.6.7','a) Las personas')
    add('AU-9.6.7','Formulario Anexo 6 y solvencia según rama','actualizacion',[ref(directiva,14,head,disposicion='9.6.7')],{'clase_actualizacion':['financiera'],'tipo_registro':['ejecutor','consultor']})
    for letter,end,cond in [('a','b)',{'origen_proveedor':['nacional'],'motivo_actualizacion':['rectificatoria']}),
                            ('b','c)',{'tipo_persona':['natural'],'motivo_actualizacion':['reduccion_capital_contable']}),
                            ('c','d)',{'tipo_persona':['juridica'],'motivo_actualizacion':['reduccion_capital_social']}),
                            ('d',None,{'motivo_actualizacion':['rectificatoria','reduccion_capital_contable','reduccion_capital_social']})]:
        add('AU-9.6.7-'+letter,'Supuesto financiero '+letter,'actualizacion',[ref(directiva,14,cut(d14,letter+')',end),disposicion='9.6.7.'+letter)],{'clase_actualizacion':['financiera'],**cond})
    groups=[('PNN','natural','nacional',[(15,cut(d15,'Para la persona natural nacional','Para la persona natural extranjera'))]),
            ('PNE','natural','extranjero',[(15,cut(d15,'Para la persona natural extranjera')),(16,cut(d16,'mínimo,','Para la persona jurídica nacional'))]),
            ('PJN','juridica','nacional',[(16,cut(d16,'Para la persona jurídica nacional','Para la persona jurídica extranjera'))]),
            ('PJE','juridica','extranjero',[(16,cut(d16,'Para la persona jurídica extranjera'))])]
    for code,person,origin,parts in groups:
        add('AU-FIN-'+code,'Información financiera: '+person+' '+origin,'actualizacion',
            [ref(directiva,p,t,disposicion='9.6.7, '+person+' '+origin) for p,t in parts],
            {'clase_actualizacion':['financiera'],'tipo_persona':[person],'origen_proveedor':[origin],'tipo_registro':['ejecutor','consultor']},
            subsupuestos='Delimitar motivo, declaración, auditoría, capital, SBS y consultor natural inscrito como ejecutor. No acumular todos los incisos.')
    # Anexo Word: conservar localizadores y celdas combinadas, sin inventar contenido de celdas vacías.
    annex=next(n for n in by_name if 'anexo-n-5-' in n);source(annex)
    reading=leer_documento(verified[annex],data_dir()/'catalogo-lecturas',False)
    document=Document(verified[annex]);fragments=reading['fragmentos']
    for block,table in enumerate(document.iter_inner_content(),1):
        if not isinstance(table,Table):continue
        person='natural' if 'NATURAL' in table.rows[0].cells[0].text else 'juridica'
        first_cells={}
        for rn,row in enumerate(table.rows,1):
            for cn,cell in enumerate(row.cells,1):first_cells.setdefault(cell._tc,(rn,cn))
        for rn,row in enumerate(table.rows,1):
            if rn<3:continue
            title=row.cells[0].text.strip();refs=[];columns=[]
            for cn,cell in enumerate(row.cells,1):
                if cn==1:continue
                rr,cc=first_cells[cell._tc];prefix=f'cuerpo/bloque:{block}/fila:{rr}/celda:{cc}/'
                matching=[f for f in fragments if f['ubicacion'].startswith(prefix)]
                columns.append({'columna':cn,'encabezado':table.rows[1].cells[cn-1].text,'localizadores':[f['ubicacion'] for f in matching],'sin_texto':not matching})
                for f in matching:
                    if any(r.get('ubicacion')==f['ubicacion'] for r in refs):continue
                    refs.append(ref(annex,quote=f['texto'],ubicacion=f['ubicacion'],disposicion='Anexo 5: '+title))
            labels={'natural':{3:'condicion_sunat',4:'nombres',5:'domicilio_fiscal',6:'profesion',7:'representacion'},
                    'juridica':{3:'condicion_sunat',4:'denominacion_social',5:'domicilio_fiscal',6:'estructura_societaria',7:'domiciliada_a_no_domiciliada',8:'no_domiciliada_a_domiciliada',9:'representacion'}}
            add('AU-A5-'+person+'-'+str(rn),title,'actualizacion',refs,{'clase_actualizacion':['legal'],'tipo_persona':[person]},dato_actualizado=labels[person][rn],
                caracter='supuesto_de_actualizacion',columnas=columns,subsupuestos='Elegir el dato que cambió y la columna del proveedor; celdas vacías no crean documentos. Las celdas combinadas conservan su procedencia.')
    tuo='tuo-27444-minjus-julio-2026.pdf';t138=page(tuo,138);t139=page(tuo,139);t193=page(tuo,193);t194=page(tuo,194)
    # El numeral 7 continúa en la página siguiente: no truncar el artículo 113.
    body=cut(t138,'1. Nombres')
    for number in range(1,7):
        quote=cut(body,str(number)+'. ',str(number+1)+'. ' if number<6 else None)
        add('RC-113-'+str(number),'Requisito del escrito '+str(number),'reconsideracion',[ref(tuo,138,quote,disposicion='113.'+str(number))])
    add('RC-113-7','Identificación de expediente ya iniciado','reconsideracion',[ref(tuo,139,cut(t139,'7. La identificación','(Texto según'),disposicion='113.7')])
    for code,title,p,text,start,end in [('207','Plazo de interposición y resolución',193,t193,'Artículo 207.',None),
                                     ('208','Mismo órgano, nueva prueba y única instancia',194,t194,'Artículo 208.-','Artículo 209.-'),
                                     ('211','Identificar el acto recurrido',194,t194,'Artículo 211.-','Artículo 212.-')]:
        add('RC-'+code,title,'reconsideracion',[ref(tuo,p,cut(text,start,end),disposicion='Artículo '+code)],caracter='condicion_de_analisis',subsupuestos='Cotejar notificación eficaz, calendario, competencia y régimen especial; no contar días ni presumir única instancia sin hechos citados.')
    result['pendientes']=['Verificar vigencia y modificatorias a las fechas del caso','Interpretar condiciones, alternativas y excepciones con fuentes y hechos citados',
                          'Adaptar formato laboral al recibirlo; la interpretación y la revisión final son tareas del coordinador']
    result['extraccion_adicional']={'pdfplumber':'0.11.9','metodo':'recorte_fisico_del_bloque_requisitos','anexo_word':'localizador_de_celda_y_bloque'}
    return result


if __name__=='__main__':
    import logging,json
    logging.getLogger('pypdf').setLevel(logging.ERROR)
    r=construir();guardar(ROOT/'rules/requisitos.v1.6.json',r)
    print(json.dumps({'unidades':len(r['requisitos']),'por_tramite':{p:sum(x['procedimiento']==p for x in r['requisitos']) for p in sorted({x['procedimiento'] for x in r['requisitos']})}}))
