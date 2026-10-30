"""Casos sinteticos de trazabilidad OCR, independientes del motor Windows."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from pypdf import PdfWriter

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from verificar_ocr import validate_record


class OcrMetadataTests(unittest.TestCase):
    def setUp(self):
        area = SCRIPTS.parent / "normativa/ocr/pruebas"
        area.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=area)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        folder = self.root / "normativa"
        folder.mkdir()
        pdf = folder / "fuente.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with pdf.open("wb") as stream:
            writer.write(stream)
        image = folder / "imagen.png"
        image.write_bytes(b"synthetic image bytes: validation does not decode")
        sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        item = {"name": pdf.name, "local_path": "normativa/fuente.pdf", "bytes": pdf.stat().st_size, "sha256": sha(pdf)}
        (folder / "manifiesto-descargas-2026-10-29.json").write_text(json.dumps({"archivos": [item]}), encoding="utf-8")
        (folder / "manifiesto-continuacion-2026-10-30.json").write_text(json.dumps({"archivos": []}), encoding="utf-8")
        (folder / "manifiesto-ampliacion-2026-10-30.json").write_text(json.dumps({"archivos": []}), encoding="utf-8")
        self.path = folder / "ocr.json"
        self.record = {"source_name": pdf.name, "source_sha256": sha(pdf), "page_pdf": 1,
                       "image_path": str(image), "image_sha256": sha(image), "width": 100, "height": 100,
                       "confidence": None, "reviewed": False, "apta_para_evaluacion": False,
                       "engine": "Windows.Media.Ocr", "windows_build": "synthetic", "language": "es-MX",
                       "text": "prueba", "lines": [{"text": "prueba", "words": [{"text": "prueba", "x": 2, "y": 2, "width": 20, "height": 10}]}]}

    def run_validation(self):
        self.path.write_text(json.dumps(self.record), encoding="utf-8")
        return validate_record(self.path, self.root)

    def test_valid_provenance_keeps_review_pending(self):
        result = self.run_validation()
        self.assertFalse(result["apta_para_evaluacion"])
        self.assertEqual(result["words"], 1)

    def test_rejects_wrong_source_and_modified_image(self):
        self.record["source_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash"):
            self.run_validation()
        self.record["source_sha256"] = hashlib.sha256((self.root / "normativa/fuente.pdf").read_bytes()).hexdigest()
        Path(self.record["image_path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Imagen"):
            self.run_validation()

    def test_rejects_invalid_page_and_coordinates(self):
        self.record["page_pdf"] = 2
        with self.assertRaisesRegex(ValueError, "Pagina"):
            self.run_validation()
        self.record["page_pdf"] = 1
        self.record["lines"][0]["words"][0]["x"] = 99
        with self.assertRaisesRegex(ValueError, "fuera de imagen"):
            self.run_validation()

    def test_cannot_claim_human_approval(self):
        self.record["apta_para_evaluacion"] = True
        with self.assertRaisesRegex(ValueError, "aprobada"):
            self.run_validation()


if __name__ == "__main__":
    unittest.main()
