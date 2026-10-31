# Tareas persistentes
Actualización: 2026-10-31. Se usan tareas en Git para mantener la continuidad sin depender de issues ni del chat. [Estado general](ESTADO.md).

| ID | Prioridad | Estado | Trabajo y evidencia de cierre |
|---|---|---|---|
| T01 | P0 | Hecho | Inspeccionar repositorio y conservar estado real en README/bitácora |
| T02 | P0 | Hecho | Plan, arquitectura, roadmap y separación de datos |
| T03 | P0 | En curso | 29 registros; mínimo de adquisición v0.1 comprobado. Cobertura normativa exhaustiva y vigencias siguen abiertas |
| T04 | P0 | En curso | DS 001: inicio 14/01 documentado; J01/J02 adoptados con límites. Quinta DCM condicionada, sin bloqueo de toda Ley 32732; fronteras concretas pendientes |
| T05 | P0 | En curso general | 47 archivos con hash y copias en Drive; adquisición mínima de 36 cerrada en T28. Nuevas fuentes solo con necesidad/versiones identificadas |
| T06 | P0 | Pendiente | Consolidar cadena Ley 32069, reglamento, TUPA y directiva hasta corte |
| T07 | P0 | Pendiente | Revisar TUO LPAG 2026, numeración y efecto en recursos |
| T08 | P0 | En curso | Anexos leídos; 22 controles candidatos y 10 casos sintéticos especificados; falta revisión del especialista |
| T09 | P1 | Pendiente | Definir carpeta privada, permisos institucionales, modelo y retención |
| T10 | P1 | En curso | v1: ingreso por panel/carpeta LISTO, memoria SQLite y coordinador en Codex; modelo autónomo integrado al panel pendiente |
| T11 | P1 | En curso | v1: lector PDF/DOCX/TXT/HTML/XLSX y OCR de expedientes acotado; DOC/XLS e imágenes incrustadas requieren conversión o cotejo |
| T12 | P1 | En curso | Motor documental v1 de 22 controles con citas y Word; no decisión administrativa ni precisión jurídica certificada |
| T13 | P1 | En curso | 87 pruebas aprobadas y DOCX v1 generado/abierto; exportación PDF bloqueada, QA visual completa v1 pendiente; Word histórico de 4 páginas no la sustituye |
| T14 | P2 | Pendiente | Expandir ejecutores, inscripciones, actualizaciones y reconsideraciones |
| T15 | P2 | Pendiente | Evaluar recuperación de MVP anterior si se obtiene ZIP; auditar antes de reutilizar |
| T16 | P1 | Hecho en alcance técnico | Indexador local PDF/DOCX, búsqueda textual, hashes y ocho pruebas técnicas |
| T17 | P1 | En curso | OCR: preparador, motor Windows y verificación de derivados; muestra de 3 páginas con errores observados |
| T18 | P1 | En curso | Diagnóstico OCR en 4 regiones y alertas de identificadores críticos implementados; integración candidata de 3 páginas comprobada; ampliar muestra y timeout/reanudación pendientes |
| T19 | P1 | Parcial | HTML y valores XLSX implementados; XLS antiguo y fórmulas sin recalcular conservan límites |
| T20 | P1 | Pendiente | Segmentación por disposición y selección temporal |
| T21 | P1 | Hecho | Resumen central de estado del proyecto, enlazado a roadmap y evidencias |
| T22 | P1 | Hecho, actualizado | Estimación orientativa con pesos y evidencia; global alrededor de 60 % |
| T23 | P1 | Hecho en alcance sintético | Circuito entrada → lectura → matriz → Word, revisiones conservadas y doce pruebas; [evidencia](PILOTO_DOCUMENTAL.md) |
| T24 | P1 | Hecho en alcance v0.1 | Propuesta textual para siete controles, citas/huellas exactas, pendientes por defecto y cobertura restante explícita |
| T25 | P1 | Hecho en alcance sintético | Aceptación/rechazo explícitos, lotes vigentes, revisión en carpeta separada, revocación y comprobación de citas en matriz |
| T26 | P1 | Sustituida para v1 | Codex registra hechos interpretados con citas para el motor; no se amplían patrones léxicos como si fueran comprensión semántica |
| T27 | P1 | Hecho en alcance acotado | OCR de imágenes/PDF, máximo diez intentos y 120 s por lote, 45 s por página; caché y cotejos declarados; dos recorridos reales comprobados |
| T28 | P0 | Hecho en alcance v0.1 | Adquisición de 36 documentos en siete grupos verificada; 17 archivos nuevos y 240 páginas; [cierre y pendientes](normativa/COBERTURA_MINIMA_PILOTO.md) |

| T29 | P0 | Hecho en alcance de decisión | Cinco criterios adoptados por asistente IA con fuentes y excepciones; [fundamento](normativa/CRITERIOS_ADOPTADOS_PILOTO.md). No implementa ni habilita los 22 controles |

| T30 | P0 | Hecho en alcance asistido | Panel, coordinador en Codex, memoria SQLite, LISTO, lectura y entregas versionadas; sin modelo autónomo incorporado al panel |
| T31 | P0 | Hecho en alcance digital | Biblioteca unificada: 47 fuentes, 2.280 fragmentos, 2.045 con texto; fuente oficial TUO y numeración de recursos cotejadas |
| T32 | P0 | Hecho en alcance documental | Motor v1 separado del candidato histórico; diez situaciones ejecutadas y 34 pruebas nuevas, sin aceptación institucional |
| T33 | P1 | Pendiente de ejemplos del trabajo | Adaptar estructura y redacción Word a modelos reales autorizados; formato provisional disponible |
| T34 | P0 | Pendiente por entorno | Completar render y QA visual de Word v1; exportaciones Word bloqueadas en este equipo. Ver VERIFICACION_V1.md |

## Dependencias
T04–T08 bloquean conclusiones normativas automatizadas del piloto. T09 bloquea documentos reales; se puede desarrollar con sintéticos. T10–T11 pueden empezar después de definir contratos de datos, sin esperar todos los módulos.

## Próxima sesión
Leer [cierres y próximos bloques](CIERRES.md). T24, T25 y T28 están cerradas en su alcance explícito. T29 fija los cinco criterios; priorizar su traducción a reglas y pruebas, TUPA por rama y cotejo TUO; después T27/coordinador con sintéticos. Antecedente: había 53 pruebas técnicas y diez casos solo especificados. V1 tiene 87 y S01–S10 implementados sobre hechos sintéticos. Mantener tareas con fuente y evidencia. Si se crean issues después, enlazar estos IDs para evitar duplicación.


## Orden vigente de v1
La continuación anterior queda como antecedente. T29 se tradujo a motor documental en T32; T30 implementó operación asistida y T31 índice unificado. T10/T11/T17/T18/T19/T20/T27 tienen cobertura nueva en oece/, pero conservan las excepciones de lectura y OCR descritas en USO_DIARIO.md. T26 de ampliar perfiles léxicos deja de ser prioridad del MVP: Codex propone y registra hechos con citas, sin fingir extracción automática semántica en el panel. T07 tiene fuente oficial y numeración de recursos cotejadas; reglas especiales y cómputo del caso siguen requiriendo análisis. El plan de los módulos adicionales sigue abierto: modo documental asistido no es evaluador automático completo. Resolver T34 y aceptar el piloto; T33 espera los modelos que aporte el usuario al empezar su trabajo.
