# OECE Assistant

Coordinador en Codex y herramientas locales para preparar evaluaciones documentales OECE/RNP con fuentes, matriz y borrador Word editable.

**Versión asistida 1.2.0 — cierre 01/11/2026; corte normativo 31/10/2026.** Panel de expedientes, lectura PDF/Word/HTML/XLSX, OCR acotado, memoria y entregas versionadas. La interpretación abierta se realiza en Codex siguiendo [AGENTS.md](AGENTS.md). El panel ejecuta herramientas deterministas, sin modelo autónomo incorporado. El usuario confirmó que la interpretación y coordinación en Codex es el funcionamiento deseado; no se requiere añadir un modelo al panel para completar este alcance.

## Empezar

1. Abrir **INICIAR_OECE.cmd** en este equipo.
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
| Operación local | Panel, carga, LISTO, estabilidad, memoria, bloqueo, reintentos y revisiones |
| Lectura/OCR | PDF digital, DOCX, TXT/HTML, valores XLSX; OCR Windows con límites, caché y cotejos declarados |
| Entregas | Word/CSV/JSON; cinco ejemplos y 19 páginas de 1.1, dos ejemplos financieros y diez páginas de 1.2 inspeccionados |
| Contraste financiero | R2/R3/R8, SBS documentada, indicadores y detección de contradicciones; sin dictamen de solvencia |
| Biblioteca | 29 registros, 48 archivos, seis manifiestos, 2.281 fragmentos y 2.046 con texto |
| Pruebas | 131; navegador con carga, campos, procesamiento y descarga Word comprobados |

Los cuatro módulos adicionales tienen una ventana automática deliberadamente acotada al **01/05–31/10/2026**. Fuera de ella, los resultados favorables/desfavorables pasan a no determinable hasta revisar fuentes. Los cálculos son propuestas documentales: no prueban autenticidad, consulta registral en vivo ni decisión administrativa. [Contrato de procedimientos](docs/CONTRATO_PROCEDIMIENTOS.md).

Avance orientativo del plan amplio: **75 % (70–80 %)**. Es una estimación de entregables, no precisión jurídica ni aceptación institucional. [Estado](docs/ESTADO.md) y [medición](docs/MEDICION_AVANCE.md).

## Documentación

- [Uso diario](docs/USO_DIARIO.md), [datos del expediente](docs/CONTRATO_EXPEDIENTE.md), [procedimientos](docs/CONTRATO_PROCEDIMIENTOS.md) y [verificación 1.2](docs/VERIFICACION_V12.md) y [contraste financiero](docs/CONTRASTE_FINANCIERO.md).
- [Plan integral](docs/PLAN_INTEGRAL.md), [roadmap](ROADMAP.md), [tareas](docs/TAREAS.md) y [cierres](docs/CIERRES.md).
- [Criterios adoptados](docs/normativa/CRITERIOS_ADOPTADOS_PILOTO.md), [consultores](rules/consultores/criterios-documentales.v1.json) y [fuentes de procedimientos](rules/procedimientos.v1.1.json).
- [Biblioteca](docs/normativa/OPERACION_V1.md), [catálogo](normativa/catalogo.json), [esquema normativo](schemas/norma.schema.json) y [seguridad](docs/SEGURIDAD.md).

## Datos y reproducción

Repositorio público: código, documentación y metadatos públicos. Expedientes, Word, transcripciones, originales e índices van en `data/` o raíz privada, excluidos de Git. Esta copia está bajo OneDrive; para documentos laborales se debe usar una ubicación autorizada. El programa no publica expedientes, comparte permisos ni presenta trámites.

Dependencias en [uso diario](docs/USO_DIARIO.md). La reconstrucción de biblioteca requiere los originales conservados fuera de Git; las pruebas usan documentos ficticios.

```text
python -m unittest discover -s tests -p "test_*.py"
python scripts/verificar_biblioteca.py --verificar-originales
python -m oece biblioteca --reconstruir
python -m oece panel
```
