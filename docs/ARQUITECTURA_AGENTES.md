# OECE Assistant — arquitectura centrada en agentes (v2)

**Decisión del titular: 05/11/2026. Modalidad preferida: agent-first / Drive-first.**

## Qué es y qué NO es

OECE Assistant es un conjunto de **instrucciones profesionales, procedimientos, contratos de evidencia y entregables** que ejecuta la **IA elegida por el titular** (Codex/ChatGPT, Claude o Grok Bot) desde su sesión y herramientas autorizadas. El coordinador y los especialistas son **roles**: no requieren procesos Python, un servicio MCP permanente ni una API de modelo externa. El cliente puede implementar estos roles como subagentes reales o como etapas aisladas de la misma conversación; **no asumir** que un proveedor soporta subagentes ni acceso automático a archivos GitHub.

- **GitHub:** versión y distribución de instrucciones, procedimientos, esquemas y pruebas sintéticas. No alberga expedientes ni claves.
- **Drive:** repositorio documental. Biblioteca normativa **existente**: [OECE Assistant / 01 Biblioteca normativa](https://drive.google.com/drive/folders/1jsswi2044osUsH7fRE03YqfPhGCHI38G). Cada expediente se identifica mediante enlace o carpeta de Drive **indicada por el titular**; `02 Expedientes` y `03 Resultados` son nombres propuestos, no carpetas cuya existencia se presuponga.
- **IA:** busca, abre, lee, razona, verifica, calcula con herramientas disponibles, prepara archivos y los guarda en Drive cuando exista conexión y autorización del titular.
- **Python/MCP existente:** **respaldo opcional** para OCR, cálculo decimal, validación y generación local; NO requisito de entrada en modalidad agent-first. No se elimina código ni se confunden sus pruebas con validación de los agentes cloud.

## Punto de entrada

Leer en orden:
1. [AGENTS.md](../AGENTS.md) — prioridad del modo agent-first.
2. [Agente coordinador](../agentes/coordinador.md).
3. [Contrato de evidencias](../contratos/control-evidencias.md).
4. Según procedimiento, **solo uno**: [CMC](../agentes/especialista-cmc.md) o [consultores](../agentes/especialista-consultores.md), con su procedimiento y contrato.
5. Para **pregunta normativa directa del titular**, [Consulta Normativa](../agentes/consulta-normativa.md) en lugar del flujo de expediente.

**Prompt portable:** [instrucciones de arranque para cualquier cliente](PROMPT_OECE_UNIVERSAL.md). Abrirlo/cargarlo en clientes que no leen automáticamente archivos del repo. `CLAUDE.md` y `GROK.md` proporcionan entradas específicas; el repositorio por sí solo no instala un agente en servicios externos.

## Flujo end-to-end previsto

`Petición del titular → Coordinador (clasifica por trámite declarado) → Especialista → Drive: expediente + biblioteca normativa → extracción y contraste → cálculo/verificación → entregables + índice de fuentes → carpeta de resultados en Drive → respuesta con enlaces`.

**Regla de fuentes:** normativas en Drive primero; si una búsqueda real no encuentra sustento suficiente, **avisar al titular antes de navegar internet** y etiquetar con claridad la procedencia. Si Drive falla, informar *falta de acceso*, no *inexistencia de norma*. La falta de un documento del **expediente** debe comunicarse; buscar en internet no sustituye contratos ni constancias individuales.

**Transferencia de documentos:** si el entorno necesita temporalmente un PDF, obtenerlo mediante el conector autorizado sin exigir descarga manual a la PC. No afirmar que la terminal cloud hereda la sesión Drive: comprobar si puede leer/subir esos bytes. Puede requerirse una copia temporal aislada; eliminarla según herramientas disponibles y las reglas aplicables. Guardar resultados en Drive explícitamente, no confiar en persistencia de la VM.

## Enrutamiento y aislamiento

- Pregunta normativa aislada → solo agente normativo, **sin expediente**.
- `aumento_cmc` declarado → agente CMC, **tres entregables secuenciales**.
- `ampliacion_consultores` declarado → agente consultores, **informe Word + matriz AC**.
- Cualquier otro trámite o clasificación contradictoria → no fingir especialidad: indicar que está fuera de los dos especialistas agent-first y derivar a la modalidad histórica si corresponde; no inventar reglas.
- El agente CMC y el de consultores **consultan la biblioteca por sí mismos**, **NO invocan automáticamente al agente de preguntas normativas**. La resolución estructurada de dudas interagente sigue diferida a T53.

## Criterio operativo transversal adquirido de capacitación (05/11/2026)

**Integridad documental independiente de suficiencia de datos:** los especialistas CMC y consultores revisan visualmente cada original **de principio a fin**, con [control de integridad](../procedimientos/control-integridad-documental.md). Si una cláusula, párrafo, artículo, hoja o parte de resolución está cortada/faltante, el agente registra **observación incluso cuando las páginas restantes aporten toda la información necesaria para el análisis**. Diferenciar indicio de incompletitud, incompletitud confirmada y documento no verificable; nunca atribuirlo automáticamente a un error OCR. Es un **criterio operativo explicado por el titular tras capacitación**, no fundamento normativo ya comprobado ni decisión administrativa automática.

## Criterios de aceptación

1. Identifica inequívocamente trámite, expediente y origen de cada evidencia; no usa el nombre del PDF para elegir el procedimiento.
2. Puede operar sin ejecutar `scripts/servidor_mcp.py` ni llamar `oece_coordinar`; no requiere índice normativo local.
3. Para expedientes, revisa documentos reales de Drive y conserva su ubicación, número de página, citas y, si puede, huella SHA-256; jamás inventa evidencia.
4. Cada cálculo tiene entradas, fórmula, resultado y segunda comprobación. Datos sin sustento = `null` / pendiente.
5. El CMC produce 01 → 02 → 03 más ficha maestra; consultores produce Word y matriz; resultados están **separados** y tienen revisión/fecha/estado.
6. Publica el resultado en Drive solo si realmente tiene permiso/herramientas; si no puede, entrega archivos o borradores disponibles y **declara expresamente que no los guardó en Drive**.
7. Pruebas unitarias de archivos comprueban instrucciones, **no sustituyen una prueba real** en ChatGPT, Claude o Grok.

## Estado

**Implementado en repo:** instrucciones y contratos agent-first. **Pendiente de verificación real:** carga de instrucciones en los tres clientes, acceso de cada cliente a la carpeta de expediente y normativa, ejecución de un caso sintético completo, generación de los archivos y guardado efectivo en Drive. **Python/MCP legado:** se conserva intacto y se puede seguir utilizando bajo demanda.
