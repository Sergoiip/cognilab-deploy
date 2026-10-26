# Task Atlas

Mapa en lienzo infinito de tus tareas de [TaskNotes](https://github.com/callumalpass/tasknotes): una nota = una tarea. Muestra hub, áreas y tareas como nodos unidos por el frontmatter, con estados, prioridades, arrastrar para crear y organización automática. Se puede exportar a un `.canvas`.

> English: infinite-canvas map of your TaskNotes tasks (one note = one task) with nodes linked through frontmatter, statuses, drag-to-create and auto-layout. Exports to `.canvas`.

**Requiere** el plugin TaskNotes. Versión 0.4.0, en desarrollo; no está publicado en la tienda de Obsidian.

## Uso
1. Instala TaskNotes y crea tareas.
2. Abre Task Atlas desde el ícono de la barra lateral o con el comando «Abrir Task Atlas».
3. En Ajustes elige carpeta de tareas y el alcance (Roadmap, Hábitos, Operaciones, Clientes, Todo).

## Estado
- Interfaz y textos en español. La traducción al inglés está pendiente.
- Los alcances usan nombres de campo en español (`area`, `cliente`, `meta`, `depende_de`). Falta volverlos configurables.
- Pendiente para la tienda de Obsidian: textos en inglés, campos configurables, pruebas en otras bóvedas, `versions.json` y release en GitHub.

## Idea para la versión pública: asistente de configuración
Un script que se corre una vez, lee las notas de tareas, proyectos y del ecosistema (por ejemplo Cadence), infiere la intención de cada una y propone el árbol norte → metas → tareas clave → hábitos, con ingeniería inversa desde el resultado. Luego escribe los campos que el plugin lee (`type: norte|meta`, `meta`, `clave`, `depende_de`, `tipo: habito`). La primera configuración (Operaciones de CogniLab, 2026-10-23) se hizo a mano y sirve de plantilla.

## Licencia
MIT. © 2026 Sergio Marcucci.
