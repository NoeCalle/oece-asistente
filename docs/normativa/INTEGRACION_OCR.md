# Integración de OCR candidato al buscador
Versión 0.1.0, ejecutada el 30/10/2026.

## Resultado comprobado
Se generó normativa/indices/biblioteca-ocr.sqlite a partir del índice digital y de las tres páginas de muestra, conservando normativa/indices/biblioteca.sqlite.

- Índice digital: 1.278 fragmentos, 940 con texto.
- Índice con OCR: 1.281 fragmentos, 943 con texto; los tres nuevos son derivados OCR candidatos.
- Repetición con los mismos derivados: cero fragmentos nuevos, mismo identificador de corpus.
- Consulta real “27444”: recuperó páginas OCR 1 y 2 del decreto aprobatorio del TUO. Página 1 incluye advertencia de identificador crítico erróneo.
- 22 pruebas técnicas aprobadas: 8 índice, 4 metadatos OCR, 4 calidad y 6 integración. Casos jurídicos sin ejecutar.

Identificador del nuevo corpus: `c7e88d73f60955a90f7cae5ba6877d7d4345e043eed27a8783bc3bb643312f14`.
[Reporte estructurado](../../normativa/integracion-ocr-2026-10-30.json).

## Uso
Requiere el índice digital y los derivados generados por el prototipo OCR. Desde la raíz, sustituir las rutas de muestra por archivos reales:

```text
python scripts/integrar_ocr.py --quality-reference tests/fixtures/ocr/referencias-regiones.v0.1.json RUTA_PAGE_0001_OCR_JSON RUTA_PAGE_0002_OCR_JSON
python scripts/indexar_normativa.py search --database normativa/indices/biblioteca-ocr.sqlite --query "27444" --limit 10
python -m unittest discover -s tests -p "test_*.py" -v
```

La referencia de calidad es opcional. Si una página carece de referencia se declara expresamente; no se inventa una aprobación. La búsqueda por defecto sigue usando el índice digital: seleccionar el nuevo índice explícitamente.
La opción --base permite partir de un índice ya ampliado y --output debe señalar otro archivo .sqlite dentro del proyecto. No se permite reemplazar el índice de entrada.

## Integridad y trazabilidad
Antes y después de integrar se verifica la fuente, la imagen y el derivado. Se exige que la fuente exista en el índice y que la página original estuviese marcada para OCR. La copia se publica al terminar; un fallo conserva la salida anterior.
La extracción original permanece como otro fragmento; el OCR lleva tipo=ocr, hash del derivado, hash de imagen, página, motor, idioma y ruta local del derivado que contiene las coordenadas de palabras.
Los fragmentos OCR incluyen ocr_pendiente_revision. Si el diagnóstico regional detecta un identificador crítico defectuoso, se añade esa alerta. Incluso los resultados dentro del umbral de muestra mantienen apta_para_evaluacion=false.

## Versiones y límites
Un mismo derivado no se duplica. Si se suministra otra versión OCR de una página que ya tiene una, reconstruir la salida desde el índice digital base; así no se mezclan versiones candidatas en una misma búsqueda.
Los identificadores de corpus cambian al incorporar derivados o diagnósticos diferentes. El ámbito del diagnóstico es solo las regiones transcritas, no la página completa.
No se corrige OCR, no se procesan lotes enteros, no se aprueba texto jurídico ni se selecciona régimen normativo. Timeout/reanudación, más referencias críticas y recuperación por disposición siguen pendientes.

[Estado del proyecto](../ESTADO.md), [OCR local](OCR_LOCAL.md), [diagnóstico de calidad](CALIDAD_OCR.md).
