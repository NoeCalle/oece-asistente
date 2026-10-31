# Biblioteca de la operación v1

## Fuentes conservadas

47 archivos y 29 registros. El mínimo anterior de 36 archivos sigue cerrado en su alcance. Se añadió la [edición oficial MINJUSDH del TUO](https://www.gob.pe/institucion/minjus/informes-publicaciones/8441836-primera-edicion-oficial-del-texto-unico-ordenado-de-la-ley-n-27444-ley-del-procedimiento-administrativo-general-aprobado-por-el-decreto-supremo-n-006-2026-jus-actualizada-al-8-07-2026), libro publicado 04/08/2026, actualizado editorialmente al 08/07/2026. No confundir esas fechas con publicación o vigencia del decreto.

[PDF oficial](https://cdn.www.gob.pe/uploads/document/file/10399631/8441836-tuo-ley-27444-ley-procedimiento-administrativo-general-julio-2026-ok.pdf?v=1785866517). [Manifiesto](../../normativa/manifiesto-operacion-2026-10-31.json): 243 páginas, 6.745.398 bytes y SHA256 `e29b8018d5d5c51bc02b4d59cb3f8802d72e3ac0c103abc6d63c3c2614e92195`. Archivado en Drive y localmente. La copia UGEL anterior con nombre LP Derecho se conserva como antecedente, no como cotejo primario suficiente.

## Recursos cotejados

PDF pp. 193–194 (impresas 191–192) leídas y renderizadas: artículo 207, recursos y términos con excepciones; artículo 208, reconsideración ante el mismo órgano, nueva prueba y excepción de única instancia, carácter opcional; artículo 211, requisitos del escrito. La numeración cotejada es 207/208, no una importación automática de 218/219 del TUO anterior.

El cómputo de un caso requiere acto, notificación, presentación, calendario, suspensiones y reglas especiales. No se presume nueva prueba por el título del anexo. J02 sigue delimitando la condición de quinta DCM de Ley 32732 para argumentos de prevalencia. El corte editorial 08/07 no acredita ausencia de cambios hasta 31/10.

También se obtuvo para diagnóstico el PDF de El Peruano (66 páginas), pero pypdf emitió errores de estructura/descompresión y no recuperó texto útil. Esa descarga diagnóstica no se añadió al inventario validado ni sustituyó la edición MINJUSDH.

## Índice unificado

`python -m oece biblioteca --reconstruir` incorpora cinco manifiestos a `normativa/indices/biblioteca-v1.sqlite`. Lee PDF digital, DOCX con encabezados/pies/tablas, HTML y valores almacenados XLSX. Omite celdas solo con estilo; fórmulas mantienen alerta de valor sin recalcular. No ejecuta macros, conexiones ni fórmulas.

Páginas sin texto suficiente conservan alertas; DOC/XLS antiguos y escaneados necesitan conversión/OCR. El OCR de expedientes usa un circuito acotado separado. La recuperación devuelve fuente, huella, localizador, texto y alertas, sin acreditar vigencia. Los índices anteriores se conservan como instantáneas. Cifras finales en [verificación v1](../VERIFICACION_V1.md).
