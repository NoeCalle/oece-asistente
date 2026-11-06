## Pendiente de afinación: jerarquía de documentos fuente para datos repetidos (2026-11-06)

**Estado: PENDIENTE DE DEFINICIÓN Y VALIDACIÓN CON EXPEDIENTES REALES.** Un mismo dato puede figurar en varias piezas (contrato, acta de entrega de terreno, acta de recepción, liquidación y resolución). No debe tratarse automáticamente como error que la columna `inicial pág` señale una página distinta de la usada por otro evaluador, si ambas fuentes respaldan el mismo dato.

**Criterio inicial propuesto por el evaluador:** para el **nombre del contratista**, cuando figure tanto en el **contrato de obra** como en el **acta de recepción**, **preferir siempre el contrato** como fuente y referenciar en la columna G la página del contrato que lo contiene. La existencia del mismo dato en el acta de recepción no desplaza esa preferencia.

**Por afinar, sin fijar todavía reglas definitivas:** construir una **matriz campo → documento preferente → fuente secundaria → regla de desempate/contradicción**, empezando por nombre de contratista y ampliando luego a objeto, ubicación, fecha contractual, monto original, participación del consorcio, recepción, adicionales, deductivos, reajustes y monto final. Priorizar documentos por **naturaleza del hecho que prueban**, y no imponer una jerarquía global idéntica para todos los campos. Ante una discrepancia material, conservar ambas referencias y registrar observación; la preferencia documental no autoriza ocultarla ni corregir valores sin evidencia.

**Prueba de aceptación futura:** seleccionar datos que aparezcan en al menos dos documentos, comprobar que el agente escoge la fuente preferente para cada campo y que la página G corresponde a esa fuente; registrar en L cualquier divergencia material y documentar excepciones justificadas. Mantener este punto como tarea pendiente hasta formalizar y probar la matriz de precedencia.

# POE-CMC-EXCEL-01 — Llenado de la plantilla Excel de aumento de CMC

**Estado:** en levantamiento guiado con el evaluador. **Inicio:** 2026-11-06. **Versión:** 0.9.
**Uso actual:** ChatGPT o Claude (y Grok si conviene) extraen de PDF y completan Excel cuando tengan archivos y herramientas; el evaluador cubre accesos manuales. **Rol diferencial previsto de GrokBot:** navegar la intranet institucional mediante su PC virtual autorizada para obtener datos y capturas inaccesibles a las otras IA en el flujo actual. No asignar por defecto a GrokBot la extracción de PDF o el llenado ordinario de Excel, que son tareas compartidas. El procedimiento no depende de disponer de GrokBot.
**Relacionado:** [Procedimiento general CMC](aumento-cmc.md) · [Especialista CMC](../agentes/especialista-cmc.md) · [Seguridad](../docs/SEGURIDAD.md).

## Alcance y criterio de verdad

Este documento recoge el **procedimiento real descrito por el evaluador**, no un flujo supuesto a partir de capturas o de los nombres de las hojas. El agente no debe inventar rutas de intranet, menús, credenciales, reglas de cálculo, imágenes o campos. Todo paso aún no enseñado se marca **PENDIENTE DE INSTRUCCIÓN**.

**Archivos de referencia recibidos por el evaluador (no incorporados al repositorio público):**
- `2026.11.06 PLANTILLA ACTUALIZADA MPR.xlsx` — plantilla maestra propuesta, pendiente de control de versión.
- `2026.11.04 AUM_CORPORACION CODINA SAC_CAP.xlsx` — ejemplo de evaluación, reservado para análisis/pruebas con datos autorizados.
- Se recibieron asimismo versiones `.xlsb`. No publicar en GitHub ejemplos completos, datos de proveedores, imágenes de intranet ni resultados financieros.

**Decisión del evaluador (2026-11-06):** la primera hoja `Datos basicos` se completa con **datos e imágenes de diversas fuentes**, por ejemplo la **intranet institucional**. Habrá que documentar cada consulta y transferencia para que un agente que maneje una PC virtual pueda reproducirla.

## Modalidades y reparto de tareas (confirmado por el evaluador)

| Modalidad | Responsable posible | Trabajo | Condición |
|---|---|---|---|
| Ingreso manual actual | Evaluador | Accede a intranet y otras pantallas institucionales, obtiene datos/capturas e ingresa contenido a Excel | Se registra la fuente y se comprueba el destino; no requiere GrokBot |
| Extracción de PDF y llenado de Excel | ChatGPT, Claude o Grok, o evaluador | Lee contratos, liquidaciones y demás PDF, extrae datos sustentados **y los incorpora directamente en las celdas correspondientes del Excel** cuando tenga herramientas de edición | Debe abrir realmente el PDF y el Excel autorizados, citar archivo/página, mapear celda destino, preservar formato y fórmulas y verificar que el valor se guardó; si no puede editar, entregar datos estructurados y declarar el pendiente |
| Elaboración/revisión de Excel | Evaluador o IA habilitada | Completa campos desde intranet, PDF u otras fuentes según acceso disponible; verifica cifras, fórmulas e imágenes | Distinguir dato copiado, extraído, calculado y verificado |
| Navegación de intranet (función diferenciadora) | GrokBot con PC virtual cuando esté disponible; mientras tanto evaluador | Accede a pantallas institucionales, consulta información y obtiene capturas; entrega datos/evidencias al flujo Excel | Acceso institucional autorizado y real; pausa ante credenciales/MFA/cambios de pantalla |

