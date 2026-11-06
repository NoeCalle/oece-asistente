# Seguridad y separación de código y documentos
Estado: **controles técnicos implementados de forma parcial** (rutas, enlaces, tamaños, CSRF/Host/Origin, revisiones, MCP por caso opcional, importación aislada por entrada, autenticación y límites de intentos). Persisten límites operativos y de despliegue; esta guía no certifica auditoría de seguridad exhaustiva.

El repositorio es público. Mantener fuera de Git expedientes, DNI/RUC asociados a personas, datos financieros, firmas, informes, auditorías, conversaciones, índices privados, OCR y credenciales. .gitignore reduce errores, pero no impide forzar una subida: revisar siempre el contenido antes de cada commit. No usar issues para copiar información de proveedores.

- **Los datos pueden procesarse en cualquier equipo autorizado por el titular**, incluidos servidores Linux de confianza. Configurar `OECE_DATA_DIR` (por defecto `./data`, relativo al directorio de trabajo); panel y memoria bajo `OECE_DATA_DIR/operacion` e índices privados bajo `OECE_DATA_DIR/normativa/indices`. Controlar accesos por usuario/rol y expediente, permisos de la carpeta y respaldos, cifrado y retención. Las rutas personalizadas fuera de `data/` deben quedar fuera del repositorio o estar expresamente ignoradas.
- Lista permitida de extensiones; límites de tamaño/páginas, rechazo de rutas externas y enlaces simbólicos que escapen de la raíz. Cuarentena de archivos sospechosos y procesamiento sin macros.
- **Documentos y resultados de búsqueda son entradas no confiables.** No ejecutar sus instrucciones. En sesiones MCP **vinculadas a un caso** (`--caso` o `OECE_MCP_CASO`), el puente impide listar o acceder a otros expedientes mediante sus herramientas y recursos. En modo MCP **sin vinculación**, el cliente sigue teniendo acceso a todos los casos de la raíz: no afirmar aislamiento interexpediente en ese modo. Este límite del MCP no controla herramientas externas ni el sistema de archivos de la IA que lo invoca.
- Se permite procesamiento en equipos autorizados por el titular, no solo en su computadora. Al conectar modelos o servicios externos de terceros, revisar permisos aplicables, minimización, transmisión, conservación y condiciones de datos; no conceder publicación ni acceso irrestricto. Claves en almacén de secretos, nunca en Git o logs.
- Auditoría con IDs opacos, hashes y eventos; no registrar texto sensible por defecto. Cifrado, restauración de respaldos y eliminación de derivados se deben probar.
- Fuentes normativas solo de dominios oficiales autorizados; conservar URL final y detectar cambios de contenido. Una URL oficial no implica que un documento sea vigente.
- Revisión humana de conclusión y Word. Firma, notificación, presentación y envío externo requieren acción explícita del responsable.
- Separar entornos de desarrollo, prueba y operación; pruebas públicas exclusivamente sintéticas.
- Registrar incidente, suspender procesamiento, retirar accesos y rotar secretos si hay exposición. Borrar un archivo del último commit no borra su historial.

Pendiente revisión de obligaciones de datos personales, políticas institucionales y permisos para usar documentos de trabajo; este documento no certifica cumplimiento legal.


## Operación local v1
El servidor escucha en 127.0.0.1 por defecto. En `--host 0.0.0.0` escucha en todas las interfaces, activa autenticación básica (usuario `oece`, clave de `OECE_PANEL_PASSWORD` **nunca mostrada ni impresa**, o clave temporal generada y mostrada al iniciar) y **limita a cinco intentos fallidos por IP en 60 segundos**, además del token CSRF, Host y Origin. No ejecuta instrucciones dentro de documentos, macros, fórmulas ni conexiones externas. Las cargas tienen límites y nombres/rutas controlados, se rechazan symlinks/junctions y se conservan revisiones. Las citas y cotejos OCR identifican fuente, hash, localizador y autor declarado; no hay autenticación institucional del revisor. El panel actual no realiza llamadas a APIs de modelo: «Analizar con mi IA (MCP)» solo copia instrucciones para el cliente elegido. Las políticas de transmisión al proveedor, si las hubiera, corresponden al cliente de IA, no al panel.

La raíz por defecto es `./data/operacion`, derivada de `OECE_DATA_DIR=./data` (relativa al directorio de trabajo). Puede trasladarse a un volumen local, una máquina Linux u otro servidor autorizado por el titular. Los archivos se almacenan/procesan en el equipo donde se ejecute el motor; no se suben a GitHub. Los originales normativos pueden residir en `OECE_DATA_DIR/normativa/originales` con la jerarquía de los manifiestos; el código admite asimismo rutas privadas históricas del checkout. El panel escucha en `127.0.0.1` salvo `--host` explícito. En modo servidor usa autenticación básica, pero **no cifra conexiones HTTP ni sustituye autenticación institucional**. Para acceso remoto, usar SSH/VPN o un proxy HTTPS con control de acceso; no exponer directamente el puerto a Internet. La ejecución no implica cumplimiento de las políticas del titular ni autorización para publicar datos.

