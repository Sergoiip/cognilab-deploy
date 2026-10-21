---
name: cd-big-picture
description: Use when delivering 'Vista Big Picture' to a client. Skeleton, scale
  1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-B
    - b5
    - ms-14
---

# B5 · Vista Big Picture

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Ver todo el negocio como un mapa navegable: clientes, tareas y sistemas conectados.

## Cuándo usarla

Cuando una lista lineal ya no alcanza.

## Método

1. Generar el mapa desde las notas reales y sus enlaces (no a mano).
2. Un canvas por cliente y uno de operaciones; vistas que se pueden intercalar.
3. Las tareas se enlazan al padre; el lienzo de tareas muestra la dependencia y los estados.
4. Regenerar sin perder las posiciones ya movidas.

## Principios

- El mapa se genera desde los datos, no los reemplaza.
- Las tarjetas son las notas reales.

## Plantilla / código base

```text
Canvas/Mapa Big Picture · Operaciones · Cliente - X · Skills · Task Space (plugin)
```

## Para replicarla en otro negocio

Todo vault con enlaces.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Mapa navegable con clientes, tareas y sistemas reales.
- [ ] Actualización desde el registro, o procedimiento documentado.
- [ ] El cliente encuentra 3 datos sin ayuda.

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
