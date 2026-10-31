# Estado de OECE Assistant
Actualizado: **31 de octubre de 2026 (America/Lima)**. Inventario con corte inicial 29/10/2026; cotejos focalizados de las cinco decisiones al 31/10/2026. Este archivo es el resumen de continuidad; el [roadmap](../ROADMAP.md) y las [tareas](TAREAS.md) contienen el detalle.

## Avance orientativo
**Alrededor de 35 % del proyecto completo (rango 30–40 %).** Es una estimación de planificación por entregables, no porcentaje de funciones operativas. [Criterios y pesos](MEDICION_AVANCE.md). El aumento corresponde al circuito documental sintético y su Word; la biblioteca sigue sin cierre jurídico.

## Resultado disponible
Biblioteca inicial en Google Drive y herramientas para integridad, lectura/búsqueda PDF/Word y OCR de muestra. Funciona el circuito sintético con matriz y Word. Ahora también propone coincidencias textuales para siete controles y permite importar decisiones explícitas a otra carpeta, comprobando citas y huellas. T24/T25 quedan cerradas en ese alcance. La activación automática de carpetas y el coordinador conversacional siguen pendientes.

| Fase del plan | Estado real | Evidencia disponible | Falta para cerrar |
|---|---|---|---|
| 0. Plan persistente | Completada | Plan, roadmap, documentación y commits en GitHub | Mantenerlos actualizados |
| 1. Biblioteca normativa | Adquisición mínima cerrada; fase jurídica abierta | T28: 36 requeridos comprobados. Total 29 registros y 46 archivos; índice anterior más complemento de 212 fragmentos con texto | Suficiencia/exhaustividad, consolidación y vigencia por disposición |
| 2. Procedimientos RNP | En curso | Piloto consultores con 22 controles candidatos y 10 casos sintéticos especificados | Revisión jurídica y resolución de excepciones/transición |
| 3. Base técnica | En curso, parcial | Lectura, búsqueda, OCR candidato, ingreso, revisiones y propuestas con revisión separada | Coordinador, activación de carpetas, OCR completo, otros formatos y endurecimiento |
| 4. Piloto consultores | Demostración documental y revisión de evidencias ejecutadas | Matriz de 22 controles; Word anterior revisado; propuesta inicial para siete controles | Ampliar cobertura, aprobar reglas y aceptación jurídica |
| 5. Validación y expansión | Pendiente | Alcance modular documentado | Ejecutores, inscripciones, actualizaciones y reconsideraciones comprobadas |

## Decisiones adoptadas
Los cinco criterios del piloto fueron adoptados con fundamento por el asistente IA, autorizado por el usuario: régimen actual de primera ampliación, condición de la quinta DCM de Ley 32732, alcance FUP, ROF actualizado y ramas por proveedor/experiencia. Se corrige el bloqueo atribuido a toda Ley 32732. Excepciones y fuentes en [criterios adoptados](normativa/CRITERIOS_ADOPTADOS_PILOTO.md) y [registro vigente](../normativa/decisiones-piloto.v0.2.json). No hay aprobación humana ficticia ni reglas nuevas ejecutadas.

