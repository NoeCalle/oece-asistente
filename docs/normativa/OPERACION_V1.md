# Biblioteca de la operación v1

## Fuentes conservadas

48 archivos y 29 registros; cierre de operación 1.1 del 01/11/2026, corte normativo 31/10/2026. El mínimo anterior de 36 archivos sigue cerrado en su alcance. Se añadió la [edición oficial MINJUSDH del TUO](https://www.gob.pe/institucion/minjus/informes-publicaciones/8441836-primera-edicion-oficial-del-texto-unico-ordenado-de-la-ley-n-27444-ley-del-procedimiento-administrativo-general-aprobado-por-el-decreto-supremo-n-006-2026-jus-actualizada-al-8-07-2026), libro publicado 04/08/2026, actualizado editorialmente al 08/07/2026. No confundir esas fechas con publicación o vigencia del decreto.

[PDF oficial](https://cdn.www.gob.pe/uploads/document/file/10399631/8441836-tuo-ley-27444-ley-procedimiento-administrativo-general-julio-2026-ok.pdf?v=1785866517). [Manifiesto](../../normativa/manifiesto-operacion-2026-10-31.json): 243 páginas, 6.745.398 bytes y SHA256 `e29b8018d5d5c51bc02b4d59cb3f8802d72e3ac0c103abc6d63c3c2614e92195`. Archivado en Drive y localmente. La copia UGEL anterior con nombre LP Derecho se conserva como antecedente, no como cotejo primario suficiente.

## Recursos cotejados

PDF pp. 193–194 (impresas 191–192) leídas y renderizadas: artículo 207, recursos y términos con excepciones; artículo 208, reconsideración ante el mismo órgano, nueva prueba y excepción de única instancia, carácter opcional; artículo 211, requisitos del escrito. La numeración cotejada es 207/208, no una importación automática de 218/219 del TUO anterior.

El cómputo de un caso requiere acto, notificación, presentación, calendario, suspensiones y reglas especiales. No se presume nueva prueba por el título del anexo. J02 sigue delimitando la condición de quinta DCM de Ley 32732 para argumentos de prevalencia. El corte editorial 08/07 no acredita ausencia de cambios hasta 31/10.

También se obtuvo para diagnóstico el PDF de El Peruano (66 páginas), pero pypdf emitió errores de estructura/descompresión y no recuperó texto útil. Esa descarga diagnóstica no se añadió al inventario validado ni sustituyó la edición MINJUSDH.

## Índice unificado

`python -m oece biblioteca --reconstruir` incorpora seis manifiestos a `normativa/indices/biblioteca-v1.sqlite`. Lee PDF digital, DOCX con encabezados/pies/tablas, HTML y valores almacenados XLSX. Omite celdas solo con estilo; fórmulas mantienen alerta de valor sin recalcular. No ejecuta macros, conexiones ni fórmulas.

Páginas sin texto suficiente conservan alertas; DOC/XLS antiguos y escaneados necesitan conversión/OCR. El OCR de expedientes usa un circuito acotado separado. La recuperación devuelve fuente, huella, localizador, texto y alertas, sin acreditar vigencia. Los índices anteriores se conservan como instantáneas. Cifras finales en [verificación v1](../VERIFICACION_V1.md).

## Ampliación 1.1

Se añadió el [folio gráfico SPIJ del artículo 28](https://spij.minjus.gob.pe/Graficos/Peru/2025/Enero/22/DS-009-2025-EF_01.pdf), enlazado desde el reglamento consolidado. Una página PDF, 773.495 bytes, SHA256 `b1296af49a7a2bc12eb41bbcac558510dbe40d38d20a646e85f6a75ba666896e`. Contiene la fórmula CMC = sumatoria de obras × G; G = a + f + e. Solo la fórmula fue adoptada: el texto antiguo de 25.7 del mismo folio no sustituye la modificatoria de 2026. [Sexto manifiesto](../../normativa/manifiesto-procedimientos-2026-10-31.json).

Se cotejaron además directiva RNP 9.2.5–9.2.6 (PDF pp. 7–9), remisiones 9.3.2–9.3.3 (p. 12), actualización 9.6 (pp. 13–14), reglamento 26/28/381 y TUO 133–135/207–208/211. Esto fundamenta los controles seleccionados, no la cadena normativa exhaustiva. [Fuentes por control](../../rules/procedimientos.v1.1.json).

Resultado unificado reconstruido: **48 fuentes, 2.281 fragmentos y 2.046 con texto**. Nueve archivos tienen alertas: escaneados, páginas con poco texto, XLS antiguo o fórmulas XLSX sin recalcular. [Reporte](../../normativa/indexacion/reporte-operacion-v11-2026-11-01.json). Búsqueda digital no equivale a norma vigente ni a lectura completa de esos archivos.
