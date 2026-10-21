---
name: cd-flujos-trabajo
description: Use when delivering 'Flujos de trabajo y ritmo semanal' to a client.
  Skeleton, scale 1-3.
version: 0.1.0
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
3. Planear según capacidad real, no según deseo; proponer sin modificar hasta que se apruebe.
4. Programar lo repetitivo (brief diario, reporte semanal) y enviar siempre un resultado, aunque sea vacío.
5. Verificar cada cambio leyéndolo de vuelta.

## Principios

- Silencio no es completado.
- No llenar todas las horas.
- En trabajos de entrega crítica, no permitir que el agente 'se calle'.

## Plantilla / código base

```text
Revisión: calendario -> bandejas -> proyectos -> pendientes de otros -> plan -> cambios aprobados
```

## Para replicarla en otro negocio

Universal.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Ciclo captura → tarea → revisión funcionando durante 2 semanas.
- [ ] Una automatización recurrente corriendo, con ejecución comprobada en log.
- [ ] Una revisión semanal hecha una vez junto al cliente.

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
