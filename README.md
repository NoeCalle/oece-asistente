# OECE Assistant

Asistente conversacional elegido y herramientas locales para preparar evaluaciones documentales OECE/RNP con fuentes, matriz y borrador Word editable.

**Versión asistida 1.6.0 — cierre 02/11/2026; corte normativo 31/10/2026.** Panel de expedientes, lectura PDF/Word/HTML/XLSX, OCR acotado, memoria y entregas versionadas. La interpretación la realiza el asistente elegido siguiendo [AGENTS.md](AGENTS.md). Codex es el cliente probado actualmente; se incluye un puente MCP local y [CLAUDE.md](CLAUDE.md) para clientes alternativos. La lectura multimodal opcional mediante API se activó en noviembre de 2026 con consentimiento explícito; la modalidad clásica de CLI/MCP continúa independiente de proveedor. La conexión real de Claude con Drive, GitHub y este puente todavía requiere comprobación. [Portabilidad y configuración](docs/PORTABILIDAD_IA.md).

[Guía de primer uso](docs/PRIMER_USO.md). Preparación técnica comprobada; el formato laboral se personalizará cuando se reciba. Las fuentes y condiciones se contrastan para cada expediente.

## Empezar

1. Iniciar el panel con `python -m oece panel` desde el directorio del proyecto (en Windows también está `INICIAR_OECE.cmd`) y pulsar **Comprobar equipo**.
2. Crear expediente, elegir trámite, completar los datos conocidos e incorporar documentos.
3. Preparar borrador y continuar el análisis en el chat de este proyecto indicando la carpeta.
4. Revisar Word y matriz; cada revisión conserva originales y citas.

También puedes escribir: **«Este proveedor solicita ampliar su categoría; revisa esta carpeta y prepara el informe»**. El coordinador debe buscar los datos antes de preguntar. [Uso diario](docs/USO_DIARIO.md).

Los modelos reales de informes se incorporarán cuando estén disponibles. El [formato provisional](templates/informe.v1.json) está separado de la lectura y las evidencias.

## Alcance comprobado

| Componente | Disponible |
|---|---|
| Ampliación de consultores | Selección temporal y 22 verificaciones documentales; no concesión automática de categoría |
| Aumento de CMC | Controles propios, obras/consorcios, propuesta decimal de capacidad y contraste con capacidad vigente citada |
| Inscripción/reinscripción | Ramas bienes, servicios, consultor y ejecutor; documentos/solvencia según datos de selección |
| Actualización | Legal o financiera; límites calendario del mes siguiente y del ejercicio anual |
| Reconsideración | Requisitos, nueva prueba/única instancia y propuesta de 15 días hábiles con calendario documentado |
| Recuperación | Respaldo íntegro y restauración en carpeta nueva, con huellas y sin reemplazar datos existentes |
| Operación local | Panel, carga, LISTO, estabilidad, memoria, bloqueo, reintentos y revisiones |
| Portabilidad IA | CLI y 17 herramientas MCP, incluidas páginas visuales y cálculos independientes del proveedor; sin API en el panel |
| Lectura/OCR | PDF digital, DOCX, TXT/HTML, valores XLSX; OCR Windows con límites, caché y cotejos declarados |
| Entregas | Word/CSV/JSON; cinco ejemplos y 19 páginas de 1.1, dos ejemplos financieros y diez páginas de 1.2 inspeccionados |
| Contraste financiero | R2/R3/R8, SBS documentada, indicadores y detección de contradicciones; sin dictamen de solvencia |
| Plan documental | 124 unidades de revisión de los cinco trámites, 153 citas; preparación por rama, sin acreditar cumplimiento |
| Fichas TUPA | Quince fichas/cuarenta páginas por rama, con códigos y huellas; recuperación de candidatas, sin dictamen de vigencia |
| Biblioteca | 29 registros, 48 archivos, seis manifiestos, 2.281 fragmentos y 2.046 con texto |
| Pruebas | 220; navegador con carga, campos, procesamiento y descarga Word comprobados |

