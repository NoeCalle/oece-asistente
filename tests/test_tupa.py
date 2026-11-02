import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from oece.comun import guardar,leer,sha
from oece.mcp_local import CURRENT,Protocolo
from oece.puente import Puente
from oece.tupa import REGISTRO,consultar
from construir_indice_tupa import construir


class TupaTests(unittest.TestCase):
    def ficha(self,**changes):
        return {'procedimiento':'inscripcion','tipo_registro':'bienes','tipo_persona':'natural',
                'origen_proveedor':'nacional','domicilio':'domiciliado','tipo_tramite':'inscripcion',
                'fecha_solicitud':'2026-10-30',**changes}
    def codes(self,**changes):return {f['codigo'] for f in consultar(self.ficha(**changes))['fichas_candidatas']}
    def test_ocho_ramas_de_obras_y_domicilio_no_se_inventa(self):
        for register,rows in [('consultor',[('natural','nacional','PA42007D51'),('natural','extranjero','PA42009762'),('juridica','nacional','PA42001C78'),('juridica','extranjero','PA4200ED2E')]),
                              ('ejecutor',[('natural','nacional','PA42003A4F'),('natural','extranjero','PA4200C4F5'),('juridica','nacional','PA42000DF5'),('juridica','extranjero','PA42009BA2')])]:
            for person,origin,code in rows:
                with self.subTest(code=code):self.assertEqual({code},self.codes(tipo_registro=register,tipo_persona=person,origen_proveedor=origin,domicilio=None))
    def test_bienes_servicios_domiciliados_comparten_ficha_por_persona(self):
        for register in ('bienes','servicios'):
            for origin in ('nacional','extranjero'):
                for person,code in [('natural','PA42004846'),('juridica','PA4200EF4C')]:
                    self.assertEqual({code},self.codes(tipo_registro=register,origen_proveedor=origin,tipo_persona=person))
    def test_no_domiciliado_no_se_confunde_con_rama_especial(self):
        for person,ordinary in [('natural','PA4200F589'),('juridica','PA4200067C')]:
            for generic in (True,False,None):
                codes=self.codes(tipo_persona=person,origen_proveedor='extranjero',domicilio='no_domiciliado',actua_por_representante=generic)
                self.assertEqual({ordinary,'PA42007484'},codes)
    def test_faltantes_conservan_alternativas_y_no_crean_requisitos(self):
        result=consultar({'procedimiento':'inscripcion'})
        self.assertEqual(13,len(result['fichas_candidatas']))
        self.assertEqual({'tipo_persona','origen_proveedor','domicilio','tipo_registro'},set(result['campos_faltantes']))
        self.assertTrue(all(f['apta_para_reglas'] is False and f['revision_humana'] is None for f in result['fichas_candidatas']))
    def test_nacional_no_domiciliado_no_recibe_codigo_por_defecto(self):
        result=consultar(self.ficha(domicilio='no_domiciliado'));self.assertEqual([],result['fichas_candidatas'])
    def test_ampliacion_y_cmc_sin_trasladar_reglas(self):
        self.assertEqual({'PA42003A92'},self.codes(procedimiento='ampliacion_consultores'))
        self.assertEqual({'PA42009D33'},self.codes(procedimiento='aumento_cmc'))
        self.assertIn('A/B/C/D',str(consultar(self.ficha(procedimiento='ampliacion_consultores'))))
    def test_actualizacion_y_recurso_no_inventan_fichas(self):
        for procedure in ('actualizacion','reconsideracion'):
            result=consultar(self.ficha(procedimiento=procedure));self.assertEqual([],result['fichas_candidatas'])
            self.assertIn('No inventar',str(result['alertas']))
    def test_fronteras_temporales_no_declaran_vigencia(self):
        for value,state in [(None,'fecha_no_documentada'),('2026-04-07','requiere_version_historica'),('2026-04-08','dentro_corte_documental_sin_resolver_vigencia'),
                            ('2026-10-31','dentro_corte_documental_sin_resolver_vigencia'),('2026-11-01','requiere_actualizar_fuentes')]:
            result=consultar(self.ficha(fecha_solicitud=value));self.assertEqual(state,result['estado_temporal'])
            self.assertEqual('no_determinable',result['aplicabilidad_juridica'])
    def test_fecha_y_selecciones_invalidas_no_son_faltantes(self):
        for changes in ({'fecha_solicitud':True},{'fecha_solicitud':'2026-02-30'},{'fecha_solicitud':'20260408'},{'tipo_persona':'jurídica'},{'procedimiento':'otro'}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):consultar(self.ficha(**changes))
    def test_recupera_continuacion_con_hash_y_pagina(self):
        result=consultar(self.ficha(tipo_registro='ejecutor'),'PA42003A4F',51)
        self.assertEqual('pagina:51',result['pagina']['ubicacion'])
        self.assertEqual(sha(result['pagina']['texto'].encode()),result['pagina']['sha256_texto'])
        self.assertIn('facturas',result['pagina']['texto'])
    def test_no_lee_paginas_ajenas_ni_codigos_incompatibles(self):
        for code,page in [('PA42004846',66),('PA42003A92',31),('../escape',None),('PA42004846',True),(None,64)]:
            with self.subTest(code=code,page=page),self.assertRaises(ValueError):consultar(self.ficha(),code,page)
    def test_fuente_alterada_es_rechazada_antes_de_extraer(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            altered=Path(area)/'alterado.pdf';altered.write_bytes(b'Alterado')
            with patch('oece.tupa.dentro',return_value=altered),self.assertRaisesRegex(ValueError,'alterado'):
                consultar(self.ficha(),'PA42004846')
    def test_indice_reconstruido_coincide_y_cubre_cuarenta_paginas(self):
        import logging
        with patch.object(logging.getLogger('pypdf'),'warning'):
            current=construir()
        self.assertEqual(leer(REGISTRO),current)
        self.assertEqual(15,len(current['fichas']));self.assertEqual(40,sum(len(f['paginas']) for f in current['fichas']))
    def test_mcp_y_cli_consultan_el_mismo_expediente(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            root=Path(area);bridge=Puente(root)
            bridge.ejecutar('oece_nuevo',{'caso':'T1','procedimiento':'inscripcion','solicitante':'Ficticio','sintetico':True})
            path=root/'T1/expediente.json';config=leer(path);config.update(self.ficha());guardar(path,config)
            meta={'io.modelcontextprotocol/protocolVersion':CURRENT,'io.modelcontextprotocol/clientCapabilities':{}}
            result=Protocolo(bridge).manejar({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'oece_tupa','arguments':{'caso':'T1','codigo':'PA42004846'},'_meta':meta}})['result']
            self.assertFalse(result['isError']);self.assertIn('pagina',result['structuredContent'])
            call={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'oece_tupa','arguments':{'caso':'T1','codigo':'PA42004846'},'_meta':meta}}
            pipe=subprocess.run([sys.executable,str(ROOT/'scripts/servidor_mcp.py'),'--raiz',str(root)],input=(json.dumps(call)+'\n').encode(),capture_output=True,timeout=20,cwd=root)
            self.assertEqual(0,pipe.returncode,pipe.stderr.decode(errors='replace'))
            self.assertEqual(result,json.loads(pipe.stdout)['result'])
            run=subprocess.run([sys.executable,'-m','oece','--memoria',str(root/'.cli'),'tupa',str(root/'T1'),'--codigo','PA42004846'],capture_output=True,timeout=20,cwd=ROOT)
            self.assertEqual(0,run.returncode,run.stderr.decode(errors='replace'))
            self.assertEqual(result['structuredContent'],json.loads(run.stdout))


if __name__=='__main__':unittest.main()
