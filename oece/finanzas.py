"""Ratios documentados: aritmética reproducible, sin dictamen de solvencia."""
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import re

from .calculos import fecha
from .comun import ROOT, leer


def importe(value, no_negativo=False):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)) or len(str(value)) > 100:
        raise ValueError('Importe financiero decimal inválido')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError('Importe financiero decimal inválido')
    if (not result.is_finite() or len(result.as_tuple().digits) > 36
            or not -12 <= result.as_tuple().exponent <= 24 or abs(result) > Decimal('1e24')
            or no_negativo and result < 0):
        raise ValueError('Importe financiero fuera del alcance de cálculo')
    return result


def ratio(code, data):
    """Compara sin redondear. R8 usa multiplicación exacta para el tercio."""
    with localcontext() as context:
        context.prec = 80
        if code == 'R2':
            numerator = importe(data['patrimonio'])
            denominator = importe(data['pasivo_corriente'], True) + importe(data['pasivo_no_corriente'], True)
            ok, limit = numerator >= denominator * Decimal('.05'), '0.05'
        elif code == 'R3':
            numerator = importe(data['activo_corriente'], True)
            denominator = importe(data['pasivo_corriente'], True)
            ok, limit = numerator >= denominator, '1'
        elif code == 'R8':
            numerator = importe(data['patrimonio'])
            denominator = importe(data['capital_social'], True)
            ok, limit = numerator * 3 >= denominator, '1/3'
        elif code == 'R9':
            numerator = importe(data['utilidad_operativa'])
            denominator = importe(data['patrimonio']) + importe(data['pasivo_no_corriente'], True)
            ok, limit = None, None
        elif code == 'RC':
            numerator = importe(data['perdidas_acumuladas'], True)
            denominator = importe(data['capital_base_perdidas'], True)
            ok, limit = None, '0.5; interpretar cobertura patrimonial y sentido de la regla'
        else:
            raise ValueError('Ratio desconocido')
        if denominator <= 0:
            raise ValueError('Denominador no positivo; no se presume infinito ni cumplimiento')
        value = numerator / denominator
        return {'ratio': code, 'numerador': str(numerator), 'denominador': str(denominator),
                'valor_aproximado': str(value.quantize(Decimal('.000000000001'))),
                'umbral': limit, 'satisface_umbral_aritmetico': ok,
                'alcance': 'indicador_referencial_sin_dictamen' if code in ('R9', 'RC') else 'comparacion_aritmetica_no_solvencia_integral'}


def aplicabilidad(config, value):
    procedure = config['procedimiento']
    if procedure == 'reconsideracion' or procedure == 'actualizacion' and config.get('clase_actualizacion') != 'financiera':
        return False
    role = 'consultor' if procedure == 'ampliacion_consultores' else 'ejecutor' if procedure == 'aumento_cmc' else config.get('tipo_registro')
    if role in ('bienes', 'servicios'):
        return False
    if role == 'ejecutor':
        return True
    if role == 'consultor':
        if config.get('tipo_persona') == 'juridica':
            return True
        if config.get('tipo_persona') == 'natural':
            registered = value('inscrito_como_ejecutor')
            return registered if type(registered) is bool else None
    return None


