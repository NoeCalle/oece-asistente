# Primer uso de OECE Assistant

Preparación técnica comprobada el 02/11/2026, versión 1.6. La herramienta está preparada para elaborar borradores con el asistente conversacional, fuentes y evidencias. El formato institucional se adaptará cuando lo recibas.

## Cuando empieces a trabajar

1. Abre **INICIAR_OECE.cmd** y pulsa **Comprobar equipo**. El resultado distingue herramientas disponibles y fecha de la biblioteca.
2. Crea el expediente, elige el trámite e incorpora documentos en la ubicación autorizada para tu trabajo. Los archivos de Drive sincronizado deben estar descargados.
3. Indica al asistente: **«Revisa este expediente de [trámite] en [carpeta], contrasta las fuentes y prepara el informe con su matriz»**. Debe buscar los datos antes de preguntarte.
4. Revisa la propuesta y las observaciones. Informe editable, matriz y originales se conservan por revisión; nueva información genera otra versión.

Puedes comenzar con la plantilla provisional. Al recibir un informe laboral autorizado ajustaremos encabezado, apartados, tablas, redacción y presentación. Lectura, reglas y trazabilidad permanecen separadas del formato.

## Qué está preparado

Los cinco trámites: ampliación de consultores, aumento CMC, inscripción/reinscripción, actualización y reconsideración. El plan contiene 124 unidades de revisión y 153 citas verificadas. Cada expediente registra los hechos acreditados y la interpretación de su autor; las tareas del plan no equivalen a cumplimiento.

Disponibles: panel, lectura de formatos admitidos, OCR Windows acotado, búsqueda normativa, cálculos, Word/matriz, revisiones, diagnóstico y respaldo/restauración. Se comprobaron 220 pruebas, cinco expedientes ficticios completos y el recorrido de navegador con descarga y diagnóstico visible. [Evidencia](VERIFICACION_V16.md).

La interpretación la aporta el asistente elegido; no se requiere una API propia. Codex es el cliente actual. El puente tiene catorce herramientas; la sesión y permisos de otro cliente se comprueban al configurarlo. [Portabilidad](PORTABILIDAD_IA.md).

## Revisión normal de cada expediente

El coordinador fija fechas, comprueba fuentes oficiales y delimita régimen, rama y excepciones. La biblioteca se conserva hasta el **31/10/2026**; una solicitud posterior requiere verificar modificatorias y actualizar cobertura/pruebas antes de ampliar conclusiones. Cambiar la fecha del equipo no acredita vigencia.

Se revisa el contenido de los documentos, no solo sus títulos. OCR dudoso, antecedentes incompletos, representación, información financiera y calendarios se resuelven con originales y datos del caso. Los puntos pendientes conservan ese estado hasta tener sustento.

Con el primer expediente laboral se confirman ubicación/permisos, funcionamiento con sus documentos y aceptación de la propuesta. Eso depende del trabajo real; no se atribuye a los ejemplos ficticios. DOC/XLS antiguos, imágenes incrustadas y fuentes parcialmente legibles conservan los límites de [uso diario](USO_DIARIO.md).

## Respaldo y recuperación

El respaldo ZIP conserva la carpeta del expediente: originales, hechos, análisis y todas sus revisiones. La recuperación exige una carpeta nueva y compara las huellas. Mantén la copia en una ubicación autorizada; el programa no la comparte ni la sube automáticamente.

Comandos para el coordinador o mantenimiento:

```text
python -m oece diagnostico --fecha AAAA-MM-DD
python -m oece respaldar RUTA_EXPEDIENTE RUTA_RESPALDO.zip
python -m oece restaurar RUTA_RESPALDO.zip CARPETA_NUEVA
```

Límite: 1 GB y 5.000 archivos. No se reemplazan copias ni carpetas existentes. Se rechazan alteraciones, rutas externas, enlaces y nombres incompatibles. Se captura la carpeta indicada, no la configuración externa de tus cuentas.

## Qué aportarás después

El modelo de informe autorizado permitirá personalizar la entrega. El primer expediente autorizado permitirá comprobar el uso laboral y la normativa de sus fechas. Puedes conocer el flujo con los ejemplos actuales mientras recibes el formato.

[Estado](ESTADO.md), [plan original](PLAN_INTEGRAL.md). La preparación técnica no equivale a certificación jurídica general ni aceptación institucional.
