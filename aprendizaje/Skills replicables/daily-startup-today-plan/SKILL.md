---
name: daily-startup-today-plan
description: Use when starting the workday to plan today.
version: 1.0.0
---

# Inicio de día: orden del día

## Cuándo usarla
"empezar", "orden del día", "qué hay hoy", o el cron de la mañana (hora por defecto,
configurable).

**Propósito:** al empezar la jornada, recolectar en solo lectura todo lo que afecta al día
(continuidad, tareas, agenda, correo, dinero/seguimientos en el CRM de la bóveda) y escribir en
la nota diaria un plan ordenado en tres bloques, con una respuesta corta. Contraparte:
`daily-close-wrapup`.

## Reglas generales
- Hoy = fecha local de la zona horaria del usuario. Nunca tocar `## Journal`. Nunca sobrescribir
  una nota diaria existente: leerla primero. Solo lectura en todo salvo la nota diaria y lo
  aprobado.
- Enviar correo/mensajes, crear/borrar eventos, marcar tareas hechas: solo con aprobación
  explícita del texto/acción exacta.
- Ingreso/egreso dictado en el mismo chat: registrarlo con el procedimiento de CRM de la bóveda,
  sin preguntar por huecos de bajo riesgo.
- Si una fuente falla, seguir con el resto y listarla en Avisos; nunca inventar datos.

## Fase 1 · Recolectar (solo lectura, en este orden)
1. **Continuidad:** nota diaria anterior y su Journal/cierre.
2. **Tareas:** carpeta de notas-tarea del gestor de tareas de la bóveda. Abierta = status no
   done/cancelled; omitir ideas sin fecha. Tomar `scheduled`/`due` <= hoy. Releer archivos (las
   tareas se cierran entre sesiones); no usar grep de `- [ ]` suelto.
3. **Agenda:** calendario de hoy (y mañana para preparar), ISO 8601 con offset. Marcar solapes;
   no tratar tentativo como confirmado.
4. **Correo:** no leídos/últimas 24 h, triaje: responder urgente / responder / acción /
   esperando / ruido. Solo lectura; solo borradores.
5. **Dinero (CRM de la bóveda):** deals ganados con pago pendiente: "cobro vencido" si la fecha
   pasó, "cobro próximo" si <= hoy+3. Entregables adeudados. Gastos recurrentes que vencen.
6. **Seguimientos:** notas-tarea tipo "seguimiento día N" con scheduled <= hoy; contactos/deals
   estancados (30+ días sin edición).
7. (Opcional, si aplica) **Bandejas de mensajería/redes:** solo lectura, reportar conteos;
   responder es trabajo repetible de cron, no entra como tarea diaria.

## Fase 2 · Escribir `daily/YYYY-MM-DD.md`
Crear si falta (conservar `## Today` y `## Journal`, Journal vacío). Si existe, editar solo
`## Today` con tres bloques:
1. Lo que tocaba el día laboral anterior.
2. Arrastrado de antes (vencido más antiguo primero: dinero/entregas, luego seguimientos, luego
   dependencias).
3. Hoy (agendado hoy, incluyendo eventos de calendario como línea no-tarea).

Formato de línea: `- [ ] [[<nombre exacto del archivo>]] · Responsable · ~H h · nota` (ej.
"vencida desde dd-mm"). Verificar que cada wikilink resuelve. **Regla:** lo repetible
(recordatorios, hábitos, seguimientos automáticos) es un CRON, no una línea en la nota diaria.

## Fase 3 · Respuesta (corta, sin rutas de la bóveda)
Orden: 1) agenda de hoy; 2) lo urgente (cobros vencidos, entregas, correos); 3) conteo por
bloque; 4) dinero; 5) seguimientos pendientes; 6) lo dejado fuera y por qué; 7) avisos (fuentes
no revisadas, ítems viejos a confirmar). Menos de ~20 líneas.

## Pitfalls
- Token OAuth vencido: no reintentar en bucle; caer a la nota diaria previa y listar
  calendario/correo en Avisos.
- Bloque 1 = ítems del bloque 3 de ayer aún abiertos.
- Tareas con `due` pero sin `scheduled` escapan del pre-movimiento automático: contrastar
  manualmente.

## Variantes
- Sin calendario/correo conectados: omitir esos pasos y declararlo.
- Equipo de una sola persona: fusionar responsable y aprobador.

## Skills relacionadas
`daily-close-wrapup` — contraparte de cierre de día.
