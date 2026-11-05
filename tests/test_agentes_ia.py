"""Pruebas sintéticas: jamás transmiten PDFs ni requieren clave de API."""
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from pypdf import PdfWriter

from oece.agentes_ia import (analizar, comprobar_calculos, decimal, previsualizar,
                             validar_referencias, verificar_revision, OpenAIBackend)
from oece.comun import guardar, leer
from oece.flujo import iniciar, Memoria
from oece.panel import crear_servidor


class ModeloFalso:
    model = "modelo-de-pruebas-sin-red"

    def __init__(self):
        self.llamadas = []
        self.mutar = None

    def leer_pdf(self, path):
        self.llamadas.append(("lector", path.name))
        if self.mutar:
            self.mutar(path)
        return {"tipo_documento": "Resolución de liquidación", "resumen": "Liquidación de prueba",
                "datos": [{"campo": "monto_total", "valor": "155.00", "pagina": 1,
                           "cita": "Liquidación declarada 155.00", "observacion": "Cotejar"}],
                "tablas": [{"pagina": 1, "titulo": "Liquidación", "moneda": "PEN",
                            "filas": [{"concepto": "Valorización", "monto": "100.00", "observacion": ""},
                                      {"concepto": "Adicional", "monto": "50.00", "observacion": ""},
                                      {"concepto": "Total declarado", "monto": "155.00", "observacion": ""}]}],
                "alertas": ["Cifras leídas visualmente; confirmar escaneo"]}

    def razonar(self, etapa, instrucciones, value, schema):
        self.llamadas.append((etapa, value))
        doc = value["documentos"][0]["id"]
        if etapa == "calculos_oece":
            return {"operaciones": [{"descripcion": "Suma de partidas", "tipo": "sumar",
                                     "operandos": [{"documento": doc, "pagina": 1, "monto": "100.00"},
                                                  {"documento": doc, "pagina": 1, "monto": "50.00"}],
                                     "resultado_documento": "155.00",
                                     "resultado_fuente": {"documento": doc, "pagina": 1},
                                     "comentario": "Revisar con PDF"}], "alertas": []}
        return {"resumen_ejecutivo": "Contraste preliminar de una liquidación.",
                "observaciones": [{"tema": "Diferencia de liquidación",
                                   "hallazgo": "La suma de conceptos no concuerda con el total declarado.",
                                   "accion_sugerida": "Cotejar resolución y tabla.",
                                   "referencias": [{"documento": doc, "pagina": 1}]}],
                "pendientes": ["Verificar autenticidad, vigencia y contexto."],
                "conclusion_provisional": "Se requiere revisar el monto."}


