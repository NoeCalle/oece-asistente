"""Indice local de fuentes. La recuperacion no acredita vigencia ni cumplimiento."""
import argparse
import hashlib
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    "normativa/manifiesto-descargas-2026-10-29.json",
    "normativa/manifiesto-continuacion-2026-10-30.json",
    "normativa/manifiesto-ampliacion-2026-10-30.json",
    "normativa/manifiesto-cierre-piloto-2026-10-30.json",
    "normativa/manifiesto-operacion-2026-10-31.json",
    "normativa/manifiesto-procedimientos-2026-10-31.json",
)
EXTRACTOR_VERSION = "0.1.0"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def safe_source(root, item):
    path = (root / item["local_path"]).resolve()
    if root not in path.parents:
        raise ValueError("Ruta de fuente fuera de la biblioteca: " + item["name"])
    raw = path.read_bytes()
    if len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]:
        raise ValueError("Integridad incorrecta: " + item["name"])
    return path


class ReaderWarnings(logging.Handler):
    def __init__(self):
        super().__init__(logging.WARNING)
        self.messages = []

    def emit(self, record):
        message = record.getMessage()
        if len(self.messages) < 50 and message not in self.messages:
            self.messages.append(message)


def extract(path):
    """Devuelve fragmentos con ubicaciones estables y advertencias explicitas."""
    blocks = []
    warnings = []
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        capture = ReaderWarnings()
        logger = logging.getLogger("pypdf")
        logger.addHandler(capture)
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                raise ValueError("PDF cifrado: requiere tratamiento explicito")
            for page_number, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                flags = []
                if len(text.strip()) < 50:
                    flags.append("requiere_ocr_o_revision")
                blocks.append(({"pagina_pdf": page_number}, text, flags))
        finally:
            logger.removeHandler(capture)
            warnings.extend(capture.messages)
        return "pypdf", blocks, warnings
    if path.suffix.lower() == ".docx":
        from docx import Document
        from docx.table import Table
        doc = Document(path)

        def walk(container, prefix):
            for block_number, block in enumerate(container.iter_inner_content(), 1):
                address = prefix + [f"bloque:{block_number}"]
                if isinstance(block, Table):
                    # Word puede repetir una celda combinada: conservar la primera.
                    seen = set()
                    for row_number, row in enumerate(block.rows, 1):
                        for cell_number, cell in enumerate(row.cells, 1):
                            if cell._tc in seen:
                                continue
                            seen.add(cell._tc)
                            walk(cell, address + [f"fila:{row_number}", f"celda:{cell_number}"])
                else:
                    blocks.append(({"ruta_bloque": "/".join(address)}, block.text, []))

        walk(doc, ["cuerpo"])
        warnings.append("DOCX: cuerpo y tablas; encabezados, pies, cuadros de texto y revisiones no cubiertos")
        return "python-docx", blocks, warnings
    return None, [], ["formato_pendiente: " + path.suffix.lower()]


