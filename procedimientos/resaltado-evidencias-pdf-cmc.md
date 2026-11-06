# POE-CMC-PDF-01 — Resaltado editable de evidencias en PDF

**Fecha de adopción:** 2026-11-06. **Estado:** capacidad técnica verificada en prueba sintética; precisión y compatibilidad del lector del evaluador pendientes de validar en **un PDF escaneado real**. **Alcance:** apoyo de revisión visual para aumento de CMC. **Carácter:** copia auxiliar de evidencia, no sustitución del Excel MPR ni del Word de observaciones.

## Objetivo confirmado por el evaluador

Al extraer un dato de un contrato, acta o resolución, **marcar en amarillo la posición concreta del texto del que salió el valor** dentro de una **copia del PDF**. Procurar precisión máxima, pero permitir que el evaluador ajuste manualmente pequeños desfases de posición y tamaño en un editor compatible como Adobe Acrobat de escritorio.

## Técnica obligatoria para permitir mover y ajustar las marcas

- **Usar anotaciones PDF auténticas y editables**, por ejemplo **Square/Rectangle annotation** (anotación de dibujo con relleno amarillo semitransparente, borde ausente). No dibujar cuadrados de manera irreversible dentro del contenido de página, no aplanar/flatten y no rasterizar el PDF original para «simular» anotaciones.
- **No depender exclusivamente del marcador nativo de texto** (Highlight/quads), pues puede permanecer anclado a caracteres y no siempre admite arrastre libre de los bordes en Acrobat. Para este flujo, se prefieren anotaciones rectangulares tanto en PDFs escaneados como en PDFs con texto seleccionable; pueden coexistir técnicas si no se pierde editabilidad.
- Color por defecto `amarillo #FFFF00`; opacidad inicial orientativa `0.25–0.35` (ajustar tras inspección para que se lea bien). Sin contorno perceptible. Para frases en varias líneas, crear **una marca por tramo/renglón**, en vez de cubrir un bloque de texto innecesariamente amplio.
- El evaluador debe poder **seleccionar, arrastrar, redimensionar y borrar** las marcas desde la herramienta de comentarios/dibujo de un visor compatible. La disponibilidad concreta depende de la aplicación, permisos y configuración del PDF; **verificar con Adobe Acrobat de escritorio antes de prometer compatibilidad universal**. Adobe documenta el cambio de tamaño con tiradores de esquina de las anotaciones de dibujo: https://helpx.adobe.com/au/acrobat/desktop/share-and-review-documents/review-documents/add-shapes-drawings.html
- No crear PDF bloqueado/protegido ni una versión «aplanada» como única salida. Guardar **original intacto** y `NOMBRE_RESALTADO.pdf` en la carpeta privada autorizada del expediente.

## Procedimiento por documento y campo

1. **Lectura:** inventariar PDF y obra/expediente, comprobar número físico de páginas; leer la página y localizar el dato específico: contratista, nombre de obra, monto, fecha, porcentaje, etc. El PDF puede contener texto seleccionable o solo imagen escaneada. No inferir el valor de un nombre de archivo.
2. **Ubicación precisa:** para texto seleccionable, usar coordenadas de palabras/cajas de texto; para escaneo, localizar visualmente la región de la imagen y transformarla a coordenadas PDF respetando orientación, recorte, escala y rotación. OCR, cuando exista, es ayuda de posición, no fuente infalible; cotejar visualmente.
3. **Anotar:** crear únicamente anotaciones rectangulares semitransparentes sobre **las palabras o cifras exactas usadas**, con el menor margen legible; evitar tapar otros campos o líneas. Si hay duda de posición, declarar `pendiente_ajuste_visual` y no presentarla como exacta.
4. **Metadatos y trazabilidad:** asociar anotación a `obra_id`, `campo_excel`, `pdf_id/nombre`, `pagina_pdf_1_based` y `valor_extraido` en el registro privado; opcionalmente colocar una breve nota interna en la anotación, sin datos personales en GitHub. No deducir que la anotación constituye validación legal ni autenticidad.
5. **Verificación técnica:** reabrir la copia guardada, confirmar que mantiene sus páginas y contenido y que las marcas existen como **objetos de anotación PDF** (no imagen o pintura permanente). Renderizar original y copia y comparar visualmente **al menos las páginas anotadas**. Comprobar que cada rectángulo cubre el dato pretendido.
6. **Corrección del evaluador:** permitir mover/redimensionar marcas y guardar la copia en Acrobat de escritorio. Si se recibe una copia corregida, reutilizar la posición ajustada en revisiones futuras solo cuando corresponda al mismo PDF/versión/página; nunca trasladar coordenadas a otro documento por nombre similar.
7. **Coherencia con Excel y Word:** `Obras nacional` G contiene página física 1-based del **PDF específico**; mantener nombre/ID PDF en expediente privado. `J` contiene dato; `L` observación breve cuando corresponda. El Word consigna observaciones documentales; no se crea una observación de error solo porque un resaltado se movió un poco.

## Salida y control de alcance

- **Dos entregables principales vigentes**: 1) Excel MPR completo/actualizado; 2) Word editable de observaciones.
- **Copias PDF resaltadas:** **evidencia auxiliar opcional solicitada por el evaluador**, sin incorporarlas como «tercer entregable institucional». Puede haber una copia por contrato u otro documento donde se hayan extraído datos. Los PDF originales se mantienen intactos.
- En entregas progresivas, actualizar marcas de documentos revisados sin perder comentarios o ajustes manuales del evaluador. No eliminar ni regenerar anotaciones ajenas de un archivo corregido sin comparación previa.
- Restricciones: PDF protegido contra anotaciones, manuscritos ilegibles, baja resolución, inclinación extrema, texto superpuesto o anotaciones incompatibles con algún visor pueden requerir intervención manual. No afirmar exactitud 100 %.

## Evidencia de viabilidad técnica

Prueba local sintética en 2026-11-06: utilizando **PyMuPDF**, se creó una anotación PDF de tipo `Square` (tipo 4) con relleno amarillo, opacidad ~0.35 y borde 0. Al guardar y reabrir el PDF, **la anotación permaneció como objeto independiente**, con su posición y opacidad recuperables. Esto **no equivale** a prueba de ajuste manual en la instalación del evaluador ni a una prueba de colocación sobre escaneo real: ambas se validarán con el siguiente contrato.
