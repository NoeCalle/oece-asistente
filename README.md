# OECE Assistant

Asistente proyectado para preparar evaluaciones documentales y borradores de informes OECE/RNP, con revisión del especialista.

**Estado al 29 de octubre de 2026 (America/Lima): planificación persistida y fase 1 iniciada. No hay aplicación operativa en este repositorio.** El repositorio inspeccionado contenía únicamente un README; el MVP y sus cuatro pruebas mencionados en una conversación anterior no se encontraron ni se verificaron.

## Objetivo

Cargar un expediente en una carpeta local o Google Drive sincronizado, conversar con un coordinador y obtener un borrador Word, una matriz de evaluación y referencias verificables. El primer módulo será ampliación de categorías de consultores de obras; después, aumento de capacidad máxima de contratación de ejecutores, inscripciones/reinscripciones, actualizaciones y reconsideraciones.

**Avance documental:** 23 archivos oficiales o copias alojadas en portales oficiales descargados y guardados en Google Drive. [Detalle de la biblioteca](docs/normativa/BIBLIOTECA.md). La revisión jurídica sigue pendiente.

## Documentos del proyecto

- [Plan integral y arquitectura](docs/PLAN_INTEGRAL.md)
- [Roadmap y criterios de cierre](ROADMAP.md)
- [Tareas persistentes](docs/TAREAS.md)
- [Inventario normativo y alcance de verificación](docs/normativa/INVENTARIO.md)
- [Bitácora de fuentes, hallazgos y pendientes](docs/normativa/VERIFICACION.md)
- [Esquema de indexación temporal y trazabilidad](docs/normativa/INDEXACION.md)
- [Mapa inicial de procedimientos](docs/PROCEDIMIENTOS.md)
- [Matriz de evaluación y plan de pruebas](docs/EVALUACION_Y_PRUEBAS.md)
- [Seguridad y separación de documentos](docs/SEGURIDAD.md)
- [Catálogo estructurado](normativa/catalogo.json) y [JSON Schema](schemas/norma.schema.json)

## Qué existe y qué falta

| Entregable | Estado |
|---|---|
| Plan, roadmap, tareas y arquitectura | Documentados |
| Inventario inicial con fuentes oficiales y fechas diferenciadas | Iniciado; cobertura parcial |
| Esquema JSON de metadatos | Creado; no es un indexador |
| Descarga y archivo en Drive | 23 archivos; manifiesto con SHA-256 |
| Consolidación por artículo y revisión jurídica | Pendiente |
| Coordinador, vigilancia de carpetas, lector/OCR y evaluación | Pendiente |
| Generador Word y pruebas de expedientes | Pendiente |
| Carga documental a Drive | Realizada mediante conector; sin sincronización automática |
| API RNP o despliegue del asistente | No implementados |

**Repositorio público:** solo código futuro, documentación del proyecto, metadatos de fuentes públicas y casos sintéticos. Expedientes, informes, credenciales y documentos de trabajo van fuera del repositorio. No subir el ZIP anterior sin inspeccionarlo y retirar datos reales.

No se certifica que el inventario cubra todas las modificatorias al corte. Una fuente encontrada no habilita por sí sola una regla de evaluación. Véanse los bloqueos de vigencia y de validación humana en la bitácora.
