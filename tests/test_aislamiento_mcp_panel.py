"""Pruebas sintéticas de aislamiento del MCP y autenticación del panel."""
import base64
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from oece.flujo import Memoria
from oece.panel import anunciar_autenticacion, crear_servidor
from oece.puente import Puente


class MCPIsolation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("E1", "E2"):
            case = self.root / name
            (case / "documentos").mkdir(parents=True)
            (case / "expediente.json").write_text(
                json.dumps({"id":name, "solicitante":name,
                            "procedimiento":"aumento_cmc"}), encoding="utf-8")
        self.bridge = Puente(self.root, caso_autorizado="E1")

    def test_sesion_no_lista_ni_lee_casos_ajenos(self):
        cases = self.bridge.ejecutar("oece_listar", {})
        self.assertEqual(["E1"], [x["caso"] for x in cases["casos"]])
        with self.assertRaisesRegex(ValueError, "sesión MCP"):
            self.bridge.ejecutar("oece_archivos", {"caso":"E2"})
        with self.assertRaises(ValueError):
            self.bridge.ejecutar("oece_nuevo",
                                {"caso":"E1", "procedimiento":"aumento_cmc",
                                 "solicitante":"Nuevo"})
        with self.assertRaises(ValueError):
            self.bridge.recurso("oece://casos/E2/salida/" + "a"*64 + "/matriz.json")

    def test_no_se_puede_incorporar_desde_otro_expediente(self):
        incoming = self.root / "entrada" / "E1"
        incoming.mkdir(parents=True)
        staged = incoming / "contrato.txt"
        staged.write_text("Original sintético", encoding="utf-8")
        other = self.root / "E2" / "documentos" / "privado.txt"
        other.write_text("OTRO EXPEDIENTE", encoding="utf-8")
        result = self.bridge.ejecutar("oece_incorporar",
                                     {"caso":"E1", "origen":"contrato.txt"})
        self.assertTrue(result["incorporado"])
        self.assertEqual(staged.read_bytes(),
                         (self.root/"E1"/"documentos"/"contrato.txt").read_bytes())
        with self.assertRaises(ValueError):
            self.bridge.ejecutar("oece_incorporar",
                                 {"caso":"E1",
                                  "origen":"../../E2/documentos/privado.txt"})
        with self.assertRaises(ValueError):
            self.bridge.ejecutar("oece_incorporar",
                                 {"caso":"E1", "origen":"../E2/privado.txt"})
        with self.assertRaises(ValueError):
            self.bridge.ejecutar("oece_incorporar",
                                 {"caso":"E2", "origen":"contrato.txt"})
        self.assertEqual("OTRO EXPEDIENTE", other.read_text(encoding="utf-8"))

    def test_enlace_simbolico_en_entrada_no_permitido(self):
        incoming = self.root/"entrada"/"E1"
        incoming.mkdir(parents=True)
        other = self.root/"E2"/"documentos"/"privado.txt"
        other.write_text("X", encoding="utf-8")
        link = incoming/"atajo.txt"
        try:
            link.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest("Sistema sin permisos para enlaces simbólicos")
        with self.assertRaises(ValueError):
            self.bridge.ejecutar("oece_incorporar",
                                 {"caso":"E1", "origen":"atajo.txt"})


class PanelAuthentication(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def start_server(self, configured=True):
        vars={"OECE_PANEL_PASSWORD":"clave-configurada"} if configured else {}
        with patch.dict(os.environ,vars,clear=True):
            server=crear_servidor(self.root,Memoria(self.root/".oece"),0,
                                  host="0.0.0.0")
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        def cleanup():
            server.shutdown()
            server.server_close()
            server.oece_pool.shutdown(wait=True)
            worker.join(timeout=3)
        self.addCleanup(cleanup)
        return server

    def test_clave_de_entorno_no_aparece_en_anuncio(self):
        with patch.dict(os.environ,{"OECE_PANEL_PASSWORD":"secreto-no-loggear"}):
            server=crear_servidor(self.root,Memoria(self.root/".oece"),0,
                                  host="0.0.0.0")
        try:
            output=io.StringIO()
            with redirect_stdout(output):
                anunciar_autenticacion(server)
            self.assertNotIn("secreto-no-loggear",output.getvalue())
            self.assertIn("oculta",output.getvalue())
            self.assertFalse(server.oece_password_generated)
        finally:
            server.server_close()
            server.oece_pool.shutdown(wait=True)

    def test_clave_aleatoria_solo_si_se_genero(self):
        with patch.dict(os.environ,{},clear=True):
            server=crear_servidor(self.root,Memoria(self.root/".oece"),0,
                                  host="0.0.0.0")
        try:
            output=io.StringIO()
            with redirect_stdout(output):
                anunciar_autenticacion(server)
            self.assertTrue(server.oece_password_generated)
            self.assertIn(server.oece_password,output.getvalue())
        finally:
            server.server_close()
            server.oece_pool.shutdown(wait=True)

    def test_limitacion_de_intentos_auth_basica(self):
        server=self.start_server()
        url=f"http://127.0.0.1:{server.server_port}/api/casos"
        wrong="Basic "+base64.b64encode(b"oece:incorrecta").decode()
        for attempt in range(5):
            req=Request(url,headers={"Authorization":wrong})
            with self.assertRaises(HTTPError) as error:
                urlopen(req,timeout=5)
            self.assertEqual(429 if attempt==4 else 401,error.exception.code)
        valid="Basic "+base64.b64encode(b"oece:clave-configurada").decode()
        with self.assertRaises(HTTPError) as locked:
            urlopen(Request(url,headers={"Authorization":valid}),timeout=5)
        self.assertEqual(429,locked.exception.code)


if __name__ == "__main__":
    unittest.main()
