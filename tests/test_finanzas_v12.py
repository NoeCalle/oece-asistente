from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.finanzas import ratio
from oece.evaluacion import evaluar
from test_operacion_v1 import ficha,evidence_fixture


def datos():
    return {'fecha_estados_financieros':'2025-12-31','moneda_estados_financieros':'PEN',
            'base_financiera_homogenea':True,'patrimonio':'100000','capital_social':'300000',
            'activo_corriente':'100000','pasivo_corriente':'100000','pasivo_no_corriente':'0',
            'utilidad_operativa':'-5000','perdidas_acumuladas':'20000','capital_base_perdidas':'300000',
            'clasificacion_sbs':'normal','fecha_reporte_sbs':'2026-09-30','ultimo_reporte_sbs_confirmado':True}


class RatiosV12(unittest.TestCase):
    def test_r2_umbral_exacto_y_margen_inferior(self):
        for net,ok in [('5',True),('4.999999999999',False),('-1',False)]:
            r=ratio('R2',{'patrimonio':net,'pasivo_corriente':'60','pasivo_no_corriente':'40'})
            self.assertIs(ok,r['satisface_umbral_aritmetico'])
    def test_r3_igualdad_y_unidad_debajo(self):
        for ac,ok in [('100',True),('99.999999999999',False)]:
            self.assertIs(ok,ratio('R3',{'activo_corriente':ac,'pasivo_corriente':'100'})['satisface_umbral_aritmetico'])
    def test_r8_tercio_exactamente_no_depende_de_decimal_repetido(self):
        self.assertTrue(ratio('R8',{'patrimonio':'100','capital_social':'300'})['satisface_umbral_aritmetico'])
        # Se ve igual a doce decimales pero no debe aprobarse.
        self.assertFalse(ratio('R8',{'patrimonio':'99.999999999999','capital_social':'300'})['satisface_umbral_aritmetico'])
    def test_r9_utilidad_negativa_es_referencial(self):
        r=ratio('R9',{'utilidad_operativa':'-5','patrimonio':'100','pasivo_no_corriente':'0'})
        self.assertEqual('-0.050000000000',r['valor_aproximado']);self.assertIsNone(r['satisface_umbral_aritmetico'])
    def test_rc_no_convierte_simbolo_en_juicio_de_solvencia(self):
        for loss in ('10','50','80'):
            self.assertIsNone(ratio('RC',{'perdidas_acumuladas':loss,'capital_base_perdidas':'100'})['satisface_umbral_aritmetico'])
    def test_denominadores_no_positivos_no_son_infinitos(self):
        for code,values in [('R2',{'patrimonio':'10','pasivo_corriente':'0','pasivo_no_corriente':'0'}),
                            ('R3',{'activo_corriente':'10','pasivo_corriente':'0'}),
                            ('R8',{'patrimonio':'10','capital_social':'0'}),
                            ('R9',{'utilidad_operativa':'1','patrimonio':'-10','pasivo_no_corriente':'0'})]:
            with self.assertRaises(ValueError):ratio(code,values)
    def test_rechaza_no_finitos_booleanos_floats_y_magnitudes(self):
        for v in ('NaN','Infinity','1e999999','1e-99999',True,1.0):
            with self.assertRaises(ValueError):ratio('R3',{'activo_corriente':v,'pasivo_corriente':'1'})
    def test_pasivos_negativos_rechazados_y_patrimonio_negativo_conservado(self):
        with self.assertRaises(ValueError):ratio('R2',{'patrimonio':'10','pasivo_corriente':'-1','pasivo_no_corriente':'10'})
        self.assertFalse(ratio('R8',{'patrimonio':'-10','capital_social':'10'})['satisface_umbral_aritmetico'])


