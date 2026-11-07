# Procedimiento operativo — aumento de CMC (agente, sin MCP obligatorio)

**Especialista:** [CMC](../agentes/especialista-cmc.md). **Salida:** [Excel MPR y Word de observaciones](../contratos/entregables-cmc.md).

**Entregables operativos vigentes:** un **Excel institucional MPR** con todas sus pestañas y un **Word editable de observaciones**. La secuencia relación de obras → factores → cálculo es **interna** y se representa dentro del Excel; JSON/ficha maestra son registros privados auxiliares, no salidas obligatorias. El Word se alimenta de las observaciones documentales detectadas y se actualiza con cada entrega. Véase [contrato vigente](../contratos/entregables-cmc.md).

**Catálogo de documentos y casuística:** antes del inventario, cargar [catálogo JSON](../casuistica/tipos-documentales-cmc.v1.json) y [lecciones observadas](../casuistica/patrones-y-lecciones-cmc.md). Separar piezas por naturaleza (hoja de ruta, pago, contrato, actas, liquidación y anexos) y por obra, aunque vengan en diferentes PDF. Cada nueva entrega se registra de manera acumulativa y sus variantes se documentan en el expediente privado. Promover a GitHub solo patrones anonimizados y no convertir observaciones aisladas en normas.

## Secuencia vigente — referencia canónica única

**Leer y ejecutar sin reordenar** [MET-CMC-01](metodologia-unica-cmc.md). Las etapas obligatorias del modo agent-first son: activación/reanudación → inventario → control visual de integridad **de todas las páginas** → extracción por PDF/obra → conciliación → cotejo normativo → cálculo y libro MPR → **N copias individuales de PDF resaltados** → **un único Word consolidado** → auditoría y publicación.

**Puerta de avance:** cada etapa conserva prueba de cobertura y pendientes en el control interno del expediente; no llamar «completo» a una etapa si quedan páginas sin ver, documentos sin mapear, montos sin sustento o archivos sin verificar. Una observación no bloqueante se registra y se continúa lo independiente. La secuencia interna histórica «relación de obras → años/factores → cálculo» sigue existiendo **dentro** de la etapa de Excel MPR, no constituye tres entregables distintos.

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
