import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from oece.comun import guardar,leer
from oece.preparacion import REGISTRO,planificar,verificar
from oece.diagnostico import comprobar
from construir_requisitos_completos import construir
from test_operacion_v1 import ficha


class PreparacionV16(unittest.TestCase):
    def config(self,**extra):
        return {**ficha(),'procedimiento':'inscripcion','tipo_registro':'bienes','tipo_tramite':'inscripcion',**extra}
    def test_catalogo_cubre_cinco_tramites_y_124_unidades(self):
        registry=leer(REGISTRO)
        self.assertEqual(124,len(registry['requisitos']))
        self.assertEqual(124,len({r['id'] for r in registry['requisitos']}))
        self.assertEqual({'inscripcion','ampliacion_consultores','aumento_cmc','actualizacion','reconsideracion'},{r['procedimiento'] for r in registry['requisitos']})
    def test_verificacion_integra_de_153_citas_y_cinco_originales(self):
        result=verificar();self.assertEqual(153,result['citas_literales']);self.assertEqual(178,result['referencias']);self.assertEqual(5,result['originales'])
    def test_reconstruccion_reproducible_incluye_trece_fichas(self):
        registry=construir();self.assertEqual(leer(REGISTRO),registry)
        self.assertEqual(13,len({r['codigo_tupa'] for r in registry['requisitos'] if r['procedimiento']=='inscripcion'}))
    def test_inscripcion_bienes_no_hereda_documentos_de_obras(self):
        c=self.config(tipo_persona='natural',origen_proveedor='nacional',domicilio='domiciliado')
        r=planificar(c);self.assertEqual(2,len(r['tareas']))
        self.assertEqual({'PA42004846'},{x['codigo_tupa'] for x in r['catalogo']});self.assertEqual([],r['alertas_exclusion'])
    def test_ocho_ramas_de_obras_seleccionan_solo_su_ficha(self):
        for register in ('consultor','ejecutor'):
            for person in ('natural','juridica'):
                for origin in ('nacional','extranjero'):
                    r=planificar(self.config(tipo_registro=register,tipo_persona=person,origen_proveedor=origin,domicilio='domiciliado'))
                    self.assertEqual(1,len({x['codigo_tupa'] for x in r['catalogo']}));self.assertTrue(r['tareas']);self.assertEqual(10,len(r['alertas_exclusion']))
    def test_faltantes_conservan_alternativas_sin_seleccion_universal(self):
        r=planificar({'procedimiento':'inscripcion','fecha_solicitud':'2026-10-30'})
        self.assertEqual(63,len(r['tareas']));self.assertEqual({'no_determinable'},{t['seleccion_documental'] for t in r['tareas']})
    def test_recorte_alterado_o_cita_trasladada_se_rechaza(self):
        registry=leer(REGISTRO);entry=next(r for r in registry['requisitos'] if r['procedimiento']=='inscripcion')
        entry['fuentes'][0]['bbox']=[0,0,10,10]
        with self.assertRaises(ValueError):verificar(registry)
    def test_anexo_word_conserva_celdas_combinadas_y_citas(self):
        entries=[r for r in leer(REGISTRO)['requisitos'] if r.get('caracter')=='supuesto_de_actualizacion']
        self.assertEqual(12,len(entries))
        row=next(r for r in entries if r['id']=='AU-A5-natural-5')
        self.assertEqual(row['columnas'][0]['localizadores'],row['columnas'][1]['localizadores'])
        self.assertNotEqual(row['columnas'][1]['localizadores'],row['columnas'][2]['localizadores'])
    def test_actualizacion_domicilio_elige_supuesto_y_columna(self):
        r=planificar(self.config(procedimiento='actualizacion',clase_actualizacion='legal',tipo_persona='natural',origen_proveedor='extranjero',domicilio='no_domiciliado',datos_actualizados=['domicilio_fiscal']))
        a5=[t for t in r['tareas'] if t['id'].startswith('AU-A5')]
        self.assertEqual(1,len(a5));self.assertEqual(4,a5[0]['columna_fuente']);self.assertTrue(a5[0]['localizadores_a_cotejar'])
    def test_no_se_inventa_texto_en_celda_vacia(self):
        r=planificar(self.config(procedimiento='actualizacion',clase_actualizacion='legal',tipo_persona='natural',origen_proveedor='extranjero',domicilio='no_domiciliado',datos_actualizados=['condicion_sunat']))
        row=next(t for t in r['tareas'] if t['id']=='AU-A5-natural-3')
        self.assertEqual('no_determinable',row['seleccion_documental']);self.assertEqual([],row['localizadores_a_cotejar'])
    def test_actualizacion_datos_invalidos_no_se_ignoran(self):
        for data in ('domicilio_fiscal',[{}],['inventado'],['nombres','nombres'],[]):
            with self.subTest(data=data),self.assertRaises(ValueError):planificar(self.config(procedimiento='actualizacion',datos_actualizados=data))
    def test_actualizacion_financiera_no_carga_anexo_legal(self):
        r=planificar(self.config(procedimiento='actualizacion',clase_actualizacion='financiera',tipo_registro='ejecutor',tipo_persona='juridica',origen_proveedor='nacional',motivo_actualizacion='anual'))
        self.assertFalse(any(t['id'].startswith('AU-A5') for t in r['tareas']))
        self.assertIn('AU-FIN-PJN',{t['id'] for t in r['tareas']});self.assertNotIn('AU-FIN-PNE',{t['id'] for t in r['tareas']})
    def test_reconsideracion_contiene_septimo_requisito_y_excepcion(self):
        r=planificar(self.config(procedimiento='reconsideracion'))
        self.assertEqual(10,len(r['tareas']));self.assertIn('RC-113-7',{t['id'] for t in r['tareas']})
        self.assertIn('única instancia',next(x for x in r['catalogo'] if x['id']=='RC-208')['fuentes'][0]['cita'])
    def test_ningun_plan_evita_revision_o_declara_vigencia(self):
        for procedure in ('inscripcion','ampliacion_consultores','aumento_cmc','actualizacion','reconsideracion'):
            r=planificar(self.config(procedimiento=procedure,fecha_solicitud='2026-11-01'))
            self.assertFalse(r['es_evaluacion_de_cumplimiento']);self.assertEqual('no_determinable',r['vigencia'])
            self.assertEqual('requiere_actualizar_fuentes',r['estado_temporal'])
    def test_diagnostico_separa_preparacion_tecnica_y_fecha(self):
        r=comprobar('2026-11-01');self.assertEqual('preparado_para_borradores_asistidos',r['estado'])
        self.assertTrue(r['requiere_revision_normativa_por_fecha']);self.assertFalse(r['api_de_modelo_requerida'])
    def test_diagnostico_detecta_original_faltante(self):
        fake={'name':'faltante.pdf','local_path':'data/no-existe-original-oece.pdf','sha256':'0'*64}
        with patch('oece.biblioteca.fuentes',return_value=[fake]),patch('oece.preparacion.verificar',return_value={}):r=comprobar('2026-10-30')
        self.assertEqual('requiere_preparacion',r['estado'])
        self.assertIn('faltante.pdf',str(r['comprobaciones']))


if __name__=='__main__':unittest.main()
