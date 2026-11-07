# POE-CMC-PDF-01 — Resaltador nativo sobre PDF escaneados

**Fecha:** 2026-11-06. **Versión:** 2.0. **Estado:** viabilidad técnica del resaltado nativo confirmada con una prueba de PDF **100 % imagen, sin texto PDF ni OCR**; posicionamiento sobre contratos reales y comportamiento de corrección manual en Adobe Acrobat/Microsoft Edge del evaluador **pendientes de prueba**.

## Condiciones confirmadas por el evaluador

- **Asumir por defecto que prácticamente el 100 % de documentos del expediente son escaneos** (PDF compuesto por imágenes). No construir el procedimiento alrededor de texto seleccionable, búsqueda de cadenas, OCR ya incorporado ni selección de palabras en Acrobat. Si excepcionalmente existiera texto, no cambia la metodología base.
- **Prioridad absoluta al resaltador nativo de PDF, tipo `Highlight`**. El usuario no quiere cuadrados, rectángulos, autoformas o capas coloreadas añadidas sobre el contenido. El objetivo es lograr marcas como las de **Resaltar** de Acrobat o Edge.
- Seleccionar **solo las palabras, cifras o líneas concretas** utilizadas para completar el Excel, no un párrafo amplio salvo necesidad.
- **Color amarillo** por defecto; tolerancia a desfases mínimos que el evaluador revisará visualmente. No afirmar que una anotación Highlight sobre un escaneo se puede **arrastrar o redimensionar** igual que una autoforma en todos los visores: la posibilidad de editar sus cuadriláteros depende del programa. Si el visor no permite moverla, el usuario podrá borrar y volver a aplicar la marca.

## Viabilidad técnica confirmada

Con **PyMuPDF `Page.add_highlight_annot(quads)`** pueden crearse **anotaciones de tipo PDF `Highlight`** incluso cuando no existe ningún carácter de texto reconocible/seleccionable: la biblioteca documenta expresamente que puede «marcar cualquier cosa» proporcionando coordenadas `Rect`/`Quad`. La anotación es un objeto `/Subtype /Highlight`, no un cuadrado `/Square` y no se aplana. Referencia: https://pymupdf.readthedocs.io/en/latest/page.html

**Ensayo sintético ejecutado:** documento de una sola página generada con una **imagen raster como único contenido**; `page.get_text("text") == ""`, una imagen, **tres anotaciones PDF reales de tipo `(8, "Highlight")`** sobre contratista, monto y objeto. Al guardar y reabrir se confirmó la presencia de las tres marcas. Se comprobó su visualización en un render posterior; este resultado no garantiza interacción específica en Acrobat/Edge ni exactitud en documentos reales.

## Convención de autor y comentario (preferencia confirmada 06/11/2026)

- En **todas** las anotaciones nativas `Highlight`, establecer el campo **autor/título** exactamente como `Noe Calle` (no `OECE Assistant`).
- El campo de **comentario/contenido** contiene **solo el dato concreto**, presentado como etiqueta breve y valor, sin información adicional: `Monto contractual S/ 1 401 840.00`, `Contratista Consorcio Huaros`, `Participación 20%`. Usar únicamente valores encontrados y verificados; no inventar importes ni RUC no legibles.
- **Omitir expresamente** fórmulas de comentario como `Dato extraído:`, `Fuente:`, `Página PDF:`, `Marcación inicial para cotejo visual`, advertencias genéricas o cualquier texto de explicación. El PDF/página/obra/celda se conserva en la **trazabilidad privada**, no dentro del comentario visible.
- No afectar posición, color, extensión ni tipo de los resaltados al editar solo el autor/comentario. Si faltan elementos de valor, consignar únicamente lo que realmente esté sustentado.

**Validación ejecutada:** en el piloto de las primeras 10 páginas del PDF de experiencias se cambiaron **20** anotaciones `Highlight` a autor `Noe Calle` y comentarios cortos. Se comprobó que se conservaban número, tipo y geometría de anotaciones y que el render resultante era idéntico al anterior.

