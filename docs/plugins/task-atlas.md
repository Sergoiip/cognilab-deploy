# Task Atlas

**Versión del catálogo:** 0.4.0 · MIT · autor Sergio Marcucci · fuente en `stack/vendor/task-atlas/`

## Metodología
Propia de CogniLab: **ingeniería inversa desde el resultado.** Se parte de un norte, se baja a pocas metas, de cada meta salen las tareas clave (con dependencias) y de cada meta se derivan hábitos que la sostienen. El mapa muestra todo en un canvas infinito.

Cómo lo lee el plugin (campos en español y fijos):
- `type: norte` y `type: meta` en notas de `Roadmap/Metas/`. La meta lleva `fase`, `orden`, `color`, `hoy`, `resultado`, `medida`.
- Tareas en `TaskNotes/Tasks/` con `meta`, `clave: true`, `depende_de` y `tipo: habito` para los hábitos.
- Alcances: Roadmap, Hábitos, Operaciones, Clientes y Todo.

## Recomendación CogniLab
1. **Escribir el norte en una frase** y el resultado que se espera.
2. **De 4 a 6 metas.** Si salen más, agrupar en fases.
3. **Tareas clave por meta, no todas.** Las que si no se hacen, la meta no avanza.
4. **Marcar dependencias** solo donde una tarea no puede empezar sin otra.
5. **Derivar hábitos** de cada meta (frecuencia semanal o mensual) y revisarlos en la sesión de seguimiento.
6. Instalarlo **después** de TaskNotes y de tener metas escritas. Con el mapa vacío no aporta.

## Cuidado
- **No crea las metas ni las tareas.** El instalador solo copia el plugin. Hoy la configuración se hace a mano; un asistente que la proponga está pendiente.
- Interfaz y campos en español, sin versión genérica ni traducción todavía.
- Depende de TaskNotes. En desarrollo; solo se ha probado en la bóveda de CogniLab.
