"""Ejemplos ficticios de actualización financiera; ningún proveedor real."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oece.comun import guardar,sha
from oece.flujo import Memoria,iniciar,procesar


def crear(destination):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    memory=Memoria(destination/'.oece');outputs={}
    for label,net in [('umbrales','100000'),('contradictorio','1000')]:
        case=destination/('demo-finanzas-'+label)
        iniciar(case,'actualizacion','Proveedor financiero ficticio sin datos reales',sintetico=True)
        config={'id':case.name,'procedimiento':'actualizacion','solicitante':'Proveedor financiero ficticio sin datos reales',
                'sintetico':True,'fecha_solicitud':'2026-06-29','tipo_persona':'juridica','origen_proveedor':'nacional',
                'domicilio':'domiciliado','tipo_registro':'ejecutor','clase_actualizacion':'financiera','motivo_actualizacion':'anual',
                'documentos_extranjeros':False,'documentos_en_espanol':True,'actua_por_representante':True,'experiencias':[]}
        guardar(case/'expediente.json',config)
        statements=[
            ('fecha_estados_financieros','2025-12-31','Estados ficticios cerrados al 2025-12-31.'),
            ('moneda_estados_financieros','PEN','Todos los importes del ejemplo están expresados en soles PEN y en unidades.'),
            ('base_financiera_homogenea',True,'Los importes del supuesto pertenecen al mismo período, moneda, unidad y persona jurídica; no mezclan matriz y sucursal.'),
            ('patrimonio',net,'Patrimonio neto ficticio PEN '+net+'.'),
            ('capital_social','300000','Capital social ficticio PEN 300000.'),
            ('activo_corriente','100000','Activo corriente ficticio PEN 100000.'),
            ('pasivo_corriente','100000','Pasivo corriente ficticio PEN 100000.'),
            ('pasivo_no_corriente','0','Pasivo no corriente ficticio PEN 0.'),
            ('utilidad_operativa','-5000','Pérdida operativa ficticia PEN 5000; utilidad operativa igual a menos 5000.'),
            ('perdidas_acumuladas','20000','Monto ficticio de pérdidas acumuladas PEN 20000, presentado como magnitud positiva.'),
            ('capital_base_perdidas','300000','La base de capital usada para este indicador ficticio es PEN 300000; su pertinencia real requiere análisis.'),
            ('clasificacion_sbs','normal','El supuesto sintético declara clasificación Normal; no procede de una consulta SBS real.'),
            ('fecha_reporte_sbs','2026-05-31','Reporte SBS ficticio fechado 2026-05-31.'),
            ('ultimo_reporte_sbs_confirmado',True,'Solo en la simulación se declara que este es el último reporte identificado; no se consultó la SBS.'),
            ('solicitud_presentada',True,'Solicitud ficticia de actualización financiera anual presentada el 2026-06-29.'),
            ('cambio_acreditado',True,'En el supuesto se identifica el ejercicio anual 2025 como variación financiera sustentada.'),
            ('ejercicio_financiero',2025,'El ejercicio financiero objeto de actualización es 2025.'),
            ('formulario_actualizacion_firmado',True,'El formulario ficticio se declara firmado solo para la simulación; no contiene firma real.'),
            ('sustentos_actualizacion_completos',True,'Los sustentos de la actualización se declaran completos exclusivamente en este supuesto.'),
            ('representacion_acreditada',True,'La representación se declara acreditada solo en este ejemplo ficticio.'),
            ('informacion_financiera_completa',True,'La información financiera se declara completa dentro de la simulación.'),
            ('informacion_financiera_disponible',True,'Hay información financiera ficticia disponible para los cálculos del ejemplo.'),
            ('solvencia_acreditada',True,'El documento ficticio afirma solvencia acreditada; esa afirmación debe contrastarse con los importes, no asumirse verdadera.')]
        path=case/'documentos/estados-sinteticos.txt'
        content='EJEMPLO SINTÉTICO SIN DATOS REALES\n'+'\n'.join(t[2] for t in statements)
        path.write_text(content,encoding='utf-8');digest=sha(path.read_bytes())
        facts=[{'campo':key,'valor':value,'autor':'Simulación documentada del coordinador','tipo_autor':'asistente_ia',
                'fecha':'2026-11-01T12:00:00-05:00','evidencias':[{'documento':'D'+digest[:12],'sha256':digest,
                'ubicacion':'linea:'+str(i+2),'cita':quote}]} for i,(key,value,quote) in enumerate(statements)]
        guardar(case/'hechos.json',facts)
        output,_=procesar(case,memory,usar_ocr=False);outputs[label]=str(output)
    guardar(destination/'entregas.json',outputs)
    return outputs


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('carpeta',type=Path);args=parser.parse_args()
    for label,folder in crear(args.carpeta).items():print(label,folder)