class FinanzasDocumentalesV12(unittest.TestCase):
    def run_module(self,values=None,module='ampliacion_consultores',**config):
        c=ficha();c.update(procedimiento=module,**config)
        docs,facts=evidence_fixture(datos() if values is None else values)
        r=evaluar(c,docs,facts)
        return r,{row['id']:row for row in r['matriz']}
    def test_ratios_satisfechos_no_sustituyen_analisis_integral(self):
        r,rows=self.run_module()
        for code in ('R2','R3','R8'):self.assertEqual('cumple',rows['FIN-'+code]['resultado'])
        self.assertEqual('no_determinable',rows['FIN-INTEGRAL']['resultado'])
        self.assertNotIn('FIN-R9',rows);self.assertNotIn('FIN-RC',rows)
        self.assertIsNone(r['calculos']['finanzas']['indicadores']['RC']['satisface_umbral_aritmetico'])
    def test_afirmacion_solvencia_no_oculta_ratio_insuficiente(self):
        _,rows=self.run_module({**datos(),'solvencia_acreditada':True,'solvencia_aplicable':True,'patrimonio':'1000'})
        self.assertEqual('no_determinable',rows['AC-22']['resultado'])
        self.assertEqual('cumple',rows['AC-22']['resultado_documental_previo'])
        self.assertEqual('no_cumple',rows['FIN-R2']['resultado']);self.assertEqual('no_cumple',rows['FIN-R8']['resultado'])
    def test_bases_mixtas_y_balance_futuro_impiden_cumplimiento(self):
        for changes in ({'base_financiera_homogenea':False},{'fecha_estados_financieros':'2027-01-01'},{'moneda_estados_financieros':'PEN/USD'}):
            r,rows=self.run_module({**datos(),**changes})
            self.assertEqual('no_determinable',rows['FIN-R2']['resultado'])
            self.assertNotIn('valor_aproximado',r['calculos']['finanzas']['ratios']['R2'])
    def test_importe_faltante_no_se_toma_como_cero(self):
        d=datos();del d['pasivo_no_corriente'];r,rows=self.run_module(d)
        self.assertEqual('no_determinable',rows['FIN-R2']['resultado']);self.assertEqual('cumple',rows['FIN-R3']['resultado'])
    def test_pc_cero_no_traslada_excepcion_de_cmc_a_liquidez(self):
        _,rows=self.run_module({**datos(),'pasivo_corriente':'0'},module='aumento_cmc')
        self.assertEqual('no_determinable',rows['FIN-R3']['resultado'])
    def test_sbs_normal_no_reportado_y_otra_clasificacion(self):
        for category,status in [('normal','cumple'),('no_reportado','cumple'),('dudoso','no_cumple')]:
            _,rows=self.run_module({**datos(),'clasificacion_sbs':category})
            self.assertEqual(status,rows['FIN-SBS']['resultado'])
    def test_reporte_sbs_futuro_o_sin_confirmar_no_es_consulta_valida(self):
        for changes in ({'fecha_reporte_sbs':'2027-01-01'},{'ultimo_reporte_sbs_confirmado':False}):
            _,rows=self.run_module({**datos(),**changes});self.assertEqual('no_determinable',rows['FIN-SBS']['resultado'])
    def test_no_impone_ratios_a_bienes_servicios_recurso_o_actualizacion_legal(self):
        for module,c in [('inscripcion',{'tipo_registro':'bienes'}),('inscripcion',{'tipo_registro':'servicios'}),
                         ('reconsideracion',{}),('actualizacion',{'clase_actualizacion':'legal'})]:
            r,rows=self.run_module(module=module,**c)
            self.assertFalse(any(k.startswith('FIN-') for k in rows));self.assertNotIn('finanzas',r.get('calculos',{}))
    def test_consultor_natural_sin_dato_de_otro_registro_no_presume_dispensa(self):
        _,rows=self.run_module(tipo_persona='natural');self.assertEqual('no_determinable',rows['FIN-01']['resultado'])
        _,rows=self.run_module({**datos(),'inscrito_como_ejecutor':False},tipo_persona='natural')
        self.assertFalse(any(k.startswith('FIN-') for k in rows))
        _,rows=self.run_module({**datos(),'inscrito_como_ejecutor':True},tipo_persona='natural');self.assertEqual('cumple',rows['FIN-R2']['resultado'])
    def test_ventana_y_regimen_no_se_saltan_por_agregar_ratios(self):
        for config in ({'fecha_solicitud':'2026-11-01'},{'fecha_solicitud':'2026-01-19'},{'historial_rnp_disponible':False}):
            result,rows=self.run_module(**config)
            self.assertFalse(result['calculos']['finanzas']['ventana_verificada'])
            self.assertFalse(any(row['resultado'] in ('cumple','no_cumple') for key,row in rows.items() if key.startswith('FIN-')))
    def test_citas_y_huellas_financieras_permanecen_en_matriz(self):
        _,rows=self.run_module()
        row=rows['FIN-R2'];self.assertTrue(row['evidencias']);self.assertTrue(row['autores'])
        self.assertEqual(6,row['fuente_normativa']['pagina_pdf']);self.assertEqual(64,len(row['fuente_normativa']['sha256']))
        self.assertEqual(7,rows['FIN-R3']['fuente_normativa']['pagina_pdf'])
    def test_informacion_ausente_y_bases_declaradas_contradiccion(self):
        _,rows=self.run_module({**datos(),'informacion_financiera_disponible':False})
        self.assertEqual('no_determinable',rows['FIN-R2']['resultado'])
    def test_ocr_sin_cotejo_no_respalda_ratios(self):
        c=ficha();docs,facts=evidence_fixture(datos());docs[0]['fragmentos'][0]['alertas']=['ocr_sin_cotejo_visual']
        r=evaluar(c,docs,facts)
        self.assertTrue(all(row['resultado']=='no_determinable' for row in r['matriz'] if row['id'].startswith('FIN-')))
    def test_entregas_financieras_conservan_registro_citas_y_word(self):
        import tempfile
        from docx import Document
        from oece.flujo import verificar_entrega
        sys.path.insert(0,str(ROOT/'scripts'))
        from crear_demos_finanzas import crear
        area=ROOT/'data/pruebas-v12';area.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=area) as name:
            outputs=crear(Path(name)/'ejemplos')
            for label,folder in outputs.items():
                verificar_entrega(folder)
                import json
                matrix=json.loads((Path(folder)/'matriz.json').read_text(encoding='utf-8'))
                self.assertIn('rules/finanzas.v1.2.json',matrix['instantanea']['dependencias'])
                document=Document(Path(folder)/'informe.docx')
                self.assertTrue(any('Valor aproximado' in cell.text for table in document.tables for row in table.rows for cell in row.cells))
                row=next(v for v in matrix['matriz'] if v['id']=='FIN-R2')
                self.assertEqual('no_cumple' if label=='contradictorio' else 'cumple',row['resultado'])


if __name__=='__main__':unittest.main()
