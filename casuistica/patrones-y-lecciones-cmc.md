# Casuística observada y pendientes de afinación — CMC

**Edición:** 2026-11-06 · **Fuentes de aprendizaje:** piloto documental de aumento de CMC trabajado con el titular. Se abstraen patrones **sin publicar contratos, proveedores, identificaciones, montos ni imágenes del expediente**. No son jurisprudencia ni reglas legales nuevas.

## Aprendizajes comprobados en la prueba

| Código | Situación observada | Qué debe hacer el agente | Estado |
|---|---|---|---|
| CAS-CMC-001 | Expediente contiene **hoja de ruta** que identifica el trámite y declara cantidad de folios, además de otros archivos | Registrar número/fecha/folio declarado; no asumir que folios = páginas de un solo PDF ni que estar presentado significa admisible | Verificado en caso |
| CAS-CMC-002 | Se adjunta **comprobante de pago** separado de documentos de obra | Registrar monto, concepto, fecha y operación como documento administrativo; no sumarlo a experiencia de obra | Verificado en caso |
| CAS-CMC-003 | **Contrato** y **acta de recepción** repiten nombre del contratista | Elegir **contrato** para ese campo y citar su PDF/página; conservar fuente secundaria si es útil | **Criterio adoptado por titular** |
| CAS-CMC-004 | Un contrato o resolución tiene referencias a **obra, contrato o CUI diferentes** entre encabezado, cuerpo o acta | Registrar los literales de cada pieza y páginas, observar la discrepancia, seguir con campos/obras independientes; no asumir que documentos distintos corresponden al mismo contrato | Verificado en caso |
| CAS-CMC-005 | Contrato, entrega de terreno y acta de inicio muestran **cronología aparente imposible o contradictoria** | Separar fecha de suscripción, entrega e inicio; observar y cotejar originales antes de concluir | Verificado en caso |
| CAS-CMC-006 | Resolución presenta un **importe en antecedentes**, otro en el **artículo aprobatorio** y/o otro en el **cuadro económico** | Distinguir concepto por concepto y fuente/página; hacer conciliación aritmética como análisis, no reemplazar importes por suposición | Verificado en caso |
| CAS-CMC-007 | Hay **deductivo de obra** y/o reajuste, además de monto final referido en la resolución | Diferenciar reducción por partidas de obra de exclusión de equipamiento/mobiliario; no sumar dos veces adicionales/metrados ni asumir que monto final equivale al monto neto admisible | Verificado en caso |
| CAS-CMC-008 | Algunas páginas digitalizadas tienen **OCR escaso** o contienen mayormente firmas | Ir a imagen para comprobar el contenido; no considerar el OCR corto prueba de hoja faltante | Verificado en caso |
| CAS-CMC-009 | Un PDF contiene **varias obras** o una obra aparece en **varios PDF** | Identificar documentos por rangos y obra por ID estable; permitir nuevas entregas y no duplicar obra al recibir acta o liquidación | Criterio de trabajo adoptado |
| CAS-CMC-010 | El campo **«inicial pág»** del Excel puede citar páginas distintas si el dato está repetido en varias piezas | Registrar página física del PDF elegido y también ID/nombre del PDF; aplicar preferencias por campo conforme se vayan confirmando | **Pendiente de afinación** |
| CAS-CMC-011 | La plantilla puede contener **encabezados combinados** para nombre de obra y formularios con fórmulas | Escribir texto en celda ancla sin descombinar; comprobar fórmulas/compatibilidad con Excel del usuario antes de dar archivo por válido | Criterio de trabajo adoptado |

## CAS-CMC-012 — Carpeta INICIAL con contratos numerados, hoja de ruta y pago separados

**Registro: 06/11/2026 · Origen: captura de la lista de archivos de Drive y explicación directa del evaluador. Estado: patrón visual observado + interpretación de nombres confirmada por el titular, pendiente cotejo del contenido de cada PDF.** Se registra únicamente la estructura anonimizada; no se suben PDFs, capturas originales ni identificadores reales del trámite al repositorio.