**Regla:** no hay obligación de usar un solo agente ni de automatizar inmediatamente la intranet. El procedimiento se afina a medida que el evaluador aporta nuevos pasos; la ausencia de automatización no bloquea su aplicación manual.

**Origen de cada dato:** consignar `fuente_tipo` (intranet, PDF del expediente, otro documento, cálculo o declaración del evaluador), `fuente_localizador` (pantalla/archivo y página), `responsable` (persona o IA), `metodo` (transcripción, extracción, cálculo, captura), `verificacion`, `estado` y `destino_excel`. Las imágenes siguen el mismo control de origen. Cualquier campo puede provenir de una fuente distinta, incluso dentro de «Datos basicos».

## Flujo operativo (incremental)

### Paso 01 — Preparar la sesión y la plantilla

1. Comprobar que el entorno y la cuenta tienen autorización para acceder al expediente y a la intranet. No eludir controles de acceso, MFA, CAPTCHA ni permisos.
2. Abrir una **copia de trabajo** de la plantilla vigente. Conservar original inalterado, nombre/versión y evidencia de su procedencia.
3. Identificar la hoja `Datos basicos` como punto inicial.
4. **PENDIENTE DE INSTRUCCIÓN:** nombre y ubicación autorizada de la plantilla, modo de apertura, versión institucional y convención de nombres de salida.

### Paso 02 — Reunir datos e imágenes para «Datos basicos»

1. Para cada campo o imagen, consultar la **fuente específica que enseñe el evaluador**; no asumir que todo procede de intranet. Algunos datos existen únicamente en PDF del expediente: una IA con acceso real puede extraerlos, o el evaluador puede transcribirlos.
2. Registrar el origen, ruta de navegación, identificador de búsqueda autorizado, etiqueta exacta mostrada, fecha de consulta, destino en Excel y validación.
3. Trasladar los datos al archivo de trabajo respetando celdas, formato y contenido ya calculado; incorporar imágenes únicamente en la ubicación y tamaño indicados.
4. Si un dato no puede obtenerse, es ilegible o discrepa de otra fuente, **no rellenar por inferencia**: registrar pendiente y solicitar revisión.
5. **PENDIENTE DE INSTRUCCIÓN:** pantallas, menús, nombres exactos de campos, celdas, posiciones de capturas e instrucciones paso a paso para cada fuente.

### Ficha de instrucción por campo o imagen

Por cada nuevo paso comunicado, añadir una fila con ID estable y, cuando sea preciso, su secuencia detallada:

| ID | Destino Excel (hoja/celda/imagen) | Dato requerido | Fuente autorizada | Ruta de navegación y búsqueda | Acción para obtener/copiar | Cotejo y evidencia | Estado |
|---|---|---|---|---|---|---|---|
| DB-001 | `Datos basicos` / por identificar | Por identificar | Intranet, PDF u otra fuente por definir | PENDIENTE | PENDIENTE | PENDIENTE | Por instruir |

Al definir cada instrucción, registrar además:
- **Precondiciones:** sesión iniciada, pantalla visible, expediente correcto, acceso autorizado.
- **Pasos de interfaz:** clics o navegación con etiquetas visibles, condición observable de éxito; evitar coordenadas fijas si puede usarse un control identificable.
- **Transformación:** literal, formato de fecha, moneda, porcentaje o captura; prohibido reinterpretar sin regla autorizada.
- **Destino:** hoja/celda/rango o posición de imagen, comportamiento de reemplazo y si se mantiene fórmula/formato.
- **Validación:** comparación visual o documental, y qué hacer ante discrepancias.
- **Evidencia y privacidad:** localizador interno y trazabilidad sin exponer secretos o documentos sensibles en GitHub.

### Paso 03 — Control de calidad de la hoja

- Verificar que se completaron únicamente destinos autorizados y que no se alteraron fórmulas, imágenes previas o vínculos accidentalmente.
- Contrastar identificación del proveedor y expediente con la fuente válida que se indique.
- Registrar campos completados, pendientes, discrepancias y fuentes efectivamente consultadas.
- **PENDIENTE DE INSTRUCCIÓN:** validaciones concretas y condición institucional de cierre de la hoja.

### Paso 04 — Continuación de las demás hojas

La secuencia para `Obras nacional`, `CLC`, `Hoja Calculo`, `datos` y `CALCULO CMC` se documentará cuando el evaluador la describa; los nombres de hoja **no equivalen** a una secuencia de ejecución confirmada. El análisis sustantivo se mantiene sujeto al [procedimiento general](aumento-cmc.md).

