# Control transversal — integridad del escaneo y continuidad de páginas

**Criterio operativo de capacitación:** comunicado por el titular el **05/11/2026**, afinado con el ejemplo concreto de folios `2/5 → 4/5`. Aplica a CMC y consultores. **Su objeto es detectar documentos incompletamente escaneados o cargados**, no hacer una corrección gramatical, ortográfica o de estilo. No se presenta como causal legal de rechazo ni se le atribuye una norma sin cotejar.

## Regla principal

El agente debe **revisar visualmente todas las páginas del documento, en orden**, aunque las primeras hojas ya contengan los datos sustantivos necesarios.

**Se registra observación por integridad cuando hay evidencia visible de una página no escaneada, omitida, desordenada o un recorte material que impide recuperar parte del documento**, o un indicio concreto y explicable de esa omisión. La suficiencia de montos, fechas, objetos o firmas en las hojas presentes **no borra la observación**.

**No emitir observación de integridad por lo siguiente cuando no haya evidencia física de omisión:** `typos`, faltas de ortografía, errores de redacción, sintaxis o concordancia, un cambio de tema, una cláusula mal numerada, saltos de artículos, documentos redactados de modo extraño o un fallo del OCR. Puede haber errores de forma sin faltar ninguna hoja. Si hay un error sustantivo que afecta la interpretación, registrarlo **en un control diferente**, no como escaneo incompleto.

## Comprobaciones en orden

1. **Cobertura real:** contar páginas del PDF disponibles y examinar primera/última hoja. Leer las imágenes completas, no limitarse a extraer texto u OCR. Si la plataforma solo permite revisar parte del archivo, registrar `no_verificable` con páginas no vistas.
2. **Numeración visual:** identificar la numeración impresa —por ejemplo `1/5, 2/5, 3/5, 4/5, 5/5`— y confrontarla con las hojas presentes, su orden y el número físico de imágenes. **Ejemplo determinante:** si se ven `1/5, 2/5, 4/5, 5/5` y no existe ninguna hoja `3/5` en el documento ni adjuntos, existe evidencia fuerte de **una hoja ausente del escaneo**. Registrar las numeraciones tal como aparecen y la búsqueda de la hoja faltante. Comprobar antes si hay numeración por secciones, anexos separados, páginas duplicadas o errores de foliación.
3. **Continuidad de lectura entre páginas contiguas:** comparar el final de una hoja con el inicio de la siguiente. Si el párrafo empieza en una hoja y debe continuar pero la siguiente arranca con un texto que **no enlaza lógica, sintáctica o materialmente**, buscar simultáneamente un salto de foliación, corte visible, fragmento de oración pendiente, referencia a una hoja intermedia o parte de texto truncada. **Una falta de relación temática por sí sola NO demuestra una hoja faltante**: puede ser redacción deficiente o cambio legítimo de sección. Cuando solo exista discontinuidad sospechosa, consignar `indicio_incompletitud` **si hay una razón objetiva verificable**, nunca `incompleto_confirmado`.
4. **Recortes físicos del escaneo:** revisar márgenes y parte inferior/superior de hojas; texto o tablas cortadas por el borde pueden mostrar pérdida material de contenido **aunque no falte una página completa**. Registrar `recorte_material` como causa, especificando posición e imagen. No confundir con una frase mal escrita.
5. **Contraste:** inspeccionar otras hojas, anexos y versión del mismo documento si están en el expediente. Si la numeración es incorrecta pero todas las hojas y continuaciones están presentes, **no clasificar como hoja omitida**. Si el OCR omitió una línea pero la imagen completa sí la muestra, clasificar como defecto OCR, sin observación de integridad.
6. **Estado:** seleccionar `completo_aparente`, `indicio_incompletitud`, `incompleto_confirmado` o `no_verificable`. `completo_aparente` no significa autenticidad garantizada. No declarar `incompleto_confirmado` basándose solo en una interpretación semántica.
7. **Salida:** si hay indicio fundamentado o incompletitud confirmada, generar `INT-DOC-###` con **evidencia visual concreta**, números impresos/hojas físicas, enlace, detalle de la transición, condición observada y propuesta de solicitar/cotejar copia íntegra. Aunque estén los datos para evaluar, conservar la observación hasta revisión. Las consecuencias procedimentales o jurídicas quedan `pendiente_de_sustento`.

## Tabla de decisiones para evitar falsos positivos

