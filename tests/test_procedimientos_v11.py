import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.calculos import cmc,fin_mes_siguiente,vencimiento_recurso
from oece.evaluacion import evaluar
from test_operacion_v1 import ficha,evidence_fixture

class CalculosV11(unittest.TestCase):
    def test_cmc_sin_experiencia_sin_informacion_100mil(self):
        self.assertEqual('100000.00',cmc(True,False)['cmc_propuesta'])
    def test_cmc_bordes_tabla_y_limite_500mil(self):
        for ac,pc,expected in [('40000','20000','150000.00'),('40001','20000','250000.00'),('60000','20000','300000.00'),('400000','50000','500000.00')]:
            self.assertEqual(expected,cmc(True,True,ac,pc)['cmc_propuesta'])
    def test_pc_cero_solo_rama_sin_experiencia(self):
        self.assertEqual('200000.00',cmc(True,True,'20000','0')['cmc_propuesta'])
        with self.assertRaises(ValueError):cmc(False,True,'20000','0',5,[self.obra()],'2026-10-30')
    def test_cmc_con_experiencia_factores_y_consorcio(self):
        work=self.obra();work['porcentaje_obligaciones']='50'
        r=cmc(False,True,'300000','100000',6,[work],'2026-10-30')
        self.assertEqual('500000',r['sumatoria_neta'])
        self.assertEqual('825000.00',r['cmc_propuesta']) # (1.00 + .40 + .25) * 500000
    def test_factor_ejecucion_superior_uno_admite_montos_finales_documentados(self):
        w=self.obra();w['monto_neto_obra']='1200000'
        r=cmc(False,False,anios_activos=5,obras=[w],corte='2026-10-30')
        self.assertEqual('0.50',r['factor_ejecucion'])
        self.assertEqual('1200000.00',r['cmc_propuesta'])
    def test_rechaza_obra_duplicada_vencida_y_no_culminada(self):
        for works in ([self.obra(),self.obra()],[{**self.obra(),'fecha_culminacion':'2000-01-01'}],[{**self.obra(),'fecha_culminacion':'2027-01-01'}]):
            with self.assertRaises(ValueError):cmc(False,False,anios_activos=5,obras=works,corte='2026-10-30')
    def test_veinte_anios_exactos_no_excluidos(self):
        r=cmc(False,False,anios_activos=5,obras=[{**self.obra(),'fecha_culminacion':'2006-10-30'}],corte='2026-10-30')
        self.assertEqual('1000000.00',r['cmc_propuesta'])
    def test_cero_y_no_finitos_no_generan_cmc(self):
        for ac,pc in [('NaN','1'),('Infinity','1'),('-1','1'),('0','0'),('100','100')]:
            with self.assertRaises(ValueError):cmc(True,True,ac,pc)
    def test_plazo_excluye_feriados_y_empieza_dia_siguiente(self):
        r=vencimiento_recurso('2026-10-01',self.calendario())
        self.assertEqual('2026-10-23',r['vencimiento'])
        self.assertEqual('2026-10-02',r['dias_contados'][0])
        self.assertNotIn('2026-10-08',r['dias_contados'])
    def test_calendario_incompleto_no_inventa_feriados(self):
        with self.assertRaises(ValueError):vencimiento_recurso('2026-10-01',{**self.calendario(),'hasta':'2026-10-05','dias_inhabiles':[]})
    def test_distancia_explicita_y_diciembre_cambio_de_anio(self):
        self.assertEqual('2026-10-27',vencimiento_recurso('2026-10-01',self.calendario(),distance=2)['vencimiento'])
        self.assertEqual('2027-01-31',fin_mes_siguiente('2026-12-15'))
        self.assertEqual('2028-02-29',fin_mes_siguiente('2028-01-31'))
    @staticmethod
    def obra():return {'id':'O1','monto_neto_obra':'1000000','monto_contratado':'1000000','porcentaje_obligaciones':'100','fecha_culminacion':'2026-08-01'}
    @staticmethod
    def calendario():return {'desde':'2026-10-01','hasta':'2026-12-31','semana_laboral':[0,1,2,3,4],'dias_inhabiles':['2026-10-08']}

