# Verificación de la versión asistida v1

Fecha: 31/10/2026. Historias verificadas: expediente local → lectura → hechos citados → selección y matriz → borrador Word; panel → API → carpeta/memoria → descarga. Solo datos sintéticos y fuentes normativas públicas.

## Resultados comprobados

| Frontera | Evidencia | Resultado |
|---|---|---|
| Interfaz a servidor | Edge de prueba: crear expediente, guardar ficha y subir TXT | Correcto |
| Servidor a documentos | Carga conservada, procesamiento en cola y revisión creada | Correcto |
| Entrega a interfaz | Descarga Word con paquete DOCX válido; cero errores JavaScript observados | Correcto |
| Motor documental | Diez situaciones S01–S10 implementadas en test_operacion_v1.py, sobre hechos sintéticos citados | Correcto en el alcance probado |
| Revisión e integridad | Repetición idempotente, cambio produce otra revisión, originales conservados, alteración rechazada | Correcto |
| Vigilancia | LISTO más estabilidad; memoria de procesamiento sobrevive al reinicio | Correcto |
| OCR real | Windows, imagen pública 3.392 caracteres; PDF escaneado de prueba 3.394 caracteres | Lectura candidata con alerta de cotejo, sin confianza inventada |
| OCR controlado | Timeout/reanudación; cita OCR bloqueada hasta cotejo declarado; se conserva texto anterior e imagen/autor | Correcto en pruebas sintéticas |
| Biblioteca | 47 fuentes; 2.280 fragmentos, 2.045 con texto; consulta de reconsideración recupera TUO MINJUSDH p. 194 | Correcto como recuperación textual |
| Presentación Word | DOCX generado y abierto en Word mediante automatización; exportación PDF bloqueada | **QA visual completa pendiente** |

**87 pruebas aprobadas**, ejecutadas con Python del entorno. Son 53 anteriores y 34 nuevas; no constituyen medición de precisión jurídica ni aceptación por un especialista. Los diez casos del archivo original v0.1 se conservan como especificación histórica sin alterar sus banderas; su implementación nueva consta en los tests S01–S10 y el registro v1.

## Demostración documental

Cuatro documentos ficticios y doce interpretaciones citadas. Honorarios finales PEN 100.000; comprobantes PEN 80.000; el control registra una diferencia de PEN 20.000 sin recurrir al presupuesto de ejecución de obra. La participación en consorcio sin obligaciones identificadas queda indeterminada. Los resultados favorables son verificaciones documentales limitadas a la evidencia y al autor registrados.

Se probó creación y descarga por navegador de un segundo expediente de interfaz sin datos reales. No se probaron casos laborales, consultas en vivo a registros ni presentación de trámites. No se simuló una aprobación humana ni un agente autónomo integrado al panel.

## Límites y problemas encontrados

La primera suite ampliada detectó fixtures antiguos que no incluían el quinto manifiesto y un handle SQLite no cerrado; se corrigieron. Se añadió reintento acotado de publicación atómica por bloqueos transitorios de OneDrive/antivirus. El OCR invocado desde Python no encontraba Get-FileHash en Windows PowerShell: se sustituyó por SHA256 de .NET, y después se comprobó reconocimiento real.

El renderizador de documentos del entorno falló por ausencia de LibreOffice. Word abrió una copia temporal del borrador, pero las dos vías de conversión PDF probadas no terminaron. Se detuvieron únicamente los procesos auxiliares creados para esas pruebas; no se tocó la instancia previa del usuario. **No se inspeccionaron PNGs de todas las páginas del Word v1 ni se declara verificada su presentación.** Los renders del Word anterior pertenecen a su revisión histórica y no sustituyen este control.

Las fuentes PDF con advertencias de estructura y las páginas con lectura insuficiente conservan su necesidad de revisión. XLS antiguo no se lee automáticamente; XLSX devuelve valores almacenados con fórmulas marcadas. Las citas textuales prueban procedencia, no verdad semántica, autenticidad ni vigencia normativa general. El análisis abierto y la comprobación de contenido son trabajo del coordinador en Codex.

## Reproducción

```text
python -m unittest discover -s tests -p "test_*.py"
python scripts/crear_demo_operativo.py CARPETA_NUEVA
python -m oece procesar CARPETA
python scripts/verificar_biblioteca.py --verificar-originales
python -m oece biblioteca --reconstruir
python -m oece biblioteca --buscar "reconsideración nueva prueba"
```

En Windows restringido, las pruebas HTTP requieren acceso a conexiones locales 127.0.0.1. El resto de pruebas usa archivos sintéticos. Los archivos binarios de biblioteca están excluidos de Git y deben estar disponibles para las comprobaciones de originales.
