"""Cálculos reproducibles. Los datos deben estar acreditados antes de invocarlos."""
from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def numero(value, minimum=Decimal('0')):
    if isinstance(value,bool) or not isinstance(value,(str,int,Decimal)):
        raise ValueError('Importe decimal inválido; usar cadena sin separador de miles')
    try: result=Decimal(value)
    except InvalidOperation: raise ValueError('Importe decimal inválido')
    if not result.is_finite() or result<minimum: raise ValueError('Importe no finito o fuera del rango')
    return result

def fecha(value):
    if not isinstance(value,str): raise ValueError('Fecha ISO requerida')
    return date.fromisoformat(value)

def fin_mes_siguiente(value):
    d=fecha(value); year,month=(d.year+1,1) if d.month==12 else (d.year,d.month+1)
    return date(year,month,monthrange(year,month)[1]).isoformat()

def vencimiento_recurso(notification,calendar,days=15,distance=0):
    """No inventa feriados: requiere cobertura y jornada declaradas y citadas.

    No decide eficacia de notificación, reglas especiales, hora o canal de ingreso.
    """
    start=fecha(notification)
    if type(days) is not int or not 1<=days<=365 or type(distance) is not int or not 0<=distance<=365:
        raise ValueError('Término de días inválido')
    if not isinstance(calendar,dict): raise ValueError('Calendario documentado requerido')
    begin,end=fecha(calendar['desde']),fecha(calendar['hasta'])
    week=calendar.get('semana_laboral');holidays=calendar.get('dias_inhabiles')
    if not isinstance(week,list) or not week or len(set(week))!=len(week) or any(type(v) is not int or v not in range(7) for v in week):
        raise ValueError('Jornada semanal explícita requerida')
    if not isinstance(holidays,list) or len(set(holidays))!=len(holidays): raise ValueError('Días inhábiles explícitos requeridos')
    excluded={fecha(v) for v in holidays}
    if start<begin or start>end or any(d<begin or d>end for d in excluded): raise ValueError('Calendario fuera de cobertura')
    current=start;count=0;sequence=[]
    while count<days+distance:
        current+=timedelta(days=1)
        if current>end: raise ValueError('Calendario insuficiente para el plazo')
        if current.weekday() in week and current not in excluded:
            count+=1;sequence.append(current.isoformat())
    return {'vencimiento':current.isoformat(),'dias_base':days,'dias_distancia_declarados':distance,
            'dias_contados':sequence,'alcance':'comparacion_de_fechas_con_calendario_declarado_no_hora_ni_canal'}

def cmc(sin_experiencia,informacion_financiera,activo=None,pasivo=None,anios_activos=None,obras=None,corte=None):
    if type(sin_experiencia) is not bool or type(informacion_financiera) is not bool:
        raise ValueError('Precisar experiencia e información financiera')
    obras=obras or []
    if sin_experiencia and obras: raise ValueError('No acumular obras en la rama sin experiencia')
    if sin_experiencia and not informacion_financiera:
        return {'cmc_propuesta':'100000.00','rama':'sin_experiencia_sin_informacion','fundamento':'Directiva 9.2.5 PDF p. 9'}
    if informacion_financiera:
        ac,pc=numero(activo),numero(pasivo);working=ac-pc
        if pc==0:
            if not sin_experiencia or ac<=0:
                raise ValueError('La regla explícita PC cero se limita a ejecutor sin experiencia y AC positivo')
            band=2;liquidity=None
        else:
            liquidity=ac/pc
            if liquidity<1 or working<0: raise ValueError('Liquidez o capital de trabajo fuera de la tabla')
            band=0 if liquidity<2 else 1 if liquidity<3 else 2
        if sin_experiencia and working<=0:
            raise ValueError('La tabla sin experiencia exige diferencia AC-PC positiva')
        row=0 if working<=20000 else 1 if working<=100000 else 2 if working<=300000 else 3
        financial=Decimal('0.10')+Decimal(row)*Decimal('0.10')+Decimal(band)*Decimal('0.05')
    else:
        financial=Decimal('0.10');liquidity=None;working=None
    if sin_experiencia:
        return {'cmc_propuesta':str((financial*1000000).quantize(Decimal('.01'))),'rama':'sin_experiencia_con_informacion',
                'factor_financiero':str(financial),'liquidez':str(liquidity) if liquidity is not None else 'PC_cero_regla_especial',
                'capital_trabajo':str(working),'fundamento':'Directiva 9.2.5 PDF pp. 8–9; Reglamento 28.4'}
    if type(anios_activos) is not int or not 1<=anios_activos<=20 or not obras or not corte:
        raise ValueError('Se requieren años activos, obras y fecha de corte')
    activity=Decimal('0.40') if anios_activos<=5 else Decimal('1.00') if anios_activos<=10 else Decimal('1.50') if anios_activos<=15 else Decimal('2.00')
    reference=fecha(corte);net=Decimal(0);contracts=Decimal(0);details=[];seen=set()
    for work in obras:
        if not isinstance(work.get('id'),str) or not work['id'] or work['id'] in seen:
            raise ValueError('Obra duplicada o sin identificador')
        seen.add(work['id'])
        ended=fecha(work['fecha_culminacion'])
        if ended>reference: raise ValueError('Obra no culminada al corte')
        try: anniversary=ended.replace(year=ended.year+20)
        except ValueError: anniversary=ended.replace(year=ended.year+20,day=28)
        if reference>anniversary: raise ValueError('Obra supera veinte años: delimitar universo antes de calcular')
        share=numero(work['porcentaje_obligaciones'])
        if share<=0 or share>100: raise ValueError('Porcentaje de obligaciones fuera de rango')
        amount=numero(work['monto_neto_obra']);contract=numero(work['monto_contratado'])
        if amount<=0 or contract<=0: raise ValueError('Monto neto o contratado no positivo')
        weighted=amount*share/100
        net+=weighted;contracts+=contract
        details.append({'id':work['id'],'neto_atribuido':str(weighted),'monto_contratado':str(contract)})
    ratio=net/contracts;execution=Decimal('.25') if ratio<1 else Decimal('.50')
    management=activity+financial+execution
    value=(net*management).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    return {'cmc_propuesta':str(value),'rama':'con_experiencia','sumatoria_neta':str(net),'sumatoria_contratos':str(contracts),
            'factor_actividad':str(activity),'factor_financiero':str(financial),'ratio_ejecucion':str(ratio),
            'factor_ejecucion':str(execution),'coeficiente_gestion':str(management),'detalle_obras':details,
            'operacion':'sumatoria_neta * (actividad + financiero + ejecucion)',
            'alcance':'propuesta_aritmetica_condicionada_al_universo_y_datos_documentados_no_CMC_oficial'}
