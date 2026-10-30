import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from crear_demo_expediente import create
from ejecutar_expediente import encoded, load, prepare
from proponer_evidencias import PROFILE, RULES, decision_template, match_groups, propose, save_new
from revisar_evidencias import export_reviewed, reviewed_config


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        area = ROOT / "data/pruebas-evidencias"
        area.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=area)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.case = self.root / "entrada"
        create(self.case)
        config = load(self.case / "expediente.json")
        config["vinculos"] = {}
        (self.case / "expediente.json").write_bytes(encoded(config))

    def accept_one(self, bundle):
        decisions = decision_template(bundle)
        decisions["decisiones"][0].update(decision="aceptada", revisor="REVISOR-SINTETICO",
                                          fecha="2026-10-30T17:00:00-05:00", motivo="Revisión técnica ficticia de localización")
        return decisions

    def test_deterministic_proposals_and_exact_anchors(self):
        first = propose(self.case)
        self.assertEqual(first, propose(self.case))
        self.assertTrue(first["propuestas"])
        for p in first["propuestas"]:
            self.assertEqual("pendiente_revision", p["estado"])
            self.assertFalse(p["apta_para_evaluacion"])
            self.assertIsNone(p["confianza"])
            for anchor in p["anclas"]:
                self.assertEqual(anchor["cita"], p["texto"][anchor["inicio"]:anchor["fin"]])
        self.assertEqual(15, len(first["controles_sin_perfil"]))
        self.assertEqual({("AC-01", "D1", "linea:2"), ("AC-02", "D1", "linea:1"),
                          ("AC-03", "D1", "linea:3"), ("AC-05", "D3", "linea:2"),
                          ("AC-07", "D2", "linea:1"), ("AC-07", "D2", "linea:2"),
                          ("AC-07", "D3", "linea:1"), ("AC-09", "D3", "linea:1"),
                          ("AC-15", "D2", "linea:3")},
                         {(p["control"], p["documento"], p["ubicacion"]) for p in first["propuestas"]})

    def test_unicode_offsets_and_word_boundaries(self):
        text = "Straße CULMINACIÓN y solicitud"
        anchors = match_groups(text, [["strasse"], ["culminacion"]])
        self.assertEqual(["Straße", "CULMINACIÓN"], [a["cita"] for a in anchors])
        self.assertEqual([], match_groups("penalidad", [["PEN"]]))
        self.assertEqual("CAFE\u0301", match_groups("CAFE\u0301", [["café"]])[0]["cita"])

    def test_pending_never_becomes_evidence(self):
        bundle = propose(self.case)
        cfg = reviewed_config(self.case, bundle, decision_template(bundle))
        self.assertEqual({}, cfg["vinculos"])
        self.assertEqual(0, cfg["revision_evidencias"]["aceptadas"])

    def test_explicit_review_export_and_matrix(self):
        bundle = propose(self.case)
        decisions = self.accept_one(bundle)
        decisions["decisiones"][1].update(decision="rechazada", revisor="REVISOR-SINTETICO",
                                         fecha="2026-10-30T17:00:00-05:00", motivo="Rechazo técnico ficticio")
        before = (self.case / "expediente.json").read_bytes()
        out = self.root / "revisado"
        status = export_reviewed(self.case, bundle, decisions, out)
        self.assertEqual(before, (self.case / "expediente.json").read_bytes())
        self.assertEqual((1, 1), (status["aceptadas"], status["rechazadas"]))
        result = prepare(out, RULES)
        self.assertEqual(1, sum(len(r["evidencias"]) for r in result["matriz"]))
        self.assertEqual({"no_determinable"}, {r["resultado"] for r in result["matriz"]})
        with self.assertRaisesRegex(ValueError, "existe"):
            export_reviewed(self.case, bundle, decisions, out)

    def test_stale_source_and_profile_rejected(self):
        bundle = propose(self.case)
        with (self.case / "solicitud.txt").open("a", encoding="utf-8") as stream:
            stream.write("Información adicional")
        with self.assertRaisesRegex(ValueError, "desactualizadas"):
            reviewed_config(self.case, bundle, decision_template(bundle))
        changed = self.root / "perfil.json"
        profile = load(PROFILE)
        profile["version"] = "CAMBIO-SINTETICO"
        changed.write_bytes(encoded(profile))
        current = propose(self.case)
        with self.assertRaisesRegex(ValueError, "desactualizadas"):
            reviewed_config(self.case, current, decision_template(current), changed)

    def test_modified_proposal_quote_rejected(self):
        bundle = propose(self.case)
        altered = copy.deepcopy(bundle)
        altered["propuestas"][0]["texto"] += "inventado"
        with self.assertRaisesRegex(ValueError, "alteradas"):
            reviewed_config(self.case, altered, decision_template(altered))

    def test_review_requires_identity_time_reason(self):
        bundle = propose(self.case)
        for missing in ("revisor", "fecha", "motivo"):
            decisions = self.accept_one(bundle)
            del decisions["decisiones"][0][missing]
            with self.assertRaises(ValueError):
                reviewed_config(self.case, bundle, decisions)
        decisions = self.accept_one(bundle)
        decisions["decisiones"][0]["fecha"] = "2026-10-30T17:00:00"
        with self.assertRaisesRegex(ValueError, "zona horaria"):
            reviewed_config(self.case, bundle, decisions)

    def test_duplicate_unknown_and_wrong_batch_decisions(self):
        bundle = propose(self.case)
        decisions = self.accept_one(bundle)
        decisions["decisiones"].append(copy.deepcopy(decisions["decisiones"][0]))
        with self.assertRaisesRegex(ValueError, "duplicada"):
            reviewed_config(self.case, bundle, decisions)
        decisions = self.accept_one(bundle)
        decisions["decisiones"][0]["propuesta_id"] = "inexistente"
        with self.assertRaisesRegex(ValueError, "desconocida"):
            reviewed_config(self.case, bundle, decisions)
        decisions = self.accept_one(bundle)
        decisions["lote_sha256"] = "otra"
        with self.assertRaisesRegex(ValueError, "otro lote"):
            reviewed_config(self.case, bundle, decisions)

    def test_reviewed_link_detects_source_quote_and_control_changes(self):
        bundle = propose(self.case)
        cfg = reviewed_config(self.case, bundle, self.accept_one(bundle))
        path = self.case / "expediente.json"
        path.write_bytes(encoded(cfg))
        with (self.case / "solicitud.txt").open("a", encoding="utf-8") as stream:
            stream.write("Cambio posterior")
        with self.assertRaisesRegex(ValueError, "Fuente.*cambió"):
            prepare(self.case, RULES)
        # Reconstituir entrada para verificar una revisión trasladada de control.
        (self.case / "solicitud.txt").write_text(load(ROOT / "tests/fixtures/expedientes/demo.json")["archivos"]["solicitud.txt"], encoding="utf-8", newline="\n")
        control = bundle["propuestas"][0]["control"]
        link = cfg["vinculos"][control][0]
        link["revision_evidencia"]["anclas"][0]["cita"] = "cita alterada"
        path.write_bytes(encoded(cfg))
        with self.assertRaisesRegex(ValueError, "Cita"):
            prepare(self.case, RULES)
        link["revision_evidencia"]["anclas"] = bundle["propuestas"][0]["anclas"]
        cfg["vinculos"] = {"AC-22": [link]}
        path.write_bytes(encoded(cfg))
        with self.assertRaisesRegex(ValueError, "otro control"):
            prepare(self.case, RULES)

    def test_duplicate_noisy_negated_text_and_limit_are_explicit(self):
        cfg = load(self.case / "expediente.json")
        cfg["documentos"].append({"id": "D4", "archivo": "solicitud.txt"})
        (self.case / "expediente.json").write_bytes(encoded(cfg))
        with (self.case / "conformidad.txt").open("a", encoding="utf-8") as stream:
            stream.write("No se acredita conformidad\n")
        profile = load(PROFILE)
        profile["limite_por_control"] = 1
        path = self.root / "perfil.json"
        path.write_bytes(encoded(profile))
        result = propose(self.case, path)
        self.assertGreater(result["visitas_a_documentos_duplicados"], 0)
        self.assertGreater(result["omitidas_por_limite"], 0)
        full = propose(self.case)
        self.assertTrue(any(p["advertencias"] for p in full["propuestas"] if p["texto"].startswith("No se acredita")))

    def test_profile_invalid_and_safe_output(self):
        profile = load(PROFILE)
        profile["controles"][0]["grupos"] = [[""]]
        path = self.root / "perfil.json"
        path.write_bytes(encoded(profile))
        with self.assertRaisesRegex(ValueError, "Términos"):
            propose(self.case, path)
        out = self.root / "lote.json"
        save_new(out, {"demo": 1})
        save_new(out, {"demo": 1})
        with self.assertRaisesRegex(ValueError, "otro contenido"):
            save_new(out, {"demo": 2})

    def test_scanned_pages_stay_out_of_text_proposals(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        writer.write(self.case / "escaneo.pdf")
        cfg = load(self.case / "expediente.json")
        cfg["documentos"].append({"id": "D4", "archivo": "escaneo.pdf"})
        (self.case / "expediente.json").write_bytes(encoded(cfg))
        bundle = propose(self.case)
        self.assertGreater(bundle["visitas_a_fragmentos_con_alerta"], 0)
        self.assertFalse(any(p["documento"] == "D4" for p in bundle["propuestas"]))

    def test_rejection_revokes_previous_link_without_overwriting_input(self):
        bundle = propose(self.case)
        out = self.root / "primera-revision"
        export_reviewed(self.case, bundle, self.accept_one(bundle), out)
        before = (out / "expediente.json").read_bytes()
        current = propose(out)
        decisions = self.accept_one(current)
        decisions["decisiones"][0]["decision"] = "rechazada"
        cfg = reviewed_config(out, current, decisions)
        self.assertEqual(0, sum(len(links) for links in cfg["vinculos"].values()))
        self.assertEqual(before, (out / "expediente.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
