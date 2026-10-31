"""Selección de ramas y verificaciones sobre hechos documentales trazables.

Una cita exacta prueba procedencia; su interpretación sigue identificada por autor.
No consulta registros en vivo ni decide autenticidad, categoría o capacidad oficial.
"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from .comun import ROOT, leer

VERSION = '1.0.0'
CORTE = date(2026, 10, 31)
MODULOS = {
    'ampliacion_consultores': 'Ampliación de categorías de consultores de obras',
    'aumento_cmc': 'Aumento de capacidad máxima de contratación',
    'inscripcion': 'Inscripción o reinscripción en el RNP',
    'actualizacion': 'Actualización de información del proveedor',
    'reconsideracion': 'Recurso de reconsideración',
}

def seleccionar(config):
    procedure = config.get('procedimiento')
    if procedure not in MODULOS:
        raise ValueError('Procedimiento desconocido')
    questions, warnings = [], []
    person, origin, home = (config.get(k) for k in ('tipo_persona', 'origen_proveedor', 'domicilio'))
    for key, value, options in [('tipo_persona', person, ('natural','juridica')),
                                ('origen_proveedor', origin, ('nacional','extranjero')),
                                ('domicilio', home, ('domiciliado','no_domiciliado'))]:
        if value not in options:
            questions.append(key)
    if origin == 'nacional' and home == 'no_domiciliado':
        questions.append('Corregir combinación nacional/no domiciliado para la clasificación RNP')
    regime = 'no_determinable'
    try:
        requested = date.fromisoformat(config.get('fecha_solicitud', ''))
        if requested > CORTE:
            questions.append('Actualizar normativa para una fecha posterior al corte 31/10/2026')
        elif procedure != 'ampliacion_consultores':
            regime = 'analisis_documental_por_procedimiento'
        elif requested <= date(2026,1,19) or config.get('tramite_en_curso_transicion') is not False:
            questions.append('Resolver frontera temporal o trámite en curso J01 con historial y actos del caso')
        elif config.get('primera_ampliacion_tras_recategorizacion') is True and config.get('historial_rnp_disponible') is True:
            regime = 'articulo_27_primera_ampliacion'
        elif config.get('regimen_categoria') == 'articulo_27' and config.get('historial_rnp_disponible') is True:
            regime = 'articulo_27_con_historial'
        else:
            questions.append('Aportar historial RNP y precisar primera ampliación o régimen ya asignado')
    except (ValueError, TypeError):
        questions.append('fecha_solicitud')
    experiences = config.get('experiencias', [])
    if not isinstance(experiences, list) or len(experiences) > 100:
        raise ValueError('Lista de experiencias inválida')
    ids = set()
    for exp in experiences:
        eid = exp.get('id')
        if not isinstance(eid, str) or not eid.isalnum() or eid in ids:
            raise ValueError('Cada experiencia necesita un ID alfanumérico único')
        ids.add(eid)
        if exp.get('origen') not in ('peru_ley','peru_fuera_ley','extranjero'):
            questions.append(f'Procedencia de experiencia {eid}')
        if type(exp.get('consorcio')) is not bool:
            questions.append(f'Participación en consorcio de experiencia {eid}')
    if config.get('categoria_solicitada') in ('A','B','C','D'):
        questions.append('Precisar significado de categoría y régimen; no homologar letras históricas')
    warnings.append('Ramas seleccionadas con datos declarados; la matriz distingue su acreditación documental')
    return {'regimen': regime, 'preguntas': questions, 'advertencias': warnings,
            'ruc_aplicable': None if person not in ('natural','juridica') or origin not in ('nacional','extranjero') or home not in ('domiciliado','no_domiciliado') else not (origin=='extranjero' and home=='no_domiciliado'),
            'experiencias': experiences, 'corte_normativo': CORTE.isoformat(),
            'criterios': 'normativa/decisiones-piloto.v0.2.json'}

def validar_hechos(facts, documents):
    if not isinstance(facts, list) or len(facts)>2000:
        raise ValueError('Lista de hechos inválida')
    index, result = {}, {}
    for d in documents:
        for b in d['fragmentos']:
            index[(d['id'],b['ubicacion'])]=(d,b)
    for fact in facts:
        key = fact.get('campo')
        if not isinstance(key,str) or not key or key in result or 'valor' not in fact:
            raise ValueError('Hecho duplicado o sin campo/valor')
        if fact.get('tipo_autor') not in ('asistente_ia','humano') or not str(fact.get('autor','')).strip():
            raise ValueError('Cada interpretación debe identificar autor y tipo')
        try:
            stamp=datetime.fromisoformat(fact['fecha'])
            if stamp.tzinfo is None:
                raise ValueError()
        except (KeyError,TypeError,ValueError):
            raise ValueError('Fecha del hecho requiere zona horaria')
        refs = fact.get('evidencias')
        if not isinstance(refs,list) or not refs:
            raise ValueError('Hecho sin evidencias localizables')
        blocked = False
        for ref in refs:
            pair=index.get((ref.get('documento'),ref.get('ubicacion')))
            if not pair:
                raise ValueError('Referencia de hecho inexistente')
            d,b=pair
            if ref.get('sha256')!=d['sha256'] or not ref.get('cita') or ref['cita'] not in b['texto']:
                raise ValueError('Cita alterada, vacía o fuente obsoleta')
            # OCR y fórmulas no se convierten en hechos acreditados por una cita textual.
            blocked = blocked or bool(b['alertas'])
        result[key]={**fact,'bloqueado_por_lectura':blocked}
    return result

def evaluar(config, documents, facts):
    route=seleccionar(config)
    facts=validar_hechos(facts,documents)
    controls=leer(ROOT/'rules/consultores/criterios-documentales.v1.json')['reglas']
    rows=[]
    def fact_value(key):
        f=facts.get(key)
        return f['valor'] if f and not f['bloqueado_por_lectura'] else None
    def emit(control, keys=(), invert=False, applicable=True, detail=None, exp=None):
        used=[facts[k] for k in keys if k in facts]
        missing=[k for k in keys if fact_value(k) is None]
        if applicable is False:
            outcome,reason='no_aplica','Rama no seleccionada; verificar los datos declarados del proveedor y experiencia'
        elif applicable is None or missing:
            outcome,reason='no_determinable','Faltan hechos acreditados o lectura apta: '+', '.join(missing or ['aplicabilidad'])
        else:
            values=[fact_value(k) for k in keys]
            if not values or any(type(v) is not bool for v in values):
                outcome,reason='no_determinable','Se requiere operación o interpretación expresa sobre los hechos citados'
            else:
                ok=all(not v if invert else v for v in values)
                outcome='cumple' if ok else 'no_cumple'
                reason='Verificación documental de los hechos citados, según interpretación de los autores identificados'
        if detail:
            outcome,reason=detail
        rows.append({'id':control['id']+(f'/{exp}' if exp else ''), 'control':control['control'],
                     'resultado':outcome,'motivo':reason,'hechos':[f['campo'] for f in used],
                     'evidencias':[r for f in used for r in f['evidencias']],
                     'autores':sorted({f['tipo_autor']+': '+f['autor'] for f in used}),
                     'fuente_normativa':control['fuente'], 'alcance':'documental_no_constituye_decision_del_OECE'})
    if config['procedimiento']!='ampliacion_consultores':
        # Los otros módulos comparten recepción, evidencias y redacción; sus decisiones
        # sustantivas se motivan en análisis firmado por autor, no en reglas prestadas.
        common=[('G-01','Identificación y objeto del procedimiento','identificacion_coincide'),
                ('G-02','Solicitud o escrito y pretensión','solicitud_presentada'),
                ('G-03','Documentos de sustento localizados','sustento_completo')]
        if config['procedimiento']=='reconsideracion':
            common += [('G-04','Acto impugnado y notificación','acto_notificado'),
                       ('G-05','Nueva prueba y supuesto aplicable','nueva_prueba_evaluada')]
        elif config['procedimiento']=='aumento_cmc':
            common += [('G-04','Experiencia en ejecución culminada','experiencia_ejecucion_acreditada'),
                       ('G-05','Capital solvencia y factores aplicables','calculo_cmc_revisado')]
        elif config['procedimiento']=='actualizacion':
            common += [('G-04','Información modificada y fecha del cambio','cambio_acreditado')]
        for rid,title,key in common:
            f=facts.get(key)
            rows.append({'id':rid,'control':title,'resultado':'no_determinable',
                         'motivo':'Evaluación sustantiva asistida; no hay reglas jurídicas automatizadas validadas para este módulo',
                         'hechos':[key] if f else [],'evidencias':f['evidencias'] if f else [],
                         'autores':[f['tipo_autor']+': '+f['autor']] if f else [],'fuente_normativa':None,
                         'alcance':'borrador_documental'})
        return {'seleccion':route,'matriz':rows,'hechos':facts,'alcance':'borrador_documental_otros_modulos'}
    for c in controls:
        rid=c['id']
        if rid=='AC-01':
            emit(c, detail=('cumple' if route['regimen'].startswith('articulo_27') else 'no_determinable',
                           'Selección del régimen según datos declarados: '+route['regimen']+'. No acredita categoría ni vigencia registral.'))
        elif rid in ('AC-05','AC-06','AC-07','AC-08','AC-09','AC-10','AC-11','AC-12','AC-13','AC-14','AC-15'):
            if not route['experiencias']:
                emit(c,detail=('no_determinable','No se han identificado experiencias para evaluar'))
            for exp in route['experiencias']:
                eid=exp['id']; prefix=f'experiencia.{eid}.'
                def e(suffixes, **kwargs):
                    emit(c,[prefix+s for s in suffixes],exp=eid,**kwargs)
                origin=exp.get('origen')
                if rid=='AC-05': e(['culminada'], applicable=True if origin in ('peru_ley','peru_fuera_ley','extranjero') else None)
                elif rid=='AC-06': e(['documento_entidad','datos_constancia_completos'],applicable=origin=='peru_ley' if origin else None)
                elif rid=='AC-07': e(['contrato','datos_contratante','aprobacion_viabilidad_conformidad','descripcion_actividades'],applicable=origin=='peru_fuera_ley' if origin else None)
                elif rid=='AC-09': e(['contrato','conformidad_viabilidad','datos_extranjero_completos'],applicable=origin=='extranjero' if origin else None)
                elif rid=='AC-10': e(['obligaciones_consorcio_identificadas'],applicable=exp.get('consorcio'))
                elif rid=='AC-11':
                    ok=config.get('categoria_solicitada') in ('a','b','c','d') and route['regimen'].startswith('articulo_27')
                    e(['objeto_corresponde_categoria','culminada'],applicable=True if ok else None)
                elif rid=='AC-12':
                    keys=['fecha_inicio_prestacion','fecha_colegiacion' if config.get('tipo_persona')=='natural' else 'fecha_inscripcion_registral']
                    vals=[fact_value(prefix+k) for k in keys]; detail=None
                    if all(isinstance(v,str) for v in vals):
                        try:
                            ok=date.fromisoformat(vals[0])>=date.fromisoformat(vals[1]); detail=('cumple' if ok else 'no_determinable','La prestación inicia después de la fecha profesional/registral citada' if ok else 'La prestación inicia antes de la fecha profesional/registral; delimitar experiencia posterior computable sin rechazar íntegramente por la fecha del contrato')
                        except ValueError: pass
                    e(keys,detail=detail)
                elif rid=='AC-13':
                    keys=['objeto_principal_revisado','sin_duplicacion']
                    e(keys)
                elif rid=='AC-14':
                    keys=['exclusiones_revisadas']
                    if exp.get('reorganizacion') is True: keys.append('excepcion_reorganizacion_revisada')
                    e(keys)
                elif rid in ('AC-08','AC-15'):
                    keys=['monto_final','comprobantes','moneda_monto','moneda_comprobantes'] if rid=='AC-08' else ['monto_final','moneda_monto','tipo_cambio','fecha_tipo_cambio','fecha_contrato']
                    applicable=(origin=='peru_fuera_ley' if origin in ('peru_ley','peru_fuera_ley','extranjero') else None) if rid=='AC-08' else None
                    detail=None
                    vals={k:fact_value(prefix+k) for k in keys}
                    if rid=='AC-15' and vals['moneda_monto']=='PEN': applicable=False
                    elif rid=='AC-15' and isinstance(vals['moneda_monto'],str): applicable=True
                    if applicable and all(v is not None for v in vals.values()):
                        try:
                            amount=Decimal(str(vals['monto_final']))
                            if not amount.is_finite() or amount<0: raise ValueError()
                            if rid=='AC-08':
                                if vals['moneda_monto']!=vals['moneda_comprobantes']: raise ValueError()
                                if not isinstance(vals['comprobantes'],list) or not vals['comprobantes']: raise ValueError()
                                numbers=[Decimal(str(v)) for v in vals['comprobantes']]
                                if any(not n.is_finite() or n<0 for n in numbers): raise ValueError()
                                delta=amount-sum(numbers)
                                detail=('cumple' if delta==0 else 'no_cumple',f'Diferencia entre monto final y suma de comprobantes: {delta} {vals["moneda_monto"]}')
                            else:
                                rate=Decimal(str(vals['tipo_cambio']))
                                if not rate.is_finite() or rate<=0: raise ValueError()
                                date.fromisoformat(vals['fecha_contrato']); date.fromisoformat(vals['fecha_tipo_cambio'])
                                if vals['fecha_contrato']!=vals['fecha_tipo_cambio']: raise ValueError()
                                detail=('cumple',f'Conversión documentada: {amount} × {rate} = {(amount*rate).quantize(Decimal("0.01"))} PEN; fuente del cambio debe cotejarse en las citas')
                        except (InvalidOperation,ValueError,TypeError):
                            detail=('no_determinable','Importes, moneda o fecha de tipo de cambio incompatibles; no se calcula con supuestos')
                    e(keys,applicable=applicable,detail=detail)
        else:
            mapping={'AC-02':['identificacion_coincide'], 'AC-03':['solicitud_presentada'],
                     'AC-16':['condiciones_articulo25_revisadas'],'AC-17':['ruc_activo','ruc_habido'],
                     'AC-18':['inhabilitado'],'AC-19':['rnp_vigente','informacion_actualizada'],
                     'AC-20':['representacion_acreditada'],'AC-21':['capacidad_legal_acreditada'],
                     'AC-22':['solvencia_aplicable','solvencia_acreditada']}
            if rid=='AC-04':
                keys=['recibo_numero','pago_fecha']; vals=[fact_value(k) for k in keys]; detail=None
                if all(isinstance(v,str) and v.strip() for v in vals):
                    try:
                        date.fromisoformat(vals[1]); detail=('cumple','Número de recibo y fecha localizados; no acredita validación del pago en línea')
                    except ValueError: pass
                emit(c,keys,detail=detail)
            elif rid=='AC-22' and fact_value('solvencia_aplicable') is False:
                emit(c,['solvencia_aplicable'],detail=('no_determinable','La alegada dispensa financiera requiere motivación de la rama en reglamento, directiva y TUPA; no se concede una excepción universal'))
            elif rid=='AC-20' and config.get('actua_por_representante') is False and config.get('tipo_persona')=='natural':
                emit(c,applicable=False)
            else:
                emit(c,mapping[rid],invert=rid=='AC-18',applicable=route['ruc_aplicable'] if rid=='AC-17' else True)
    for row in rows:
        if route['regimen']=='no_determinable' and row['resultado'] in ('cumple','no_cumple'):
            row['resultado']='no_determinable'
            row['motivo']='Régimen temporal sin seleccionar. Verificación parcial conservada: '+row['motivo']
    return {'seleccion':route,'matriz':rows,'hechos':facts,'alcance':'verificacion_documental_condicionada_a_hechos_citados'}
