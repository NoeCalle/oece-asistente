# Indexación normativa y temporal
Estado: diseño y esquema de metadatos creado; extracción e indexador no implementados.

## Tres objetos distintos
1. Instrumento: identidad jurídica estable (tipo + número + año + emisor + jurisdicción), título, publicación, emisión, relaciones y procedimientos.
2. Versión documental: fuente final, fecha de captura, hash SHA-256, formato, firma si se verificó, tamaño, idioma, ubicación privada y método de extracción. Una URL puede cambiar de archivo: el hash identifica la versión.
3. Disposición: artículo/numeral/literal/anexo, texto y ubicación, intervalo de eficacia, modificaciones que lo afectan y revisión humana. La vigencia del instrumento completo no basta.

El [catálogo](../../normativa/catalogo.json) implementa solo metadatos iniciales del instrumento. El [JSON Schema](../../schemas/norma.schema.json) fija esta fase: revisión humana null y apta_para_reglas=false. Para admitir reglas revisadas se requerirá una versión posterior del esquema, con acta/revisor/fecha y evidencia íntegra. No cambiar simplemente false a true.

## Campos y semántica
- fecha_emision: firma/aprobación; fecha_publicacion: diario oficial cuando se acredita; consultado_el: fecha de esta investigación. No intercambiables.
- vigencia.desde/hasta: intervalo por confirmar, con fundamento y estado. hasta se modelará como límite exclusivo en la capa de disposiciones.
- null: desconocido o no determinado; nunca equivale a vigente indefinidamente.
- estados: identificado_oficial, texto_oficial_consultado, vigencia_parcial_verificada, condicionada, en_conflicto, historico, orientacion, pendiente.
- relaciones: modifica, deroga, aprueba, reglamenta, actualiza, corrige; destino es otro ID del catálogo. Delimitar disposiciones y fecha efectiva antes de resolver temporalidad.
- procedimientos: identificadores internos, no códigos TUPA. Solo registrar código oficial después de cotejar ficha.
- archivo.sha256: null hasta descarga real. No derivarlo del enlace o del texto del buscador.

## Esquema previsto de un fragmento
fragment_id, instrument_id, document_version_id, article_path, page_pdf, page_printed, block_id, text, extraction_method, confidence, valid_from, valid_to, temporal_condition, source_url, sha256, review_id.
Para Word sin paginación estable, usar bloque/tabla/celda y una copia renderizada identificada por hash. Para OCR guardar coordenadas y referencia a imagen.

## Selección de norma para un expediente
1. Fijar fechas de solicitud, contratación/experiencia, notificación y acto impugnado según trámite.
2. Seleccionar régimen y normas transitorias; no usar automáticamente fecha actual ni fecha del contrato para todo.
3. Resolver cambios por disposición. Si hay condición no acreditada, intervalos en conflicto o cobertura insuficiente: no_determinable y revisión.
4. Recuperar fragmentos solo de versiones permitidas para esa fecha y procedimiento.
5. Congelar snapshot del corpus, reglas y fuentes en cada informe. Una actualización posterior crea nueva revisión.

## Cadena de trazabilidad
Conclusión → fila de matriz → regla y versión → hechos → archivo/hash/página → fragmento normativo/hash/disposición → fuente oficial.
Persistir también código/commit, modelo y versión de instrucciones, momento de ejecución, correcciones humanas y motivo. No publicar esa cadena cuando contenga datos de expediente.

## Ingestión a implementar
Descarga oficial → conservación original → hash → extracción → control de calidad → segmentación por disposición → relaciones temporales → revisión → índice textual → evaluación de recuperación → índice semántico opcional.
Las consolidaciones internas deben declararse como tales y enlazar todos los actos; conservar las versiones anteriores. Las orientaciones y proyectos normativos se indexan en colecciones separadas y no habilitan requisitos.

## Controles
Validación JSON Schema, IDs únicos, referencias existentes, fechas calendario válidas, dominio oficial, hash/archivo coherentes. Luego pruebas de intervalos, derogación parcial, vigencia condicionada, fe de erratas, fuente reemplazada y cambio de numeración. Validar estructura no valida contenido jurídico.
