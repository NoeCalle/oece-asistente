# Control de calidad OCR: primer diagnóstico
Fecha: 30/10/2026. Se evaluaron cuatro regiones seleccionadas de tres páginas. No es una muestra estadística ni un benchmark de todos los documentos.

## Método
Transcripción manual de regiones observadas en las imágenes renderizadas; referencia fijada por hash de fuente, página, hash de imagen y rectángulo en píxeles.
Se calcula distancia de edición por carácter (CER) y por palabra (WER), normalizando mayúsculas y espacios. Los identificadores críticos deben aparecer completos. El umbral CER del 5 % es una propuesta técnica sin aprobación del especialista. No se corrige el OCR automáticamente.

| Región | CER observado | Resultado diagnóstico |
|---|---:|---|
| Q01-numero-decreto | 25.00 % | requiere_revision |
| Q02-titulo-tuo | 1.71 % | dentro_umbral_de_muestra |
| Q03-referencia-articulo | 1.22 % | dentro_umbral_de_muestra |
| Q04-titulo-articulo-85 | 1.82 % | dentro_umbral_de_muestra |

El número del decreto se reconoció como `006-2026-J(-F` frente a la referencia visual `006-2026-JUS`: el control lo envía a revisión. Las otras tres regiones quedaron dentro del umbral propuesto de caracteres, pero conservan revisión humana obligatoria; incluso allí hay diferencias de símbolos o acentos.
Estos resultados no autorizan citas jurídicas ni muestran que el resto de cada página sea correcto.

## Uso
```text
python scripts/evaluar_calidad_ocr.py tests/fixtures/ocr/referencias-regiones.v0.1.json
python -m unittest discover -s tests -p "test_*.py" -v
```
Requiere los derivados OCR locales y las fuentes referidas en los manifiestos. Las pruebas unitarias técnicas usan datos sintéticos; la ejecución real usa las cuatro regiones de la referencia.

22 pruebas técnicas aprobadas: 8 indexador, 4 trazabilidad OCR, 4 diagnóstico de calidad y 6 integración. Los diez casos jurídicos siguen sin ejecutar.
Siguiente paso: ampliar referencias con importes, porcentajes y fechas del piloto, revisar el criterio de calidad y ampliar la [integración candidata](INTEGRACION_OCR.md) a más páginas conservando texto original y alertas.

[Referencia de regiones](../../tests/fixtures/ocr/referencias-regiones.v0.1.json), [resultado reproducible](../../normativa/calidad-ocr-2026-10-30.json), [estado](../ESTADO.md).
