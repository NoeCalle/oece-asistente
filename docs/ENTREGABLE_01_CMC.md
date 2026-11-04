# Entregable 1 de 3 — Formato de cálculo de la Capacidad Máxima de Contratación (CMC)

**Registrado:** 04/11/2026. **Origen:** tres fotografías aportadas por el usuario durante la definición de OECE Assistant. **Estado:** referencia funcional recibida; **adaptación de plantilla y validación con expediente autorizado pendientes**. Este archivo documenta requisitos, **no** acredita un caso ni la vigencia de normas posteriores al corte del repositorio (31/10/2026).

## Alcance y relación con los otros entregables

El usuario identifica este conjunto documental como **uno** de los **tres entregables laborales** que deberá poder preparar OECE Assistant. No deducir el nombre, contenido ni requisitos de los entregables 2 y 3: se registrarán cuando los aporte.

Las tres fotografías son tres **vistas/hojas de referencia del mismo tipo de entregable CMC**; no confundirlas con los tres entregables laborales. Las imágenes contienen formatos y datos de ejemplo que no deben asumirse del mismo expediente (la relación de obras de la primera fotografía es distinta de las obras de la tercera). **No subir fotografías, nombres de proveedores, RUC, expedientes ni originales a este repositorio público.** Mantenerlos en carpeta privada autorizada.

## Estructura observable del entregable CMC

1. **Formato institucional de resultado.** Encabezado «OECE – DRNP – SDOR / Formato para el cálculo de la capacidad máxima de contratación», **versión 01, fecha de aprobación 29/12/2025** según fotografía. Casillas de proveedor, N.º de trámite y tipo de trámite. Expone **CMC = Σ Obras × G**, con **G = a + f + e**: actividad en obras, financiero y ejecución. Sección de hasta cinco obras visibles en el ejemplo, sumatoria, casilla resaltada «CMC a otorgar», nota sobre actualización de información legal y financiera para aumento de CMC, y constancia «consultas en páginas web: sí/no», fuentes y fechas de consulta. El número de filas visible **no debe constituir límite artificial** para expedientes con más obras.
2. **Hoja auxiliar de cálculo.** Cuadro por obra con monto contratado, monto de experiencia, fecha de contrato y recepción; eje por años para revisar período; tablas de factores **f** (capital de trabajo y liquidez), **a** (antigüedad) y **e** (relación de ejecución). Permite explicar por qué cada factor y año se emplearon y sumar los importes usados.
3. **Relación analítica de obras.** Datos del trámite, proveedor y RNP; importe de activo corriente y pasivo corriente; por obra: identificador/objeto, monto del contrato en moneda original, fecha de suscripción, fecha de recepción, porcentaje de participación, monto final liquidado en soles, descuentos —por ejemplo equipamiento/mobiliario— y monto de experiencia. Incluye exclusiones (una obra identificada como «DESISTIDO»), totales y campos sin completar. Los guiones o blancos **son pendientes**, no ceros verificados.

## Campos para extracción estructurada y trazabilidad

- **Cabecera:** identificador del expediente/trámite; procedimiento `aumento_cmc`; proveedor y RUC, tipo de registro, fecha de solicitud/corte, CMC vigente informada por RNP y fecha/fuente de consulta.
- **Período:** fecha de corte y ventana de veinte años pertinente a la regla aplicable; registrar fecha de contrato y culminación/recepción por separado y cualquier fecha que requiera contraste. El eje de años de la hoja auxiliar no reemplaza el control de vigencia.
- **Por obra:** ID estable, código de procedimiento/contrato, objeto, estado (candidata, incluida, excluida, pendiente), motivo de exclusión —incluido desistimiento—, moneda/unidad, monto de contrato, monto final, descuentos, monto neto admisible, participación u obligaciones atribuibles y **si el monto de experiencia ya incluye esa participación**; fechas de suscripción, culminación, recepción, documentos probatorios y referencias verificables.
- **Finanzas y factores:** AC, PC, período/fuente, capital de trabajo, liquidez o regla especial para PC=0, años de actividad sustentados, factor `a`, factor `f`, cociente de ejecución, factor `e`, `G`, `Σ Obras`, CMC calculada y comparación con la CMC vigente cuando proceda.
- **Cierre:** verificación legal/financiera, observaciones, consultas externas realizadas realmente (fuente y fecha; no marcar sí sin consultar), estado borrador/revisión, nombre/fecha del revisor humano **solo cuando haya revisión real** y ubicación privada del documento.

