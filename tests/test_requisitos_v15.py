import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from oece.calculos import cmc
from oece.comun import guardar,leer,sha
from oece.flujo import Memoria,iniciar,procesar
from oece.mcp_local import CURRENT
from oece.requisitos import REGISTRO,planificar,verificar
from construir_requisitos import construir
from test_operacion_v1 import ficha


class RequisitosV15(unittest.TestCase):
    def config(self,procedure='ampliacion_consultores',origin='peru_ley',sub=False):
        return {**ficha(),'procedimiento':procedure,'experiencias':[{'id':'E1','origen':origin,'consorcio':False,'subcontrato':sub}]}
    def tasks(self,**changes):
        return planificar(self.config(**changes))['tareas']
    def ids(self,**changes):return {t['requisito_id'] for t in self.tasks(**changes)}
    def test_consultor_tres_procedencias_no_acumulan_documentos(self):
        for origin,expected in [('peru_ley',{'AC-L-a'}),('peru_fuera_ley',{'AC-P-'+v for v in 'abcde'}),('extranjero',{'AC-E-a','AC-E-b'})]:
            self.assertEqual({'AC-R01','AC-R02'}|expected,self.ids(origin=origin))
    def test_cmc_tres_procedencias_y_subcontrato_separados(self):
        for origin,sub,expected in [('peru_ley',False,{'CMC-L-a'}),('peru_ley',True,{'CMC-S-'+v for v in 'abcde'}),
                                    ('peru_fuera_ley',False,{'CMC-P-'+v for v in 'abcd'}),('extranjero',False,{'CMC-E-a','CMC-E-b'})]:
            self.assertEqual({'CMC-R01','CMC-R02'}|expected,self.ids(procedure='aumento_cmc',origin=origin,sub=sub))
    def test_subcontrato_desconocido_no_equivale_a_contrato_directo(self):
        rows=self.tasks(procedure='aumento_cmc',sub=None)
        self.assertEqual(6,sum(r['seleccion_documental']=='no_determinable' for r in rows))
        self.assertNotIn('aplica',{r['seleccion_documental'] for r in rows if r['experiencia']})
    def test_origen_desconocido_conserva_pregunta_y_alternativas(self):
        result=planificar(self.config(origin=None))
        self.assertEqual(8,sum(t['seleccion_documental']=='no_determinable' for t in result['tareas']))
        self.assertIn('Procedencia',str(result['pendientes']))
    def test_sin_experiencias_no_inventa_fila_ni_presume_falta_documental(self):
        config=self.config();config['experiencias']=[];result=planificar(config)
        self.assertEqual(2,len(result['tareas']));self.assertIn('Identificar experiencias',str(result['pendientes']))
    def test_plan_no_es_aprobacion_y_cada_tarea_espera_interpretacion(self):
        result=planificar(self.config())
        self.assertFalse(result['es_evaluacion_de_cumplimiento'])
        self.assertEqual('no_determinable',result['vigencia'])
        self.assertEqual({'pendiente_interpretacion'},{r['revision'] for r in result['tareas']})
    def test_subcontrato_especial_conserva_revision_y_no_lo_prohibe_por_defecto(self):
        for procedure,origin in [('aumento_cmc','extranjero'),('aumento_cmc','peru_fuera_ley'),('ampliacion_consultores','peru_ley')]:
            result=planificar(self.config(procedure,origin,True));self.assertIn('delimitar subcontrato',str(result['pendientes']))
            self.assertTrue(result['tareas']);self.assertNotIn('no_cumple',str(result))
    def test_alternativa_de_contrato_principal_no_exige_las_dos_vias(self):
        item=next(r for r in leer(REGISTRO)['requisitos'] if r['id']=='CMC-S-a')
        self.assertEqual({'copia_contrato_principal','referencia_registro_plataforma'},{a['via'] for a in item['alternativas_documentales']})
        self.assertIn('basta precisar',item['fuentes'][0]['cita'])
    def test_diez_exclusiones_son_alertas_y_no_documentos_adicionales(self):
        alerts=planificar(self.config())['alertas_exclusion']
        self.assertEqual(10,len(alerts));self.assertEqual({'alerta_de_analisis_no_documento_adicional'},{a['caracter'] for a in alerts})
    def test_otros_procedimientos_no_heredan_listas_de_ampliacion(self):
        for procedure in ('inscripcion','actualizacion','reconsideracion'):
            result=planificar(self.config(procedure));self.assertEqual('fuera_cobertura',result['estado'])
            self.assertEqual([],result['tareas']);self.assertEqual([],result['alertas_exclusion'])
    def test_fecha_posterior_no_extiende_vigencia(self):
        config=self.config();config['fecha_solicitud']='2026-11-01';r=planificar(config)
        self.assertEqual('requiere_actualizar_fuentes',r['estado_temporal']);self.assertEqual('no_determinable',r['vigencia'])
    def test_subcontrato_de_tipo_incorrecto_rechazado(self):
        with self.assertRaises(ValueError):planificar(self.config(sub='no'))
    def test_todas_las_citas_y_referencias_se_cotejan_con_originales(self):
        r=verificar();self.assertEqual(3,r['originales']);self.assertEqual(59,r['referencias']);self.assertEqual(34,r['citas_literales'])
    def test_cita_normativa_alterada_se_rechaza(self):
        registry=leer(REGISTRO);registry['requisitos'][0]['fuentes'][0]['cita']='Requisito inventado fuera del original'
        with self.assertRaisesRegex(ValueError,'Cita'):verificar(registry)
    def test_reconstruccion_reproducible_sin_aprobacion_humana(self):
        actual=construir();self.assertEqual(leer(REGISTRO),actual)
        self.assertEqual(24,len(actual['requisitos']));self.assertTrue(all(r['revision_humana'] is None and r['apta_para_reglas'] is False for r in actual['requisitos']))
    def test_cmc_pc_cero_bandas_con_experiencia_sin_infinito(self):
        work={'id':'O1','monto_neto_obra':'1000000','monto_contratado':'1000000','porcentaje_obligaciones':'100','fecha_culminacion':'2026-08-01'}
        for ac,score in [('0.01','0.20'),('20000','0.20'),('20000.01','0.30'),('100000','0.30'),('100000.01','0.40'),('300000','0.40'),('300000.01','0.50')]:
            result=cmc(False,True,ac,'0',5,[work],'2026-10-30');self.assertEqual(score,result['factor_financiero'])
            self.assertIn('9.2.6.d',result['tratamiento_pc_cero']);self.assertNotIn('Infinity',str(result))
    def test_cmc_pc_cero_sin_activo_positivo_rechazado(self):
        for exp in (True,False):
            with self.assertRaises(ValueError):cmc(exp,True,'0','0')
    def test_entrega_conserva_plan_registro_y_dependencias_sin_marcarlo_evaluado(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            root=Path(area);case=root/'caso';iniciar(case,sintetico=True)
            config=self.config();guardar(case/'expediente.json',config)
            (case/'documentos/solicitud.txt').write_text('Ejemplo sintético de solicitud.',encoding='utf-8')
            output,_=procesar(case,Memoria(root/'.oece'),False);result=leer(output/'matriz.json')
            self.assertIn('plan_documental',result);self.assertFalse(result['plan_documental']['es_evaluacion_de_cumplimiento'])
            self.assertEqual(sha(REGISTRO.read_bytes()),result['instantanea']['dependencias']['rules/requisitos-ampliaciones.v1.5.json'])
            self.assertEqual(result['plan_documental']['sha256_registro'],result['instantanea']['dependencias']['rules/requisitos-ampliaciones.v1.5.json'])
    def test_mcp_stdio_y_cli_mismo_plan_sin_modelo(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            root=Path(area);case=root/'E1';iniciar(case,sintetico=True);guardar(case/'expediente.json',self.config())
            call={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'oece_requisitos','arguments':{'caso':'E1'},'_meta':{'io.modelcontextprotocol/protocolVersion':CURRENT,'io.modelcontextprotocol/clientCapabilities':{}}}}
            pipe=subprocess.run([sys.executable,str(ROOT/'scripts/servidor_mcp.py'),'--raiz',str(root)],input=(json.dumps(call)+'\n').encode(),capture_output=True,cwd=root,timeout=30)
            self.assertEqual(0,pipe.returncode);response=json.loads(pipe.stdout)['result'];self.assertFalse(response['isError'])
            cli=subprocess.run([sys.executable,'-m','oece','--memoria',str(root/'.cli'),'requisitos',str(case)],capture_output=True,cwd=ROOT,timeout=30)
            self.assertEqual(0,cli.returncode,cli.stderr.decode(errors='replace'));self.assertEqual(response['structuredContent'],json.loads(cli.stdout))


if __name__=='__main__':unittest.main()
