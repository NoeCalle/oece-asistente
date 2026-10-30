# Roadmap
Actualización: 2026-10-30. Corte normativo investigado: 2026-10-29. Las fases se cierran por evidencia, no por número de archivos. [Estado general](docs/ESTADO.md).

| Fase | Estado | Entregables | Condición de salida |
|---|---|---|---|
| 0. Persistencia | Completada en esta entrega | Plan, arquitectura, tareas y estado real | Archivos guardados en GitHub y commit comprobado |
| 1. Biblioteca normativa | En curso; indexador textual implementado | Inventario, fuentes, fechas, relaciones, esquema y búsqueda | Originales con hash; modificatorias y vigencias revisadas; cobertura del piloto aprobada |
| 2. Procedimientos | Iniciada en paralelo con biblioteca | Fichas, requisitos, excepciones y matriz | Cada regla enlaza disposición vigente y evidencia; revisión del especialista |
| 3. Base técnica | Extracción/búsqueda y muestra OCR local; resto pendiente | Ingreso local/Drive sincronizado, persistencia, lector y OCR | Caso sintético de extremo a extremo; reanudación y aislamiento comprobados |
| 4. Piloto consultores | Pendiente | Evaluación de ampliación y borrador Word | Matriz y Word coherentes; citas verificadas y revisión humana |
| 5. Validación y expansión | Pendiente | Ejecutores, inscripciones, actualizaciones, reconsideraciones | Aceptación por módulo y regresión temporal/documental |

## Orden inmediato
1. Resolver discrepancias y vigencias condicionadas del inventario.
2. Descargar originales oficiales y anexos, verificar integridad y registrar hash.
3. Consolidar disposiciones del piloto y fichas del TUPA vigente.
4. Revisar matriz con especialista y construir expedientes sintéticos.
5. Integrar OCR con control de calidad y continuar ingreso/extracción; elegir runtime del coordinador antes de automatizar conclusiones.

Se aprobaron 12 pruebas técnicas: 8 del indexador y 4 de metadatos OCR. Se ejecutó OCR real en 3 páginas; integración y revisión de exactitud pendientes. Las pruebas del asistente completo siguen pendientes; no se ha recuperado el MVP anterior. No hay estimación de fecha de entrega hasta dimensionar documentos, formatos y conjunto de casos.
