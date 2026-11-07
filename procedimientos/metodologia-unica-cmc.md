# MET-CMC-01 — Metodología única y secuencial de aumento de CMC

**Versión:** 1.0 · **Vigencia operativa:** 2026-11-07 · **Aplica a:** todo expediente declarado `aumento_cmc`.
**Carácter:** procedimiento de trabajo interno, no fuente de derecho ni aprobación administrativa.
**Autoridad:** esta es la **secuencia canónica** para coordinador y especialista CMC; los documentos de integridad, Excel, resaltado y contrato de entregables detallan **cómo** ejecutar cada etapa, no autorizan cambiar el orden. **No se aplica a ampliación de categoría de consultores.**

## Principios que no se negocian

- **Un expediente, una revisión vigente.** Mantener una única carpeta de entrega actual y un historial separado; nunca dispersar por fases los PDF o los Word finales. No reemplazar originales.
- **Un PDF de experiencia de entrada → una copia PDF resaltada de salida.** Con `N` PDF fuente de contratos/experiencias, deben existir `N` copias individuales, correlativas y con el nombre de origen más `_RESALTADO.pdf`. `N` no implica `N` obras: un archivo puede contener varias piezas/obras y una obra puede tener varios archivos. Hoja de ruta/pago son documentos administrativos, no se cuentan en `N`.
- **Dos entregables principales:** (1) **libro Excel MPR** completo o progresivo, basado en la plantilla institucional vigente, y (2) **un solo Word editable con todas las observaciones consolidadas**. Los `N` PDF son **sustentos auxiliares obligatorios para esta forma de entrega**, no un tercer formato de evaluación; un ZIP puede añadirse como comodidad, pero no sustituye los archivos individuales.
- **Evidencia antes de conclusión:** todo hecho o importe lleva `PDF exacto + página física 1-based + pieza documental + literal + estado de cotejo`. Distinguir contrato, liquidación, reajuste, recepción y experiencia computable; no completar `null` con estimaciones.
- **Trabajo ordenado pero no rígidamente bloqueante:** si una obra/campo está observado, registrarlo y **continuar los trabajos independientes**. Se puede entregar un avance, pero jamás declararlo completo ni saltarse un control sin señalarlo.
- **Normativa de biblioteca Drive primero** y vigencia al corte del expediente. No afirmar requisitos, exclusiones o factores por intuición. Internet solo con aviso previo cuando la biblioteca es insuficiente; nunca reemplaza documentación del expediente.
- **Privacidad:** documentos reales, RUC, imágenes, montos de un proveedor, notas, transcripciones y controles privados permanecen únicamente en almacenamiento autorizado; **GitHub recibe código y lecciones desidentificadas**, nunca el expediente.

## Secuencia obligatoria y puertas de control

