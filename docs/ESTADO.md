# Estado de OECE Assistant

## Aprendizaje operativo — integridad documental, 05/11/2026

**Regla afinada:** revisión de **páginas realmente escaneadas**, no corrección de errores de redacción. Se contrasta **foliación visible** (ej. `2/5 → 4/5`, ausencia de `3/5`), orden físico, continuidad material de párrafos entre hojas y recortes del escaneo. Registrar observación si hay omisión confirmada o indicio objetivo **aunque estén todos los datos sustantivos en las hojas restantes**. **Typos, faltas de ortografía, cláusulas mal numeradas y cambios de tema no son por sí solos hojas faltantes**; el OCR defectuoso tampoco. Diferenciar confirmado, indicio y no verificable, sin presumir consecuencia legal. Se actualizó coordinador, especialistas, entregables, prompt y [procedimiento](../procedimientos/control-integridad-documental.md). Prueba real con expedientes pendiente.

## Arquitectura principal agent-first — 05/11/2026

**Implementado en GitHub:** [coordinador](../agentes/coordinador.md), [especialista CMC](../agentes/especialista-cmc.md), [especialista consultores](../agentes/especialista-consultores.md), [consulta normativa](../agentes/consulta-normativa.md), [procedimientos y contratos](ARQUITECTURA_AGENTES.md), [prompt portable](PROMPT_OECE_UNIVERSAL.md) y [pruebas de aceptación](PRUEBAS_AGENTES.md). La modalidad preferida es **la IA de suscripción ejecutando roles por instrucciones**: normas y expedientes desde Drive, resultados a Drive, código/prompts en GitHub. **No requiere iniciar MCP, panel o Python** como paso obligatorio.

**Pendiente:** configuración/carga real de estas instrucciones y **validación completa en Codex, Claude y Grok Bot** con Drive, generación de archivos y escritura efectiva de resultados. Las pruebas estáticas verifican los archivos, no la experiencia real del cliente. Las tres plantillas CMC nativas siguen pendientes; **no** se simula entrega de formato oficial.

**Respaldo opcional:** el sistema Python/MCP versión 1.6 se conserva sin eliminar sus rutas, cálculos, controles y pruebas. Los párrafos históricos de abajo documentan ese motor **local**, no limitan el nuevo modo agent-first. La gestión de dudas automática entre agentes sigue pendiente (T53).

## Estado heredado — motor Python/MCP

Actualización: **02/11/2026, America/Lima**. Versión **1.6.0**. Preparación técnica comprobada para elaborar borradores con el asistente conversacional. [Primer uso](PRIMER_USO.md), [verificación](VERIFICACION_V16.md), [plan](PLAN_INTEGRAL.md).

## Resultado disponible

Los cinco trámites producen lectura, matriz y Word con hechos citados, autoría y revisiones conservadas: ampliación de consultores, aumento CMC, inscripción/reinscripción, actualización y reconsideración. El asistente interpreta documentos y fuentes; las herramientas ejecutan lectura/OCR, controles, cálculos y generación. El panel no incorpora un modelo autónomo ni requiere una API propia.

La preparación documental cubre 124 unidades, con 153 citas en cinco originales: trece fichas de inscripción, supuestos de actualización y requisitos del recurso, además de ampliación/aumento. Cada unidad conserva condiciones y alternativas. El plan no acredita por sí solo cumplimiento. [Registro](../rules/requisitos.v1.6.json).

Disponibles: panel, carpeta LISTO, memoria, diagnóstico, respaldos y recuperación en carpeta nueva. El puente MCP ofrece catorce herramientas. Codex es el cliente actual; la sesión real de otro cliente se comprueba al configurarlo con sus permisos. [Portabilidad](PORTABILIDAD_IA.md).

## Evidencia de preparación

- **220 pruebas aprobadas**, incluidas ramas, citas/recortes, datos desconocidos, diagnóstico y recuperación.
- Cinco expedientes ficticios nuevos con Word, matriz y plan; recuperación de consultores y de inscripción con informe íntegro.
- Navegador Edge con creación, carga, ficha, procesamiento, descarga y diagnóstico visible; cero errores JavaScript observados.
- Ocho comprobaciones técnicas satisfactorias y OCR Windows disponible. El diagnóstico distingue esto de la revisión normativa por fecha.
- Biblioteca activa: **48 originales, 29 registros, seis manifiestos**. Índice de 2.281 fragmentos, 2.046 con texto; nueve archivos con alertas/lectura parcial.
- QA visual histórica: cinco Word 1.1/19 páginas, dos Word financieros 1.2/diez páginas y un Word CMC 1.5/seis páginas inspeccionados. Los cinco nuevos Word 1.6 se comprobaron estructuralmente; el de actualización con cita del Anexo 5 se renderizó e inspeccionó en tres páginas. Los otros cuatro no reciben esa QA visual por herencia.

La corrección CMC con experiencia/AC positivo/PC cero de 9.2.6.d está incorporada. La solvencia conserva un análisis separado: ratios, SBS documentada, riesgos y contradicciones. [Contrato financiero](CONTRASTE_FINANCIERO.md).

## Inicio laboral y límites

**Personalización:** recibir el formato autorizado y ajustar presentación/redacción. La plantilla provisional permite empezar.

**Primer uso real:** confirmar ubicación/permisos, procesar un expediente autorizado y contrastar interpretaciones con originales y práctica del área. No se afirma aceptación institucional por haber pasado casos ficticios.

**Normativa:** corte **31/10/2026**. Las cuatro ramas adicionales conservan ventana 01/05–31/10/2026; consultores conserva J01–J05. Una fecha posterior exige revisar fuentes, modificatorias y reglas antes de ampliar conclusiones. El nuevo intento de lectura del compendio de El Peruano produjo errores y no amplió el corte.

La cadena completa por disposición, excepciones y casos históricos del plan amplio sigue abierta. El coordinador puede completar análisis específicos con citas; no se declara evaluación jurídica exhaustiva. DOC/XLS antiguos, imágenes incrustadas y algunas fuentes escaneadas mantienen sus límites. [Uso diario](USO_DIARIO.md).

## Actualización complementaria — 05/11/2026

**Actualización de alcance:** OECE Consulta Normativa funciona mediante la **conexión Google Drive del cliente de IA (ChatGPT, Claude o Grok Bot)**. El titular pregunta directamente, sin expediente, sin descargar la biblioteca ni necesitar índice local o API extra. Se busca primero en Drive; si no hay sustento suficiente, **se avisa antes de buscar en internet** y se identifican las fuentes externas. `oece_consultar_normativa` solo devuelve el plan para el cliente; **no ejecuta la conexión Drive**. El puente mantiene **21 herramientas**. [Contrato](CONSULTA_NORMATIVA.md).

**Alcance acotado:** no se añadió invocación desde especialistas CMC/consultores ni se resolvió aún el protocolo de dudas de expediente. Esta segunda fase queda registrada en T53. La biblioteca local y la vigencia jurídica no se vuelven actuales automáticamente al actualizar el repositorio.

## Medición y continuidad

La preparación técnica es distinta de completar el plan amplio de automatización. Se conserva su estimación orientativa **75 % (70–80 %)**; no es precisión jurídica. [Método](MEDICION_AVANCE.md).

Continuidad guardada en [tareas](TAREAS.md), [cierres](CIERRES.md) y [ejecución 1.6](../proyecto/ejecuciones/preparacion-v16-2026-11-01.json). La siguiente aportación del usuario es el modelo laboral y el primer expediente autorizado cuando corresponda. Las fuentes se mantienen según sus fechas.
