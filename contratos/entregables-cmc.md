# Contrato de salida — aumento de CMC: DOS entregables operativos

**Decisión del titular (06/11/2026):** para la evaluación ordinaria de aumento de Capacidad Máxima de Contratación (CMC), el paquete visible del especialista consta de **un Excel de evaluación** y **un Word de observaciones**. Esta instrucción **sustituye** la antigua entrega obligatoria de ficha maestra y tres JSON independientes en el modo agent-first. Los modelos de datos [históricos](../docs/CONTRATO_DATOS_CMC.md), [relación de obras](../docs/ENTREGABLE_01_RELACION_OBRAS.md), [factores](../docs/ENTREGABLE_02_FACTORES_EXPERIENCIA.md) y [resumen de cálculo](../docs/ENTREGABLE_03_RESUMEN_CMC.md) se conservan como **etapas lógicas y referencias de validación internas**, no como entregables adicionales ni como tres formularios que haya que inventar.

## Entregable 1 — Excel institucional MPR de evaluación

**Formato:** copia íntegra de la plantilla MPR vigente que facilite el titular, con **todas sus pestañas originales** (en el piloto, seis); no crear un Excel nuevo con tres hojas ni reconstruir la plantilla salvo instrucción expresa. Preservar fórmulas, combinaciones, estilos, tablas, nombre de hojas, anchos, elementos de plantilla y vínculos. Original intocable. La extensión/guardado final debe ser compatible con Microsoft Excel 2013 del titular. Para el piloto, la fuente que abre correctamente es el archivo binario `.xlsb` y la escritura segura utiliza el Excel de Windows autorizado; **no fingir compatibilidad probada si no se abrió en Excel**.

**Rellenado progresivo:** primero `Datos basicos` con los campos sustentados; luego `Obras nacional` conforme lleguen uno o varios PDF por obra. En cada campo de `Obras nacional`, la columna `G` («inicial pág») identifica la página física, **desde 1**, del PDF **concreto** que sustenta el dato; guardar además el nombre/ID del PDF en el expediente privado (no asumir que todas las obras están en un mismo PDF). La columna `J` contiene el dato y la `L` las notas necesarias. Nombres de obra en la **celda ancla de los encabezados combinados**, como texto, nunca imagen. No sobreescribir fórmulas con valores ni completar campos sin soporte como cero. Referencia: [procedimiento de llenado](../procedimientos/llenado-excel-aumento-cmc.md).

**Cálculo:** continuar dentro de las hojas previstas por la plantilla con liquidaciones, componentes netos, adicionales/deductivos, participación consorcial, años/factores y CMC cuando la evidencia sea suficiente. Mantener claramente diferenciada CMC **simulada/provisional** de una capacidad aprobada. En controles internos `CMC_a_otorgar=null` salvo decisión institucional ajena al agente.

**Control de aceptación:** estructura idéntica salvo cambios autorizados, fórmulas preservadas, páginas G asociadas al PDF correcto, montos reproducibles y cotejados, títulos de obras visibles, estado de campos y limitaciones; verificar apertura real en Excel 2013 cuando se disponga del programa.

## Entregable 2 — Word de observaciones documentales

**Formato:** un único `.docx` editable, breve, con título `Observaciones documentales — [expediente]`, fecha/corte, estado de revisión y fuente del expediente. No duplicar el contenido de todas las pestañas del Excel.

**Estructura sugerida:**
1. **Identificación y alcance:** expediente, procedimiento, documentos revisados y grado real de revisión (página leída, pendiente, escaneo dudoso).
2. **Observaciones numeradas:** una fila o párrafo por observación con `ID`, `obra` o `expediente`, `documento/PDF y página`, `hecho comprobado`, `discrepancia o faltante`, `impacto`, `acción recomendada`, `estado`. Distinguir `inconsistencia_documental`, `integridad_escaneo`, `dato_pendiente` y `control_por_verificar`.
3. **Conclusión operativa muy breve:** qué se puede seguir evaluando; qué campos/obras quedan reservados; documentación necesaria para cerrar observaciones.

