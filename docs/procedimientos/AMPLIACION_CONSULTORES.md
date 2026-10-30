# Ampliación de categorías de consultores: ficha inicial
Versión 0.1 — actualización 2026-10-30; corte normativo investigado 2026-10-29. Extracción documental para revisión; no motor de decisión.

## Identificación comprobada
TUPA consultado: archivo modificación 073-2026, páginas PDF/impresas 31 y 32, revisadas visualmente.
- Denominación: Ampliación de Categorías para Consultores de Obras.
- Código: PA42003A92.
- Formulario referido: DRNP-SDOR-FOR-0001.
- La ficha muestra S/ 310, 30 días hábiles y evaluación previa con silencio negativo.
- Órgano que aprueba según ficha: Subdirección de Operaciones Registrales.
Estos datos describen la versión archivada; no son parámetros vigentes habilitados para expedientes. La ficha antecede al TUO 2026 y la cadena completa de cambios sigue abierta.

## Régimen y categorías: control previo obligatorio
El artículo 27 distingue categorías por tipo de consultoría: formulación de fichas/estudios con componente de infraestructura, elaboración de expediente técnico, supervisión de elaboración y supervisión de ejecución. La Cuarta DCT regula la transición desde categorías A/B/C/D por montos.

El [Comunicado 001-2026-OECE](https://www.gob.pe/institucion/oece/noticias/1336986-comunicado-n-001-2026-oece-asignacion-de-especialidades-y-categorias-de-consultores-de-obra-en-el-marco-de-la-ley-n-32069-y-su-reglamento) informa la recategorización y la reevaluación en la primera ampliación/reinscripción. Se consultó el texto completo de la página oficial y se conservó HTML. Su imagen es solo una portada: no es un PDF con el contenido normativo.

El anexo 2 de la Directiva 001-2025 presenta umbrales históricos/transitorios: B (un servicio de 400 000 o dos de 200 000), C (uno de 4 millones o dos de 2 millones), D (uno de 20 millones o dos de 10 millones), referidos a los montos que define el propio anexo y su contexto. **No aplicarlos por defecto a una ampliación actual.** No son montos del honorario del consultor. Esta lectura se hizo de la tabla DOCX, no certifica vigencia general.

## Discrepancias que requieren resolución
- TUPA p.31 aún describe categorías por montos; el formulario p.90 incluye categorías por tipo de consultoría. No deducir régimen solo por la letra.
- Comunicado anuncia aplicación desde 19/01/2026, mientras el encabezado del numeral 3 de Cuarta DCT consultado dice día siguiente de publicación. Revisar el caso situado en la frontera y actos posteriores.
- El texto consolidado 3.5 (p.228) y el numeral 5 del comunicado describen de distinta manera los expedientes en curso. Cotejar publicación original, erratas y criterio oficial antes de decidir ese supuesto.
- No calcular automáticamente el vencimiento de 120 días hábiles sin calendario oficial, suspensiones y marco aplicable.
- La Quinta DCT sobre FUP también contiene reglas transitorias: no confundir registro con acreditación de requisitos en un procedimiento de selección.

## Matriz
[22 controles estructurados](../../rules/consultores/matriz.v0.1.json), con fuente, SHA-256 y página. Todos deshabilitados y sin aprobación humana.
- **AC-01 — régimen:** Determinar fecha de solicitud, registro previo, recategorización y primera ampliación/reinscripción.
- **AC-02 — identificación:** Vincular solicitante, tipo de persona y representación con formulario.
- **AC-03 — solicitud:** Verificar presentación de solicitud mediante formulario.
- **AC-04 — pago:** Comprobar número de recibo y fecha de pago.
- **AC-05 — experiencia:** Clasificar cada experiencia: Perú bajo Ley, Perú fuera de Ley o extranjero; verificar culminación.
- **AC-06 — peru_ley:** Verificar constancia o documento equivalente emitido por la entidad y datos exigidos.
- **AC-07 — peru_fuera_ley:** Verificar contrato, sustento del contratante, aprobación/viabilidad/conformidad y descripción de actividades.
- **AC-08 — peru_fuera_ley:** Contrastar suma de comprobantes con monto final de consultoría.
- **AC-09 — extranjero:** Verificar contrato y documentos de conformidad o viabilidad con datos exigidos.
- **AC-10 — consorcio:** Identificar obligaciones asumidas por integrante y evitar atribuir toda la experiencia al solicitante.
- **AC-11 — categoría:** Distinguir cuatro tipos de consultoría y condición con/sin experiencia.
- **AC-12 — experiencia_personal:** Contrastar fecha de colegiación o constitución/inscripción según persona.
- **AC-13 — no_duplicación:** No duplicar una misma consultoría en especialidades incompatibles; identificar objeto principal.
- **AC-14 — exclusiones:** Revisar supuestos de experiencia no computable, sin rechazo automático.
- **AC-15 — moneda:** Registrar moneda, fecha del contrato y fuente del tipo de cambio.
- **AC-16 — condiciones:** Revisar inscripción y condiciones del artículo 25 sin imponer requisitos financieros universales.

## Experiencia y documentos
Tres rutas conforme al art.381.4 y TUPA: Perú bajo la Ley; Perú fuera de ella; extranjero. Conservar alternativas de acreditación, condiciones por objeto, participación en consorcio y moneda. Nunca convertir todas las rutas en una lista acumulativa obligatoria.

## Aceptación antes de habilitar
Resolver transitoriedad; revisar artículo 25 por persona; delimitar vigencia de directiva/anexos; cotejar requerimientos íntegros; validar criterios con especialista; preparar documentos sintéticos y luego pruebas ejecutables. El conjunto inicial de casos es una especificación, aún no pruebas corridas.

## Condiciones por persona incorporadas
AC-17 a AC-22: condición tributaria según domicilio; sanción vigente; RNP e información actualizada; representación con alternativa para extranjero no domiciliado; capacidad legal; solvencia con remisión a directiva. Son controles candidatos, pendientes de validación. No agregan requisitos a los previstos en norma.
