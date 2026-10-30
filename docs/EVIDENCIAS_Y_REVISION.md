# Propuesta y revisión de evidencias
Entrega técnica v0.1 del 30/10/2026. Cierra T24 y T25 en el alcance descrito aquí. Solo expedientes declarados sintéticos; sin conclusiones jurídicas ni autenticación institucional.

## Qué funciona
El sistema busca términos y grupos de términos dentro de los fragmentos leídos y propone vínculos con controles. **No usa un modelo ni interpreta suficiencia jurídica.** Cada propuesta conserva documento, ubicación, huellas de fuente y fragmento, texto original, citas con posiciones exactas, términos coincidentes y versión del perfil. La confianza queda vacía; no se inventa una puntuación.

El [perfil inicial](../rules/consultores/perfil-evidencias.v0.1.json) cubre siete controles: AC-01, AC-02, AC-03, AC-05, AC-07, AC-09 y AC-15. Los otros quince se enumeran como sin perfil; no se consideran evaluados ni no aplicables. Las palabras admiten diferencias de mayúsculas y tildes, conservando la cita original. Una coincidencia de moneda, contrato o conformidad no prueba el requisito.

Se omiten documentos duplicados por contenido y fragmentos con alertas de lectura. Hay un límite de veinte propuestas por control y un conteo explícito de coincidencias omitidas. Las visitas a duplicados y fragmentos con alerta se cuentan por control, no como archivos distintos. Negaciones, ausencias o texto ficticio producen una advertencia; nunca una aprobación.

## Revisión separada
Todas las propuestas nacen pendientes. La plantilla de decisiones exige una elección explícita de aceptación o rechazo, revisor, fecha con zona horaria y motivo. Lo no decidido sigue pendiente. La identidad se declara en el archivo; todavía no se autentica ni firma.

Antes de importar decisiones, se vuelve a producir el lote y se compara completo. Cambiar documentos, configuración, perfil, matriz o implementación invalida el lote correspondiente. Las decisiones deben identificar ese lote y propuestas existentes, sin duplicados.

La revisión se exporta a **otra carpeta**, con copias de documentos, configuración, propuestas y decisiones. Se conserva la entrada y se rechaza sobrescribir un destino existente. Una aceptación añade un vínculo con procedencia; un rechazo retira el vínculo coincidente, incluso si se había declarado o aceptado antes. Una decisión pendiente mantiene los vínculos previamente declarados y no añade otros.

El lector de expedientes v0.2 comprueba de nuevo las huellas, citas y asociación al control/documento/localizador de cada vínculo revisado. Los 22 resultados legales continúan `no_determinable`, independientemente de las decisiones documentales.

## Cómo repetirlo
Desde la raíz del proyecto, usando las dependencias de `requirements-indexacion.txt`:

```powershell
python scripts/crear_demo_expediente.py --sin-vinculos --salida data/evidencias/entrada
python scripts/proponer_evidencias.py --entrada data/evidencias/entrada --salida data/evidencias/propuestas.json --plantilla-decisiones data/evidencias/decisiones.json
```

Revisar los textos y completar únicamente las decisiones que correspondan en `decisiones.json`. Un registro tiene esta forma; los valores de ejemplo no son una aprobación:

```json
{
  "propuesta_id": "ID copiado de la propuesta",
  "decision": "pendiente",
  "revisor": null,
  "fecha": null,
  "motivo": ""
}
```

Para aceptar/rechazar se usan `aceptada` o `rechazada`, con revisor, motivo y fecha como `2026-10-30T17:00:00-05:00`. Mantener el identificador de lote que produjo la plantilla. Después:

```powershell
python scripts/revisar_evidencias.py --entrada data/evidencias/entrada --propuestas data/evidencias/propuestas.json --decisiones data/evidencias/decisiones.json --salida data/evidencias/revisado
python scripts/ejecutar_expediente.py --entrada data/evidencias/revisado --salida data/evidencias/salida
```

El último comando usa el generador Word existente; este bloque no entrega una nueva versión del Word revisado visualmente en la demostración anterior. Los resultados de este bloque se comprobaron hasta la matriz preparada y las carpetas de revisión.

## Prueba y alcance del cierre
**47 pruebas técnicas aprobadas:** 34 anteriores y 13 de propuesta/revisión. La muestra sin vínculos produjo nueve propuestas con nueve localizadores esperados, sin añadir evidencia automáticamente. Se probó exportar todas pendientes: cero vínculos nuevos. Una simulación claramente identificada aceptó una, rechazó otra y mantuvo siete pendientes; la matriz solo incorporó la aceptada. No fue una revisión humana real.

Las pruebas incluyen citas exactas con Unicode, límites de palabra, cambios de fuente/perfil, propuestas alteradas, decisiones incompletas/duplicadas/desconocidas, revisión trasladada de control, negaciones, duplicados, límite de propuestas, PDF sin texto y revocación de un vínculo previo. No miden precisión general sobre expedientes reales ni completan los diez casos jurídicos.

[Registro de ejecución](../proyecto/ejecuciones/evidencias-revision-2026-10-30.json). [Cierres y pendientes de fase](CIERRES.md).
