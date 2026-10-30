"""Compara regiones OCR con transcripcion manual; no aprueba evidencia juridica."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

from indexar_normativa import ROOT, read_json
from verificar_ocr import validate_record


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def distance(expected, observed):
    previous = list(range(len(observed) + 1))
    for i, left in enumerate(expected, 1):
        current = [i]
        for j, right in enumerate(observed, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (left != right)))
        previous = current
    return previous[-1]


def region_text(record, box):
    x1, y1, x2, y2 = box
    if not 0 <= x1 < x2 <= record["width"] or not 0 <= y1 < y2 <= record["height"]:
        raise ValueError("Region fuera de imagen")
    selected = []
    for line in record["lines"]:
        words = []
        for word in line["words"]:
            cx, cy = word["x"] + word["width"] / 2, word["y"] + word["height"] / 2
            if x1 <= cx < x2 and y1 <= cy < y2:
                words.append(word["text"])
        if words:
            selected.append(" ".join(words))
    return " ".join(selected)


def compare(expected, observed, critical_tokens, max_cer):
    if not 0 <= max_cer <= 1 or not expected.strip():
        raise ValueError("Referencia o umbral no valido")
    left, right = normalize(expected), normalize(observed)
    cer = distance(left, right) / len(left)
    wer = distance(left.split(), right.split()) / len(left.split())
    missing = [token for token in critical_tokens if not re.search(
        r"(?<!\w)" + re.escape(normalize(token)) + r"(?!\w)", right)]
    return {"cer": cer, "wer": wer, "critical_tokens_missing": missing,
            "status": "requiere_revision" if missing or cer > max_cer else "dentro_umbral_de_muestra",
            "apta_para_evaluacion": False, "human_review_required": True}


def evaluate(reference_path, root=ROOT):
    root = Path(root).resolve()
    reference = read_json(reference_path)
    results = []
    for case in reference["regions"]:
        path = (root / case["ocr_path"]).resolve()
        provenance = validate_record(path, root)
        if provenance["image_sha256"] != case["image_sha256"]:
            raise ValueError("La referencia corresponde a otra imagen")
        if provenance["source_sha256"] != case["source_sha256"] or provenance["page_pdf"] != case["page_pdf"]:
            raise ValueError("La referencia corresponde a otra fuente/pagina")
        observed = region_text(read_json(path), case["roi_xyxy"])
        result = compare(case["reference_text"], observed, case["critical_tokens"], reference["max_cer_propuesto"])
        results.append({"id": case["id"], "source_sha256": case["source_sha256"], "page_pdf": case["page_pdf"],
                        "roi_xyxy": case["roi_xyxy"], "reference_text": case["reference_text"], "observed_text": observed,
                        "derived_sha256": provenance["derived_sha256"], **result})
    return {"reference_sha256": hashlib.sha256(Path(reference_path).read_bytes()).hexdigest(),
            "scope": "Regiones seleccionadas; no estima precision de documentos completos", "results": results,
            "apta_para_evaluacion": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(evaluate(args.reference), ensure_ascii=False, indent=2))
