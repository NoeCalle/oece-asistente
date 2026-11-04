# Uso diario de OECE Assistant

## Trabajo con el coordinador

Abre este proyecto en Codex o en otro asistente con acceso autorizado al motor y los documentos, y escribe, por ejemplo: **«Este proveedor solicita ampliar su categoría. Revisa la carpeta [ruta] y prepara el informe»**. Las instrucciones del proyecto coordinan lectura, normativa, hechos con citas, análisis y Word. No necesitas conocer los comandos. El coordinador debe pedir solo los datos que no encuentre en los documentos.

El formato de Word es provisional. Cuando dispongas de informes reales autorizados, podremos adaptar sus apartados, lenguaje y presentación conservando el mismo circuito de evidencias. No se necesita esperar esos ejemplos para preparar borradores.

## Panel de carpetas

Inicia el panel con `python -m oece panel` en el equipo autorizado (en Windows también puedes usar **INICIAR_OECE.cmd**). El panel se abre en el navegador de ese equipo. Crea el expediente, selecciona el trámite e incorpora sus documentos. **Preparar borrador** ejecuta lectura, selección, matriz y Word. **Continuar con mi asistente** copia un pedido con la ruta del expediente para pegarlo en el cliente elegido. Una ruta de este equipo requiere acceso local; no da acceso desde un chat remoto por sí sola.

La interpretación se realiza en el asistente elegido, como pidió el usuario el 01/11/2026. Codex está probado; el puente para otros clientes se verifica a nivel de protocolo y herramientas. No es necesario añadir un modelo propio al panel. Sus instrucciones guiadas y generación local funcionan sin configurar una API nueva. No se declara una integración automática con un modelo en segundo plano.

## Carpeta privada configurable, equipos locales o servidores de confianza

Cada expediente tiene `expediente.json` y una subcarpeta `documentos`. El coordinador puede crear esa estructura. **Los datos pueden procesarse en cualquier equipo autorizado por el titular**, sea un equipo personal, un servidor Linux de confianza o una carpeta sincronizada de Drive. Los archivos deben estar disponibles como archivos reales para el proceso; no basta un acceso directo a un documento de Google.

Para activar la preparación automática, crear un archivo llamado **LISTO** en la carpeta del expediente. Mientras el panel está abierto, comprueba periódicamente las carpetas de su raíz, espera estabilidad y prepara una revisión nueva si cambian los originales, la ficha o el análisis. La vigilancia guarda estado y evita repetir una entrega sin cambios. Los errores se conservan y se reintentan hasta tres veces; un procesamiento manual permite corregir y volver a ejecutar. El análisis libre con IA se inicia conversando con el asistente elegido, que debe tener acceso al motor y al expediente.

La raíz privada se selecciona con **`OECE_DATA_DIR`**, por defecto **`./data` relativa al directorio desde donde se ejecuta Python**. Por convención, los expedientes, el panel y la memoria quedan en `OECE_DATA_DIR/operacion`; el índice de normativa en `OECE_DATA_DIR/normativa/indices`. Para una ubicación distinta, establecer la variable en la máquina autorizada antes de iniciar el proceso. Los originales normativos pueden mantenerse bajo `OECE_DATA_DIR/normativa/originales` según sus rutas manifestadas. `--raiz` permite anular el directorio de expedientes en panel/MCP. El programa no sube expedientes a GitHub ni a Drive mediante API ni cambia permisos. El cliente de IA debe tener acceso real y autorizado a esos archivos, incluso cuando se ejecuta en otro servidor.

```bash
# Linux / macOS
export OECE_DATA_DIR=/srv/oece-data
python -m oece panel
python scripts/configurar_cliente.py
```

```powershell
# Windows / PowerShell
$env:OECE_DATA_DIR = 'D:\\OECE-Datos'
python -m oece panel
```

El MCP puede iniciarse con `python scripts/servidor_mcp.py`, que usa por defecto `OECE_DATA_DIR/operacion`; las rutas explícitas `--raiz` siguen disponibles. La configuración generada por `scripts/configurar_cliente.py` no se publica en Git. Si se trabaja desde otro directorio, `./data` cambiará: definir una ruta absoluta en `OECE_DATA_DIR` para servicios permanentes.

## Entregas

Cada revisión conserva informe Word editable, matriz CSV, matriz JSON con citas, manifiesto de integridad y originales. La incorporación de información produce otra revisión sin sobrescribir la anterior. Los duplicados de contenido se identifican; una entrega alterada se rechaza para que se revise su integridad. El estado y las conversaciones guiadas se guardan localmente en SQLite.

