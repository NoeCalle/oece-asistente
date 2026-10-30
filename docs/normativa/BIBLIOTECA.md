# Biblioteca documental: primera carga
Fecha de trabajo: 2026-10-29, America/Lima.

## Organización
GitHub conserva plan, metadatos, fuentes públicas y hashes. Google Drive conserva documentos en OECE Assistant / 01 Biblioteca normativa / Originales - recopilacion 2026-10-29. Se mantiene una copia local en normativa/originales/2026-10-29, excluida de Git. No se configuró sincronización automática ni se cargaron expedientes.

## Contenido: 23 archivos
- Directiva RNP 001-2025-OECE/CD y nueve anexos, conservando PDF/Word/Excel originales.
- Ley 32069 consolidada por OECE con corte declarado al 19/07/2026.
- Reglamento consolidado con corte declarado al 09/01/2026; no incluye por ese motivo la modificación de octubre.
- Ley 32732; DS 001-2026-EF; RD 001-2026-EF/54.01; DS 009-2025-EF y fe de erratas; DS 222-2026-EF.
- DS 006-2026-JUS: archivo de cuatro páginas del decreto aprobatorio, y separata de 48 páginas.
- TUPA base 2025, actualización 002-2026 y modificación 073-2026.

El PDF de la separata de Ley 27444 está alojado en gob.pe, pero su nombre incluye referencia a LPDerecho. Se conserva como copia de procedencia declarada, pendiente de cotejar con la publicación primaria. No confundir alojamiento oficial con validación de firmas. El archivo MINJUS de cuatro páginas no equivale al TUO íntegro.

## Verificación efectuada
SHA-256 calculado sobre cada descarga. Trece PDFs del lote inicial se abrieron con pypdf y se contaron páginas; la separata adicional también se abrió (48 páginas). Los siete DOCX/XLSX pasaron comprobación ZIP y manifiesto Office; los dos XLS solo comprobaron cabecera OLE. Esto no certifica fórmulas, contenido completo, firmas ni ausencia de defectos visuales.
La extracción PDF produjo advertencias de referencias internas en algunos archivos: se conservaron los originales sin reparar. Es necesario revisar visualmente las páginas utilizadas como evidencia y localizar los avisos por archivo antes de habilitar reglas.
Los 23 documentos se comprobaron por listado de Drive, IDs y tamaño frente al manifiesto local. No se volvió a descargar cada copia de Drive para comparar hash.

## Hallazgos y pendientes
La descarga directa recuperó fuentes que antes devolvían 403/418. El compendio también enlaza Ley 32185: incorporarla a la investigación antes de considerar cerrada la cadena.
Se obtuvo el original de la resolución de bases estándar de enero de 2026. Falta documentar el cotejo de su publicación y la disposición de vigencia del DS 001-2026-EF.
La condición de Ley 32732 aún requiere análisis del acto habilitante. Mantener deshabilitadas las reglas.
Completar originales de Ley 32069, 32103, 32185, 32187, 32515, DL 1715, FUP, ROF y actos aprobatorios del TUPA; comprobar si existen cambios posteriores. El manifiesto distingue consolidaciones, anexos, originales y copias.

## Evidencia persistente
[Manifiesto de descargas](../../normativa/manifiesto-descargas-2026-10-29.json): URL de origen, tipo de archivo, tamaño, SHA-256 y comprobación realizada. El índice con enlaces privados de Drive se guarda dentro de la biblioteca, no en este repositorio público.

## Continuación registrada el 30/10/2026
Captura HTML del Comunicado 001-2026-OECE añadida a Drive (23 archivos iniciales + 1 captura). Su imagen vinculada es una portada. [Manifiesto complementario](../../normativa/manifiesto-continuacion-2026-10-30.json). Revisión visual: DS 001 p.15, TUPA pp.31–32 y reglamento p.228. [Hallazgos](HALLAZGOS_PILOTO.md).

## Prototipo de índice local
Se implementó extracción de texto PDF y cuerpo/tablas DOCX, búsqueda por palabras y ubicación trazable. [Uso y límites](INDEXADOR_LOCAL.md). XLS, XLSX y HTML siguen archivados sin extracción; las páginas sin texto suficiente requieren OCR o revisión. La indexación no valida vigencia.
