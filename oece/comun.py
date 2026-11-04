import hashlib
import json
import os
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

def data_dir():
    """Raíz de datos privados, independiente del sistema operativo y del checkout."""
    value = os.environ.get('OECE_DATA_DIR', './data')
    if not value.strip():
        raise ValueError('OECE_DATA_DIR no puede estar vacía')
    return Path(value).expanduser().resolve()

def normalizar_ruta_relativa(value):
    """Ruta relativa portátil con /; rechaza escapes, UNC y unidades Windows."""
    if not isinstance(value, (str, PurePath)) or not str(value) or '\x00' in str(value):
        raise ValueError('Ruta relativa inválida')
    raw = str(value).replace('\\', '/')
    portable = PurePosixPath(raw)
    if (portable.is_absolute() or PureWindowsPath(raw).drive
            or '..' in portable.parts or str(portable) == '.'):
        raise ValueError('Se requiere una ruta relativa interior')
    return portable.as_posix()


def normalizar_registro_rutas(value):
    """Normaliza solo claves de rutas relativas, sin alterar citas ni hashes."""
    keys = {'local_path', 'derivado_local', 'ruta_relativa', 'relative_path',
            'source_relative_path', 'output_relative_path'}
    if isinstance(value, dict):
        return {key: (normalizar_ruta_relativa(item)
                      if key in keys and isinstance(item, str)
                      else normalizar_registro_rutas(item))
                for key, item in value.items()}
    if isinstance(value, list):
        return [normalizar_registro_rutas(item) for item in value]
    return value


def ruta_original(local_path):
    """Busca originales privados y en la estructura histórica del repositorio."""
    relative = normalizar_ruta_relativa(local_path)
    primary = dentro(data_dir(), relative)
    if primary.is_file():
        return primary
    legacy = dentro(ROOT, relative)
    return legacy if legacy.is_file() else primary

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
        for attempt in range(5):
            try:
                os.replace(name, path)
                break
            except PermissionError:
                if attempt==4:raise
                time.sleep(.1*(2**attempt))
    finally:
        if Path(name).exists():
            Path(name).unlink()

def dentro(root, relative):
    root = Path(root).resolve()
    candidate = Path(normalizar_ruta_relativa(relative))
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
