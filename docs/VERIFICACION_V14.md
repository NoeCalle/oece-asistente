# Verificación 1.4: fichas TUPA y descarga del panel

01/11/2026. **169 pruebas aprobadas:** 154 anteriores, catorce de TUPA y una regresión del panel. No se modifica el corte normativo 31/10/2026 ni se declara una sesión real de Claude.

## Consulta de fuentes

Quince fichas y cuarenta páginas del anexo TUPA ya conservado. Encabezados/códigos y hashes de texto comprobados al reconstruir el índice. La consulta distingue ocho ramas de obras, personas para bienes/servicios, extranjero no domiciliado y posible régimen especial. Conserva alternativas ante datos ausentes y no asigna código a actualización/reconsideración sin delimitar su trámite.

Las pruebas cubren fechas anterior/igual a publicación, dentro/igual al corte y posterior; valores inválidos; rama nacional/no domiciliado; código y página ajenos; original alterado; reconstrucción reproducible. Ninguna fecha produce una declaración de vigencia. Se recupera el mismo contenido por CLI, llamada MCP y proceso stdio real desde otro directorio.

El catálogo MCP actual tiene doce herramientas. La prueba de protocolo actual y negociación initialize sigue pasando. No se usa API de modelo ni se editan configuraciones de Claude.

Fuente oficial web y límites de acceso documentados en [la guía TUPA](normativa/FICHAS_TUPA.md). Cotejo visual acotado a páginas 31, 50, 51 y 66; no revisión humana ni jurídica exhaustiva. No se crean nuevos Word finales ni se reutiliza QA histórica como revisión de informes nuevos.

## Fallo detectado y corregido

La primera suite de 168 pruebas detectó un HTTP 400 al descargar. El listado aceptaba una carpeta `.preparando-...` en el breve intervalo entre la escritura de su manifiesto y su renombrado atómico. La descarga exige el identificador definitivo de 64 caracteres hexadecimales y rechazaba el temporal.

El listado ahora publica únicamente directorios con ese identificador y manifiesto. Verifica además que las rutas interiores no sean enlaces/uniones externos. La regresión crea expresamente un temporal con manifiesto y confirma que no aparece como descargable. Se mantiene la publicación atómica del motor.

La suite final pasó con 169 pruebas. El panel actualizado se reinició sin trabajos activos y recorrió creación, ficha, booleanos, carga, procesamiento, descarga Word y actualización financiera anual en Edge, con cero errores JavaScript observados. Se comprobó la descarga como archivo DOCX; no se presenta ese archivo ficticio de prueba como informe final revisado visualmente.

## Integridad y pendientes

Verificador de biblioteca: 29 registros, 48 originales comprobados y 47 referencias de motores. La consulta TUPA agrega un índice de recuperación, no nuevos requisitos al evaluador ni una aceptación por un booleano agregado.

[Ejecución registrada](../proyecto/ejecuciones/tupa-v14-2026-11-01.json). Permanecen abiertos el desglose completo de requisitos/excepciones, cadena temporal por disposición, uso con otro cliente real, expedientes autorizados y modelos laborales. La estimación general se conserva en 75 %.
