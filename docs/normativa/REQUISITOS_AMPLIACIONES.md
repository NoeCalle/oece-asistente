# Plan documental de ampliación y aumento CMC

Versión 1.5, 01/11/2026. Se segmentan **24 requisitos expresos**: diez de ampliación de consultores y catorce de aumento CMC. Se registran también diez alertas de exclusión de experiencia. El coordinador obtiene una lista por expediente y por experiencia, con cita literal, disposición, página, URL y hash del original.

El plan organiza la lectura; **no acredita que un documento exista, que su contenido satisfaga el requisito ni que la norma sea aplicable al caso**. Sus tareas quedan pendientes de interpretación. La matriz de evaluación mantiene sus controles y hechos citados; el plan no cambia automáticamente sus resultados.

## Fuentes y cobertura

- TUPA modificado por RPE D000073-2026-OECE-PRE: PA42003A92, página 31; PA42009D33, página 28. El [acto publicado](https://busquedas.elperuano.pe/dispositivo/NL/2503213-1) fue consultado nuevamente; no acredita una cadena exhaustiva de cambios.
- [Reglamento oficial consolidado](https://cdn.www.gob.pe/uploads/document/file/7594705/6444155-reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf?v=1787002595): 381.4, página 210; 381.5, páginas 210–212. Se enlaza la disposición de respaldo de cada requisito.
- [Directiva RNP](https://cdn.www.gob.pe/uploads/document/file/7946960/6682380-directiva-de-procedimientos-y-tramites-ante-el-registro-nacional-de-proveedores.pdf?v=1745192527): 9.2.9, páginas 11–12; remisiones 9.3.1–9.3.3, página 12. Se conservan las diez alertas separadas de la lista documental.

[Registro estructurado](../../rules/requisitos-ampliaciones.v1.5.json). El verificador comprueba tres originales, 59 referencias y 34 citas literales completas. Las citas provienen del TUPA y la directiva; el reglamento aporta referencias complementarias por disposición/página. La coincidencia literal prueba procedencia, no equivalencia jurídica ni vigencia.

## Listas alternativas por experiencia

| Procedimiento y rama | Documentos del requisito 3 |
|---|---|
| Consultor, Perú bajo Ley | Constancia u otro documento de la entidad con los datos exigidos; atender condición de categoría (a) y objeto |
| Consultor, Perú fuera de Ley | Contrato; documento del contratante; aprobación/viabilidad/conformidad según corresponda; descripción de obra y actividades; comprobantes equivalentes al monto final |
| Consultor, extranjero | Contrato; documento de conformidad o viabilidad y datos del contratante según corresponda |
| Ejecutor, Perú bajo Ley, contrato directo | Constancia u otro documento de la entidad con los datos exigidos |
| Ejecutor, Perú fuera de Ley | Contrato; documento del contratante; conformidad de obra; facturas o boletas equivalentes al monto final |
| Ejecutor, extranjero | Contrato; documento del contratante con datos y montos del componente obra |
| Ejecutor, subcontrato bajo Ley | Contrato principal o referencia admitida; autorización de la entidad; subcontrato; documento del contratista principal; facturas equivalentes al monto final |

A todas las ramas se agregan solicitud mediante formulario y número/fecha de pago, sin inventar una obligación universal de adjuntar un comprobante. Los datos exigidos de cada documento se conservan en la cita completa, incluyendo las condiciones de consorcio. Una fila no significa que baste el título del documento.

Para el contrato principal del subcontrato se conservan dos vías alternativas: copia, o número del contrato/nomenclatura/entidad en la solicitud cuando efectivamente se encuentre registrado en la plataforma. No se exigen ambas vías ni se da por comprobado el registro solo porque se haya escrito su número.

Procedencia desconocida conserva alternativas. En aumento CMC bajo Ley, `subcontrato=null` no equivale a contrato directo: se pregunta antes de seleccionar 3.1.i o 3.3. Los subcontratos extranjeros/privados y los invocados por consultores conservan una incidencia para delimitar régimen y exclusiones; no se extiende automáticamente la lista de obras públicas peruanas.

## Exclusiones y condiciones abiertas

Las diez alertas de 9.2.9 incluyen, entre otros supuestos, contratación sin condiciones registrales/capacidad exigibles, servicios generales, supervisión temporal, ciertos subcontratos, contratos marco en ejecución, partidas/componentes, ausencia de rol integral y autoconstrucción. Se devuelve cada literal íntegro para interpretar su alcance. No se convierten en diez documentos adicionales ni en hechos negativos probados por ausencia de una palabra.

La reorganización societaria requiere el artículo 25.7 modificado y sus excepciones: se mantiene J05 y no se introduce el rechazo del texto anterior. La condición de categoría (a), las especialidades, el objeto de la consultoría, autoridad competente y transición J01 permanecen expresamente por delimitar. Las condiciones generales del artículo 25, solvencia y documentos extranjeros siguen su análisis propio.

## Operación y conservación

```text
python -m oece requisitos RUTA_EXPEDIENTE
python scripts/construir_requisitos.py
```

Por MCP: `oece_requisitos` con el ID del caso; el catálogo actual tiene trece herramientas. La CLI y el servidor verifican las fuentes antes de devolver el plan. La generación conserva el plan en `matriz.json` como `plan_documental`, y añade las huellas del registro y del índice TUPA a las dependencias de cada revisión. Si cambia el registro durante la preparación, se rechaza la mezcla de versiones.

Este apoyo detallado está en la matriz JSON y en la herramienta del coordinador; no se afirma que las 24 filas se evalúen automáticamente ni que se haya añadido un anexo de checklist al Word/CSV. El análisis y sus referencias conservan el contrato de hechos/documentos/normas adicionales existente. Las nuevas filas no reciben aceptación humana ficticia.

No se incorporan listas de inscripción, actualización ni reconsideración en este registro. Fuera del corte 31/10/2026 se pide actualización de fuentes. Tampoco dentro del corte se certifica automáticamente vigencia. [Estado](../ESTADO.md), [verificación](../VERIFICACION_V15.md).
