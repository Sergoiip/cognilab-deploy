# TaskNotes

**Versión del catálogo:** 4.13.10 · MIT · repo callumalpass/tasknotes

## Metodología (según el plugin)
**Una tarea es una nota.** Cada tarea es un archivo Markdown con frontmatter (título, estado, fecha, prioridad, contextos, proyectos, tiempo estimado, recurrencia). Las vistas (lista, kanban, calendario, agenda) son consultas de Obsidian Bases sobre esas notas. No hay base de datos propia. Los nombres de las propiedades se pueden reasignar, y se pueden añadir campos propios que quedan disponibles para filtrar y agrupar. Acepta lenguaje natural al crear tareas («comprar X mañana #recados»), seguimiento de tiempo, pomodoro, recurrencia con reglas estándar y sincronización de calendario. Tiene API HTTP opcional.

## Recomendación CogniLab
- **Un proyecto = una nota; una tarea = una nota enlazada al proyecto** con la propiedad `projects`. Es la unión que usan Task Atlas y los reportes.
- **Pocas tareas clave, no cientos.** Una tarea por resultado que se pueda marcar como hecho. Lo fino va dentro de la nota.
- **Estados mínimos:** abierta, en progreso, hecha. Añadir más solo si el cliente los usa de verdad.
- **Si hay otro sistema que genera tareas** (por ejemplo un tablero que sincroniza notas), tratar esas notas como de solo lectura y crear las tareas propias en otra carpeta. Si no, el sincronizador pisa los cambios.
- Usar el campo `meta` y `clave` que lee Task Atlas cuando el cliente lleve metas.

## Cuidado
- Depende de Obsidian Bases. Versiones viejas de Obsidian no sirven.
- Las notas con Markdown pegado en el título (viñetas, negritas) generan tareas basura. Limpiar el título al crear.
