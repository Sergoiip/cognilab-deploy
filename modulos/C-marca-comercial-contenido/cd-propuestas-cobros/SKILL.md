---
name: cd-propuestas-cobros
description: Use when delivering 'Propuestas, cotizaciones y cobros' to a client.
  Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c2
    - ms-05
---

# C2 · Propuestas, cotizaciones y cobros

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Cada oferta y cobro sale con la cara de la marca, queda registrada y genera sus seguimientos.

## Cuándo usarla

Cuando se cotiza, se cierra una venta o se cobra.

## Método

1. Documento **corto y visual**, centrado en el resultado que el cliente quiere (no en un marco teórico).
2. Registrar la cotización como **lead** (con el PDF enlazado) en el CRM; pasar a negocio solo cuando se acepta.
3. Crear los seguimientos como tareas, no como texto en la nota.
4. Numerar consecutivamente los cobros y guardar la plantilla.
5. Verificar visualmente, versionar las ediciones (`_v2`, `_v3`) y revisar que cada cifra cambiada se actualizó en todo el documento.

## Principios

- Una oferta no lleva estadísticas de mercado ni la estrategia completa.
- Todo precio no confirmado queda como pendiente visible.
- Los datos de pago nunca se copian a documentación general.

## Plantilla / código base

```text
Lead  ->  Cotización (PDF)  ->  Negocio (Pipeline)  ->  Cobro  ->  Seguimiento (tareas)
```

## Para replicarla en otro negocio

Cambia los precios y la plantilla legal. El ciclo lead → cobro → seguimiento es universal.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Plantillas de propuesta, cotización y cuenta de cobro, con numeración.
- [ ] Un documento real emitido de punta a punta.
- [ ] Seguimiento programado.

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