def build_index(root, output, manifests=MANIFESTS):
    root, output = Path(root).resolve(), Path(output).resolve()
    if root not in output.parents or output.suffix != ".sqlite":
        raise ValueError("Guardar el indice .sqlite dentro de la raiz del proyecto")
    manifest_paths = [(root / name).resolve() for name in manifests]
    if any(root not in path.parents for path in manifest_paths):
        raise ValueError("Manifiesto fuera de la raíz del proyecto")
    items = [item for path in manifest_paths for item in read_json(path)["archivos"]]
    catalog = read_json(root / "normativa/catalogo.json")["normas"]
    prepared = [(item, safe_source(root, item)) for item in items]
    if len({p for _, p in prepared}) != len(prepared):
        raise ValueError("Ruta duplicada en manifiestos")
    if any(output == p for _, p in prepared):
        raise ValueError("El indice no puede reemplazar una fuente")
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(suffix=".sqlite", dir=output.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        connection.executescript("""
            PRAGMA user_version=1;
            CREATE TABLE documents (id TEXT PRIMARY KEY, metadata TEXT NOT NULL);
            CREATE TABLE fragments (id TEXT PRIMARY KEY, document_id TEXT NOT NULL,
                locator TEXT NOT NULL, text TEXT NOT NULL, flags TEXT NOT NULL);
            CREATE VIRTUAL TABLE search USING fts5(fragment_id UNINDEXED, text,
                tokenize='unicode61 remove_diacritics 2');
        """)
        summary = {"extractor_version": EXTRACTOR_VERSION, "documentos": [], "fragmentos": 0,
                   "apta_para_evaluacion": False,
                   "alcance": "extraccion textual; vigencia y OCR pendientes",
                   "motores": {name: importlib.metadata.version(name) for name in ("pypdf", "python-docx")}}
        snapshot = {"archivos": items, "catalogo": catalog, "motores": summary["motores"],
                    "extractor_version": EXTRACTOR_VERSION}
        summary["corpus_id"] = hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()
        for item, path in prepared:
            # Una version se identifica por contenido; conservar todas sus procedencias.
            version_id = item["sha256"]
            existing = connection.execute("SELECT metadata FROM documents WHERE id=?", (version_id,)).fetchone()
            if existing:
                metadata = json.loads(existing[0])
                metadata["procedencias"].append({"nombre": item["name"], "url": item["source_url"]})
                connection.execute("UPDATE documents SET metadata=? WHERE id=?", (json.dumps(metadata), version_id))
                continue
            matching = [n for n in catalog if n["archivo"]["sha256"] == version_id or n["id"] == item.get("instrument_id")]
            metadata = {"nombre": item["name"], "sha256": version_id,
                        "procedencias": [{"nombre": item["name"], "url": item["source_url"]}],
                        "normas": [{"id": n["id"], "vigencia_declarada": n["vigencia"],
                                    "validacion": n["validacion"]["nivel"]} for n in matching],
                        "procedimientos": sorted({p for n in matching for p in n["procedimientos"]}),
                        "apta_para_evaluacion": False, "firma_verificada": False}
            try:
                engine, blocks, warnings = extract(path)
                status = "extraido_con_revision_pendiente" if engine else "formato_pendiente"
            except Exception as error:
                engine, blocks, warnings = None, [], [type(error).__name__ + ": " + str(error)]
                status = "error_lectura"
            # Detectar cambios concurrentes durante la lectura antes de publicar el indice.
            safe_source(root, item)
            if blocks and all("requiere_ocr_o_revision" in flags for _, _, flags in blocks):
                status = "requiere_ocr_o_revision"
            elif any(flags for _, _, flags in blocks):
                status = "extraccion_parcial"
            metadata.update(motor=engine, motor_version=summary["motores"].get(engine),
                            extractor_version=EXTRACTOR_VERSION, corpus_id=summary["corpus_id"],
                            confianza_extraccion=None, estado=status, advertencias=warnings)
            connection.execute("INSERT INTO documents VALUES (?, ?)", (version_id, json.dumps(metadata, ensure_ascii=False)))
            low_text = 0
            for locator, text, flags in blocks:
                fragment_id = hashlib.sha256((EXTRACTOR_VERSION + version_id + json.dumps(locator, sort_keys=True)).encode()).hexdigest()
                connection.execute("INSERT INTO fragments VALUES (?, ?, ?, ?, ?)",
                                   (fragment_id, version_id, json.dumps(locator), text, json.dumps(flags)))
                connection.execute("INSERT INTO search VALUES (?, ?)", (fragment_id, text))
                low_text += bool(flags)
            summary["fragmentos"] += len(blocks)
            summary["documentos"].append({"nombre": item["name"], "sha256": version_id, "estado": status,
                                           "fragmentos": len(blocks), "fragmentos_con_alerta": low_text,
                                           "fragmentos_con_texto": sum(bool(text.strip()) for _, text, _ in blocks),
                                           "advertencias": warnings})
        connection.execute("CREATE TABLE run (summary TEXT NOT NULL)")
        connection.execute("INSERT INTO run VALUES (?)", (json.dumps(summary, ensure_ascii=False),))
        connection.commit()
        connection.close()
        connection = None
        os.replace(temporary, output)
        return summary
    finally:
        if connection is not None:
            connection.close()
        if temporary.exists():
            temporary.unlink()


def search_index(database, query, procedure=None, limit=10):
    if not query.strip() or not 1 <= limit <= 100:
        raise ValueError("Consulta vacia o limite fuera de 1..100")
    # Tratar cada palabra como literal; no permitir operadores FTS del usuario.
    expression = " AND ".join('"' + term.replace('"', '""') + '"' for term in query.split())
    uri = Path(database).resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    try:
        cursor = connection.execute("""
            SELECT f.id, f.locator, f.text, f.flags, d.metadata
            FROM search s JOIN fragments f ON f.id=s.fragment_id
            JOIN documents d ON d.id=f.document_id
            WHERE search MATCH ? ORDER BY rank
        """, (expression,))
        results = []
        for fragment_id, locator, text, flags, raw_metadata in cursor:
            metadata = json.loads(raw_metadata)
            if procedure and procedure not in metadata["procedimientos"]:
                continue
            results.append({"fragment_id": fragment_id, "ubicacion": json.loads(locator),
                            "texto": text, "alertas": json.loads(flags), "documento": metadata,
                            "apta_para_evaluacion": False})
            if len(results) >= limit:
                break
        return results
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "search"))
    parser.add_argument("--database", type=Path, default=ROOT / "normativa/indices/biblioteca.sqlite")
    parser.add_argument("--manifest", action="append", help="Manifiesto relativo a la raíz; repetible para un índice complementario")
    parser.add_argument("--query")
    parser.add_argument("--procedure")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.action == "build":
        result = build_index(ROOT, args.database, tuple(args.manifest) if args.manifest else MANIFESTS)
    else:
        if args.manifest:
            parser.error("--manifest solo se admite con build")
        if args.query is None:
            parser.error("search requiere --query")
        result = search_index(args.database, args.query, args.procedure, args.limit)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
