"""Tres entregables CMC: datos semánticos, orden y trazabilidad, sin archivos reales."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import json
import threading
from urllib.request import urlopen
from pypdf import PdfWriter

from oece.comun import leer, sha
from oece.formatos_cmc import preparar, validar, publicar, verificar_publicacion
from oece.puente import Puente, herramientas
from oece.flujo import Memoria
from oece.panel import crear_servidor


class TresEntregablesCMC(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bridge = Puente(Path(self.tmp.name) / "operacion")
        self.bridge.ejecutar("oece_nuevo", {"caso": "E-CMC", "procedimiento": "aumento_cmc",
                        "solicitante": "Proveedor sintético", "sintetico": True})
        self.case = Path(self.tmp.name) / "operacion" / "E-CMC"
        for name in ("contrato.pdf", "liquidacion.pdf"):
            w = PdfWriter()
            w.add_blank_page(width=300, height=450)
            with (self.case / "documentos" / name).open("wb") as stream:
                w.write(stream)
        listing = self.bridge.ejecutar("oece_archivos", {"caso": "E-CMC"})["documentos"]
        self.docs = {Path(p["archivo"]).name: p for p in listing}

    def ev(self, name, field, quote):
        return {"campo": field,
                "documento": self.docs[name]["id"], "pagina": 1, "cita": quote}

    def base(self):
        data = self.bridge.ejecutar("oece_modelo_cmc", {"caso": "E-CMC"})["modelo"]
        data["expediente"].update(numero_tramite="TR-001", rnp="RNP-ABC",
                                  fecha_corte="2026-10-31", activo_corriente="3000000.00",
                                  pasivo_corriente="1000000.00")
        data["obras"] = [{
            "id": "OB-01", "objeto": "Construcción de colegio", "entidad": "Entidad de prueba",
            "numero_contrato": "001-2026", "fecha_contrato": "2026-01-10",
            "fecha_recepcion": "2026-08-01", "monto_contrato": "800000.00",
            "moneda_contrato": "PEN", "porcentaje_participacion": "75.00",
            "participacion_aplicada": True, "monto_liquidado": "720000.00",
            "descuento_equipamiento": "10000.00", "otros_descuentos": "5000.00",
            "monto_experiencia": "600000.00", "estado": "propuesta_incluir",
            "motivo_estado": "Sujeto a cotejo de la normativa",
            "anios_marcados": [2026],
            "evidencias": [
                self.ev("contrato.pdf", "fecha_contrato", "Fecha 10/01/2026"),
                self.ev("liquidacion.pdf", "fecha_recepcion", "Recepción agosto 2026"),
                self.ev("liquidacion.pdf", "monto_liquidado", "Liquidado S/720000"),
                self.ev("liquidacion.pdf", "monto_experiencia", "Experiencia 600000"),
                self.ev("contrato.pdf", "porcentaje_participacion", "75% participación"),
            ],
            "observaciones": ["Verificar que la participación no se aplique dos veces"]
        }, {
            "id": "OB-02", "objeto": "Obra desistida", "entidad": None,
            "numero_contrato": None, "fecha_contrato": None, "fecha_recepcion": None,
            "monto_contrato": "300000.00", "moneda_contrato": "PEN",
            "porcentaje_participacion": None, "participacion_aplicada": None,
            "monto_liquidado": None, "descuento_equipamiento": None,
            "otros_descuentos": None, "monto_experiencia": "300000.00",
            "estado": "excluida", "motivo_estado": "Desistimiento a verificar",
            "anios_marcados": [], "evidencias": [
                self.ev("contrato.pdf", "motivo_estado", "DESISTIDO")],
            "observaciones": []
        }]
        for key, value in (("actividad", "1.00"), ("financiero", "0.75"),
                           ("ejecucion", "0.50")):
            data["factores"][key].update(
                valor=value, sustento="Propuesta basada en documental a contrastar",
                norma_por_verificar="Regla vigente por revisar",
                referencias=[{k: v for k, v in self.ev("liquidacion.pdf", "monto_experiencia", "Liquidación").items()
                              if k != "campo"}])
        data["consultas"] = [{"servicio": "RNP de prueba", "realizada": False,
                             "fecha": None, "resultado": "No consultado", "referencias": []}]
        data["observaciones"] = ["Esperar plantillas nativas"]
        return data

    def save(self, data, expected=None):
        return self.bridge.ejecutar("oece_guardar", {
            "caso": "E-CMC", "tipo": "datos_cmc", "contenido": data,
            "sha_esperado": expected})

    def test_modelo_vacio_y_secuencia(self):
        empty = self.bridge.ejecutar("oece_entrada", {"caso": "E-CMC", "tipo": "datos_cmc"})
        self.assertIsNone(empty["sha256"])
        self.assertEqual("cmc-datos-v1", empty["contenido"]["version"])
        self.assertEqual("aumento_cmc", empty["contenido"]["expediente"]["tipo_tramite"])
        self.assertEqual(20, len(herramientas()))

    def test_tres_paquetes_independientes_y_calculo_condicionado(self):
        self.save(self.base())
        result = self.bridge.ejecutar("oece_publicar_cmc", {"caso": "E-CMC"})
        self.assertFalse(result["plantillas_recibidas"])
        self.assertEqual(4, len(result["recursos"]))
        folder = Path(result["carpeta"])
        e1 = leer(folder / "entregable-01-datos.json")
        e2 = leer(folder / "entregable-02-datos.json")
        e3 = leer(folder / "entregable-03-datos.json")
        self.assertEqual(["OB-01", "OB-02"], [v["id"] for v in e1["obras"]])
        self.assertEqual(["OB-01"], e1["obras_propuestas_calculables"])
        self.assertEqual("600000.00", e1["sumatoria_experiencia_parcial_soles"])
        self.assertEqual([2026], e2["obras_y_anios"][0]["anios_marcados"])
        self.assertEqual("2.25", e2["G_provisional"])
        self.assertEqual("1350000.00", e3["CMC_calculada_provisional_soles"])
        self.assertIsNone(e3["CMC_a_otorgar"])
        self.assertEqual("borrador_pendiente_revision", e3["estado"])
        self.assertEqual("datos_listos_para_mapeo", verificar_publicacion(folder)["estado"])
        resource=self.bridge.recurso(result["recursos"][0]["uri"])["contents"][0]
        self.assertIn("entregable_01_datos",resource["text"])
        self.assertEqual("application/json",resource["mimeType"])
        reused = self.bridge.ejecutar("oece_publicar_cmc", {"caso": "E-CMC"})
        self.assertTrue(reused["reutilizada"])

    def test_clasificacion_dga_es_opcional_y_tiene_fuente(self):
        work=self.base()
        work["obras"][0]["especialidad"]="Edificaciones y afines"
        work["obras"][0]["subespecialidad"]="Edificación educativa"
        work["obras"][0]["tipologia"]="Edificación para educación básica"
        work["obras"][0]["evidencias"].append(self.ev(
            "contrato.pdf", "subespecialidad", "Edificación educativa"))
        uno,dos,tres=preparar(self.case,work)
        self.assertEqual("Edificación educativa",
                         dos["obras_y_anios"][0]["clasificacion_dga"]["subespecialidad"])
        self.assertIsNone(tres["CMC_a_otorgar"])
        without=self.base()
        uno2,dos2,tres2=preparar(self.case,without)
        self.assertIsNone(dos2["obras_y_anios"][0]["clasificacion_dga"]["subespecialidad"])
        self.assertEqual(tres["CMC_calculada_provisional_soles"],
                         tres2["CMC_calculada_provisional_soles"])

    def test_documento_sin_evidencia_no_se_cuenta(self):
        sample = self.base()
        sample["obras"][0]["evidencias"] = [
            item for item in sample["obras"][0]["evidencias"]
            if item["campo"] != "monto_experiencia"]
        e1, e2, e3 = preparar(self.case, sample)
        self.assertEqual([], e1["obras_propuestas_calculables"])
        self.assertFalse(e1["sumatoria_completa"])
        self.assertIsNone(e3["CMC_calculada_provisional_soles"])
        self.assertTrue(any("monto_experiencia" in p for p in e3["pendientes"]))

    def test_anos_ausentes_detienen_resultado_final(self):
        sample = self.base()
        sample["obras"][0]["anios_marcados"] = []
        e1, e2, e3 = preparar(self.case, sample)
        self.assertTrue(e1["sumatoria_completa"])
        self.assertIsNone(e3["CMC_calculada_provisional_soles"])
        self.assertTrue(any("años" in p for p in e3["pendientes"]))

    def test_no_deduce_factor_ausente(self):
        sample = self.base()
        sample["factores"]["financiero"]["valor"] = None
        _, e2, e3 = preparar(self.case, sample)
        self.assertIsNone(e2["G_provisional"])
        self.assertIsNone(e3["CMC_calculada_provisional_soles"])

    def test_consorcio_pendiente_sin_doble_aplicar(self):
        sample = self.base()
        sample["obras"][0]["participacion_aplicada"] = None
        e1, _, e3 = preparar(self.case, sample)
        self.assertEqual([], e1["obras_propuestas_calculables"])
        self.assertIsNone(e3["CMC_calculada_provisional_soles"])
        self.assertTrue(any("participacion_aplicada" in p for p in e3["pendientes"]))

    def test_rechaza_documentos_y_paginas_inventados(self):
        sample = self.base()
        for changes in ({"documento": "Dfalso"}, {"pagina": 100}):
            with self.subTest(changes=changes):
                d = deepcopy(sample)
                d["obras"][0]["evidencias"][0].update(changes)
                with self.assertRaises(ValueError):
                    self.save(d)
        self.assertFalse((self.case / "datos-cmc.json").exists())

    def test_rechaza_fuente_sin_obra_o_estado_desconocido(self):
        for modifications in (("estado", "cumple"), ("id", "../salir")):
            with self.subTest(modifications=modifications):
                d = self.base()
                d["obras"][0][modifications[0]] = modifications[1]
                with self.assertRaises(ValueError):
                    validar(self.case, d)

    def test_cambio_crea_revision_nueva_y_conserva_anterior(self):
        data = self.base()
        old_hash = self.save(data)["sha256"]
        original = publicar(self.case)
        changed = deepcopy(data)
        changed["obras"][0]["monto_experiencia"] = "590000.00"
        self.save(changed, expected=old_hash)
        current = publicar(self.case)
        self.assertNotEqual(original["revision"], current["revision"])
        self.assertTrue(Path(original["carpeta"]).exists())
        self.assertEqual("590000.00",
                         leer(Path(current["carpeta"]) / "entregable-01-datos.json")[
                            "sumatoria_experiencia_parcial_soles"])

    def test_alteracion_paquete_detectada(self):
        self.save(self.base())
        result = publicar(self.case)
        folder = Path(result["carpeta"])
        (folder / "entregable-02-datos.json").write_text("CAMBIADO")
        with self.assertRaisesRegex(ValueError, "alterado"):
            verificar_publicacion(folder)
        with self.assertRaisesRegex(ValueError, "alterado"):
            publicar(self.case)

    def test_no_sustituye_nativos_y_no_confunde_ejemplos_fotograficos(self):
        data = self.base()
        data["obras"][0]["monto_experiencia"] = None
        e1, e2, e3 = preparar(self.case, data)
        self.assertIsNone(e3["CMC_calculada_provisional_soles"])
        self.assertNotIn("13612500", str((e1,e2,e3)))
        self.assertNotIn("7400000", str((e1,e2,e3)))
        self.assertFalse((self.case / "entregable-01.xlsx").exists())

    def test_panel_muestra_tres_formatos_y_encargo_al_coordinador(self):
        self.save(self.base())
        prepared=publicar(self.case)
        server=crear_servidor(self.case.parent, Memoria(self.case.parent / ".panel-mem"), 0)
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        base=f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base + "/api/casos", timeout=10) as response:
                cases=json.load(response)["casos"]
            self.assertEqual([prepared["revision"]], cases[0]["paquetes_cmc"])
            with urlopen(base + "/api/pedido-ia?caso=E-CMC", timeout=10) as response:
                prompt=json.load(response)["texto"]
            self.assertIn("oece_modelo_cmc",prompt)
            self.assertIn("oece_publicar_cmc",prompt)
            self.assertIn("TRES ENTREGABLES CMC",prompt)
            with urlopen(base + "/descargar-cmc?caso=E-CMC&revision="
                         + prepared["revision"] + "&archivo=entregable-03-datos.json",
                         timeout=10) as response:
                data=json.load(response)
            self.assertIsNone(data["CMC_a_otorgar"])
            self.assertEqual("1350000.00",data["CMC_calculada_provisional_soles"])
        finally:
            server.shutdown()
            server.server_close()
            server.oece_pool.shutdown(wait=True)
            worker.join()

    def test_carga_cmc_incompatible_con_otro_tramite(self):
        self.bridge.ejecutar("oece_nuevo", {"caso": "OTRO", "procedimiento": "inscripcion",
            "solicitante": "Proveedor", "sintetico": True})
        other = Path(self.tmp.name) / "operacion" / "OTRO" / "documentos"
        other.mkdir(exist_ok=True)
        (other / "origen.pdf").write_bytes((self.case / "documentos" / "contrato.pdf").read_bytes())
        with self.assertRaisesRegex(ValueError, "solo corresponden"):
            self.bridge.ejecutar("oece_guardar", {"caso": "OTRO", "tipo": "datos_cmc",
                "contenido": self.base(), "sha_esperado": None})


if __name__ == "__main__":
    unittest.main()
