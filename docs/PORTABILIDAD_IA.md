# OECE Assistant con el asistente que elijas

Decisión del usuario del 01/11/2026: Codex puede seguir siendo el cliente actual, pero las instrucciones, documentos y herramientas deben poder usarse desde otra IA, por ejemplo Claude. **No se integra una API de modelo al panel.**

## Estructura compartida

| Parte | Función | Qué cambia al pasar a otro asistente |
|---|---|---|
| Asistente elegido | Interpreta documentos, selecciona normas y redacta análisis | El cliente/modelo y sus permisos |
| GitHub | Código, instrucciones AGENTS.md, reglas y contratos versionados | Autorizar el conector GitHub del otro cliente |
| Drive o carpeta local | Normativa original, expedientes y entregas privadas | Autorizar su conector o carpeta sincronizada |
| Herramientas OECE | Lectura, OCR, cálculos, citas, Word y revisiones | Acceso al mismo motor Python, por terminal o MCP local |
| Panel | Organizar, cargar y descargar; copiar el pedido al asistente | Botón neutral Continuar con mi asistente |

Conectar solamente GitHub y Drive permite leer información, pero esos conectores no ejecutan automáticamente el motor local OECE. Para conservar el mismo circuito de cálculos/Word se necesita acceso a ese motor: terminal autorizada o el puente MCP local incluido. Los permisos y sesiones de una aplicación no se transfieren automáticamente a otra.

Las reglas y contratos son los mismos. **No se garantiza texto ni interpretación idénticos entre modelos**: se comparan las fuentes, hechos, cálculos y observaciones. Cada autor de IA queda identificado y no se convierte en revisor humano.

## Instrucciones comunes

[AGENTS.md](../AGENTS.md) es la fuente única del procedimiento. [CLAUDE.md](../CLAUDE.md) importa ese archivo para Claude Code; no contiene otra copia de las reglas. Un cliente que solo lee GitHub debe abrir AGENTS.md y seguir los documentos que referencia. No se presupone que un chat web cargue automáticamente los archivos de instrucciones de un repositorio.

