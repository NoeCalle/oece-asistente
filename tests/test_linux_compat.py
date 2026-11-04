"""Portabilidad Linux/Windows: OCR, host seguro, argumentos y launcher."""
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from oece.comun import ROOT
from oece.flujo import Memoria
from oece.lectura import binario, leer_documento, motor_ocr, ocr_imagen
from oece.panel import crear_servidor


class OCRPortatil(unittest.TestCase):
    def test_binario_poppler_admite_linux_sin_exe(self):
        with patch('oece.lectura.sys.platform', 'linux'), patch('oece.lectura.shutil.which', side_effect=lambda n: '/usr/bin/pdftoppm' if n == 'pdftoppm' else None):
            self.assertEqual('/usr/bin/pdftoppm', binario('pdftoppm.exe'))

    def test_detecta_tesseract_fuera_de_windows(self):
        with patch('oece.lectura.sys.platform', 'linux'), patch('oece.lectura.shutil.which', side_effect=lambda n: '/usr/bin/tesseract' if n == 'tesseract' else None):
            self.assertEqual('Tesseract', motor_ocr())

    def test_prefiere_windows_pero_usa_tesseract_si_falta_powershell(self):
        def which(n):
            return '/bin/tesseract' if n == 'tesseract' else '/bin/powershell.exe' if n == 'powershell.exe' else None
        with patch('oece.lectura.sys.platform', 'win32'), patch('oece.lectura.shutil.which', side_effect=which):
            self.assertEqual('Windows.Media.Ocr', motor_ocr())
        with patch('oece.lectura.sys.platform', 'win32'), patch('oece.lectura.shutil.which', side_effect=lambda n: '/bin/tesseract' if n == 'tesseract' else None):
            self.assertEqual('Tesseract', motor_ocr())

    def test_ocr_tesseract_guarda_cache_y_exige_cotejo(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);image=folder/'imagen.png';Image.new('RGB',(250,80),'white').save(image)
            tsv={'text':['','CONTRATO','123'], 'block_num':[1,1,1], 'par_num':[1,1,1],
                 'line_num':[1,1,1], 'left':[0,12,100], 'top':[0,6,6],
                 'width':[0,75,20], 'height':[0,20,20]}
            with patch('oece.lectura.motor_ocr',return_value='Tesseract'), patch('pytesseract.image_to_data',return_value=tsv) as run:
                a=ocr_imagen(image,folder,'a'*64,1)
                b=ocr_imagen(image,folder,'a'*64,1)
            self.assertEqual('CONTRATO 123',a['text']);self.assertEqual(a,b)
            self.assertEqual('spa',a['language']);self.assertFalse(a['reviewed'])
            self.assertFalse(a['apta_para_evaluacion']);self.assertEqual(1,run.call_count)
            self.assertEqual(45,run.call_args.kwargs['timeout'])
            with patch('oece.lectura.motor_ocr',return_value='Tesseract'),patch('pytesseract.image_to_data',return_value=tsv):
                p=folder/'documento.png';Image.new('RGB',(250,80),'white').save(p)
                d=leer_documento(p,folder/'cache')
            self.assertEqual('Tesseract',d['fragmentos'][0]['motor'])
            self.assertIn('ocr_sin_cotejo_visual',d['fragmentos'][0]['alertas'])

    def test_falta_motor_no_inventa_resultado(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'escaneo.png';Image.new('RGB',(40,40),'white').save(p)
            with patch('oece.lectura.motor_ocr',return_value=None):
                result=leer_documento(p,Path(temp)/'cache')
            self.assertTrue(result['reintentar'])
            self.assertIn('ocr_pendiente',result['fragmentos'][0]['alertas'])

    def test_launcher_existe_y_no_contiene_rutas_windows(self):
        script=(ROOT/'INICIAR_OECE.sh').read_text(encoding='utf-8')
        self.assertIn('python3',script)
        self.assertIn('OECE_HOST',script)
        self.assertNotIn('powershell.exe',script.lower())


class PanelRed(unittest.TestCase):
    def test_bind_modo_servidor_pide_password(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ,{'OECE_PANEL_PASSWORD':'clave-sintetica'}):
                server=crear_servidor(Path(temp),Memoria(Path(temp)/'.oece'),0,host='0.0.0.0')
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            url=f'http://127.0.0.1:{server.server_port}/api/casos'
            try:
                with self.assertRaises(HTTPError) as err:
                    urlopen(url,timeout=10)
                self.assertEqual(401,err.exception.code)
                basic=base64.b64encode(b'oece:clave-sintetica').decode()
                req=Request(url,headers={'Authorization':'Basic '+basic})
                with urlopen(req,timeout=10) as response:
                    self.assertEqual(200,response.status)
                    self.assertEqual([],json.loads(response.read())['casos'])
            finally:
                server.shutdown();server.server_close()
                server.oece_pool.shutdown(wait=True);worker.join()


if __name__=='__main__':
    unittest.main()
