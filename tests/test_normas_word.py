from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from oece.biblioteca import fuentes,leer_fuente,validar_normas
from oece.comun import guardar,leer
from oece.flujo import iniciar,Memoria,procesar
from oece.puente import Puente


class NormasWord(unittest.TestCase):
    def norma(self):
        s=next(s for s in fuentes() if 'anexo-n-5-' in s['name'])
        loc='cuerpo/bloque:4/fila:5/celda:4/bloque:1';r=leer_fuente(s['name'],ubicacion=loc)
        return {'codigo':'N-Anexo5','archivo':s['name'],'sha256':s['sha256'],'url':s['source_url'],'ubicacion':loc,
                'disposicion':'Anexo 5, persona natural extranjera no domiciliada, domicilio fiscal','cita':r['texto'],
                'autor':'Asistente de IA de prueba','criterio':'Ejemplo ficticio para revisar el sustento del cambio de domicilio, condicionado a la rama documentada.'}
    def test_cita_word_y_lectura_mcp_por_celda(self):
        n=self.norma();self.assertEqual([n],validar_normas([n]))
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            r=Puente(area).ejecutar('oece_norma',{'archivo':n['archivo'],'ubicacion':n['ubicacion']})
        self.assertEqual(n['cita'],r['texto']);self.assertEqual(n['sha256'],r['fuente']['sha256'])
    def test_no_acepta_celda_falsa_cita_falsa_ni_pagina_ambigua(self):
        n=self.norma()
        for change in ({'ubicacion':'cuerpo/falso'},{'cita':'Texto inexistente'},{'pagina_pdf':1}):
            with self.subTest(change=change),self.assertRaises(ValueError):validar_normas([{**n,**change}])
    def test_informe_y_matriz_conservan_cita_y_localizador_word(self):
        from docx import Document
        with tempfile.TemporaryDirectory(dir=ROOT/'data') as area:
            root=Path(area);case=root/'caso';c=iniciar(case,'actualizacion','Ejemplo ficticio',True)
            c.update(fecha_solicitud='2026-10-30',tipo_persona='natural',origen_proveedor='extranjero',domicilio='no_domiciliado',clase_actualizacion='legal',datos_actualizados=['domicilio_fiscal'])
            guardar(case/'expediente.json',c);(case/'documentos/solicitud.txt').write_text('Solicitud ficticia para actualizar domicilio.',encoding='utf-8')
            n={**self.norma(),'pagina_pdf':None};other={**n,'codigo':'N-Contraste','ubicacion':'cuerpo/bloque:4/fila:5/celda:2/bloque:5'}
            other['cita']=leer_fuente(other['archivo'],ubicacion=other['ubicacion'])['texto']
            guardar(case/'normas.json',[n,other]);guardar(case/'analisis.json',[{'texto':'Revisar el sustento de domicilio y distinguir las columnas del Anexo 5; las citas no acreditan su aplicabilidad por sí solas.','autor':'Asistente de IA de prueba','referencias':[n['codigo'],other['codigo']]}])
            output,_=procesar(case,Memoria(root/'.oece'),False)
            self.assertEqual(n,leer(output/'matriz.json')['normas_adicionales'][0])
            text='\n'.join(p.text for p in Document(output/'informe.docx').paragraphs)
            self.assertIn(n['ubicacion'],text);self.assertIn(other['ubicacion'],text);self.assertNotIn('página PDF None',text)


if __name__=='__main__':unittest.main()
