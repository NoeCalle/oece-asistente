import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def bytes_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')

def leer(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def guardar(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.oece-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(bytes_json(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if Path(name).exists():
            Path(name).unlink()

def dentro(root, relative):
    root = Path(root).resolve()
    candidate = Path(relative)
    if candidate.is_absolute() or '..' in candidate.parts:
        raise ValueError('Se requiere una ruta relativa interior')
    path = root / candidate
    # Rechazar symlinks/junctions, incluso si apuntan a otro lugar del caso.
    for part in [path, *path.parents]:
        if part == root:
            break
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('No se admiten enlaces ni uniones de carpetas')
    resolved = path.resolve()
    if root not in resolved.parents:
        raise ValueError('Ruta fuera de la carpeta autorizada')
    return resolved

def csv_seguro(value):
    value = str(value)
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else value