## Qué se probó
- **53 pruebas técnicas aprobadas:** 23 de biblioteca/OCR, 12 del circuito de expediente, 13 de propuesta/revisión y cinco de cobertura.
- T28 cerrado: 36 archivos requeridos de siete grupos, sin faltantes y con huellas locales verificadas. Diecisiete archivos nuevos conservados en Drive; ROF histórico separado del actualizado. [Alcance del cierre](normativa/COBERTURA_MINIMA_PILOTO.md).
- Muestra nueva sin vínculos: nueve propuestas, todas pendientes; cero incorporaciones automáticas. Simulación técnica separada: una aceptada, una rechazada y siete pendientes. La matriz incorporó solo la aceptada; los 22 resultados siguieron `no_determinable`. No fue revisión humana real.
- Tres documentos sintéticos, 11 fragmentos y siete vínculos declarados a seis controles. Los 22 resultados jurídicos permanecen `no_determinable`.
- Repetición sin duplicar entregas; cambios conservan la revisión anterior y originales. Se rechazan entradas declaradas como reales, rutas externas, evidencias inexistentes y matriz habilitada; un fallo de redacción no publica una entrega parcial.
- Word de cuatro páginas exportado con Word instalado e inspeccionado página por página. [Alcance y reproducción](PILOTO_DOCUMENTAL.md).
- Cinco originales adicionales descargados y archivados en Drive; referencias recuperadas de Ley 32103 PDF p. 20, Ley 32187 p. 11 y Ley 32515 p. 8. [Registro](../normativa/indexacion/validacion-ampliacion-2026-10-30.json).
- Búsqueda real de una referencia conocida: directiva RNP, numeral 9.3.3, página PDF 12.
- OCR real de DS 006-2026-JUS páginas 1–2 y DS 009-2025-EF página 20. Las tres salidas conservan fuente, página, hash de imagen y coordenadas.
- Se observaron errores de reconocimiento al comparar las imágenes. Cuatro regiones comparadas con transcripción manual: un identificador crítico falló y quedó marcado para revisión. No se declara exactitud general. [Diagnóstico](normativa/CALIDAD_OCR.md).

Los diez casos jurídicos son una especificación y **no fueron ejecutados**. El índice anterior conserva 1.184 fragmentos con texto; el complemento separado de las fuentes nuevas añade 212 y mantiene DL escaneado/HTML/XLSX pendientes de lectura automática. No se unificaron índices en este bloque. [Resultado actualizado](normativa/RESULTADO_INDEXACION.md). Las pruebas técnicas y el borrador no acreditan aceptación jurídica ni precisión general de extracción.

## Orden de continuación
1. Traducir los [cinco criterios adoptados](normativa/CRITERIOS_ADOPTADOS_PILOTO.md) a selección de régimen y ramas, con pruebas de sus excepciones. Consolidar TUPA por rama y cotejo primario TUO. La adquisición mínima v0.1 ya está comprobada.
2. Ampliar referencias críticas y completar timeout/reanudación antes de procesar lotes OCR; la integración candidata de tres páginas ya está comprobada.
3. Segmentar y recuperar disposiciones con versiones y revisión identificadas.
4. Ampliar la cobertura de propuestas, hoy de siete controles; incorporar activación de carpeta y coordinador sobre el circuito documental probado.
5. Comprobar reglas y casos antes de habilitar conclusiones; documentar la revisión y aceptación del piloto para uso institucional. La autorización para tomar criterios de diseño ya está dada.

## Referencias de continuidad
- [Plan integral](PLAN_INTEGRAL.md)
- [Cierres comprobados y siguiente bloque](CIERRES.md)
- [Cobertura mínima y límites jurídicos](normativa/COBERTURA_MINIMA_PILOTO.md)
- [Propuesta y revisión de evidencias](EVIDENCIAS_Y_REVISION.md)
- [Piloto documental](PILOTO_DOCUMENTAL.md) y [ejecución registrada](../proyecto/ejecuciones/demo-consultores-2026-10-30.json)
- [Fuentes nuevas y pendientes](normativa/AMPLIACION_FUENTES.md)
- [Word sintético en Drive](https://drive.google.com/file/d/1LTpu3vLvPbSE25a2ZXd_tbIxi-QKnLAu/view)
- [Ficha del primer procedimiento](procedimientos/AMPLIACION_CONSULTORES.md)
- [Hallazgos normativos](normativa/HALLAZGOS_PILOTO.md)
- [Resultado de indexación](normativa/RESULTADO_INDEXACION.md)
- [OCR: alcance y prueba](normativa/OCR_LOCAL.md)

Las dudas jurídicas siguen registradas; una herramienta técnica terminada no cierra la fase normativa. El almacenamiento de expedientes y la elección de modelo/runtime siguen pendientes.
