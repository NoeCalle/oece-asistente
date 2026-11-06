# Procedimiento operativo — aumento de CMC (agente, sin MCP obligatorio)

**Especialista:** [CMC](../agentes/especialista-cmc.md). **Salida:** [tres archivos secuenciales y ficha](../contratos/entregables-cmc.md).

**Catálogo de documentos y casuística:** antes del inventario, cargar [catálogo JSON](../casuistica/tipos-documentales-cmc.v1.json) y [lecciones observadas](../casuistica/patrones-y-lecciones-cmc.md). Separar piezas por naturaleza (hoja de ruta, pago, contrato, actas, liquidación y anexos) y por obra, aunque vengan en diferentes PDF. Cada nueva entrega se registra de manera acumulativa y sus variantes se documentan en el expediente privado. Promover a GitHub solo patrones anonimizados y no convertir observaciones aisladas en normas.

| Fase | Acción del agente | Control antes de avanzar |
|---|---|---|
| 0. Identificar | Confirmar `aumento_cmc` por orden explícita o ficha, enlace Drive, solicitante, fecha de corte y documentación disponible | No inferir procedimiento por el nombre del PDF |
| 1. Inventariar | Revisar documentos Drive: solicitud, obras, recepción, liquidación, consorcio, financieros | Enlaces reales, ID estable por obra y lista de ausentes |
| 2. Normativa | Buscar biblioteca Drive, leer artículos/anexos aplicables; web solo después de avisar si falta sustento | Fuente etiquetada, fecha y pasaje concreto |
| 3. Relación de obras | Registrar fecha, moneda, contrato, liquidación, descuentos, participación, experiencia candidata, desistimientos/exclusiones y evidencias | `entregable-01-datos.json` coherente; exclusiones no suman |
| 4. Años y factores | Con datos de fase 3, marcar años admisibles, identificar universo y determinar `a`, `f`, `e` sustentados | `entregable-02-datos.json`; `G=a+f+e` solo si son determinables |
| 5. Cálculo | Verificar `ΣObras` y `CMC_provisional = ΣObras × G`; recalcular con herramienta independiente y registrar fórmula | `entregable-03-datos.json`, con `CMC_a_otorgar=null` |
| 6. Entrega | Ficha maestra, control de coherencia y listado de pendientes; guardar archivos en Drive si posible | Enlaces verdaderos, revisión e indicación de límites |

### Verificaciones específicas

- Participación consorcial: identificar base y si **ya** se aplicó; no multiplicar dos veces.
- Monto contractual, final liquidado, deducciones y experiencia son conceptos distintos.
- Obra desistida/excluida/pendiente no suma como experiencia admisible.
- No asumir años acreditados solo por fecha; registrar fundamento de inclusión.
- Factor financiero con PC=0: **no dividir por cero**; estudiar la rama normativa documentada.
- Solo calcular si montos/monedas y factores son compatibles y están acreditados; si no, `null` más pendiente.
- Toda regla normativa debe contar con documento/página y versión consultada. No transferir datos ilustrativos de fotos/plantillas al expediente.

### Documentos normativos y especificaciones ya existentes

- [Contrato histórico de datos CMC](../docs/CONTRATO_DATOS_CMC.md).
- [Formato 1: relación](../docs/ENTREGABLE_01_RELACION_OBRAS.md), [formato 2: factores](../docs/ENTREGABLE_02_FACTORES_EXPERIENCIA.md), [formato 3: resumen](../docs/ENTREGABLE_03_RESUMEN_CMC.md).
- [Criterios de procedimientos, alcance y restricciones](../docs/CONTRATO_PROCEDIMIENTOS.md).
- [Contrato de evidencia](../contratos/control-evidencias.md).

**No ejecutar la ruta Python/MCP histórica salvo que el titular la requiera o resulte útil como verificador opcional.** El agente puede utilizar aritmética de la nube del cliente sin infraestructura adicional.
