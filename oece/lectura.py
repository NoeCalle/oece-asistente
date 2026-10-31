"""Lectura local y OCR por página con caché, límites y procedencia."""
from html.parser import HTMLParser
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile

from .comun import ROOT, guardar, leer, sha

VERSION = '1.0.0'
IMPLEMENTACION = sha(Path(__file__).read_bytes())

def aplicar_cotejos(documents, records):
    """Incorpora transcripción visual declarada conservando texto OCR y autoría.

    Valida procedencia, no autentica al revisor ni comprueba que miró la imagen.
    Solo el coordinador que la haya inspeccionado debe registrar este cotejo.
    """
    from datetime import datetime
    if not isinstance(records,list) or len(records)>2000: raise ValueError('Cotejos inválidos')
    index={(d['id'],b['ubicacion']):(d,b) for d in documents for b in d['fragmentos']}
    seen=set()
    for item in records:
        key=(item.get('documento'),item.get('ubicacion'))
        if key in seen or key not in index: raise ValueError('Cotejo duplicado o sin fragmento')
        seen.add(key);d,b=index[key]
        if 'ocr_sin_cotejo_visual' not in b['alertas'] or not b.get('imagen_sha256'):
            raise ValueError('El cotejo requiere un fragmento OCR con imagen identificada')
        if item.get('sha256')!=d['sha256'] or item.get('imagen_sha256')!=b['imagen_sha256']:
            raise ValueError('Cotejo de otra fuente o imagen')
        if item.get('tipo_autor') not in ('asistente_ia','humano') or not item.get('autor') or not isinstance(item.get('transcripcion'),str) or not item['transcripcion'].strip():
            raise ValueError('Cotejo sin transcripción o autor identificado')
        try:
            if datetime.fromisoformat(item['fecha']).tzinfo is None: raise ValueError()
        except (KeyError,TypeError,ValueError): raise ValueError('Cotejo sin fecha y zona horaria')
        b['texto_ocr_original']=b['texto'];b['texto']=item['transcripcion'];b['cotejo_declarado']=item
        b['alertas']=[a for a in b['alertas'] if a!='ocr_sin_cotejo_visual']

class TextoHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.hidden = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag in ('p', 'div', 'tr', 'li', 'br', 'h1', 'h2', 'h3'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

def binario(nombre):
    variable = 'OECE_' + nombre.upper().replace('.', '_')
    configured = os.environ.get(variable)
    if configured and Path(configured).is_file():
        return configured
    found = shutil.which(nombre)
    if found:
        return found
    base = Path(sys.executable).resolve().parent.parent / 'native/poppler/Library/bin'
    if (base / nombre).is_file():
        return str(base / nombre)
    raise ValueError(f'No se encontró {nombre}; configurar {variable}')

def ocr_imagen(image, cache, source_sha, page, timeout=45):
    image_sha = sha(image.read_bytes())
    output = cache / f'ocr-{page}.json'
    if output.exists():
        previous = leer(output)
        if previous.get('source_sha256') == source_sha and previous.get('image_sha256') == image_sha:
            return previous
    job = cache / f'trabajo-{page}.json'
    guardar(job, {'source_sha256': source_sha, 'source_name': image.name,
                 'pages': [{'image_path': str(image.resolve()), 'image_sha256': image_sha,
                            'page_pdf': page, 'output_path': str(output.resolve())}]})
    powershell = shutil.which('powershell.exe')
    if not powershell:
        raise ValueError('OCR Windows no disponible en este equipo')
    result = subprocess.run([powershell, '-NoProfile', '-File', str(ROOT / 'scripts/ocr_windows.ps1'),
                            '-Root', str(cache.resolve()), '-Job', str(job.resolve())],
                           capture_output=True, timeout=timeout, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode or not output.exists():
        raise ValueError('Motor OCR no completó esta página')
    data = leer(output)
    if data.get('source_sha256') != source_sha or data.get('image_sha256') != image_sha:
        raise ValueError('Procedencia OCR incoherente')
    return data

def leer_documento(path, cache, usar_ocr=True, timeout=45):
    path, cache = Path(path), Path(cache)
    raw = path.read_bytes()
    if len(raw) > 30_000_000:
        raise ValueError('Archivo supera 30 MB')
    source_sha = sha(raw)
    cache = cache / source_sha / VERSION
    cache.mkdir(parents=True, exist_ok=True)
    saved = cache / ('lectura-ocr.json' if usar_ocr else 'lectura-digital.json')
    if saved.exists():
        result = leer(saved)
        if result.get('sha256') == source_sha and result.get('implementacion_sha256') == IMPLEMENTACION and not result.get('reintentar'):
            return result
    blocks, warnings = [], []
    def add(loc, text, alerts=None, **extra):
        blocks.append({'ubicacion': loc, 'texto': text, 'alertas': alerts or [], **extra})
    deadline=time.monotonic()+120
    pending_attempts=0
    def recognize(image, number):
        nonlocal pending_attempts
        try:
            cached=cache/f'ocr-{number}.json'
            if not cached.exists():
                if pending_attempts>=10 or time.monotonic()>=deadline:
                    raise ValueError('Límite de OCR por lote; reanudar en siguiente ejecución')
                pending_attempts+=1
            data = ocr_imagen(image, cache, source_sha, number, max(1,min(timeout,int(deadline-time.monotonic()))))
            add(f'pagina:{number}', data['text'], ['ocr_sin_cotejo_visual'],
                motor='Windows.Media.Ocr', imagen_sha256=data['image_sha256'], confianza=None)
        except (ValueError, subprocess.TimeoutExpired) as error:
            add(f'pagina:{number}', '', ['ocr_pendiente'], motor='OCR', confianza=None)
            warnings.append(f'Página {number}: {type(error).__name__}; puede reintentarse')
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        from pypdf import PdfReader
        pdf = PdfReader(path)
        if pdf.is_encrypted:
            raise ValueError('PDF protegido; se necesita una copia legible')
        if len(pdf.pages) > 500:
            raise ValueError('PDF supera 500 páginas por archivo')
        for n, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ''
            if len(text.strip()) >= 50 or not usar_ocr:
                add(f'pagina:{n}', text, [] if len(text.strip()) >= 50 else ['lectura_insuficiente'], motor='pypdf')
                continue
            image = cache / f'pagina-{n}.png'
            try:
                if not (cache/f'ocr-{n}.json').exists() and (pending_attempts>=10 or time.monotonic()>=deadline):
                    add(f'pagina:{n}',text,['ocr_pendiente'],motor='pypdf')
                    continue
                if not image.exists():
                    subprocess.run([binario('pdftoppm.exe'), '-f', str(n), '-l', str(n), '-singlefile',
                                    '-scale-to', '2200', '-png', str(path.resolve()), str(image.with_suffix(''))],
                                   capture_output=True, check=True, timeout=timeout,
                                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                recognize(image, n)
            except (ValueError, subprocess.SubprocessError):
                add(f'pagina:{n}', text, ['ocr_pendiente'], motor='pypdf')
                warnings.append(f'Página {n}: conversión pendiente; puede reintentarse')
    elif suffix == '.docx':
        with zipfile.ZipFile(path) as z:
            if sum(i.file_size for i in z.infolist()) > 120_000_000:
                raise ValueError('Paquete Word descomprimido demasiado grande')
        from docx import Document
        from docx.table import Table
        doc = Document(path)
        def walk(container, prefix):
            for n, block in enumerate(container.iter_inner_content(), 1):
                loc = f'{prefix}/bloque:{n}'
                if isinstance(block, Table):
                    seen = set()
                    for rn, row in enumerate(block.rows, 1):
                        for cn, cell in enumerate(row.cells, 1):
                            if cell._tc not in seen:
                                seen.add(cell._tc)
                                walk(cell, f'{loc}/fila:{rn}/celda:{cn}')
                elif block.text.strip():
                    add(loc, block.text, motor='python-docx')
        walk(doc, 'cuerpo')
        seen = set()
        for n, sec in enumerate(doc.sections, 1):
            for name in ('header', 'footer', 'first_page_header', 'first_page_footer', 'even_page_header', 'even_page_footer'):
                part = getattr(sec, name)
                if part._element not in seen:
                    seen.add(part._element)
                    walk(part, f'seccion:{n}/{name}')
        warnings.append('Word: imágenes, cuadros de texto, notas y cambios controlados requieren inspección visual')
    elif suffix in ('.png', '.jpg', '.jpeg', '.tif', '.tiff'):
        from PIL import Image
        with Image.open(path) as image:
            if image.width * image.height > 40_000_000:
                raise ValueError('Imagen demasiado grande')
            if getattr(image, 'n_frames', 1) > 1:
                raise ValueError('Imagen multipágina: convertir a PDF para conservar todas las páginas')
            target = cache / 'imagen.png'
            image.thumbnail((2200, 2200))
            image.convert('RGB').save(target)
        if usar_ocr:
            recognize(target, 1)
        else:
            add('pagina:1', '', ['ocr_pendiente'])
    elif suffix in ('.txt', '.csv', '.md', '.html', '.htm'):
        text = raw.decode('utf-8-sig')
        if suffix in ('.html', '.htm'):
            parser = TextoHTML()
            parser.feed(text)
            text = ''.join(parser.parts)
        for n, line in enumerate(text.splitlines(), 1):
            if line.strip():
                add(f'linea:{n}', line)
    elif suffix == '.xlsx':
        # Lectura XML local; no se ejecutan fórmulas, macros ni conexiones.
        import xml.etree.ElementTree as ET
        ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        with zipfile.ZipFile(path) as z:
            if sum(i.file_size for i in z.infolist()) > 120_000_000:
                raise ValueError('Libro descomprimido demasiado grande')
            strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
            for sheet in sorted(n for n in z.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')):
                for c in ET.fromstring(z.read(sheet)).findall('.//m:c', ns):
                    v, formula = c.find('m:v', ns), c.find('m:f', ns)
                    if v is None and formula is None and c.find('m:is',ns) is None:
                        continue
                    text = v.text or '' if v is not None else ''.join(c.itertext())
                    if c.get('t') == 's':
                        text = strings[int(text)]
                    add(f'{sheet}/celda:{c.get("r")}', text, ['formula_no_recalculada'] if formula is not None else [])
        warnings.append('Excel: valores almacenados; fórmulas sin recalcular; fechas y formatos requieren cotejo')
    else:
        raise ValueError(f'Formato {suffix} no legible directamente; conservar y convertir a PDF o DOCX')
    if sha(path.read_bytes()) != source_sha:
        raise ValueError('El documento cambió durante la lectura')
    result = {'sha256': source_sha, 'lector_version': VERSION, 'implementacion_sha256':IMPLEMENTACION, 'fragmentos': blocks,
              'advertencias': warnings, 'reintentar': any('ocr_pendiente' in b['alertas'] for b in blocks)}
    guardar(saved, result)
    return result
