"""Agente de consulta normativa de suscripción: Drive primero, web con aviso.

Prueba la ruta declarativa del servidor MCP, no la conexión real de clientes a
Google Drive o a buscadores externos.
"""
import unittest

from oece.consulta_normativa import (
    AVISO_FUENTE_EXTERNA, DRIVE_BIBLIOTECA, DRIVE_ID, consultar
)
from oece.enrutador import ESPECIALISTAS, INTRO, INSTRUCCION_CMC, INSTRUCCION_CONSULTORES
from oece.mcp_local import CURRENT, Protocolo
from oece.puente import Puente, herramientas
import tempfile
from pathlib import Path


class ConsultaNormativaDriveFirst(unittest.TestCase):
    def test_consulta_no_exige_descarga_expediente_ni_indice_local(self):
        with tempfile.TemporaryDirectory() as root:
            bridge = Puente(Path(root) / "operacion")
            result = bridge.ejecutar("oece_consultar_normativa", {
                "pregunta": "¿Qué indica la RD 0016-2025 sobre tipologías?",
                "fecha": "2026-11-05",
            })
            self.assertEqual("pendiente_busqueda_drive_por_cliente", result["estado"])
            self.assertEqual(DRIVE_BIBLIOTECA, result["biblioteca_drive"])
            self.assertEqual(DRIVE_ID, result["id_carpeta_drive"])
            self.assertFalse(result["requiere_expediente"])
            self.assertFalse(result["requiere_copia_local"])
            self.assertFalse(result["requiere_indice_local"])
            self.assertFalse(result["requiere_api_oece"])
            self.assertEqual([], result["evidencias"])
            self.assertFalse(result["el_servidor_mcp_leyo_drive"])
            self.assertFalse(result["el_servidor_mcp_consulto_internet"])
            self.assertEqual([], list((Path(root) / "operacion").glob("*/expediente.json")))

    def test_drive_primero_y_web_solo_por_insuficiencia_con_aviso(self):
        result = consultar("¿Qué regula una resolución?")
        drive, internet = result["protocolo"]
        self.assertEqual("drive", drive["origen"])
        self.assertEqual("internet", internet["origen"])
        self.assertIn("conector de Google Drive", drive["accion"])
        self.assertIn("subcarpetas", drive["accion"])
        self.assertIn("ÚNICAMENTE", internet["condicion"])
        self.assertIn("ANTES", internet["accion"])
        self.assertEqual(AVISO_FUENTE_EXTERNA, internet["aviso_previo_obligatorio"])
        self.assertIn("Biblioteca Drive", result["formato_respuesta"])
        self.assertIn("Internet", result["formato_respuesta"])

    def test_no_afirma_ausencia_si_conector_inaccesible(self):
        result = consultar("¿Qué dice la norma?")
        self.assertIn("NO decir", result["si_drive_no_es_accesible"])
        self.assertIn("no equivale a no encontrar", result["protocolo"][1]["condicion"])
        self.assertTrue(result["biblioteca_drive"].startswith("https://drive.google.com/drive/folders/"))

    def test_sin_revision_normativa_automatica_ni_otra_api(self):
        result = consultar("¿Qué dice el artículo 2?", limite=3)
        self.assertEqual(3, result["limite_fuentes_sugerido"])
        self.assertFalse(result["respuesta_generada_por_modelo"])
        self.assertFalse(result["requiere_api_oece"])
        self.assertIn("ni llamar a agentes CMC", result["restricciones"])
        self.assertIn("no inventar citas", result["formato_respuesta"])

    def test_valida_pregunta_fecha_y_limite(self):
        for question in ("", " ", "a"*501):
            with self.subTest(question=question[:6]), self.assertRaises(ValueError):
                consultar(question)
        for date_str in ("2026-02-30", "5/11/2026", "not-a-date"):
            with self.subTest(fecha=date_str), self.assertRaises(ValueError):
                consultar("tipologías", fecha=date_str)
        for limit in (True, 0, 11, -1):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                consultar("tipologías", limite=limit)

    def test_solo_lectura_mcp_sin_parametro_de_caso(self):
        tool = next(t for t in herramientas() if t["name"] == "oece_consultar_normativa")
        self.assertTrue(tool["annotations"]["readOnlyHint"])
        self.assertNotIn("caso", tool["inputSchema"]["properties"])
        self.assertEqual(["pregunta"], tool["inputSchema"]["required"])
        with tempfile.TemporaryDirectory() as root:
            bridge = Puente(root)
            rpc = Protocolo(bridge)
            req = {
                "jsonrpc": "2.0", "id": 1, "method": "tools/call",
                "params": {
                    "_meta": {
                        "io.modelcontextprotocol/protocolVersion": CURRENT,
                        "io.modelcontextprotocol/clientCapabilities": {},
                    },
                    "name": "oece_consultar_normativa",
                    "arguments": {"pregunta": "¿Qué es una subespecialidad?"},
                },
            }
            data = rpc.manejar(req)["result"]
            self.assertFalse(data["isError"])
            self.assertEqual("pendiente_busqueda_drive_por_cliente",
                             data["structuredContent"]["estado"])

    def test_especialistas_no_invocan_consulta_personal(self):
        for specialist in ESPECIALISTAS.values():
            self.assertNotIn("oece_consultar_normativa",
                             specialist["herramientas_especializadas"])
        self.assertNotIn("oece_consultar_normativa",
                         INTRO + INSTRUCCION_CMC + INSTRUCCION_CONSULTORES)


if __name__ == "__main__":
    unittest.main()