**No emitir observaciones solo por errores tipográficos irrelevantes ni considerar OCR escaso prueba de página faltante.** Registrar diferencias reales sin declarar automáticamente incumplimiento o rechazo. Cuando no se detecten observaciones tras la revisión posible, el Word puede decir `Sin observaciones documentales identificadas en el alcance revisado`, aclarando verificaciones aún pendientes. No inventar artículo, número de contrato, página ni hallazgo.

**Concordancia:** las observaciones relevantes de `Obras nacional` columna L son un resumen breve y deben concordar con el Word. El Word aporta la descripción, fuente, incidencia y acción, sin duplicar información irrelevante. Registrar observaciones y **continuar con otras obras/campos que no estén bloqueados**.

## Evidencia auxiliar: PDF escaneados con resaltado nativo

Para cada documento PDF del que se extraigan datos, el evaluador solicita, cuando corresponda, una **copia auxiliar con los fragmentos fuente resaltados en amarillo mediante anotaciones PDF nativas `Highlight`**. **Asumir que casi el 100 % de los originales son escaneos imagen sin texto reconocible**. El agente localiza visualmente el dato y ubica sus `Quads` en coordenadas de página; no usar rectángulos/autoformas superpuestos ni aplanar la anotación. Cada marca remite a una obra/campo/archivo/página. Conservar PDF original y cualquier corrección posterior del evaluador.

La **edición manual de la posición** en Acrobat/Edge requiere validación: el resaltado nativo puede no permitir arrastre libre; en ese caso, borrar y reaplicar el marcado. La prueba de creación de `Highlight` sobre página solo imagen ya fue positiva; la exactitud de escaneos reales sigue por comprobar. Véase [procedimiento de resaltado](../procedimientos/resaltado-evidencias-pdf-cmc.md).

**No cambian los dos entregables principales:** Excel MPR + Word de observaciones. Estos PDF resaltados son respaldo visual auxiliar.

## Registros de trabajo que NO se entregan por defecto

Se permite usar internamente, en almacenamiento **privado del expediente**, JSON/CSV, inventario documental, fichas por campo, registros de páginas, trazabilidad, bitácora y comprobación decimal. Sirven para reanudación, auditabilidad y aprendizaje, **no constituyen archivos adicionales que el evaluador deba recibir ni formatos institucionales independientes**. El repositorio público nunca contiene originales, transcripciones ni datos personales de expedientes.

Si el evaluador solicita explícitamente un archivo de control adicional, se entrega como anexo excepcional, identificado como auxiliar. La inexistencia de un archivo JSON no excusa la falta de trazabilidad.

## Entrega incremental y cierre

- Por cada nueva remesa de contratos, actas, liquidaciones o documentación financiera: **actualizar acumulativamente el mismo expediente**, con una copia revisada del Excel y versión actualizada del Word; no borrar lo previamente sustentado ni duplicar obras.
- Cada ronda: devolver **solo los dos archivos visibles**, indicando resumen de nuevas obras/campos, observaciones y pendientes. Si una herramienta o acceso impide editar uno, informar con precisión qué queda sin hacer y ofrecer únicamente resultados realmente creados.
- Al finalizar: verificar correspondencia Excel/Word, referencias PDF, integridad, cálculo/participaciones/factores y ausencia de errores estructurales; estados `completo_para_revision`, `parcial_con_pendientes` o `bloqueado`.
- Ningún entregable equivale a aprobación administrativa, firma, otorgamiento de CMC ni verificación de autenticidad.
- Publicar en Drive solo cuando exista destino autorizado y el conector confirme la escritura; de lo contrario entregar enlaces del chat a archivos efectivamente generados.

Aplican [control de evidencias](control-evidencias.md), [integridad documental](../procedimientos/control-integridad-documental.md), [biblioteca de casuística](../casuistica/README.md) y [procedimiento CMC](../procedimientos/aumento-cmc.md).
