# Contrato de datos CMC — ficha maestra para tres formatos

**Fecha: 05/11/2026.** Se dispone de la estructura de datos y de pruebas sintéticas. **Los archivos editables nativos de los tres formatos aún no han sido recibidos.** No confundir los JSON preparados con el formato institucional final.

## Objetivo

Leer los PDF escaneados de contratos, cartas, resoluciones de recepción y liquidaciones una sola vez con la IA visual elegida por el usuario. Conservar una **ficha maestra de datos** (archivo privado `datos-cmc.json`) con fuentes de cada obra y cifra. Después generar tres paquetes diferenciados que permitan llenar las plantillas nativas cuando el usuario las proporcione.

El esquema se obtiene mediante `oece_modelo_cmc(caso)` o `oece_entrada(caso, tipo="datos_cmc")`. Incluye seis claves: `version`, `expediente`, `obras`, `factores`, `consultas` y `observaciones`. No añadir ni eliminar claves arbitrariamente.

### Expediente

`proveedor`, `numero_tramite`, `tipo_tramite` (necesariamente `aumento_cmc`), `rnp`, `fecha_corte`, `activo_corriente` y `pasivo_corriente`.

### Cada elemento de `obras[]`

| Campo | Qué significa |
|---|---|
| `id` | ID de obra estable (por ejemplo OB-01) |
| `objeto`, `entidad`, `numero_contrato` | Identificación contractual |
| `fecha_contrato`, `fecha_recepcion` | Fechas propuestas con sustento documental |
| `monto_contrato`, `moneda_contrato` | Monto contractual original y moneda |
| `porcentaje_participacion` | Participación del proveedor en consorcio |
| `participacion_aplicada` | `true` si el monto de experiencia ya refleja la participación; `false` si aún no; `null` si se desconoce |
| `monto_liquidado` | Liquidación final propuesta; **no confundir con monto contractual** |
| `descuento_equipamiento`, `otros_descuentos` | Importes que pueden requerir exclusión o revisión |
| `monto_experiencia` | Importe propuesto por la IA, **no aceptado automáticamente** |
| `estado` | `propuesta_incluir`, `pendiente` o `excluida` |
| `motivo_estado` | Justificación de la propuesta de inclusión, desistimiento o exclusión |
| `anios_marcados` | Años propuestos para el segundo formato, **sin inferencia automática por fecha** |
| `evidencias` | Cada entrada tiene `campo`, `documento`, `pagina` y `cita` |
| `observaciones` | Incertidumbres y comprobaciones pendientes |

**Citas:** `documento` debe ser ID `D<sha12>` del inventario del expediente; `pagina` es la página física del PDF empezando en 1. OECE verifica que fuente, huella y página existan. La literalidad de la cita y su interpretación visual quedan pendientes de revisión profesional.

**Importes:** representar decimales en cadenas sin separador de miles, como `"1250000.50"`. Un dato desconocido es `null`, nunca cero inventado. La IA distingue monto contratado, liquidado, deducciones, pagos y experiencia. No aplicar dos veces el porcentaje de un consorcio.

### Factores y consultas

`factores` contiene `actividad` (a), `financiero` (f) y `ejecucion` (e). Cada factor requiere `valor` (decimal o `null`), `sustento`, `referencias` (PDF, página y cita) y `norma_por_verificar`. OECE calcula `G=a+f+e` con `Decimal` solo si existen los tres valores, sin acreditar su corrección o vigencia normativa.

`consultas[]` contiene `servicio`, `realizada` (booleano), `fecha`, `resultado` y `referencias`. **No marcar una consulta como realizada si el asistente no la ejecutó realmente.**

## Orden y correspondencia con las plantillas futuras

1. **Formato 1 — Relación de obras y montos:** `entregable-01-datos.json`. Enumera obras propuestas, pendientes, desistidas y excluidas. Conserva montos contractuales, liquidación, descuentos, consorcios y experiencia, cada uno con sus referencias. Excluidas no suman.
2. **Formato 2 — Matriz de años y factores:** `entregable-02-datos.json`. Toma exclusivamente las obras computables propuestas de la fase 1 y coloca fechas, años, experiencia, a/f/e y G. Si un año está pendiente, no cierra la CMC provisional.
3. **Formato 3 — Resumen institucional CMC:** `entregable-03-datos.json`. Recibe los resultados de las dos fases, calcula cuando hay suficientes datos `CMC_calculada_provisional_soles = ΣObras×G` y conserva `CMC_a_otorgar = null`. La propuesta nunca equivale a otorgamiento administrativo.

Cuando falta evidencia de un monto, recepción, participación o criterio legal, el resultado se mantiene como parcial o pendiente. Los valores ilustrativos de las fotografías del 04/11 (**S/ 7 400 000; S/ 6 050 000; G=2,25; CMC=13 612 500**) **no son datos verificados de un único expediente** y nunca deben copiarse al nuevo caso.

## Operación con IA agnóstica y MCP

1. La IA elegida abre `oece_contexto` y `oece_archivos`, lee cada página con `oece_pagina_visual` y, cuando corresponda, prepara la lectura visual y los cálculos de liquidación.
2. Consulta `oece_modelo_cmc` para conocer **todos** los campos. Recupera `oece_entrada(caso,tipo="datos_cmc")` para obtener contenido previo y SHA-256.
3. Completa `datos_cmc` con todos los campos, referencias por página, estados y `null` donde faltan pruebas. Guarda con `oece_guardar(caso,tipo="datos_cmc",contenido=...,sha_esperado=...)`.
4. Ejecuta `oece_publicar_cmc(caso)`. OECE valida el contrato, fuentes, fechas, importes, exclusiones y dependencias. Publica los cuatro JSON, incluido `ficha-maestra.json`, en `datos_formatos_cmc/<revision_sha256>/`, sin sobrescribir versiones.
5. Cuando se reciban las tres plantillas nativas editables, se crearán adaptadores de celdas/campos para **copiar solo los datos revisados**. La verificación final comparará sus valores y fórmulas con los tres JSON. La lectura y clasificación de PDF **no deberá repetirse** salvo que haya nuevas evidencias.

Por CLI: `python -m oece formatos-cmc RUTA --modelo` muestra el esquema; `python -m oece formatos-cmc RUTA` publica, siempre que la ficha maestra esté guardada. Ninguna operación llama a una API de IA.

**Importante:** el paquete significa «datos listos para vinculación», no «monto validado» ni «CMC otorgada». Se requiere cotejo humano, fuentes normativas vigentes, y revisión de los archivos nativos cuando existan. No colocar datos laborales ni copias de expedientes en GitHub público.
