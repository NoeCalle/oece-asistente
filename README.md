# OECE Assistant

Herramientas locales y coordinador en Codex para preparar evaluaciones documentales OECE/RNP con citas, matriz y borrador Word editable.

**Versión operativa asistida v1 — 31/10/2026.** Hay panel de expedientes, carga, lectura PDF/Word/HTML/XLSX, OCR con reanudación, selección de régimen de consultores, hechos citados y entregas versionadas. La conversación abierta y la interpretación se realizan en Codex siguiendo [AGENTS.md](AGENTS.md). El panel y la vigilancia son herramientas deterministas, sin modelo autónomo incorporado.

## Empezar

1. Abrir **INICIAR_OECE.cmd** en este equipo.
2. Crear expediente, elegir trámite e incorporar documentos.
3. Preparar el borrador y continuar su análisis en el chat de este proyecto con la ruta de la carpeta.
4. Descargar Word y matriz; cada revisión conserva originales y citas.

También puedes escribir en Codex: **«Revisa esta carpeta, el proveedor solicita ampliar su categoría y necesito el informe»**. El coordinador usa las herramientas y pide solo información que no encuentre. [Uso diario](docs/USO_DIARIO.md).

Los modelos reales de informes pueden incorporarse después. El [formato provisional](templates/informe.v1.json) está separado del circuito de evidencias.

## Alcance comprobado

| Componente | Estado |
|---|---|
| Ampliación de consultores | Selección temporal y por proveedor/experiencia; 22 verificaciones documentales sobre hechos citados; no concesión automática de categoría |
| CMC, inscripción/reinscripción, actualización y reconsideración | Recepción, lectura, evidencias, análisis asistido y Word; evaluadores sustantivos automáticos completos pendientes |
| Carpetas locales o Drive sincronizado | LISTO, estabilidad, bloqueo, revisiones y reintentos; archivos descargados |
| Panel local | Creación, ficha, carga, procesamiento y descarga Word comprobados en navegador |
| Conversación | Codex como coordinador; comandos guiados locales y memoria SQLite; sin integración automática nueva con un modelo |
| Lectura | PDF digital, DOCX con tablas/encabezados/pies, TXT/HTML y valores almacenados XLSX |
| OCR | Windows real, límites, caché y reanudación; cotejo declarado antes de apoyar hechos favorables |
| Entregas | Word provisional, CSV seguro, JSON trazable y revisiones; QA visual completa del Word v1 pendiente por bloqueo de exportación |
| Biblioteca | 29 registros y 47 archivos; cinco manifiestos; índice unificado local; cierre jurídico exhaustivo pendiente |
| Pruebas | 87 aprobadas, incluidas diez situaciones del piloto con hechos sintéticos; no precisión jurídica general |

El plan global sigue abierto. La versión asistida prepara borradores; no se declaran terminadas la evaluación autónoma de todos los módulos ni la aceptación institucional. [Estado y evidencia](docs/ESTADO.md). Estimación orientativa del plan completo: alrededor de **60 %**, no porcentaje de precisión.

## Documentación

- [Uso diario](docs/USO_DIARIO.md), [contrato de expediente](docs/CONTRATO_EXPEDIENTE.md) y [verificación v1](docs/VERIFICACION_V1.md).
- [Plan integral](docs/PLAN_INTEGRAL.md), [roadmap](ROADMAP.md), [tareas](docs/TAREAS.md), [cierres](docs/CIERRES.md) y [medición](docs/MEDICION_AVANCE.md).
- [Cinco criterios adoptados](docs/normativa/CRITERIOS_ADOPTADOS_PILOTO.md) y [criterios documentales ejecutados](rules/consultores/criterios-documentales.v1.json).
- [Biblioteca y TUO oficial](docs/normativa/OPERACION_V1.md), [catálogo](normativa/catalogo.json), [JSON Schema](schemas/norma.schema.json) y [seguridad](docs/SEGURIDAD.md).

## Datos y reproducción

Repositorio público: solo código, documentación, metadatos públicos y ejemplos sintéticos. Expedientes, informes, transcripciones e índices de trabajo van en `data/` o raíz privada, excluidos de Git. Esta copia está bajo OneDrive y puede sincronizarse con esa cuenta; usar una ubicación autorizada para documentos laborales. El programa no publica expedientes ni presenta trámites.

Dependencias y comandos en uso diario. La biblioteca binaria está fuera de Git; su reconstrucción requiere los originales conservados. Las pruebas crean documentos sintéticos locales.

```text
python -m unittest discover -s tests -p "test_*.py"
python scripts/verificar_biblioteca.py --verificar-originales
python -m oece biblioteca --reconstruir
python -m oece panel
```