## Separación de etapas para evitar cortes (confirmado 2026-11-06)

Para un expediente de aumento de CMC ejecutar **dos fases separadas**, sin adelantarse a la segunda:

- **Fase documental:** inventario de PDFs y datos identificativos; apertura del PDF de experiencias original; conteo total de páginas; mapa de segmentos por obra, contrato y pieza; datos extraídos y cada localizador; control de lectura completa, imágenes y páginas no verificadas; almacenar índice versionado en carpeta privada del expediente. Si los documentos son escaneados, no presentar el texto parcial como revisión completa. Documentar montos contractuales o liquidaciones como **datos literales preliminares**, sin decidir su computabilidad. Prohibido emitir decisión normativa o CMC durante esta fase.
- **Fase normativa y cálculo:** **solo tras instrucción del titular** y con las extracciones identificadas; buscar biblioteca normativa en Drive primero, determinar elegibilidad, participaciones y factores con sustento, y luego generar entregables y Excel revisado.

En un caso piloto el archivo de experiencia contenía 94 páginas, de las que solo 2 tenían capa de texto. Fue necesario revisar páginas visualmente y preparar un índice de tres grupos documentales; la validación de detalle, integridad y todos los importes permanece pendiente. **No almacenar el índice real ni los nombres/datos de ese proveedor en GitHub público.**

## Auditoría de cobertura visual por página (aprendizaje 2026-11-06)

Para escaneos extensos, generar **una fila por cada página física del PDF**, con identificador de obra, tipo de documento, disponibilidad de capa de texto y controles independientes: (a) vista general; (b) lectura detallada; (c) foliación impresa; (d) continuidad de texto; (e) exactitud de cifras. **No confundir 94/94 páginas vistas a escala de miniatura con 94/94 páginas leídas exhaustivamente**.

En el primer piloto de experiencia se comprobó la existencia de 94 páginas, pero solo las primeras 2 tenían texto PDF; las otras 92 eran imágenes. Se cubrieron las 94 mediante inspección visual general y quedó pendiente verificar cláusulas, detalles, foliación impresa y continuidad a tamaño legible. La bitácora privada de cobertura se guarda en la carpeta del expediente, nunca en el GitHub público.

Al continuar, revisar los tramos documentales completos por obra; documentar el estado como `vista_general`, `lectura_detallada`, `cotejo_integridad` y `verificado` **solo tras evidencias correspondientes**. Prohibido usar porcentajes de progreso que sugieran validación integral si solo hay cobertura visual panorámica.

## Llenado específico de la plantilla MPR (piloto Codina, 2026-11-06)

**Orden obligatorio de trabajo:** primero `Datos basicos` (hasta donde haya evidencia), después `Obras nacional` por cada obra. No esperar a tener todos los campos de datos básicos para pasar a las obras; registrar pendientes.

**No insertar imágenes para reemplazar texto de documentación.** Si el evaluador anterior pegó una imagen del nombre u objeto de la obra, el agente escribe el texto fielmente, normalizado solo para legibilidad. Debe conservar números, moneda, fechas y fórmulas en los tipos de celda que espera la plantilla.

**Mapa de la plantilla `2026.11.06 PLANTILLA ACTUALIZADA MPR.xlsx`:**
- `Datos basicos`: proveedor en `B4`; hoja de trámite en `F5`; RNP `F9`, RUC `F10`, SUNARP `F11`; período financiero `F15`; activo corriente `F16`; pasivo corriente `F17`. Es importante escribir en **F**, no desplazarse a E. Dejar en blanco los datos no sustentados.
- `Obras nacional`: las tres primeras obras ocupan `9:24`, `31:46`, `53:68` respectivamente. Filas `8`, `30` y `52` sirven para identificar la obra con **texto** y documento de respaldo, no captura.
- Para cada **campo individual**, escribir el dato en **columna J (Datos)** y la **página del PDF donde aparece la evidencia** en **columna G («inicial pág»)**. Numeración **real del PDF, base 1**, no folio impreso ni número de página del archivo Word. El PDF se cita en su versión original. Si el valor surge de varias piezas, registrar en G la página principal y detallar las demás páginas y operación en L.
- **Columna L**: observaciones iniciales concretas, incluyendo discrepancia, fuente alternativa, dato no encontrado y riesgo documental; no sustituye la información de la columna J.
- **Cuidado con tipos:** por ejemplo, `J12/J34/J56` representan la participación porcentual consorcial como `0.20/0.50/0.30` con formato `0%`, **no una cadena descriptiva**; nombres y RUC deben ir en campos de contratista y notas de observación sin romper enlaces de cálculo. Fechas como fechas reales de Excel y montos como números, no texto.
- Si una imagen escaneada es poco legible, registrar página y `pendiente_cotejo`; si no se pudo determinar, **dejar celda de dato vacía** y describirlo en L. No confundir «no acreditado» con valor cero.
- Antes de entregar, controlar hojas preservadas, fórmulas en todas las pestañas, cruces y resultados. El motor de vista previa puede mostrar `#NAME?` por fórmulas matriciales o de búsqueda; comprobar el original y no atribuir automáticamente el error al expediente.

