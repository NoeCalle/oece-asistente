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
El servidor escucha en 127.0.0.1 por defecto. En `--host 0.0.0.0` se habilita autenticación básica (usuario `oece` y clave de `OECE_PANEL_PASSWORD`, o clave aleatoria mostrada en consola); el token de escritura, Host y origen se siguen comprobando. No ejecuta instrucciones dentro de documentos, macros, fórmulas ni conexiones externas. Las cargas tienen límites y nombres/rutas controlados, se rechazan symlinks/junctions y se conservan revisiones. Las citas y cotejos OCR identifican fuente, hash, localizador y autor declarado; no hay autenticación institucional del revisor. Salvo si el operador activa explícitamente la función opt-in «Analizar PDF con IA», el panel no transmite documentos a modelos externos.

La raíz por defecto es `./data/operacion`, derivada de `OECE_DATA_DIR=./data` (relativa al directorio de trabajo). Puede trasladarse a un volumen local, una máquina Linux u otro servidor autorizado por el titular. Los archivos se almacenan/procesan en el equipo donde se ejecute el motor; no se suben a GitHub. Los originales normativos pueden residir en `OECE_DATA_DIR/normativa/originales` con la jerarquía de los manifiestos; el código admite asimismo rutas privadas históricas del checkout. El panel escucha en `127.0.0.1` salvo `--host` explícito. En modo servidor usa autenticación básica, pero **no cifra conexiones HTTP ni sustituye autenticación institucional**. Para acceso remoto, usar SSH/VPN o un proxy HTTPS con control de acceso; no exponer directamente el puerto a Internet. La ejecución no implica cumplimiento de las políticas del titular ni autorización para publicar datos.

## OCR portátil

El OCR en Windows conserva el motor nativo existente. Fuera de Windows, o sin ese motor, se selecciona Tesseract (`pytesseract`, idioma `spa`), sin modificar originales. Las transcripciones conservan SHA-256 de fuente/imagen, cajas de texto, límites y caché; cualquier hecho obtenido queda sujeto a cotejo humano/IA declarado. En Ubuntu instalar `tesseract-ocr`, `tesseract-ocr-spa` y `poppler-utils`. La disponibilidad OCR no es requisito para procesar documentos digitales.

## Migración de rutas almacenadas

Las rutas relativas se persisten con `/` (POSIX) y se resuelven con `pathlib`. El lector admite por compatibilidad registros antiguos con `\\`, pero rechaza componentes `..`, rutas UNC y rutas con unidad de Windows cuando se espera una ruta relativa. El comando `python -m oece migrar-rutas` migra índices JSON/SQLite privados con respaldo; no altera hashes de documentos originales y requiere detener escritores para evitar cambios concurrentes. Los índices y respaldos siguen fuera de Git.


## Tratamiento de PDFs mediante IA externa (opt-in)

La modalidad `analizar-ia` envía los PDFs del expediente a la API de OpenAI **solo con consentimiento explícito**, tanto desde el panel (casilla y botón) como desde la CLI (`--autorizar-envio`). La clave `OPENAI_API_KEY` se carga de las variables de entorno del servidor autorizado, nunca se escribe en los expedientes ni en Git. El panel local y el modo determinista no envían información a un modelo. `--previsualizar` no hace ninguna llamada de API.

La API puede tener costes y los PDFs pueden contener datos personales, firmas y contratos sometidos a deberes de reserva. Antes de su uso institucional deben verificarse la autorización para transmitirlos y las condiciones de privacidad, retención y ubicación de procesamiento del proveedor. Las solicitudes se hacen con `store:false`; para archivos PDF grandes se utiliza carga temporal en Files API con intento de eliminación al terminar. **No se garantiza eliminación inmediata de los registros que la política del proveedor pueda conservar**. Los reportes, copias de originales y transcripciones se conservan en almacenamiento privado local con huellas SHA-256; nunca en el repositorio. Los textos de los PDFs se tratan como datos no confiables, no instrucciones. Las citas visuales y las operaciones aritméticas son propuestas condicionadas a cotejo humano con el documento original y norma aplicable; no son acreditaciones automáticas.
