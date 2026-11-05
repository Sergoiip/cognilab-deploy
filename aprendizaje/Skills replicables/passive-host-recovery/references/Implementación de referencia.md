# Implementación de referencia

## Runtime y conexión
La fuente se refiere a Hermes Agent, código versionado en Git y dependencias con uv. Cargar su skill operativa y consultar documentación oficial antes de adaptar comandos. Para un runtime aislado, usar un archivo de `git archive` de {{REVISION_FUENTE}} y resolución congelada del archivo de bloqueo con extras realmente requeridos. Comparar hashes y bytes instalados; no confundir un entorno que importa con compatibilidad de todos los canales.

Usar `HERMES_HOME` apuntando a un hogar de ensayo para las verificaciones. Evitar `hermes import`: puede iniciar un gateway. La validación del CLI debe excluir comandos con efectos secundarios.

Para SSH determinista de servicio, `-F /dev/null` evita includes de configuración que un sandbox de systemd podría rechazar. Configurar explícitamente identidad y archivo de `known_hosts` con validación estricta. Mantener este último fuera del scratch. No se exportan claves ni nombres de máquinas.

## Bases y almacenamiento
Usar `sqlite3.Connection.backup` con origen abierto mediante URI de solo lectura; después ejecutar `PRAGMA integrity_check` sobre la copia y comparar conteos por tabla. No hacer rsync de DB/WAL vivos. Las bases se copian individualmente; advertir que no hay corte transaccional global del hogar.

El perfil por defecto y otros perfiles son dominios distintos: nunca ampliar alcance a estos últimos sin permiso. Espacios kanban pueden duplicar grandes volúmenes de audio o notas: excluirlos si no pertenecen a la lista permitida. Manifiesto de todos los archivos con SHA-256 y tamaño; directorios 0700, archivos 0600. Usar staging y renombrado atómico dentro de un sistema de archivos compatible. Un temporizador de usuario systemd puede ejecutar solo backup, con retención limitada y sin comandos de promoción.

## Promoción y ensayo
Inspeccionar gateway existente y puertos reales mediante herramientas del sistema. Rechazar por alcance positivo del primario, pero no considerar la falta de alcance como autorización. Quarantinar cron, kanban, outboxes y hooks restaurados antes del primer arranque. Revisar leases y entregas antes de autorizar resume.

No se incluyen implementaciones, backups ni resultados de simulacros; los controles son requisitos a probar en cada destino, no garantías de recuperación.

## Documentación pública
- https://hermes-agent.nousresearch.com/docs
- https://docs.python.org/3/library/sqlite3.html

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
