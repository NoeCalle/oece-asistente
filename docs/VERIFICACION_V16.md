# Verificación de preparación 1.6

02/11/2026. **220 pruebas aprobadas:** 188 anteriores, dieciséis de preparación/diagnóstico, trece de respaldo/restauración y tres de citas normativas Word. Corte normativo conservado: 31/10/2026.

## Cobertura de preparación

El [registro 1.6](../rules/requisitos.v1.6.json) contiene 124 unidades: diez de ampliación, catorce de aumento, 63 de inscripción, 27 de actualización y diez de reconsideración. Incluye trece fichas de inscripción, doce supuestos del Anexo 5 y los siete numerales del artículo 113, incluido el numeral 7 que continúa en otra página.

Se verifican cinco originales, 178 referencias y 153 citas. Las listas de inscripción usan el bloque físico Requisitos de cada página, con pdfplumber 0.11.9. Recorte, página y cita quedan registrados; se evita mezclar la descripción que el orden de extracción intercala entre requisitos. Las continuaciones conservan ambos pasajes. No se afirma segmentación jurídica exhaustiva de cada literal dentro de un requisito complejo.

Actualización incorpora 9.6.1–9.6.7, ramas financieras y Anexo 5 Word, con localizadores y columnas combinadas. Una celda vacía no crea un documento ni prueba por sí sola una excepción. Se renderizó e inspeccionó el anexo original en sus tres páginas sin modificarlo.

Las tareas siguen pendientes de interpretación. El plan orienta al coordinador y se conserva en matriz JSON; no concede cumplimiento ni reemplaza los hechos citados de los controles.

## Pruebas y operación

- Selección de ocho ramas de obras, bienes/servicios y alternativas ante datos ausentes.
- Supuestos y columnas de actualización; celdas combinadas/vacías; separación legal/financiera y continuación del recurso.
- Reconstrucción reproducible; recorte o cita alterados rechazados; fuentes y bytes comprobados antes de reutilizar el cotejo textual.
- Diagnóstico de dependencias, originales, índice y plan. La preparación técnica no habilita vigencia para una fecha posterior al corte.
- Respaldo/restauración idénticos, sin reemplazar copias ni destino; límites, hash, entradas extra, colisiones Windows, enlaces y rutas de escape. Un caso vacío recupera su carpeta documentos. Se comprueba el reintento ante un bloqueo transitorio de Windows sin sobrescribir el destino.

Cinco expedientes ficticios produjeron Word, matriz y plan. Se recuperó un caso de consultores desde respaldo y se procesó. Un respaldo final de inscripción se restauró con su Word íntegro. No se atribuye validación laboral a estos ejemplos.

Panel actualizado en Edge: creación, ficha, booleanos, carga, procesamiento, descarga Word, actualización financiera y botón Comprobar equipo. Cero errores JavaScript observados. Diagnóstico final: ocho comprobaciones técnicas satisfactorias, OCR Windows disponible y revisión normativa requerida para 02/11/2026.

Los cinco nuevos Word se comprobaron estructuralmente. El informe final de actualización con cita del Anexo 5 se renderizó y revisó en sus tres páginas. Los otros cuatro nuevos Word no reciben esa QA visual por herencia; las seis páginas 1.5 y las revisiones anteriores conservan su evidencia histórica. Cada informe laboral se revisará visualmente con su contenido final.

Se comprobaron citas normativas DOCX por bloque/celda, rechazo de localizadores o citas falsos y conservación de dos citas del mismo anexo en Word. El cotejo de PDF reutiliza la extracción de cada página/recorte manteniendo el hash de los bytes en cada llamada; evita repetir trabajo y permite responder por MCP dentro del ensayo. La respuesta de acceso denegado del panel consume cuerpos pequeños antes de cerrar la conexión, para conservar el error HTTP en Windows.

## Fuentes y alcance del cierre

Biblioteca activa: 48 originales y 29 registros. Se capturó el compendio oficial de El Peruano, idNorma 25: 6.186.402 bytes, 294 páginas declaradas, SHA-256 `cf7c1ff65674553e2bf75b999f9497061e0b5ad18ed25219f00764df0ea74bd3`. El lector produjo errores de descompresión y no obtuvo texto útil en las páginas examinadas. Queda como candidato local, sin promoverlo a reglas ni ampliar la ventana. No se declara ausencia de modificatorias por ese intento.

Cierre: **preparación técnica para borradores asistidos**. La plantilla laboral se adapta al recibirla. Vigencia, régimen, hechos y aceptación del primer caso real se comprueban en su contexto. La cadena temporal completa del plan amplio y la sesión real de otro cliente conservan sus pendientes.

[Primer uso](PRIMER_USO.md), [ejecución](../proyecto/ejecuciones/preparacion-v16-2026-11-01.json), [estado](ESTADO.md).
