# Procedimiento operativo — aumento de CMC (agente, sin MCP obligatorio)

**Especialista:** [CMC](../agentes/especialista-cmc.md). **Salida:** [Excel MPR y Word de observaciones](../contratos/entregables-cmc.md).

**Entregables operativos vigentes:** un **Excel institucional MPR** con todas sus pestañas y un **Word editable de observaciones**. La secuencia relación de obras → factores → cálculo es **interna** y se representa dentro del Excel; JSON/ficha maestra son registros privados auxiliares, no salidas obligatorias. El Word se alimenta de las observaciones documentales detectadas y se actualiza con cada entrega. Véase [contrato vigente](../contratos/entregables-cmc.md).

**Catálogo de documentos y casuística:** antes del inventario, cargar [catálogo JSON](../casuistica/tipos-documentales-cmc.v1.json) y [lecciones observadas](../casuistica/patrones-y-lecciones-cmc.md). Separar piezas por naturaleza (hoja de ruta, pago, contrato, actas, liquidación y anexos) y por obra, aunque vengan en diferentes PDF. Cada nueva entrega se registra de manera acumulativa y sus variantes se documentan en el expediente privado. Promover a GitHub solo patrones anonimizados y no convertir observaciones aisladas en normas.

| Fase | Acción del agente | Control antes de avanzar |
|---|---|---|
| 0. Identificar | Confirmar `aumento_cmc` por orden explícita o ficha, enlace Drive, solicitante, fecha de corte y documentación disponible | No inferir procedimiento por el nombre del PDF |
| 1. Inventariar | Revisar documentos Drive: solicitud, obras, recepción, liquidación, consorcio, financieros | Enlaces reales, ID estable por obra y lista de ausentes |
| 2. Normativa | Buscar biblioteca Drive, leer artículos/anexos aplicables; web solo después de avisar si falta sustento | Fuente etiquetada, fecha y pasaje concreto |
| 3. Relación de obras | Registrar fecha, moneda, contrato, liquidación, descuentos, participación, experiencia candidata, desistimientos/exclusiones y evidencias | Campos de obras en Excel sustentados; exclusiones no suman |
| 4. Años y factores | Con datos de fase 3, marcar años admisibles, identificar universo y determinar `a`, `f`, `e` sustentados | Factores dentro del Excel; `G=a+f+e` solo si son determinables |
| 5. Cálculo | Verificar `ΣObras` y `CMC_provisional = ΣObras × G`; recalcular con herramienta independiente y registrar fórmula | CMC provisional en Excel cuando haya sustento; `CMC_a_otorgar=null` en control interno |
| 6. Entrega | **Excel MPR + Word de observaciones**, control cruzado, pendientes; guardar archivos en Drive si posible | Dos archivos visibles y verificables; estado y limitaciones |

### Verificaciones específicas

- Participación consorcial: identificar base y si **ya** se aplicó; no multiplicar dos veces.
- Monto contractual, final liquidado, deducciones y experiencia son conceptos distintos.
- Obra desistida/excluida/pendiente no suma como experiencia admisible.
- No asumir años acreditados solo por fecha; registrar fundamento de inclusión.
- Factor financiero con PC=0: **no dividir por cero**; estudiar la rama normativa documentada.
- Solo calcular si montos/monedas y factores son compatibles y están acreditados; si no, `null` más pendiente.
- Toda regla normativa debe contar con documento/página y versión consultada. No transferir datos ilustrativos de fotos/plantillas al expediente.

### Especificaciones históricas e internas (no entregas adicionales)

- [Contrato histórico de datos CMC](../docs/CONTRATO_DATOS_CMC.md).
- [Relación](../docs/ENTREGABLE_01_RELACION_OBRAS.md), [factores](../docs/ENTREGABLE_02_FACTORES_EXPERIENCIA.md) y [resumen](../docs/ENTREGABLE_03_RESUMEN_CMC.md) son etapas lógicas históricas, **no** tres archivos obligatorios.
- [Criterios de procedimientos, alcance y restricciones](../docs/CONTRATO_PROCEDIMIENTOS.md).
- [Contrato de evidencia](../contratos/control-evidencias.md).

**No ejecutar la ruta Python/MCP histórica salvo que el titular la requiera o resulte útil como verificador opcional.** El agente puede utilizar aritmética de la nube del cliente sin infraestructura adicional.
