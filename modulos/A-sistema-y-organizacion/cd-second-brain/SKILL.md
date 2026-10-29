---
name: cd-second-brain
description: Use when delivering 'Second Brain / sistema de registro (Obsidian)' to
  a client. Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-A
    - a2
    - ms-09
---

# A2 · Second Brain / sistema de registro (Obsidian)

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Un solo lugar donde viven clientes, ventas, sesiones, gastos y tareas, con reglas claras de dónde va cada cosa.

## Cuándo usarla

Siempre: cada hecho del negocio se anota (sesión, ingreso, gasto, lead, tarea).

## Método

1. Definir **carpetas y campos fijos por entidad** (cliente, lead, negocio, actividad, gasto).
2. Una tarea = una nota enlazada a su padre; nada de casillas sueltas que dupliquen.
3. Anotar lo dicho tal cual (pagado/entregado) y confirmar lo ambiguo.
4. Usar los valores exactos de cada lista (si no, el tablero no agrupa).
5. Revisar el estado a diario/semanal y contrastarlo con el registro en la nube.

## Principios

- Una fuente de verdad por dato.
- Una nota en la carpeta equivocada es invisible.
- Documentar el esquema (en el manual del cliente).

## Plantilla / código base

```yaml
status: open
priority: normal
scheduled: 2026-10-09
projects:
  - "[[Nota padre]]"
```

## Plugin asociado

A escala 2+ este módulo se apoya en **Lab Cadence** — ver metodología y recomendaciones de uso en
`stack/vendor/lab-cadence/METODOLOGIA.md`.

## Para replicarla en otro negocio

Cualquier negocio de servicios: cambia las entidades y la moneda.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Bóveda abierta y funcionando en el equipo del cliente, con sincronización probada.
- [ ] Entidades y campos fijos definidos y documentados (esquema).
- [ ] Mínimo 10 registros reales cargados con el cliente.
- [ ] En sesión, el cliente crea una nota y una tarea enlazada sin ayuda.

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