Los cinco trámites tienen controles documentales propios. La versión 1.1 añade propuestas de capacidad de ejecutores y plazos de actualización/reconsideración; para inscripción selecciona registro y modalidad, y para actualización clase y motivo. Las conclusiones dependen de hechos con citas que interpreta el coordinador, no de marcar una casilla en el panel. Los cuatro módulos adicionales se limitan automáticamente a solicitudes del 01/05–31/10/2026; fechas posteriores requieren verificar y actualizar fuentes. [Datos y límites por procedimiento](CONTRATO_PROCEDIMIENTOS.md).

## Lectura y OCR

Se leen PDF digital, Word DOCX con tablas/encabezados/pies, TXT, HTML y valores almacenados de XLSX. Las imágenes y páginas PDF con lectura insuficiente pasan al OCR nativo de Windows, o a Tesseract (spa) cuando el primero no está disponible. El OCR mantiene límites por lote y página, caché, huellas y reanudación en ambas plataformas. Los errores y textos pendientes se muestran. No se inventa un porcentaje de confianza. Fórmulas de Excel, imágenes incrustadas en Word, cuadros de texto, revisiones y formatos DOC/XLS antiguos requieren conversión o inspección específica.

## Rutas POSIX e índices normativos existentes

Los manifiestos y registros de OECE guardan rutas relativas con **`/`**, independientemente del sistema operativo. El motor también interpreta rutas heredadas con barras invertidas, como `normativa\\originales\\2026-10-29\\tupa-modificacion-2026-073.pdf`, mediante `pathlib`, sin suponer que `\\` sea un separador en Linux. No se admiten rutas que salgan de la raíz privada (`..`), unidades Windows ni rutas UNC como referencias relativas.

Los JSON normativos publicados en Git se han migrado a POSIX. Para migrar **índices locales anteriores** en tu equipo o servidor (SQLite y JSON), detén el panel y cualquier proceso que utilice esos archivos y ejecuta:

```bash
# Simular la migración (no cambia los archivos)
python -m oece migrar-rutas --simular

# Migrar índices en OECE_DATA_DIR/normativa
python -m oece migrar-rutas

# También puedes indicar otro directorio o un índice concreto
python -m oece migrar-rutas --ruta /srv/oece-data/normativa/indices/biblioteca.sqlite
```

Solo se reescriben campos de **rutas relativas** en registros JSON y columnas de índices SQLite. Se preservan los SHA-256 de documentos, citas y textos no relacionados con rutas. Antes de cada cambio se guarda un respaldo `.pre-rutas-AAAAmmddTHHMMSSZ.bak` junto al archivo. La migración es idempotente y no modifica los originales normativos ni expedientes. Los archivos privados deben migrarse en el equipo donde se almacenan; no pueden modificarse desde GitHub. Si un índice necesita reconstruirse, conservar siempre los originales identificados por sus hashes.

## Linux (Ubuntu)

El motor Python, el panel HTTP, los expedientes y la lectura digital pueden ejecutarse en Ubuntu con Python **3.12 o posterior**. El script [`INICIAR_OECE.sh`](../INICIAR_OECE.sh) cumple la función del lanzador Windows `INICIAR_OECE.cmd` sin requerir PowerShell ni escritorio.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip tesseract-ocr tesseract-ocr-spa poppler-utils

# Desde la raíz del repositorio (usar un Python 3.12 o posterior)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-linux.txt

