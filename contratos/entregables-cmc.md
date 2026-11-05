# Contrato de salida — aumento CMC: tres entregables secuenciales

**Fuente de verdad para los campos:** [docs/CONTRATO_DATOS_CMC.md](../docs/CONTRATO_DATOS_CMC.md) y especificaciones de [entregable 1](../docs/ENTREGABLE_01_RELACION_OBRAS.md), [2](../docs/ENTREGABLE_02_FACTORES_EXPERIENCIA.md), [3](../docs/ENTREGABLE_03_RESUMEN_CMC.md). Este archivo define el **contrato del agente cloud**, no reemplaza ni altera las fórmulas normativas.

## Paquete mínimo (si la plataforma puede crear archivos)

Carpeta de revisión del expediente de Drive, con **cuatro JSON independientes** y un resumen opcional de lectura. Nunca copiar este paquete a GitHub.

| Orden | Archivo | Contenido mínimo y comprobación |
|---|---|---|
| Maestra | `ficha-maestra.json` | `version`, `expediente`, `obras`, `factores`, `consultas`, `observaciones`; obra con ID estable, fuente por campo y condiciones |
| 1 | `entregable-01-datos.json` | Relación de obras, identificación, fecha contrato/recepción, moneda, montos contractuales/liquidados, descuentos, porcentaje aplicado, experiencia **propuesta**, estado/desistimiento/exclusión y evidencia |
| 2 | `entregable-02-datos.json` | Depende del 1; obras computables candidatas, años marcados con evidencia, suma de experiencia y factores `a`, `f`, `e`; `G = a + f + e` o `null` si falta insumo |
| 3 | `entregable-03-datos.json` | Depende del 1 y 2; suma de obras sustentadas, G, fórmula `CMC = ΣObras × G` cuando proceda, `CMC_calculada_provisional_soles` o `null`, **`CMC_a_otorgar = null`** |

## Claves de control que debe conservar el agente

- `expediente.tipo_tramite = "aumento_cmc"`.
- Los IDs de obras, estados y montos en 1 deben corresponder exactamente a la maestra y a los IDs usados en 2/3.
- `participacion_aplicada` distingue `true`, `false` y `null`; **no** volver a multiplicar si ya se ajustó el monto.
- `estado`: `propuesta_incluir`, `pendiente` o `excluida`. `desistida` se anota como motivo explícito de exclusión, **no suma**.
- Cada importe desconocido debe ser `null`, no `0`; usar cadenas decimales: `"250000.00"`, no números binarios imprecisos.
- `factores.actividad`, `factores.financiero`, `factores.ejecucion`: cada uno con `valor`, `sustento`, `referencias` y `norma_por_verificar`. G **solo** se cierra si las tres entradas tienen fundamento.
- `consultas` con `servicio`, `realizada`, `fecha`, `resultado`, `referencias`. Nunca afirmar consultas RNP/SUNAT/otras no realizadas.
- Ante discrepancia en datos, moneda, fórmula o años → `parcial_con_pendientes`, no cifra final inventada.

## Campos mínimos de portada/manifiesto

```json
{
  "caso": "EXP-DEMO",
  "procedimiento": "aumento_cmc",
  "revision": "REV-001",
  "fecha_analisis": null,
  "estado": "parcial_con_pendientes",
  "origen_expediente": null,
  "fuentes": [],
  "observaciones": [],
  "pendientes": [],
  "entregables": [
    "ficha-maestra.json",
    "entregable-01-datos.json",
    "entregable-02-datos.json",
    "entregable-03-datos.json"
  ]
}
```

`EXP-DEMO` **es solo un ejemplo ficticio**. En la entrega real el agente documentará enlace Drive y estado de publicación verificados.

## Formatos oficiales: límite vigente

**Las tres plantillas editables nativas institucionales aún no han sido entregadas.** Los cuatro archivos son **datos preparados** para rellenarlas en una siguiente iteración. No generar planillas que aparenten ser oficiales, no poner fechas/sellos oficiales simulados, ni afirmar que CMC ha sido otorgada. Si el cliente puede crear XLSX de revisión como visualización, etiquetarlo claramente **auxiliar no oficial**.

## Criterios de aceptación

Los tres archivos deben ser independientes, completos en su esquema, **orden 1→2→3**, con procedencia por dato, exclusiones, comprobación decimal reproducible, pendientes explícitos y resultados no fingidos. El coordinador devuelve enlaces Drive **solo de archivos realmente publicados**. Reglas transversales: [control de evidencias](control-evidencias.md).