**Alcance de esta iteración:** los datos generales y económicos iniciales se llenan solo en lo acreditado; `Obras nacional` se llena con tres obras y sus páginas, además de reservas OB-01 (diferencia liquidación), OB-02 (identidad contractual y cronología) y OB-03 (liquidación vs deductivo/fecha acta). **Es un llenado preliminar, no una CMC otorgada.**

### Preservación obligatoria de la plantilla Excel (incidente REV13 → REV14)

- **Crear una copia del archivo original y trabajar sobre ella**; nunca recrear la plantilla desde cero ni alterar el archivo fuente.
- Escribir solo en celdas de datos habilitadas. Verificar previamente combinaciones: **G8, G30 y G52 son celdas interiores de rangos combinados** y nunca se deben usar para números de página. Las páginas van en G9:G24, G31:G46 y G53:G68 según los datos correspondientes.
- Conservar exactamente todas las fórmulas, combinaciones, nombres de pestañas, validaciones, dibujos y elementos adjuntos de la plantilla. No reemplazar fórmulas por sus valores calculados (incidente `datos!F4`).
- Un motor de exportación que reserializa el libro y pierde elementos o modifica combinaciones **no es apto para entregar la copia**. En ese caso, preservar el paquete original y modificar únicamente las celdas de entrada, sin reexportar indiscriminadamente el libro.
- **Prueba estructural obligatoria previa a entrega:** comparar por hoja el número y texto de las fórmulas, las referencias de todos los rangos combinados, los nombres de hoja, los archivos de imágenes/dibujos, las relaciones y las demás partes del Excel; verificar que cualquier cambio se limite a las entradas intencionales.
- En REV14 se preservaron 4.210 fórmulas, 1.706 rangos combinados en 6 hojas y las seis imágenes originales. Se incorporaron 8 datos en `Datos basicos`, 120 en `Obras nacional` y solo se corrigió el formato de tres celdas de fecha.


### Encabezados de nombre de obra en celdas combinadas (corrección del piloto, 2026-11-06)

**Obligatorio:** la hoja `Obras nacional` tiene las cabeceras combinadas `D6:J6` para OB-01, `D28:J28` para OB-02 y `D50:J50` para OB-03. Escribir el **nombre legible de la obra como texto** en la celda superior izquierda **D6, D28, D50**, respectivamente, **sin descombinar** ni pegar capturas. Estos campos son distintos de `J15/J37/J59` (objeto contractual). El primer generador binario (Excel 2013) omitió estas 3 celdas, aunque había cargado 128 entradas de las demás tablas; la corrección del generador incorpora 131 valores en total. En el piloto, usar textos derivados de los contratos en páginas PDF 9, 33 (identidad de río Chillón en el cuerpo; encabezado alternativo río Poturo se conserva como observación) y 68. Verificar visualmente la presencia de los tres títulos **antes de declarar el archivo completo**.

### Nueva plantilla recibida: .xlsm exportada por Excel (2026-11-06)

El titular aportó `2026.11.06 PLANTILLA ACTUALIZADA MPR.xlsm` tras guardarla desde Excel. Contiene seis pestañas y **no incluye proyecto VBA** (no hay `vbaProject.bin` en el paquete), aunque tiene extensión habilitada para macros. Se generó una **copia de trabajo** `CMC-TEST-001_PLANTILLA_MPR_LLENADA_REV16.xlsm`, con 8 valores en `Datos basicos` y 120 en `Obras nacional`. El maestro se conserva intacto.

**Método aplicado:** usar `artifact_tool` para escribir/verificar entradas y, para retener el formato `.xlsm` no exportable por esa API, transmitir exclusivamente los nodos de valores a las dos hojas del paquete original; no reserializar el resto. La comparación posterior verifica 35 partes originales idénticas, fórmulas y combinaciones intactas y seis pestañas legibles. **No declarar compatibilidad definitiva hasta abrir en Microsoft Excel de Windows sin reparación**, porque los problemas previos eran específicos de Excel. Si la plantilla `.xlsm` del titular también resulta defectuosa al abrirse en Excel, el problema no puede resolverse asegurando únicamente equivalencia estructural.

### Fuente de plantilla validada en Microsoft Excel: formato binario .xlsb (2026-11-06)

**Resultado de prueba del titular:** `2026.11.06 PLANTILLA ACTUALIZADA MPR.xlsx`, SIN modificar, produce la misma advertencia de reparación en Microsoft Excel. En cambio, `2026.11.06 PLANTILLA ACTUALIZADA MPR.xlsb` abre y funciona correctamente. Por ello la causa primaria no son los valores ingresados a REV13–REV15: el `.xlsx` proporcionado **ya presenta incompatibilidad/defecto** de apertura; no puede asumirse que sus metadatos sean válidos por ser un ZIP estructuralmente legible. El origen preciso de la incompatibilidad requiere un análisis adicional y no debe afirmarse sin pruebas.

