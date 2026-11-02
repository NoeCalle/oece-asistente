"""Reconstruye quince fichas identificadas del anexo oficial, sin resolver vigencia."""
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.biblioteca import fuentes
from oece.comun import dentro,guardar,sha

# Identificación cotejada con los encabezados; no inferir ramas desde texto libre.
MAPA=[
 ('PA42009D33',28,30,'aumento_cmc',{}),
 ('PA42003A92',31,33,'ampliacion_consultores',{}),
 ('PA4200F589',34,35,'inscripcion',{'tipo_registro':['bienes','servicios'],'tipo_persona':['natural'],'origen_proveedor':['extranjero'],'domicilio':['no_domiciliado']}),
 ('PA4200067C',36,37,'inscripcion',{'tipo_registro':['bienes','servicios'],'tipo_persona':['juridica'],'origen_proveedor':['extranjero'],'domicilio':['no_domiciliado']}),
]
for start,code,register,person,origin in [
 (38,'PA42007D51','consultor','natural','nacional'),(41,'PA42009762','consultor','natural','extranjero'),
 (44,'PA42001C78','consultor','juridica','nacional'),(47,'PA4200ED2E','consultor','juridica','extranjero'),
 (50,'PA42003A4F','ejecutor','natural','nacional'),(53,'PA4200C4F5','ejecutor','natural','extranjero'),
 (56,'PA42000DF5','ejecutor','juridica','nacional'),(59,'PA42009BA2','ejecutor','juridica','extranjero')]:
 MAPA.append((code,start,start+2,'inscripcion',{'tipo_registro':[register],'tipo_persona':[person],'origen_proveedor':[origin]}))
for start,code,person in [(62,'PA4200EF4C','juridica'),(64,'PA42004846','natural')]:
 MAPA.append((code,start,start+1,'inscripcion',{'tipo_registro':['bienes','servicios'],'tipo_persona':[person],'domicilio':['domiciliado']}))
MAPA.append(('PA42007484',66,67,'inscripcion',{'tipo_registro':['bienes','servicios'],'origen_proveedor':['extranjero'],'domicilio':['no_domiciliado']}))

def construir():
 from pypdf import PdfReader
 source=next(s for s in fuentes() if s['name']=='tupa-modificacion-2026-073.pdf')
 if source['sha256']!='d3ab3f6b87f7b5706177c8a7f6df8bd202a0f3878c686f23a5047d5264834b7e':raise ValueError('Revisar mapa antes de cambiar de original')
 path=dentro(ROOT,source['local_path'])
 if sha(path.read_bytes())!=source['sha256']:raise ValueError('Original alterado')
 pdf=PdfReader(path);items=[]
 for code,start,end,procedure,conditions in MAPA:
  text=pdf.pages[start-1].extract_text() or ''
  heading=re.search(r'Denominación del Procedimiento Administrativo\s+"(.*?)"\s+Código:\s*(\w+)',text,re.S)
  if not heading or heading[2]!=code:raise ValueError('Encabezado no coincide: '+code)
  alerts=['Leer requisitos, notas y base legal de todas las páginas. El orden de extracción no reproduce siempre la maquetación.']
  if code=='PA42003A92':alerts.append('La descripción menciona categorías A/B/C/D: no resuelve el régimen del artículo 27 ni la transición J01. No usarla como umbral automático.')
  if code=='PA42007484':alerts.append('Rama especial de bienes sofisticados/servicios especializados sin representante en Perú. No presumirla por actua_por_representante=false; comprobar condiciones y responsable designado por la entidad.')
  if code in ('PA4200F589','PA4200067C'):alerts.append('Cotejar representación en Perú o país de origen; el campo genérico actua_por_representante no delimita por sí solo la rama especial.')
  items.append({'codigo':code,'denominacion':re.sub(r'\s+',' ',heading[1]),'procedimiento':procedure,'condiciones':conditions,
                'paginas':[{'pagina_pdf':p,'sha256_texto':sha((pdf.pages[p-1].extract_text() or '').encode('utf-8'))} for p in range(start,end+1)],
                'alertas':alerts,'revision_humana':None,'apta_para_reglas':False})
 return {'version':'0.1.0','fecha':'2026-11-01','corte_documental':'2026-10-31',
         'fuente':{k:source[k] for k in ('name','instrument_id','source_url','local_path','sha256')},
         'publicacion_acto':{'fecha':'2026-04-08','url':'https://busquedas.elperuano.pe/dispositivo/NL/2503213-1'},
         'eficacia':{'desde':None,'hasta':None,'estado':'cadena_por_disposicion_pendiente'},
         'alcance':'Índice de fichas y páginas completas; candidatas según datos declarados. No consolidación jurídica ni evaluación exhaustiva de cada requisito.',
         'fichas':items}

if __name__=='__main__':
 import logging
 logging.getLogger('pypdf').setLevel(logging.ERROR)
 result=construir();guardar(ROOT/'normativa/indice-tupa.v0.1.json',result)
 print(json.dumps({'fichas':len(result['fichas']),'paginas':sum(len(f['paginas']) for f in result['fichas'])}))
