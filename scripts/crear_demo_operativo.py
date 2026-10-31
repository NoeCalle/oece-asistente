"""Ejemplo ficticio reproducible para probar panel, evidencia, diferencia y Word."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oece.comun import ROOT,guardar,leer
from oece.flujo import iniciar,Memoria,preparar,procesar

def create(folder):
    folder=Path(folder)
    if folder.exists():
        raise ValueError('Usar una carpeta nueva para conservar las demostraciones previas')
    c=iniciar(folder,solicitante='Consultora Ejemplo Sin Datos Reales',sintetico=True)
    c.update(fecha_solicitud='2026-10-30',tipo_persona='juridica',origen_proveedor='nacional',domicilio='domiciliado',
             historial_rnp_disponible=True,primera_ampliacion_tras_recategorizacion=True,
             tramite_en_curso_transicion=False,categoria_solicitada='b',actua_por_representante=True,
             experiencias=[{'id':'E1','origen':'peru_fuera_ley','consorcio':True}])
    guardar(folder/'expediente.json',c)
    files={
        'solicitud.txt':[
            'EJEMPLO SINTÉTICO. No es una solicitud ni consulta de registro real.',
            'Proveedor ficticio Consultora Ejemplo Sin Datos Reales. Solicitud ficticia de ampliación presentada para elaborar expedientes técnicos de obra.',
            'En esta simulación la identidad del solicitante coincide con el formulario.',
            'Recibo ficticio DEMO-2026-014. Fecha de pago simulada 2026-10-29.',
            'La representación y la consulta registral no se han incorporado al ejemplo.'],
        'contrato.txt':[
            'EJEMPLO SINTÉTICO. Contrato DEMO-014 sin efectos comerciales.',
            'Consultoría privada en Perú fuera del ámbito de la Ley. Elaboración de expediente técnico de una edificación ficticia.',
            'Monto final de honorarios de consultoría PEN 100000.00. No es el presupuesto de ejecución de obra.',
            'El servicio se contrató en consorcio. No se incorporó el documento de distribución de obligaciones.',
            'Fecha de suscripción simulada 2026-02-01. Inicio de prestación simulado 2026-02-10.'],
        'conformidad.txt':[
            'EJEMPLO SINTÉTICO. Conformidad ficticia del contrato DEMO-014.',
            'Servicio culminado el 2026-08-31, con aprobación ficticia del expediente técnico por el contratante.',
            'Actividades declaradas: elaboración de planos, memoria, metrados y presupuesto.',
            'El documento omite datos registrales completos del contratante y obligaciones de cada integrante.'],
        'comprobantes.txt':[
            'EJEMPLO SINTÉTICO. Relación ficticia de comprobantes, sin validez tributaria.',
            'Comprobante DEMO-F001 por PEN 50000.00 y DEMO-F002 por PEN 30000.00.',
            'Total de comprobantes de honorarios PEN 80000.00. No hay sustento del saldo en este ejemplo.']}
    for name,lines in files.items(): (folder/'documentos'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    memory=Memoria(folder.parent/'.oece')
    result,_=preparar(folder,memory,False)
    docs={Path(d['archivo']).name:d for d in result['documentos']}
    specs=[
        ('identificacion_coincide',True,'solicitud.txt',3),
        ('solicitud_presentada',True,'solicitud.txt',2),
        ('recibo_numero','DEMO-2026-014','solicitud.txt',4),
        ('pago_fecha','2026-10-29','solicitud.txt',4),
        ('experiencia.E1.contrato',True,'contrato.txt',2),
        ('experiencia.E1.monto_final','100000.00','contrato.txt',3),
        ('experiencia.E1.moneda_monto','PEN','contrato.txt',3),
        ('experiencia.E1.culminada',True,'conformidad.txt',2),
        ('experiencia.E1.aprobacion_viabilidad_conformidad',True,'conformidad.txt',2),
        ('experiencia.E1.descripcion_actividades',True,'conformidad.txt',3),
        ('experiencia.E1.comprobantes',['50000.00','30000.00'],'comprobantes.txt',2),
        ('experiencia.E1.moneda_comprobantes','PEN','comprobantes.txt',2),
    ]
    facts=[]
    for key,value,name,line in specs:
        d=docs[name];b=next(b for b in d['fragmentos'] if b['ubicacion']==f'linea:{line}')
        facts.append({'campo':key,'valor':value,'autor':'Simulación reproducible del coordinador',
                      'tipo_autor':'asistente_ia','fecha':'2026-10-31T12:00:00-05:00',
                      'evidencias':[{'documento':d['id'],'sha256':d['sha256'],'ubicacion':b['ubicacion'],'cita':b['texto']}]})
    guardar(folder/'hechos.json',facts)
    guardar(folder/'analisis.json',[{'texto':'La diferencia de PEN 20000.00 corresponde a honorarios de consultoría. Debe aclararse con sustento documental; no se presume que el presupuesto de la obra cubra el saldo. La participación en consorcio requiere identificar las obligaciones del solicitante antes de atribuirle experiencia.',
                                    'autor':'Simulación reproducible del coordinador','referencias':['AC-08/E1','AC-10/E1']}])
    output,_=procesar(folder,memory,False)
    return output

if __name__=='__main__':
    folder=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'data/operacion/ejemplo-consultores'
    print(create(folder))
