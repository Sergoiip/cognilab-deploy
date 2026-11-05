# Actualizaciones verificadas sin perder extensiones

## Antes de tocar runtime
- Fijar origen y commit real; texto del commit y nombre de ZIP no prueban tag. Preservar paquete original y manifiesto completo.
- Revisar licencia de cada versión aunque conserve número o nombre. Una licencia anterior permisiva no autoriza código nuevo restrictivo. Si no hay derechos de redistribución, excluir bundle y patches de la entrega.
- Auditar bootstrap y helpers por sus efectos completos. Un flag que excluye aplicaciones no garantiza que no escriba bienvenida, carpetas, identidad o skills.
- Hacer comparación por archivo entre versión previa, nueva y runtime; preservar extensiones si upstream no cambió y detenerse ante conflictos simultáneos. Una copia en un perfil no actualiza otros perfiles ni sesiones ya cargadas.
- Conservar versiones operativas más recientes del registro canónico de tareas. No degradarlas por consistencia con catálogo.

## Migración de identidad técnica
Un cambio de ID de plugin o tipo de vista es migración. Con autorización y respaldo privado, copiar configuración sin perder campos, sustituir solo IDs exactos en activación y vistas autorizadas y mantener una sola implementación habilitada. Conservar la antigua para rollback, no dos instancias activas.

Probar matchers de proyectos contra rutas completas y basename; no asumir que una actualización conserva la corrección local. Aplicar un parche revisado en staging no convierte runtime en vendor byte-idéntico. Mantener hashes originales y manifiesto de diferencias independiente.

## Alcance y pruebas
Distinguir mencionado en documentación, incluido como archivos, instalable por bootstrap, copiado en disco, habilitado, cargado y funcionalmente probado. Buscar nombres alternativos en todo el texto del paquete antes de declarar ausencia, sin equiparar productos por semejanza.

Separar manifiesto de plugins del inventario de skills. Validar hashes, sintaxis de JavaScript y conservación de ajustes; no copiar data.json a un staging compartible. Una API saludable prueba el registro de tareas, no el renderizado de paneles derivados. Un matcher probado no demuestra Today, Calendar y Home equivalentes.

No reiniciar editores con trabajo sin guardar. CLI que depende de DISPLAY o está deshabilitada no significa instalación rota. Obtener entorno gráfico real antes de diagnosticar y no activar depuración por rutina.

## Paquetes y propuestas
Comparar esquema consumido con generador: una encuesta puede omitir claves y un plan puede emitir exclusiones vacías. Llevar exclusiones aprobadas explícitamente. Un catálogo de esqueletos o variantes por desarrollar no implementa un flujo ni satisface aceptación. Conservar fuente canónica completa, no depender de scratch.

## Implementación de referencia y límite legal
Cadence ha usado IDs distintos entre distribuciones; TaskNotes debe mantenerse como autoridad canónica. Task Atlas tuvo cambios de licencia con versión aparente igual. Esta referencia describe lecciones de interoperabilidad: no distribuye su código, parches ni bundle restrictivo y no hereda licencias antiguas.

Origen: síntesis de lecciones locales de comparación, migración y pruebas de plugins.
