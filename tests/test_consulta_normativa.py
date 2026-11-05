"""Consultas normativas personales: pruebas sin corpus privado ni red."""
from contextlib import closing
from io import BytesIO
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from oece.consulta_normativa import consultar
from oece.comun import sha
from oece.enrutador import ESPECIALISTAS
from oece.mcp_local import Protocolo, CURRENT
from oece.puente import Puente, herramientas


def pdf_con_texto(texto):
    writer = PdfWriter()
    page = writer.add_blank_page(width=600, height=800)
    font = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    }))
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({NameObject("/F1"): font}),
    })
    stream = DecodedStreamObject()
    escaped = texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream.set_data(("BT /F1 12 Tf 20 700 Td (" + escaped + ") Tj ET").encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(stream)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


class ConsultaNormativa(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        env = patch.dict(os.environ, {"OECE_DATA_DIR": str(self.root/"privado")})
        env.start()
        self.addCleanup(env.stop)
        self.path = self.root/"privado/normativa/originales/sintetica/resolucion-demo.pdf"
        self.path.parent.mkdir(parents=True)
        self.text = (
            "Resolucion Directoral 0016-2025. Las subespecialidades y tipologias "
            "de obras se clasifican conforme al listado anexo."
        )
        raw = pdf_con_texto(self.text)
        self.path.write_bytes(raw)
        self.source = {
            "name": "resolucion-demo.pdf",
            "local_path": "normativa/originales/sintetica/resolucion-demo.pdf",
            "instrument_id": "rd-0016-sintetica",
            "kind": "original",
            "source_url": "https://www.gob.pe/institucion/demo/normas-legales/1",
            "source_page": "https://www.gob.pe/institucion/demo",
            "sha256": sha(raw),
        }
        self.db = self.root/"privado/normativa/indices/biblioteca-v1.sqlite"
        self.db.parent.mkdir(parents=True)
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.executescript(
                "CREATE TABLE fuentes(id TEXT PRIMARY KEY,metadata TEXT);"
                "CREATE TABLE fragmentos(id INTEGER PRIMARY KEY,fuente TEXT,"
                " ubicacion TEXT,texto TEXT,alertas TEXT);"
                "CREATE VIRTUAL TABLE buscar USING fts5("
                "id UNINDEXED,texto,tokenize='unicode61 remove_diacritics 2');"
            )
            conn.execute("INSERT INTO fuentes VALUES(?,?)",
                         (self.source["sha256"], json.dumps(self.source)))
            conn.execute("INSERT INTO fragmentos(fuente,ubicacion,texto,alertas)"
                         " VALUES(?,?,?,?)",
                         (self.source["sha256"], "pagina:1", self.text, "[]"))
            conn.execute("INSERT INTO buscar(id,texto) VALUES (?,?)", (1, self.text))
        patches = [
            patch("oece.biblioteca.fuentes", return_value=[self.source]),
            patch("oece.consulta_normativa.fuentes", return_value=[self.source]),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)
        self.bridge = Puente(self.root/"operacion")

    def test_pregunta_directa_sin_expediente_entrega_cita_con_sha(self):
        result = self.bridge.ejecutar(
            "oece_consultar_normativa",
            {"pregunta": "Que dice la Resolucion Directoral 0016-2025 sobre tipologias?",
             "fecha": "2026-11-05"})
        self.assertEqual("evidencia_local_disponible", result["estado"])
        self.assertEqual("consulta_directa_del_titular", result["modo"])
        self.assertFalse(result["requiere_expediente"])
        self.assertFalse(result["invocacion_entre_agentes"])
        self.assertFalse(result["respuesta_generada_por_modelo"])
        self.assertEqual([], list((self.root/"operacion").glob("*/expediente.json")))
        evidence = result["evidencias"][0]
        self.assertEqual("pagina:1", evidence["ubicacion"])
        self.assertEqual(1, evidence["pagina_pdf"])
        self.assertEqual(self.source["sha256"], evidence["sha256"])
        self.assertIn("subespecialidades", evidence["cita_textual_extraida"])
        self.assertEqual(self.source["source_url"], evidence["url_oficial"])
        self.assertFalse(evidence["vigencia_comprobada"])
        self.assertTrue(any("posterior al corte" in x for x in result["pendientes"]))

    def test_consulta_por_termino_especifico_usa_fallback_fts(self):
        result = consultar("Que requisitos sobre tipologias?")
        self.assertEqual("evidencia_local_disponible", result["estado"])
        self.assertEqual(1, len(result["evidencias"]))

    def test_sin_indice_informa_drive_y_no_inventa_articulo(self):
        self.db.unlink()
        result = self.bridge.ejecutar("oece_consultar_normativa",
                                     {"pregunta": "Que dice la RD 0016?"})
        self.assertEqual("sin_indice_local", result["estado"])
        self.assertEqual([], result["evidencias"])
        self.assertIn("drive.google.com", result["biblioteca_drive"])
        self.assertFalse(result["vigencia_verificada"])

    def test_archivo_alterado_no_usa_fragmentos_del_indice(self):
        self.path.write_bytes(self.path.read_bytes() + b"tamper")
        result = consultar("Que dice la resolucion sobre subespecialidades?")
        self.assertEqual("sin_evidencia_cotejada", result["estado"])
        self.assertFalse(result["evidencias"])
        self.assertTrue(any("SHA-256" in x for x in result["pendientes"]))

    def test_indice_con_fuente_no_manifestada_no_es_evidencia(self):
        with patch("oece.consulta_normativa.fuentes", return_value=[]):
            result = consultar("tipologias de obras")
        self.assertEqual("sin_evidencia_cotejada", result["estado"])
        self.assertFalse(result["evidencias"])

    def test_no_entrega_instrucciones_de_documentos_como_ordenes(self):
        result = consultar("Clasificacion de obras")
        self.assertIn("no instrucciones", result["indicaciones_al_asistente"].lower())
        self.assertFalse(result["respuesta_generada_por_modelo"])

    def test_validaciones_de_pregunta_fecha_y_limite(self):
        for question in ("", " ", "a"*501):
            with self.assertRaises(ValueError):
                consultar(question)
        for fecha in ("2026-02-30", "5/11/2026", "not-a-date"):
            with self.assertRaises(ValueError):
                consultar("tipologias", fecha=fecha)
        with self.assertRaises(ValueError):
            consultar("tipologias", limite=True)
        with self.assertRaises(ValueError):
            self.bridge.ejecutar(
                "oece_consultar_normativa", {"pregunta": "tipologias", "caso": "E1"})

    def test_herramienta_mcp_solo_lectura_y_disponible_en_protocolo(self):
        tool = next(x for x in herramientas()
                    if x["name"] == "oece_consultar_normativa")
        self.assertTrue(tool["annotations"]["readOnlyHint"])
        self.assertEqual(["pregunta"], tool["inputSchema"]["required"])
        self.assertNotIn("caso", tool["inputSchema"]["properties"])
        rpc = Protocolo(self.bridge)
        meta = {"io.modelcontextprotocol/protocolVersion": CURRENT,
                "io.modelcontextprotocol/clientCapabilities": {}}
        answer = rpc.manejar({
            "jsonrpc": "2.0", "id": 10, "method": "tools/call",
            "params": {"_meta": meta, "name": "oece_consultar_normativa",
                       "arguments": {"pregunta": "tipologias"}}
        })
        self.assertFalse(answer["result"]["isError"])
        self.assertEqual("evidencia_local_disponible",
                         answer["result"]["structuredContent"]["estado"])

    def test_especialistas_existentes_no_invocan_al_nuevo_agente(self):
        for specialist in ESPECIALISTAS.values():
            self.assertNotIn(
                "oece_consultar_normativa", specialist["herramientas_especializadas"])
        from oece.enrutador import INTRO, INSTRUCCION_CMC, INSTRUCCION_CONSULTORES
        self.assertNotIn("oece_consultar_normativa",
                         INTRO + INSTRUCCION_CMC + INSTRUCCION_CONSULTORES)


if __name__ == "__main__":
    unittest.main()
