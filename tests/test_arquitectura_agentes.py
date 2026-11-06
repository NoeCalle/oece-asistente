"""Contratos documentales de agentes: sin MCP, sin Drive y sin datos privados.

Estas verificaciones solo comprueban consistencia estática del repositorio; no
certifican ejecución cloud, lectura de Drive ni validez de evaluaciones.
"""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTES = [
    "agentes/coordinador.md",
    "agentes/especialista-cmc.md",
    "agentes/especialista-consultores.md",
    "agentes/consulta-normativa.md",
]
CONTRATOS = [
    "contratos/control-evidencias.md",
    "contratos/entregables-cmc.md",
    "contratos/informe-consultores.md",
]
PROCEDIMIENTOS = [
    "procedimientos/aumento-cmc.md",
    "procedimientos/ampliacion-consultores.md",
    "procedimientos/control-integridad-documental.md",
]
ENTRADAS = [
    "AGENTS.md", "CLAUDE.md", "GROK.md",
    "docs/ARQUITECTURA_AGENTES.md",
    "docs/PROMPT_OECE_UNIVERSAL.md",
    "docs/PRUEBAS_AGENTES.md",
]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ArquitecturaAgentes(unittest.TestCase):
    def test_todos_los_archivos_existen(self):
        for path in AGENTES + CONTRATOS + PROCEDIMIENTOS + ENTRADAS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)

    def test_todos_los_links_relativos_resuelven(self):
        for path in AGENTES + CONTRATOS + PROCEDIMIENTOS + ENTRADAS:
            text = read(path)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                target = target.split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                expected = ROOT / Path(path).parent / target
                with self.subTest(source=path, target=target):
                    self.assertTrue(expected.is_file(), str(expected))

    def test_coordinador_enruta_sin_deducir_por_pdf(self):
        coordinator = read("agentes/coordinador.md")
        self.assertIn("aumento_cmc", coordinator)
        self.assertIn("ampliacion_consultores", coordinator)
        self.assertIn("normativa", coordinator.lower())
        self.assertIn("no", coordinator.lower())
        self.assertIn("PDF", coordinator)
        self.assertIn("sin MCP", coordinator)

    def test_especialidades_no_mezclan_formulas(self):
        cmc = read("agentes/especialista-cmc.md")
        consultants = read("agentes/especialista-consultores.md")
        self.assertIn("G = a + f + e", cmc)
        self.assertIn("CMC_a_otorgar = null", cmc)
        self.assertIn("entregable-01-datos.json", cmc)
        self.assertIn("entregable-02-datos.json", cmc)
        self.assertIn("entregable-03-datos.json", cmc)
        self.assertIn("No", consultants)
        self.assertIn("G=a+f+e", consultants)
        self.assertIn("informe.docx", consultants)
        self.assertIn("matriz.csv", consultants)
        self.assertIn("matriz.json", consultants)

    def test_fuentes_drive_primero_y_web_con_aviso(self):
        for path in AGENTES + ["docs/PROMPT_OECE_UNIVERSAL.md",
                               "contratos/control-evidencias.md"]:
            content = read(path).lower()
            with self.subTest(path=path):
                self.assertIn("drive", content)
        normative = read("agentes/consulta-normativa.md").lower()
        self.assertIn("avisar", normative)
        self.assertIn("antes", normative)
        self.assertIn("internet", normative)
        self.assertIn("no se puede consultar", normative)


    def test_integridad_documental_no_se_confunde_con_suficiencia(self):
        procedimiento = read("procedimientos/control-integridad-documental.md")
        for item in ("capacitaci", "05/11/2026", "aunque",
                     "indicio_incompletitud", "incompleto_confirmado",
                     "no_verificable", "cláusulas", "párrafos", "OCR",
                     "consecuencia_administrativa"):
            with self.subTest(item=item):
                self.assertIn(item, procedimiento)
        for path in ("agentes/coordinador.md",
                     "agentes/especialista-cmc.md",
                     "agentes/especialista-consultores.md",
                     "contratos/control-evidencias.md",
                     "docs/PROMPT_OECE_UNIVERSAL.md",
                     "contratos/entregables-cmc.md",
                     "contratos/informe-consultores.md"):
            text = read(path)
            with self.subTest(path=path):
                self.assertIn("control-integridad-documental.md", text)
                self.assertIn("observaci", text.lower())
        cmc = read("contratos/entregables-cmc.md")
        self.assertIn("entregable-01-datos.json", cmc)
        self.assertIn("ficha-maestra.json", cmc)
        consultants = read("contratos/informe-consultores.md")
        self.assertIn("matriz", consultants.lower())
        self.assertIn("integridad documental", consultants.lower())

    def test_legacy_no_es_obligatorio_y_falta_prueba_cloud(self):
        agents = read("AGENTS.md")
        self.assertIn("NO exigir", agents)
        self.assertIn("opcional", agents.lower())
        plan = read("docs/ARQUITECTURA_AGENTES.md")
        self.assertIn("Pendiente de verificación real", plan)
        self.assertIn("Python/MCP legado", plan)
        prompt = read("docs/PROMPT_OECE_UNIVERSAL.md")
        self.assertIn("CMC_a_otorgar", prompt)
        self.assertIn("NO llaman automáticamente", prompt)


if __name__ == "__main__":
    unittest.main()
