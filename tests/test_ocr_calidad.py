"""Comprueba errores criticos y limites del diagnostico OCR."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evaluar_calidad_ocr import compare, region_text


class QualityTests(unittest.TestCase):
    def test_critical_number_rejected_even_with_low_character_error(self):
        expected = "Texto extenso de referencia " * 20 + "articulo 207"
        observed = expected[:-3] + "208"
        result = compare(expected, observed, ["207"], 0.05)
        self.assertLess(result["cer"], 0.05)
        self.assertEqual(result["status"], "requiere_revision")

    def test_critical_token_cannot_match_part_of_a_longer_number(self):
        self.assertEqual(compare("207", "2072", ["207"], 1)["critical_tokens_missing"], ["207"])

    def test_perfect_match_never_grants_juridical_approval(self):
        result = compare("Ley 27444", "LEY 27444", ["27444"], 0.05)
        self.assertEqual(result["cer"], 0)
        self.assertFalse(result["apta_para_evaluacion"])
        self.assertTrue(result["human_review_required"])

    def test_roi_excludes_words_from_other_column(self):
        record = {"width": 100, "height": 100, "lines": [{"words": [
            {"text": "izquierda", "x": 1, "y": 1, "width": 20, "height": 10},
            {"text": "derecha", "x": 60, "y": 1, "width": 20, "height": 10}]}]}
        self.assertEqual(region_text(record, [0, 0, 50, 50]), "izquierda")
        with self.assertRaises(ValueError):
            region_text(record, [0, 0, 101, 100])


if __name__ == "__main__":
    unittest.main()