| Situación observada | Clasificación y acción |
|---|---|
| Páginas impresas `1/5, 2/5, 4/5, 5/5`, sin `3/5` entre el PDF y sus anexos | `incompleto_confirmado` **si la secuencia es inequívoca**; observar omisión de folio `3/5`. Si aún falta verificar adjuntos o foliación, `indicio_incompletitud`. |
| Hoja `2/5` termina con una oración abierta; hoja `4/5` inicia otra idea y `3/5` no existe | **Observación obligatoria**, evidenciada por numeración y continuidad. |
| Hoja A termina en mitad de una frase, B comienza sin continuación, **sin** numeración verificable | `indicio_incompletitud` cuando hay un corte/continuación objetivamente interrumpida; solicitar cotejo, **sin afirmar qué página falta**. |
| Hoja A y B tratan asuntos distintos, pero numeración es continua y ningún texto se corta | Cambio de sección o redacción; **no** observación por hoja faltante. |
| El contrato dice «Cláusula 5», luego «Cláusula 8», pero foliación y contenido son continuos | Posible **error de numeración/redacción**, **no** afirmar página faltante. |
| Errores tipográficos, ortográficos, puntuación o frases mal redactadas sin pérdida visible | **No** emitir `INT-DOC`; considerar otro control solo si afectan sustantivamente el expediente. |
| Una parte de texto o tabla queda fuera del borde escaneado | `indicio_incompletitud` o `incompleto_confirmado` según evidencia visual; causa `recorte_material`. |
| Texto OCR no recupera palabras que **sí se ven** en la imagen del PDF | Defecto de extracción/OCR, **no** documento materialmente incompleto. |
| No fue posible ver las imágenes o todas las páginas | `no_verificable`: explicar limitación; no inventar hojas ausentes. |

## Datos de observación (ejemplo sintético, no evidencia real)

```json
{
  "codigo": "INT-DOC-001",
  "tipo": "integridad_documental",
  "causa": "folio_omitido_en_escaneo",
  "documento": "contrato-ejemplo.pdf",
  "enlace_drive": null,
  "estado_integridad": "incompleto_confirmado",
  "paginas_pdf_visibles": [1, 2, 3, 4],
  "numeracion_impresa_visible": ["1/5", "2/5", "4/5", "5/5"],
  "folio_ausente_indicado": "3/5",
  "evidencia_visual": "Tras la hoja impresa 2/5 se observa 4/5 y no aparece 3/5 en el archivo revisado",
  "continuidad_texto": "El párrafo al final de 2/5 no continúa al inicio de 4/5",
  "informacion_sustantiva_disponible": true,
  "accion_propuesta": "Solicitar copia completa o cotejar original",
  "consecuencia_administrativa": "pendiente_de_sustento"
}
```

**En expedientes reales, usar solo datos observados:** el ejemplo no indica que se haya leído un contrato auténtico. Diferenciar `paginas_pdf_visibles` (posición en archivo) de `numeracion_impresa_visible` (folio estampado en documento). Si el documento no tiene foliación impresa, dejarla `null`, no inventarla.

## Registro en entregables

- **CMC:** observación `INT-DOC-###` en `ficha-maestra.json.observaciones` y documento/obra del `entregable-01-datos.json`; transmitir como pendiente a 2 y 3 si afecta el sustento. No cambiar las seis claves del contrato histórico.
- **Consultores:** sección de integridad en `informe.docx` y referencia en el campo `observaciones` del control relevante de `matriz.csv`/`matriz.json`. No inventar códigos AC normativos.
- **Coordinador:** verificar que la observación sobreviva a la preparación de resultados incluso si los datos analíticos eran suficientes.

## Pruebas mínimas de aceptación

1. **Positivo:** `2/5 → 4/5` sin `3/5` y salto de continuación → observación `INT-DOC` aun si el monto y objeto están disponibles.
2. **Positivo con incertidumbre:** frase físicamente interrumpida entre hojas, sin folios impresos → observación de **indicio**, no falta confirmada.
3. **Negativo:** contrato completo con errores ortográficos, typos o frases poco claras → **no** observación de integridad.
4. **Negativo:** cláusulas 5 y 8 consecutivas por error de numeración, con hojas continuas → **no** declarar escaneo incompleto.
5. **Negativo:** párrafos sobre temas diferentes en hojas consecutivas con texto y folios continuos → **no** inferir omisión.
6. **Negativo:** OCR defectuoso pero PDF visual completo → **no** inferir hoja faltante.
7. **Bloqueado:** no se puede revisar el archivo entero → `no_verificable`.
