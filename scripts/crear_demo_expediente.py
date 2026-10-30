"""Materializa una entrada sintética reproducible sin sobrescribir archivos."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def create(destination):
    fixture = json.loads((ROOT / "tests/fixtures/expedientes/demo.json").read_text(encoding="utf-8"))
    destination.mkdir(parents=True, exist_ok=True)
    files = {**fixture["archivos"], "expediente.json": json.dumps(fixture["expediente"], ensure_ascii=False, indent=2)}
    for name, text in files.items():
        path = destination / name
        if path.exists() and path.read_text(encoding="utf-8") != text:
            raise ValueError("Entrada existente diferente; use otra carpeta: " + name)
    for name, text in files.items():
        (destination / name).write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    create(args.salida)
    print(str(args.salida.resolve()))
