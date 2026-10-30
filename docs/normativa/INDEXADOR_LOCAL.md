# Indexador local de la biblioteca normativa
Versión técnica 0.1.0, 30/10/2026. Esta herramienta implementa extracción y búsqueda; la selección jurídica de versiones y la evaluación de expedientes siguen pendientes.

## Uso
Requiere Python 3.12 o superior, SQLite con FTS5 y las dependencias fijadas en requirements-indexacion.txt. Se comprobó con pypdf 6.10.0 y python-docx 1.2.0 del entorno local.
Los originales deben estar en las rutas declaradas por los dos manifiestos de descarga. GitHub conserva los manifiestos; las copias se mantienen fuera de Git.

```text
python -m pip install -r requirements-indexacion.txt
python scripts/verificar_biblioteca.py --verificar-originales
python scripts/indexar_normativa.py build
python scripts/indexar_normativa.py search --query "ampliación categorías" --procedure ampliacion_consultores --limit 3
python -m unittest discover -s tests -p "test_*.py" -v
```

La base se crea en normativa/indices/biblioteca.sqlite, excluida de Git. Las búsquedas abren la base en modo lectura. No se requiere cuenta de modelo ni conexión de red para la extracción o búsqueda.

## Qué conserva
- SHA-256 del documento y todas las procedencias cuando dos archivos contienen los mismos bytes.
- PDF: número de página PDF (desde 1), texto y alerta si tiene menos de 50 caracteres. La página impresa no se infiere.
- DOCX: párrafos del cuerpo y celdas, incluidas tablas anidadas, con ruta de bloque/fila/celda. Las celdas combinadas no se duplican dentro de la misma tabla.
- Identificador estable del fragmento derivado de versión de extractor, hash y ubicación.
- Motor y versión, identificador del corpus y estado de revisión declarado en catálogo. La confianza de extracción queda null: no se inventa una puntuación.
- Un resultado siempre devuelve apta_para_evaluacion=false. El filtro por procedimiento organiza la recuperación; no resuelve la vigencia por fecha.

## Integridad y fallos
Verifica tamaño y hash antes y después de leer cada fuente. Si cambian, aborta y conserva el índice anterior. Rechaza rutas de fuentes fuera de la raíz del proyecto. Construye una base temporal y solo sustituye la anterior al finalizar.
Un documento ilegible queda en error_lectura; formatos sin lector quedan en formato_pendiente. Un índice puede contener archivos pendientes: consultar siempre el resumen. Detectar un archivo no equivale a haber extraído todo su contenido.
Las advertencias del lector PDF se conservan (hasta 50 mensajes distintos por documento). Los originales permanecen sin reparar ni modificar.

## Límites actuales
- PDF digital y DOCX; DOC antiguo, XLS, XLSX y HTML pendientes.
- Existe un [prototipo OCR de muestra](OCR_LOCAL.md) separado; aún no se incorpora al índice.
- Encabezados, pies, cuadros de texto y revisiones de Word no cubiertos.
- El orden del texto extraído de PDF puede perder columnas y relaciones de tablas. Revisar visualmente la página antes de utilizarla como evidencia.
- No segmenta todavía por artículo/numeral; el fragmento PDF completo es una página.
- No consolida normas, no calcula plazos, no selecciona automáticamente el régimen aplicable y no revisa firmas.
- No vigila carpetas ni sincroniza Drive. Este es un componente previo a esas funciones.
- La batería actual tiene ocho pruebas del indexador y cuatro de metadatos OCR. Los diez casos jurídicos de la matriz no están ejecutados.

## Referencias técnicas
[Extracción PDF](https://pypdf.readthedocs.io/en/stable/user/extract-text.html), [Documentos Word](https://python-docx.readthedocs.io/en/latest/api/document.html) y [SQLite en Python](https://docs.python.org/3/library/sqlite3.html). El comportamiento ejecutado corresponde a las versiones fijadas, no a una promesa sobre versiones futuras.