| Etapa | Trabajo en orden | Condición para marcarla completada |
|---|---|---|
| **0. Activar y reanudar** | Leer `AGENTS.md`, coordinador, especialista, este método y contrato. Confirmar trámite, carpeta fuente, permisos, carpeta de resultados y revisión vigente. **Inspeccionar avances antes de reanalizar.** | Acceso comprobado, expediente bien identificado y etapa más antigua pendiente determinada. |
| **1. Inventariar** | Enumerar **todos** los archivos; separar administrativos de `N` PDF de experiencia; registrar nombre, enlace/ID, versión/huella si existe y **cantidad real de páginas**. Mapear provisionalmente `OB-##` sin suponer `N = número de obras`. | Lista cerrada de `N` fuentes y folios; falta de acceso/duplicados expresamente señalada. |
| **2. Control visual de integridad** | Para **cada PDF y cada una de sus páginas físicas**, revisar imagen, orden, foliación impresa, continuidad entre páginas, márgenes/recortes, legibilidad y anexos. Aplicar `control-integridad-documental.md`. | Cobertura **total de páginas verificadas** o estado `no_verificable` con rangos faltantes. `N páginas = N páginas revisadas` no se presume por haber abierto el PDF. |
| **3. Extraer por documento y obra** | En orden de inventario, **terminar el mapa documental del PDF**: contrato, consorcio, recepción, adicionales/deductivos, liquidación, constancias y demás piezas, aunque estén mezcladas. Capturar campos con página precisa. Identificar documentos faltantes y contradicciones. | Cada PDF tiene registro completo de piezas/estado de lectura, datos fuente y pendientes; cada obra se vincula con documentos exactos sin duplicidad. |
| **4. Conciliar experiencias** | Contrastar por obra solicitud, contrato, consorcio, acta, resoluciones y liquidación. Separar importe contratado, importe liquidado, reajustes, deducciones, componentes no obra, participación y propuesta de valor neto. Mantener los dos literales discrepantes. | Por cada obra, estado `sustentado`, `pendiente_por_campo` o `excluido_con_sustento`; nunca clasificar «acreditado» por tener un PDF resaltado. |
| **5. Contrastar normativa** | Abrir norma **real** en biblioteca, comprobar fecha de versión y vigencia aplicable, norma/numeral/página, excepciones y pertinencia para **aumento** de CMC. Determinar tratamiento de controversias sin inventar reglas. | Cada decisión de admisibilidad, neto y factores tiene fuente normativa verificable; si falta, conservar decisión pendiente. |
| **6. Calcular y llenar MPR** | Construir relación de obras admisibles; determinar años, `a`, `f`, `e` y `G` solo con sustento; preparar valores en las pestañas reales del MPR y comprobar aritmética por método independiente. Preservar fórmulas, hojas y formatos. | Excel MPR **efectivamente generado, abierto y revisado**, o indicar claramente que existe **solo generador/datos preparados**, sin presentar eso como Excel terminado. |
| **7. Resaltar evidencias** | Actualizar las `N` copias **individuales** con `Highlight` nativo amarillo, autor `Noe Calle` y comentario breve del dato. Marcar los **campos usados** y resolver marcas desviadas. No alterar el PDF origen ni aplanar. | Correspondencia 1:1 por archivo; igual número de páginas que su fuente; revisión visual del alineamiento y tipo `Highlight`. Si un PDF aún carece de evidencias verificables o marcas requeridas, declararlo parcial, no completo. |
| **8. Consolidar Word y auditar cruce** | Mantener **un único Word vigente**: identificación, relación/estado de todas las obras, todas las observaciones comprobadas con página, alcance, impacto, acción propuesta y pendientes. Cotejar Word ↔ Excel ↔ PDFs ↔ fuentes y lista de cambios. | **Una sola versión actual del Word**, sin omitir hallazgos de rondas previas; datos y referencias congruentes, archivo editable y visualmente revisado. |
| **9. Publicar y cerrar** | Publicar en Drive autorizado; verificar existencia, **cantidad, nombres y versión**; mover revisiones anteriores a histórico conservando trazabilidad. Registrar siguiente pendiente si entrega parcial. | Carpeta vigente con `N` PDF individuales + **1 Word** + **1 Excel MPR cuando efectivamente se haya generado**. Estado declarado `completo_para_revision`, `parcial_con_pendientes` o `bloqueado`, nunca «aprobado». |

**Regla de reanudación:** a «continúa», el motor **no comienza un análisis paralelo ni crea otra carpeta de salida**. Lee el control de avance privado y la carpeta vigente; retoma **la primera etapa con cobertura incompleta**, sin borrar observaciones ni repetir trabajos ya verificados. Si detecta un fallo anterior, lo corrige en su etapa y propaga la rectificación al Word, Excel y PDF afectados.

## Registro mínimo de avance, privado y persistente

Mantener en `CONTROL INTERNO` del expediente (Drive autorizado o `OECE_DATA_DIR`, **nunca Git**) una tabla/JSON con una fila por PDF original y un registro separado por obra:

- **Por PDF:** ID/URL, nombre original, cantidad de páginas, páginas visualmente revisadas/rangos pendientes, tipos y páginas de piezas, obra(s) asociadas, integridad (`completo_aparente / indicio_incompletitud / incompleto_confirmado / no_verificable`), extracción (sí/no/parcial), anotaciones nativas y QA (sí/no/parcial), link a copia.
- **Por obra:** `OB-##`, origen(es), campos cotejados, montos por naturaleza (contractual/liquidado/neto/reajuste/no obra), porcentaje consorcial y base, recepción, estado de admisibilidad, fuentes normativas, bloqueos y observaciones.
- **Por observación:** ID estable, obra/campo, hecho/alternativas literales, PDF y página, clasificación (informativa/cotejo pendiente/bloqueo por obra/transversal), impacto, diligencia, estado y fecha de cierre.
- **Por revisión:** versión, etapa, `páginas_revisadas/páginas_totales`, `N PDF fuentes/N copias resaltadas`, `obras_conciliadas/obras_identificadas`, datos financieros disponibles, Excel ejecutado sí/no, Word consolidado sí/no, vínculo Drive verificado y pendientes.

