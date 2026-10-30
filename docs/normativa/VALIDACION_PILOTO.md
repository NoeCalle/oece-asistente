# Validación de la preparación del piloto
Fecha de ejecución: 2026-10-30. Corte normativo investigado: 2026-10-29.

Se ejecutó scripts/verificar_biblioteca.py --verificar-originales con Python del entorno y validación JSON Schema del catálogo con PowerShell Test-Json.

Resultado:
- 23 registros normativos; sin IDs duplicados, relaciones rotas ni fuentes fuera de los dominios oficiales permitidos.
- 24 archivos manifestados: 23 del primer lote y captura HTML oficial del comunicado.
- Tamaño y SHA-256 de las 24 copias locales coinciden con sus manifiestos.
- 22 controles candidatos, con fuentes y hashes coherentes; páginas dentro del documento registrado.
- 10 casos sintéticos especificados y pendientes de ejecución, vinculados a controles existentes.
- 15 enlaces locales de docs/ resueltos sin errores.
- Catálogo conforme al JSON Schema existente.

La comprobación de páginas valida límites numéricos, no interpreta el contenido. Se inspeccionaron visualmente las páginas identificadas en HALLAZGOS_PILOTO.md. Los documentos restantes requieren su propia revisión.
La matriz sigue deshabilitada; ninguna aprobación humana está registrada. Estos resultados no son pruebas funcionales del asistente ni certificación de vigencia normativa.

Para repetir:
```text
python scripts/verificar_biblioteca.py
python scripts/verificar_biblioteca.py --verificar-originales
```
La primera modalidad funciona con metadatos del repositorio; la segunda requiere las copias locales excluidas de Git. No requiere paquetes externos.
