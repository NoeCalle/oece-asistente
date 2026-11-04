"""Biblioteca unificada local y citas por página de originales manifestados."""
from pathlib import Path
from contextlib import closing
import os
import sqlite3
import tempfile

from .comun import ROOT, bytes_json, data_dir, leer, normalizar_registro_rutas, ruta_original, sha
from .lectura import leer_documento

MANIFIESTOS=['normativa/manifiesto-descargas-2026-10-29.json','normativa/manifiesto-continuacion-2026-10-30.json',
             'normativa/manifiesto-ampliacion-2026-10-30.json','normativa/manifiesto-cierre-piloto-2026-10-30.json',
             'normativa/manifiesto-operacion-2026-10-31.json','normativa/manifiesto-procedimientos-2026-10-31.json']

def fuentes():
    return [f for m in MANIFIESTOS for f in normalizar_registro_rutas(leer(ROOT/m))['archivos']]

def leer_fuente(archivo,pagina=None,ubicacion=None):
    from io import BytesIO
    source=next((s for s in fuentes() if s['name']==archivo),None)
    if source is None:raise ValueError('Fuente no manifestada')
    path=ruta_original(source['local_path']);raw=path.read_bytes()
    if sha(raw)!=source['sha256']:raise ValueError('Original normativo alterado')
    if path.suffix.lower()=='.pdf':
        from pypdf import PdfReader
        pdf=PdfReader(BytesIO(raw))
        if ubicacion is not None or type(pagina) is not int or not 1<=pagina<=len(pdf.pages):raise ValueError('Página normativa fuera del original o ubicación ambigua')
        text=pdf.pages[pagina-1].extract_text() or '';loc='pagina:'+str(pagina)
    elif path.suffix.lower()=='.docx':
        if pagina is not None or not isinstance(ubicacion,str) or not ubicacion:raise ValueError('Anexo Word requiere ubicación de bloque/celda, sin página PDF')
        result=leer_documento(path,data_dir()/'catalogo-lecturas',False)
        if result['sha256']!=source['sha256']:raise ValueError('Anexo normativo cambió durante lectura')
        block=next((b for b in result['fragmentos'] if b['ubicacion']==ubicacion),None)
        if block is None:raise ValueError('Ubicación no contenida en el anexo Word')
        text=block['texto'];loc=ubicacion
    else:raise ValueError('Fuente adicional requiere PDF digital o DOCX con localizador')
    if len(text)>200_000:raise ValueError('Fragmento normativo demasiado extenso')
    return {'fuente':source,'ubicacion':loc,'texto':text,'alcance':'Lectura digital; no acredita vigencia ni revisión visual de tablas o imágenes.'}

def validar_normas(normas):
    if not isinstance(normas,list) or len(normas)>100: raise ValueError('Lista de normas inválida')
    by_name={f['name']:f for f in fuentes()};codes=set()
    for n in normas:
        if not isinstance(n,dict):raise ValueError('Cada cita normativa debe ser un objeto')
        code=n.get('codigo','')
        if not isinstance(code,str) or not code.startswith('N-') or not code[2:].isalnum() or code in codes:
            raise ValueError('Código normativo único requerido: N-identificador')
        codes.add(code)
        item=by_name.get(n.get('archivo'))
        if not item or n.get('sha256')!=item['sha256'] or n.get('url')!=item['source_url']:
            raise ValueError('Fuente normativa fuera de los originales manifestados')
        text=leer_fuente(item['name'],n.get('pagina_pdf'),n.get('ubicacion'))['texto']
        quote=n.get('cita')
        if not isinstance(quote,str) or not quote.strip() or quote not in text: raise ValueError('Cita normativa no contenida literalmente en la ubicación')
        if not n.get('disposicion') or not n.get('autor') or not n.get('criterio'):
            raise ValueError('La cita normativa necesita disposición, autor y criterio de aplicabilidad')
    return normas

def construir(output,cache):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(suffix='.sqlite',dir=output.parent);os.close(fd)
    counts={'documentos':0,'fragmentos':0,'con_texto':0,'pendientes':[]}
    try:
        with closing(sqlite3.connect(name)) as c, c:
            c.executescript("CREATE TABLE fuentes(id TEXT PRIMARY KEY,metadata TEXT); CREATE TABLE fragmentos(id INTEGER PRIMARY KEY,fuente TEXT,ubicacion TEXT,texto TEXT,alertas TEXT); CREATE VIRTUAL TABLE buscar USING fts5(id UNINDEXED,texto,tokenize='unicode61 remove_diacritics 2');")
            for f in fuentes():
                p=ruta_original(f['local_path'])
                if sha(p.read_bytes())!=f['sha256']: raise ValueError('Fuente alterada: '+f['name'])
                if c.execute('SELECT 1 FROM fuentes WHERE id=?',(f['sha256'],)).fetchone(): continue
                c.execute('INSERT INTO fuentes VALUES(?,?)',(f['sha256'],bytes_json(f).decode()))
                counts['documentos']+=1
                try: result=leer_documento(p,cache,usar_ocr=False)
                except ValueError:
                    counts['pendientes'].append(f['name']);continue
                for b in result['fragmentos']:
                    cursor=c.execute('INSERT INTO fragmentos(fuente,ubicacion,texto,alertas) VALUES(?,?,?,?)',
                                     (f['sha256'],b['ubicacion'],b['texto'],bytes_json(b['alertas']).decode()))
                    c.execute('INSERT INTO buscar(id,texto) VALUES(?,?)',(cursor.lastrowid,b['texto']))
                    counts['fragmentos']+=1;counts['con_texto']+=bool(b['texto'].strip())
                if any(b['alertas'] for b in result['fragmentos']): counts['pendientes'].append(f['name'])
            c.execute('CREATE TABLE resumen(datos TEXT)');c.execute('INSERT INTO resumen VALUES(?)',(bytes_json(counts).decode(),))
        os.replace(name,output)
    finally:
        if Path(name).exists(): Path(name).unlink()
    return counts

def buscar(database,query,limit=10):
    if not query.strip() or not 1<=limit<=100: raise ValueError('Consulta o límite inválido')
    expression=' AND '.join('"'+t.replace('"','""')+'"' for t in query.split())
    import json
    with closing(sqlite3.connect(Path(database).resolve().as_uri()+'?mode=ro',uri=True)) as c:
        rows=c.execute('SELECT f.ubicacion,f.texto,f.alertas,n.metadata FROM buscar b JOIN fragmentos f ON f.id=b.id JOIN fuentes n ON n.id=f.fuente WHERE buscar MATCH ? ORDER BY rank LIMIT ?',(expression,limit))
        return [{'ubicacion':r[0],'texto':r[1],'alertas':json.loads(r[2]),'fuente':normalizar_registro_rutas(json.loads(r[3])),'alcance':'recuperacion_no_acredita_vigencia'} for r in rows]