**Decisión de implementación:** usar **exclusivamente el `.xlsb` funcional como archivo maestro**, generar primero una **copia `.xlsb`**, y editarla con el motor nativo de Microsoft Excel (por ejemplo, automatización COM en Windows), escribiendo SOLO valores en `Datos basicos` y `Obras nacional`. No convertir el `.xlsb` a `.xlsx` mediante lectores/escritores generales, porque la conversión puede cambiar relaciones, extensiones, fórmulas, formatos combinados o componentes binarios. Comprobar apertura en Microsoft Excel SIN diálogo de reparación, además de fórmulas/celdas combinadas, ANTES de declarar el entregable válido.

**Limitación de ejecución:** herramientas que solo leen XLSB o exportan XLSX no prueban que puedan editar XLSB preservando el libro. Si no está disponible el motor Excel/COM en el entorno de ejecución, proporcionar una automatización local verificable o declarar el impedimento, en vez de entregar otro XLSX incompatible.

### Incidente de archivo que Microsoft Excel intenta reparar — REV14 (06/11/2026)

El evaluador abrió REV14 y Excel informó reparación de `xl/metadata.xml`, propiedades del libro y celdas de otra hoja; la vista perdió combinaciones y el nombre de proveedor quedó partido en varias líneas. **La comprobación de que hay 4.210 fórmulas y 1.706 rangos combinados NO prueba por sí sola que Excel pueda abrir el archivo sin repararlo.** No volver a declarar «corregido» un libro basándose solo en recuentos XML.

**Procedimiento de recuperación adoptado:** partir de los **bytes del archivo original**, cambiar solo los nodos de valor de las celdas de entrada originalmente vacías, sin reserializar hojas completas, estilos, metadatos, fórmulas, relaciones, dibujos o anchos. En el piloto los únicos miembros del paquete que deben variar son `xl/worksheets/sheet1.xml` (`Datos basicos`) y `xl/worksheets/sheet2.xml` (`Obras nacional`); no modificar `xl/metadata.xml`, `xl/styles.xml` ni `xl/worksheets/sheet3.xml` a `sheet6.xml`. Para fechas que estaban sin formato de fecha, escribir texto legible conservando estilo, no crear estilos. Verificar identidad byte a byte de todas las demás partes, legibilidad XML, combinaciones y fórmulas, y obtener prueba de apertura en **Microsoft Excel** antes de declarar aptitud definitiva. Si no se puede abrir Excel en el entorno, decirlo explícitamente.

## Lección del primer piloto: evaluación ciega sin Excel previamente resuelto (2026-11-06)

**En operación real no existe Excel de evaluación completado por un tercero.** El único libro de entrada editable es una **copia limpia de la plantilla institucional vigente**. El expediente, las consultas autorizadas y la biblioteca normativa son las fuentes de datos; la copia de una evaluación anterior solo sirve en pruebas como patrón de comparación **después de producir y congelar el resultado independiente**, nunca para extraer montos, factores, notas o fórmulas de un nuevo caso.

**Prueba mínima de aceptación:**
1. Partir de plantilla limpia, inventariar fuentes originales (PDF escaneados, intranet y financieros) y llenar hoja/celda con evidencia de procedencia.
2. Construir obras, montos netos, participaciones y observaciones desde el expediente, sin mirar la evaluación modelo.
3. Obtener y justificar a/f/e con normativa aplicable y valores efectivamente acreditados; si faltan datos, mantener `null` y continuar con los campos disponibles.
4. Conservar originales, fórmulas, imágenes y todas las hojas de la plantilla; crear copia revisada, verificar celdas escritas, fórmulas y resultado final, y comprobar que no aparezcan errores de fórmula/celdas vacías críticos.
5. **Solo después**, si hay un Excel patrón de prueba, comparar por celda y explicar diferencias; no forzar el resultado esperado.
6. Distinguir entregables: (a) plantilla oficial efectivamente rellenada, (b) libro auxiliar de verificación, (c) simulación basada en evaluación previa. **Nunca llamar al segundo ni al tercero «plantilla institucional completada».**

**Resultado del primer caso didáctico:** se rellenaron cuatro celdas identificativas en una copia parcial de `Datos basicos`; se elaboró un libro auxiliar de verificación y un libro de simulación derivado del ejemplo resuelto, pero **no se completó de forma independiente la plantilla institucional de seis hojas desde cero**. La coincidencia de CMC demuestra reproducción aritmética, **no** validación del flujo de producción. Como control adicional, el libro `SIMULACION_CMC_REV12` presenta fórmulas de validación cuya lectura arroja `#NAME?` en algunos campos; requieren comprobación/corrección antes de considerarlo entregable final.

## Lectura de PDF escaneado por lotes con recuperación (instrucción del evaluador, 2026-11-06)

**Regla operativa obligatoria:** procesar **como máximo 20 páginas por lote**, recomendando **15 páginas** cuando el escaneo sea pesado, tenga tablas o se necesite OCR. No lanzar una lectura de 94 páginas en una sola operación. Si el lote tarda demasiado o falla, reducirlo a 5–10 páginas y reanudar desde el último punto confirmado, **sin volver a procesar todo el PDF**.

