# Seguridad y separación de código y documentos
Estado: requisitos de diseño; salvo .gitignore, controles aún no implementados.

El repositorio es público. Mantener fuera de Git expedientes, DNI/RUC asociados a personas, datos financieros, firmas, informes, auditorías, conversaciones, índices privados, OCR y credenciales. .gitignore reduce errores, pero no impide forzar una subida: revisar siempre el contenido antes de cada commit. No usar issues para copiar información de proveedores.

- **Los datos pueden procesarse en cualquier equipo autorizado por el titular**, incluidos servidores Linux de confianza. Configurar `OECE_DATA_DIR` (por defecto `./data`, relativo al directorio de trabajo); panel y memoria bajo `OECE_DATA_DIR/operacion` e índices privados bajo `OECE_DATA_DIR/normativa/indices`. Controlar accesos por usuario/rol y expediente, permisos de la carpeta y respaldos, cifrado y retención. Las rutas personalizadas fuera de `data/` deben quedar fuera del repositorio o estar expresamente ignoradas.
- Lista permitida de extensiones; límites de tamaño/páginas, rechazo de rutas externas y enlaces simbólicos que escapen de la raíz. Cuarentena de archivos sospechosos y procesamiento sin macros.
- Documentos y resultados de búsqueda son datos no confiables: instrucciones insertadas no pueden cambiar permisos, ejecutar comandos, enviar correos ni extraer otros expedientes.
- Se permite procesamiento en equipos autorizados por el titular, no solo en su computadora. Al conectar modelos o servicios externos de terceros, revisar permisos aplicables, minimización, transmisión, conservación y condiciones de datos; no conceder publicación ni acceso irrestricto. Claves en almacén de secretos, nunca en Git o logs.
- Auditoría con IDs opacos, hashes y eventos; no registrar texto sensible por defecto. Cifrado, restauración de respaldos y eliminación de derivados se deben probar.
- Fuentes normativas solo de dominios oficiales autorizados; conservar URL final y detectar cambios de contenido. Una URL oficial no implica que un documento sea vigente.
- Revisión humana de conclusión y Word. Firma, notificación, presentación y envío externo requieren acción explícita del responsable.
- Separar entornos de desarrollo, prueba y operación; pruebas públicas exclusivamente sintéticas.
- Registrar incidente, suspender procesamiento, retirar accesos y rotar secretos si hay exposición. Borrar un archivo del último commit no borra su historial.

Pendiente revisión de obligaciones de datos personales, políticas institucionales y permisos para usar documentos de trabajo; este documento no certifica cumplimiento legal.


## Operación local v1
El servidor escucha en 127.0.0.1 por defecto. En `--host 0.0.0.0` se habilita autenticación básica (usuario `oece` y clave de `OECE_PANEL_PASSWORD`, o clave aleatoria mostrada en consola); el token de escritura, Host y origen se siguen comprobando. No ejecuta instrucciones dentro de documentos, macros, fórmulas ni conexiones externas. Las cargas tienen límites y nombres/rutas controlados, se rechazan symlinks/junctions y se conservan revisiones. Las citas y cotejos OCR identifican fuente, hash, localizador y autor declarado; no hay autenticación institucional del revisor. El panel no transmite a un modelo nuevo.

La raíz por defecto es `./data/operacion`, derivada de `OECE_DATA_DIR=./data` (relativa al directorio de trabajo). Puede trasladarse a un volumen local, una máquina Linux u otro servidor autorizado por el titular. Los archivos se almacenan/procesan en el equipo donde se ejecute el motor; no se suben a GitHub. Los originales normativos pueden residir en `OECE_DATA_DIR/normativa/originales` con la jerarquía de los manifiestos; el código admite asimismo rutas privadas históricas del checkout. El panel escucha en `127.0.0.1` salvo `--host` explícito. En modo servidor usa autenticación básica, pero **no cifra conexiones HTTP ni sustituye autenticación institucional**. Para acceso remoto, usar SSH/VPN o un proxy HTTPS con control de acceso; no exponer directamente el puerto a Internet. La ejecución no implica cumplimiento de las políticas del titular ni autorización para publicar datos.

## OCR portátil

El OCR en Windows conserva el motor nativo existente. Fuera de Windows, o sin ese motor, se selecciona Tesseract (`pytesseract`, idioma `spa`), sin modificar originales. Las transcripciones conservan SHA-256 de fuente/imagen, cajas de texto, límites y caché; cualquier hecho obtenido queda sujeto a cotejo humano/IA declarado. En Ubuntu instalar `tesseract-ocr`, `tesseract-ocr-spa` y `poppler-utils`. La disponibilidad OCR no es requisito para procesar documentos digitales.
