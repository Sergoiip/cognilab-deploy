# Organización temporal: carga, energía y horarios

> Parte de la **Organización Intencional** (CogniLab). Es la versión general, sin datos de
> ningún cliente. Explica cómo el agente arma y protege la semana de una persona a partir de su
> energía real, no de las horas libres del calendario. La usa el módulo A3 (Flujos de trabajo y
> ritmo semanal) y se alimenta del mecanismo «carga biológica-cognitiva» del grupo 9 del canvas
> (ver `bootstrap/METODO-DEL-CAOS-AL-SISTEMA.md`).

## Fundamento

- **El tiempo es fijo y la energía es dinámica.** Se planea pensando en una persona que funciona
  por ciclos biológicos, no en una máquina constante. Por eso cada tarea se ubica según el tipo
  de carga que impone, no según el primer hueco libre.
- **La atención es un recurso finito y un músculo que se entrena.** Se trabaja en bloques cortos
  con pausas, y se amplían de forma progresiva. La fuerza de voluntad no se exige en bruto: se
  diseñan los activadores.
- **Entrar en foco cuesta energía.** Hay que romper una barrera inicial (la «muralla»). Para
  bajar ese costo, cada bloque profundo arranca con una **pregunta invitadora**: una pregunta
  curiosa, tipo experimento, que genera tensión y que solo se responde haciendo el trabajo.
  Funciona por la curiosidad y por el efecto Zeigarnik. El bloque también lleva un
  **entregable** concreto que dice cuándo está terminado.
- **El sistema libera, no restringe.** Nunca se llenan todas las horas. Si un día no hay
  energía, el plan se adapta y la persona no tiene que forzarse.

## 1. Clasificar la carga (triple clasificación)

Toda actividad recurrente entra en una de tres categorías antes de planear:

| Carga | Qué es | Ejemplos |
|---|---|---|
| **Analítica** (foco profundo) | Concentración alta, novedad, problemas complejos, decisiones críticas, escritura o código intenso | Presupuesto, propuesta, estrategia, preparar una negociación |
| **Operativa** (flujo ligero) | Necesaria pero mecánica o semiautomática | Registrar pagos, actualizar el CRM, publicar, responder correos de rutina |
| **Restauradora** (recarga activa) | Repone energía y atención | Movimiento, pausas activas, actividades creativas de bajo estrés, rituales de transición |

Lo creativo con poca exigencia de decisión (edición, diseño repetitivo) suele ir en la franja
operativa y creativa de la tarde, salvo que la persona diga otra cosa.

## 2. Encontrar la curva de energía (autorregistro de 7 días)

Durante una semana se registran dos variables por momento del día: el **nivel de energía** y la
**carga de la tarea**. Con eso se identifican:

- **Ventanas de flow:** foco alto y tiempo disponible. Ahí va lo analítico.
- **Valles:** baja la energía. Ahí va lo operativo o, mejor, lo restaurador.

Mientras no haya registro, se parte del patrón más común (lo analítico por la mañana; desde la
media tarde, lo operativo y creativo) **y se le pregunta a la persona**. Nunca se asume.

## 3. Parámetros del ritmo (se configuran por persona)

Cada parámetro tiene un valor por defecto del método. Se ajusta con el autorregistro y con lo
que la persona declare:

| Parámetro | Por defecto | Notas |
|---|---|---|
| Ritual AM de activación | 30–60 min antes del primer bloque | Movimiento breve, ducha, desayuno con journaling |
| Inicio del trabajo profundo | El que declare la persona | Es el ancla del día |
| Duración del bloque | 37–50 min | La persona decide en el momento. **No se dibuja en el calendario**: el bloque es el ritmo interno de la sesión |
| Pausa entre bloques | 7–10 min | Restauradora: moverse, hidratarse, sin pantalla |
| Bloques profundos por día | 3–4 | Se amplían de forma progresiva cuando el foco se sostiene |
| Franja operativa y creativa | Desde media tarde | Tareas mecánicas, repetitivas o creativas de baja exigencia |

Estos valores van en el campo opcional `ritmo:` del manifiesto (ver más abajo).

## 4. Lo innegociable va primero

Antes de ubicar una sola tarea, el calendario se ancla con lo que sostiene la energía. El
calendario funciona como **mapa de intención**: cada bloque es un compromiso de la persona
consigo misma.

| Innegociable | Qué es | Notas |
|---|---|---|
| **Ritual AM de activación** | Movimiento breve, ducha y desayuno con journaling (descarga cognitiva) | Sin celular hasta terminar. El movimiento antes del trabajo profundo deja impulso; si hace 1 minuto, cuenta |
| **Comidas** | Almuerzo como corte entre la ventana profunda y la franja de la tarde | Ahí llega el resumen de lo informativo |
| **Ritual PM de cierre** | 1) Cerrar el día. 2) Preparar mañana y **fijar la ÚNICA tarea** («si la hago, todo lo demás se vuelve más fácil o innecesario»). 3) Escribir la historia del día | Cierra los bucles abiertos que dañan el sueño; deja la mañana sin decisiones |
| **Revisión semanal (WAR)** | Procesar el Inbox, auditar los proyectos, revisar el tracker de hábitos y armar la semana | Se ubica donde la persona elija; puede ser el primer bloque profundo de la semana |
| **Sueño y entrenamiento** | Según lo que declare la persona | Nunca se recortan para meter tareas |