1. **Inventariar antes de empezar:** contar páginas y generar rangos consecutivos, sin solapamientos ni huecos. Ejemplo para 94 páginas, con máximo 20: `1–20`, `21–40`, `41–60`, `61–80`, `81–94`. Con lotes de 15: `1–15`, `16–30`, `31–45`, `46–60`, `61–75`, `76–90`, `91–94`.
2. **Persistir tras cada lote:** guardar extracción estructurada por página (obra, tipo de instrumento, texto útil, montos, fechas, participación y referencias), imágenes/recortes necesarios y una bitácora de estado, **en almacenamiento privado autorizado del expediente**, no en GitHub.
3. **Estados separados:** `no_iniciado`, `procesando`, `extraido_pendiente_cotejo`, `verificado`, `error_reintentar`. Un lote solo cuenta como **procesado** si sus resultados se han escrito y comprobado; una miniatura revisada no es lectura detallada.
4. **Reanudación:** al iniciar una sesión nueva, consultar la bitácora persistida y continuar desde la primera página/lote no confirmado. Si la operación se cortó en la página 23, por ejemplo, **no declarar completado el tramo 21–40**; conservar 21–23 únicamente si están guardadas y verificadas como extracción, y reiniciar en 24 o en el primer faltante.
5. **Control de calidad por lote:** contrastar datos relevantes con imagen original y anotar páginas ilegibles, transiciones, faltantes de foliación, contradicciones y OCR dudoso. No corregir por conjetura. Registrar alcance exacto de la revisión.
6. **Indicadores verificables:** reportar `páginas_extraídas_y_guardadas / total`, `páginas_verificadas / total`, `lotes_completados / total_lotes`, y `páginas_pendientes`. El avance visual panorámico va por separado. Mostrar ambos números, no un porcentaje arbitrario como sustituto.
7. **Salidas intermedias:** `extraccion_lote_001_015.json` (o rango real), `control_paginas.csv`, `pendientes.json`, con versiones o identificadores estables. La consolidación final combina solo lotes confirmados, detecta duplicados/huecos y nunca elimina evidencias previas.
8. **Separación de fases:** primero cerrar la extracción de todos los lotes y las excepciones relevantes; solo después, con autorización del titular, iniciar evaluación normativa y cálculo CMC.

**Motivo de esta regla:** el primer intento de extracción masiva de `EXPERIENCIAS.pdf` (94 páginas escaneadas) se interrumpió tras aproximadamente 23 páginas. El usuario estableció limitar futuras lecturas a 15–20 páginas por lote para evitar interrupciones y pérdida de avance. **Esos 23 resultados no se consideran persistidos/validados salvo que la bitácora y sus archivos lo acrediten.**

## Método normal para sustentos de experiencia escaneados (confirmado 2026-11-06)

**Supuesto operativo:** en expedientes típicos de experiencia, los contratos, actas y liquidaciones suelen presentarse como **páginas escaneadas**. La falta de capa de texto PDF no es defecto del expediente ni razón para abandonar la extracción. El agente prioriza la **interpretación visual de imágenes a tamaño legible**, usando OCR cuando resulte necesario y siempre cotejando su salida con la imagen.

**Secuencia por bloques pequeños para evitar cortes**:
1. Abrir el PDF original y enumerar todas las páginas. Mantener inalterado el original y su vínculo privado.
2. Agrupar por obra y por pieza documental usando vistas panorámicas; marcar cada página cubierta solo como `vista_general`.
3. Renderizar con resolución suficiente **cada página que aporte hechos** (identidad, contrato, consorcio, fecha, monto, recepción, liquidación, adicionales, deductivos). Leerla visualmente; si es ilegible, ampliar recortes; OCR es una ayuda secundaria, no evidencia autónoma.
4. Registrar por cada dato: nombre de PDF, número de página del PDF, tipo de documento, transcripción literal breve, valor interpretado, campo, estado de lectura y dudas.
5. Verificar continuidad de las piezas y folios de las páginas intermedias: una portada y un artículo resolutivo no acreditan por sí solos la revisión íntegra de la resolución. Inspeccionar las transiciones a tamaño legible y anotar cualquier señal objetiva de omisión.
6. Diferenciar `lectura_visual_ampliada_campos`, `integridad_comprobada` y `cotejo_documental_completo`. No marcar página/obra como completamente verificada con una inspección por miniaturas ni por extracción OCR sola.
7. Consolidar revisiones incrementales privadas `REVxx` preservando resultados anteriores, pendientes y enlaces originales; no promover importes o fechas a experiencia computable durante la fase documental.

**Piloto:** la ampliación de las páginas 15, 16 y 32 de una obra permitió extraer CUI, sistema, modalidad, monto de contrato, plazos, fechas de terreno/inicio/término previsto y presupuesto adicional, sin calificar normativa ni sumar el adicional. El control integral de continuidad sigue pendiente. Los datos específicos del proveedor se conservan **solo en el expediente privado**, no en GitHub.

