"""Regresión de enrutamiento agnóstico: un coordinador, dos especialidades aisladas."""
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import urlopen

from pypdf import PdfWriter

from oece.comun import guardar, leer
from oece.enrutador import coordinar
from oece.flujo import Memoria
from oece.panel import crear_servidor
from oece.puente import Puente, herramientas


class CoordinadorDual(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)/"operacion"
        self.bridge=Puente(self.root)
        self.bridge.ejecutar("oece_nuevo", {
            "caso":"CMC1","procedimiento":"aumento_cmc",
            "solicitante":"Empresa ficticia CMC","sintetico":True})
        self.bridge.ejecutar("oece_nuevo", {
            "caso":"CONS1","procedimiento":"ampliacion_consultores",
            "solicitante":"Consultor ficticio","sintetico":True})

    def route(self, case):
        return self.bridge.ejecutar("oece_coordinar",{"caso":case})

    def test_un_mismo_coordinador_enruta_ambos_sin_pdf_ni_api(self):
        with patch.dict(os.environ, {}, clear=True):
            cmc=self.route("CMC1")
            consultor=self.route("CONS1")
        self.assertEqual(21,len(herramientas()))
        self.assertEqual("aumento_cmc",cmc["procedimiento"])
        self.assertEqual("ampliacion_consultores",consultor["procedimiento"])
        self.assertEqual(0,cmc["pdf"])
        self.assertEqual(0,consultor["pdf"])
        self.assertEqual(5,len(cmc["fases"]))
        self.assertEqual(5,len(consultor["fases"]))
        self.assertEqual("cliente_ia_mcp_agnostico_sin_api_propia",cmc["operacion"])
        self.assertFalse(cmc["plan_documental"]["verificado_con_originales"])
        self.assertFalse(consultor["plan_documental"]["verificado_con_originales"])
        self.assertIn("Cargar los originales",cmc["pendientes"][0])

    def test_cmc_activa_solo_tres_formatos_y_calculos(self):
        plan=self.route("CMC1")
        self.assertIn("TRES ENTREGABLES CMC",plan["texto"])
        self.assertIn("oece_publicar_cmc",plan["texto"])
        self.assertIn("oece_modelo_cmc",plan["texto"])
        self.assertIn("oece_calcular_liquidacion",plan["herramientas_especializadas"])
        self.assertEqual(4,len(plan["entregables"]))
        self.assertNotIn("oece_generar",plan["herramientas_especializadas"])
        self.assertIn("CMC",plan["especialista"])

    def test_consultores_activa_controles_ac_y_no_tres_formatos(self):
        plan=self.route("CONS1")
        self.assertIn("oece_generar",plan["texto"])
        self.assertIn("controles AC",plan["texto"])
        self.assertIn("historial RNP",plan["texto"])
        self.assertEqual(3,len(plan["entregables"]))
        self.assertNotIn("oece_publicar_cmc",plan["herramientas_especializadas"])
        self.assertNotIn("oece_calcular_liquidacion",plan["herramientas_especializadas"])
        self.assertIn("CONSULTOR",plan["texto"])

    def test_bloquea_mover_herramientas_cmc_a_consultores(self):
        for tool,args in [
            ("oece_modelo_cmc", {"caso":"CONS1"}),
            ("oece_publicar_cmc", {"caso":"CONS1"}),
            ("oece_entrada", {"caso":"CONS1","tipo":"datos_cmc"}),
            ("oece_calcular_liquidacion",
             {"caso":"CONS1","operaciones":[],"alertas":[]}),
        ]:
            with self.subTest(tool=tool), self.assertRaises(ValueError):
                self.bridge.ejecutar(tool,args)
        # El caso CMC sí tiene acceso al contrato de sus formatos.
        expected=self.bridge.ejecutar("oece_modelo_cmc",{"caso":"CMC1"})
        self.assertEqual("cmc-datos-v1",expected["modelo"]["version"])

    def test_plan_se_actualiza_con_ficha_pero_no_por_nombre_del_pdf(self):
        case=self.root/"CONS1"
        pdf=case/"documentos"/"CONTRATO_AUMENTO_CMC.pdf"
        writer=PdfWriter()
        writer.add_blank_page(width=200,height=300)
        with pdf.open("wb") as stream:writer.write(stream)
        still_consultor=self.route("CONS1")
        self.assertEqual("ampliacion_consultores",still_consultor["procedimiento"])
        self.assertEqual(1,still_consultor["pdf"])
        cfg=leer(case/"expediente.json")
        cfg["categoria_solicitada"]="b"
        guardar(case/"expediente.json",cfg)
        updated=self.route("CONS1")
        self.assertNotIn("Precisar categoría solicitada y régimen aplicable",updated["pendientes"])
        self.assertEqual("ampliacion_consultores",updated["procedimiento"])

    def test_identidad_distinta_rechaza_inyeccion_de_ruta(self):
        path=self.root/"CONS1"/"expediente.json"
        config=leer(path)
        config["id"]="CMC1"
        guardar(path,config)
        with self.assertRaisesRegex(ValueError,"identidad"):
            coordinar(self.root/"CONS1")

    def test_no_presenta_cobertura_dual_para_otros_tres_procedimientos(self):
        self.bridge.ejecutar("oece_nuevo", {
            "caso":"OTRO","procedimiento":"inscripcion",
            "solicitante":"Ejemplo","sintetico":True})
        with self.assertRaisesRegex(ValueError,"Coordinación especializada"):
            self.route("OTRO")

    def test_panel_usa_exactamente_las_dos_rutas_mcp(self):
        server=crear_servidor(self.root,Memoria(self.root/".mem-web"),0)
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            for case,specialist in (("CMC1","aumento_cmc"),
                                    ("CONS1","ampliacion_consultores")):
                with urlopen(f"http://127.0.0.1:{server.server_port}/api/pedido-ia?caso={case}",
                             timeout=10) as response:
                    plan=json.load(response)
                self.assertEqual(specialist,plan["procedimiento"])
                self.assertEqual(0,plan["pdf"])
                self.assertIn("oece_coordinar",plan["texto"])
                self.assertIn("mcp",plan["modo"].lower())
                self.assertTrue(plan["entregables"])
        finally:
            server.shutdown()
            server.server_close()
            server.oece_pool.shutdown(wait=True)
            worker.join()


if __name__=="__main__":
    unittest.main()
