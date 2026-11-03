import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from oece.comun import guardar,sha
from oece.flujo import iniciar
from oece.respaldo import crear,restaurar,validar,MANIFEST


class RespaldoTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'data');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.case=self.root/'caso';iniciar(self.case,sintetico=True)
        (self.case/'documentos/original.txt').write_text('Original ficticio',encoding='utf-8')
        guardar(self.case/'auditoria/entradas/version.json',{'dato':'histórico ficticio'})
        guardar(self.case/'salida/revision/conservada.json',{'dato':'entrega ficticia'})
        self.zip=self.root/'respaldo.zip'
    def test_captura_restauracion_identica_y_original_conservado(self):
        result=crear(self.case,self.zip)
        destination=self.root/'recuperado';restaurar(self.zip,destination)
        source={p.relative_to(self.case).as_posix():p.read_bytes() for p in self.case.rglob('*') if p.is_file()}
        restored={p.relative_to(destination).as_posix():p.read_bytes() for p in destination.rglob('*') if p.is_file()}
        self.assertEqual(source,restored);self.assertEqual(len(source),result['archivos']);self.assertTrue(self.case.is_dir())
    def test_no_reemplaza_respaldo_anterior(self):
        crear(self.case,self.zip);raw=self.zip.read_bytes()
        with self.assertRaises(FileExistsError):crear(self.case,self.zip)
        self.assertEqual(raw,self.zip.read_bytes())
    def test_no_sobrescribe_destino_existente(self):
        crear(self.case,self.zip)
        with self.assertRaises(ValueError):restaurar(self.zip,self.case)
        self.assertEqual('Original ficticio',(self.case/'documentos/original.txt').read_text())
    def test_respaldo_dentro_de_caso_rechazado(self):
        with self.assertRaises(ValueError):crear(self.case,self.case/'copia.zip')
    def archive(self,files,records=None):
        records=records or {name:{'bytes':len(raw),'sha256':sha(raw)} for name,raw in files.items()}
        with zipfile.ZipFile(self.zip,'w') as z:
            for name,raw in files.items():z.writestr(name,raw)
            z.writestr(MANIFEST,json.dumps({'version':'1.0.0','expediente':'ficticio','archivos':records}))
    def test_rutas_de_escape_y_nombres_inseguros_rechazados(self):
        for name in ('../fuera.txt','/absoluto.txt','C:/fuera.txt','carpeta/../fuera.txt','CON.txt','a\\b','ruta//doble','ruta./archivo','a:flujo'):
            self.archive({'expediente.json':b'{}',name:b'x'})
            with self.subTest(name=name),self.assertRaises(ValueError):restaurar(self.zip,self.root/'nuevo')
            self.assertFalse((self.root/'nuevo').exists())
    def test_hash_incorrecto_rechazado_sin_publicar(self):
        self.archive({'expediente.json':b'{}'},{'expediente.json':{'sha256':'0'*64,'bytes':2}})
        with self.assertRaises(ValueError):restaurar(self.zip,self.root/'nuevo')
        self.assertFalse((self.root/'nuevo').exists())
    def test_entradas_extra_no_manifestadas_rechazadas(self):
        self.archive({'expediente.json':b'{}','extra.txt':b'x'},{'expediente.json':{'sha256':sha(b'{}'),'bytes':2}})
        with self.assertRaises(ValueError):validar(self.zip)
    def test_nombres_que_colisionan_en_windows_rechazados(self):
        self.archive({'expediente.json':b'{}','A.txt':b'a','a.txt':b'b'})
        with self.assertRaises(ValueError):validar(self.zip)
    def test_enlace_zip_rechazado(self):
        self.archive({'expediente.json':b'{}'})
        with zipfile.ZipFile(self.zip,'a') as z:
            info=zipfile.ZipInfo('enlace');info.create_system=3;info.external_attr=0o120777<<16;z.writestr(info,'fuera')
        with self.assertRaises(ValueError):validar(self.zip)
    def test_limite_de_archivos_y_bytes(self):
        with patch('oece.respaldo.MAX_FILES',1),self.assertRaises(ValueError):crear(self.case,self.zip)
        with patch('oece.respaldo.MAX_BYTES',1),self.assertRaises(ValueError):crear(self.case,self.zip)
    def test_error_de_captura_no_deja_respaldo_incompleto(self):
        with patch('oece.respaldo.zipfile.ZipFile.writestr',side_effect=OSError('Fallo simulado')),self.assertRaises(OSError):crear(self.case,self.zip)
        self.assertFalse(self.zip.exists())
    def test_caso_sin_originales_conserva_carpeta_para_incorporarlos(self):
        empty=self.root/'vacio';iniciar(empty,sintetico=True)
        crear(empty,self.zip);restaurar(self.zip,self.root/'vacio-recuperado')
        self.assertTrue((self.root/'vacio-recuperado/documentos').is_dir())
    def test_reintenta_publicacion_bloqueada_sin_reemplazar_destino(self):
        crear(self.case,self.zip);original=Path.rename;attempts=[]
        def delayed(path,target):
            attempts.append(path.name)
            if len(attempts)<3:raise PermissionError('Bloqueo transitorio simulado')
            return original(path,target)
        with patch.object(Path,'rename',new=delayed):restaurar(self.zip,self.root/'reintento')
        self.assertEqual(3,len(attempts));self.assertTrue((self.root/'reintento/documentos/original.txt').is_file())


if __name__=='__main__':unittest.main()