Los cuatro módulos adicionales tienen una ventana automática deliberadamente acotada al **01/05–31/10/2026**. Fuera de ella, los resultados favorables/desfavorables pasan a no determinable hasta revisar fuentes. Los cálculos son propuestas documentales: no prueban autenticidad, consulta registral en vivo ni decisión administrativa. [Contrato de procedimientos](docs/CONTRATO_PROCEDIMIENTOS.md).

Avance orientativo del plan amplio: **75 % (70–80 %)**. Es una estimación de entregables, no precisión jurídica ni aceptación institucional. [Estado](docs/ESTADO.md) y [medición](docs/MEDICION_AVANCE.md).

[Consulta TUPA y límites](docs/normativa/FICHAS_TUPA.md) · [Verificación 1.6](docs/VERIFICACION_V16.md). Se corrigió también la aparición intermitente de entregas temporales en el listado de descargas.

## Documentación

- [Uso diario](docs/USO_DIARIO.md), [datos del expediente](docs/CONTRATO_EXPEDIENTE.md), [procedimientos](docs/CONTRATO_PROCEDIMIENTOS.md) y [verificación de portabilidad](docs/VERIFICACION_PORTABILIDAD.md) y [verificación financiera](docs/VERIFICACION_V12.md) y [contraste financiero](docs/CONTRASTE_FINANCIERO.md).
- [Plan integral](docs/PLAN_INTEGRAL.md), [roadmap](ROADMAP.md), [tareas](docs/TAREAS.md) y [cierres](docs/CIERRES.md).
- [Criterios adoptados](docs/normativa/CRITERIOS_ADOPTADOS_PILOTO.md), [consultores](rules/consultores/criterios-documentales.v1.json) y [fuentes de procedimientos](rules/procedimientos.v1.1.json).
- [Biblioteca](docs/normativa/OPERACION_V1.md), [catálogo](normativa/catalogo.json), [esquema normativo](schemas/norma.schema.json) y [seguridad](docs/SEGURIDAD.md).

## Linux y servidor sin escritorio

Compatible con Ubuntu (Python 3.12+) y con Windows. En Ubuntu instala Tesseract en español y Poppler:

```bash
sudo apt install -y tesseract-ocr tesseract-ocr-spa poppler-utils python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-linux.txt
bash INICIAR_OECE.sh
```

Para escuchar en la red desde un servidor sin escritorio:

```bash
export OECE_DATA_DIR=/srv/oece-data
export OECE_PANEL_PASSWORD='contraseña-larga-y-privada'
python -m oece panel --host 0.0.0.0 --port 8000
```

El modo servidor solicita usuario `oece` y contraseña; sin `OECE_PANEL_PASSWORD` genera una clave temporal en consola. **No publicar directamente el panel HTTP**: usar SSH/VPN o un proxy inverso HTTPS. El OCR utiliza Windows.Media.Ocr cuando existe y Tesseract (`spa`) en Ubuntu o cuando falta el motor Windows. Los mismos cotejos y límites se aplican a ambos. [Guía Ubuntu y Windows](docs/USO_DIARIO.md).

### Migración de índices antiguos

Los `local_path` de los manifiestos y del índice TUPA están normalizados a separadores POSIX (`/`). Se aceptan rutas heredadas `\\` mediante `pathlib`, incluidos los equipos Linux. Para actualizar índices privados existentes sin perder metadatos ni hashes:

```bash
python -m oece migrar-rutas --simular
python -m oece migrar-rutas
```

El comando migra JSON/SQLite en `OECE_DATA_DIR/normativa`, conserva respaldo por archivo e impide escapes fuera de las raíces. Ejecutarlo con el panel detenido. [Guía de uso diario](docs/USO_DIARIO.md).

## Datos y reproducción

Repositorio público: solo código, documentación y metadatos públicos. **Los datos pueden procesarse en cualquier equipo autorizado por el titular**, incluidos servidores Linux de confianza. Expedientes, Word, transcripciones, originales, índices y credenciales no se suben a Git. `data/` y `expedientes/` siguen excluidos mediante `.gitignore` (revisar los cambios antes de publicar).

