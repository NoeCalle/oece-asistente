"""Cuatro expedientes ficticios para comprobar las ampliaciones del motor."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oece.comun import guardar
from oece.flujo import iniciar,Memoria,preparar,procesar

def crear(raiz):
    raiz=Path(raiz);memory=Memoria(raiz/'.oece');outputs={}
    calendar={'desde':'2026-10-01','hasta':'2026-12-31','semana_laboral':[0,1,2,3,4],'dias_inhabiles':['2026-10-08']}
    cases={
      'inscripcion':({'tipo_registro':'bienes','tipo_tramite':'inscripcion','tipo_persona':'natural','actua_por_representante':False},[
        ('identificacion_coincide',True,'En esta simulación la identidad coincide con la solicitud ficticia presentada.'),
        ('solicitud_presentada',True,'Solicitud ficticia presentada para inscripción como proveedor de bienes.'),
        ('recibo_numero','DEMO-IN-01','Recibo ficticio DEMO-IN-01, pagado el 2026-10-29.'),
        ('pago_fecha','2026-10-29','Fecha de pago de ejemplo 2026-10-29; no es validación bancaria.'),
        ('ruc_activo',True,'Consulta tributaria ficticia: estado activo y condición habido.'),
        ('ruc_habido',True,'Consulta tributaria ficticia: estado activo y condición habido.'),
        ('inhabilitado',False,'Consulta ficticia del proveedor: sin inhabilitación vigente en esta simulación.'),
        ('capacidad_legal_acreditada',True,'Capacidad legal ficticia sustentada para el ejemplo de persona natural.'),
        ('documentacion_registro_completa',True,'Los documentos de la rama de persona natural nacional para bienes están completos en la simulación.')]),
      'aumento_cmc':({'tipo_registro':'ejecutor','tipo_persona':'juridica','experiencias':[{'id':'O1','origen':'peru_fuera_ley','consorcio':True}]},[
        ('sin_experiencia',False,'Se acredita una obra ficticia culminada en el ejemplo.'),
        ('informacion_financiera_disponible',True,'Balance ficticio disponible: activo corriente PEN 300000 y pasivo corriente PEN 100000.'),
        ('activo_corriente','300000','Activo corriente ficticio PEN 300000.'),
        ('pasivo_corriente','100000','Pasivo corriente ficticio PEN 100000.'),
        ('moneda_calculo','PEN','Todos los montos del ejemplo están expresados en PEN.'),
        ('universo_cmc_revisado',True,'Universo ficticio revisado: monto neto de obra sin equipamiento ni consultoría, monto contratado total y participación por obligaciones del 50 por ciento.'),
        ('anios_activos',6,'Seis años de actividad en obras acreditados en la simulación, dentro de los veinte últimos años.'),
        ('obras_calculo_cmc',[{'id':'O1','monto_neto_obra':'1000000','monto_contratado':'1000000','porcentaje_obligaciones':'50','fecha_culminacion':'2026-08-01'}],
          'Obra ficticia O1: neto PEN 1000000, contratado PEN 1000000, obligaciones 50 por ciento, culminación 2026-08-01.'),
        ('cmc_vigente','200000','CMC vigente ficticia PEN 200000. No es una consulta al RNP.')]),
      'actualizacion':({'tipo_registro':'consultor','clase_actualizacion':'legal','tipo_persona':'juridica'},[
        ('solicitud_presentada',True,'Formulario de actualización ficticio presentado el 2026-10-30.'),
        ('cambio_acreditado',True,'Variación ficticia de domicilio ocurrida el 2026-08-10.'),
        ('fecha_cambio','2026-08-10','La variación ficticia de domicilio ocurrió el 2026-08-10.'),
        ('formulario_actualizacion_firmado',True,'El formulario de esta simulación se declara firmado; no contiene firma real.'),
        ('sustentos_actualizacion_completos',True,'Se incluyen sustentos ficticios de la variación de domicilio para el ejemplo.')]),
      'reconsideracion':({'tipo_persona':'juridica'},[
        ('identificacion_coincide',True,'Identidad del recurrente ficticio coincide con el escrito de ejemplo.'),
        ('solicitud_presentada',True,'Recurso ficticio presentado el 2026-10-30 contra la resolución DEMO-R-01.'),
        ('acto_impugnado_identificado',True,'Acto ficticio impugnado: resolución DEMO-R-01.'),
        ('requisitos_escrito_completos',True,'Los requisitos del escrito se declaran completos en este supuesto sintético.'),
        ('notificacion_eficaz',True,'Notificación ficticia declarada eficaz el 2026-10-01, solo para la simulación.'),
        ('acto_impugnable',True,'El acto de ejemplo se declara impugnable para esta simulación.'),
        ('mismo_organo',True,'El escrito ficticio se dirige al mismo órgano que emitió el acto.'),
        ('organo_unica_instancia',False,'El órgano del supuesto ficticio no constituye única instancia.'),
        ('nueva_prueba',False,'En la simulación no se ha aportado nueva prueba.'),
        ('fecha_notificacion','2026-10-01','Fecha de notificación del supuesto: 2026-10-01.'),
        ('calendario_recurso',calendar,'Calendario exclusivamente sintético del servicio: lunes a viernes y 2026-10-08 inhábil, cobertura octubre a diciembre. No es calendario oficial.'),
        ('calendario_entidad_confirmado',True,'Para probar el algoritmo se confirma el calendario ficticio anterior, sin afirmar validación institucional.'),
        ('dias_termino_distancia',0,'En este supuesto ficticio el término de distancia documentado es cero.'),
        ('regla_general_recurso_aplicable',True,'Solo para el supuesto de prueba se aplica la regla general; no se invoca régimen especial.')])}
    for module,(extra,specs) in cases.items():
        folder=raiz/('demo-'+module)
        if folder.exists():raise ValueError('Usar una raíz de ejemplos nueva')
        c=iniciar(folder,module,'Proveedor Ficticio Sin Datos Reales',True)
        c.update(fecha_solicitud='2026-10-30',tipo_persona='juridica',origen_proveedor='nacional',domicilio='domiciliado',documentos_extranjeros=False,documentos_en_espanol=True)
        c.update(extra);guardar(folder/'expediente.json',c)
        lines=['EJEMPLO SINTÉTICO. No es un expediente ni consulta real.']+[s[2] for s in specs]
        (folder/'documentos/supuesto.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        result,_=preparar(folder,memory,False);d=result['documentos'][0]
        facts=[]
        for n,(key,value,text) in enumerate(specs,2):
            facts.append({'campo':key,'valor':value,'autor':'Simulación del coordinador','tipo_autor':'asistente_ia','fecha':'2026-10-31T15:00:00-05:00',
                          'evidencias':[{'documento':d['id'],'ubicacion':f'linea:{n}','sha256':d['sha256'],'cita':text}]})
        guardar(folder/'hechos.json',facts);outputs[module]=str(procesar(folder,memory,False)[0])
    guardar(raiz/'entregas.json',outputs)
    return outputs

if __name__=='__main__':
    import json
    print(json.dumps(crear(Path(sys.argv[1])),ensure_ascii=True,indent=2))
