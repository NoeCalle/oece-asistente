"""Descarga únicamente fuentes NORMATIVAS públicas manifestadas para CI.

No descarga, publica ni reconstruye expedientes laborales. Comprueba tamaño y
SHA-256 antes de guardar el original bajo OECE_DATA_DIR; evita archivos parciales.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path
import json
import os
import tempfile
import time
from urllib.request import Request, urlopen

from oece.comun import ROOT, data_dir, dentro, ruta_original

MANIFESTS = [
    'normativa/manifiesto-descargas-2026-10-29.json',
    'normativa/manifiesto-continuacion-2026-10-30.json',
    'normativa/manifiesto-ampliacion-2026-10-30.json',
    'normativa/manifiesto-cierre-piloto-2026-10-30.json',
    'normativa/manifiesto-operacion-2026-10-31.json',
    'normativa/manifiesto-procedimientos-2026-10-31.json',
]
USER_AGENT = 'Mozilla/5.0 OECE-Assistant-CI/1.0'


def descargar(item):
    relative = str(item['local_path']).replace('\\', '/')
    target = dentro(data_dir(), relative)
    if target.is_file() and target.stat().st_size == item['bytes'] and sha256(target.read_bytes()).hexdigest() == item['sha256']:
        return item['name'], 'presente'
    target.parent.mkdir(parents=True, exist_ok=True)
    previous = None
    for attempt in range(3):
        try:
            req = Request(item['source_url'], headers={'User-Agent': USER_AGENT, 'Accept': '*/*'})
            with urlopen(req, timeout=60) as response:
                chunks = []
                size = 0
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    size += len(block)
                    if size > 65_000_000:
                        raise ValueError('Fuente supera límite de 65 MB')
                    chunks.append(block)
            raw = b''.join(chunks)
            if len(raw) != item['bytes'] or sha256(raw).hexdigest() != item['sha256']:
                raise ValueError('Fuente cambió: bytes o SHA-256 no coinciden')
            fd, name = tempfile.mkstemp(prefix='.descarga-', dir=target.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw)
                os.replace(name, target)
            finally:
                if Path(name).exists():
                    Path(name).unlink()
            return item['name'], 'descargado'
        except (OSError, ValueError) as error:
            previous = error
            time.sleep(attempt + 1)
    raise RuntimeError(f'{item["name"]}: {previous}')


def main():
    documents = [f for name in MANIFESTS for f in json.loads((ROOT / name).read_text(encoding='utf-8-sig'))['archivos']]
    unique = {f['sha256']: f for f in documents}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(descargar, item): item['name'] for item in unique.values()}
        errors = []
        for future in as_completed(futures):
            try:
                name, state = future.result()
                print(state, name, flush=True)
            except Exception as error:
                errors.append(str(error))
        if errors:
            raise RuntimeError(f'{len(errors)} fuente(s) pública(s) no recuperada(s):\n' + '\n'.join(errors))
    print(f'Fuentes normativas verificadas: {len(unique)}')


if __name__ == '__main__':
    main()