export OECE_DATA_DIR=/srv/oece-data  # o ./data por defecto
bash INICIAR_OECE.sh
```

El OCR elige automáticamente **Windows.Media.Ocr** cuando está disponible en Windows; en Ubuntu (o Windows sin ese motor) usa **Tesseract** mediante `pytesseract` con idioma **`spa`**. Los PDF escaneados se renderizan con `pdftoppm` de Poppler. Se respetan los límites existentes: **45 segundos por página, 120 por lote y 10 intentos nuevos por lote**, caché de archivos y hashes SHA-256, alertas `ocr_pendiente` y `ocr_sin_cotejo_visual`. El OCR nunca acredita un hecho sin cotejo. Puede comprobarse la instalación con `tesseract --list-langs` (debe figurar `spa`), `pdftoppm -h` y `python -m oece diagnostico`.

Para ejecutarlo **sin escritorio en un servidor Ubuntu**:

```bash
export OECE_DATA_DIR=/srv/oece-data
export OECE_PANEL_PASSWORD='una-clave-larga-generada-por-ti'
python -m oece panel --host 0.0.0.0 --port 8000
```

En `--host 0.0.0.0` el panel exige autenticación básica (`usuario: oece` y la contraseña `OECE_PANEL_PASSWORD`); si no se define, genera una contraseña temporal y la muestra en la terminal. El token de escritura, comprobación de `Host` y `Origin`, protección contra traversal y las revisiones versionadas continúan activos. **El panel sirve HTTP y no incorpora TLS**: para acceder desde otra máquina, usar VPN, túnel SSH o proxy inverso HTTPS con controles de acceso, y **no exponer directamente el puerto 8000 a Internet**. Ejemplo de túnel desde el equipo cliente: `ssh -L 8000:127.0.0.1:8000 usuario@servidor`, cuando el servidor escucha en loopback.

La ruta `OECE_DATA_DIR` sigue siendo configurable en cualquier sistema y los expedientes nunca se agregan al repositorio Git. El lanzador Linux también admite `OECE_HOST=0.0.0.0` y `OECE_PORT=8000`, así como las opciones CLI `--host`/`--port`.

## Instalación y comandos de mantenimiento

Instala Python 3.12 o posterior y `pip install -r requirements-indexacion.txt` en cualquier equipo autorizado. La lectura digital PDF/DOCX/XLSX puede funcionar en Linux; en Ubuntu se utiliza Tesseract con `pytesseract` y `tesseract-ocr-spa`, sin PowerShell. El lanzador Windows acepta `-Python` u `OECE_PYTHON` y busca `.venv`/PATH. No hay dependencia de rutas de OneDrive ni de unidades de Windows.

```text
python -m oece panel --puerto 8765  # usa OECE_DATA_DIR/operacion por defecto
python -m oece nuevo CARPETA --procedimiento ampliacion_consultores --solicitante NOMBRE
python -m oece leer CARPETA
python -m oece procesar CARPETA
python -m oece observar RAIZ_DE_EXPEDIENTES
python -m oece biblioteca --reconstruir
python -m oece biblioteca --buscar "ampliación categorías"
python -m unittest discover -s tests -p "test_*.py"
```

Cerrar el navegador no detiene el servidor. Para detenerlo, terminar el proceso Python o el servicio que lo administra en el equipo correspondiente. No se instala como servicio de inicio automático. El panel escucha en 127.0.0.1 de forma predeterminada. Con `--host 0.0.0.0` escucha en red y exige contraseña, además de controles de origen y token; no es un portal multiusuario ni sustituye autenticación institucional o HTTPS.

## Presentación de Word verificada

Se revisaron visualmente cinco ejemplos sintéticos de la versión 1.1 (19 páginas), usando LibreOffice local para convertirlos y examinar todas sus páginas. Esta verificación no reemplaza la revisión de cada informe nuevo, especialmente tablas largas o documentos reales. El bloqueo de exportación de la versión anterior queda superado para este circuito; el formato continúa provisional. [Evidencia](VERIFICACION_V11.md).

## Contraste financiero desde 1.2

El coordinador prepara importes con citas y bases homogéneas. El informe incorpora R2/R3/R8, indicadores referenciales y reporte SBS documentado, con detección de contradicciones respecto de una declaración de solvencia. No convierte ratios en un dictamen ni aplica la excepción PC cero de CMC a solvencia. [Contrato financiero](CONTRASTE_FINANCIERO.md) y [verificación](VERIFICACION_V12.md). El corte no se amplía.

## Otro asistente de IA

Leer [portabilidad](PORTABILIDAD_IA.md). GitHub guarda instrucciones y reglas; Drive contiene documentos; la CLI o el MCP local ejecutan lectura/cálculo/Word. Las autorizaciones no se trasladan entre cuentas. Se generó una configuración local revisable, pero no se modificó ni inició una aplicación Claude.

## Consultar la ficha TUPA

El coordinador puede consultar `oece_tupa` por MCP o `python -m oece tupa RUTA_EXPEDIENTE`. Recibe fichas candidatas según los datos conocidos y puede leer cada página por su código oficial. No debe sumar los requisitos de todas las candidatas ni confundir una fecha dentro del corte con vigencia confirmada. [Cobertura de quince fichas y límites](normativa/FICHAS_TUPA.md).

## Plan de revisión de documentos

Para ampliación de consultores y aumento CMC, el coordinador puede consultar oece_requisitos por MCP o `python -m oece requisitos RUTA_EXPEDIENTE`. El plan separa las listas por experiencia, devuelve citas y queda conservado en la matriz JSON. Sus tareas permanecen pendientes de interpretación; no sustituyen el análisis ni son documentos ya acreditados. [Guía](normativa/REQUISITOS_AMPLIACIONES.md).

## Inicio preparado y respaldo

[Guía breve para comenzar](PRIMER_USO.md). El botón **Comprobar equipo** revisa herramientas, biblioteca e índice; distingue el resultado técnico de la fecha normativa. La preparación documental ya cubre los cinco trámites con 124 unidades y 153 citas.

El asistente puede crear un respaldo local con `python -m oece respaldar CARPETA ARCHIVO.zip` y recuperarlo con `python -m oece restaurar ARCHIVO.zip CARPETA_NUEVA`. La restauración exige destino nuevo y conserva originales/revisiones. La plantilla laboral se adaptará cuando sea facilitada. [Verificación](VERIFICACION_V16.md).
