# Piloto documental con expediente sintético
Fecha: 30/10/2026. Implementación técnica inicial; revisión jurídica pendiente.

Ya funciona un recorrido local explícito: carpeta de entrada → lectura → vínculos de evidencia declarados → matriz JSON → borrador Word. No hay todavía activación automática de carpetas, conversación con un coordinador ni evaluación jurídica habilitada.

## Ejecución reproducible
Requiere Python y las dependencias fijadas en `requirements-indexacion.txt`.

```powershell
python scripts/crear_demo_expediente.py --salida data/demo-v1/entrada
python scripts/ejecutar_expediente.py --entrada data/demo-v1/entrada --salida data/demo-v1/salida
python -m unittest discover -s tests -p "test_*.py"
```

El ejemplo usa tres textos ficticios: solicitud, contrato y conformidad. No son formularios presentados ni documentos auténticos. Los siete vínculos a seis controles fueron declarados en la configuración. La herramienta comprueba que el documento, el localizador y el texto existen; no infiere que basten para acreditar un requisito.

## Entrada y salidas
La carpeta contiene `expediente.json` y los documentos listados explícitamente. El indicador `sintetico` debe ser `true`; se rechazan entradas declaradas como reales. La marca es una declaración: no anonimiza ni detecta información personal. El [ejemplo reproducible](../tests/fixtures/expedientes/demo.json) define el contrato mínimo de entrada.

Cada entrega se guarda en una carpeta identificada por la huella de configuración, documentos, matriz candidata, implementación, lector y versiones de dependencias. Contiene:

- `originales/`: copias exactas de los documentos leídos.
- `expediente.json` y `reglas.json`: instantáneas de la configuración y matriz candidata.
- `matriz.json`: fragmentos, huellas, vínculos, motivos y referencias normativas por control.
- `informe.docx`: borrador legible para revisión.
- `entrega.json`: secuencia de estados completados y huellas de los archivos de entrega.

Repetir la misma entrada reutiliza la entrega solo si sus archivos siguen íntegros. Modificar un documento crea otra revisión y conserva la anterior. Un fallo de redacción no publica una carpeta final incompleta. No hay reanudación por etapa: se vuelve a ejecutar la operación completa. El historial de estados se escribe al completar la entrega, no constituye una cola persistente ni una bitácora de eventos en tiempo real.

## Lectura y límites
Admite TXT UTF-8, PDF digital y cuerpo/tablas de DOCX. Conserva líneas, páginas o rutas de bloques. Un PDF sin texto suficiente queda señalado para OCR/revisión; el lector de expedientes aún no incorpora automáticamente la capa OCR de la biblioteca. Encabezados, pies, cuadros de texto y revisiones de Word no están cubiertos.

Los 22 resultados son `no_determinable`: las reglas siguen deshabilitadas y sin aprobación humana. La falta de vínculo se muestra como tal, sin convertirla en incumplimiento. Las fuentes normativas de la matriz conservan URL, huella y página; no se selecciona automáticamente el régimen vigente.

Los límites comprobados incluyen 1–100 documentos, máximo 20 MB por archivo, rutas resueltas dentro de la entrada, identificadores únicos y rechazo de vínculos inexistentes. Falta endurecer lectores ante archivos hostiles, límites de tiempo/memoria y concurrencia. Esto no habilita datos personales ni uso institucional.

## Verificación de esta entrega
**34 pruebas técnicas aprobadas:** 22 anteriores y 12 del circuito de expediente. Se verificaron repetición sin duplicación, preservación de revisiones/originales, rechazo de salidas alteradas, rutas externas, controles o evidencias inexistentes, reglas habilitadas y fallo de redacción sin entrega parcial. Una prueba adicional de lectura dentro de ese conjunto usa DOCX y PDF sintéticos; el PDF en blanco conserva su alerta.

El Word final tiene cuatro páginas revisadas visualmente: resumen e inventario; matriz continua con cabecera repetida en dos páginas; extractos, huellas y enlaces de fuentes. Se corrigió una línea heredada del estilo de título durante la revisión. El conversor empaquetado falló por ausencia de LibreOffice en Windows; se exportó el mismo DOCX con Word instalado y se inspeccionaron todas las imágenes obtenidas con Poppler. Esta comprobación visual fue manual en la sesión, no una función incorporada al generador.

Los [diez casos jurídicos especificados](../tests/fixtures/consultores/casos-especificacion.json) siguen sin ejecutarse. Esta demostración técnica no sustituye su aceptación. [Registro de ejecución](../proyecto/ejecuciones/demo-consultores-2026-10-30.json).

Copias para revisión en Drive: [borrador Word](https://drive.google.com/file/d/1LTpu3vLvPbSE25a2ZXd_tbIxi-QKnLAu/view) y [matriz JSON](https://drive.google.com/file/d/1sqPo8MXtFl-PMsFZ9agOQgll0pJtHKny/view). Son datos ficticios; no se cambiaron permisos de compartición.

## Siguiente incremento
Cerrar vigencias y régimen temporal del piloto; ampliar la extracción y propuesta de evidencias conservando revisión humana; integrar OCR de expedientes; preparar activación de carpeta y coordinador sobre este contrato. Definir almacenamiento privado, acceso, retención y proveedor/modelo antes de procesar datos reales.