**Estructura observada:** carpeta de expediente de aumento CMC con subcarpeta `AUM/INICIAL`. Dentro, **13 archivos PDF separados**, numerados `01_` a `13_`, cuyos nombres incluyen `CONTRATO` y una referencia descriptiva de obra; también aparece **un PDF administrativo cuyo nombre comienza por el año y código del trámite** (patrón `2026-…-LIMA.pdf` en esta muestra), y **un PDF con nombre `R` seguido de números** (patrón `R#####.pdf`).

**Significado informado por el evaluador:**
- `01_CONTRATO...pdf`, `02_CONTRATO...pdf`, etc. → **candidatos a documentos contractuales de obras diferentes**. No asumir que son 13 obras admisibles ni que un contrato incluye recepción o liquidación.
- `2026-…-LIMA.pdf` → **hoja de ruta** del trámite; identificar expediente y datos de presentación al abrir.
- `R#####.pdf` → **comprobante o constancia de pago del derecho de trámite**; verificar concepto, operación, fecha e importe en el documento.

**Reglas para inventario automatizado:** (1) reconocer la agrupación `AUM/INICIAL` cuando exista, sin volverla ruta obligatoria universal; (2) registrar **cada PDF por separado**, con su nombre/ID y clasificación `candidato_por_nombre`; (3) ordenar contratos por prefijo numérico pero **confirmar la relación obra↔contrato leyendo el PDF** antes de asignar `OB-##`; (4) clasificar hoja de ruta y pago como piezas del **expediente general**, no experiencias de obra; (5) permitir varias piezas dentro de un mismo PDF o varias piezas de una obra repartidas en PDFs; (6) no deducir ausencia de actas/resoluciones solo porque no se ven con ese nombre: podrían figurar como anexos internos. Registrar `documentos_pendientes_de_verificar` cuando corresponda.

**Impacto en los dos entregables:** los datos contractuales que se acrediten alimentan progresivamente el **Excel MPR**; diferencias, faltantes y asuntos verificables se resumen en el **Word de observaciones**. Los nombres de archivo sirven para orientar la lectura, **nunca como evidencia suficiente del contenido**. No extraer montos, fechas ni afirmaciones de suficiencia del simple listado.

**Aprendizaje para próximas muestras:** verificar si otros expedientes repiten los prefijos `R` y `20XX-...`, y registrar excepciones cuando un archivo con prefijo coincidente tenga otra naturaleza. Estas convenciones son heurísticas locales, no reglas institucionales universales.

## CAS-CMC-013 — Resaltador nativo amarillo sobre PDF escaneado

**Origen:** solicitud/corrección del evaluador el 06/11/2026. **Estado:** criterio operativo adoptado; prueba sintética de anotación `Highlight` superada, prueba de precisión y edición en Acrobat/Edge sobre documento real pendiente.

**Cambio de enfoque:** el evaluador aclaró que **no quiere autoformas ni rectángulos** sino las marcas equivalentes al **resaltador nativo de Acrobat o Microsoft Edge**, y que **prácticamente el 100 % de los expedientes serán PDF escaneados sin texto seleccionable**. El asistente debe reconocer visualmente cada dato y ubicar anotaciones PDF **`Highlight` / `QuadPoints`** amarillas directamente sobre la imagen, en una **copia** del original. No depender de capa de texto/OCR ni convertir el resaltado a un dibujo aplanado.

**Nota de usabilidad:** los resaltados nativos sobre escaneos pueden no permitir ser movidos libremente por arrastre en todos los visores; la corrección manual puede exigir **eliminar y volver a resaltar**, por lo que el agente debe maximizar la precisión inicial y reabrir/renderizar cada página anotada. Trazabilidad `obra→PDF→página→campo Excel→anotación`. PDF marcado = evidencia auxiliar; Excel MPR y Word siguen siendo entregables principales. Procedimiento: [POE-CMC-PDF-01 v2.0](../procedimientos/resaltado-evidencias-pdf-cmc.md).

## CAS-CMC-014 — Comentarios de resaltado breves con autor Noe Calle

**Criterio adoptado por el titular (06/11/2026):** todas las anotaciones `Highlight` llevan autor `Noe Calle` y su comentario visible contiene **únicamente el dato** como etiqueta y valor (por ejemplo `Monto contractual S/ 1 401 840.00`). No incluir `OECE Assistant`, `Dato extraído`, `Fuente`, número de página, avisos de cotejo ni prosa explicativa. La procedencia completa continúa disponible en el registro **privado** de trazabilidad, sin ocupar el comentario.