class ModulosV11(unittest.TestCase):
    def evaluate(self,module,values,**config):
        c=ficha();c.update(procedimiento=module,**config)
        d,f=evidence_fixture(values);return evaluar(c,d,f)
    def test_inscripcion_bienes_no_exige_finanzas_ni_experiencia(self):
        r=self.evaluate('inscripcion',{'solicitud_presentada':True,'identificacion_coincide':True},tipo_registro='bienes',tipo_tramite='inscripcion',documentos_extranjeros=False,documentos_en_espanol=True)
        rows={row['id']:row for row in r['matriz']}
        self.assertEqual('cumple',rows['IN-01']['resultado'])
        self.assertEqual('no_aplica',rows['IN-09']['resultado'])
        self.assertNotIn('IN-11',rows)
        self.assertTrue(all(row['fuente_normativa'] for row in rows.values()))
    def test_consultor_natural_tambien_ejecutor_exige_finanzas(self):
        r=self.evaluate('inscripcion',{'inscrito_como_ejecutor':True},tipo_persona='natural',tipo_registro='consultor',tipo_tramite='reinscripcion')
        row=next(row for row in r['matriz'] if row['id']=='IN-09')
        self.assertEqual('no_determinable',row['resultado'])
        self.assertIn('informacion_financiera_completa',row['motivo'])
    def test_calculo_cmc_no_confunde_propuesta_con_aumento(self):
        values={'sin_experiencia':True,'informacion_financiera_disponible':False,'moneda_calculo':'PEN','universo_cmc_revisado':True,'cmc_vigente':'200000'}
        r=self.evaluate('aumento_cmc',values)
        rows={row['id']:row for row in r['matriz']}
        self.assertEqual('100000.00',r['calculos']['cmc']['cmc_propuesta'])
        self.assertEqual('no_cumple',rows['CMC-10']['resultado'])
        self.assertEqual('no_determinable',rows['CMC-11/E1']['resultado'])
    def test_calculo_no_usa_otra_moneda(self):
        r=self.evaluate('aumento_cmc',{'sin_experiencia':True,'informacion_financiera_disponible':False,'moneda_calculo':'USD','universo_cmc_revisado':True})
        self.assertNotIn('cmc',r['calculos'])
        self.assertEqual('no_determinable',next(row for row in r['matriz'] if row['id']=='CMC-09')['resultado'])
    def test_actualizacion_legal_fuera_del_mes_no_declara_extemporaneo_sin_calendario(self):
        r=self.evaluate('actualizacion',{'fecha_cambio':'2026-08-10'},clase_actualizacion='legal')
        row=next(row for row in r['matriz'] if row['id']=='AU-03')
        self.assertEqual('no_determinable',row['resultado']);self.assertIn('2026-09-30',row['motivo'])
    def test_actualizacion_financiera_anual_no_confunde_nacional_extranjero(self):
        for origin,end in [('nacional','2026-06-30'),('extranjero','2026-09-30')]:
            r=self.evaluate('actualizacion',{'ejercicio_financiero':2025},clase_actualizacion='financiera',motivo_actualizacion='anual',origen_proveedor=origin)
            self.assertEqual(end,r['calculos']['actualizacion']['limite_calendario'])
    def test_reconsideracion_unica_instancia_no_exige_nueva_prueba(self):
        r=self.evaluate('reconsideracion',{'organo_unica_instancia':True})
        row=next(row for row in r['matriz'] if row['id']=='RC-04')
        self.assertEqual('no_aplica',row['resultado']);self.assertTrue(row['evidencias'])
    def test_reconsideracion_sin_excepcion_y_sin_nueva_prueba(self):
        r=self.evaluate('reconsideracion',{'organo_unica_instancia':False,'nueva_prueba':False})
        self.assertEqual('no_cumple',next(row for row in r['matriz'] if row['id']=='RC-04')['resultado'])
    def test_recurso_plazo_documentado_y_fuera_del_plazo(self):
        values={'fecha_notificacion':'2026-10-01','calendario_recurso':CalculosV11.calendario(),'calendario_entidad_confirmado':True,'dias_termino_distancia':0,'regla_general_recurso_aplicable':True}
        r=self.evaluate('reconsideracion',values)
        self.assertEqual('2026-10-23',r['calculos']['reconsideracion']['vencimiento'])
        self.assertEqual('no_cumple',next(row for row in r['matriz'] if row['id']=='RC-05')['resultado'])
    def test_fuera_de_ventana_no_da_resultado_favorable(self):
        r=self.evaluate('inscripcion',{'identificacion_coincide':True,'solicitud_presentada':True},fecha_solicitud='2025-01-01',tipo_registro='bienes',tipo_tramite='inscripcion')
        self.assertFalse(any(row['resultado']=='cumple' for row in r['matriz']))
    def test_cuatro_procedimientos_entregan_word_matriz_y_fuentes(self):
        import tempfile
        sys.path.insert(0,str(ROOT/'scripts'))
        from crear_demos_procedimientos import crear
        from oece.flujo import verificar_entrega
        from docx import Document
        area=ROOT/'data/pruebas-v11';area.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=area) as name:
            outputs=crear(Path(name)/'expedientes')
            self.assertEqual(4,len(outputs))
            for module,folder in outputs.items():
                verificar_entrega(folder)
                result=json.loads((Path(folder)/'matriz.json').read_text(encoding='utf-8'))
                self.assertTrue(all(row['fuente_normativa'] for row in result['matriz']))
                self.assertIn('EJEMPLO SINTÉTICO',' '.join(p.text for p in Document(Path(folder)/'informe.docx').paragraphs))

if __name__=='__main__':unittest.main()
