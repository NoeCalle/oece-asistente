"""Integracion candidata: duplicados, evidencia original y fallos atomicos."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import closing

from pypdf import PdfWriter

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from indexar_normativa import build_index, search_index
import integrar_ocr


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        area = SCRIPTS.parent / "normativa/indices/pruebas"
        area.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=area)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.folder = self.root / "normativa"
        self.folder.mkdir()
        self.source = self.folder / "fuente.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        with self.source.open("wb") as stream:
            writer.write(stream)
        self.sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        self.item = {"name": self.source.name, "local_path": "normativa/fuente.pdf", "bytes": self.source.stat().st_size,
                     "sha256": self.sha(self.source), "source_url": "https://www.gob.pe/fuente-sintetica", "instrument_id": "prueba"}
        self.manifest = self.folder / "manifiesto-descargas-2026-10-29.json"
        self.manifest.write_text(json.dumps({"archivos": [self.item]}), encoding="utf-8")
        (self.folder / "manifiesto-continuacion-2026-10-30.json").write_text('{"archivos": []}', encoding="utf-8")
        (self.folder / "manifiesto-ampliacion-2026-10-30.json").write_text('{"archivos": []}', encoding="utf-8")
        (self.folder / "manifiesto-cierre-piloto-2026-10-30.json").write_text('{"archivos": []}', encoding="utf-8")
        (self.folder / "manifiesto-operacion-2026-10-31.json").write_text('{"archivos": []}', encoding="utf-8")
        (self.folder / "catalogo.json").write_text(json.dumps({"normas": [{"id": "prueba", "archivo": {"sha256": self.item["sha256"]},
             "vigencia": {"desde": None}, "validacion": {"nivel": "pendiente"}, "procedimientos": ["ampliacion_consultores"]}]}), encoding="utf-8")
        self.base = self.folder / "indices/base.sqlite"
        self.output = self.folder / "indices/ocr.sqlite"
        build_index(self.root, self.base)
        self.image = self.folder / "pagina.png"
        self.image.write_bytes(b"synthetic image bytes")
        self.record = {"source_name": self.source.name, "source_sha256": self.item["sha256"], "page_pdf": 1,
                       "image_path": str(self.image), "image_sha256": self.sha(self.image), "width": 100, "height": 100,
                       "engine": "Windows.Media.Ocr", "windows_build": "synthetic", "language": "es-MX",
                       "confidence": None, "reviewed": False, "apta_para_evaluacion": False, "text": "Ley 27444",
                       "lines": [{"text": "Ley 27444", "words": [{"text": "Ley", "x": 1, "y": 1, "width": 10, "height": 10}]}]}
        self.ocr = self.folder / "pagina.ocr.json"
        self.write_record()

    def write_record(self):
        self.ocr.write_text(json.dumps(self.record), encoding="utf-8")

    def run_integration(self, base=None, output=None, quality=None):
        return integrar_ocr.integrate(self.root, base or self.base, output or self.output, [self.ocr], quality)

    def test_search_preserves_original_and_returns_pending_alert(self):
        before = self.sha(self.base)
        result = self.run_integration()
        self.assertEqual(self.sha(self.base), before)
        self.assertEqual(result["fragmentos_totales"], 2)
        hits = search_index(self.output, "27444", "ampliacion_consultores")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["ubicacion"]["pagina_pdf"], 1)
        self.assertEqual(hits[0]["ubicacion"]["tipo"], "ocr")
        self.assertIn("ocr_pendiente_revision", hits[0]["alertas"])
        self.assertFalse(hits[0]["apta_para_evaluacion"])
        with closing(sqlite3.connect(self.output)) as connection:
            rows = connection.execute("SELECT text, locator FROM fragments").fetchall()
        self.assertTrue(any(text == "" and "tipo" not in json.loads(loc) for text, loc in rows))

    def test_repeat_does_not_duplicate_derivative(self):
        self.run_integration()
        result = self.run_integration(base=self.output, output=self.folder / "indices/segunda.sqlite")
        self.assertEqual(result["ocr_agregados"], 0)
        self.assertEqual(result["fragmentos_ocr"], 1)
        self.assertEqual(result["fragmentos_totales"], 2)

    def test_image_change_keeps_previous_output(self):
        self.run_integration()
        before = self.sha(self.output)
        self.image.write_bytes(b"modified")
        with self.assertRaisesRegex(ValueError, "Imagen"):
            self.run_integration()
        self.assertEqual(self.sha(self.output), before)

    def test_other_ocr_version_requires_rebuild_from_digital_base(self):
        self.run_integration()
        self.record["text"] = "Texto corregido candidato"
        self.write_record()
        with self.assertRaisesRegex(ValueError, "Otra version OCR"):
            self.run_integration(base=self.output, output=self.folder / "indices/segunda.sqlite")

    def test_output_cannot_replace_base(self):
        before = self.sha(self.base)
        with self.assertRaisesRegex(ValueError, "distintos"):
            self.run_integration(output=self.base)
        self.assertEqual(before, self.sha(self.base))

    def test_critical_quality_alert_and_stale_report(self):
        check = {"id": "Q", "source_sha256": self.item["sha256"], "page_pdf": 1,
                 "derived_sha256": self.sha(self.ocr), "status": "requiere_revision", "cer": 0.1,
                 "critical_tokens_missing": ["006-2026-JUS"]}
        with patch.object(integrar_ocr, "evaluate", return_value={"reference_sha256": "synthetic", "results": [check]}):
            self.run_integration(quality="synthetic-reference")
        self.assertIn("error_identificador_critico_en_muestra", search_index(self.output, "27444")[0]["alertas"])
        check["derived_sha256"] = "0" * 64
        with patch.object(integrar_ocr, "evaluate", return_value={"reference_sha256": "synthetic", "results": [check]}):
            with self.assertRaisesRegex(ValueError, "otra version OCR"):
                self.run_integration(quality="synthetic-reference")


if __name__ == "__main__":
    unittest.main()
