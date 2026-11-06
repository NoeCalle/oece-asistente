# Biblioteca de casuística del OECE Assistant — CMC

**Propósito:** que el especialista reconozca los documentos que suelen adjuntarse a expedientes de aumento de CMC, sepa **qué estructuras buscar**, qué dato extraer, en qué etapa se usa y cómo actuar ante variantes o contradicciones. No es una nueva norma ni entrenamiento de los pesos del modelo; es **memoria documental versionada que el agente consulta en cada expediente**.

## Contenido

- [Catálogo JSON de tipos de documentos](tipos-documentales-cmc.v1.json) — identificadores estables, títulos alternativos, estructura típica, campos candidatos, unidad de análisis, señales de reconocimiento y controles. Orientado al análisis automatizado.
- [Casuística y lecciones del piloto](patrones-y-lecciones-cmc.md) — casos observados, soluciones operativas confirmadas, hipótesis, excepciones y pendientes de afinación.

## Algoritmo del agente al recibir cada archivo

1. **Inventariar el archivo:** nombre real, identificador/URL de origen, páginas PDF, huella si es posible, fecha de recepción y expediente al que pertenece; no inferir contenido por nombre únicamente.
2. **Detectar piezas internas:** un PDF puede contener varios documentos, varias obras o páginas de firmas/anexos; y una obra puede estar repartida entre muchos PDF. Marcar rangos **por pieza** y asociar cada una a expediente general u obra (`OB-##`), sin duplicarla.
3. **Reconocer el tipo:** comparar contenido/cabecera/autoridad/parte resolutiva/firmas con el catálogo, y registrar `tipo_documental`, `certeza`, `subtipo` y `documento_id`. Un título puede estar mal redactado o repetido.
4. **Extraer por función probatoria:** cada campo tiene el PDF y página física 1-based de origen. No llenar recepción desde un contrato ni liquidación desde una promesa de consorcio. En `Obras nacional`, G = página del **PDF citado**; mantener además el archivo/ID en el registro del expediente. En J va el dato; en L la discrepancia o nota.
5. **Aplicar precedencia solo donde se haya decidido:** preferir el **contrato para el nombre del contratista** si también consta en recepción. Para otros campos la prioridad sigue pendiente de afinación. Si hay valores distintos, guardar ambos, indicar origen y marcar observación sin ocultarlos.
6. **Continuar progresivamente:** si solo llegó un contrato, llenar campos contractuales. Cuando llegue la recepción o resolución, actualizar **la misma obra** y conservar el registro previo y versiones del Excel. No detener todo por observaciones parciales.
7. **Cerrar la iteración con aprendizaje:** registrar patrón observado y evidencia en el expediente privado; clasificarlo como `candidato`, `verificado_en_caso` o `criterio_adoptado` y, si es generalizable y no contiene información privada, proponer añadirlo al catálogo/guía versionados en GitHub. Nunca promover automáticamente una coincidencia a obligación legal.
8. **Separar datos:** GitHub público almacena solo este **conocimiento general y anonimizado**. PDF originales, nombres personales, RUC, montos por proveedor, transcripciones, imágenes y la matriz de evidencias de cada caso permanecen en el Drive/carpeta privada autorizada.

## Estado y semántica

- `criterio_adoptado`: instrucción operativa expresamente comunicada por el titular. No equivale a fuente normativa.
- `verificado_en_caso`: se observó en un expediente concreto; no se universaliza.
- `candidato`: patrón o hipótesis sugerida que debe cotejarse.
- `pendiente_afinacion`: preferencia documental aún no decidida.
- `normativo`: solo cuando está sustentado por norma vigente identificada y artículo/página comprobados. Esta biblioteca **no atribuye por sí sola** ese estado.

## Casuística acumulativa

Para cada nueva obra o expediente se puede añadir a la memoria privada un registro con esta forma (valores de ejemplo, **no datos reales**):

```json
{
  "expediente_id": "CASO-EJEMPLO",
  "obra_id": "OB-01",
  "archivo_id": "PDF-A",
  "pagina_pdf": 7,
  "tipo_documental": "contrato_obra",
  "campo": "nombre_contratista",
  "valor": null,
  "estado_lectura": "pendiente_cotejo",
  "estado_casuistica": "candidato",
  "observacion_id": null
}
```

**No construir un expediente real a partir de este ejemplo.** Consultar también [control de evidencias](../contratos/control-evidencias.md), [integridad documental](../procedimientos/control-integridad-documental.md) y [llenado progresivo Excel MPR](../procedimientos/llenado-excel-aumento-cmc.md).
