"""Formato provisional sustituible cuando se aporten informes institucionales."""
from .comun import ROOT, leer

def redactar(result, path):
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE
    template=leer(ROOT/'templates/informe.v1.json')
    doc=Document()
    sec=doc.sections[0]
    sec.page_width,sec.page_height=Inches(8.5),Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.75)
    sec.left_margin=sec.right_margin=Inches(.8)
    for name,size in [('Normal',11),('Title',23),('Subtitle',11),('Heading 1',14),('Heading 2',12)]:
        style=doc.styles[name]
        style.font.name='Calibri'; style.font.size=Pt(size); style.font.color.rgb=RGBColor(0,0,0)
        style.paragraph_format.space_after=Pt(7)
    for border in doc.styles.element.xpath('.//w:pBdr'):
        border.getparent().remove(border)
    doc.core_properties.title=result['titulo']
    doc.core_properties.author='OECE Assistant'
    footer=sec.footer.paragraphs[0]
    footer.text='BORRADOR PARA REVISIÓN  |  '+result['id_ejecucion'][:12]+'  |  Página '
    f=OxmlElement('w:fldSimple'); f.set(qn('w:instr'),'PAGE'); footer._p.append(f)
    for run in footer.runs: run.font.size=Pt(8)
    def table(headers, records, widths):
        t=doc.add_table(rows=1,cols=len(headers)); t.autofit=False
        for col,width in zip(t.columns,widths): col.width=Inches(width)
        for c,h,w in zip(t.rows[0].cells,headers,widths): c.text=h; c.width=Inches(w)
        header=OxmlElement('w:tblHeader'); t.rows[0]._tr.get_or_add_trPr().append(header)
        for record in records:
            for cell,value,width in zip(t.add_row().cells,record,widths):
                cell.text=str(value); cell.width=Inches(width)
        for rn,row in enumerate(t.rows):
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
            for cell in row.cells:
                cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                pr=cell._tc.get_or_add_tcPr()
                borders=OxmlElement('w:tcBorders')
                for side in ('top','left','bottom','right','insideH','insideV'):
                    b=OxmlElement('w:'+side)
                    for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]: b.set(qn('w:'+k),v)
                    borders.append(b)
                pr.append(borders)
                shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'E7EEF5' if rn==0 else 'FFFFFF'); pr.append(shade)
                margins=OxmlElement('w:tcMar')
                for side in ('top','left','bottom','right'):
                    m=OxmlElement('w:'+side); m.set(qn('w:w'),'100');m.set(qn('w:type'),'dxa');margins.append(m)
                pr.append(margins)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(4)
                    for r in p.runs: r.font.size=Pt(10);r.bold=rn==0
        doc.add_paragraph().paragraph_format.space_after=Pt(1)
    def url_link(p,url,label):
        element=OxmlElement('w:hyperlink')
        element.set(qn('r:id'),p.part.relate_to(url,RELATIONSHIP_TYPE.HYPERLINK,is_external=True))
        run=OxmlElement('w:r');text=OxmlElement('w:t');text.text=label;run.append(text);element.append(run);p._p.append(element)
    doc.add_paragraph(result['titulo'],'Title')
    doc.add_paragraph(template['subtitulo'],'Subtitle')
    if result['sintetico']: doc.add_paragraph('EJEMPLO SINTÉTICO SIN DATOS DE UN PROVEEDOR REAL')
    doc.add_paragraph(result['resumen'])
    table(['Dato','Referencia'],[
        ('Expediente',result['expediente']),('Solicitante',result['solicitante']),
        ('Procedimiento',result['titulo']),('Fecha de solicitud declarada',result['fecha_solicitud'] or 'Por precisar'),
        ('Corte normativo',result['seleccion']['corte_normativo'])], [1.8,5.1])
    doc.add_heading(template['secciones']['objeto'],1)
    doc.add_paragraph('Examinar la documentación recibida, identificar las condiciones y evidencias aplicables y proponer observaciones para la evaluación del expediente. Este borrador no constituye una decisión del OECE ni acredita autenticidad documental o una consulta en línea a registros públicos.')
    doc.add_heading(template['secciones']['antecedentes'],1)
    for item in result['antecedentes']:
        doc.add_paragraph(item)
    doc.add_heading(template['secciones']['documentos'],1)
    table(['ID','Documento','Lectura'],[(d['id'],d['archivo'],str(len(d['fragmentos']))+' fragmentos'+(' con alertas' if any(b['alertas'] for b in d['fragmentos']) else '')) for d in result['documentos']], [1.25,4.2,1.45])
    doc.add_heading(template['secciones']['base'],1)
    doc.add_paragraph('Selección de régimen: '+result['seleccion']['regimen']+'. Los datos que definen la rama están declarados en la ficha del expediente. J01 a J05 contienen criterios adoptados por el asistente IA y sus excepciones.')
    sources={}
    for row in result['matriz']:
        src=row.get('fuente_normativa')
        if src:
            key=(src['archivo'],src['disposicion'],src['pagina_pdf'])
            if key not in sources: sources[key]=('N'+str(len(sources)+1),src)
    for source in result.get('normas_adicionales',[]):
        sources[(source['archivo'],source['disposicion'],source['pagina_pdf'])]=(source['codigo'],source)
    for code,src in sources.values():
        p=doc.add_paragraph(f'{code}. {src["disposicion"]}; {src["archivo"]}, página PDF {src["pagina_pdf"]}. ')
        url_link(p,src['url'],'Fuente oficial')
    if not sources:
        doc.add_paragraph('Este módulo entrega un borrador documental asistido. Incorporar las disposiciones específicas verificadas en el análisis; no se reutilizan automáticamente las reglas de consultores.')
    doc.add_heading(template['secciones']['analisis'],1)
    counts=result['conteo']
    doc.add_paragraph(f'La matriz registra {counts.get("cumple",0)} verificaciones documentales satisfechas, {counts.get("no_cumple",0)} diferencias, {counts.get("no_determinable",0)} puntos no determinables y {counts.get("no_aplica",0)} puntos de otras ramas. Estos resultados se limitan a los hechos y documentos citados.')
    # Las explicaciones se mantienen en prosa; matriz compacta sin párrafos extensos.
    for row in result['matriz']:
        if row['resultado']=='no_aplica': continue
        doc.add_paragraph(row['id']+'  '+row['control'],'Heading 2')
        doc.add_paragraph(row['resultado'].replace('_',' ').capitalize()+'. '+row['motivo'])
        refs=row['evidencias']
        if refs:
            doc.add_paragraph('Sustento: '+'; '.join(dict.fromkeys(e['documento']+' '+e['ubicacion'] for e in refs))+'.')
            quote=refs[0]['cita']
            doc.add_paragraph('Extracto: '+quote[:600]+('…' if len(quote)>600 else ''))
        if row['autores']: doc.add_paragraph('Interpretación registrada por '+', '.join(row['autores'])+'.')
    for para in result.get('analisis',[]):
        doc.add_paragraph(para['texto'])
        doc.add_paragraph('Referencias: '+', '.join(para['referencias'])+'. Autor: '+para['autor']+'.')
    doc.add_heading(template['secciones']['observaciones'],1)
    if result['preguntas']:
        for q in result['preguntas']: doc.add_paragraph(q,'List Bullet')
    else: doc.add_paragraph('No se detectaron faltantes dentro de los controles ejecutados; verificar alcance y fuentes antes de adoptar una decisión administrativa.')
    doc.add_heading(template['secciones']['conclusion'],1)
    doc.add_paragraph(result['conclusion'])
    doc.add_heading(template['secciones']['anexos'],1)
    doc.add_paragraph('Acompañan este informe la matriz CSV y JSON, los originales conservados y el manifiesto de integridad. El formato es provisional y se ajustará a los modelos institucionales que aporte el usuario.')
    for d in result['documentos']:
        p=doc.add_paragraph(d['id']+' '+d['archivo']+'\nSHA256 '+d['sha256'])
        for r in p.runs: r.font.size=Pt(9)
    doc.save(path)