La raíz privada se configura con **`OECE_DATA_DIR`**; sin variable, se usa **`./data` relativa al directorio de trabajo**. El panel, la memoria y los expedientes usan `$OECE_DATA_DIR/operacion`; los índices de biblioteca se guardan en `$OECE_DATA_DIR/normativa/indices`. Puede seguir indicándose `--raiz` para el panel/MCP. Si se usan originales normativos del manifiesto, colócalos bajo `$OECE_DATA_DIR/normativa/originales` conservando su estructura relativa; por compatibilidad también se buscan en el árbol privado heredado del repositorio.

Ejemplo en Linux/macOS:

```bash
export OECE_DATA_DIR=/srv/oece-data
python -m oece panel
```

Ejemplo en PowerShell:

```powershell
$env:OECE_DATA_DIR = 'D:\\OECE-Datos'
python -m oece panel
```

El panel permanece vinculado a `127.0.0.1`; ejecutar en otro servidor no lo convierte en servicio multiusuario ni lo expone automáticamente por red. El programa no publica expedientes, comparte permisos ni presenta trámites.

Dependencias en [uso diario](docs/USO_DIARIO.md). La reconstrucción de biblioteca requiere los originales conservados fuera de Git; las pruebas usan documentos ficticios.

```text
python -m unittest discover -s tests -p "test_*.py"
python scripts/verificar_biblioteca.py --verificar-originales
python -m oece biblioteca --reconstruir
python -m oece panel
```


## Revisión visual multi-IA (MCP, sin API ni clave en OECE)

**OECE es agnóstico:** puedes elegir Codex, Claude Code u otro cliente que admita MCP local y contenido visual de tipo `image`. No necesita `OPENAI_API_KEY`, ni paga una API adicional de OECE. El cliente seleccionado puede tener sus propios requisitos de cuenta, suscripción y tratamiento de datos; compruébalos antes de utilizar expedientes institucionales.

1. En Ubuntu o Windows instala las dependencias del proyecto y Poppler (`pdftoppm`). Ejecuta `python scripts/configurar_cliente.py` e incorpora la configuración MCP generada en tu asistente compatible (ver [portabilidad](docs/PORTABILIDAD_IA.md)).
2. Abre `python -m oece panel`, crea el expediente y carga contratos, cartas, resoluciones de recepción y liquidaciones escaneadas.
3. Pulsa **Analizar con mi IA (MCP)**. Se copia el encargo; pégalo en el cliente que tengas conectado a OECE. El panel **no envía PDFs ni llama a un modelo**.
4. El cliente usa `oece_pagina_visual` para ver cada página sin OCR previo, `oece_guardar` con el tipo `lecturas_ia` para conservar las propuestas, `oece_calcular_liquidacion` para contrastar aritmética con `Decimal` y `oece_publicar_analisis` para generar un informe Word versionado.
5. Revisa en el panel la nueva sección **Proyecto de análisis IA** y descarga `informe-ia.docx`, JSON y cálculos. Las citas visuales y cifras **siguen pendientes de cotejo humano**, y el análisis no acredita por sí solo requisitos ni vigencia normativa.

La arquitectura es independiente del modelo: **lector visual → calculista de liquidación → integrador** son roles que ejecuta el asistente elegido, no tres suscripciones. OECE conserva copias y SHA-256 dentro del expediente privado. Se prohíbe inventar cifras, páginas, firmas o decisiones. Si el cliente no soporta imágenes MCP, debe informarlo; OCR es un recurso de respaldo, no equivalente a visión. Para instrucciones completas ver [uso diario](docs/USO_DIARIO.md) y [AGENTS.md](AGENTS.md).

La ruta histórica `python -m oece analizar-ia ... --autorizar-envio` conserva una integración antigua opcional con API OpenAI; **no es necesaria ni se usa desde el panel ni desde MCP**. No hay pruebas con un cliente de IA real y documentos laborales auténticos; la regresión utiliza PDF sintéticos.
