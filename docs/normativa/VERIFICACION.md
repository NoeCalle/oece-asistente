# Bitácora de verificación normativa
Consulta realizada el 2026-10-29, zona America/Lima. Investigación inicial dirigida al RNP, no dictamen de vigencia exhaustivo.

## Evidencia y método
Se buscaron instrumentos por denominación en OECE/gob.pe, MEF, MINJUS, SUNAT y El Peruano. Se abrió texto oficial cuando estuvo disponible. Algunas rutas gob.pe respondieron 418 y el PDF de la directiva 403; por eso se registró el método “resultado_buscador_oficial” cuando solo se recuperó contenido indexado. No se guardaron binarios, firmas verificadas ni hashes. No se usaron páginas privadas o proxies como sustento normativo.

| Hallazgo | Evidencia consultada | Qué se valida | Qué falta |
|---|---|---|---|
| Ley 32069 y DS 009-2025-EF | [Resolución de aprobación de directiva](https://busquedas.elperuano.pe/api/visor_html/2391987-1) y [compendio OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento) | Inicio general 22/04/2025; publicación de ley 24/06/2024 y reglamento 22/01/2025 | Excepciones, erratas y cadena completa de cambios |
| Cambios de ley | [Compendio OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento) | Identifica 32103, 32187, 32515, DL 1715 y 32732 | Originales, alcance por disposición y exhaustividad |
| Ley 32732 | [Compendio OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento) | Publicación reportada 19/07/2026; vigencia de modificación condicionada según novena DCF | Identificar y revisar acto reglamentario habilitante; no asignar fecha efectiva todavía |
| DS 001-2026-EF | [Compendio OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento) | Publicación 08/01/2026 y vigencia reportada 14/01/2026 | Resolver contraste con portal Perú Compras que muestra 09/01; leer DCF y resolución de bases estándar |
| DS 222-2026-EF | [El Peruano, texto abierto](https://busquedas.elperuano.pe/dispositivo/EX/2567159-1) | Publicación 21/10/2026 y modificación de decimocuarta DCF sobre certificación | Cerrar fecha de eficacia; no inferir que habilita modificación de Ley 32732 |
| Directiva 001-2025-OECE/CD | [Texto oficial HTML](https://busquedas.elperuano.pe/api/visor_html/2391987-1); [ficha OECE](https://www.gob.pe/institucion/oece/normas-legales/6682380-001-2025-oece-cd) | Identidad, resolución aprobatoria, inicio 22/04/2025, remisiones del numeral 9.3 | Revisar anexos íntegros y cambios posteriores hasta el corte |
| TUPA | [Índice OECE](https://www.gob.pe/institucion/oece/informes-publicaciones/tipos/16-tupa) y [resolución modificatoria](https://busquedas.elperuano.pe/dispositivo/NL/2503213-1) | Cadena identificada: DS 086-2025-EF, RGG 002-2026 y RPE 073-2026 | Obtener fichas y todas las actualizaciones intermedias, plazos/tasas por procedimiento |
| RPE D000073-2026 | [El Peruano, texto abierto](https://busquedas.elperuano.pe/dispositivo/NL/2503213-1) | Emisión 31/03/2026; publicación 08/04/2026 | Lectura de anexos e impacto RNP; fecha de eficacia |
| Nuevo TUO LPAG | [MINJUS](https://www.gob.pe/institucion/minjus/normas-legales/8169463-006-2026-jus), [control SUNAT](https://www.sunat.gob.pe/legislacion/procedim/normasadua/gja-01/ctrlCambios/index.htm), [noticia oficial](https://www.elperuano.pe/noticia/294713-tramites-mas-simples-entra-en-vigencia-el-nuevo-tuo-de-la-ley-de-procedimiento-administrativo) | DS 006-2026-JUS; publicación 30/04/2026; inicio reportado 01/05/2026; sustitución del TUO 2019 | Texto íntegro y artículos concretos para recursos, plazos y notificación |
| FUP | [Informe oficial MEF/OECE](https://www.mef.gob.pe/contenidos/acerc_mins/anexos/04_IRC_CESE_OECE_2026.pdf) | Identifica Directiva 001-2026-OECE/CD y vigencia 11/02/2026 | Original de aprobación y anexo; relación exacta con datos del piloto |
| Transición CMC | [Comunicado 011-2025](https://www.gob.pe/institucion/oece/noticias/1239547-comunicado-n-011-2025-oece-obligaciones-de-los-ejecutores-de-obra-sobre-la-reinscripcion-y-aumento-de-capacidad-maxima-de-contratacion) | Fuente orientativa identificada | Revisar norma transitoria vigente y cambios posteriores |

## Inconsistencias que deben conservarse
1. No equiparar fecha de ficha, fecha de firma y publicación en diario oficial. Ejemplos: TUPA marzo/abril y TUO abril 28/30.
2. El compendio recuperado muestra inconsistencias de actualización y fechas en el entorno de Ley 32515. Sus fechas permanecen null.
3. El compendio y Perú Compras difieren sobre DS 001-2026-EF. El catálogo conserva 14/01 como dato provisional atribuido, con estado en_conflicto y reglas deshabilitadas.
4. No tratar el reglamento consolidado a enero como vigente sin incorporar la modificación encontrada en octubre.
5. Las guías de trámites pueden tener actualización anterior al corte y referencias históricas. No trasladar tasas, plazos o fórmulas a código desde estas guías.
6. No confundir Directiva 001-2025-OECE/CD (RNP), Lineamiento 001-2025-OECE/CD (otra materia), Directiva 001-2025-OECE/GG ni Resolución Ministerial 006-2026-JUS con el Decreto Supremo del mismo número.

## Cierre pendiente de fase 1
Obtener originales y anexos desde fuentes oficiales; calcular SHA-256; comprobar fecha y firma cuando proceda; construir relaciones a nivel de disposición; revisar transitoriedad; cotejar TUPA contra reglamento y directiva; revisión humana. Un buscador sin resultados no acredita ausencia de derogatorias o modificatorias. Volver a revisar las fuentes antes de cada evaluación real.

## Estado del repositorio observado
Repositorio público NoeCalle/oece-asistente, rama main, commit de partida 296b948e8e1f3debaffe2cb263e0af0cb71ab63e. Único archivo inicial: README.md con título del repositorio. Sin código, pruebas, AGENTS.md ni documentación previa observados en el árbol inicial. El ZIP mencionado en el chat previo no fue recibido, recuperado ni ejecutado.

## Continuación: descarga y Drive
Se superaron los errores de acceso inicial usando descarga directa de las páginas oficiales. Se descargaron y archivaron 23 archivos; véase [BIBLIOTECA.md](BIBLIOTECA.md). Las observaciones anteriores describen el estado inicial, no el estado de descarga actual. Ninguna revisión humana ni regla queda aprobada.

## Continuación registrada 30/10/2026
Inicio 14/01/2026 del DS 001-2026-EF sustentado con DCF y publicación del acto habilitante. Se conserva arriba la discrepancia histórica. Se recuperó el comunicado de categorías y se elaboró matriz candidata del piloto. [Hallazgos](HALLAZGOS_PILOTO.md). No se cierra fase 1 ni se aprueban reglas.
