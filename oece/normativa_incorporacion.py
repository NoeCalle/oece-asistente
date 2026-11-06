"""Incorpora un original normativo adicional verificado a OECE_DATA_DIR.

No usa claves ni APIs de IA. Solo descarga de la URL oficial fijada en el
catálogo público o registra una copia local marcada pendiente de cotejo.
Las nuevas fuentes no sustituyen las normas anteriores.
"""
from contextlib import closing
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import os
import re
import sqlite3
import tempfile

from pypdf import PdfReader

from .comun import ROOT, data_dir, dentro, guardar, leer, sha
from .biblioteca import fuentes

LIMIT = 15_000_000
CATALOG = ROOT / "rules/fuentes-transversales.v1.json"
PRIVATE_MANIFEST = "normativa/manifiesto-adicionales.json"


def catalogo():
    data = leer(CATALOG)
    if data.get("version") != "fuentes-transversales-v1":
        raise ValueError("Catálogo de normas transversales no compatible")
    return data["instrumentos"]


def estado_norma(item):
    known = next((f for f in fuentes() if f.get("instrument_id") == item["id"]), None)
    if known is None:
        return {"incorporada_biblioteca": False, "original_verificado": False,
                "indice_actualizado": False, "motivo": "PDF original pendiente de importar en equipo autorizado"}
    from .comun import ruta_original
    path = ruta_original(known["local_path"])
    present = path.is_file()
    match = present and sha(path.read_bytes()) == known["sha256"]
    index = data_dir() / "normativa" / "indices" / "biblioteca-v1.sqlite"
    indexed = False
    if match and index.is_file():
        try:
            with closing(sqlite3.connect(index.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                indexed = db.execute("SELECT 1 FROM fuentes WHERE id=?", (known["sha256"],)).fetchone() is not None
        except sqlite3.Error:
            indexed = False
    return {"incorporada_biblioteca": True, "original_verificado": match,
            "indice_actualizado": indexed,
            "fuente_oficial_descargada": bool(known.get("verificacion", {}).get("descarga_desde_enlace_oficial")),
            "motivo": ("Original/index y SHA-256 coinciden; comprobar vigencia" if indexed
                       else "Original SHA-256 coincide; reconstruir índice" if match
                       else "Archivo ausente o hash distinto: no utilizar para citas")}


def _comprobar_pdf(raw, item):
    if not isinstance(raw, bytes) or not 100 < len(raw) <= LIMIT or not raw.startswith(b"%PDF"):
        raise ValueError("Se requiere un PDF válido de máximo 15 MB")
    try:
        reader = PdfReader(BytesIO(raw))
        if reader.is_encrypted or not 1 <= len(reader.pages) <= 100:
            raise ValueError("PDF cifrado o sin páginas válidas")
        text = " ".join((p.extract_text() or "") for p in reader.pages[:2])
    except Exception as exc:
        raise ValueError("No se pudo verificar estructura del PDF") from exc
    collapsed = re.sub(r"\s+", "", text).upper()
    # Cada fuente debe declarar marcadores propios: un PDF de otra resolución
    # no puede validarse mediante el texto fijo de RD 0016-2025.
    markers = item.get("marcadores_pdf")
    if (not isinstance(markers, list) or not markers or
            any(not isinstance(marker, str) or not marker.strip() for marker in markers)):
        raise ValueError("Catálogo sin marcadores PDF identificativos para esta norma")
    if not all(re.sub(r"\s+", "", marker).upper() in collapsed for marker in markers):
        raise ValueError("El PDF no se identifica con la norma y sus marcadores catalogados")
    return {"paginas": len(reader.pages), "identificacion_textual": True}


def _descargar(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "cdn.www.gob.pe":
        raise ValueError("La URL no pertenece al repositorio oficial permitido")
    req = Request(url, headers={"User-Agent": "OECE-Assistant-Normativa/1.0"})
    try:
        with urlopen(req, timeout=45) as response:
            final = urlparse(response.geturl())
            if final.scheme != "https" or final.netloc != "cdn.www.gob.pe":
                raise ValueError("La descarga redirigió fuera del dominio oficial")
            content = response.read(LIMIT + 1)
    except OSError as exc:
        raise ValueError("No se pudo descargar PDF oficial. Descárgalo desde el enlace del MEF y usa --archivo") from exc
    if len(content) > LIMIT:
        raise ValueError("Documento excede 15 MB")
    return content


def incorporar(instrumento, archivo=None, descargar=False):
    """Devuelve registro verificable; no actualiza reglas sin revisión profesional."""
    choices = {x["id"]: x for x in catalogo()}
    if instrumento not in choices:
        raise ValueError("Norma no pre-registrada en el catálogo")
    if (archivo is None) == (descargar is False):
        raise ValueError("Usar exactamente una opción: --archivo o --descargar")
    item = choices[instrumento]
    raw = _descargar(item["pdf_oficial"]) if descargar else Path(archivo).resolve().read_bytes()
    inspection = _comprobar_pdf(raw, item)
    digest = sha(raw)
    target = dentro(data_dir(), item["ruta_original"])
    private = dentro(data_dir(), PRIVATE_MANIFEST)
    previous = leer(private) if private.exists() else {"version": "adicionales-v1", "archivos": []}
    if previous.get("version") != "adicionales-v1" or not isinstance(previous.get("archivos"), list):
        raise ValueError("Manifiesto adicional no compatible")
    found = next((entry for entry in previous["archivos"]
                  if entry.get("instrument_id") == instrumento
                  or entry.get("name") == item["nombre_archivo"]), None)
    if found is not None:
        if found["sha256"] != digest:
            raise ValueError("La norma existente tiene otro SHA-256: preservar ambas versiones y revisar antes de sustituir")
        if not target.is_file() or sha(target.read_bytes()) != digest:
            raise ValueError("Original manifestado ausente o alterado")
        return {"estado": "ya_registrada", "archivo": str(target), "sha256": digest,
                "paginas": inspection["paginas"], "indice": "puede requerir reconstrucción"}
    # Conservar cualquier archivo previo no registrado; nunca sobrescribir originales.
    if target.exists():
        raise ValueError("Ya existe un archivo de igual nombre sin entrada de manifiesto")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".rd-dga-", suffix=".pdf", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if sha(Path(temp).read_bytes()) != digest:
            raise ValueError("Error de integridad al guardar la norma")
        os.rename(temp, target)
    finally:
        if Path(temp).exists():
            Path(temp).unlink()
    entry = {
        "name": item["nombre_archivo"], "instrument_id": instrumento,
        "source_url": item["pdf_oficial"], "source_page": item["fuente_oficial"],
        "local_path": item["ruta_original"], "kind": "original",
        "sha256": digest, "bytes": len(raw),
        "verificacion": {**inspection,
                         "descarga_desde_enlace_oficial": bool(descargar),
                         "cotejo_fuente_manual_pendiente": not descargar},
        "vigencia_revisada": False, "firma_digital_verificada": False,
        "perfil": list(item["aplicacion"]),
    }
    guardar(private, {"version": "adicionales-v1",
                      "archivos": previous["archivos"] + [entry]})
    return {"estado": "original_registrado", "archivo": str(target),
            "manifiesto_privado": str(private), "sha256": digest,
            "paginas": inspection["paginas"], "fuente_confirmada_por_descarga": bool(descargar),
            "vigencia_verificada": False, "indice": "ejecutar python -m oece biblioteca --reconstruir"}
