---
name: cd-flujos-trabajo
description: Use when delivering 'Flujos de trabajo y ritmo semanal' to a client.
  Skeleton, scale 1-3.
version: 0.2.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-A
    - a3
    - ms-12
---

# A3 · Flujos de trabajo y ritmo semanal

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Un ciclo fijo de revisión y tareas programadas para que nada dependa de acordarse.

## Cuándo usarla

Cierre de semana, y todo lo que se repite igual cada día o semana.

## Método

1. Declarar la fuente de verdad y el periodo; revisar calendario, bandejas y proyectos.
2. Convertir cada pendiente en acción, espera o archivo; marcar proyectos sin siguiente paso.
3. Planear según capacidad real, no según deseo: clasificar cada pendiente por carga (analítica, operativa, restauradora) y ubicarlo según la curva de energía de la persona, con bloques profundos que llevan pregunta invitadora y entregable. Proponer sin modificar hasta que se apruebe. Protocolo completo: `bootstrap/ORGANIZACION-TEMPORAL.md`.
4. Programar lo repetitivo (brief diario, reporte semanal) y enviar siempre un resultado, aunque sea vacío.
5. Verificar cada cambio leyéndolo de vuelta.

## Principios

- Silencio no es completado.
- No llenar todas las horas.
- Se planea con la energía, no con el tiempo libre: lo analítico va en las ventanas de flow y lo operativo y creativo en los valles.
- Durante la ventana profunda el agente solo avisa lo que pide una acción; lo informativo se junta en un resumen al cerrarla.
- Antes de mover trabajo por falta de energía, preguntar siempre.
- Una reunión sin hora confirmada se marca en el día con una nota; nunca se inventa la hora.
- En trabajos de entrega crítica, no permitir que el agente 'se calle'.

## Plantilla / código base

```text
Revisión: calendario -> bandejas -> proyectos -> pendientes de otros -> plan -> cambios aprobados
```

## Plugin asociado

Este módulo se apoya en **Task Atlas** para visualizar el ritmo de tareas — ver metodología y
recomendaciones de uso en `stack/vendor/task-atlas/METODOLOGIA.md`.

## Para replicarla en otro negocio

Universal.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Ciclo captura → tarea → revisión funcionando durante 2 semanas.
- [ ] Una automatización recurrente corriendo, con ejecución comprobada en log.
- [ ] Una revisión semanal hecha una vez junto al cliente.
- [ ] Organización temporal configurada: carga clasificada, ritmo declarado, una semana armada en calendario y ventana profunda respetada (ver `bootstrap/ORGANIZACION-TEMPORAL.md`).

**Comunes a todo módulo:**

- [ ] Verificado: se probó en real antes de entregar, con evidencia (captura, log o archivo).
- [ ] Faltante declarado: lista escrita de lo que no quedó hecho y de las limitaciones.
- [ ] Documentado: una página de uso con los nombres, rutas y tono del cliente.
- [ ] Aceptado: el cliente confirma por escrito (mensaje o acta). Esa aceptación dispara el hito.
- [ ] Sin datos ajenos: nada de otro cliente ni de Sergio en lo entregado.

## Escalas

- `variantes/1-individuo.md`
- `variantes/2-negocio.md`
- `variantes/3-equipo.md`
