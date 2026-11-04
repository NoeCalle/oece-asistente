"""Pruebas de portabilidad de datos privados en Linux, Windows y MCP."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from oece.comun import ROOT, data_dir, ruta_original
from scripts.configurar_cliente import configurar


class RutasPrivadas(unittest.TestCase):
    def test_por_defecto_data_relativa_al_directorio_actual(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop('OECE_DATA_DIR', None)
            self.assertEqual((Path.cwd() / 'data').resolve(), data_dir())

    def test_variable_absoluta_y_relativa(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ, {'OECE_DATA_DIR': temp}):
                self.assertEqual(Path(temp).resolve(), data_dir())
            with patch.dict(os.environ, {'OECE_DATA_DIR': './datos-prueba'}):
                self.assertEqual((Path.cwd() / 'datos-prueba').resolve(), data_dir())

    def test_variable_vacia_rechazada(self):
        with patch.dict(os.environ, {'OECE_DATA_DIR': ' '}):
            with self.assertRaisesRegex(ValueError, 'OECE_DATA_DIR'):
                data_dir()

    def test_original_acepta_separadores_heredados_y_no_escapa(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ, {'OECE_DATA_DIR': temp}):
                target = Path(temp) / 'normativa/originales/prueba.txt'
                target.parent.mkdir(parents=True)
                target.write_text('Ejemplo ficticio', encoding='utf-8')
                self.assertEqual(target.resolve(), ruta_original(r'normativa\originales\prueba.txt'))
                with self.assertRaises(ValueError):
                    ruta_original('../no-autorizado.txt')

    def test_configuracion_mcp_hereda_raiz_y_variable(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ, {'OECE_DATA_DIR': temp}):
                mcp = configurar()['mcpServers']['oece']
                self.assertEqual(str(Path(temp).resolve()), mcp['env']['OECE_DATA_DIR'])
                self.assertEqual(str((Path(temp) / 'operacion').resolve()), mcp['args'][-1])
                extra = configurar(root=Path(temp) / 'otros')['mcpServers']['oece']
                self.assertEqual(str((Path(temp) / 'otros').resolve()), extra['args'][-1])

    def test_panel_usa_variable_cuando_no_hay_raiz_explicita(self):
        from oece.__main__ import main
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ, {'OECE_DATA_DIR': temp}), \
                    patch.object(sys, 'argv', ['oece', 'panel', '--puerto', '8770']), \
                    patch('oece.panel.servir') as run:
                main()
                raiz, memoria, puerto = run.call_args.args
                self.assertEqual((Path(temp) / 'operacion').resolve(), raiz.resolve())
                self.assertEqual((Path(temp) / 'operacion/.oece').resolve(), memoria.root)
                self.assertEqual(8770, puerto)

    def test_mcp_sin_raiz_usa_variable(self):
        with tempfile.TemporaryDirectory() as temp:
            env = {**os.environ, 'OECE_DATA_DIR': temp}
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts/servidor_mcp.py')],
                input=b'', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env=env, cwd=str(ROOT), timeout=15,
            )
            self.assertEqual(0, result.returncode, result.stderr.decode('utf-8', errors='replace'))
            self.assertTrue((Path(temp) / 'operacion/.oece').is_dir())
            self.assertFalse(result.stdout)

    def test_gitignore_mantiene_datos_y_expedientes(self):
        ignores = (ROOT / '.gitignore').read_text(encoding='utf-8').splitlines()
        self.assertIn('data/', ignores)
        self.assertIn('expedientes/', ignores)
        self.assertIn('*.docx', ignores)


if __name__ == '__main__':
    unittest.main()