def incorporar(result, config):
    facts = result['hechos']
    def value(key):
        f = facts.get(key)
        return f['valor'] if f and not f['bloqueado_por_lectura'] else None
    applicable = aplicabilidad(config, value)
    if applicable is False:
        return result
    registry = leer(ROOT / 'rules/finanzas.v1.2.json')
    sources = registry['fuentes']
    rows = result['matriz']
    calculations = result.setdefault('calculos', {}).setdefault('finanzas', {'ratios': {}, 'indicadores': {}})

    def emit(rid, title, status, reason, keys, source='dir923'):
        used = [facts[k] for k in keys if k in facts]
        rows.append({'id': rid, 'control': title, 'resultado': status, 'motivo': reason,
                     'hechos': [f['campo'] for f in used],
                     'evidencias': [e for f in used for e in f['evidencias']],
                     'autores': sorted({f['tipo_autor'] + ': ' + f['autor'] for f in used}),
                     'fuente_normativa': sources[source],
                     'fuentes_complementarias': [sources['reg2552']] + ([sources['dir924'], sources['dir933']] if config['procedimiento'] == 'ampliacion_consultores' else []),
                     'alcance': 'propuesta_aritmetica_financiera_no_dictamen_institucional'})

    base_keys = ['fecha_estados_financieros', 'moneda_estados_financieros', 'base_financiera_homogenea']
    try:
        if applicable is not True:
            raise ValueError('Precisar rama y, para consultor natural, inscripción vigente como ejecutor; no presumir dispensa financiera')
        if value('informacion_financiera_disponible') is False and value('base_financiera_homogenea') is True:
            raise ValueError('Contradicción: se declaran bases financieras cotejadas y, a la vez, información financiera no disponible')
        if value('base_financiera_homogenea') is not True:
            raise ValueError('Cotejar mismo período, moneda, unidad y ámbito de los importes; no se mezclan estados de matriz/sucursal')
        end = fecha(value('fecha_estados_financieros'))
        if end > fecha(config.get('fecha_solicitud')):
            raise ValueError('Los estados financieros citados son posteriores a la solicitud')
        if not isinstance(value('moneda_estados_financieros'), str) or not re.fullmatch('[A-Z]{3}', value('moneda_estados_financieros')):
            raise ValueError('Identificar moneda de los estados; no convertir ni mezclar monedas')
        base_ok, base_reason = True, 'Bases citadas declaradas homogéneas; verificar vigencia y suficiencia de los estados para la rama'
        calculations.update(fecha_estados=end.isoformat(), moneda=value('moneda_estados_financieros'))
    except (ValueError, TypeError) as error:
        base_ok, base_reason = False, str(error)
    emit('FIN-01', 'Bases para el contraste financiero', 'cumple' if base_ok else 'no_determinable', base_reason,
         base_keys + (['inscrito_como_ejecutor'] if config.get('tipo_persona') == 'natural' else []))

    fields = {'R2': ['patrimonio', 'pasivo_corriente', 'pasivo_no_corriente'],
              'R3': ['activo_corriente', 'pasivo_corriente'], 'R8': ['patrimonio', 'capital_social'],
              'R9': ['utilidad_operativa', 'patrimonio', 'pasivo_no_corriente'],
              'RC': ['perdidas_acumuladas', 'capital_base_perdidas']}
    for code, keys in fields.items():
        data = {key: value(key) for key in keys}
        try:
            if not base_ok:
                raise ValueError('Bases financieras sin cotejo suficiente: ' + base_reason)
            missing = [key for key in keys if data[key] is None]
            if missing:
                raise ValueError('Faltan importes citados: ' + ', '.join(missing))
            calculation = ratio(code, data)
            status = 'cumple' if calculation['satisface_umbral_aritmetico'] else 'no_cumple'
            reason = (f'Ratio {code} ≈ {calculation["valor_aproximado"]}; umbral ≥ {calculation["umbral"]}. '
                      'Comparación con valores exactos, sin redondear para decidir; no determina solvencia integral.')
        except (ValueError, TypeError, ArithmeticError) as error:
            calculation = {'ratio': code, 'estado': 'no_determinable', 'motivo': str(error)}
            status, reason = 'no_determinable', str(error)
        target = 'indicadores' if code in ('R9', 'RC') else 'ratios'
        calculations[target][code] = calculation
        if code in ('R9', 'RC'):
            calculation['hechos'] = base_keys + keys
            calculation['evidencias'] = [e for key in base_keys + keys for e in facts.get(key, {}).get('evidencias', [])]
            if code == 'RC':
                calculation['nota'] = 'No automatiza un sentido de aprobación/rechazo a partir de ≥ 0.5; cotejar otras cuentas libres que cubran pérdidas y el análisis patrimonial.'
            continue
        emit('FIN-' + code, 'Contraste aritmético del ratio ' + code, status, reason, keys + base_keys,
             'dir923' if code == 'R2' else 'dir923_p7')

    sbs_keys = ['clasificacion_sbs', 'fecha_reporte_sbs', 'ultimo_reporte_sbs_confirmado']
    try:
        if applicable is not True or any(value(k) is None for k in sbs_keys) or value('ultimo_reporte_sbs_confirmado') is not True:
            raise ValueError('Se necesita el último reporte SBS identificado y citado; no es consulta en línea')
        if fecha(value('fecha_reporte_sbs')) > fecha(config.get('fecha_solicitud')):
            raise ValueError('Reporte SBS posterior a la solicitud')
        category = value('clasificacion_sbs')
        if category not in ('normal', 'no_reportado', 'problemas_potenciales', 'deficiente', 'dudoso', 'perdida'):
            raise ValueError('Clasificación SBS sin interpretación reconocida')
        status = 'cumple' if category in ('normal', 'no_reportado') else 'no_cumple'
        reason = 'Clasificación del reporte citado: ' + category + '; no acredita una consulta SBS en vivo'
    except (ValueError, TypeError) as error:
        status, reason = 'no_determinable', str(error)
    emit('FIN-SBS', 'Clasificación documentada de la central de riesgos', status, reason, sbs_keys, 'reg2552')
    key = 'analisis_solvencia_integral_documentado'
    status = 'cumple' if applicable is True and value(key) is True else 'no_determinable'
    emit('FIN-INTEGRAL', 'Evaluación integral y equilibrio patrimonial', status,
         'Análisis citado para revisar; los ratios aislados no prueban solvencia ni autenticidad' if status == 'cumple'
         else 'Falta análisis integral citado de solvencia y equilibrio capital/patrimonio, incluidas pérdidas y coberturas cuando correspondan',
         [key], 'reg2552')
    conflicts = [row['id'] for row in rows if row['id'] in ('FIN-R2', 'FIN-R3', 'FIN-R8', 'FIN-SBS') and row['resultado'] == 'no_cumple']
    if conflicts:
        for row in rows:
            if row['id'] in ('AC-22', 'CMC-08', 'IN-09', 'AU-04') and row['resultado'] == 'cumple':
                row['resultado_documental_previo'] = row['resultado']
                row['resultado'] = 'no_determinable'
                row['contrastes_en_conflicto'] = conflicts
                row['motivo'] = 'La declaración citada de solvencia requiere aclaración frente a los contrastes ' + ', '.join(conflicts) + '. Se conservan hechos y citas; no se presume solvencia integral.'
    try:
        in_range = date.fromisoformat(registry['ventana_automatica'][0]) <= fecha(config.get('fecha_solicitud')) <= date.fromisoformat(registry['ventana_automatica'][1])
    except (ValueError, TypeError):
        in_range = False
    calculations['ventana_verificada'] = in_range and result['seleccion']['regimen'] != 'no_determinable'
    if not in_range or result['seleccion']['regimen'] == 'no_determinable':
        for row in rows:
            if row['id'].startswith('FIN-') and row['resultado'] in ('cumple', 'no_cumple'):
                row['resultado'] = 'no_determinable'
                row['motivo'] = 'Rama o ventana temporal financiera sin verificar. Propuesta conservada: ' + row['motivo']
    return result
