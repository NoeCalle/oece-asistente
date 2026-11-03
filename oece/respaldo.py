"""Respaldo local íntegro y restauración exclusiva de un expediente."""
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import shutil
import tempfile
import time
import zipfile

from .comun import dentro,leer,sha,bytes_json

MAX_BYTES=1_000_000_000
MAX_FILES=5000
MANIFEST='respaldo-oece.json'


def _files(root):
    result=[]
    for directory,dirs,names in os.walk(root,followlinks=False):
        for name in dirs:dentro(root,(Path(directory)/name).relative_to(root))
        for name in names:
            path=Path(directory)/name;rel=path.relative_to(root).as_posix();safe=dentro(root,rel)
            if safe.is_file():result.append((rel,safe))
    return sorted(result)


def _nombre(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or name.startswith('/'):
        raise ValueError('Nombre inseguro en respaldo')
    p=PurePosixPath(name)
    if any(x in ('','.','..') or x.endswith((' ','.')) or any(c in x for c in '<>"|?*') for x in name.split('/')):raise ValueError('Ruta insegura en respaldo')
    reserved={'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}
    if any(x.split('.')[0].upper() in reserved for x in p.parts):raise ValueError('Nombre reservado en respaldo')
    return p


def crear(caso,archivo):
    caso=Path(caso).resolve();archivo=Path(archivo).resolve()
    if not (caso/'expediente.json').is_file():raise ValueError('Expediente no encontrado')
    if archivo==caso or caso in archivo.parents:raise ValueError('Guardar respaldo fuera del expediente')
    candidates=[];total=0
    for rel,safe in _files(caso):
        _nombre(rel)
        if rel==MANIFEST:raise ValueError('Nombre de manifiesto reservado')
        total+=safe.stat().st_size
        if total>MAX_BYTES or len(candidates)>=MAX_FILES:raise ValueError('Respaldo supera límite de 1 GB o 5000 archivos')
        candidates.append((rel,safe))
    archivo.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive: nunca reemplaza un respaldo anterior.
    created=False
    try:
        out=archivo.open('xb');created=True
        with out,zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,allowZip64=True) as z:
            records={}
            for rel,path in candidates:
                raw=path.read_bytes();records[rel]={'sha256':sha(raw),'bytes':len(raw)};z.writestr(rel,raw)
            # Comprobar estabilidad de entradas/entregas durante la captura.
            final=[rel for rel,_ in _files(caso)]
            if final!=[r for r,_ in candidates]:raise ValueError('Expediente cambió durante respaldo')
            for rel,path in candidates:
                if sha(path.read_bytes())!=records[rel]['sha256']:raise ValueError('Archivo cambió durante respaldo')
            z.writestr(MANIFEST,bytes_json({'version':'1.0.0','expediente':leer(caso/'expediente.json')['id'],'archivos':records,'alcance':'Contenido de esta carpeta de expediente; no incorpora configuraciones de cuentas ni memoria externa'}))
    except Exception:
        if created:archivo.unlink(missing_ok=True)
        raise
    result=validar(archivo)
    with archivo.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'archivo':str(archivo),'sha256':digest,'archivos':result['archivos'],'bytes_originales':total}


def validar(archivo):
    with zipfile.ZipFile(archivo) as z:
        entries=z.infolist();names=[i.filename for i in entries]
        if len(names)!=len({n.casefold() for n in names}) or len(names)>MAX_FILES+1 or MANIFEST not in names:raise ValueError('Respaldo duplicado o sin manifiesto')
        if sum(i.file_size for i in entries)>MAX_BYTES+4_000_000:raise ValueError('Respaldo descomprimido fuera de límite')
        for item in entries:
            _nombre(item.filename)
            if item.is_dir() or ((item.external_attr>>16)&0o170000)==0o120000:raise ValueError('No se admiten directorios/enlaces en respaldo')
        if z.getinfo(MANIFEST).file_size>4_000_000:raise ValueError('Manifiesto demasiado grande')
        manifest=json.loads(z.read(MANIFEST));records=manifest.get('archivos')
        if manifest.get('version')!='1.0.0' or not isinstance(records,dict) or set(records)!=(set(names)-{MANIFEST}) or 'expediente.json' not in records:raise ValueError('Manifiesto incoherente')
        for name,record in records.items():
            digest=hashlib.sha256();size=0
            with z.open(name) as stream:
                while chunk:=stream.read(1_000_000):digest.update(chunk);size+=len(chunk)
            if digest.hexdigest()!=record.get('sha256') or size!=record.get('bytes'):raise ValueError('Archivo alterado en respaldo: '+name)
        if z.getinfo('expediente.json').file_size>4_000_000:raise ValueError('Ficha demasiado grande')
        config=json.loads(z.read('expediente.json'))
        if not isinstance(config,dict) or not config.get('id') or config['id']!=manifest.get('expediente'):raise ValueError('Identidad del expediente no coincide')
        return {'archivos':len(records),'expediente':manifest['expediente']}


def restaurar(archivo,destino):
    validated=validar(archivo);destino=Path(destino).resolve()
    if destino.exists():raise ValueError('El destino ya existe; elegir una carpeta nueva')
    parent=destino.parent;parent.mkdir(parents=True,exist_ok=True)
    temporary=Path(tempfile.mkdtemp(prefix='.restaurando-',dir=parent))
    try:
        dentro(temporary,'documentos').mkdir()
        with zipfile.ZipFile(archivo) as z:
            if len(z.infolist())>MAX_FILES+1 or z.getinfo(MANIFEST).file_size>4_000_000:raise ValueError('Respaldo cambió o excede límite')
            records=json.loads(z.read(MANIFEST))['archivos']
            if len(records)>MAX_FILES:raise ValueError('Demasiadas entradas')
            total_written=0
            for name,record in records.items():
                target=dentro(temporary,_nombre(name));target.parent.mkdir(parents=True,exist_ok=True)
                written=0
                with z.open(name) as source,target.open('xb') as out:
                    while chunk:=source.read(1_000_000):
                        written+=len(chunk);total_written+=len(chunk)
                        if written>record['bytes'] or total_written>MAX_BYTES:raise ValueError('Entrada creció durante restauración')
                        out.write(chunk)
        # Segundo cotejo antes de publicar; también detecta un ZIP cambiado entre pasos.
        with zipfile.ZipFile(archivo) as z:records=json.loads(z.read(MANIFEST))['archivos']
        for name,record in records.items():
            if sha(dentro(temporary,name).read_bytes())!=record['sha256']:raise ValueError('Restauración no coincide')
        if destino.exists():raise ValueError('El destino apareció durante restauración')
        for attempt in range(5):
            try:
                temporary.rename(destino);break
            except PermissionError:
                if destino.exists() or attempt==4:raise
                time.sleep(.15*(2**attempt))
    finally:
        if temporary.exists():
            if temporary.resolve().parent!=parent.resolve() or not temporary.name.startswith('.restaurando-'):raise ValueError('Temporal fuera del destino')
            shutil.rmtree(temporary)
    return {'destino':str(destino),'archivos':validated['archivos'],'expediente':validated['expediente'],'original_conservado':True}
