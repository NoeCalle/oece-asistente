# Uso diario de OECE Assistant

## Trabajo con el coordinador

Abre este proyecto en Codex o en otro asistente con acceso autorizado al motor y los documentos, y escribe, por ejemplo: **«Este proveedor solicita ampliar su categoría. Revisa la carpeta [ruta] y prepara el informe»**. Las instrucciones del proyecto coordinan lectura, normativa, hechos con citas, análisis y Word. No necesitas conocer los comandos. El coordinador debe pedir solo los datos que no encuentre en los documentos.

El formato de Word es provisional. Cuando dispongas de informes reales autorizados, podremos adaptar sus apartados, lenguaje y presentación conservando el mismo circuito de evidencias. No se necesita esperar esos ejemplos para preparar borradores.

## Panel de carpetas

Abre **INICIAR_OECE.cmd** desde esta carpeta. El panel se abre en el navegador de tu equipo. Crea el expediente, selecciona el trámite e incorpora sus documentos. **Preparar borrador** ejecuta lectura, selección, matriz y Word. **Continuar con mi asistente** copia un pedido con la ruta del expediente para pegarlo en el cliente elegido. Una ruta de este equipo requiere acceso local; no da acceso desde un chat remoto por sí sola.

La interpretación se realiza en el asistente elegido, como pidió el usuario el 01/11/2026. Codex está probado; el puente para otros clientes se verifica a nivel de protocolo y herramientas. No es necesario añadir un modelo propio al panel. Sus instrucciones guiadas y generación local funcionan sin configurar una API nueva. No se declara una integración automática con un modelo en segundo plano.

## Carpetas locales o Drive sincronizado

Cada expediente tiene `expediente.json` y una subcarpeta `documentos`. El coordinador puede crear esa estructura. Una carpeta puede estar en una unidad local o Google Drive sincronizado. Los archivos deben estar descargados completamente; seleccionar **conservar siempre en este dispositivo** cuando corresponda. No basta un acceso directo a un documento de Google.

Para activar la preparación automática, crear un archivo llamado **LISTO** en la carpeta del expediente. Mientras el panel está abierto, comprueba periódicamente las carpetas de su raíz, espera estabilidad y prepara una revisión nueva si cambian los originales, la ficha o el análisis. La vigilancia guarda estado y evita repetir una entrega sin cambios. Los errores se conservan y se reintentan hasta tres veces; un procesamiento manual permite corregir y volver a ejecutar. El análisis libre con IA se inicia conversando con el asistente elegido, que debe tener acceso al motor y al expediente.

La carpeta predeterminada es `data/operacion` dentro de este proyecto. **Esta copia del proyecto está en OneDrive**: su contenido puede sincronizarse con esa cuenta. Para expedientes laborales usa la ubicación autorizada por tu organización. El programa no sube expedientes a GitHub ni a Drive mediante API, no cambia permisos y no presenta trámites. Si una raíz externa no está autorizada en la sesión de Codex, seleccionar una carpeta permitida o conceder acceso a esa ubicación en el momento de usarla.

## Entregas

Cada revisión conserva informe Word editable, matriz CSV, matriz JSON con citas, manifiesto de integridad y originales. La incorporación de información produce otra revisión sin sobrescribir la anterior. Los duplicados de contenido se identifican; una entrega alterada se rechaza para que se revise su integridad. El estado y las conversaciones guiadas se guardan localmente en SQLite.

Los cinco trámites tienen controles documentales propios. La versión 1.1 añade propuestas de capacidad de ejecutores y plazos de actualización/reconsideración; para inscripción selecciona registro y modalidad, y para actualización clase y motivo. Las conclusiones dependen de hechos con citas que interpreta el coordinador, no de marcar una casilla en el panel. Los cuatro módulos adicionales se limitan automáticamente a solicitudes del 01/05–31/10/2026; fechas posteriores requieren verificar y actualizar fuentes. [Datos y límites por procedimiento](CONTRATO_PROCEDIMIENTOS.md).

## Lectura y OCR

Se leen PDF digital, Word DOCX con tablas/encabezados/pies, TXT, HTML y valores almacenados de XLSX. Las imágenes y páginas PDF con lectura insuficiente pasan a OCR de Windows. El OCR tiene límite por lote y por página; conserva caché y puede reanudar. Los errores y textos pendientes se muestran. No se inventa un porcentaje de confianza. Fórmulas de Excel, imágenes incrustadas en Word, cuadros de texto, revisiones y formatos DOC/XLS antiguos requieren conversión o inspección específica.

## Instalación y comandos de mantenimiento

En este equipo se utiliza Python del entorno de Codex, pypdf, python-docx, Pillow, Poppler y OCR de Windows. Para otra instalación: Python 3.12 o posterior y `pip install -r requirements-indexacion.txt`; instalar/configurar Poppler y un idioma de OCR Windows, por ejemplo español de México. El lanzador acepta -Python o OECE_PYTHON y busca .venv/PATH; conserva el entorno de Codex como alternativa en este equipo. En otro equipo configurar un Python compatible según los comandos siguientes.

```text
python -m oece panel --raiz RUTA_AUTORIZADA --puerto 8765
python -m oece nuevo CARPETA --procedimiento ampliacion_consultores --solicitante NOMBRE
python -m oece leer CARPETA
python -m oece procesar CARPETA
python -m oece observar RAIZ_DE_EXPEDIENTES
python -m oece biblioteca --reconstruir
python -m oece biblioteca --buscar "ampliación categorías"
python -m unittest discover -s tests -p "test_*.py"
```

Cerrar el navegador no detiene el proceso local. Para detenerlo, cerrar el proceso de Python del panel desde el administrador de tareas o detener la terminal si se inició allí. No se instala como servicio de inicio automático. El panel escucha únicamente en 127.0.0.1 y aplica controles de origen y token a las escrituras; no es un portal multiusuario ni un sistema institucional de autenticación.

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
