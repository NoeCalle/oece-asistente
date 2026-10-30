"""Crea otro indice con OCR candidato; conserva la extraccion digital original."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile

from indexar_normativa import ROOT, read_json
from verificar_ocr import validate_record
from evaluar_calidad_ocr import evaluate

VERSION = "0.1.0"


def integrate(root, base, output, records, quality_reference=None):
    root, base, output = Path(root).resolve(), Path(base).resolve(), Path(output).resolve()
    if root not in base.parents or root not in output.parents or output == base or output.suffix != ".sqlite":
        raise ValueError("Usar indices distintos dentro de la raiz")
    if not base.is_file() or not records:
        raise ValueError("Falta indice base o muestra OCR")
    quality = evaluate(quality_reference, root) if quality_reference else {"reference_sha256": None, "results": []}
    prepared = []
    for path in records:
        path = Path(path).resolve()
        provenance = validate_record(path, root)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != provenance["derived_sha256"]:
            raise ValueError("OCR cambio durante validacion")
        record = json.loads(raw)
        checks = [r for r in quality["results"] if r["source_sha256"] == record["source_sha256"]
                  and r["page_pdf"] == record["page_pdf"]]
        if any(r["derived_sha256"] != provenance["derived_sha256"] for r in checks):
            raise ValueError("Diagnostico corresponde a otra version OCR")
        prepared.append((path, provenance, record, checks))
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(suffix=".sqlite", dir=output.parent)
    os.close(fd)
    temporary = Path(name)
    connection = None
    source = None
    try:
        source = sqlite3.connect(base.as_uri() + "?mode=ro", uri=True)
        connection = sqlite3.connect(temporary)
        source.backup(connection)
        source.close()
        source = None
        summary = json.loads(connection.execute("SELECT summary FROM run").fetchone()[0])
        base_corpus = summary.get("base_corpus_id", summary["corpus_id"])
        connection.execute("""CREATE TABLE IF NOT EXISTS ocr_derivatives (
            id TEXT PRIMARY KEY, document_id TEXT NOT NULL, page_pdf INTEGER NOT NULL,
            metadata TEXT NOT NULL, UNIQUE(document_id, page_pdf))""")
        inserted = 0
        for path, provenance, record, checks in prepared:
            doc_id, page = record["source_sha256"], record["page_pdf"]
            document = connection.execute("SELECT metadata FROM documents WHERE id=?", (doc_id,)).fetchone()
            if not document:
                raise ValueError("Fuente OCR no pertenece al indice base")
            page_rows = connection.execute("SELECT locator, flags FROM fragments WHERE document_id=?", (doc_id,)).fetchall()
            if not any(json.loads(loc).get("pagina_pdf") == page and json.loads(loc).get("tipo") != "ocr"
                       and "requiere_ocr_o_revision" in json.loads(flags) for loc, flags in page_rows):
                raise ValueError("La pagina base no estaba marcada para OCR")
            derivative_id = provenance["derived_sha256"]
            prior = connection.execute("SELECT id FROM ocr_derivatives WHERE document_id=? AND page_pdf=?", (doc_id, page)).fetchone()
            if prior and prior[0] != derivative_id:
                raise ValueError("Otra version OCR de la misma pagina: reconstruir desde indice digital base")
            diagnostic = {"reference_sha256": quality["reference_sha256"],
                          "scope": "solo_regiones" if checks else "sin_referencia_para_esta_pagina",
                          "checks": [{k: r[k] for k in ("id", "status", "cer", "critical_tokens_missing")} for r in checks]}
            flags = ["ocr_pendiente_revision"]
            if any(r["critical_tokens_missing"] for r in checks):
                flags.append("error_identificador_critico_en_muestra")
            if any(r["status"] == "requiere_revision" for r in checks):
                flags.append("diagnostico_regional_requiere_revision")
            locator = {"pagina_pdf": page, "tipo": "ocr", "ocr_sha256": derivative_id,
                       "imagen_sha256": record["image_sha256"], "derivado_local": path.relative_to(root).as_posix(),
                       "motor": record["engine"], "idioma": record["language"], "diagnostico": diagnostic}
            metadata = {**provenance, "derivado_local": path.relative_to(root).as_posix(), "diagnostico": diagnostic}
            connection.execute("INSERT OR REPLACE INTO ocr_derivatives VALUES (?, ?, ?, ?)",
                               (derivative_id, doc_id, page, json.dumps(metadata, ensure_ascii=False)))
            fragment_id = hashlib.sha256(("ocr:" + VERSION + ":" + derivative_id).encode()).hexdigest()
            if connection.execute("SELECT 1 FROM fragments WHERE id=?", (fragment_id,)).fetchone():
                connection.execute("UPDATE fragments SET locator=?, flags=? WHERE id=?",
                                   (json.dumps(locator), json.dumps(flags), fragment_id))
            else:
                connection.execute("INSERT INTO fragments VALUES (?, ?, ?, ?, ?)",
                                   (fragment_id, doc_id, json.dumps(locator), record["text"], json.dumps(flags)))
                connection.execute("INSERT INTO search VALUES (?, ?)", (fragment_id, record["text"]))
                inserted += 1
        derivatives = [json.loads(row[0]) for row in connection.execute("SELECT metadata FROM ocr_derivatives ORDER BY id")]
        corpus_id = hashlib.sha256(json.dumps({"base": base_corpus, "version": VERSION, "ocr": derivatives}, sort_keys=True).encode()).hexdigest()
        document_rows = connection.execute("SELECT id, metadata FROM documents").fetchall()
        for doc_id, raw in document_rows:
            metadata = json.loads(raw)
            metadata["corpus_id"] = corpus_id
            metadata["ocr_paginas_disponibles"] = [d["page_pdf"] for d in derivatives if d["source_sha256"] == doc_id]
            connection.execute("UPDATE documents SET metadata=? WHERE id=?", (json.dumps(metadata, ensure_ascii=False), doc_id))
        summary.update(base_corpus_id=base_corpus, corpus_id=corpus_id, integrador_ocr=VERSION,
                       fragmentos=connection.execute("SELECT COUNT(*) FROM fragments").fetchone()[0],
                       fragmentos_ocr=len(derivatives), derivados_ocr=derivatives,
                       alcance="Texto digital y capa OCR candidata; vigencia y revision pendientes")
        connection.execute("DELETE FROM run")
        connection.execute("INSERT INTO run VALUES (?)", (json.dumps(summary, ensure_ascii=False),))
        # Verificar que texto, imagen y fuente no cambiaron antes de publicar.
        for path, provenance, _, _ in prepared:
            if validate_record(path, root)["derived_sha256"] != provenance["derived_sha256"]:
                raise ValueError("Derivado OCR modificado durante integracion")
        connection.commit()
        connection.close()
        connection = None
        os.replace(temporary, output)
        return {"corpus_id": corpus_id, "base_corpus_id": base_corpus, "ocr_agregados": inserted,
                "fragmentos_ocr": len(derivatives), "fragmentos_totales": summary["fragmentos"],
                "derivados": derivatives, "apta_para_evaluacion": False}
    finally:
        if source is not None:
            source.close()
        if connection is not None:
            connection.close()
        if temporary.exists():
            temporary.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--base", type=Path, default=ROOT / "normativa/indices/biblioteca.sqlite")
    parser.add_argument("--output", type=Path, default=ROOT / "normativa/indices/biblioteca-ocr.sqlite")
    parser.add_argument("--quality-reference", type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(integrate(ROOT, args.base, args.output, args.records, args.quality_reference), ensure_ascii=False, indent=2))
