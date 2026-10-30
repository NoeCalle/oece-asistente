# Resultado del indexador local
Ejecución: 30/10/2026. Corpus: `22f64ccec9226ee225a72696d09535125a6fc433a230a8af8bcdc876a935b80e`.

## Resultado comprobado
24 archivos registrados. 1.278 fragmentos conservados por ubicación, de los cuales **940 contienen texto**. Los fragmentos vacíos se conservan para identificar páginas pendientes; no se cuentan como contenido recuperado.

| Estado | Archivos | Interpretación |
|---|---|---|
| Extraído con revisión pendiente | 14 | Lectura textual disponible; no validación jurídica |
| Extracción parcial | 2 | TUPA modificado y actualizado, con 4 páginas de texto escaso cada uno |
| Requiere OCR o revisión | 2 | Reglamento original, 196 páginas; decreto aprobatorio TUO, 4 páginas |
| Formato pendiente | 6 | 3 XLSX, 2 XLS y captura HTML |

Los 2 archivos sin texto suficiente no se consideran leídos satisfactoriamente. Para investigación existen además consolidaciones/separata con texto, que deben cotejarse con sus fuentes.

## Pruebas
Ocho pruebas técnicas superadas: búsqueda con acentos; ubicaciones de tablas anidadas; integridad y conservación del índice anterior; cambio de fuente durante lectura; rechazo de ruta externa; deduplicación con procedencias; formato pendiente/error de lectura; PDF sin texto; consultas que no ejecutan operadores introducidos. Algunas pruebas cubren más de una condición.

Comprobación sobre biblioteca real: consulta `9.3.3`, filtro `ampliacion_consultores`, recuperó la directiva RNP en página PDF 12. Fuente, SHA-256 y corpus permanecen en el resultado. Esto comprueba recuperación de una referencia conocida; no mide exhaustividad ni precisión general.

[Reporte estructurado](../../normativa/indexacion/reporte-2026-10-30.json). [Guía para repetir](INDEXADOR_LOCAL.md).

## Límites y siguiente paso
Los diez casos jurídicos continúan como especificación no ejecutada. OCR, lectores HTML/Excel, segmentación por disposición, selección temporal, interpretación de requisitos y aplicación conversacional siguen pendientes.
Primero resolver el tratamiento de PDFs escaneados y probar recuperación de varias referencias con páginas esperadas. En paralelo completar modificatorias y criterios de transición. No habilitar la matriz jurídica por el hecho de disponer de búsqueda textual.
