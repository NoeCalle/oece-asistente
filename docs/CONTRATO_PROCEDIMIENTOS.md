# Procedimientos y cálculos de la versión 1.1

El coordinador prepara estos datos a partir del expediente. El usuario no tiene que escribir JSON. Se aplica el [contrato de hechos y evidencias](CONTRATO_EXPEDIENTE.md): cita literal, ubicación, huella, autor, tipo de autor y fecha con zona. Una cita comprueba procedencia; su relación con el hecho requiere interpretación. OCR sin cotejo no acredita automáticamente un cumplimiento.

## Alcance temporal y resultados

Los cuatro módulos nuevos usan la ventana **01/05–31/10/2026**. Fuera de ella, los controles que darían cumple/no cumple pasan a no determinable; se conserva el cálculo como propuesta para revisar. No hay actualización automática de normas por fecha del equipo. Antes de ampliar la ventana deben comprobarse versiones, modificatorias y pruebas. Consultores mantiene su selección temporal específica J01–J05.

Los resultados son documentales y aritméticos. No autentican documentos, consultan SUNAT/RNP/TCP en vivo, conceden inscripción/capacidad ni resuelven recursos. El panel no interpreta automáticamente un documento con un modelo: esa tarea la realiza el coordinador en Codex.

## Selección en expediente.json

| Campo | Valores |
|---|---|
| `procedimiento` | `inscripcion`, `aumento_cmc`, `actualizacion`, `reconsideracion` o `ampliacion_consultores` |
| `fecha_solicitud` | Fecha ISO documentada; no fecha de creación de carpeta por defecto |
| `tipo_persona`, `origen_proveedor`, `domicilio` | Natural/jurídica, nacional/extranjero, domiciliado/no domiciliado; sin dato = null |
| `tipo_registro` | `bienes`, `servicios`, `consultor`, `ejecutor` |
| `tipo_tramite` | Para inscripción: `inscripcion` o `reinscripcion` |
| `clase_actualizacion` | `legal` o `financiera` |
| `motivo_actualizacion` | Financiera: `anual`, `rectificatoria`, `reduccion_capital_contable`, `reduccion_capital_social` |
| `documentos_extranjeros`, `documentos_en_espanol`, `actua_por_representante` | Booleanos o null; dato ausente no se convierte en falso |
| `experiencias` | Lista con `id`, `origen`, `consorcio`, `subcontrato` cuando corresponda; cotejar cada obra |

El panel permite estos campos de selección. Los campos especializados de consultores y los hechos se completan con el coordinador. La ficha declara una rama; no acredita por sí sola sus requisitos.

## Controles comunes e inscripción

Hechos usados: `identificacion_coincide`, `solicitud_presentada`, `recibo_numero`, `pago_fecha`, `ruc_activo`, `ruc_habido`, `inhabilitado`, `representacion_acreditada`, `capacidad_legal_acreditada`. Se seleccionan la excepción de RUC del extranjero no domiciliado y representación según la rama, sin consulta en vivo.

Para inscripción/reinscripción: `profesion_colegiacion_acreditada`, `informacion_financiera_completa`, `solvencia_acreditada`, `documentacion_registro_completa`, `sin_experiencia`, `experiencia_acreditada`, `inscrito_como_ejecutor` según registro/persona. Bienes y servicios no reciben automáticamente las exigencias financieras o de experiencia de obras. Consultor natural inscrito también como ejecutor tiene tratamiento financiero específico conforme a directiva 9.2.4. El hecho agregado `documentacion_registro_completa` exige que el coordinador haya examinado los documentos de la rama: el programa no los comprueba uno por uno solo por ese booleano.

Documentos extranjeros: `legalizacion_apostilla_original` y `traduccion_identifica_traductor`, condicionados a procedencia e idioma. Subsisten excepciones que deben motivarse con disposiciones adicionales verificadas.

## Capacidad máxima de contratación

La propuesta usa `sin_experiencia`, `informacion_financiera_disponible`, `moneda_calculo` = `PEN`, `universo_cmc_revisado` = true y, según rama, `activo_corriente`, `pasivo_corriente`, `anios_activos` y `obras_calculo_cmc`. Importes decimales como cadenas sin separador de miles; se rechazan booleanos, float, negativos y valores no finitos.