Los innegociables se crean como **eventos recurrentes**, solo en los días que declare la persona.
Las tareas se acomodan alrededor; nunca al revés.

## 5. Cómo el agente arma la semana en el calendario

1. **Juntar lo pendiente** de todas las fuentes de verdad (tablero de tareas, CRM, compromisos
   con clientes y reuniones confirmadas) y clasificar cada ítem por carga.
2. **Ubicar primero las reuniones confirmadas**, con su hora real.
   - **Si una reunión todavía no tiene hora,** se marca el día completo con una nota («hora por
     confirmar») y esa franja se deja liviana. Se actualiza cuando la confirmen; nunca se inventa
     una hora.
   - **Si una reunión no tiene día,** queda como tarea («confirmar día y hora»), no como evento.
3. **Poner las sesiones profundas** desde la hora de inicio, después de los innegociables: **un
   solo evento continuo por tarea**, en horas completas y uno detrás de otro, sin huecos. Los
   bloques de 37–50 min y sus pausas no se dibujan, porque fragmentan la vista de calendario: la
   persona los maneja por dentro de la sesión, y la descripción del evento lo recuerda. La primera
   sesión del día es la ÚNICA tarea que fijó el ritual PM anterior.
4. **Cada sesión profunda lleva en la descripción:**
   - ❓ **Pregunta invitadora:** una pregunta concreta y curiosa sobre esa tarea.
   - ✅ **Entregable:** qué tiene que quedar hecho al cerrar el bloque.
5. **La franja de la tarde** va con lo operativo y creativo. Las tareas cortas de registro se
   juntan al final del día.
6. **Colores por frente, no por carga.** La carga ya la dice la hora: la mañana es analítica y
   la tarde, operativa y creativa. El color responde a **para quién o para qué es**:
   - Un color por cliente o frente activo, el mismo toda la semana y en todos los eventos de ese
     frente.
   - Un color propio para lo de la persona (su producto, su contenido).
   - Las **reuniones** van en un color de alto contraste que no use ningún frente, para que
     salten a la vista.
   - Los **innegociables** van en un color neutro (gris), porque son el fondo de la semana y no
     compiten con el trabajo.
   - La revisión semanal lleva su propio color tenue.
   La leyenda se le entrega a la persona y se guarda en su perfil; si entra un frente nuevo, se le
   asigna un color libre.
7. **Verificar al final:** releer los eventos creados, confirmar que no se cruzan y que nada
   analítico cayó en un valle. Reportarle la semana a la persona por día.
8. **Proponer antes de imponer:** el plan se presenta y la persona lo ajusta. Las preferencias
   que declare (horarios, duración de bloques) se guardan en su perfil para la próxima semana.

## 6. Proteger la ventana profunda

- **Mientras corren los bloques profundos, el agente solo envía avisos que piden una acción
  inmediata**, en formato de una línea. Lo informativo (reportes de crons, resúmenes, novedades)
  se junta en **un solo resumen al cerrar la ventana**.
- **Las urgencias reales pasan siempre.** Una urgencia es algo que se pierde o se rompe si se
  espera hasta el cierre de la ventana.
- Los crons que corren en esa ventana se reprograman para después o dejan su salida para el
  resumen.

## 7. Regla de flexibilidad

Si un día la persona no tiene energía para lo analítico, ese trabajo se mueve al siguiente día
disponible y el día queda operativo o restaurador. **El agente pregunta siempre antes de mover
algo**: propone el nuevo acomodo, espera la confirmación y solo entonces cambia el calendario.

## Criterio de hecho (se suma al de A3)

- [ ] Las actividades recurrentes de la persona están clasificadas por tipo de carga.
- [ ] Innegociables (rituales AM y PM, comidas, revisión semanal) creados como eventos
      recurrentes en los días declarados.
- [ ] Los parámetros del ritmo (inicio, bloque, pausa, franjas) están declarados por la persona
      y guardados.
- [ ] Una semana completa armada en el calendario, con una sesión continua por tarea, cada
      una con su pregunta invitadora y su entregable, sin cruces ni fragmentos.
- [ ] Los avisos del agente respetan la ventana profunda durante al menos una semana, con
      evidencia en el log.

## Escalas

- **Individuo:** el ritmo es de una sola persona y ella decide todo.
- **Negocio pequeño:** el ritmo del dueño ordena el del negocio. Las reuniones con clientes y los
  horarios de atención se ubican fuera de su ventana profunda siempre que se pueda.
- **Equipo:** cada persona declara su ritmo. Se acuerda una ventana profunda común, sin
  reuniones internas, y las reuniones se agrupan en franjas compartidas.