## Flujo de marcado en PDF escaneado — método único base

1. **Examinar la imagen de la página del PDF** donde se encuentra el dato (contratista, obra, monto, fecha, participación, etc.). La extracción documental del valor y la ubicación visual son tareas separadas; no asumir que el PDF se puede buscar por texto.
2. **Localizar la zona exacta de los caracteres sobre la imagen** mediante visión o una ayuda OCR temporal, si resulta útil; el OCR no es requisito ni fuente de verdad automática. Para evidencia dudosa, conservar `pendiente_cotejo`. Usar inspección visual a resolución suficiente, con ampliación cuando haga falta.
3. **Convertir coordenadas de imagen a PDF**, teniendo en cuenta la escala de renderizado, orientación, rotación y cropbox. Definir un `Quad` por fragmento/renglón o múltiples `Quads` si una frase ocupa más de una línea. Preferir cubrir solo la altura de los caracteres y un margen pequeño, evitando invadir renglones adyacentes.
4. **Crear anotaciones nativas `Highlight`** con `add_highlight_annot`, amarillo y opacidad moderada, manteniendo anotación sin aplanar. No utilizar por defecto `add_rect_annot`, `Square`, `Shape`, `Ink` ni una imagen amarilla como sustituto.
5. **Guardar copia `NOMBRE_RESALTADO.pdf`**, conservar el original intacto. Reabrirla y comprobar que las marcas aparecen como `Highlight` (no `Square`), con el mismo número de páginas y contenido.
6. **Verificación visual obligatoria:** renderizar y revisar cada página con marcas; comprobar que cubren exactamente el dato fuente y que no alteran el texto visible. Si alguna está desviada, recalcular/recrear coordenadas antes de entregar; identificar casos que aún requieran corrección manual.
7. **Compatibilidad de corrección manual:** abrir la copia en **Adobe Acrobat de escritorio y/o Edge** con el evaluador. Comprobar selección, eliminación y posibilidad real de reajuste de las anotaciones. No prometer arrastre/redimensionamiento de resaltado nativo en PDF imagen; si el visor no lo soporta, la corrección consiste en borrar y volver a resaltar.
8. **Trazabilidad:** mantener en registro privado `expediente → OB-## → archivo PDF concreto → página física 1-based → campo/celda Excel → valor → coordenadas y/o ID de anotación`. Cuando la revisión humana ajuste el PDF, conservar esa versión para siguientes iteraciones.

## Relación con entregables

1. **Excel MPR de evaluación** y 2. **Word de observaciones** siguen siendo **únicos entregables principales**. Los PDF resaltados son **copias auxiliares de sustento**, no un tercer formato administrativo obligatorio. Una observación por desfase gráfico no es una discrepancia contractual.
2. El campo `G` («inicial pág») del Excel corresponde a la página **del archivo PDF concreto**, no a una suma de páginas de todos los documentos; el expediente privado identifica el PDF y la anotación fuente.
3. Incorporar progresivamente los resaltados a cada contrato, acta y resolución recibido; no sobrescribir comentarios ni cambios manuales previos sin cotejo.

## Criterios de aceptación pendientes para piloto real

- En al menos una página de un contrato escaneado real, resaltar cinco fragmentos de distintos tamaños, incluido número pequeño, nombre largo y texto que cambia de línea.
- Comprobar visualmente cobertura sin tachar ni tapar información.
- Verificar el tipo `Highlight` y persistencia tras guardar/reabrir.
- Probar cómo funcionan las correcciones de marcas en Acrobat/Edge del evaluador.
- Registrar errores de alineación y ajustar el método antes de escalar a todos los contratos.

**Límites:** escaneos inclinados, perspectiva, baja resolución, letra borrosa, firmas superpuestas y límites técnicos de lectores PDF pueden requerir corrección manual. No inventar precisión 100 % ni implicar autenticidad documental por existencia del resaltado.
