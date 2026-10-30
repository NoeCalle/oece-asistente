"""Valida procedencia y geometria del OCR; no mide exactitud del texto."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from pypdf import PdfReader
from indexar_normativa import MANIFESTS, ROOT, read_json, safe_source


def validate_record(path, root=ROOT):
    root, path = Path(root).resolve(), Path(path).resolve()
    if root not in path.parents:
        raise ValueError("Derivado OCR fuera de raiz")
    record = read_json(path)
    items = [d for m in MANIFESTS for d in read_json(root / m)["archivos"]]
    matching = [d for d in items if d["name"] == record["source_name"]]
    if len(matching) != 1 or matching[0]["sha256"] != record["source_sha256"]:
        raise ValueError("Fuente OCR desconocida o hash incorrecto")
    source = safe_source(root, matching[0])
    page = record["page_pdf"]
    if type(page) is not int or not 1 <= page <= len(PdfReader(source).pages):
        raise ValueError("Pagina OCR fuera de fuente")
    image = Path(record["image_path"]).resolve()
    if root not in image.parents or hashlib.sha256(image.read_bytes()).hexdigest() != record["image_sha256"]:
        raise ValueError("Imagen OCR fuera de raiz o modificada")
    if record["confidence"] is not None or record["reviewed"] is not False or record["apta_para_evaluacion"] is not False:
        raise ValueError("Muestra OCR no puede declararse aprobada ni tener confianza inventada")
    if record["engine"] != "Windows.Media.Ocr" or not isinstance(record["text"], str) or not record["text"].strip():
        raise ValueError("Motor o texto OCR no valido")
    width, height = record["width"], record["height"]
    if width <= 0 or height <= 0:
        raise ValueError("Dimensiones OCR no validas")
    count = 0
    for line in record["lines"]:
        for word in line["words"]:
            values = [word[k] for k in ("x", "y", "width", "height")]
            if not all(isinstance(v, (int, float)) and math.isfinite(v) and v >= 0 for v in values):
                raise ValueError("Coordenadas OCR no validas")
            x, y, w, h = values
            if x + w > width + 1 or y + h > height + 1:
                raise ValueError("Palabra OCR fuera de imagen")
            count += 1
    if not count:
        raise ValueError("OCR sin palabras localizadas")
    return {"source_name": record["source_name"], "source_sha256": record["source_sha256"],
            "page_pdf": page, "image_sha256": record["image_sha256"],
            "derived_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "engine": record["engine"], "windows_build": record["windows_build"],
            "language": record["language"], "characters": len(record["text"]), "words": count,
            "visual_review_required": True, "apta_para_evaluacion": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps([validate_record(path) for path in args.records], ensure_ascii=False, indent=2))
