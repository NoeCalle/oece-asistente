# Proceso de cambios para OECE Assistant

## Flujo recomendado

1. No desarrollar nuevas funciones con commits directos en `main`. Crear una rama temática: `fix/`, `feat/` o `docs/`.
2. Agrupar cambios relacionados en un **pull request** con el motivo, riesgos, archivos modificados y pruebas ejecutadas.
3. Ejecutar **`portabilidad.yml` en Windows y Ubuntu**. Una falla bloquea la integración. Para corregir una prueba, preferir validar **comportamientos** y contratos, no depender de una palabra exacta de instrucciones.
4. Revisar el diff del PR antes de integrar: no subir PDF, expedientes, originales, claves ni rutas privadas. Inspeccionar `.gitignore`.
5. Registrar explícitamente qué pruebas **no se han ejecutado** por falta del corpus normativo. `tests.yml` es manual y estricto cuando los originales pueden recuperarse.
6. Solicitar revisión humana y utilizar **merge de PR** tras controles; conservar trazabilidad. No afirmar aprobación institucional por CI verde.

## Protección de main (configuración GitHub pendiente de aprobación manual)

En **Settings → Branches / Rulesets**, crear una regla para `main` que:
- exija PR antes de fusionar y rechace pushes directos;
- exija pruebas de `portabilidad` en **ubuntu-latest** y **windows-latest**;
- requiera resolución de conversaciones de revisión y bloquee merge con checks fallidos;
- opcionalmente exija un revisor distinto del autor (tener en cuenta disponibilidad de colaboradores).

**Esta configuración de protección NO se activa por añadir este documento.** Necesita los permisos de administración de GitHub. Un PR por sí solo **no impide** futuros pushes directos a main si no hay reglas.

## Qué significa cada estado CI

- **Portabilidad (push/PR):** regresión sintética independiente del corpus, incluidas rutas, seguridad, agentes, cálculo, OCR y compatibilidad de plataformas. Verde **no implica** validación jurídica ni pruebas con expedientes reales.
- **Suite completa con originales (manual):** exige recuperar/verificar el corpus antes de ejecutar `python -m unittest discover`. Si faltan PDFs debe **fallar**, no aparecer como verde por saltar la suite.
- **Validación externa de agentes:** comprobar lectura Drive, interpretación de casos autorizados, producción de entregables y publicación; estas pruebas no están cubiertas por GitHub Actions sin conexiones autorizadas.

## Auditoría del 05/11/2026

Cambios implementados en la rama `fix/auditoria-seguridad-ci-20261105`: prueba estática menos frágil; MCP con sesión por caso opcional y directorio de entrada aislado; contraseña ambiental oculta y bloqueo temporal de intentos fallidos; CI de corpus completo manual; correcciones acotadas del validador PDF/XLSX; documentación operativa actualizada. Revisar el PR correspondiente y los checks antes del merge.

Pendientes separados: revisar consistencia de rutas/estilo con herramientas automáticas; auditar los permisos efectivos de Google Drive y aprobar política de publicación de criterios (el repositorio público no los certifica).