**Prueba:** se modificaron 20 anotaciones en la copia del PDF de 10 páginas; se verificó que las marcas seguían siendo tipo `Highlight` y sus geometrías y apariencias no cambiaron.

## CAS-CMC-015 — Un archivo de pago puede contener formulario y anexos de obras

**Fuente del aprendizaje:** revisión documental de una carpeta de aumento CMC en noviembre de 2026. **Estado:** estructura comprobada en caso; no regla universal. Un archivo cuyo nombre comienza por `R` y parece ser un comprobante de pago puede contener **también la solicitud de trámite, anexos con relación de obras y montos declarados** en las páginas posteriores. **Acción del agente:** abrir y clasificar **todas** sus páginas, no etiquetar el PDF entero como comprobante de pago por el nombre o la primera hoja. Conservar rangos de páginas por pieza y confrontar los importes declarados con contratos y liquidaciones auténticos. La relación de obras del solicitante es una **declaración**, no prueba definitiva de ejecución, recepción, participación o monto computable.

## CAS-CMC-016 — PDF llamado contrato con recepción, liquidación y constancia adentro

**Estado:** estructura comprobada en caso, pendiente de ampliar a nuevas muestras. Un archivo con nombre `CONTRATO` puede contener **contrato, acuerdo consorcial, acta de recepción, resolución de liquidación y constancia de prestación**, entre otros soportes, además de páginas de anexos. **Acción del agente:** elaborar mapa de tramos dentro de cada PDF; leer hojas relevantes y verificar integridad visual; asignar fuente/campo/página según la **pieza específica**, sin afirmar que faltan recepción o liquidación por no ver archivos independientes con esos nombres. Para denominación del contratista, mantener preferencia por contrato según regla ya adoptada.

## CAS-CMC-017 — Distinguir declaraciones de monto, componente obra y objeto de contrato

**Estado:** patrón comprobado en caso, criterios de computabilidad pendientes de cotejo normativo. Pueden coexistir un **monto contractual bruto**, un **monto de «solo componente de obra»** indicado en una constancia y un **monto declarado como final** en un formulario; no son automáticamente equivalentes. Una liquidación puede incorporar **reajustes** que no consten en el cuadro declarativo del solicitante. Y la **descripción de obra en la solicitud** puede no coincidir con el contrato adjunto bajo el mismo orden de relación. **Acción del agente:** preservar los literales y cifras por concepto, comparar páginas exactas, registrar cada inconsistencia o conciliación respaldada en el Word y reservar la obra/campo afectado sin detener las demás. No atribuir diferencias automáticamente a equipamiento, mobiliario ni irregularidad; no otorgar CMC por inferencia.

## CAS-CMC-018 — Mobiliario/equipamiento segregado en presupuesto de infraestructura

**Estado: verificado en expediente real, interpretación normativa pendiente.** En el presupuesto integrante de un contrato de obra educativa puede existir un **capítulo independiente de implementación de mobiliario escolar y equipos**, junto a capítulos de infraestructura. El importe desagregado es un componente de **costo directo** y no coincide necesariamente con su participación en el precio **bruto** de contrato (que contiene gastos generales, utilidad e IGV).

**Aprendizaje:** al identificar capítulos de mobiliario/equipamiento, extraer la descripción literal y su monto del documento anexo, separar el componente de infraestructura, cotejar la base del precio contractual y de liquidación, y verificar con norma aplicable la procedencia y método de exclusión **antes de descontar**. No restar directamente el costo directo del monto total con impuestos ni excluir cualquier elemento llamado «equipamiento» por su nombre sin clasificar su función. Mantener soporte de páginas y cálculo en expediente privado; en GitHub conservar solo este patrón abstracto.

## CAS-CMC-019 — Participaciones consorciales ocultas en anexos internos de cada PDF

**Estado: verificado en caso.** En algunos expedientes el porcentaje atribuible al solicitante figura dentro del **contrato de consorcio** agregado como anexo al PDF denominado «CONTRATO»; puede no aparecer en la portada o primera página del contrato de ejecución, y puede haber varios consorciados con porcentajes distintos.

