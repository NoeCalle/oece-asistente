"""Prepara una muestra OCR explicita, sin modificar los PDF originales."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from pypdf import PdfReader
from indexar_normativa import MANIFESTS, ROOT, read_json, safe_source


def prepare(source_name, pages, renderer, root=ROOT):
    root = Path(root).resolve()
    renderer = Path(renderer).resolve()
    if not renderer.is_file():
        raise ValueError("No se encontro pdftoppm")
    items = [d for m in MANIFESTS for d in read_json(root / m)["archivos"]]
    matches = [d for d in items if d["name"] == source_name]
    if len(matches) != 1:
        raise ValueError("Fuente inexistente o ambigua")
    item = matches[0]
    source = safe_source(root, item)
    count = len(PdfReader(source).pages)
    if not pages or len(pages) > 10 or len(set(pages)) != len(pages) or any(p < 1 or p > count for p in pages):
        raise ValueError("Seleccionar de 1 a 10 paginas distintas dentro del PDF")
    folder = (root / "normativa/ocr" / item["sha256"]).resolve()
    if root not in folder.parents:
        raise ValueError("Salida OCR fuera de raiz")
    folder.mkdir(parents=True, exist_ok=True)
    request = {"source_name": source_name, "source_sha256": item["sha256"], "render_scale": 2200, "pages": []}
    for page in pages:
        prefix = folder / f"page-{page:04d}"
        subprocess.run([str(renderer), "-f", str(page), "-l", str(page), "-scale-to", "2200",
                        "-png", "-singlefile", str(source), str(prefix)], check=True, timeout=120,
                       capture_output=True)
        image = prefix.with_suffix(".png")
        request["pages"].append({"page_pdf": page, "image_path": str(image),
                                 "image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                                 "output_path": str(prefix.with_suffix(".ocr.json"))})
    safe_source(root, item)
    job = folder / "job.json"
    job.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    return job


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--pages", required=True, help="Paginas PDF, por ejemplo 1,2")
    parser.add_argument("--renderer", required=True, type=Path)
    args = parser.parse_args()
    print(prepare(args.source, [int(p) for p in args.pages.split(",")], args.renderer))