## Primer mapeo de celdas verificado (plantilla 06/11/2026)

El contraste **estructural** entre plantilla vacía y Excel ejemplo permitió localizar los siguientes destinos; el contenido de cada expediente siempre debe obtenerse de sus propias fuentes y no copiarse del caso ejemplo:

| ID | Campo | Destino | Origen documental esperado | Tratamiento |
|---|---|---|---|---|
| DB-001 | Denominación del proveedor | `Datos basicos!B4` | Hoja de ruta/formulario | Texto exacto, cotejar |
| DB-002 | Número de hoja de trámite | `Datos basicos!E5` | Hoja de ruta | Texto exacto, cotejar |
| DB-003 | Registro RNP | `Datos basicos!E9` | Hoja de ruta y, si corresponde, consulta intranet | Mantener como identificador; verificar |
| DB-004 | RUC | `Datos basicos!E10` | Hoja de ruta/formulario | 11 dígitos, no inferir |
| DB-005 | Partida SUNARP | `Datos basicos!E11` | Consulta registral/documento acreditativo | Pendiente de fuente válida |
| DB-006 | Capital SUNARP | `Datos basicos!E12` | Consulta registral/documento acreditativo | Pendiente |
| DB-007 | CMC vigente | `Datos basicos!E13` | RNP/intranet o constancia acreditativa | Pendiente, no asumir del ejemplo |
| DB-008 | Periodo financiero | `Datos basicos!E15` | Documentación financiera | Pendiente |
| DB-009 | Activo corriente | `Datos basicos!E16` | Documentación financiera | Pendiente |
| DB-010 | Pasivo corriente | `Datos basicos!E17` | Documentación financiera | Pendiente |

**Atención:** las fechas y demás rótulos pueden variar entre versiones de plantilla y Excel ejemplo. No trasladar celdas basadas en la fila del ejemplo sin revisar versión. Las capturas de intranet y reglas de las demás celdas siguen sin enseñarse.

**Prueba piloto:** durante la primera ejecución con el expediente Codina se obtuvo un borrador local `CMC-TEST-001_Datos-basicos_REV01.xlsx` con los cuatro primeros datos identificativos (B4, E5, E9, E10) procedentes de la hoja de ruta. Esto es una **copia preliminar no validada institucionalmente**, no equivale a un Excel ya publicado en Drive; debe verificarse preservación de imágenes/fórmulas y el resto de celdas permanece pendiente.

## Tratamiento de PDF extensos con múltiples contratos de experiencia (confirmado 2026-11-06)

El evaluador advierte que el documento más voluminoso puede ser el que acredita experiencia y que el proveedor puede adjuntar **varios contratos y sus documentos sustentatorios reunidos en un solo PDF**. Por tanto:

1. **Un archivo PDF no equivale a una obra ni a un contrato.** Antes de extraer montos, inspeccionar la totalidad del archivo y construir un índice interno por obra/contrato.
2. Para cada bloque identificar su **primera y última página del PDF**, folios impresos cuando existan, tipo de pieza (contrato, adenda, acta, recepción, liquidación, consorcio u otros), entidad, objeto, números, fechas y vínculos entre piezas.
3. Asignar IDs estables `OB-01`, `OB-02`, etc.; una obra puede abarcar varios tramos no contiguos y un contrato puede aparecer junto con varios documentos. Registrar **cada tramo exacto** en el índice, sin atribuir documentos a una obra solo por cercanía de páginas.
4. La revisión puede hacerse por lotes de páginas para manejar PDFs grandes, pero **debe cubrir todas las páginas** y dejar constancia de páginas no procesadas, ilegibles, repetidas o fuera de orden. No concluir que el expediente fue revisado integralmente solo por leer los primeros segmentos o extraer texto.
5. Aplicar [control de integridad documental](control-integridad-documental.md): cotejar numeración visible, continuidad física y páginas faltantes. Diferenciar defectos de escaneo de errores de OCR; contrastar visualmente cuando sea necesario.
6. Vincular cada valor extraído a `archivo PDF + página(s) del archivo + folio(s) impresos si los hay + obra/contrato + pieza documental`. Contrastar datos incompatibles o contradictorios; no sumar automáticamente todos los contratos ni asumir que todos cumplen requisitos.
7. Solo después del índice y cotejo pasar los datos acreditables a las celdas de la plantilla; **preservar fórmulas y diseño**, registrar hoja/celda y comprobar el valor guardado.
8. Los PDF originales y el índice por expediente se conservan en Drive o almacenamiento privado autorizado; **en GitHub solo el procedimiento genérico y pruebas sintéticas**.

**Modelo mínimo del índice privado (por contrato/obra):** `obra_id`, `pdf_origen`, `tramos_paginas_pdf`, `folios_impresos`, `tipo_documento`, `numero_contrato`, `entidad`, `fecha`, `monto`, `moneda`, `participacion`, `observaciones`, `estado_revision`. Los campos no sustentados quedan pendientes, nunca inferidos.

