# Control transversal — integridad visual del documento

**Origen del criterio:** aprendizaje comunicado por el titular durante su capacitación OECE el **05/11/2026**. Es un **criterio operativo de revisión**, no una cita normativa verificada ni una causal legal de rechazo por sí mismo. Aplica tanto a **aumento de CMC** como a **ampliación de categoría de consultores**. Su fundamento jurídico y su eventual forma institucional de subsanación se comprobarán cuando se aporte la referencia correspondiente.

## Regla principal

**Un documento debe examinarse como unidad documental completa.** El agente genera una **observación de integridad documental** cuando comprueba que faltan páginas, secciones, cláusulas o partes de párrafos, o cuando encuentra **indicios concretos** de ello que requieren cotejo. **La observación se registra incluso si todas las páginas conservadas contienen la información sustantiva necesaria para evaluar el trámite.** La suficiencia de datos para el cálculo o análisis **no elimina** la falta de integridad visual o material.

No basta leer únicamente las páginas que contienen montos, fechas, firmas, objetos o experiencia. **Revisar el documento completo en orden**, dentro de las posibilidades de acceso y legibilidad del cliente.

## Secuencia de revisión visual por documento

1. **Apertura y cobertura:** abrir el PDF, sus imágenes o vistas completas; identificar número de páginas legibles, primera/última página, orden, continuidad de páginas y calidad de lectura. Si no pudo acceder a todas, marcar `no_verificable` y explicar qué rango faltó revisar.
2. **Continuidad interna:** comparar numeración impresa y foliación cuando existan, páginas consecutivas, encabezados/pies y relación entre el final de una página y el comienzo de la siguiente. Un salto **no es prueba automática** de ausencia de hojas; verificar numeraciones alternativas y anexos.
3. **Integridad del texto:** buscar cláusulas incompletas, saltos injustificados entre cláusulas o artículos, párrafos que comienzan o terminan abruptamente, frases truncadas al cambiar de página, márgenes cortados y texto ilegible.
4. **Integridad estructural:** verificar si existe cierre material del documento, anexos mencionados que debían acompañarlo, continuidad de artículos, considerandos y parte resolutiva en resoluciones, así como referencias de contratos o constancias. Una firma ausente o una cláusula de numeración atípica no demuestra automáticamente que falten hojas.
5. **Contraste y resultado:** decidir `completo_aparente`, `indicio_incompletitud`, `incompleto_confirmado` o `no_verificable`. `completo_aparente` es únicamente resultado de revisión visual, **no autenticidad ni certificación de integridad**.
6. **Observación:** registrar hallazgo específico, documento/enlace de Drive, páginas o secciones contiguas, prueba observable, gravedad o incertidumbre y acción propuesta (solicitar copia íntegra/cotejar con original). No inventar número de página ausente cuando la secuencia no lo demuestra.
7. **Separación:** registrar **por separado** (a) disponibilidad de datos para evaluación y (b) integridad documental. Aunque (a) sea suficiente, si (b) es `indicio_incompletitud` o `incompleto_confirmado`, mantener observación y **no declarar el documento íntegro**. En caso confirmado, **no cerrar favorablemente el requisito sustentado solo con ese documento** sin revisión del responsable; la consecuencia administrativa requiere sustento normativo.

## Ejemplos de indicadores (no presunciones absolutas)

| Documento | Hallazgo visual | Registro |
|---|---|---|
| Contrato | Tras cláusula quinta el PDF pasa directamente a cláusula octava; no se localizan las sexta y séptima en el expediente | `indicio_incompletitud` hasta descartar numeración errónea u hojas anexas |
| Contrato | Página termina con «El contratista se obliga a…» y la siguiente inicia otro artículo, sin continuación | `indicio_incompletitud` o `incompleto_confirmado` solo cuando el cotejo lo demuestre |
| Resolución | La parte resolutiva comienza en «Artículo 3» y no aparecen artículos anteriores en el archivo/carpeta | Observación por posible documento incompleto, con páginas y contexto |
| Resolución | Se observa corte físico/escaneado del texto en el margen | Observación por texto truncado, con imagen/página y fragmento |
| Cualquier PDF | Faltó descargar o abrir un segmento, o hay páginas ilegibles | `no_verificable`, no asegurar ni completitud ni ausencia real |
| Cualquier PDF | OCR omite texto, pero en vista visual las páginas son continuas e íntegras | Problema de **extracción/OCR**, no registrar como hoja faltante |

## Campos sugeridos de una observación

```json
{
  "codigo": "INT-DOC-001",
  "tipo": "integridad_documental",
  "documento": "<nombre real>",
  "enlace_drive": "<enlace real verificado o null>",
  "estado_integridad": "indicio_incompletitud",
  "ubicacion": "páginas o secciones visibles verificadas",
  "hecho_observado": "detalle específico visto por el agente",
  "informacion_sustantiva_disponible": true,
  "accion_propuesta": "cotejar original o solicitar copia íntegra",
  "consecuencia_administrativa": "pendiente_de_sustento",
  "origen_criterio": "capacitacion_titular_2026-11-05"
}
```

Los marcadores entre ángulos son **placeholders** y no se deben copiar a expedientes como evidencia. `informacion_sustantiva_disponible = true` **no** elimina la observación.

## Dónde registrar la observación

- **CMC:** incluir observación textual con código `INT-DOC-###` en la ficha maestra (`observaciones`) y en el **entregable 1** junto a la obra/documento. Reflejarla como **pendiente de integridad** en los entregables 2 y 3 cuando afecte el sustento utilizado. No romper las seis claves existentes de `ficha-maestra.json` ni inventar campos obligatorios nuevos en el esquema del motor legacy.
- **Consultores:** incorporar una sección **«Observaciones de integridad documental»** en `informe.docx` y enlazar los hallazgos en `matriz.csv`/`matriz.json` (campo `observaciones` del control afectado), sin inventar un identificador normativo AC nuevo. Requisito no sustentado de forma íntegra: `pendiente` para revisión.
- **Coordinador:** cotejar que la observación **no haya desaparecido** de los archivos finales por tener datos aparentemente suficientes.

## Casos de aceptación del agente

1. Contrato tiene montos, fecha y objeto necesarios, **pero falta cláusula/párrafo/página** → **observación obligatoria** y estado diferenciado; no borrarla al calcular.
2. Resolución contiene la decisión y fecha, **pero está truncada** → **observación obligatoria**, aunque esos datos sean legibles.
3. PDF carece de una hoja **según evidencia visible** → observación, con localizador; si solo se sospecha, indicar **indicio** en vez de afirmar ausencia confirmada.
4. PDF parece completo después de revisión real → `completo_aparente`; no certificar autenticidad.
5. No se puede ver todas las páginas → `no_verificable`, con alcance exacto de la limitación.
