import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verificar_cobertura_piloto import assess


class CoverageTests(unittest.TestCase):
    def setUp(self):
        area = ROOT / "data/pruebas-cobertura"
        area.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=area)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "fuente.txt"
        self.source.write_bytes(b"fuente sintetica")
        self.item = {"name": "fuente.txt", "local_path": "fuente.txt", "bytes": self.source.stat().st_size,
                     "sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(), "source_url": "https://www.gob.pe/prueba-sintetica"}
        self.plan = {"procedimiento": "ampliacion_consultores", "habilita_reglas": False,
                     "grupos": [{"id": "grupo", "prioridad": "principal", "archivos_obligatorios": ["fuente.txt"],
                                  "pendiente_juridico": ["Revisión humana"]}]}
        self.save()

    def save(self):
        (self.root / "plan.json").write_text(json.dumps(self.plan), encoding="utf-8")
        (self.root / "manifest.json").write_text(json.dumps({"archivos": [self.item]}), encoding="utf-8")

    def assess(self, originals=False):
        return assess(self.root, "plan.json", ("manifest.json",), originals)

    def test_complete_acquisition_never_closes_law(self):
        result = self.assess(True)
        self.assertEqual("completa_en_alcance_versionado", result["estado_adquisicion"])
        self.assertFalse(result["cierre_juridico"])
        self.assertFalse(result["apta_para_evaluacion"])
        self.assertEqual("solo_cobertura_de_manifiestos", self.assess()["estado_adquisicion"])

    def test_missing_source_or_manifest_blocks_closure(self):
        self.source.unlink()
        self.assertEqual(["fuente.txt"], self.assess(True)["faltantes"])
        self.plan["grupos"][0]["archivos_obligatorios"].append("ausente.pdf")
        self.save()
        self.assertEqual("pendiente", self.assess()["estado_adquisicion"])

    def test_changed_original_fails_integrity(self):
        self.source.write_bytes(b"original cambiado")
        with self.assertRaisesRegex(ValueError, "Integridad"):
            self.assess(True)

    def test_unofficial_provenance_and_external_path_rejected(self):
        self.item["source_url"] = "https://example.org/no-oficial"
        self.save()
        with self.assertRaisesRegex(ValueError, "oficiales"):
            self.assess()
        self.item["source_url"] = "https://www.gob.pe/prueba"
        self.item["local_path"] = "../fuera.txt"
        self.save()
        with self.assertRaisesRegex(ValueError, "fuera"):
            self.assess(True)

    def test_duplicate_and_enabling_plan_rejected(self):
        self.plan["grupos"].append(self.plan["grupos"][0])
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicado"):
            self.assess()
        self.plan["habilita_reglas"] = True
        self.save()
        with self.assertRaisesRegex(ValueError, "habilitar"):
            self.assess()


if __name__ == "__main__":
    unittest.main()
