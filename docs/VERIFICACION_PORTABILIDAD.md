# Verificación de portabilidad de IA

Versión 1.3, 01/11/2026. **154 pruebas aprobadas**, incluidas 23 nuevas del puente local. El motor de IA no se integra al panel; el cliente elegido invoca las herramientas.

## Comprobaciones realizadas

- Proceso stdio real desde un directorio distinto del repositorio, descubrimiento MCP 2026-07-28 y negociación initialize 2025-11-25. El catálogo de once herramientas coincide entre ambos perfiles.
- Lectura de originales con ID, huella, localizadores y paginación; normas solo desde originales manifestados con comprobación de hash/página.
- Raíz de acceso explícita, rechazo de recorridos externos, nombres reservados y argumentos desconocidos. No hay herramienta de shell ni puerto público.
- Escritura de entradas con hash esperado y copia previa conservada. ID y condición sintética no se pueden cambiar; el puente no atribuye hechos/cotejos nuevos a un humano.
- Una cita falsa guardada se rechaza al generar. Dos autores IA de prueba usan el mismo control y reciben el mismo resultado documental, conservando su autoría. Son perfiles de prueba, no dos modelos reales.
- Generación Word/matriz y recuperación por recurso MCP, con rechazo de entregas alteradas y URIs fuera del alcance. El Word recuperado tiene estructura DOCX; no se presenta como informe visualmente revisado en un cliente externo.
- Configuración local revisable generada sin claves de modelo ni edición de aplicaciones. Resolución de Python explícito/variable de entorno/.venv/PATH y alternativa de compatibilidad del equipo.
- Panel con mensaje neutral para el asistente elegido; el flujo de navegador se comprueba tras reiniciar el proceso actualizado.

Los cinco ejemplos/19 páginas de 1.1 y los dos ejemplos/diez páginas de 1.2 permanecen como revisiones históricas verificadas. La portabilidad no sustituye el cotejo visual de cada informe nuevo.

## Alcance demostrado y pendiente

**Demostrado:** contrato común, protocolo stdio, lectura, cálculos/controles existentes, evidencias, generación y recuperación local. Se ejecuta sin solicitar una clave API de modelo. Los originales normativos disponibles siguen siendo 48; el corte no se amplía.

**No demostrado:** inicio de sesión de Claude, autorización de sus conectores GitHub/Drive, lectura automática de las instrucciones en su aplicación, disponibilidad de OCR/archivos en otro sistema operativo o visualización/descarga nativa del Word en ese cliente. Se valida cuando el usuario conecte el cliente elegido. No se garantiza interpretación idéntica entre IAs.

[Guía y fuentes oficiales del protocolo/cliente](PORTABILIDAD_IA.md). [Registro estructurado](../proyecto/ejecuciones/portabilidad-v13-2026-11-01.json). La estimación del plan se mantiene en 75 %; cadena normativa, casos reales y modelos laborales conservan sus pendientes.
