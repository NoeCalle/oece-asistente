"""Regresión portable para rutas heredadas con barras invertidas, índices y SQLite."""
import json
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

from oece.comun import (ROOT, dentro, data_dir, normalizar_registro_rutas,
                        normalizar_ruta_relativa, ruta_original)
from oece.biblioteca import fuentes
from oece.migracion_rutas import migrar, migrar_json, migrar_sqlite
from scripts.indexar_normativa import safe_source


LEGACY = r'normativa\originales\2026-10-29\tupa-modificacion-2026-073.pdf'
POSIX = 'normativa/originales/2026-10-29/tupa-modificacion-2026-073.pdf'


class RutasPosix(unittest.TestCase):
    def test_backslash_path_loaded_as_real_file_on_linux_and_windows(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {'OECE_DATA_DIR': temp}):
            target = Path(temp) / POSIX
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b'PDF ficticio para probar solo ruta')
            self.assertEqual(POSIX, normalizar_ruta_relativa(LEGACY))
            self.assertEqual(target.resolve(), ruta_original(LEGACY))
            self.assertEqual(target.resolve(), dentro(temp, LEGACY))
            # El archivo no se guarda con un nombre que contenga el carácter \ en Linux.
            self.assertTrue(target.is_file())
            self.assertNotIn('\\', normalizar_ruta_relativa(LEGACY))

    def test_indexador_resuelve_manifest_legacy_en_ruta_linux(self):
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / POSIX
            target.parent.mkdir(parents=True)
            target.write_bytes(b'ejemplo')
            result = safe_source(Path(temp), {
                'name': 'tupa-modificacion-2026-073.pdf',
                'local_path': LEGACY,
                'bytes': 7, 'sha256': sha256(b'ejemplo').hexdigest()})
            self.assertEqual(target.resolve(), result)

    def test_no_confunde_regex_con_ruta_ni_modifica_digests(self):
        record = {'fuente': {'local_path': LEGACY, 'sha256': 'a'*64},
                  'pattern': r'^\d{4}-\d{2}$', 'cita': r'texto \\ fórmula'}
        normalized = normalizar_registro_rutas(record)
        self.assertEqual(POSIX, normalized['fuente']['local_path'])
        self.assertEqual(record['pattern'], normalized['pattern'])
        self.assertEqual(record['cita'], normalized['cita'])
        self.assertEqual(record['fuente']['sha256'], normalized['fuente']['sha256'])
        self.assertEqual(normalized, normalizar_registro_rutas(normalized))

    def test_prevents_backslash_traversal_and_windows_absolute(self):
        forbidden = [
            r'..\fuera.pdf', r'normativa\..\fuera.pdf',
            r'C:\Users\Usuario\archivo.pdf', r'C:archivo.pdf',
            r'\\servidor\compartido\archivo.pdf', '/etc/passwd', '.']
        with tempfile.TemporaryDirectory() as temp:
            for value in forbidden:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    dentro(temp, value)

    def test_manifiestos_y_tupa_versionados_son_posix(self):
        actual = fuentes()
        self.assertGreater(len(actual), 40)
        self.assertTrue(all('\\' not in r['local_path'] for r in actual))
        tupa = json.loads((ROOT/'normativa/indice-tupa.v0.1.json').read_text(encoding='utf-8'))
        self.assertEqual(POSIX, tupa['fuente']['local_path'])


class MigrarIndices(unittest.TestCase):
    def test_migracion_json_conserva_citas_y_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'indice-pruebas.json'
            original = {'fuente': {'local_path': LEGACY, 'sha256':'0'*64},
                        'schema': {'pattern': r'\d{4}'}, 'cita': r'\w+\s+TUPA'}
            path.write_text(json.dumps(original), encoding='utf-8')
            report = migrar_json(path)
            self.assertEqual(1, report['cambios'])
            new = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(POSIX, new['fuente']['local_path'])
            self.assertEqual(original['schema'], new['schema'])
            self.assertEqual(original['cita'], new['cita'])
            backup = Path(report['respaldo'])
            self.assertEqual(LEGACY, json.loads(backup.read_text(encoding='utf-8'))['fuente']['local_path'])
            self.assertEqual(0, migrar_json(path)['cambios'])

    def test_migracion_sqlite_conserva_sha_y_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'biblioteca.sqlite'
            with closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE documents (id TEXT PRIMARY KEY, metadata TEXT NOT NULL)')
                db.execute('CREATE TABLE fuentes (id TEXT, local_path TEXT)')
                metadata={'local_path':LEGACY, 'sha256':'b'*64, 'cita':r'9\.\d+'}
                db.execute('INSERT INTO documents VALUES (?,?)',('a',json.dumps(metadata)))
                db.execute('INSERT INTO fuentes VALUES (?,?)',('a',LEGACY))
            result=migrar_sqlite(path)
            self.assertEqual(2,result['cambios'])
            with closing(sqlite3.connect(path)) as db, db:
                row=json.loads(db.execute("SELECT metadata FROM documents WHERE id='a'").fetchone()[0])
                self.assertEqual(POSIX,row['local_path'])
                self.assertEqual('b'*64,row['sha256'])
                self.assertEqual(r'9\.\d+',row['cita'])
                self.assertEqual(POSIX,db.execute('SELECT local_path FROM fuentes').fetchone()[0])
                self.assertEqual('ok',db.execute('PRAGMA integrity_check').fetchone()[0])
            with closing(sqlite3.connect(result['respaldo'])) as db:
                self.assertEqual(LEGACY,db.execute('SELECT local_path FROM fuentes').fetchone()[0])
            self.assertEqual(0,migrar_sqlite(path)['cambios'])

    def test_simulacion_no_modifica_indices(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'indice.json'
            p.write_text(json.dumps({'local_path':LEGACY}),encoding='utf-8')
            before=p.read_bytes()
            result=migrar_json(p,preview=True)
            self.assertEqual(1,result['cambios'])
            self.assertEqual(before,p.read_bytes())
            self.assertNotIn('respaldo',result)

    def test_migracion_auto_de_indices_privados(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'normativa/indices'
            root.mkdir(parents=True)
            p=root/'indice-auxiliar.json'
            p.write_text(json.dumps({'local_path':LEGACY}),encoding='utf-8')
            report=migrar(root)
            self.assertEqual(1,report['cambios'])
            self.assertEqual(POSIX,json.loads(p.read_text(encoding='utf-8'))['local_path'])

    def test_error_de_escape_no_altera_original(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'biblioteca.sqlite'
            with closing(sqlite3.connect(path)) as db, db:
                db.execute('CREATE TABLE documents (id TEXT PRIMARY KEY, metadata TEXT)')
                db.execute('INSERT INTO documents VALUES (?,?)',('1',json.dumps({'local_path':r'..\privado.txt'})))
            original=path.read_bytes()
            with self.assertRaises(ValueError):
                migrar_sqlite(path)
            self.assertEqual(original,path.read_bytes())


if __name__=='__main__':
    unittest.main()
