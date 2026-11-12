---
name: daily-close-wrapup
description: "Use when closing the day: tasks, journal, activity."
version: 1.0.0
---

# Cierre del día

## Cuándo usarla
"cierra el día", "fin del día", o el cron diario nocturno (hora por defecto, configurable).

**Propósito:** al terminar la jornada, verificar que todo lo dictado hoy quedó registrado en el
CRM de la bóveda, cerrar/reagendar tareas con evidencia, escribir el Journal, preparar la nota de
mañana y dar un reporte corto. Contraparte: `daily-startup-today-plan`.

## 1. Alcance
Hoy = fecha local. **Nunca borrar nada.** Solo marcar `status: done` en tareas confirmadas por
el usuario, o reagendar abiertas a mañana.

## 2. Verificar registros del día
- **Ingresos/egresos dictados hoy:** revisar el historial de chat de hoy buscando "ingreso",
  "pago", "gasto", "anota". Por cada uno, confirmar que existe el registro correspondiente en el
  CRM de la bóveda; si no, crearlo con el procedimiento de CRM de la bóveda (nunca inventando el
  formato: copiar el frontmatter de un registro existente del mismo tipo).
- **Reuniones/sesiones de hoy:** revisar actividades tipo reunión con fecha de hoy; si ninguna
  tiene esa fecha, NO asumir "sin actividad": preguntar explícitamente.
- **Gastos registrados hoy:** confirmar monto, categoría, método de pago; señalar huecos.

## 3. Tareas: cerrar o reagendar
- **Hechas hoy:** preguntar una vez en el reporte final, no una por una. Con confirmación:
  `status: done`, `completedDate: hoy`.
- **Abiertas agendadas hoy:** NO subir a mañana lo repetible (eso es un cron). Reagendar
  escaneando TODAS las notas-tarea abiertas con `scheduled` = hoy, no solo los wikilinks de la
  nota diaria.
- **Vencido:** tareas con `scheduled` < hoy y abiertas → arrastre de mañana. Señalar lo vencido
  hace más de 7 días.

## 4. Reconstruir el día desde el historial del agente (opcional, para cerrar huecos de registro)
Para reconstruir con precisión qué pasó en el día cruzando todos los canales (chat móvil,
escritorio, crons) en vez de depender solo del historial visible en el chat actual, consultar en
modo solo lectura la base de estado del agente (`state.db` en el directorio del perfil activo de
Hermes, $HERMES_HOME):

```python
import sqlite3, datetime, os
db = os.path.join(os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes')), 'state.db')
c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
tz = datetime.datetime.now().astimezone().tzinfo  # zona horaria local del equipo
hoy = datetime.date.today()
s = datetime.datetime(hoy.year, hoy.month, hoy.day, 0, 0, tzinfo=tz).timestamp()
e = s + 86400
rows = c.execute("""
    select m.timestamp, s.source, m.role, m.content
    from messages m join sessions s on s.id = m.session_id
    where m.timestamp >= ? and m.timestamp < ?
      and m.role in ('user','assistant') and m.content is not null
    order by m.timestamp
""", (s, e)).fetchall()
```
Fuentes típicas: `telegram`, `desktop`, `cron`. Ignorar mensajes vacíos/de sistema (prefijos
`[IMPORTANT:`, `[Cron delivery:`) y deduplicar. Útil cuando el historial de la sesión actual
está incompleto o se perdió contexto.

## 5. Journal
Escribir/anexar `## Journal` con fecha/hora del cierre y una viñeta por categoría (sesiones,
ingresos, egresos, tareas cerradas/movidas, seguimientos, pendientes de cobro, decisiones).
Menos de 15 líneas, sin repetir `## Today`, omitiendo categorías vacías.

## 6. Nota de mañana
Crear `daily/<mañana>.md` si no existe, con las secciones 1 (tareas de hoy aún abiertas) y 2 (ya
vencidas), mismo estilo que la nota del día actual.

## 7. Reporte final (<20 líneas, sin rutas)
Sesiones · ingresos del día · egresos · tareas cerradas · movidas a mañana (las importantes) ·
seguimientos pendientes · cobros próximos/vencidos · avisos (sesiones sin estado, tareas
vencidas, dictados sin registrar).

## Verificación
- Cada ingreso/egreso dictado tiene su registro con fecha de hoy.
- Ninguna tarea cerrada sin confirmación o evidencia.
- Todos los wikilinks de la nota de mañana resuelven.

## Variantes
- Sin sesiones/reuniones presenciales: omitir el punto 2 de reuniones y centrarse en
  entregas/cobros.

## Skills relacionadas
`daily-startup-today-plan` — contraparte de inicio de día.