Anthropic documenta el uso de [AGENTS.md y su importación desde CLAUDE.md](https://code.claude.com/docs/en/memory). También documenta [servidores MCP locales por stdio](https://code.claude.com/docs/en/mcp). Son mecanismos de cliente; todavía debe comprobarse su configuración real en la cuenta/aplicación del usuario.

## Dos formas de usar las herramientas

**Con acceso a una terminal**, el asistente puede usar los comandos de [uso diario](USO_DIARIO.md), sobre una copia local del código y una raíz documental autorizada. El motor Python no importa un SDK de proveedor ni solicita claves de modelo.

**Con MCP local**, el cliente inicia `scripts/servidor_mcp.py` y llama las herramientas OECE. El servidor se comunica por entrada/salida del proceso, no abre un puerto, no expone un servidor público y no llama a ningún modelo. No accede por sí mismo a las cuentas de Drive o GitHub.

Preparar una configuración revisable, sin editar las configuraciones de ningún cliente:

```text
python scripts/configurar_cliente.py --raiz RUTA_DOCUMENTAL_AUTORIZADA --salida data/config/oece-mcp.json
python scripts/probar_mcp.py --raiz RUTA_DOCUMENTAL_AUTORIZADA
```

El primer comando genera un bloque `mcpServers` con rutas absolutas del Python y lanzador de ese equipo. Se importa o combina en el cliente que admita MCP local; **no reemplazar su configuración completa**. No guardar ese archivo local en Git, ya que contiene rutas del usuario. No contiene una clave API de IA.

En clientes solo web, un conector remoto no obtiene acceso a procesos de este equipo por estar conectado a Drive. Debe usarse un cliente con herramientas locales o un despliegue remoto autorizado, que no forma parte de esta entrega. Anthropic distingue [conectores remotos y mecanismos locales](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp); su disponibilidad depende del producto y configuración elegidos. No se presupone una compatibilidad igual entre Claude web, Desktop, Code y Cowork.

## Preparación del equipo

Python 3.12 o posterior y las dependencias de `requirements-indexacion.txt`. Para el panel Windows se puede indicar `-Python` o `OECE_PYTHON`, usar `.venv` o un Python compatible del PATH. El entorno de Codex queda solo como alternativa de compatibilidad para este equipo.

Para buscar/cotejar normas, conservar los originales de Drive en sus rutas manifestadas y reconstruir el índice con `python -m oece biblioteca --reconstruir`. GitHub no contiene esos binarios. `oece_contexto` informa cuántos originales hay presentes; presencia no es comprobación de vigencia.

La independencia de proveedor de IA no significa independencia de sistema operativo: **el OCR implementado usa Windows** y Poppler. En otro sistema, se puede usar lectura digital o conectar las herramientas de este equipo; no se declara implementado otro motor OCR. Para Poppler, configurar `OECE_PDFTOPPM_EXE` o PATH según el entorno.

## Herramientas del puente

1. `oece_contexto`: instrucciones comunes, contratos y capacidades.
2. `oece_listar` / `oece_nuevo`: expedientes de la raíz autorizada.
3. `oece_incorporar`: copia un original desde la misma raíz al expediente sin moverlo ni sobrescribirlo.
4. `oece_archivos` / `oece_leer`: inventario con huellas y lectura paginada, con OCR opcional.
5. `oece_buscar_normativa` / `oece_norma`: recuperación local y lectura de una página PDF manifestada, comprobando su hash.
6. `oece_entrada` / `oece_guardar`: leer y registrar ficha/hechos/análisis/normas/cotejos. La edición exige el hash actual y conserva la versión previa.
7. `oece_generar`: valida y conserva la entrega; devuelve recursos Word, CSV, JSON y manifiesto.

Desde 1.4 se añade `oece_tupa`: consulta fichas candidatas por expediente y recupera páginas de la ficha con sus huellas. Desde 1.5 se añade también `oece_requisitos`, con 24 requisitos de ampliación/aumento y diez alertas. Son trece herramientas actuales. El plan conserva tareas pendientes de interpretación y no acredita cumplimiento. [Guía TUPA](normativa/FICHAS_TUPA.md).

Las herramientas se complementan con `resources/read` para recuperar una entrega por URI `oece://casos/...`. El Word se devuelve como recurso binario; la presentación o descarga depende del cliente. Leer/generar no sube nada a Drive. El conector del cliente debe efectuar una subida solo cuando esté autorizada.

Los JSON guardados son declaraciones, **no resultados ya aprobados**. La generación verifica citas, localizadores, huellas y cálculos antes de conservar una entrega. El puente no atribuye hechos ni cotejos nuevos a un revisor humano. Los originales del caso se colocan en `documentos/`; una carpeta existente no se inicializa silenciosamente.

## Perfil y límites del conector

Implementación stdio con la [revisión MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio), descubrimiento y metadatos por solicitud. Incluye negociación `initialize` para 2025-11-25, 2025-06-18 y 2024-11-05. Es un perfil local acotado de herramientas/recursos; no ofrece sampling, prompts, tareas duraderas ni suscripciones y no es una certificación de interoperabilidad universal.

Máximo ocho millones de bytes por mensaje y cuatro millones por entrada JSON. Lectura paginada hasta veinte fragmentos y 200.000 caracteres por respuesta; recursos de entrega hasta diez MB. Estos son límites técnicos del puente, adicionales a los del lector. Las operaciones se serializan en cada proceso; los bloqueos y hashes protegen frente a ediciones/procesamientos concurrentes. La cancelación suprime la respuesta, pero una operación local iniciada puede finalizar y conservar su revisión; debe revisarse el estado antes de repetir. No hay shell ni acceso a rutas arbitrarias fuera de la raíz seleccionada.

## Estado de comprobación

El puente se prueba con cliente de protocolo local, proceso stdio real, dos autores IA de prueba y los mismos contratos. **No se ha iniciado sesión ni ejecutado una evaluación con Claude real.** Sus conectores GitHub/Drive y la recuperación/visualización del Word siguen por comprobar en ese cliente. No se necesita una API propia de modelo para esta arquitectura; la cuenta y funciones del asistente elegido tienen sus propias condiciones de acceso.