**Aprendizaje:** buscar la sección/pieza consorcial a lo largo del PDF, atribuir el porcentaje **solo al integrante correcto** y documentar su página física en ese archivo. No inferir participación del título de archivo ni atribuir automáticamente a un mismo consorcio varias obras con nombres geográficos similares. Si el acuerdo separa obligaciones, revisar además la naturaleza de dichas obligaciones sin equiparar por defecto porcentaje económico y experiencia computable.

## CAS-CMC-020 — Reajustes incluidos en liquidación pero renunciados en otra pieza

**Estado: verificado en caso, tratamiento normativo pendiente.** El cuadro de liquidación puede mostrar un importe total que incorpora reajustes mientras que un documento del expediente menciona **renuncia a su cobro**. No son sinónimos `reajuste reconocido`, `reajuste pagado`, `reajuste renunciado` ni `monto de obra computable`.

**Aprendizaje:** extraer **por separado** importe original, reajuste, impuestos, monto de liquidación, texto de renuncia y su página/documento, identificar si la renuncia afecta el cobro o el monto técnico, y no sumar ni excluir automáticamente los reajustes en CMC sin fundamento. Cuando el método no esté definido, mantener como `pendiente_cotejo_normativo`, sin paralizar otras obras.

## Ficha de captura de una nueva casuística

Cada nueva situación se registra como **observación verificable**, no como generalización automática:

- **Identificador y título:** `CAS-CMC-NNN`, nombre breve.
- **Disparador:** texto, sección o relación entre documentos que activa el reconocimiento.
- **Variantes observadas:** nombre alternativo, diferente orden, sin folios, varios adjuntos, documento de consorcio separado.
- **Evidencia privada:** expediente/obra, PDF/ID, páginas exactas (no subir al repositorio público).
- **Riesgo:** solo del campo, de la obra o transversal.
- **Acción operativa:** qué extraer, qué cotejar y qué se puede seguir procesando.
- **Clasificación:** `candidato`, `verificado_en_caso`, `criterio_adoptado`; `normativo` requiere además norma y artículo verificables.
- **Fecha, versión y responsable de afinación** cuando se acuerde una regla estable.

## Matriz de precedencia por campo — en evolución

| Campo | Documento preferente | Alternativas | Estado |
|---|---|---|---|
| Nombre del contratista | **Contrato de obra** | Acta de recepción | **Adoptado** |
| Nombre exacto de la obra | Por definir | Contrato, acta de recepción, resolución | Pendiente |
| Monto contractual original | Por definir | Contrato, adendas y resoluciones | Pendiente |
| Porcentaje de consorcio | Por definir | Contrato/promesa formal/acuerdo de consorcio | Pendiente |
| Fecha de recepción | Por definir | Acta de recepción y otros documentos que la refieran | Pendiente |
| Importe de liquidación y monto neto | Por definir; distinguir conceptos | Resolución y cuadro económico | Pendiente |
| Adicional, deductivo, reajuste | Por definir | Resoluciones y cuadros económicos | Pendiente |

**Importante:** la preferencia de una fuente no permite ocultar discrepancias. Si el dato es controvertido, el agente conserva las dos versiones con páginas y marca pendiente de cotejo. Nunca convierte automáticamente un patrón del piloto en motivo legal de rechazo.

## Método de mejora entre expedientes

Al cerrar cada ronda, revisar: (1) documento nuevo o variante no catalogada; (2) campos hallados y su fuente; (3) conflicto entre fuentes; (4) lección suficientemente generalizable; (5) actualización de esta guía/JSON **sin datos privados**; (6) si se aprueba una nueva precedencia, pasar de «pendiente» a «criterio adoptado». El catálogo puede actualizarse sin rehacer expedientes existentes; cada expediente conserva su versión de reglas y sus evidencias.

La **biblioteca de casuística** no aprende de forma autónoma fuera de las conversaciones: funciona como memoria persistente que un agente debe **leer y actualizar deliberadamente** cuando tenga acceso y autorización. La extracción técnica no acredita por sí sola autenticidad o suficiencia administrativa.
