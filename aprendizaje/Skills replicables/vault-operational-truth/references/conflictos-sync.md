# Recuperación de conflictos sin atribuciones prematuras

1. Ante una nota vacía o dibujo desaparecido, inventariar el nombre original, hermanos de conflicto, backups y estado del sincronizador. Leer script, filtros y journal antes de culpar al editor.
2. Una política que conserva ambas versiones puede renombrar las dos y retirar el nombre original. Distinguir esa retirada de una posterior recreación a cero bytes: esta última requiere evidencia independiente de autoría.
3. Detener planificación y comprobar que no siga corriendo el servicio antes de restaurar. Conservar ambos lados y listados persistentes. Pausar timer no equivale a deshabilitarlo para el próximo login.
4. Inspeccionar archivos que siguen creciendo, por ejemplo grabaciones dentro del árbol. Pueden abortar comparación por cambio de tamaño; un modo recover puede reutilizar listados previos. No detener una grabación ni disparar resync por iniciativa propia.
5. Comparar versiones y restaurar datos existentes, no regenerar el dibujo para disimular una pérdida. Validar contenedor comprimido, JSON, elementos no eliminados y textos; eso prueba datos, no render visual.
6. Reproducir políticas solo en dos árboles aislados. Añadir un archivo estable además del que cambia: si cambia todo el conjunto, una protección de cambios totales puede abortar antes de llegar al conflicto que se pretende probar.
7. Tras restauración autorizada, verificar bytes y comportamiento; reanudar solo con alcance y política comprobados. No borrar conflictos ni históricos por ordenar.

## Implementación de referencia
rclone bisync con --conflict-resolve none y --conflict-loser num es un ejemplo de preservación de ambos lados. Leer ayuda de la versión instalada antes de usar flags. En Excalidraw, un bloque compressed-json puede validarse mediante LZString.decompressFromBase64 y parseo JSON dentro de un entorno aislado, sin modificar la fuente. No se incluye código de plugins.

La configuración preventiva del sincronizador se describe en la skill de calendario y sincronización segura del paquete; esta referencia se concentra en recuperación y conserva el principio de no ejecutar resync automático.

Origen: abstracción de incidentes locales de notas, dibujos y sincronización.
