# Casuística observada y pendientes de afinación — CMC

**Edición:** 2026-11-06 · **Fuentes de aprendizaje:** piloto documental de aumento de CMC trabajado con el titular. Se abstraen patrones **sin publicar contratos, proveedores, identificaciones, montos ni imágenes del expediente**. No son jurisprudencia ni reglas legales nuevas.

## Aprendizajes comprobados en la prueba

| Código | Situación observada | Qué debe hacer el agente | Estado |
|---|---|---|---|
| CAS-CMC-001 | Expediente contiene **hoja de ruta** que identifica el trámite y declara cantidad de folios, además de otros archivos | Registrar número/fecha/folio declarado; no asumir que folios = páginas de un solo PDF ni que estar presentado significa admisible | Verificado en caso |
| CAS-CMC-002 | Se adjunta **comprobante de pago** separado de documentos de obra | Registrar monto, concepto, fecha y operación como documento administrativo; no sumarlo a experiencia de obra | Verificado en caso |
| CAS-CMC-003 | **Contrato** y **acta de recepción** repiten nombre del contratista | Elegir **contrato** para ese campo y citar su PDF/página; conservar fuente secundaria si es útil | **Criterio adoptado por titular** |
| CAS-CMC-004 | Un contrato o resolución tiene referencias a **obra, contrato o CUI diferentes** entre encabezado, cuerpo o acta | Registrar los literales de cada pieza y páginas, observar la discrepancia, seguir con campos/obras independientes; no asumir que documentos distintos corresponden al mismo contrato | Verificado en caso |
| CAS-CMC-005 | Contrato, entrega de terreno y acta de inicio muestran **cronología aparente imposible o contradictoria** | Separar fecha de suscripción, entrega e inicio; observar y cotejar originales antes de concluir | Verificado en caso |
| CAS-CMC-006 | Resolución presenta un **importe en antecedentes**, otro en el **artículo aprobatorio** y/o otro en el **cuadro económico** | Distinguir concepto por concepto y fuente/página; hacer conciliación aritmética como análisis, no reemplazar importes por suposición | Verificado en caso |
| CAS-CMC-007 | Hay **deductivo de obra** y/o reajuste, además de monto final referido en la resolución | Diferenciar reducción por partidas de obra de exclusión de equipamiento/mobiliario; no sumar dos veces adicionales/metrados ni asumir que monto final equivale al monto neto admisible | Verificado en caso |
| CAS-CMC-008 | Algunas páginas digitalizadas tienen **OCR escaso** o contienen mayormente firmas | Ir a imagen para comprobar el contenido; no considerar el OCR corto prueba de hoja faltante | Verificado en caso |
| CAS-CMC-009 | Un PDF contiene **varias obras** o una obra aparece en **varios PDF** | Identificar documentos por rangos y obra por ID estable; permitir nuevas entregas y no duplicar obra al recibir acta o liquidación | Criterio de trabajo adoptado |
| CAS-CMC-010 | El campo **«inicial pág»** del Excel puede citar páginas distintas si el dato está repetido en varias piezas | Registrar página física del PDF elegido y también ID/nombre del PDF; aplicar preferencias por campo conforme se vayan confirmando | **Pendiente de afinación** |
| CAS-CMC-011 | La plantilla puede contener **encabezados combinados** para nombre de obra y formularios con fórmulas | Escribir texto en celda ancla sin descombinar; comprobar fórmulas/compatibilidad con Excel del usuario antes de dar archivo por válido | Criterio de trabajo adoptado |

## Ficha de captura de una nueva casuística

Cada nueva situación se registra como **observación verificable**, no como generalización automática:

- **Identificador y título:** `CAS-CMC-NNN`, nombre breve.
- **Disparador:** texto, sección o relación entre documentos que activa el reconocimiento.
- **Variantes observadas:** nombre alternativo, diferente orden, sin folios, varios adjuntos, documento de consorcio separado.
- **Evidencia privada:** expediente/obra, PDF/ID, páginas exactas (no subir al repositorio público).
- **Riesgo:** solo del campo, de la obra o transversal.
- **Acción operativa:** qué extraer, qué cotejar y qué se puede seguir procesando.
- **Clasificación:** `candidato`, `verificado_en_caso`, `criterio_adoptado`; `normativo` requiere además norma y artículo verificables.
- **Fecha, versión y responsable de afinación** cuando se acuerde una regla estable.

## Matriz de precedencia por campo — en evolución

| Campo | Documento preferente | Alternativas | Estado |
|---|---|---|---|
| Nombre del contratista | **Contrato de obra** | Acta de recepción | **Adoptado** |
| Nombre exacto de la obra | Por definir | Contrato, acta de recepción, resolución | Pendiente |
| Monto contractual original | Por definir | Contrato, adendas y resoluciones | Pendiente |
| Porcentaje de consorcio | Por definir | Contrato/promesa formal/acuerdo de consorcio | Pendiente |
| Fecha de recepción | Por definir | Acta de recepción y otros documentos que la refieran | Pendiente |
| Importe de liquidación y monto neto | Por definir; distinguir conceptos | Resolución y cuadro económico | Pendiente |
| Adicional, deductivo, reajuste | Por definir | Resoluciones y cuadros económicos | Pendiente |

**Importante:** la preferencia de una fuente no permite ocultar discrepancias. Si el dato es controvertido, el agente conserva las dos versiones con páginas y marca pendiente de cotejo. Nunca convierte automáticamente un patrón del piloto en motivo legal de rechazo.

## Método de mejora entre expedientes

Al cerrar cada ronda, revisar: (1) documento nuevo o variante no catalogada; (2) campos hallados y su fuente; (3) conflicto entre fuentes; (4) lección suficientemente generalizable; (5) actualización de esta guía/JSON **sin datos privados**; (6) si se aprueba una nueva precedencia, pasar de «pendiente» a «criterio adoptado». El catálogo puede actualizarse sin rehacer expedientes existentes; cada expediente conserva su versión de reglas y sus evidencias.

La **biblioteca de casuística** no aprende de forma autónoma fuera de las conversaciones: funciona como memoria persistente que un agente debe **leer y actualizar deliberadamente** cuando tenga acceso y autorización. La extracción técnica no acredita por sí sola autenticidad o suficiencia administrativa.
