# Datos de un expediente operativo

El usuario trabaja con carpetas, documentos y conversación. Este contrato sirve al coordinador para preparar esos datos sin pedir al usuario que programe ni redacte JSON.

## Archivos y conservación

`expediente.json` identifica procedimiento, solicitante, fecha, persona, origen y domicilio. Los originales se conservan en `documentos/`. `hechos.json` registra interpretaciones con citas. `analisis.json` contiene párrafos adicionales con referencias. `normas.json` añade disposiciones específicas verificadas. `lectura.json` es la lectura de trabajo. `salida/<revision>/` conserva Word, matriz CSV/JSON, manifiesto y copia de originales/configuración. Ninguno de esos datos se publica en Git.

Datos de selección para consultores: `historial_rnp_disponible`, `primera_ampliacion_tras_recategorizacion`, `tramite_en_curso_transicion` (booleanos o null), `regimen_categoria` opcional `articulo_27`, `categoria_solicitada` a/b/c/d según artículo 27, `actua_por_representante`. `experiencias` contiene ID alfanumérico, `origen` (`peru_ley`, `peru_fuera_ley`, `extranjero`), `consorcio` y, si corresponde, `reorganizacion`. No introducir un dato ausente como falso.

## Hechos citados

Cada hecho tiene un campo único, valor, autor, tipo de autor, fecha con zona y una o más evidencias. Ejemplo de estructura (los valores de referencia se obtienen de la lectura real, no se copian de este ejemplo):

```json
{
  "campo": "experiencia.E1.culminada",
  "valor": true,
  "autor": "Coordinador OECE Assistant",
  "tipo_autor": "asistente_ia",
  "fecha": "2026-10-31T12:00:00-05:00",
  "evidencias": [{
    "documento": "ID obtenido de lectura.json",
    "ubicacion": "pagina:2",
    "sha256": "huella completa del original",
    "cita": "Texto literal que respalda la interpretación"
  }]
}
```

Las citas inexistentes, vacías o de otra huella se rechazan. Un fragmento OCR pendiente de cotejo o una fórmula no recalculada no habilitan un hecho favorable. Una cita exacta acredita procedencia, no prueba por sí sola la verdad ni la corrección de una interpretación; el coordinador debe contrastar el contenido y queda identificado como autor IA. Las fuentes externas representan el estado a la fecha de su documento, no una consulta en vivo.

Después de inspeccionar la imagen, el coordinador puede registrar `cotejos.json`: lista de `{documento, ubicacion, sha256, imagen_sha256, transcripcion, autor, tipo_autor, fecha}`. La imagen original derivada está en la caché de lecturas por huella. Solo se admite un cotejo por fragmento OCR y deben coincidir fuente e imagen. Se conserva el texto OCR anterior junto con la transcripción declarada y su autor. Esto habilita el uso de esa transcripción; el sistema no autentica al revisor ni demuestra por código que miró la imagen. Nunca marcar como humano el cotejo del asistente. No permite convertir una fórmula sin recalcular en hecho revisado.

Campos globales del evaluador de consultores: `identificacion_coincide`, `solicitud_presentada`, `recibo_numero` (texto), `pago_fecha` (ISO), `condiciones_articulo25_revisadas`, `ruc_activo`, `ruc_habido`, `inhabilitado`, `rnp_vigente`, `informacion_actualizada`, `representacion_acreditada`, `capacidad_legal_acreditada`, `solvencia_aplicable`, `solvencia_acreditada`. Salvo indicación, son booleanos, no textos "sí". La negativa de aplicabilidad de solvencia exige motivación específica y no da una exoneración automática.

Campos por experiencia, prefijo `experiencia.<ID>.`: `culminada`, `documento_entidad`, `datos_constancia_completos`, `contrato`, `datos_contratante`, `aprobacion_viabilidad_conformidad`, `descripcion_actividades`, `conformidad_viabilidad`, `datos_extranjero_completos`, `obligaciones_consorcio_identificadas`, `objeto_corresponde_categoria`, `objeto_principal_revisado`, `sin_duplicacion`, `exclusiones_revisadas`, `excepcion_reorganizacion_revisada` (booleanos). Los controles agregados requieren revisar sus datos exigidos completos; la mera aparición del nombre del documento no acredita el agregado.

Campos de cálculo: `monto_final` y `tipo_cambio` son cadenas decimales sin separador de miles; `comprobantes` es lista de cadenas decimales; `moneda_monto` y `moneda_comprobantes` son códigos como PEN/USD; `fecha_contrato`, `fecha_inicio_prestacion`, `fecha_colegiacion`, `fecha_inscripcion_registral` y `fecha_tipo_cambio` son fechas ISO. La comparación profesional/registral usa inicio de la prestación, no la sola firma del contrato ni constitución sin inscripción. Un inicio anterior requiere delimitar la parte computable, no rechazar íntegramente la experiencia. Se usa Decimal; monedas incompatibles, cantidades no finitas, fecha de cambio distinta del contrato y ausencia de tasa producen resultado indeterminado. El control de comprobantes compara honorario de consultoría con honorario, no presupuesto de obra.

## Análisis y normas adicionales

`analisis.json` es una lista de párrafos `{texto, autor, referencias}`. Cada referencia debe existir en la matriz, en documentos o en códigos normativos adicionales. Esto comprueba resolución de referencias; la sustentación semántica corresponde al autor, no a un comparador de cadenas.

`normas.json` es una lista `{codigo, archivo, sha256, url, pagina_pdf, disposicion, cita, autor, criterio}`. El código tiene forma `N-identificador`; archivo, URL y hash deben coincidir con un original manifestado. La página debe existir y la cita ser literal en ella. `criterio` explica por qué esa disposición y versión se aplica al caso. No usar un acto distinto como sustituto del habilitante no comprobado. El cotejo de citas funciona con PDF digital; normas escaneadas precisan lectura visual y preparación separada, sin afirmar que el OCR las valida.

## Estados y límites

El motor de consultores ejecuta verificaciones documentales condicionadas a los hechos registrados y al régimen seleccionado. No concede categorías, no prueba autenticidad, no firma y no presenta trámites. El resultado favorable de un control no equivale a una conclusión favorable global. Régimen sin determinar impide resolver automáticamente sus controles sustantivos. Los otros cuatro módulos ejecutan controles documentales propios y propuestas aritméticas de CMC/plazos en la ventana 01/05–31/10/2026; no constituyen evaluadores sustantivos completos. Ver [campos, fuentes y límites](CONTRATO_PROCEDIMIENTOS.md).
