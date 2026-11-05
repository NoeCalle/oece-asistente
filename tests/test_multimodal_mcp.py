"""Integración de visión y liquidación con clientes MCP, sin APIs ni originales privados."""
import base64
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfWriter

from oece.comun import leer
from oece.mcp_local import Protocolo, CURRENT
from oece.puente import Puente, herramientas
from oece.agentes_ia import verificar_revision


class MCPVisualSinAPI(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name) / "operacion"
        self.bridge = Puente(self.root)
        self.bridge.ejecutar("oece_nuevo", {
            "caso": "E1", "procedimiento": "ampliacion_consultores",
            "solicitante": "Empresa sintética", "sintetico": True})
        self.case = self.root / "E1"
        self.source = self.case / "documentos" / "liquidacion.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=500, height=700)
        writer.add_blank_page(width=500, height=700)
        with self.source.open("wb") as stream:
            writer.write(stream)
        self.doc = self.bridge.ejecutar("oece_archivos", {"caso": "E1"})["documentos"][0]
        self.lectura = {
            "tipo_documento": "Resolución de liquidación",
            "resumen": "Liquidación sintética, lectura no acreditada",
            "datos": [{"campo": "monto_declarado", "valor": "155.00", "pagina": 1,
                       "cita": "Total 155.00", "observacion": "Cotejar página original"}],
            "tablas": [{"pagina": 1, "titulo": "Cuadro de liquidación", "moneda": "PEN",
                        "filas": [{"concepto": "Valorización", "monto": "100.00", "observacion": ""},
                                  {"concepto": "Adicional", "monto": "50.00", "observacion": ""},
                                  {"concepto": "Total", "monto": "155.00", "observacion": ""}]}],
            "alertas": ["Cifras pendientes de cotejo visual"]
        }

    def registro(self, **changes):
        return {"id": self.doc["id"], "archivo": self.doc["archivo"],
                "sha256": self.doc["sha256"], "paginas": 2,
                "lectura": self.lectura, **changes}

    def guardar_lecturas(self, content=None):
        return self.bridge.ejecutar("oece_guardar", {
            "caso": "E1", "tipo": "lecturas_ia",
            "contenido": content if content is not None else [self.registro()],
            "sha_esperado": None})

    def operacion(self):
        did = self.doc["id"]
        return {"descripcion": "Suma", "tipo": "sumar",
                "operandos": [{"documento": did, "pagina": 1, "monto": "100.00"},
                              {"documento": did, "pagina": 1, "monto": "50.00"}],
                "resultado_documento": "155.00",
                "resultado_fuente": {"documento": did, "pagina": 1},
                "comentario": "Cotejar subtotales"}

    def sintesis(self):
        return {"resumen_ejecutivo": "Revisión preliminar de un monto de liquidación.",
                "observaciones": [{"tema": "Diferencia",
                                   "hallazgo": "Diferencia de 5.00 entre suma y monto declarado.",
                                   "accion_sugerida": "Inspeccionar páginas originales.",
                                   "referencias": [{"documento": self.doc["id"], "pagina": 1}]}],
                "pendientes": ["Verificar firmas, autenticidad y normativa aplicable."],
                "conclusion_provisional": "No se ha acreditado el monto."}

    def calcular(self):
        return self.bridge.ejecutar("oece_calcular_liquidacion", {
            "caso": "E1", "operaciones": [self.operacion()], "alertas": []})

    def test_imagen_mcp_real_en_canal_image_no_base64_en_texto(self):
        def fake_render(command, **kwargs):
            Path(str(command[-1]) + ".jpg").write_bytes(b"\xff\xd8" + b"foto-ficticia" + b"\xff\xd9")
            return subprocess.CompletedProcess(command, 0)
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": "oece_pagina_visual",
                              "arguments": {"caso": "E1", "documento": self.doc["id"], "pagina": 2},
                              "_meta": {"io.modelcontextprotocol/protocolVersion": CURRENT,
                                        "io.modelcontextprotocol/clientCapabilities": {}}}}
        with patch("oece.multimodal_mcp.binario", return_value="pdftoppm"), \
             patch("oece.multimodal_mcp.subprocess.run", side_effect=fake_render):
            response = Protocolo(self.bridge).manejar(request)
        result = response["result"]
        self.assertFalse(result["isError"])
        self.assertEqual("image", result["content"][1]["type"])
        self.assertEqual("image/jpeg", result["content"][1]["mimeType"])
        self.assertEqual("foto-ficticia", base64.b64decode(result["content"][1]["data"])[2:-2].decode())
        self.assertEqual(2, result["structuredContent"]["pagina"])
        self.assertNotIn("data", result["structuredContent"])
        self.assertNotIn("foto-ficticia", result["content"][0]["text"])
        self.assertEqual(self.doc["sha256"], result["structuredContent"]["sha256"])

    def test_vision_rechaza_pagina_ajena(self):
        with self.assertRaisesRegex(ValueError, "Página no existe"):
            self.bridge.ejecutar("oece_pagina_visual", {
                "caso": "E1", "documento": self.doc["id"], "pagina": 3})
        with self.assertRaisesRegex(ValueError, "PDF no encontrado"):
            self.bridge.ejecutar("oece_pagina_visual", {
                "caso": "E1", "documento": "D000000000000", "pagina": 1})

    def test_guardar_lecturas_rechaza_fuente_hash_y_pagina_falsas(self):
        for incorrect in ({"sha256": "0" * 64}, {"paginas": 3},
                          {"id": "D000000000000"}):
            with self.subTest(incorrect=incorrect), self.assertRaises(ValueError):
                self.guardar_lecturas([self.registro(**incorrect)])
        self.assertFalse((self.case / "lecturas-ia-trabajo.json").exists())
        self.assertTrue(self.guardar_lecturas()["guardado"])

    def test_cliente_codex_y_claude_comparten_herramientas_sin_api(self):
        self.assertEqual(17, len(herramientas()))
        self.guardar_lecturas()
        computed = self.calcular()
        self.assertEqual("150.00", computed["operaciones"][0]["resultado_decimal"])
        self.assertEqual("-5.00", computed["operaciones"][0]["diferencia_decimal"])
        self.assertEqual("diferencia_aritmetica", computed["operaciones"][0]["estado"])
        for model in ("Codex", "Claude Code"):
            result = self.bridge.ejecutar("oece_publicar_analisis",
                       {"caso": "E1", "modelo": model, "sintesis": self.sintesis()})
            self.assertIn(model, result["modelo"])
            self.assertEqual(4, len(result["recursos"]))
            folder = Path(result["carpeta"])
            self.assertTrue((folder / "informe-ia.docx").read_bytes().startswith(b"PK"))
            self.assertEqual("mcp-local-sin-api", verificar_revision(folder)["origen"])
            payload = leer(folder / "analisis-ia.json")
            self.assertFalse(payload["aprobado"])
            self.assertEqual("pendiente", payload["documentos"][0]["cotejo_visual"])
            binary = self.bridge.recurso(result["recursos"][0]["uri"])
            self.assertEqual("PK", base64.b64decode(binary["contents"][0]["blob"])[:2].decode())
            self.assertTrue(self.bridge.ejecutar("oece_publicar_analisis",
                {"caso": "E1", "modelo": model, "sintesis": self.sintesis()})["reutilizada"])

    def test_no_inventa_calculos_ni_admite_lecturas_sin_sustento(self):
        self.guardar_lecturas()
        edited = self.operacion()
        edited["operandos"][0]["monto"] = "999999.00"
        computed = self.bridge.ejecutar("oece_calcular_liquidacion", {
            "caso": "E1", "operaciones": [edited], "alertas": ["Dato por cotejar"]})
        self.assertEqual("pendiente_cotejo_de_importes", computed["operaciones"][0]["estado"])

    def test_analisis_no_se_publica_sin_calculos(self):
        self.guardar_lecturas()
        with self.assertRaisesRegex(ValueError, "oece_calcular_liquidacion"):
            self.bridge.ejecutar("oece_publicar_analisis",
                {"caso": "E1", "modelo": "Codex", "sintesis": self.sintesis()})

    def test_analisis_no_se_publica_con_referencia_inventada(self):
        self.guardar_lecturas()
        self.calcular()
        bad = self.sintesis()
        bad["observaciones"][0]["referencias"][0]["documento"] = "D000000000000"
        with self.assertRaisesRegex(ValueError, "documento inexistente"):
            self.bridge.ejecutar("oece_publicar_analisis",
                {"caso": "E1", "modelo": "Codex", "sintesis": bad})
        self.assertFalse((self.case / "analisis_ia").exists())

    def test_recalcula_si_alguien_modifica_resultados_almacenados(self):
        self.guardar_lecturas()
        self.calcular()
        path = self.case / "calculos-ia-trabajo.json"
        payload = leer(path)
        payload["resultado"]["operaciones"][0]["resultado_decimal"] = "999.99"
        from oece.comun import guardar
        guardar(path, payload)
        with self.assertRaisesRegex(ValueError, "alterados"):
            self.bridge.ejecutar("oece_publicar_analisis",
                {"caso": "E1", "modelo": "Codex", "sintesis": self.sintesis()})

    def test_mcp_no_necesita_clave_ni_red(self):
        with patch.dict("os.environ", {}, clear=True):
            result = self.bridge.ejecutar("oece_contexto", {})
            self.assertIsNone(result["proveedor_ia"])
            self.assertIn("sin API", result["alcance"])
            self.guardar_lecturas()
            self.assertEqual(1, len(self.calcular()["operaciones"]))


if __name__ == "__main__":
    unittest.main()
