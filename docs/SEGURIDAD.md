# Seguridad y separación de código y documentos
Estado: requisitos de diseño; salvo .gitignore, controles aún no implementados.

El repositorio es público. Mantener fuera de Git expedientes, DNI/RUC asociados a personas, datos financieros, firmas, informes, auditorías, conversaciones, índices privados, OCR y credenciales. .gitignore reduce errores, pero no impide forzar una subida: revisar siempre el contenido antes de cada commit. No usar issues para copiar información de proveedores.

- Raíz de datos privada configurable y separada del checkout; acceso por usuario/rol y expediente. Revisar permisos de Drive/OneDrive, copias de respaldo y plazo de retención autorizado.
- Lista permitida de extensiones; límites de tamaño/páginas, rechazo de rutas externas y enlaces simbólicos que escapen de la raíz. Cuarentena de archivos sospechosos y procesamiento sin macros.
- Documentos y resultados de búsqueda son datos no confiables: instrucciones insertadas no pueden cambiar permisos, ejecutar comandos, enviar correos ni extraer otros expedientes.
- Sin enviar contenido real a modelos externos hasta definir proveedor, autorización institucional, minimización y políticas de retención. Claves en almacén de secretos, nunca en Git o logs.
- Auditoría con IDs opacos, hashes y eventos; no registrar texto sensible por defecto. Cifrado, restauración de respaldos y eliminación de derivados se deben probar.
- Fuentes normativas solo de dominios oficiales autorizados; conservar URL final y detectar cambios de contenido. Una URL oficial no implica que un documento sea vigente.
- Revisión humana de conclusión y Word. Firma, notificación, presentación y envío externo requieren acción explícita del responsable.
- Separar entornos de desarrollo, prueba y operación; pruebas públicas exclusivamente sintéticas.
- Registrar incidente, suspender procesamiento, retirar accesos y rotar secretos si hay exposición. Borrar un archivo del último commit no borra su historial.

Pendiente revisión de obligaciones de datos personales, políticas institucionales y permisos para usar documentos de trabajo; este documento no certifica cumplimiento legal.
