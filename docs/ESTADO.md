# Estado de OECE Assistant

Actualización: **31/10/2026, America/Lima**. Versión operativa asistida **v1.0.0**. [Uso diario](USO_DIARIO.md), [verificación](VERIFICACION_V1.md) y [plan integral](PLAN_INTEGRAL.md).

## Resultado disponible

Se puede crear un expediente en el panel, cargar documentos, preparar lectura, matriz y Word, y continuar el análisis conversando en Codex. Hay originales y revisiones conservados, hechos con citas y autor identificado, cotejos OCR declarados y memoria SQLite. El formato provisional puede adaptarse después a modelos laborales reales.

El panel no incorpora un modelo autónomo. La interpretación abierta se hace en Codex; la vigilancia LISTO prepara un borrador documental, sin iniciar por sí sola un análisis libre de IA. No se añadió una API nueva ni se verificó un servicio institucional.

## Evidencia de la entrega

- **87 pruebas aprobadas:** 53 anteriores y 34 de operación v1. Incluyen S01–S10 con hechos sintéticos, citas alteradas, fronteras, comprobantes, consorcios, RUC extranjero, OCR y conservación.
- Navegador real: creación, ficha, carga, procesamiento y descarga Word; cero errores de JavaScript observados. Token, origen y rutas también probados por HTTP.
- OCR real Windows de una página pública: 3.392 caracteres, sin confianza inventada, pendiente de cotejo visual. Timeout, reanudación y transcripción declarada con imagen/autor se prueban por separado.
- **47 archivos y 29 registros**, con edición oficial MINJUSDH del TUO actualizada al 08/07/2026. Artículos 207–208, PDF pp. 193–194, cotejados visualmente.
- Ejemplo sintético: cuatro originales, doce hechos citados, diferencia de PEN 20.000 en honorarios y obligaciones de consorcio faltantes. Word y matriz quedan conservados por revisión.
- Word generado y abierto mediante automatización. Exportación PDF bloqueada en este equipo: QA visual de todas las páginas pendiente; no se declara verificado el diseño final.

## Estado por fase

| Fase | Disponible | Pendiente real |
|---|---|---|
| Plan | Persistente y actualizado | Mantenimiento |
| Biblioteca | Mínimo adquirido, fuentes ampliadas e índice unificado | Cadena por disposición, cambios posteriores, escaneados y formatos antiguos |
| Procedimientos | J01–J05 adoptados; motor documental de consultores y diez situaciones ejecutadas | Excepciones temporales, TUPA por rama y evaluadores sustantivos de otros módulos |
| Base técnica | Panel, memoria, LISTO, revisiones, lectura y OCR acotado | Modelo autónomo integrado si se elige ese despliegue; autenticación para servicio institucional compartido |
| Piloto | Flujo asistido carpeta a Word/CSV/JSON ejecutado | Modelos reales, aceptación funcional y validación con casos autorizados |
| Expansión | Cuatro módulos adicionales en modo documental asistido | Reglas y cálculos automáticos completos de cada procedimiento |

## Funcionamiento adoptado

Codex es el coordinador de este proyecto; [AGENTS.md](../AGENTS.md) dirige el trabajo. Python ejecuta operaciones locales y genera Word. La carpeta predeterminada es `data/operacion`, excluida de Git, dentro de esta ubicación OneDrive; se admite otra raíz autorizada o Drive sincronizado con archivos descargados. El motor local no transmite documentos a un servicio nuevo.

Los [criterios documentales v1](../rules/consultores/criterios-documentales.v1.json) están separados de la matriz candidata histórica v0.1. Cumple/no cumple se limita al control documental y a los hechos citados; no concede categoría ni prueba autenticidad. La autoría IA no se registra como humana. Los otros módulos no heredan reglas de consultores.

## Continuación

1. Usar el piloto asistido con un expediente autorizado y ajustar las observaciones a la necesidad funcional.
2. Incorporar los modelos de informes que el usuario reciba al empezar su trabajo y adaptar la plantilla.
3. Continuar el alcance amplio: excepciones normativas y evaluadores de ejecutores, inscripciones, actualizaciones y reconsideraciones. Esta expansión es distinta del ajuste de formato.

**Avance global orientativo: alrededor de 60 % (55–65 %)**. Hay versión asistida disponible; no se afirma que solo falte un formato para completar toda la automatización. [Criterios de estimación](MEDICION_AVANCE.md).