Cada cifra usada debe remitir a un documento y a un localizador/cita, más el cálculo reproducible. Cuando falte el monto liquidado o el soporte de descuentos, marcar `no_determinable`/pendiente en lugar de inferirlo de «monto contratado». No atribuir el mismo porcentaje de consorcio dos veces.

## Ejemplo aritmético visible en hoja auxiliar (NO caso validado)

La hoja de trabajo muestra, a título **ilustrativo**, `Σ Obras = S/ 6 050 000`, `a = 1,50`, `f = 0,50`, `e = 0,25`; por tanto `G = 2,25` y **CMC = S/ 13 612 500**. La relación de contratos presenta un total de **S/ 7 400 000**. La hoja financiera exhibe AC de **S/ 2 500 000** y PC de **S/ 500 000**. Los importes manuscritos de experiencia suman 6 050 000, pero en la ficha detallada las columnas de liquidación, descuentos y experiencia están vacías. Por ello la cifra **no queda acreditada con las fotografías** y debe reconstruirse de los sustentos del expediente. El importe RNP visible no debe presumirse aprobado o contrastable sin confirmar concepto, fecha y fuente.

Atención: el formato de resultado (fotografía 1) contiene códigos de obras **distintos** del ejemplo analítico (fotografías 2–3). **No cruzar ni concatenar ambos ejemplos** como un expediente homogéneo.

## Integración prevista sin rehacer el motor

- **Motor existente:** `oece/calculos.py::cmc`, procedimiento `aumento_cmc`, validaciones y contratos de `docs/CONTRATO_PROCEDIMIENTOS.md`. La aritmética con `Decimal` ya existe; no sustituirla por lectura visual ni dejar que una IA elija resultados sin datos citados.
- **Adaptador de datos:** mapear documentos reales al contrato del motor, cotejando tratamiento de montos netos, consorcios y exclusiones, y distinguiendo `monto_contratado` de `monto_de_experiencia`. Investigar especialmente el caso donde monto informado de experiencia **ya está atribuido** por porcentaje, para evitar ponderación doble.
- **Generador de formato:** incorporar plantilla CMC **independiente del Word de informe provisional**; conservar formulario visual o un equivalente editable y sus hojas de cálculo/relación de obras cuando sean requeridas. Registrar versión/código/fecha de plantilla y no presentar un facsímil no verificado como formulario oficial. Exportar borrador revisable, no decisión ni «CMC otorgada» institucional.
- **Coordinación humana:** mostrar de forma clara evidencia faltante, datos incompletos, obras excluidas, discrepancias entre auxiliares y principal, consultas no efectuadas, normativa por fecha y datos que requieren conformidad especializada.
- **Privacidad:** imágenes originales y expedientes laborales exclusivamente en ubicación autorizada, nunca en GitHub público; este documento contiene sólo los requisitos y números ilustrativos mínimos.

## Criterios de aceptación para la adaptación

1. Para expedientes sintéticos, reproducir con `Decimal` la fórmula y factores del caso ilustrativo **sin presentar los montos como probados**.
2. Generar un **entregable CMC diferenciado** con encabezado, factores, relación de obras, sumatoria, resultado y registro de consultas/observaciones; no limitar el número de obras a cinco.
3. Poder excluir una obra desistida y señalar que una obra sin evidencias de culminación, montos finales o participación permanece pendiente.
4. Detectar contraste inconsistente entre hoja de obras, hoja auxiliar y formato final; impedir doble aplicación de porcentajes de participación.
5. Mantener evidencias, huellas, referencias normativas, fecha/corte, versiones, autoría y revisión humana sin afirmar consulta en línea o emisión oficial no realizada.
6. Probar con datos ficticios y revisar visualmente salida antes de validar un primer expediente laboral autorizado.

## Seguimiento

Ver `docs/TAREAS.md` **T49** y el issue asociado. La recepción de este formato satisface parcialmente la espera de modelo documental en T33, **pero no cierra T33** (otros entregables y revisión institucional pendientes).
