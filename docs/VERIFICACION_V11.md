# Verificación de la versión 1.1

**Antecedente conservado.** La versión 1.2 añade contraste financiero: [verificación actual](VERIFICACION_V12.md). Las cifras siguientes corresponden a 1.1.

Cierre: **01/11/2026, America/Lima**. Corte normativo usado: **31/10/2026**. Versión local asistida; no certificación jurídica ni aceptación institucional. [Registro estructurado con huellas](../proyecto/ejecuciones/operacion-v11-2026-11-01.json).

## Comportamiento comprobado

109 pruebas: las 87 anteriores y 22 de la expansión. Se probaron bandas financieras y sus fronteras, PC cero según rama, factores, consorcios, duplicados, antigüedad/futuro de obras, cifras no finitas, calendario explícito, cobertura insuficiente, distancia, cambio de año, inscripción sin cargas de obras para bienes, solvencia del consultor natural también ejecutor, moneda, actualización anual nacional/extranjera, nueva prueba/única instancia y ventana temporal. La integración ejecuta los cuatro módulos y comprueba Word/CSV/originales/manifiesto. [Pruebas nuevas](../tests/test_procedimientos_v11.py).

El navegador Edge ejecutó creación, clasificación de inscripción, persistencia de booleanos, carga TXT sintética, preparación y descarga Word; también guardó clase/motivo de actualización financiera anual. Cero errores JavaScript observados. La suite HTTP comprueba rechazo de solicitudes sin token, origen externo y rutas/nombres peligrosos. En una repetición el equipo interrumpió una conexión local; el grupo de 34 pruebas de operación pasó al repetirse y la ejecución final completa pasó con 109/109. No se relajaron controles ni se sustituyó el rechazo esperado por aceptar cualquier error de red.

## Word: revisión visual cerrada en alcance sintético

| Ejemplo | Páginas inspeccionadas | Resultado relevante |
|---|---:|---|
| Ampliación consultores | 6 | Diferencia de honorarios PEN 20.000; faltantes de consorcio y otros datos visibles |
| Aumento de CMC | 4 | Propuesta PEN 825.000, con factores y sin conclusión global favorable por faltantes |
| Inscripción | 3 | Rama de bienes natural; sin requisitos financieros de obras |
| Actualización | 3 | Límite calendario superado; requiere aclarar días/reglas especiales |
| Reconsideración | 3 | Nueva prueba faltante y cómputo con calendario expresamente ficticio |
| Total | 19 | Cinco informes |

Se corrigieron etiquetas internas y agrupación de citas/autores y se regeneraron los cinco informes. Se inspeccionaron todas las páginas finales: no se observaron texto cortado, superposiciones ni tablas fuera de página. Son ejemplos de formato provisional, sin datos de proveedores reales. No se extrapola esta revisión a cualquier documento futuro ni a aceptación institucional.

La exportación 1.0 bloqueada se resolvió con **LibreOffice 26.8.2 x64**, extraído como imagen administrativa bajo `data/herramientas/`, sin sustituir Word ni instalar un servicio de inicio. [Paquete oficial y suma de verificación](https://download.documentfoundation.org/libreoffice/stable/26.8.2/win/x86_64/LibreOffice_26.8.2_Win_x86-64.msi.mirrorlist). SHA256 del paquete: `ff4b911403b67ee9e6249f820f9782c44bb32c94fdaa45b0da53a8e419e5307a`. Se utilizó el renderizador de documentos de Codex con perfiles de conversión aislados y se examinaron las PNG de todas las páginas. El instalador, binarios, PDF/PNG de inspección y Word quedan fuera de Git. El bloqueo histórico de automatización Word no se declara reparado.

## Fuentes utilizadas y límites

- [Reglamento oficial consolidado](https://cdn.www.gob.pe/uploads/document/file/7594705/6444155-reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf?v=1787002595): artículos 25–28 y 381; páginas PDF 13–16 y 195–212 según rama.
- [Directiva RNP oficial](https://cdn.www.gob.pe/uploads/document/file/7946960/6682380-directiva-de-procedimientos-y-tramites-ante-el-registro-nacional-de-proveedores.pdf): tablas y experiencia 9.2.5–9.2.6 (pp. 7–9), remisiones de aumento/ampliación 9.3.2–9.3.3 (p. 12), actualizaciones 9.6 (pp. 13–14). La remisión expresa a 9.2.4 actualiza J05, sin inventar una aprobación humana.
- [Folio gráfico oficial SPIJ](https://spij.minjus.gob.pe/Graficos/Peru/2025/Enero/22/DS-009-2025-EF_01.pdf): fórmula CMC, artículo 28; página PDF 1, impresa 8. No se adopta como actual el texto antiguo de 25.7 del mismo folio.
- [TUO oficial MINJUSDH 2026](https://cdn.www.gob.pe/uploads/document/file/10399631/8441836-tuo-ley-27444-ley-procedimiento-administrativo-general-julio-2026-ok.pdf?v=1785866517): artículos 133–135 (pp. 153–154), 207–208/211 (pp. 193–194). La fecha editorial no acredita ausencia de cambios posteriores.

[Fuentes exactas, huellas y páginas por control](../rules/procedimientos.v1.1.json). La biblioteca reconstruida comprende 48 archivos/29 registros/seis manifiestos, 2.281 fragmentos y 2.046 con texto. Nueve archivos conservan alertas por escaneado, poco texto o formatos/fórmulas pendientes. [Reporte](../normativa/indexacion/reporte-operacion-v11-2026-11-01.json). Los estados jurídicos del catálogo y de la matriz candidata histórica no se convierten en aprobados por tener una extracción o una prueba técnica.

## Pendiente real

Completar cadena normativa/excepciones y TUPA por rama; comprobar fuentes para solicitudes posteriores al corte; validar interpretación y resultados con expedientes autorizados; definir condiciones institucionales de acceso/retención; adaptar modelos reales cuando el usuario los tenga. La conversación abierta usa Codex, sin modelo autónomo incorporado al panel. [Estado y estimación](ESTADO.md).
