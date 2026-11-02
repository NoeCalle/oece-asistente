# Consulta trazable de fichas TUPA

Versión 1.4, 01/11/2026. Índice de **quince fichas y cuarenta páginas**, del anexo de la RPE D000073-2026-OECE-PRE. Es recuperación de fuentes por rama: no reemplaza la interpretación ni verifica por sí misma cada requisito.

## Fuente y comprobación

El [acto publicado en El Peruano](https://busquedas.elperuano.pe/dispositivo/NL/2503213-1), consultado el 01/11, señala emisión 31/03/2026 y publicación 08/04/2026. Su artículo 1 modifica el TUPA aprobado por DS 086-2025-EF y actualizado por RGG D000002-2026-OECE-GG. El [Portal de Transparencia OECE](https://transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad=10&id_tema=5&ver=) lista estos tres antecedentes. Esto documenta esa relación, sin certificar ausencia de cambios posteriores.

El [anexo oficial](https://cdn.www.gob.pe/uploads/document/file/9763405/7983873-modificacion-del-tupa-del-oece.pdf) ya estaba conservado en el primer manifiesto; no es una descarga nueva. SHA-256: `d3ab3f6b87f7b5706177c8a7f6df8bd202a0f3878c686f23a5047d5264834b7e`. Se verificaron el original, los quince encabezados/códigos y la extracción de cada página. El acceso web al anexo devolvió 403 y la ficha gob.pe 418 en esta consulta; se distingue ese fallo de la integridad de la copia preservada.

Se inspeccionaron visualmente las páginas 31, 50, 51 y 66. No se declara revisión visual de las cuarenta páginas ni revisión humana. Los metadatos conservan `revision_humana=null` y `apta_para_reglas=false`. [Registro](../../normativa/indice-tupa.v0.1.json), [comprobación de fuentes](../../normativa/revision-tupa-2026-11-01.json).

## Fichas cubiertas

| Código | Rama | Páginas PDF |
|---|---|---|
| PA42009D33 | Aumento CMC | 28–30 |
| PA42003A92 | Ampliación de categorías | 31–33 |
| PA4200F589 | Bienes/servicios, natural extranjera no domiciliada, con representación según ficha | 34–35 |
| PA4200067C | Bienes/servicios, jurídica extranjera no domiciliada, con representación según ficha | 36–37 |
| PA42007D51 | Consultor natural nacional | 38–40 |
| PA42009762 | Consultor natural extranjero | 41–43 |
| PA42001C78 | Consultor jurídico nacional | 44–46 |
| PA4200ED2E | Consultor jurídico extranjero | 47–49 |
| PA42003A4F | Ejecutor natural nacional | 50–52 |
| PA4200C4F5 | Ejecutor natural extranjero | 53–55 |
| PA42000DF5 | Ejecutor jurídico nacional | 56–58 |
| PA42009BA2 | Ejecutor jurídico extranjero | 59–61 |
| PA4200EF4C | Bienes/servicios, jurídica nacional o extranjera domiciliada | 62–63 |
| PA42004846 | Bienes/servicios, natural nacional o extranjera domiciliada | 64–65 |
| PA42007484 | Bienes sofisticados/servicios especializados, extranjero no domiciliado sin representante en Perú | 66–67 |

## Uso por el coordinador

`oece_tupa` recibe el ID del caso y devuelve fichas candidatas, datos faltantes, páginas, fuente, huellas y alertas. Para leer una página, añadir `codigo` y opcionalmente `pagina`; por defecto lee la primera de esa ficha. El código debe pertenecer a las candidatas y la página a esa ficha. Se comprueban manifiesto, hash del PDF y hash del texto extraído antes de devolver contenido.

Con terminal:

```text
python -m oece tupa RUTA_EXPEDIENTE
python -m oece tupa RUTA_EXPEDIENTE --codigo PA42003A92 --pagina 31
python scripts/construir_indice_tupa.py
```

El último comando reconstruye el índice desde el original identificado; rechaza un cambio de archivo sin revisar el mapa. Las instrucciones son comunes para cualquier cliente con acceso al motor. En MCP hay ahora trece herramientas, incluida la consulta de requisitos incorporada en 1.5; no se añade una API de modelo.

## Límites que evita la selección

- Un dato ausente conserva alternativas y una pregunta; no convierte natural/jurídica o nacional/extranjera en un valor por defecto.
- Para bienes/servicios extranjeros no domiciliados, se muestran las fichas ordinaria y especial pertinentes. `actua_por_representante=false` no demuestra la falta de representante en Perú ni que se trate de bienes sofisticados/servicios especializados. Deben cotejarse esas condiciones y el responsable designado por la entidad.
- Inscripción y reinscripción comparten ficha, pero tienen ramas diferentes de experiencia. La consulta alerta si falta esa modalidad; no exige conjuntamente todos sus documentos.
- Actualización no recibe un código inventado de inscripción. Se consulta su directiva. Reconsideración requiere identificar el procedimiento del acto impugnado antes de recuperar su ficha y recursos.
- La página 31 describe categorías A/B/C/D. Ese párrafo descriptivo no resuelve la transición ni sustituye el artículo 27 y J01. Se conserva como alerta, sin introducir umbrales automáticos.
- En las páginas 50–51 un requisito continúa en la página siguiente. La extracción también puede ubicar la descripción después de requisitos. Por eso se entregan páginas completas con sus localizadores, sin afirmar una separación automática infalible por requisito.

## Fecha y continuación

Una solicitud anterior al 08/04/2026 requiere revisar una versión histórica. Posterior al 31/10/2026 requiere actualizar fuentes. Dentro de ese intervalo solo se informa que está dentro del corte documental: **la aplicabilidad jurídica sigue como no determinable**, porque la cadena por disposición no está cerrada. Publicación no se convierte automáticamente en eficacia, ni `hasta=null` en vigencia indefinida.

Quedan la segmentación artículo/numeral/literal, los intervalos y condiciones por disposición, la matriz completa de requisitos/excepciones y su cotejo con reglamento/directiva. Esta entrega cierra la recuperación técnica de estas quince fichas. No cierra T06/T08/T20 ni amplía la ventana de evaluación. [Estado](../ESTADO.md).