Una **observación no se pierde** al pasar a la siguiente versión. Una obra sin observaciones conocidas **no es automáticamente una obra aprobada**. No registrar todas las páginas como vistas solo por extraer texto/OCR o generar una miniatura.

## Estructura de carpetas

```text
EXPEDIENTE (copia de trabajo autorizada)/
├─ INICIAL/                                 # Todos los originales; no modificar
└─ RESULTADOS OECE ASSISTANT/
   ├─ ENTREGA_CONSOLIDADA_VIGENTE/
   │  ├─ 01_<nombre original>_RESALTADO.pdf
   │  ├─ 02_<nombre original>_RESALTADO.pdf
   │  ├─ ... hasta N copias individuales
   │  ├─ OBSERVACIONES_CONSOLIDADAS.docx   # exactamente uno vigente
   │  └─ MPR_EVALUACION.xlsb               # solo si efectivamente generado
   ├─ CONTROL INTERNO/                      # privado; no forma parte de entrega
   └─ HISTORICO_VERSIONES_ANTERIORES/       # versiones anteriores sin mezclar
```

En expedientes reales, **respetar el nombre e ID de una carpeta de entrega ya creada**; `ENTREGA_CONSOLIDADA_VIGENTE` es convención conceptual, no una orden de renombrar carpetas en curso. No guardar en la carpeta vigente ZIP parciales, Word antiguos ni carpetas históricas. Si `MPR_EVALUACION.xlsb` no existe, **no inventarlo**.

## Cómo informar avances sin aparentar un cierre

Comunicar al usuario **solo**: (1) etapa actual y cobertura `X/Y`; (2) hallazgos nuevos realmente cotejados con PDF/página; (3) qué se actualizó y **enlace real verificado**; (4) lo que sigue pendiente y su causa. No usar «evaluación integral», «13/13 revisados» o «terminado» si solo se abrió una primera/última página, se leyeron algunas hojas o se marcó un importe por archivo.

## Puerta final de calidad (obligatoria antes de decir «completo»)

- [ ] Todos los documentos y páginas **realmente accesibles** inventariados; se declara cualquier imposibilidad de ver imágenes.
- [ ] Todas las páginas revisadas para integridad, y cada una de las piezas identificadas y analizadas.
- [ ] Las obras y documentos mapeados sin duplicados; todas las observaciones siguen en el **único Word consolidado**.
- [ ] Montos y porcentajes sustentados por página; separamos obra/no obra, reajustes, liquidación y participación.
- [ ] Normativa aplicable comprobada en fuente original con fecha/versión y artículo/numeral/página.
- [ ] Excel institucional **real** generado y validado, con todas sus pestañas y fórmulas; no es solo `.vbs` o ZIP.
- [ ] `N` PDF copias individualmente visibles, nombres pareados, páginas preservadas, marcas `Highlight` revisadas.
- [ ] Drive confirma **un solo Word vigente** y ningún duplicado de versiones en entrega actual.
- [ ] No hay decisiones/obras indispensables pendientes **si se etiqueta `completo_para_revision`**; de lo contrario `parcial_con_pendientes` con pendientes explícitos.

**Documentos complementarios:** [control visual](control-integridad-documental.md) · [Excel](llenado-excel-aumento-cmc.md) · [resaltado nativo](resaltado-evidencias-pdf-cmc.md) · [contrato de entregables](../contratos/entregables-cmc.md) · [control de evidencias](../contratos/control-evidencias.md).

**Modificación del método:** solo por cambio **expreso del titular**, respaldado con versión, motivo y efecto en expedientes iniciados. Una casuística nueva, hallazgo o preferencia del motor **no reordena por sí misma** las etapas.
