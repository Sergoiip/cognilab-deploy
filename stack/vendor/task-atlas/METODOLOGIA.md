# Task Atlas — metodología y recomendaciones de uso

Qué resuelve y cómo usarlo bien — no la mecánica de instalación (eso va en `README.md`).

## Qué problema resuelve

Una lista plana de tareas esconde dos cosas que importan más que la lista misma: **qué depende
de qué**, y **qué está en espera vs. qué avanza solo**. Task Atlas dibuja esas tareas como nodos
en un lienzo (hub, áreas, tareas) enlazados por el frontmatter real de TaskNotes — el mapa no es
decorativo, es la forma de ver de un vistazo dónde se traba el trabajo.

## Cómo se relaciona con las otras piezas

- **Cadence** registra el hecho de negocio (cliente, trato, gasto).
- **TaskNotes** gestiona la tarea en sí (una nota por tarea, con `status`/`scheduled`/`projects`).
- **Task Atlas** la dibuja: una tarea sin nodo visible en el mapa normalmente significa que le
  falta el enlace `projects` a su padre, no que "no existe".

## Principios de uso (heredados del método A3 — Flujos de trabajo)

1. **Silencio no es completado.** Un nodo que no se mueve ni cambia de estado durante varios días
   no significa que está resuelto — significa que nadie lo ha tocado. Revisarlo activamente, no
   asumir que "si no suena la alarma, va bien".
2. **No llenar todas las horas del mapa.** Un plan que ocupa el 100% de la capacidad real no deja
   espacio para lo urgente que aparece a mitad de semana; eso rompe el ritmo completo, no solo esa
   tarea.
3. **Planear según capacidad real, no según deseo.** Si el mapa muestra más nodos "en curso" de
   los que una persona puede sostener a la vez, el problema no es el mapa — es que hay que
   decidir qué se pausa.
4. **Revisión con cadencia fija**, no "cuando se acuerde": inicio de día (qué toca hoy) y cierre
   de semana (qué avanzó, qué quedó en espera y por qué).

## Cómo leer el mapa

- **Hub → áreas → tareas:** el hub es el punto de partida; las áreas agrupan por frente de
  trabajo; cada tarea cuelga de su área por el enlace de `projects`.
- **Estados por color/nodo:** un nodo "en espera" sin nota de qué espera es una señal de alerta —
  toda tarea en espera debe decir espera de qué o de quién.
- **Auto-layout:** reorganiza el mapa automáticamente; úsalo después de crear varios nodos de
  golpe en vez de acomodarlos a mano uno por uno.
- **Arrastrar para crear:** sirve para capturar una tarea nueva directamente desde el mapa sin
  salir a crear la nota aparte — mantiene el hábito de "todo tarea-like se vuelve una nota", no
  una idea suelta en la cabeza.

## Cuándo mirarlo (recomendación de cadencia)

- **Inicio de día:** confirmar que lo planeado para hoy sigue siendo lo correcto antes de empezar
  a trabajar, no a mitad de mañana.
- **Cierre de semana:** identificar nodos que no se movieron toda la semana y decidir
  explícitamente qué pasa con cada uno (se retoma, se reagenda con fecha real, o se cancela).

## Qué NO hacer

- No usar el mapa solo para "verlo bonito" sin tocarlo — si no se actualizan los estados, el mapa
  miente igual que una lista desactualizada, solo que visualmente.
- No crear nodos huérfanos (sin `projects` a un área/hub): se vuelven invisibles en la vista de
  mapa aunque existan como nota.
- No sobrecargar un solo día/área con más nodos de los que realmente se pueden cerrar — es mejor
  ver el mapa "incómodamente lleno" a tiempo que descubrirlo al final de la semana.

## Dependencia

Requiere TaskNotes instalado y activo (lee `TaskNotes/Tasks/`). Sin TaskNotes, Task Atlas no
tiene qué dibujar.
