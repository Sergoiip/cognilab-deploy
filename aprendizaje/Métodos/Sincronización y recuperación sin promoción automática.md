---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Sincronización y recuperación sin promoción automática

## Parámetros
RAIZ_DATOS, CONFIG_PRIVADA, EXCLUSIONES, SERVICIO_UNICO, RETENCION, DESTINO_RESTAURACION y AUTORIDAD_PRIMARIA deben acordarse. Credenciales quedan fuera del paquete.

## Sincronización
- Evitar dos sincronizadores sobre el mismo árbol. Pausar uno y comprobar también su servicio antes de implantar otro; cambiar filtros puede exigir rebaselización explícita. No ejecutar resync u override global como reparación genérica.
- Excluir configuración del editor, estados del agente, plugins, claves y runtime; una exclusión nueva no elimina copias antiguas ni descubre secretos dentro de Markdown. Depuración y rotación previas se tratan aparte.
- Conservar variantes de conflicto y diagnosticar ambos lados; no elegir por mtime. Un archivo que sigue creciendo no está listo para reconciliación.
- Versionado local no sustituye respaldo externo y puede compactar ediciones de ráfaga. Comprobar política real con archivo sintético y separación temporal suficiente; editar/borrar/restaurar solo con autorización.

## Recuperación
- Obtener snapshots consistentes por base con backup de SQLite y comprobación de integridad; reconocer que no existe transacción global entre bases y archivos.
- Validar inventario, hashes, rutas y compatibilidad de runtime antes de restaurar a un directorio inexistente y aislado. No importar bases ni credenciales al paquete replicable.
- Respaldo pasivo no es failover. Falta de conectividad no prueba que el principal esté aislado: exigir evidencia manual de exclusión mutua antes de promoción.
- Revisar cron, entregas pendientes, hooks, plugins, rutas y autenticación; no reproducir trabajos restaurados automáticamente. Aceptar explícitamente la posible pérdida desde el snapshot.
- Separar pruebas offline de activación real. Los scripts locales de recuperación revisados están acoplados a rutas, host y rol; no se exportan ni se ejecutan aquí.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