Cada obra de cálculo contiene `id`, `monto_neto_obra`, `monto_contratado`, `porcentaje_obligaciones` y `fecha_culminacion`. El universo debe estar documentado, sin duplicados, con obras culminadas al corte y no mayores de veinte años. Se atribuye el neto según obligaciones de consorcio; el denominador del factor de ejecución usa los montos contratados explícitos. Se permite que el monto final sea mayor que el contratado: no se inventa la restricción contraria. No se convierten monedas automáticamente.

- Con experiencia: sumatoria neta atribuida × (actividad + financiero + ejecución), según artículo 28 y directiva 9.2.5–9.2.6.
- Sin experiencia: tabla específica hasta PEN 500.000; sin información financiera, PEN 100.000. La regla expresa PC = 0 y AC positivo se aplica solo a esa rama; en otras no se extrapola.
- El aumento contrasta la propuesta con `cmc_vigente` citada y revisa `rnp_vigente`, `informacion_actualizada`, solvencia y documentación de cada obra. Una propuesta superior no basta para concederlo.

Por experiencia se examinan culminación, componente de obra, exclusiones, documentos de entidad o contrato/conformidad/comprobantes según procedencia; obligaciones de consorcio y autorización/documentos de subcontrato cuando corresponda. Los IDs exactos de hechos y controles están en [el evaluador](../oece/procedimientos.py). El universo financiero y de obras requiere revisión sustantiva; los controles no implementan toda solvencia contable ni todas las exclusiones posibles.

## Actualizaciones

Hechos: `solicitud_presentada`, `cambio_acreditado`, `formulario_actualizacion_firmado`, `sustentos_actualizacion_completos`, `fecha_cambio` o `ejercicio_financiero`, más representación/financieros aplicables.

La actualización legal y las financieras rectificatorias/reducciones calculan el último día calendario del mes siguiente. La financiera anual propone 30 de junio para nacional o 30 de septiembre para extranjero, del año siguiente al ejercicio culminado. Si la presentación supera el límite calendario, el resultado es no determinable hasta comprobar días inhábiles, exigibilidad, prórrogas y reglas especiales. No se declara extemporaneidad definitiva por aritmética de fechas.

## Reconsideración

Hechos: `acto_impugnado_identificado`, `requisitos_escrito_completos`, `notificacion_eficaz`, `acto_impugnable`, `mismo_organo`, `organo_unica_instancia`, `nueva_prueba`, `fundamentacion_vinculada_al_acto`, identidad y solicitud. La excepción de nueva prueba exige hecho citado de única instancia; no basta el nombre de un anexo.

El cómputo requiere `fecha_notificacion`, `calendario_recurso`, `calendario_entidad_confirmado`, `dias_termino_distancia` y `regla_general_recurso_aplicable`. El calendario declara `desde`, `hasta`, `semana_laboral` (lunes = 0, domingo = 6) y lista `dias_inhabiles`; debe cubrir íntegramente el cómputo. No se inventan feriados ni se presume distancia cero. Se cuentan 15 días hábiles posteriores a la notificación y los días de distancia declarados; no se resuelven eficacia de notificación, horario, canal, notificación tácita, suspensiones o régimen especial.

## Fuentes y conservación

[Registro de fuentes por control](../rules/procedimientos.v1.1.json) con original, URL, hash y página. Los cálculos y factores quedan en `matriz.json`; Word resume la propuesta y sus límites. La revisión conserva hechos, normas, análisis, originales y dependencias. Los [ejemplos reproducibles](../scripts/crear_demos_procedimientos.py) son ficticios; su calendario de reconsideración es sintético y no acredita el calendario oficial de una entidad.

## Contraste financiero desde 1.2

El coordinador prepara importes con citas y bases homogéneas. El informe incorpora R2/R3/R8, indicadores referenciales y reporte SBS documentado, con detección de contradicciones respecto de una declaración de solvencia. No convierte ratios en un dictamen ni aplica la excepción PC cero de CMC a solvencia. [Contrato financiero](CONTRASTE_FINANCIERO.md) y [verificación](VERIFICACION_V12.md). El corte no se amplía.
