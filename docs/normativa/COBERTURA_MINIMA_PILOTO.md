# Cobertura documental mínima del piloto
Cierre de adquisición: 31/10/2026. Lote recuperado: 30/10/2026. Se mantiene el corte investigado 29/10/2026; no se certifica exhaustividad ni vigencia a la fecha de cierre.

Se cierra **T28, adquisición del alcance documental v0.1**: 36 archivos expresamente enumerados, en siete grupos, disponibles localmente con tamaño y SHA256 verificados. La biblioteca completa contiene **46 archivos y 29 registros**. Este cierre no habilita reglas ni concluye la fase jurídica.

[Alcance versionado](../../normativa/cobertura-piloto.v0.1.json), [resultado reproducible](../../normativa/cobertura-piloto-reporte-2026-10-30.json) y [registro de ejecución](../../proyecto/ejecuciones/cierre-fuentes-piloto-2026-10-31.json).

## Archivos incorporados
Diecisiete archivos nuevos: quince PDF de 240 páginas en total, un XLSX y una captura HTML. [Manifiesto con huellas, URLs e IDs de Drive](../../normativa/manifiesto-cierre-piloto-2026-10-30.json). Se comprobaron los 17 archivos en el listado de Drive y sus tamaños; no se volvieron a descargar para recalcular sus huellas en la nube. [Carpeta de originales](https://drive.google.com/drive/folders/1WStqSLHYFrFwQUPMTRZ611DwBeubZw2m). No se cambiaron permisos de compartición.

| Grupo | Documentación recuperada | Alcance comprobado y límite |
|---|---|---|
| DL 1715 | Expediente oficial del Congreso de 28 páginas y texto HTML de El Peruano | Publicación dentro del PDF en pp. 27–28; texto del decreto en pp. 2–5. Archivo escaneado, sin extracción digital útil. Emisión 03/02/2026 y cabecera de publicación 04/02/2026 cotejadas visualmente |
| FUP | Resolución 030-2026, directiva de 13 páginas y anexo XLSX | Gestión de información FUP; perfil complementario. La hoja se comprobó como paquete Office, sin validar celdas ni fórmulas |
| ROF inicial | DS 067, sección primera, Resolución 049 y sección segunda; Resolución 002 e integrado anterior | Antecedentes conservados; el integrado anterior no se utiliza como versión actual |
| ROF actualizado | Resolución 088 y sección segunda modificada; Resolución 090 e integrado actualizado | Se recupera la modificación citada expresamente en el TUPA. Fechas de eficacia y cambios posteriores aún necesitan cotejo por disposición |
| TUPA | Resoluciones 002-2026 y 073-2026 | Completan los actos junto a los tres TUPA ya archivados. El PDF base contiene el DS 086, pp. 1–3; no se volvió a descargar ese mismo contenido |

Fuentes primarias: [Congreso, DL 1715](https://www3.congreso.gob.pe/comisiones2025/constitucion/laborcontrolpolitico/decretos-legislativos/), [El Peruano, publicación 2483559-7](https://busquedas.elperuano.pe/dispositivo/NL/2483559-7), [FUP](https://www.gob.pe/institucion/oece/normas-legales/7719040-001-2026-oece-cd), [DS 067](https://www.gob.pe/institucion/mef/normas-legales/6667223-067-2025-ef), [ROF modificado por 088](https://www.gob.pe/institucion/oece/normas-legales/7502026-088-2025-oece-pre), [ROF integrado aprobado por 090](https://www.gob.pe/institucion/oece/normas-legales/7532575-090-2025-oece-pre), [actualización TUPA](https://www.gob.pe/institucion/oece/informes-publicaciones/7647432-tupa-actualizado-del-oece-r-g-g-n-002-2026-oece-gg) y [modificación TUPA](https://www.gob.pe/institucion/oece/normas-legales/7983806-073-2026-oece-pre).

## Hallazgos delimitados
**ROF:** el artículo 3 de la Resolución 090, PDF p. 4, deroga expresamente la Resolución 002-2025 que aprobó el integrado anterior. Se registra el antecedente como histórico. El integrado actualizado contiene las funciones de Operaciones Registrales en artículo 74, PDF p. 36. Se verificaron ambas páginas visualmente; no se infiere la fecha aplicable a un expediente ni se certifican cambios posteriores.

**DS 067:** el PDF incluye fragmentos de otros instrumentos. La DCF sobre vigencia del ROF OECE está en p. 2, no debe confundirse con la disposición de Perú Compras que aparece en p. 1. La primera DCF condiciona el inicio y exceptúa la segunda DCF; no se asigna una fecha universal a todo el documento.

**FUP:** objeto y ámbito leídos en p. 2. El numeral 11.3, p. 12, remite a comunicaciones de implementación y se refiere a documentación en procedimientos de selección. No se convierte esa referencia en dispensa automática del trámite de ampliación RNP. La página oficial declara publicación 10/02/2026 e inicio 11/02/2026; todavía falta comprobar cada efecto concreto.

**DL 1715:** su artículo 3 modifica el artículo 85.1 e de Ley 32069, sobre medidas cautelares. Se conserva como parte de la cadena legal, sin introducir un requisito de categoría de consultor. El expediente incluye antecedentes y otras normas en las páginas de publicación; no se trata todo el PDF como texto exclusivo del DL. El visor web presenta un encabezado ajeno, por lo que se cotejaron cuerpo, identificador y páginas de publicación.

## Indexación comprobada
Se creó un **índice complementario separado**, `normativa/indices/complemento-cierre-piloto.sqlite`: 17 documentos, 240 fragmentos por página y **212 con texto**. Catorce PDF disponen de extracción digital; el DL requiere OCR/revisión, y HTML/XLSX permanecen sin lector automático. El formulario FUP también aparece en la p. 13 de su PDF.

Tres referencias conocidas fueron recuperadas: ROF actualizado p. 36, Resolución 090 p. 4 y directiva FUP p. 12. [Resumen de indexación](../../normativa/indexacion/reporte-cierre-piloto-2026-10-30.json). No se midió recuperación general ni se unificó este índice con el anterior. Los índices anteriores se conservan como instantáneas, con sus propios metadatos y cortes.

## Qué queda abierto
Las cinco preguntas del registro v0.1 tienen ahora [criterios adoptados y excepciones](CRITERIOS_ADOPTADOS_PILOTO.md), documentados el 31/10/2026 en el [registro vigente v0.2](../../normativa/decisiones-piloto.v0.2.json). Se identifica autor asistente IA y fecha, sin registrar revisión humana inexistente. La condición de Ley 32732 queda delimitada a la quinta DCM y la publicación de RPE 090 se verificó el 19/12/2025. El cuadro anterior conserva el estado de adquisición del 30/10; estas decisiones actualizan sus cotejos focalizados. El cotejo primario del TUO y los recursos también continúan abiertos dentro del alcance jurídico.

La presencia de los 36 archivos no prueba que el universo normativo sea suficiente. Los históricos y anexos destinados a otros procedimientos permanecen separados del mínimo. Ningún registro ni control se declara apto para evaluación jurídica.

## Repetición y pruebas
```powershell
python scripts/verificar_biblioteca.py --verificar-originales
python scripts/verificar_cobertura_piloto.py --verificar-originales
python scripts/indexar_normativa.py build --database normativa/indices/OTRO_INDICE.sqlite --manifest normativa/manifiesto-cierre-piloto-2026-10-30.json
python -m unittest discover -s tests -p "test_*.py"
```

**53 pruebas técnicas aprobadas:** 47 anteriores, cinco de cobertura y una del límite de manifiestos. Se comprobaron adquisición completa sin aprobación jurídica, faltantes, alteración de original, fuentes no oficiales, rutas externas y planes duplicados o que pretendan habilitar reglas. Un manifiesto externo se rechaza conservando el índice anterior. El modo sin originales solo informa cobertura declarada; no permite declarar íntegra la copia local.
