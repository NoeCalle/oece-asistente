"""Migración conservadora de rutas relativas en índices privados JSON/SQLite.

No modifica expedientes ni originales normativos. Para evitar corrupción,
detener el panel y otros escritores antes de ejecutar la migración.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile

from .comun import data_dir, normalizar_registro_rutas, normalizar_ruta_relativa


JSON_COLUMNS = {'metadata', 'summary', 'locator', 'datos', 'fuente', 'source',
                'origen_json', 'config', 'manifest'}
PATH_COLUMNS = {'local_path', 'derivado_local', 'ruta_relativa', 'relative_path',
                'source_relative_path', 'output_relative_path'}


def _q(name):
    return '"' + name.replace('"', '""') + '"'


def _backup(path):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    candidate = path.with_name(path.name + f'.pre-rutas-{stamp}.bak')
    suffix = 0
    while candidate.exists():
        suffix += 1
        candidate = path.with_name(path.name + f'.pre-rutas-{stamp}-{suffix}.bak')
    return candidate


def _atomic_text(path, new_text, preview=False):
    if preview:
        return None
    backup = _backup(path)
    fd, tmp = tempfile.mkstemp(prefix='.rutas-', suffix=path.suffix, dir=path.parent)
    os.close(fd)
    try:
        Path(tmp).write_text(new_text, encoding='utf-8', newline='\n')
        shutil.copy2(path, backup)
        os.replace(tmp, path)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()
    return str(backup)


def migrar_json(path, preview=False):
    path = Path(path)
    original = path.read_text(encoding='utf-8-sig')
    old = json.loads(original)
    new = normalizar_registro_rutas(old)
    if new == old:
        return {'archivo': str(path), 'tipo': 'json', 'cambios': 0}
    new_text = json.dumps(new, ensure_ascii=False, indent=2) + '\n'
    backup = _atomic_text(path, new_text, preview)
    return {'archivo': str(path), 'tipo': 'json', 'cambios': 1,
            'respaldo': backup, 'simulacion': bool(preview)}


def _table_rows(conn):
    for name, definition in conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"):
        # Solo columnas de rutas o JSON; excluir tablas virtuales y FTS5.
        if name.startswith('sqlite_') or 'VIRTUAL TABLE' in definition.upper():
            continue
        columns = [row[1] for row in conn.execute(f'PRAGMA table_info({_q(name)})')]
        for col in columns:
            if col in JSON_COLUMNS or col in PATH_COLUMNS:
                yield name, col


def _transform(value, column):
    if not isinstance(value, str):
        return value
    if column in PATH_COLUMNS:
        return normalizar_ruta_relativa(value)
    try:
        old = json.loads(value)
    except (ValueError, TypeError):
        return value
    new = normalizar_registro_rutas(old)
    return (json.dumps(new, ensure_ascii=False, separators=(',', ':'))
            if new != old else value)


def migrar_sqlite(path, preview=False):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError('Índice SQLite inexistente o enlace no admitido')
    if any(Path(str(path) + ext).exists() for ext in ('-wal', '-shm', '-journal')):
        raise ValueError('Detener procesos y hacer checkpoint de SQLite antes de migrar')
    fd, tmp = tempfile.mkstemp(prefix='.rutas-', suffix='.sqlite', dir=path.parent)
    os.close(fd)
    try:
        source = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
        try:
            target = sqlite3.connect(tmp)
            try:
                source.backup(target)
                target.commit()
            finally:
                target.close()
        finally:
            source.close()
        conn = sqlite3.connect(tmp)
        try:
            total = 0
            for table, column in list(_table_rows(conn)):
                query = f'SELECT rowid, {_q(column)} FROM {_q(table)}'
                try:
                    rows = conn.execute(query).fetchall()
                except sqlite3.OperationalError:
                    continue
                for rowid, value in rows:
                    updated = _transform(value, column)
                    if updated == value:
                        continue
                    conn.execute(
                        f'UPDATE {_q(table)} SET {_q(column)}=? WHERE rowid=?',
                        (updated, rowid))
                    total += 1
            if conn.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('La migración dejó un índice SQLite inválido')
            if preview:
                conn.rollback()
            else:
                conn.commit()
        finally:
            conn.close()
        result = {'archivo': str(path), 'tipo': 'sqlite', 'cambios': total,
                  'simulacion': bool(preview)}
        if total and not preview:
            backup = _backup(path)
            shutil.copy2(path, backup)
            os.replace(tmp, path)
            result['respaldo'] = str(backup)
        return result
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()


def migrar(root=None, preview=False):
    """Migra índices existentes en OECE_DATA_DIR/normativa o ruta explícita."""
    root = Path(root) if root is not None else data_dir() / 'normativa'
    if not root.exists():
        return {'raiz': str(root), 'archivos': [], 'cambios': 0}
    if root.is_symlink():
        raise ValueError('No migrar directorios enlazados')
    if root.is_file():
        candidates = [root]
    else:
        candidates = [p for p in sorted(root.rglob('*')) if p.is_file()
                      and not p.is_symlink() and not ({'originales', 'ocr'} & set(p.relative_to(root).parts))]
    results = []
    for item in candidates:
        if item.suffix.lower() in ('.sqlite', '.db'):
            results.append(migrar_sqlite(item, preview))
        elif item.suffix.lower() == '.json' and (
                'indice' in item.name.lower() or 'manifiesto' in item.name.lower()
                or 'indices' in item.parts or 'index' in item.parts):
            results.append(migrar_json(item, preview))
    return {'raiz': str(root), 'archivos': results,
            'cambios': sum(x['cambios'] for x in results), 'simulacion': bool(preview)}
