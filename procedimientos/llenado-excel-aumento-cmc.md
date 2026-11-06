# POE-CMC-EXCEL-01 — Llenado de la plantilla Excel de aumento de CMC

**Estado:** en levantamiento guiado con el evaluador. **Inicio:** 2026-11-06. **Versión:** 0.2.
**Uso actual:** procedimiento asistido con ingreso manual por el evaluador y extracción/análisis documental por ChatGPT, Claude o Grok según sus herramientas y acceso autorizados. **Uso futuro opcional:** reproducción de pasos de interfaz por GrokBot desde una PC virtual. No supeditar el procedimiento a disponer de GrokBot.
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
| Lectura de PDF | ChatGPT, Claude o Grok, o evaluador | Extrae cifras, fechas, información de obras y otros campos que solo constan en archivos PDF | Debe abrir realmente el PDF autorizado, citar archivo y página y marcar incertidumbres; si no tiene acceso, no inventa resultados |
| Elaboración/revisión de Excel | Evaluador o IA habilitada | Completa campos siguiendo las instrucciones confirmadas, preserva fórmulas e imágenes y contrasta resultados | Distinguir dato copiado, extraído, calculado y verificado |
| Automatización posterior | GrokBot con PC virtual, si se habilita | Ejecuta pasos de interfaz ya documentados, incluidos los de intranet permitidos | Autorización y acceso efectivos; pausa ante credenciales/MFA/cambios de pantalla |

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
| Pendiente | — | Primera ruta real, campo y captura aportados por el evaluador | Por levantar |

> **Mantenimiento:** cada explicación nueva del evaluador actualiza este archivo, incrementa versión y distingue hechos confirmados de instrucciones pendientes. No publicar ejemplos reales o credenciales en commits.
