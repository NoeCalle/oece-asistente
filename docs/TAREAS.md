# Tareas persistentes
Actualización: 2026-10-31. Se usan tareas en Git para mantener la continuidad sin depender de issues ni del chat. [Estado general](ESTADO.md).

| ID | Prioridad | Estado | Trabajo y evidencia de cierre |
|---|---|---|---|
| T01 | P0 | Hecho | Inspeccionar repositorio y conservar estado real en README/bitácora |
| T02 | P0 | Hecho | Plan, arquitectura, roadmap y separación de datos |
| T03 | P0 | En curso | 29 registros; mínimo de adquisición v0.1 comprobado. Cobertura normativa exhaustiva y vigencias siguen abiertas |
| T04 | P0 | En curso | DS 001: inicio 14/01 documentado; J01/J02 adoptados con límites. Quinta DCM condicionada, sin bloqueo de toda Ley 32732; fronteras concretas pendientes |
| T05 | P0 | En curso general | 46 archivos con hash y copias en Drive; adquisición mínima de 36 cerrada en T28. Nuevas fuentes solo con necesidad/versiones identificadas |
| T06 | P0 | Pendiente | Consolidar cadena Ley 32069, reglamento, TUPA y directiva hasta corte |
| T07 | P0 | Pendiente | Revisar TUO LPAG 2026, numeración y efecto en recursos |
| T08 | P0 | En curso | Anexos leídos; 22 controles candidatos y 10 casos sintéticos especificados; falta revisión del especialista |
| T09 | P1 | Pendiente | Definir carpeta privada, permisos institucionales, modelo y retención |
| T10 | P1 | En curso | Ingreso explícito sintético, huellas, revisiones y entrega íntegra implementados; faltan runtime y estado conversacional |
| T11 | P1 | En curso | Biblioteca PDF/Word y OCR candidato; lector de expedientes TXT/PDF/DOCX; falta OCR integrado de expedientes |
| T12 | P1 | En curso | Demostración documental con matriz de 22 controles y Word; falta evaluación jurídica aprobada |
| T13 | P1 | En curso | Word anterior de 4 páginas revisado; 53 pruebas técnicas aprobadas; aceptación jurídica pendiente |
| T14 | P2 | Pendiente | Expandir ejecutores, inscripciones, actualizaciones y reconsideraciones |
| T15 | P2 | Pendiente | Evaluar recuperación de MVP anterior si se obtiene ZIP; auditar antes de reutilizar |
| T16 | P1 | Hecho en alcance técnico | Indexador local PDF/DOCX, búsqueda textual, hashes y ocho pruebas técnicas |
| T17 | P1 | En curso | OCR: preparador, motor Windows y verificación de derivados; muestra de 3 páginas con errores observados |
| T18 | P1 | En curso | Diagnóstico OCR en 4 regiones y alertas de identificadores críticos implementados; integración candidata de 3 páginas comprobada; ampliar muestra y timeout/reanudación pendientes |
| T19 | P1 | Pendiente | Lectores HTML/Excel |
| T20 | P1 | Pendiente | Segmentación por disposición y selección temporal |
| T21 | P1 | Hecho | Resumen central de estado del proyecto, enlazado a roadmap y evidencias |
| T22 | P1 | Hecho, actualizado | Estimación orientativa con pesos y evidencia; global alrededor de 35 % |
| T23 | P1 | Hecho en alcance sintético | Circuito entrada → lectura → matriz → Word, revisiones conservadas y doce pruebas; [evidencia](PILOTO_DOCUMENTAL.md) |
| T24 | P1 | Hecho en alcance v0.1 | Propuesta textual para siete controles, citas/huellas exactas, pendientes por defecto y cobertura restante explícita |
| T25 | P1 | Hecho en alcance sintético | Aceptación/rechazo explícitos, lotes vigentes, revisión en carpeta separada, revocación y comprobación de citas en matriz |
| T26 | P1 | Pendiente | Ampliar perfiles documentales a los quince controles restantes con referencias de prueba definidas |
| T27 | P1 | Pendiente | Integrar OCR de expedientes con trazabilidad, timeout y reanudación; coordinar con T11/T18 |
| T28 | P0 | Hecho en alcance v0.1 | Adquisición de 36 documentos en siete grupos verificada; 17 archivos nuevos y 240 páginas; [cierre y pendientes](normativa/COBERTURA_MINIMA_PILOTO.md) |

| T29 | P0 | Hecho en alcance de decisión | Cinco criterios adoptados por asistente IA con fuentes y excepciones; [fundamento](normativa/CRITERIOS_ADOPTADOS_PILOTO.md). No implementa ni habilita los 22 controles |

## Dependencias
T04–T08 bloquean conclusiones normativas automatizadas del piloto. T09 bloquea documentos reales; se puede desarrollar con sintéticos. T10–T11 pueden empezar después de definir contratos de datos, sin esperar todos los módulos.

## Próxima sesión
Leer [cierres y próximos bloques](CIERRES.md). T24, T25 y T28 están cerradas en su alcance explícito. T29 fija los cinco criterios; priorizar su traducción a reglas y pruebas, TUPA por rama y cotejo TUO; después T27/coordinador con sintéticos. Hay 53 pruebas técnicas aprobadas; los diez casos jurídicos siguen sin ejecutar. Mantener tareas con fuente y evidencia. Si se crean issues después, enlazar estos IDs para evitar duplicación.
