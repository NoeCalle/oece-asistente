"""Verificaciones documentales por procedimiento y cálculos de alcance explícito."""
from datetime import date
from .calculos import cmc, fecha, fin_mes_siguiente, vencimiento_recurso
from .comun import ROOT, leer

class Evaluador:
    def __init__(self,config,route,facts):
        self.config,self.route,self.facts=config,route,facts
        self.sources=leer(ROOT/'rules/procedimientos.v1.1.json')['fuentes']
        self.rows=[];self.calculations={}
    def value(self,key):
        f=self.facts.get(key)
        return f['valor'] if f and not f['bloqueado_por_lectura'] else None
    def row(self,rid,title,source,keys=(),applicable=True,invert=False,operation=None,extras=()):
        used=[self.facts[k] for k in keys if k in self.facts]
        values=[self.value(k) for k in keys]
        if applicable is False:
            status,reason='no_aplica','Fuera de la rama seleccionada; verificar los datos de clasificación declarados'
        elif applicable is None or any(v is None for v in values):
            missing=[k for k,v in zip(keys,values) if v is None]
            status,reason='no_determinable','Falta información acreditada o aplicabilidad: '+', '.join(missing or ['rama'])
        elif operation:
            try: status,reason=operation(*values)
            except (ValueError,TypeError,KeyError,ArithmeticError) as error:
                status,reason='no_determinable',str(error)
        elif any(type(v) is not bool for v in values) or not values:
            status,reason='no_determinable','Se necesitan datos del tipo indicado y una interpretación respaldada'
        else:
            ok=all(not v if invert else v for v in values)
            status='cumple' if ok else 'no_cumple'
            reason='Verificación documental según hechos citados y autoría declarada; no consulta en vivo ni decisión administrativa'
        self.rows.append({'id':rid,'control':title,'resultado':status,'motivo':reason,
                          'hechos':[f['campo'] for f in used], 'evidencias':[r for f in used for r in f['evidencias']],
                          'autores':sorted({f['tipo_autor']+': '+f['autor'] for f in used}),
                          'fuente_normativa':self.sources[source],
                          'fuentes_complementarias':[self.sources[s] for s in extras],
                          'alcance':'documental_y_aritmetico_condicionado_a_hechos_citados'})
    def payment(self,rid,source):
        def check(receipt,paid):
            if not isinstance(receipt,str) or not receipt.strip(): raise ValueError('Número de recibo requerido')
            payment=fecha(paid);requested=fecha(self.config['fecha_solicitud'])
            return ('cumple','Número y fecha localizados; no valida el pago en línea') if payment<=requested else ('no_cumple','La fecha de pago citada es posterior a la solicitud declarada; aclarar la secuencia')
        self.row(rid,'Número de recibo y fecha de pago',source,['recibo_numero','pago_fecha'],operation=check)
    def common(self,prefix,source,payment=True):
        self.row(prefix+'01','Identidad y solicitud',source,['identificacion_coincide','solicitud_presentada'])
        if payment:self.payment(prefix+'02',source)
        self.row(prefix+'03','Condición RUC activo y habido cuando corresponde','reg25',['ruc_activo','ruc_habido'],applicable=self.route['ruc_aplicable'])
        self.row(prefix+'04','Ausencia de inhabilitación vigente documentada','reg25',['inhabilitado'],invert=True)
        representative=self.config.get('actua_por_representante')
        applicable=False if representative is False and self.config.get('tipo_persona')=='natural' else True if representative is True or self.config.get('tipo_persona')=='juridica' else None
        self.row(prefix+'05','Facultad de representación y registro aplicable','reg25',['representacion_acreditada'],applicable=applicable)
        self.row(prefix+'06','Capacidad legal según registro y persona','reg25',['capacidad_legal_acreditada'])
    def foreign_documents(self,prefix):
        foreign=self.config.get('documentos_extranjeros')
        self.row(prefix+'EX1','Legalización o apostilla del documento original','reg25',['legalizacion_apostilla_original'],applicable=foreign)
        spanish=self.config.get('documentos_en_espanol')
        applicable=False if foreign is False or spanish is True else True if foreign is True and spanish is False else None
        self.row(prefix+'EX2','Traducción simple con identificación del traductor','reg25',['traduccion_identifica_traductor'],applicable=applicable)
    def registration(self):
        role=self.config.get('tipo_registro');mode=self.config.get('tipo_tramite')
        source='reg381_bienes' if role in ('bienes','servicios') else 'reg381_consultores' if role=='consultor' else 'reg381_ejecutores' if role=='ejecutor' else 'reg381_general'
        self.common('IN-',source)
        valid=role in ('bienes','servicios','consultor','ejecutor') and mode in ('inscripcion','reinscripcion')
        self.row('IN-07','Tipo de registro y modalidad del trámite',source,operation=lambda:('cumple','Registro y modalidad declarados; verificar concordancia con la solicitud') if valid else ('no_determinable','Precisar tipo_registro y tipo_tramite'))
        self.row('IN-08','Profesión y colegiación aplicables','reg25',['profesion_colegiacion_acreditada'],applicable=self.config.get('tipo_persona')=='natural' and role in ('consultor','ejecutor') if valid else None)
        financial=True if role=='ejecutor' or role=='consultor' and self.config.get('tipo_persona')=='juridica' else False if role in ('bienes','servicios') else self.value('inscrito_como_ejecutor') if role=='consultor' else None
        self.row('IN-09','Información y solvencia financiera de la rama',source,['informacion_financiera_completa','solvencia_acreditada'],applicable=financial,extras=('dir924',))
        self.row('IN-10','Documentación específica de la rama del artículo 381',source,['documentacion_registro_completa'],applicable=True if valid else None)
        if role in ('consultor','ejecutor'):
            no_experience=self.value('sin_experiencia')
            self.row('IN-11','Experiencia acreditada cuando se invoca',source,['experiencia_acreditada'],applicable=False if no_experience is True else True if no_experience is False else None)
        self.foreign_documents('IN-')
        if role=='ejecutor':self.capacity('IN-CMC')
    def capacity(self,rid='CMC-09'):
        keys=['sin_experiencia','informacion_financiera_disponible','moneda_calculo','universo_cmc_revisado']
        no_experience=self.value('sin_experiencia');financial=self.value('informacion_financiera_disponible')
        if financial is True:keys+=['activo_corriente','pasivo_corriente']
        if no_experience is False:keys+=['anios_activos','obras_calculo_cmc']
        def calculate(*values):
            data=dict(zip(keys,values))
            if data['moneda_calculo']!='PEN' or data['universo_cmc_revisado'] is not True:
                raise ValueError('Antes de calcular, acreditar moneda PEN y universo neto/contratado revisado, incluyendo consorcios y exclusiones')
            result=cmc(data['sin_experiencia'],data['informacion_financiera_disponible'],data.get('activo_corriente'),data.get('pasivo_corriente'),data.get('anios_activos'),data.get('obras_calculo_cmc'),self.config['fecha_solicitud'])
            self.calculations['cmc']=result
            return 'cumple','Propuesta aritmética de CMC: PEN '+result['cmc_propuesta']+'. No acredita el otorgamiento, aumento ni solvencia general del proveedor.'
        self.row(rid,'Cálculo propuesto de capacidad máxima de contratación','reg28',keys,operation=calculate,extras=('formula_cmc','dir925','dir926','dir926d','dir932'))
    def capacity_increase(self):
        self.common('CMC-','reg381_aumento')
        self.row('CMC-07','RNP de ejecutor e información actualizada','reg25',['rnp_vigente','informacion_actualizada'])
        self.row('CMC-08','Solvencia y documentación financiera aplicable','reg25',['solvencia_acreditada','informacion_financiera_completa'])
        self.capacity()
        proposed=self.calculations.get('cmc')
        def compare(current):
            from .calculos import numero
            if not proposed:raise ValueError('No hay CMC propuesta calculable')
            increased=numero(proposed['cmc_propuesta'])>numero(current)
            return ('cumple','La propuesta aritmética supera la CMC vigente citada') if increased else ('no_cumple','La propuesta aritmética no supera la CMC vigente citada; no se sustenta aumento con estos valores')
        self.row('CMC-10','Contraste de propuesta con CMC vigente','reg381_aumento',['cmc_vigente'],operation=compare)
        experiences=self.route['experiencias']
        if not experiences:self.row('CMC-11','Experiencia culminada para sustentar aumento','reg381_aumento',['experiencia_acreditada'])
        for exp in experiences:
            eid=exp['id'];prefix=f'experiencia.{eid}.';origin=exp.get('origen')
            keys=['culminada','componente_obra_delimitado','exclusiones_revisadas']
            if origin=='peru_ley':keys+=['documento_entidad','datos_constancia_completos']
            elif origin=='peru_fuera_ley':keys+=['contrato','datos_contratante','conformidad_obra','comprobantes_equivalentes']
            elif origin=='extranjero':keys+=['contrato','datos_extranjero_completos']
            else:origin=None
            self.row('CMC-11/'+eid,'Documentación de obra según procedencia','reg381_aumento',[prefix+k for k in keys],applicable=True if origin else None)
            if exp.get('consorcio') is True:self.row('CMC-12/'+eid,'Obligaciones y porcentaje de consorcio','dir926',[prefix+'obligaciones_consorcio_identificadas'])
            if exp.get('subcontrato') is True:self.row('CMC-13/'+eid,'Autorización y documentos de subcontrato bajo Ley','reg381_aumento',[prefix+'subcontrato_autorizado',prefix+'documentacion_subcontrato_completa'])
        self.foreign_documents('CMC-')
    def update(self):
        kind=self.config.get('clase_actualizacion')
        self.row('AU-01','Solicitud y variación que se actualiza','reg26',['solicitud_presentada','cambio_acreditado'])
        self.row('AU-02','Formulario firmado y sustentos aplicables','dir96',['formulario_actualizacion_firmado','sustentos_actualizacion_completos'])
        if kind=='legal' or kind=='financiera' and self.config.get('motivo_actualizacion') in ('rectificatoria','reduccion_capital_contable','reduccion_capital_social'):
            def limit(change):
                end=fin_mes_siguiente(change);presented=fecha(self.config['fecha_solicitud'])
                if presented<fecha(change):raise ValueError('La solicitud precede al cambio; revisar fechas')
                self.calculations['actualizacion']={'limite_calendario':end,'regla':'finalizacion_mes_siguiente','requiere_cotejar_dia_habil_y_reglas_especiales':True}
                return ('cumple','La fecha de presentación está dentro del límite calendario '+end+'; cotejar prórroga si el último día es inhábil') if presented<=fecha(end) else ('no_determinable','La fecha supera el límite calendario '+end+'; revisar días inhábiles, prórrogas y reglas especiales antes de declarar extemporaneidad')
            self.row('AU-03','Límite del mes siguiente de ocurrida la variación','reg26',['fecha_cambio'],operation=limit,extras=('dir96','dir967'))
        elif kind=='financiera' and self.config.get('motivo_actualizacion')=='anual':
            def annual(year):
                if type(year) is not int or year<2000 or year>=fecha(self.config['fecha_solicitud']).year:raise ValueError('Se requiere un ejercicio anual culminado anterior al año de presentación')
                origin=self.config.get('origen_proveedor')
                if origin not in ('nacional','extranjero'):raise ValueError('Origen del proveedor pendiente')
                end=date(year+1,6,30) if origin=='nacional' else date(year+1,9,30)
                self.calculations['actualizacion']={'limite_calendario':end.isoformat(),'ejercicio':year,'requiere_cotejar_exigibilidad_y_prorrogas':True}
                return ('cumple','Presentación dentro del límite calendario anual '+end.isoformat()) if fecha(self.config['fecha_solicitud'])<=end else ('no_determinable','Posterior al límite calendario anual '+end.isoformat()+'; revisar exigibilidad, días inhábiles y reglas especiales')
            self.row('AU-03','Límite anual según proveedor nacional o extranjero','reg26',['ejercicio_financiero'],operation=annual)
        else:self.row('AU-03','Clase y motivo de actualización','reg26',operation=lambda:('no_determinable','Precisar clase legal/financiera y motivo anual/rectificatoria/reducción'))
        if kind=='financiera':
            applicable=self.config.get('tipo_registro') in ('consultor','ejecutor') if self.config.get('tipo_registro') else None
            self.row('AU-04','Información financiera y solvencia de la rama','dir967',['informacion_financiera_completa','solvencia_acreditada'],applicable=applicable)
        self.row('AU-05','Representación para actualización','dir96',['representacion_acreditada'],applicable=False if self.config.get('tipo_persona')=='natural' and self.config.get('actua_por_representante') is False else True)
        self.foreign_documents('AU-')
    def reconsideration(self):
        self.row('RC-01','Acto impugnado y requisitos del escrito','tuo211',['identificacion_coincide','solicitud_presentada','acto_impugnado_identificado','requisitos_escrito_completos'])
        self.row('RC-02','Notificación eficaz y acto recurrible','tuo207',['notificacion_eficaz','acto_impugnable'])
        self.row('RC-03','Interposición ante el mismo órgano','tuo208',['mismo_organo'])
        def proof(unique,new):
            if type(unique) is not bool:raise ValueError('Precisar si el órgano constituye única instancia')
            if unique:return 'no_aplica','Nueva prueba no exigida en el supuesto documentado de única instancia del artículo 208'
            if type(new) is not bool:raise ValueError('Evaluar nueva prueba; el título de un anexo no basta')
            return ('cumple','Nueva prueba identificada e interpretada en las citas') if new else ('no_cumple','No se acredita nueva prueba en la rama que la exige')
        unique=self.value('organo_unica_instancia')
        keys=['organo_unica_instancia'] if unique is True else ['organo_unica_instancia','nueva_prueba']
        self.row('RC-04','Nueva prueba y excepción de única instancia','tuo208',keys,operation=lambda *v:proof(v[0],v[1] if len(v)>1 else None))
        def term(notified,calendar,confirmed,distance,general):
            if confirmed is not True or general is not True:raise ValueError('Confirmar calendario de la entidad y aplicación de regla general antes del cómputo')
            result=vencimiento_recurso(notified,calendar,distance=distance);self.calculations['reconsideracion']=result
            requested=fecha(self.config['fecha_solicitud'])
            if requested<fecha(notified):raise ValueError('Presentación anterior a notificación; revisar eficacia y antecedentes')
            ok=requested<=fecha(result['vencimiento'])
            return ('cumple' if ok else 'no_cumple','Comparación de fechas con calendario citado: vencimiento '+result['vencimiento']+'. No decide hora, canal, notificación tácita ni régimen especial.')
        self.row('RC-05','Cómputo propuesto de quince días hábiles','tuo207',['fecha_notificacion','calendario_recurso','calendario_entidad_confirmado','dias_termino_distancia','regla_general_recurso_aplicable'],operation=term,extras=('tuo133','tuo135'))
        self.row('RC-06','Fundamentación y relación de la prueba con el acto','tuo208',['fundamentacion_vinculada_al_acto'])
    def run(self):
        {'inscripcion':self.registration,'aumento_cmc':self.capacity_increase,'actualizacion':self.update,'reconsideracion':self.reconsideration}[self.config['procedimiento']]()
        # Versiones antiguas o posteriores al corte no reciben conclusión automática.
        requested=self.config.get('fecha_solicitud')
        try: in_range=date(2026,5,1) <= fecha(requested) <= date(2026,10,31)
        except (ValueError,TypeError):in_range=False
        if not in_range:
            for row in self.rows:
                if row['resultado'] in ('cumple','no_cumple'):
                    row['resultado']='no_determinable';row['motivo']='Fuera de la ventana temporal verificada 01/05–31/10/2026. '+row['motivo']
        return {'seleccion':self.route,'matriz':self.rows,'hechos':self.facts,'calculos':self.calculations,
                'alcance':'verificaciones_documentales_y_calculos_por_procedimiento_no_decision_administrativa'}

def evaluar_procedimiento(config,route,facts):
    return Evaluador(config,route,facts).run()
