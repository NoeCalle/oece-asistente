# Pruebas de aceptación — arquitectura de agentes sin MCP

## Validación estática en GitHub

`tests/test_arquitectura_agentes.py` comprueba que existen las instrucciones, roles, contratos, rutas de referencia, separación de especialidades, Drive-first y avisos previos a internet. Esto **no** demuestra que una IA haya leído Drive, ejecutado un cálculo correcto o subido un Word.

## Prueba end-to-end A — pregunta normativa del titular

**Entrada:** «¿Qué establece el artículo X de un documento identificable en la carpeta normativa Drive?». Verificar que el cliente:
- Abre la carpeta real y el archivo, no inventa página.
- Cita `Biblioteca Drive` y no usa internet si hay evidencia suficiente.
- Si no hay sustento tras búsqueda efectiva, informa **antes** de abrir web, y la marca `Internet`.
- Si conector falla, informa fallo y no concluye «no existe».

**Aprobación:** enlaces y pasajes comprobables. Registrar proveedor, fecha, pregunta, evidencia y resultado de prueba.

## Prueba end-to-end B — CMC sintético

**Entrada:** carpeta privada Drive con dos obras ficticias: una elegible *según fuentes simuladas expresamente etiquetadas como sintéticas* y otra desistida. El ejercicio es de integridad de datos, **no de decisión legal**.
- Indicar `aumento_cmc` explícito.
- El coordinador activa CMC y no consultores.
- El agente lee documentos, no completa montos que falten ni incluye la obra desistida.
- Entrega `ficha-maestra.json`, `entregable-01-datos.json`, `entregable-02-datos.json`, `entregable-03-datos.json` en ese orden, con referencias y `CMC_a_otorgar=null`.
- Comprueba que 2 toma exactamente los IDs computables de 1 y 3 reconcilia totales; sin factores fundamentados, el cálculo queda pendiente.
- Guarda en Drive si el cliente puede; comprobar enlaces.

**Aprobación:** consistencia de referencias/cifras, no apariencia de formato oficial.

## Prueba end-to-end C — consultores sintético

**Entrada:** carpeta privada Drive con solicitud ficticia de ampliación de categoría, contrato de consultoría y documento de experiencia incompleto.
- Indicar `ampliacion_consultores` explícito.
- No aplicar `G=a+f+e` ni sumar presupuesto de obra como honorario.
- Matriz AC con controles sustentados, incluyendo `pendiente` cuando falta evidencia.
- Informe Word editable con mismo expediente, fuentes y revisión; si DOCX no se generó, reconocerlo.
- Guardar en Drive solo si ocurrió y comprobar enlaces.

**Aprobación:** Word/matriz consistentes, sin aprobación institucional.

## Prueba transversal D — páginas no escaneadas (no typos)

El control visual busca **hojas omitidas y recortes físicos**, no errores de ortografía ni de redacción. **Suficiencia de datos y continuidad del escaneo son controles independientes**. [Regla precisa](../procedimientos/control-integridad-documental.md).

| Caso sintético | Resultado esperado |
|---|---|
| Contrato paginado `1/5, 2/5, 4/5, 5/5`, sin `3/5` en el PDF ni anexos; contiene monto, fecha y objeto | **Observación obligatoria** `INT-DOC-###`, aunque esos datos basten para parte del trámite; registrar evidencia visual y folio `3/5` omitido; confirmar solo cuando la secuencia sea inequívoca |
| Hoja impresa `2/5` termina párrafo abierto y `4/5` no lo continúa, sin `3/5` | **Observación obligatoria**, con ambas evidencias independientes |
| Fin de una hoja con frase interrumpida; inicio de la siguiente no enlaza y no hay numeración visible | **Indicio justificado**, no afirmar automáticamente hoja ausente o número inventado |
| Resolución con páginas continuas y párrafos coherentes, pero ortografía o sintaxis deficientes | **No observación de integridad** por `typo` o redacción |
| Contrato salta de cláusula 5 a 8, pero hojas y texto son continuos | **No afirmar página omitida**: posible error de numeración de cláusulas |
| Dos páginas contiguas cambian de asunto, con foliación correcta y párrafos completos | **No** atribuir el cambio temático a pérdida de hoja |
| OCR omite un párrafo que sí está visible en imagen completa | **No** generar `INT-DOC`; marcar defecto de extracción si procede |
| Texto al borde queda fuera del escaneo, aunque todas las páginas estén presentes | Observación por `recorte_material`, no por hoja completa faltante |
| No es posible abrir todas las imágenes del PDF | `no_verificable`, sin afirmar una omisión |

**Verificación de entregables:** CMC mantiene el hallazgo en ficha maestra/entregable 1 y, cuando afecte su sustento, en 2 y 3. Consultores lo incluye en sección específica del informe y observaciones de matriz. En todos los casos el agente identifica **página física del PDF, numeración impresa, evidencia visual y grado de certeza**, sin equiparar una discontinuidad semántica aislada a falta confirmada. Pruebas de uso real en los tres clientes cloud aún pendientes.

## Prueba de portabilidad

Repetir A, B, C en **Codex Cloud, Claude Cloud y Grok Bot**, registrando por cada uno:
- Lectura de repo/instrucciones: `comprobada` / `falló`.
- Acceso real a carpeta normativa: `comprobado` / `falló`.
- Lectura de PDF del expediente: `comprobada` / `falló`.
- Creación Word/JSON/CSV: lista y ruta.
- Escritura efectiva de resultados Drive: enlaces o `no_publicado`.
- Capacidad de detectar una cifra/fecha inexistente y mantener `pendiente`.

**Estado inicial:** estas pruebas end-to-end **no se han ejecutado ni aprobado** en las tres nubes. No transformar la creación de prompts o pruebas estáticas en una certificación de disponibilidad cloud.
