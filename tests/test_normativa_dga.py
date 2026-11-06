"""RD 0016 DGA: fuente transversal, original privado y verificación sin red."""
from contextlib import closing
from io import BytesIO
from pathlib import Path
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject

from oece.biblioteca import fuentes, leer_fuente
from oece.comun import leer, sha
from oece.normativa_incorporacion import catalogo, estado_norma, incorporar, _comprobar_pdf, _descargar
from oece.puente import Puente


def pdf_de_prueba(text):
    writer=PdfWriter()
    page=writer.add_blank_page(width=600,height=800)
    font=DictionaryObject({
        NameObject("/Type"):NameObject("/Font"),
        NameObject("/Subtype"):NameObject("/Type1"),
        NameObject("/BaseFont"):NameObject("/Helvetica"),
    })
    ref=writer._add_object(font)
    page[NameObject("/Resources")]=DictionaryObject({
        NameObject("/Font"):DictionaryObject({NameObject("/F1"):ref}),
    })
    stream=DecodedStreamObject()
    escaped=text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream.set_data(("BT /F1 12 Tf 20 700 Td ("+escaped+") Tj ET").encode("ascii"))
    page[NameObject("/Contents")]=writer._add_object(stream)
    out=BytesIO()
    writer.write(out)
    return out.getvalue()


class FuentesTransversales(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        patcher=patch.dict(os.environ, {"OECE_DATA_DIR":str(self.root/"data")})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.item=catalogo()[0]
        self.original=pdf_de_prueba(
            "Resolucion Directoral 0016-2025-EF/54.01. Listado de "
            "Subespecialidades y Tipologias de Obras y Consultoria de Obras.")
        self.input=self.root/"src-rd0016.pdf"
        self.input.write_bytes(self.original)

    def test_catalogo_es_para_ambos_procedimientos(self):
        self.assertEqual("rd-0016-2025-ef-54-01",self.item["id"])
        self.assertEqual({"aumento_cmc","ampliacion_consultores"},
                         set(self.item["aplicacion"]))
        self.assertEqual(5,len(self.item["especialidades_reglamento_art_157_2"]))
        self.assertEqual("2025-05-10",self.item["fecha_publicacion"])
        self.assertFalse(estado_norma(self.item)["incorporada_biblioteca"])

    def test_registro_local_original_sha_y_lectura_documental(self):
        result=incorporar(self.item["id"],archivo=self.input)
        self.assertEqual("original_registrado",result["estado"])
        self.assertEqual(sha(self.original),result["sha256"])
        self.assertFalse(result["fuente_confirmada_por_descarga"])
        self.assertFalse(result["vigencia_verificada"])
        self.assertTrue(Path(result["archivo"]).exists())
        manifest=leer(result["manifiesto_privado"])
        self.assertEqual("adicionales-v1",manifest["version"])
        self.assertEqual(1,len(manifest["archivos"]))
        self.assertTrue(manifest["archivos"][0]["verificacion"]["cotejo_fuente_manual_pendiente"])
        self.assertEqual(self.item["nombre_archivo"],
                         fuentes()[-1]["name"])
        detail=leer_fuente(self.item["nombre_archivo"],pagina=1)
        self.assertIn("0016-2025-EF/54.01",detail["texto"])
        self.assertTrue(estado_norma(self.item)["original_verificado"])
        self.assertFalse(estado_norma(self.item)["indice_actualizado"])
        self.assertEqual("ya_registrada",
                         incorporar(self.item["id"],archivo=self.input)["estado"])

    def test_indice_reportado_solo_si_realmente_contiene_el_sha(self):
        incorporar(self.item["id"],archivo=self.input)
        idx=self.root/"data/normativa/indices/biblioteca-v1.sqlite"
        idx.parent.mkdir(parents=True)
        with closing(sqlite3.connect(idx)) as c, c:
            c.execute("CREATE TABLE fuentes(id TEXT PRIMARY KEY, metadata TEXT)")
            c.execute("INSERT INTO fuentes VALUES(?,?)",(sha(self.original),"{}"))
        self.assertTrue(estado_norma(self.item)["indice_actualizado"])

    def test_descarga_oficial_registra_procedencia_no_firma(self):
        with patch("oece.normativa_incorporacion._descargar",return_value=self.original) as mock:
            result=incorporar(self.item["id"],descargar=True)
        mock.assert_called_once_with(self.item["pdf_oficial"])
        self.assertTrue(result["fuente_confirmada_por_descarga"])
        manifest=leer(result["manifiesto_privado"])
        self.assertFalse(manifest["archivos"][0]["firma_digital_verificada"])

    def test_fuente_falsa_y_url_insegura_no_se_importan(self):
        fake=pdf_de_prueba("Resolucion no relacionada ni verificada")
        with self.assertRaisesRegex(ValueError,"no se identifica"):
            _comprobar_pdf(fake,self.item)
        with self.assertRaisesRegex(ValueError,"oficial"):
            _descargar("https://otro-ejemplo.invalid/documento.pdf")
        with self.assertRaisesRegex(ValueError,"exactamente una"):
            incorporar(self.item["id"])

    def test_identificacion_pdf_por_marcadores_propios_de_otra_norma(self):
        other = {"id":"rd-9999-2027-ef", "marcadores_pdf":["9999-2027", "REGLAMENTO"]}
        valid = pdf_de_prueba("Resolucion 9999-2027 REGLAMENTO")
        self.assertEqual(1, _comprobar_pdf(valid,other)["paginas"])
        with self.assertRaisesRegex(ValueError,"no se identifica"):
            _comprobar_pdf(self.original,other)
        with self.assertRaisesRegex(ValueError,"marcadores"):
            _comprobar_pdf(valid,{"id":"rd-9999-2027-ef"})

    def test_original_modificado_no_se_sustituye(self):
        result=incorporar(self.item["id"],archivo=self.input)
        Path(result["archivo"]).write_bytes(self.original+b"modificado")
        status=estado_norma(self.item)
        self.assertFalse(status["original_verificado"])
        with self.assertRaisesRegex(ValueError,"alterado"):
            incorporar(self.item["id"],archivo=self.input)

    def test_dos_coordinadores_misma_fuente_con_criterios_diferentes(self):
        bridge=Puente(self.root/"data/operacion")
        for name,procedure in (("E1","aumento_cmc"),
                               ("C1","ampliacion_consultores")):
            bridge.ejecutar("oece_nuevo",{"caso":name,"procedimiento":procedure,
                           "solicitante":"Empresa de prueba","sintetico":True})
        first=bridge.ejecutar("oece_coordinar",{"caso":"E1"})
        second=bridge.ejecutar("oece_coordinar",{"caso":"C1"})
        norm1=first["fuentes_normativas_transversales"][0]
        norm2=second["fuentes_normativas_transversales"][0]
        self.assertEqual(norm1["id"],norm2["id"])
        self.assertFalse(norm1["estado_local"]["original_verificado"])
        self.assertIn("liquidación",first["texto"])
        self.assertIn("categoría",second["texto"])
        self.assertNotEqual(norm1["alcance_procedimiento"],
                            norm2["alcance_procedimiento"])
        incorporar(self.item["id"],archivo=self.input)
        after=bridge.ejecutar("oece_coordinar",{"caso":"C1"})
        self.assertTrue(after["fuentes_normativas_transversales"][0]
                            ["estado_local"]["original_verificado"])
        self.assertEqual("ampliacion_consultores",after["procedimiento"])


if __name__=="__main__":
    unittest.main()
