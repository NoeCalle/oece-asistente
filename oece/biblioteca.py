"""Biblioteca unificada local y citas por página de originales manifestados."""
from pathlib import Path
from contextlib import closing
import os
import sqlite3
import tempfile

from .comun import ROOT, bytes_json, dentro, leer, sha
from .lectura import leer_documento

MANIFIESTOS=['normativa/manifiesto-descargas-2026-10-29.json','normativa/manifiesto-continuacion-2026-10-30.json',
             'normativa/manifiesto-ampliacion-2026-10-30.json','normativa/manifiesto-cierre-piloto-2026-10-30.json',
             'normativa/manifiesto-operacion-2026-10-31.json']

def fuentes():
    return [f for m in MANIFIESTOS for f in leer(ROOT/m)['archivos']]

def validar_normas(normas):
    if not isinstance(normas,list) or len(normas)>100: raise ValueError('Lista de normas inválida')
    by_name={f['name']:f for f in fuentes()};codes=set()
    for n in normas:
        code=n.get('codigo','')
        if not isinstance(code,str) or not code.startswith('N-') or not code[2:].isalnum() or code in codes:
            raise ValueError('Código normativo único requerido: N-identificador')
        codes.add(code)
        item=by_name.get(n.get('archivo'))
        if not item or n.get('sha256')!=item['sha256'] or n.get('url')!=item['source_url']:
            raise ValueError('Fuente normativa fuera de los originales manifestados')
        path=dentro(ROOT,item['local_path'])
        if sha(path.read_bytes())!=item['sha256']: raise ValueError('Original normativo alterado')
        from pypdf import PdfReader
        if path.suffix.lower()!='.pdf': raise ValueError('Cita normativa adicional: usar original PDF con página')
        pdf=PdfReader(path);page=n.get('pagina_pdf')
        if type(page) is not int or not 1<=page<=len(pdf.pages): raise ValueError('Página normativa fuera del original')
        text=pdf.pages[page-1].extract_text() or ''
        quote=n.get('cita')
        if not isinstance(quote,str) or not quote.strip() or quote not in text: raise ValueError('Cita normativa no contenida literalmente en la página')
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
                p=dentro(ROOT,f['local_path'])
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
        return [{'ubicacion':r[0],'texto':r[1],'alertas':json.loads(r[2]),'fuente':json.loads(r[3]),'alcance':'recuperacion_no_acredita_vigencia'} for r in rows]
