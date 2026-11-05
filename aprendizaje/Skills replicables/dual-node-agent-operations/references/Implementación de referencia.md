# Implementación de referencia · Hermes, Tailscale y SSH

Esta sección concreta el patrón genérico; los nombres técnicos no representan datos de clientes.

- Consultar la habilidad hermes-agent y documentación oficial vigente antes de elegir comandos, flags y claves de configuración. Descubrirlos en la instalación; no fijar una versión universal.
- Confirmar perfil activo, mecanismos soportados de backup y conexión remota SSH de Desktop, autenticación del backend y comportamiento de gateway y cron.
- Tailscale no sustituye autenticación. SSH requiere huella contrastada; mantener restricciones de red y no publicar puertos del router.
- Una conexión remota de Desktop no transfiere mensajería ni tareas programadas. MCP conectado no prueba todas las herramientas.
- Usar SQLite backup o mecanismo consistente soportado; no sincronizar bases vivas. Separar sincronización de documentos de snapshots recuperables.
- En sistemas con systemd, comprobar unidades, reinicio automático y persistencia de usuario. No asumir que todas las plataformas usan ese gestor.
- Dependencias gráficas como Obsidian/TaskNotes deben probarse después de reiniciar y sin sesión gráfica cuando eso forme parte del requisito.
- Ejecutar corte desde un coordinador independiente del gateway que se detendrá. Verificar aislamiento de todos los escritores antes de promover.
- El script Herramientas/exportar.py del paquete exporta documentación; no migra sistemas ni implementa promoción automática.

Consultar también las referencias de procedimiento, aceptación y recuperación de esta skill. Esta implementación es documental; cada instalación requiere sus propias pruebas.

Origen: adaptación técnica de un patrón operativo generalizado; sin configuración de clientes.
