# Procedimiento operativo · Hermes dual

## Principios
Un único escritor operativo y una fuente de estado activa. El cliente remoto no es automáticamente un ejecutor local ni un respaldo recuperable. Tailscale aporta conectividad privada; no sustituye autenticación del backend ni verificación SSH. Compartir documentos no equivale a compartir memoria e historial.

## Fases y puertas de avance
1. **Descubrir:** roles autorizados, fuente canónica, sistemas, perfiles, versiones, canales, tareas, dependencias y responsables. Salida: inventario sin secretos.
2. **Asegurar acceso:** Tailscale, clave SSH dedicada, huella contrastada, límites de red y autenticación. Salida: acceso probado y superficie de escucha documentada.
3. **Proteger:** respaldo consistente de ambas instalaciones, integridad y restauración aislada, retención y permisos. Salida: punto de retorno recuperable.
4. **Preparar:** versiones compatibles y rutas adaptadas. Backend destino sin mensajería ni cron activos. Salida: historial, modelo y herramientas probados sin duplicación.
5. **Conectar:** Desktop remoto y conexión local diferenciada; capacidades locales probadas una por una. Salida: matriz capacidad→equipo→prueba→límite.
6. **Compartir archivos:** alcance explícito, exclusiones, versionado, prueba bidireccional, borrado y restauración. Salida: ausencia de solapamiento con otros sincronizadores. No incluir estado vivo de Hermes.
7. **Autorizar corte:** confirmar ventana, estado de origen, rollback, canal alternativo y coordinador independiente del gateway. Salida: autorización registrada y escritores inventariados.
8. **Cortar:** detener escritores, capturar estado final consistente, transferir y verificar; impedir reactivación del origen antes de activar destino. Salida: una única operación activa.
9. **Validar:** canal real, tarea inocua, contexto, herramientas, reinicio, ausencia del secundario y recuperación. Salida: evidencia y pendientes explícitos.

## Operación permanente
Definir responsables de actualizaciones, energía, respaldos, alertas y revisión de restauración. Medir retraso y duración de copias antes de prometer una frecuencia. Alertar por respaldo obsoleto sin activar automáticamente otro gateway. Registrar dependencias que exigen sesión gráfica y límites cuando un equipo esté apagado.

## Condiciones de aborto
Identidad SSH inesperada; respaldo no verificable; incompatibilidad no resuelta; actividad de escritores desconocida; estado final ambiguo; duplicación; falta de autenticación; fallo de integridad. Detener cambios, preservar evidencias y no promover otro equipo hasta aislar al anterior.

Los comandos concretos se descubren en la versión instalada y documentación oficial; este procedimiento no inventa flags ni rutas universales.