## Reglas de ejecución para GrokBot u otro agente con PC virtual

1. Leer primero `AGENTS.md`, `agentes/especialista-cmc.md`, `procedimientos/aumento-cmc.md` y este POE; operar solo con permisos y herramientas realmente disponibles.
2. No usar accesos personales ajenos ni pedir almacenar contraseñas, cookies o tokens en prompts, capturas, logs o repo. Dejar al titular el inicio de sesión y los desafíos MFA/CAPTCHA.
3. Navegar por la intranet **solo** siguiendo pasos verificados de este documento; si la interfaz cambia, detener esa subrutina y registrar la diferencia, sin explorar arbitrariamente pantallas sensibles.
4. Capturas institucionales, fichas de proveedores, documentos e informes van al almacenamiento privado autorizado, **nunca al repositorio público**. En el registro del caso guardar fuente/fecha/identificador interno, no el contenido sensible.
5. No ejecutar macros ni habilitar contenido activo solo para completar la plantilla. Preservar fórmulas y comprobar resultados; no confundir reproducción del Excel con aprobación normativa.
6. Guardar una copia de salida versionada y un reporte de ejecución: pasos hechos, fuentes efectivamente accesibles, validaciones, excepciones, pendientes y operaciones manuales.
7. Sin firma, aprobación, notificación o envío institucional automático; requieren revisión y acción expresa de la persona responsable.

## Bitácora de aprendizaje

| Fecha | Versión | Instrucción confirmada | Estado |
|---|---|---|---|
| 2026-11-06 | 0.1 | La hoja inicial es `Datos basicos`; se llena con datos e imágenes de varias fuentes, entre ellas intranet; el registro se mantiene en GitHub para ejecución posterior mediante PC virtual | Confirmada |
| 2026-11-06 | 0.2 | Mientras no se use GrokBot, el evaluador ingresa datos manualmente. Hay información exclusiva de PDF que puede extraer ChatGPT, Claude o Grok con acceso efectivo. Se permite flujo híbrido y refinamiento progresivo | Confirmada |
| 2026-11-06 | 0.3 | ChatGPT, Claude o Grok pueden **extraer de los PDF y llenar directamente la plantilla Excel**, siempre que tengan acceso y herramientas de lectura/escritura; verificar persistencia y fórmulas. La intervención manual se reserva para tareas sin acceso o que necesiten revisión | Confirmada |
| 2026-11-06 | 0.4 | GrokBot se reserva principalmente para navegación automatizada de la intranet con PC virtual; extracción PDF y edición Excel no son funciones exclusivas de GrokBot y pueden realizarlas ChatGPT/Claude. Hasta probar el acceso, la intranet la atiende manualmente el evaluador | Confirmada |
| 2026-11-06 | 0.5 | Un PDF de experiencia puede reunir múltiples contratos, liquidaciones y anexos; indexar cada obra con rangos de páginas y evidencias, cubrir el documento completo y no equiparar un archivo con una obra | Confirmada |
| 2026-11-06 | 0.6 | Primer mapeo estructural de celdas de «Datos basicos» y piloto de llenado documental de cuatro campos; los valores reales no se publican en GitHub | Parcialmente verificada |
| 2026-11-06 | 0.7 | Separar extracción documental y evaluación normativa; PDFs escaneados pueden carecer de capa de texto; indexar por página y dejar cifras descriptivas sin computar hasta la fase normativa | Confirmada |
| 2026-11-06 | 0.8 | Auditoría por cada página y distinción obligatoria entre inspección visual completa del PDF y lectura detallada/cotejo de integridad de cada página | Confirmada |
| 2026-11-06 | 0.9 | Para documentos habituales escaneados, usar lectura visual ampliada y OCR secundario; extraer en bloques pequeños con estado independiente de integridad y sin adelantar normativa | Confirmada |
| 2026-11-06 | 1.0 | Lectura de PDF por lotes de 15–20 páginas como máximo; guardar checkpoint por lote, reanudar tras cortes y medir progreso desde archivos confirmados, no desde intentos | Confirmada |
| 2026-11-06 | 1.1 | El piloto con Excel ya resuelto no prueba llenado autónomo; iniciar desde plantilla limpia, usar evaluación anterior solo como patrón posterior y distinguir simulación de libro institucional completo | Confirmada |
| 2026-11-06 | 1.2 | Orden Datos basicos→Obras nacional; F4/F5 y fuentes, G=«inicial pág» del PDF, J=datos, L=observaciones; transcripción textual de nombres y tipos numéricos intactos | Confirmada |
| 2026-11-06 | 1.3 | Copia fiel de plantilla y prueba estructural antes de entregar; evitar celdas combinadas interiores y pérdida de fórmulas/dibujos por exportación | Confirmada |
| Pendiente | — | Primera ruta real, campo y captura aportados por el evaluador | Por levantar |

> **Mantenimiento:** cada explicación nueva del evaluador actualiza este archivo, incrementa versión y distingue hechos confirmados de instrucciones pendientes. No publicar ejemplos reales o credenciales en commits.