## OCR portátil

El OCR en Windows conserva el motor nativo existente. Fuera de Windows, o sin ese motor, se selecciona Tesseract (`pytesseract`, idioma `spa`), sin modificar originales. Las transcripciones conservan SHA-256 de fuente/imagen, cajas de texto, límites y caché; cualquier hecho obtenido queda sujeto a cotejo humano/IA declarado. En Ubuntu instalar `tesseract-ocr`, `tesseract-ocr-spa` y `poppler-utils`. La disponibilidad OCR no es requisito para procesar documentos digitales.

## Migración de rutas almacenadas

Las rutas relativas se persisten con `/` (POSIX) y se resuelven con `pathlib`. El lector admite por compatibilidad registros antiguos con `\\`, pero rechaza componentes `..`, rutas UNC y rutas con unidad de Windows cuando se espera una ruta relativa. El comando `python -m oece migrar-rutas` migra índices JSON/SQLite privados con respaldo; no altera hashes de documentos originales y requiere detener escritores para evitar cambios concurrentes. Los índices y respaldos siguen fuera de Git.


## Tratamiento de PDFs mediante IA externa (opt-in)

El flujo agnóstico actual no requiere una API en OECE. El panel copia instrucciones y el cliente conectado por MCP puede recibir páginas escaneadas como imágenes. **El cliente puede enviar esas imágenes a su proveedor**, según su configuración y política de datos, por lo que igualmente se requiere autorización para procesar expedientes reales. La CLI histórica separada `python -m oece analizar-ia ... --autorizar-envio` aún dispone de API OpenAI opt-in: no se invoca desde el panel ni MCP, y no es necesaria para el flujo agnóstico. `--previsualizar` no usa red.

La API puede tener costes y los PDFs pueden contener datos personales, firmas y contratos sometidos a deberes de reserva. Antes de su uso institucional deben verificarse la autorización para transmitirlos y las condiciones de privacidad, retención y ubicación de procesamiento del proveedor. Las solicitudes se hacen con `store:false`; para archivos PDF grandes se utiliza carga temporal en Files API con intento de eliminación al terminar. **No se garantiza eliminación inmediata de los registros que la política del proveedor pueda conservar**. Los reportes, copias de originales y transcripciones se conservan en almacenamiento privado local con huellas SHA-256; nunca en el repositorio. Los textos de los PDFs se tratan como datos no confiables, no instrucciones. Las citas visuales y las operaciones aritméticas son propuestas condicionadas a cotejo humano con el documento original y norma aplicable; no son acreditaciones automáticas.


## Aislamiento de expedientes en MCP (modo histórico)

**Perfil recomendado:** iniciar con `python scripts/servidor_mcp.py --caso EXP-001`, o `OECE_MCP_CASO=EXP-001`. Con la sesión vinculada, `oece_listar` muestra únicamente ese expediente; `oece_nuevo` queda bloqueado; las llamadas a herramientas para otro `caso` y el acceso a sus URIs `oece://casos/...` se rechazan. **Esto limita el puente MCP**, pero no los permisos de la propia máquina virtual, usuario del sistema operativo u otros conectores de la IA.

**Importación protegida:** `oece_incorporar(caso,origen)` solo acepta un archivo situado dentro de `<raiz>/entrada/<caso>/`, con `origen` relativo a ese directorio. No se pueden utilizar `../`, rutas absolutas ni enlaces simbólicos para abrir documentos ajenos. El panel puede seguir subiendo originales directamente a `documentos/`. En uso administrativo, sin `--caso`, el puente mantiene acceso a múltiples expedientes y **no equivale a una sesión aislada**.

**Autenticación del panel:** nunca registrar la contraseña suministrada por `OECE_PANEL_PASSWORD`. Se presenta por consola una clave **solo si el programa la genera**. El control de intentos por IP es una barrera básica; configurar también bloqueo/rate limit en el proxy o VPN. Si se usa un proxy, varias personas pueden compartir la misma IP vista por el proceso; no confiar en `X-Forwarded-For` enviado por el cliente. Mantener la publicación HTTP deshabilitada frente a internet.

**Conectores Drive y repo público:** que los documentos sean públicos o utilizables no implica que deba hacerse pública la carpeta de Drive. Revisar explícitamente los permisos de lectura/escritura compartida. El repositorio enlaza la carpeta normativa: el enlace no garantiza acceso, pero expone su identificador; no insertar URLs privadas de expedientes ni tokens en el código. Permisos efectivos de Drive **no auditados desde este repositorio**.