class AgentesMultimodales(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "exp-1"
        iniciar(self.folder, sintetico=True)
        self.pdf = self.folder / "documentos" / "liquidacion.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=250)
        with self.pdf.open("wb") as output:
            writer.write(output)
        self.modelo = ModeloFalso()

    def test_consentimiento_explicito_bloquea_sin_red(self):
        with self.assertRaises(PermissionError):
            analizar(self.folder, cliente=self.modelo)
        self.assertEqual([], self.modelo.llamadas)
        self.assertFalse((self.folder / "analisis_ia").exists())

    def test_previsualizar_no_invoca_ia(self):
        preview = previsualizar(self.folder)
        self.assertEqual(1, preview["paginas"])
        self.assertEqual("documentos/liquidacion.pdf", preview["archivos"][0]["archivo"])
        self.assertEqual([], self.modelo.llamadas)

    def test_cadena_lector_calculador_integrador_y_word(self):
        stages = []
        result = analizar(self.folder, autorizar_envio=True, cliente=self.modelo, progress=stages.append)
        self.assertEqual("borrador_ia", result["estado"])
        self.assertEqual(1, result["calculos"])
        self.assertEqual(["leyendo_pdf", "subagente_liquidaciones", "subagente_integrador"], stages)
        self.assertEqual(["lector", "calculos_oece", "sintesis_oece"], [s[0] for s in self.modelo.llamadas])
        path = Path(result["carpeta"])
        self.assertEqual("PK", (path / "informe-ia.docx").read_bytes()[:2].decode())
        self.assertEqual(1, len(verificar_revision(path)["originales"]))
        result_data = leer(path / "analisis-ia.json")
        operation = result_data["calculos"]["operaciones"][0]
        self.assertEqual("150.00", operation["resultado_decimal"])
        self.assertEqual("-5.00", operation["diferencia_decimal"])
        self.assertEqual("diferencia_aritmetica", operation["estado"])
        self.assertEqual("pendiente", result_data["documentos"][0]["cotejo_visual"])
        self.assertFalse(result_data["aprobado"])
        reused = analizar(self.folder, autorizar_envio=True, cliente=self.modelo)
        self.assertTrue(reused["reutilizada"])
        self.assertEqual(3, len(self.modelo.llamadas))

    def test_edicion_de_entrega_hace_fallar_integridad(self):
        result = analizar(self.folder, autorizar_envio=True, cliente=self.modelo)
        path = Path(result["carpeta"])
        (path / "calculos-ia.json").write_text("alterado", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "modificada"):
            verificar_revision(path)
        with self.assertRaisesRegex(ValueError, "modificada"):
            analizar(self.folder, autorizar_envio=True, cliente=self.modelo)

    def test_valida_pagina_inexistente_sin_publicar(self):
        original = self.modelo.leer_pdf
        def corrupt(path):
            data = original(path)
            data["datos"][0]["pagina"] = 9
            return data
        self.modelo.leer_pdf = corrupt
        with self.assertRaisesRegex(ValueError, "página inexistente"):
            analizar(self.folder, autorizar_envio=True, cliente=self.modelo)
        self.assertFalse((self.folder / "analisis_ia").exists())

    def test_pdf_cambiado_mientras_ia_lee_no_publica(self):
        def mutate(path):
            path.write_bytes(path.read_bytes()+b"alterado")
        self.modelo.mutar = mutate
        with self.assertRaisesRegex(ValueError, "cambió"):
            analizar(self.folder, autorizar_envio=True, cliente=self.modelo)
        self.assertFalse((self.folder / "analisis_ia").exists())

    def test_documentos_no_pdf_se_reportan_como_omitidos(self):
        (self.folder / "documentos" / "carta.txt").write_text("Carta", encoding="utf-8")
        preview = previsualizar(self.folder)
        self.assertEqual(["documentos/carta.txt"], preview["omitidos"])
        result = analizar(self.folder, autorizar_envio=True, cliente=self.modelo)
        self.assertEqual(["documentos/carta.txt"], leer(Path(result["carpeta"]) / "analisis-ia.json")["omitidos"])

    def test_decimal_rechaza_texto_y_notacion_ambigua(self):
        for bad in ("1,000.00", "S/ 100", "nan", "1e5", "-Inf", ""):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                decimal(bad)

    def test_calculadora_marca_numeros_no_presentes_en_fuentes(self):
        fake = self.modelo.leer_pdf(self.pdf)
        doc = {"id": "D1", "paginas": 1, "lectura": fake}
        operation = self.modelo.razonar("calculos_oece", "", {"documentos": [doc]}, {})
        operation["operaciones"][0]["operandos"][0]["monto"] = "999.00"
        reviewed = comprobar_calculos(operation, [doc])
        self.assertEqual("pendiente_cotejo_de_importes", reviewed["operaciones"][0]["estado"])

    def test_nunca_acepta_referencias_de_documentos_inexistentes(self):
        doc = {"id": "D1", "paginas": 1}
        synthesis = self.modelo.razonar("sintesis_oece", "", {"documentos": [doc]}, {})
        synthesis["observaciones"][0]["referencias"][0]["documento"] = "inventado"
        with self.assertRaisesRegex(ValueError, "documento inexistente"):
            validar_referencias(synthesis, [doc])

    def test_backend_http_usa_store_false_y_formato_estructurado(self):
        class ClienteSinRed(OpenAIBackend):
            def __init__(self):
                self.key = "clave-falsa"
                self.model = "gpt-4.1"
                self.last_payload = None
            def request(self, path, payload=None, method="POST", mime="application/json"):
                self.last_payload = payload
                return {"status": "completed", "output": [
                    {"type": "message", "content": [
                        {"type": "output_text", "text": '{"ok": true}'}]}]}
        client = ClienteSinRed()
        response = client.responder("ejemplo", "Solo prueba", [{"type":"input_text","text":"ejemplo"}],
                                    {"type":"object", "properties":{"ok":{"type":"boolean"}},
                                     "required":["ok"],"additionalProperties":False})
        self.assertEqual({"ok": True}, response)
        self.assertIs(client.last_payload["store"], False)
        self.assertEqual("json_schema", client.last_payload["text"]["format"]["type"])

    def test_sin_clave_no_usa_api(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                OpenAIBackend()

    def test_panel_mcp_no_invoca_api_ni_requiere_clave(self):
        root = Path(self.temp.name)
        server = crear_servidor(root, Memoria(root / ".oece"), 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = f"http://127.0.0.1:{server.server_port}"
        def request(path, data=None):
            raw = json.dumps(data).encode() if data is not None else None
            headers = {"X-OECE-Token": server.oece_token}
            req = Request(base + path, data=raw, headers=headers)
            with urlopen(req, timeout=15) as response:
                return response.read()
        try:
            with patch.dict(os.environ, {}, clear=True):
                info = json.loads(request("/api/pedido-ia?caso=exp-1"))
                self.assertEqual(1, info["pdf"])
                self.assertIn("mcp", info["modo"].lower())
                self.assertIn("oece_pagina_visual", info["texto"])
                self.assertIn("oece_generar", info["texto"])
                self.assertIn("No uses oece_publicar_cmc", info["texto"])
                self.assertEqual([], self.modelo.llamadas)
                for authorized in (False, True):
                    with self.assertRaises(HTTPError) as ex:
                        request("/api/analizar-ia", {"caso": "exp-1",
                                                    "autorizar_envio": authorized})
                    self.assertEqual(400, ex.exception.code)
                self.assertFalse((self.folder / "analisis_ia").exists())
        finally:
            server.shutdown()
            server.server_close()
            server.oece_pool.shutdown(wait=True)
            worker.join()


if __name__ == "__main__":
    unittest.main()
