# Contrato de salida — ampliación de categoría de consultores

**Guía de contenido y requisitos:** [docs/CONTRATO_EXPEDIENTE.md](../docs/CONTRATO_EXPEDIENTE.md), [docs/normativa/REQUISITOS_AMPLIACIONES.md](../docs/normativa/REQUISITOS_AMPLIACIONES.md), [docs/CONTRATO_PROCEDIMIENTOS.md](../docs/CONTRATO_PROCEDIMIENTOS.md) y [contrato de evidencias](control-evidencias.md).

## Archivos de salida

1. **`informe.docx`** — Word editable con descripción, análisis documental, controles, observaciones, limitaciones y conclusión **provisional para revisión**.
2. **`matriz.csv` y `matriz.json`** — controles AC evaluados individualmente, mismos IDs y resultados, con enlaces reales por evidencia.
3. **`entrega.json`** — ID, origen en Drive, procedimiento `ampliacion_consultores`, revisión, fecha, archivos, fuentes, pendientes y estado de publicación.

Si la IA no dispone de generación de Word/CSV, **no afirmar producción**: entregar un documento editable completo en el formato que sí permita y marcar `docx_no_generado` o `no_publicado` cuando corresponda.

## Estructura mínima del informe Word

- Portada: expediente/solicitante, trámite, categoría solicitada, fecha de análisis y leyenda **borrador para revisión**.
- Objetivo y alcance de revisión; documentos realmente consultados del expediente.
- Marco normativo **leído** en Biblioteca Drive (identificar documento, artículo, fecha, página y vínculo), y citas de internet separadas con su aviso previo.
- Antecedentes RNP, categoría solicitada, régimen temporal/condiciones y datos de representación cuando correspondan.
- **Análisis de cada experiencia:** ID, contrato de consultoría, objeto, origen, culminación/conformidad, período, honorarios, comprobantes, consorcio, vínculos documentales y observaciones.
- **Controles AC:** evaluación individual con resultado motivado (cumple/no_cumple/pendiente/no_aplica). No inferir todo el cumplimiento a partir de una constancia.
- **Observaciones de integridad del escaneo:** documentar `INT-DOC-###` ante **folios ausentes** (p. ej. `2/5 → 4/5` sin `3/5`), párrafos **interrumpidos entre páginas con indicios objetivos de corte** o pérdida material por recorte, indicando folios físicos/impresos, vínculo, evidencia y grado de certeza. **La observación persiste aunque los datos útiles estén completos.** No tratar errores tipográficos, redacción deficiente, numeración de cláusulas o cambio de tema, por sí solos, como hoja no escaneada. Ver [procedimiento](../procedimientos/control-integridad-documental.md).
- Contradicciones y documentos faltantes; hechos que requieran validación profesional.
- Conclusión documental **no vinculante**, estado `completo_para_revision`, `parcial_con_pendientes` o `bloqueado`; sin otorgamiento de categoría.

## Columnas mínimas de matriz

`id_control`, `requisito`, `condicion_aplicabilidad`, `resultado`, `fundamento`, `norma_documento`, `norma_ubicacion`, `enlace_norma`, `expediente_documento`, `expediente_pagina`, `enlace_expediente`, `observaciones`.

- `resultado` solo: `cumple`, `no_cumple`, `pendiente`, `no_aplica`; este último siempre motivado.
- Si faltan documentos, el control pertinente es `pendiente`, no `cumple` ni `no_aplica` por defecto.
- Relacionar cada fila de la matriz con la sección y evidencia de informe. Informe y matriz no pueden contradecirse sin observación.
- Los importes monetarios de consultoría no son presupuestos de obras; factores CMC de ejecutores están prohibidos aquí.
- Cada consulta a sistemas externos se consigna como efectuada **solo con evidencia de ejecución**.

## Comprobación de publicación

Antes de afirmar entrega Drive, comprobar existencia/enlace de **cada** archivo; no confiar en persistencia del contenedor cloud. Si no se pudo subir alguno, enumerarlo claramente en `entrega.json` o en la respuesta al titular. Datos reales del expediente no se publican en GitHub.
