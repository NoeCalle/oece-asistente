# Contraste financiero documentado

Versión 1.2, 01/11/2026. Corte normativo y ventana financiera conservados: **01/05–31/10/2026**. Esta herramienta contrasta importes citados; no emite un dictamen de solvencia.

## Alcance y fundamento

Se aplica a ejecutores y consultores jurídicos; para consultor natural se necesita el dato citado de inscripción vigente como ejecutor. No se imponen ratios de obras a bienes/servicios, a reconsideraciones o a actualizaciones legales. Una rama desconocida queda por aclarar.

El [Reglamento oficial](https://cdn.www.gob.pe/uploads/document/file/7594705/6444155-reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf?v=1787002595), 25.5.2.b.1.1–b.1.3, PDF pp. 14–15, distingue reporte de riesgos, ratios/análisis económico y equilibrio patrimonial. La [directiva RNP](https://cdn.www.gob.pe/uploads/document/file/7946960/6682380-directiva-de-procedimientos-y-tramites-ante-el-registro-nacional-de-proveedores.pdf?v=1745192527), 9.2.3, pp. 6–7, contiene estos indicadores; 9.2.4 y remisión 9.3.3 tratan al consultor natural también ejecutor. [Registro exacto de fuentes](../rules/finanzas.v1.2.json).

| Indicador | Operación | Tratamiento |
|---|---|---|
| R2 | Patrimonio / (pasivo corriente + pasivo no corriente) | Comparar ≥ 0,05 |
| R3 | Activo corriente / pasivo corriente | Comparar ≥ 1 |
| R8 | Patrimonio / capital social | Comparar ≥ 1/3 mediante multiplicación exacta |
| R9 | Utilidad operativa / (patrimonio + pasivo no corriente) | Referencial; no aprueba/rechaza automáticamente |
| RC | Magnitud de pérdidas acumuladas / capital base documentado | Mostrar indicador y pendiente de interpretación/cobertura; no inferir aprobación del signo ≥ 0,5 |

La excepción PC = 0 del cálculo de CMC sin experiencia no se traslada al ratio R3. Un denominador no positivo queda no determinable; no se presume infinito. La CMC propuesta y el contraste de solvencia son operaciones distintas.

## Datos que prepara el coordinador

Se conserva el [contrato de hechos y citas](CONTRATO_EXPEDIENTE.md). Cada valor necesita autor, fecha, huella, localizador y cita que lo sustente. El cotejo de bases no es un nuevo documento formal exigido al proveedor: es una condición del cálculo para no mezclar importes.

- Bases: `fecha_estados_financieros`, `moneda_estados_financieros` y `base_financiera_homogenea` = true. El coordinador debe contrastar período, moneda, unidad y ámbito matriz/sucursal. La fecha no puede ser posterior a la solicitud. Un código de tres letras identifica la moneda declarada, sin certificar que sea un código ISO válido ni convertir valores.
- Importes: `activo_corriente`, `pasivo_corriente`, `pasivo_no_corriente`, `patrimonio`, `capital_social`, `utilidad_operativa`, `perdidas_acumuladas` y `capital_base_perdidas` según indicador. No se completa con cero un dato ausente. No se presume que el capital base de pérdidas sea capital social.
- Riesgos: `clasificacion_sbs`, `fecha_reporte_sbs`, `ultimo_reporte_sbs_confirmado`. Se admite clasificación citada Normal o no reportado como contraste favorable documental; otras categorías identificadas producen diferencia. Confirmar que sea el último reporte aplicable exige revisión, no una consulta en vivo inventada.
- Análisis: `analisis_solvencia_integral_documentado`, cuando exista una evaluación citada del equilibrio patrimonial, pérdidas/coberturas y demás condiciones aplicables. Ratios satisfechos sin ese análisis no completan el control integral.

Importes como cadenas decimales sin separadores de miles. Se admiten patrimonio y utilidad negativos; pasivos, activo, capital y magnitud de pérdidas se tratan como no negativos en estas operaciones. Límites técnicos: hasta 36 dígitos significativos, 12 decimales y magnitud 10²⁴; valores mayores quedan para revisión. No son límites jurídicos de montos. Se rechazan booleanos, float, valores no finitos y exponentes extremos.

## Resultados y contradicciones

Los controles `FIN-01`, `FIN-R2`, `FIN-R3`, `FIN-R8`, `FIN-SBS` y `FIN-INTEGRAL` conservan citas y autoría. JSON guarda numeradores, denominadores y valores aproximados a doce decimales; los umbrales se comparan con valores exactos. Word muestra tabla y observaciones. R9/RC permanecen como indicadores, sin convertirse en cumplimiento de solvencia.

Si una declaración de solvencia satisface un control agregado pero contradice un ratio o reporte, ese control agregado pasa a no determinable. Se conserva su resultado documental previo y los IDs del conflicto; los hechos originales no se reescriben. Esto se aplica a `AC-22`, `IN-09`, `CMC-08` y `AU-04`.

OCR sin cotejo no sostiene los cálculos. Fuera de la ventana o sin régimen seleccionado, se conservan las propuestas y se deshabilita la conclusión de sus controles. La antigüedad admisible de estados, períodos requeridos por cada rama, exclusiones, cobertura de pérdidas y evaluación integral siguen requiriendo análisis del caso.
