# OCR local de muestra
Estado al 30/10/2026: prototipo probado en tres páginas; sin integración al índice ni revisión jurídica.

## Componentes
- scripts/preparar_ocr.py: selecciona entre 1 y 10 páginas PDF por ejecución, valida la fuente contra manifiesto y las renderiza con pdftoppm a una escala máxima de 2200 píxeles.
- scripts/ocr_windows.ps1: usa Windows.Media.Ocr en Windows PowerShell 5.1, valida las imágenes y guarda texto, líneas, palabras y coordenadas.
- scripts/verificar_ocr.py: comprueba procedencia, página, hashes, geometría y estado de revisión. No calcula precisión del OCR.

No instala motores ni envía documentos a servicios externos. En este equipo estaban disponibles en-US y es-MX; la muestra usó es-MX. Otros equipos requieren idioma OCR instalado y acceso al motor Windows. El script no cambia esa configuración.

## Ejecución
Requiere las dependencias de requirements-indexacion.txt y un ejecutable pdftoppm existente. Desde la raíz del proyecto:

```text
python scripts/preparar_ocr.py --source ds-006-2026-jus.pdf --pages 1,2 --renderer RUTA_AL_EJECUTABLE_PDFTOPPM
powershell.exe -NoProfile -File scripts/ocr_windows.ps1 -Root RUTA_ABSOLUTA_DEL_PROYECTO -Job RUTA_DEL_JOB_DEVUELTA -Language es-MX
python scripts/verificar_ocr.py RUTA_AL_ARCHIVO_PAGE_0001_OCR_JSON
python -m unittest discover -s tests -p "test_*.py" -v
```

Las rutas de ejemplo deben sustituirse por las reales. El trabajo queda en normativa/ocr/<sha256-del-pdf>/, excluido de Git. Originales y derivados permanecen separados. Ejecutar el preparador otra vez con otras páginas actualiza job.json de esa fuente, conservando los derivados previos.

## Trazabilidad
Cada salida indica hash de PDF, página PDF, hash de imagen, idioma, motor, compilación Windows y coordenadas en píxeles de la imagen renderizada. El motor no expone una puntuación de confianza ni una versión de motor independiente: ambos quedan null cuando corresponda; la compilación Windows se registra aparte.

reviewed=false y apta_para_evaluacion=false son obligatorios en esta muestra. Verificación de coordenadas y hashes no equivale a aprobación del texto. Las imágenes vinculadas deben conservarse para revisar cada palabra citada.

## Resultado y límites
Se procesaron DS 006-2026-JUS p.1 (2172 caracteres), p.2 (3392) y DS 009-2025-EF p.20 (7099). Se compararon visualmente las tres páginas y se observaron errores en caracteres y números. No se midió tasa de error, no se corrigió texto automáticamente y no se procesaron las 200 páginas completas de los dos PDF detectados sin texto suficiente.
El índice anterior conserva sus resultados y alertas. No se debe usar una cifra OCR sin cotejarla con la imagen.

[Reporte de muestra](../../normativa/ocr-muestra-2026-10-30.json). [Estado general](../ESTADO.md).

## Siguiente trabajo
Definir muestras con transcripción de referencia, tolerancias por campos críticos y señales de rechazo. Añadir timeout para operaciones WinRT, control de fallo por página y reanudación antes de ejecutar lotes largos. Después integrar derivados revisables a un índice nuevo conservando la versión anterior.

Referencia técnica: [OCR de Windows](https://learn.microsoft.com/en-us/uwp/api/windows.media.ocr.ocrengine).
