# Plugins de Obsidian del stack: metodología y uso recomendado

Una ficha por plugin. Cada una separa tres cosas para no mezclar hechos con opinión:
- **Metodología (según el plugin):** lo que dice su propia documentación.
- **Recomendación CogniLab:** cómo conviene usarlo en el deploy. Es criterio nuestro.
- **Cuidado:** límites, riesgos y lo que no está probado.

| Plugin | Perfil | Para qué | Ficha |
|---|---|---|---|
| Obsidian Git | ligero | respaldo y versionado de la bóveda | [obsidian-git.md](obsidian-git.md) |
| Templater | ligero | plantillas de notas | [templater.md](templater.md) |
| TaskNotes | negocio | tareas como notas | [tasknotes.md](tasknotes.md) |
| Task Atlas | negocio | metas, tareas y hábitos en canvas | [task-atlas.md](task-atlas.md) |
| Cadence (fork CogniLab) | negocio | CRM, planner y finanzas | [cadence.md](cadence.md) |
| Excalidraw | equipo | mapas y diagramas a mano | [excalidraw.md](excalidraw.md) |

## Principios comunes
1. **Markdown es la fuente de verdad.** Todos guardan datos en notas con frontmatter. Si un plugin falla, los datos siguen legibles y se pueden migrar.
2. **Un campo, un dueño.** Cada propiedad la escribe un solo plugin o una sola persona. Task Atlas lee lo que TaskNotes escribe y no lo duplica.
3. **Las máquinas hacen lo mecánico; la persona decide.** Los plugins organizan y muestran. Qué se prioriza y qué se descarta lo decide el cliente.
4. **Todo es opcional.** Si el cliente ya usa otra herramienta, se respeta (modo `cliente` del instalador).

## Orden de adopción sugerido (propuesta, sin medir)
Git y Templater en la fase 1. TaskNotes cuando el cliente ya anota tareas. Cadence cuando hay clientes o ventas que seguir. Task Atlas al final, cuando ya hay metas y tareas que mapear. Excalidraw solo si el cliente piensa en diagramas.

## Cómo se verificó
Las secciones «según el plugin» salen de los README oficiales de cada repositorio (versión del catálogo). Las recomendaciones salen del uso en CogniLab. Ninguna se ha probado todavía con un cliente externo.
