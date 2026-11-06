"""Pruebas de lectura XLSX sin libros privados."""
from pathlib import Path
import tempfile
import unittest
import zipfile

from oece.lectura import leer_documento

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def worksheet(value, shared=False):
    typ=' t="s"' if shared else ""
    return (f'<worksheet xmlns="{MAIN}"><sheetData><row r="1">'
            f'<c r="A1"{typ}><v>{value}</v></c>'
            '</row></sheetData></worksheet>').encode("utf-8")


class XLSXGuardias(unittest.TestCase):
    def test_hojas_se_ordenan_numericamente(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            doc=root/"ejemplo.xlsx"
            with zipfile.ZipFile(doc,"w") as z:
                for number in (10,2,1):
                    z.writestr(f"xl/worksheets/sheet{number}.xml",
                               worksheet(number))
            result=leer_documento(doc,root/"cache")
            locations=[v["ubicacion"] for v in result["fragmentos"]]
            self.assertEqual([
                "xl/worksheets/sheet1.xml/celda:A1",
                "xl/worksheets/sheet2.xml/celda:A1",
                "xl/worksheets/sheet10.xml/celda:A1",
            ],locations)

    def test_referencia_de_texto_compartido_invalida(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            doc=root/"invalido.xlsx"
            with zipfile.ZipFile(doc,"w") as z:
                z.writestr("xl/sharedStrings.xml",
                           f'<sst xmlns="{MAIN}"><si><t>OK</t></si></sst>')
                z.writestr("xl/worksheets/sheet1.xml", worksheet("7",shared=True))
            with self.assertRaisesRegex(ValueError,
                                         "Referencia de texto compartido inválida.*sheet1"):
                leer_documento(doc,root/"cache")

    def test_indice_negativo_no_usa_ultimo_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            doc=root/"negativo.xlsx"
            with zipfile.ZipFile(doc,"w") as z:
                z.writestr("xl/sharedStrings.xml",
                           f'<sst xmlns="{MAIN}"><si><t>OK</t></si></sst>')
                z.writestr("xl/worksheets/sheet1.xml", worksheet("-1",shared=True))
            with self.assertRaisesRegex(ValueError,"Referencia de texto compartido inválida"):
                leer_documento(doc,root/"cache")


if __name__ == "__main__":
    unittest.main()
