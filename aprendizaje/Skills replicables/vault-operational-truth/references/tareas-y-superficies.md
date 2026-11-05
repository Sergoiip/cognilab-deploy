# Tareas canónicas y superficies derivadas

## Conexión y configuración
Descubrir la bóveda abierta, flags del servidor y puerto configurado, sin imprimir tokens. La ausencia del catálogo no prueba ausencia de servidor integrado. Usar el registro oficial de conexión y el esquema real de las herramientas; no editar a mano bloques completos de configuración. Comprobar bind local y health con identidad de la bóveda. La aplicación que aloja el servicio debe estar abierta.

En un escritorio remoto, obtener variables gráficas y autorización de la sesión viva. No fijar sockets ni archivos xauth transitorios. Un registro de bóveda copiado o un URI que terminó sin error no demuestran cuál bóveda se abrió. Si es necesario modificar ajustes en disco, cerrar solo ventanas identificadas y con autorización, conservar el registro anterior y reabrir de forma controlada. El arranque tras login no prueba servicio antes del login ni un reinicio completo.

## Esquemas y escritura
- Leer schemas antes de llamar herramientas; recorrer páginas y comprobar total, offset y returned según el contrato real. Comparar rutas únicas entre API HTTP y MCP, no solo longitud de arrays.
- Buscar tarea existente; fijar estado, prioridad, tags, enlaces y detalles de forma explícita. Para tareas sin fecha comprobar que la creación no haya aplicado el día actual; limpiar scheduled y due con null por API y leer de nuevo, sin cambiar defaults globales.
- Registrar campos personalizados antes de enviarlos; un mapper puede descartarlos silenciosamente. Verificar opciones de filtro y leer la propiedad persistida, no afirmarla por estar en texto libre.
- Enlaces de proyecto con ruta completa deben resolverse por metadata del editor; basename solo es compatibilidad y puede colisionar. Probar enlaces completos, alias y nombres repetidos.
- Reemplazar capturas provisionales por enlaces solo tras confirmar persistencia canónica. Un backup con tags de tarea y extensión .md puede reaparecer como duplicado incluso dentro de un archivo histórico.
- Si el SDK MCP difiere del ejemplo, inspeccionar firma, factory HTTP, tupla de streams y nombres de campos. Un entorno aislado debe declarar sus dependencias HTTP explícitamente; no imprimir bearer ni llevarlo a argumentos de procesos.

## Prueba por superficie
1. Obtener snapshot canónico con rutas; resolver objeto de archivo cuando una mutación oficial lo necesite. Prohibir escritores YAML alternativos en tests.
2. Usar la autoridad de estados para completado personalizado. Un checkbox solicita un objetivo de completitud, no un ciclo arbitrario de estados.
3. Comprobar selección scheduled OR due, archivo/completado y secciones disjuntas. No inferir paridad de home o calendario desde el panel diario.
4. Mostrar agenda real como sección soportada; un enlace o transclusión no necesariamente presenta sus puntos en una tarjeta Markdown. Probar también el botón de apertura de nota diaria y su plantilla futura, preservando diario.
5. Fijar fecha expandida en consultas de notas históricas. Esperar tarjetas visibles de altura no nula; toolbar con total puede preceder al render asíncrono y coexistir con DOM oculto.
6. Refrescar solo región de tareas ante cambios; proteger entradas en debounce y usar generaciones contra respuestas antiguas. Probar títulos con muchos chips: separar fila del título y enlaces con wrap para evitar colapso.
7. Harness aislado: ejecutar bundle staging con stubs del editor y DOM de prueba, hacer fallar mutaciones crudas y verificar llamadas oficiales. Un fixture que afirma que todos los archivos existen puede dejar un bucle de colisiones infinito.
8. RED contra base y GREEN contra staging; conservar backup/diff y verificar que runtime no cambió durante ensayo. No cambiar tareas reales para probar toggles.

## Implementación de referencia
TaskNotes: cacheManager.getAllTasks() entrega tareas con path; statusManager interpreta estados; updateTaskProperty y taskService.createTask son seams oficiales que deben verificarse en la versión instalada. applyDefaults:false evita defaults en quick-add cuando está soportado. Cadence y Task Atlas pueden visualizar el mismo registro sin compartir todos sus selectores. Dependencias visuales de Atlas no equivalen a disparadores del sistema de tareas o del agente. No se incluye código de esos plugins.

Origen: reformulación de lecciones locales de tareas, agendas y pruebas de integración.
