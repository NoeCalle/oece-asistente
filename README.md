# OECE Assistant

Asistente proyectado para preparar evaluaciones documentales y borradores de informes OECE/RNP, con revisión del especialista.

**Estado al 31 de octubre de 2026 (America/Lima): adquisición documental mínima v0.1 comprobada, biblioteca buscable y circuito sintético con matriz y Word. El coordinador conversacional y la evaluación jurídica siguen pendientes.** El MVP mencionado en una conversación anterior no se encontró ni se verificó al inspeccionar el repositorio.

**Avance global orientativo: 35 % (rango 30–40 %).** [Cómo se estima](docs/MEDICION_AVANCE.md). **[Estado actualizado](docs/ESTADO.md)** — fases, evidencia y continuación.

## Objetivo

Cargar un expediente en una carpeta local o Google Drive sincronizado, conversar con un coordinador y obtener un borrador Word, una matriz de evaluación y referencias verificables. El primer módulo será ampliación de categorías de consultores de obras; después, aumento de capacidad máxima de contratación de ejecutores, inscripciones/reinscripciones, actualizaciones y reconsideraciones.

**Cierre documental T28:** 36 archivos requeridos en siete grupos, verificados dentro de un alcance explícito. Biblioteca total: **46 archivos en Drive y 29 registros**. Índice anterior con 1.184 fragmentos con texto, más un complemento separado de 212. [Qué se cerró y qué falta](docs/normativa/COBERTURA_MINIMA_PILOTO.md). No se certifica exhaustividad ni vigencia jurídica.

**Piloto documental ejecutado:** circuito sintético con matriz y Word anterior de cuatro páginas revisadas visualmente. Propone coincidencias para siete controles y permite aceptar/rechazar con citas verificadas, en otra carpeta y sin alterar la entrada. **53 pruebas técnicas aprobadas.** [Propuesta y revisión](docs/EVIDENCIAS_Y_REVISION.md). Los diez casos jurídicos siguen sin ejecutar y los 22 resultados permanecen `no_determinable`.

## Documentos del proyecto

- [Plan integral y arquitectura](docs/PLAN_INTEGRAL.md)
- [Roadmap y criterios de cierre](ROADMAP.md)
- [Tareas persistentes](docs/TAREAS.md)
- [Inventario normativo y alcance de verificación](docs/normativa/INVENTARIO.md)
- [Bitácora de fuentes, hallazgos y pendientes](docs/normativa/VERIFICACION.md)
- [Esquema de indexación temporal y trazabilidad](docs/normativa/INDEXACION.md)
- [Mapa inicial de procedimientos](docs/PROCEDIMIENTOS.md)
- [Matriz de evaluación y plan de pruebas](docs/EVALUACION_Y_PRUEBAS.md)
- [Circuito sintético y borrador Word](docs/PILOTO_DOCUMENTAL.md)
- [Cierres comprobados y próximos bloques](docs/CIERRES.md)
- [Cobertura mínima documental y cinco decisiones pendientes](docs/normativa/COBERTURA_MINIMA_PILOTO.md)
- [Propuesta textual y revisión de evidencias](docs/EVIDENCIAS_Y_REVISION.md)
- [Seguridad y separación de documentos](docs/SEGURIDAD.md)
- [Catálogo estructurado](normativa/catalogo.json) y [JSON Schema](schemas/norma.schema.json)

## Qué existe y qué falta

| Entregable | Estado |
|---|---|
| Plan, roadmap, tareas y arquitectura | Documentados |
| Inventario inicial con fuentes oficiales y fechas diferenciadas | Iniciado; cobertura parcial |
| Metadatos y esquema JSON | Creados |
| Indexación PDF/Word y búsqueda textual local | Prototipo implementado; [guía](docs/normativa/INDEXADOR_LOCAL.md) |
| Descarga y archivo en Drive | 46 archivos; mínimo v0.1 de 36 comprobado; cuatro manifiestos con SHA-256 |
| Consolidación por artículo y revisión jurídica | Pendiente |
| Lectura TXT, PDF digital y cuerpo/tablas de DOCX | Biblioteca y primer lector de expedientes sintéticos |
| OCR local de Windows | 3 páginas buscables en una capa candidata separada; [integración](docs/normativa/INTEGRACION_OCR.md) |
| OCR de lotes completos, coordinador y evaluación | Pendiente |
| Entrada sintética, revisiones, matriz y Word | Implementados y probados; revisión jurídica pendiente |
| Propuestas y revisión de evidencias | Perfil inicial de siete controles; decisiones explícitas, huellas/citas y revocación; [alcance](docs/EVIDENCIAS_Y_REVISION.md) |
| Carga documental a Drive | Realizada mediante conector; sin sincronización automática |
| API RNP o despliegue del asistente | No implementados |

**Repositorio público:** solo código, documentación del proyecto, metadatos de fuentes públicas y casos sintéticos. Expedientes, informes, credenciales y documentos de trabajo van fuera del repositorio. No subir el ZIP anterior sin inspeccionarlo y retirar datos reales.

No se certifica que el inventario cubra todas las modificatorias al corte. Una fuente encontrada no habilita por sí sola una regla de evaluación. Véanse los bloqueos de vigencia y de validación humana en la bitácora.

Para verificar metadatos y trazabilidad: `python scripts/verificar_biblioteca.py`. El modo `--verificar-originales` requiere las copias locales. [Resultados del piloto](docs/normativa/VALIDACION_PILOTO.md).
