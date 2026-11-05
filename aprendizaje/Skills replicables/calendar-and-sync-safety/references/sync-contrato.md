# Contrato de sincronización recurrente

## Configuración preventiva
1. Descubrir SO, herramientas existentes y remotos. Confirmar carpetas y dirección antes de cualquier upload; nunca asumir todo el HOME. Un explorador remoto no es cliente de sync.
2. Autenticar en navegador por flujo soportado, sin contraseñas ni tokens en chat, argumentos o logs. Comprobar identidad con metadatos mínimos del proveedor; un nombre de remote no basta.
3. Examinar nombres, tamaños, symlinks y rutas de claves JSON sin imprimir valores. Excluir secretos, configuración de plugins con tokens, workspaces, cachés y dependencias; mantener notas/tareas dentro del alcance aprobado. No seguir symlinks fuera de la raíz.
4. Guardar listados y locks en estado persistente fuera de caches podables. Mantener filtro único y estable. Sentinelas iguales en ambos lados, límite de borrados y backups fuera de cada raíz reducen el daño; backups remotos deben vivir en su mismo remote correspondiente.
5. Inicializar solo tras dry-run revisado y filtros finales. Conservar conflicto de ambos lados, no elegir ganador silencioso. Omitir shortcuts o documentos nativos si se promete equivalencia de archivos ordinarios y declarar esa exclusión.
6. Servicio de usuario oneshot y timer deben tener parada ordenada y frecuencia descrita desde fin de ejecución, no tiempo real continuo. Ejecución sin sesión requiere autorización separada, no activar linger por defecto.
7. Probar mediante la unidad real un archivo propio: local → remoto, cambio remoto → local, borrado → desaparecido en ambos y recuperable en backup. Hacer comparación completa y verificar exclusiones en el destino, no solo en el filtro escrito.
8. Leer resultado de servicio, habilitación/actividad del timer y próximo disparo después de terminar. Un timer recién habilitado puede dispararse inmediatamente si el tiempo de arranque ya transcurrió.

## Mantenimiento y recuperación
Pausar planificación antes de mantenimiento y comprobar que no quede ejecución activa. Preservar listados, filtros y ambas versiones tras errores. No programar resync automático; un recover puede reutilizar listados y un archivo que crece puede invalidar el ciclo. No crear retención ni borrar versiones acumuladas sin autorización.

Un aviso de retiro del cliente OAuth compartido exige plan de reautorización, no promesa de durabilidad. No crear proyectos cloud por iniciativa propia. Un resultado actual exitoso no resuelve ese riesgo futuro.

## Implementación de referencia
rclone bisync ofrece check-access, max-delete, resilient, recover, max-lock, filters-file, backup-dir1/2 y preservación con conflict-resolve none/conflict-loser num. Validar opciones con ayuda local y documentación pública para la versión instalada; no copiar una línea de flags ciegamente. Usar --no-output en configuración cuando suprima credenciales. KIO GDrive es acceso de navegación, no sustituto de sincronización.

Origen: abstracción de lecciones locales de sincronización y verificación por servicio real.
