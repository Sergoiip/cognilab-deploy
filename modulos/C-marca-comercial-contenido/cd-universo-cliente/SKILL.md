---
name: cd-universo-cliente
description: Use when delivering 'Universo de cliente y guiones' to a client. Skeleton,
  scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c4
    - ms-08
---

# C4 · Universo de cliente y guiones

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Cada cliente recurrente tiene su 'universo' de notas para que el trabajo salga en su voz.

## Cuándo usarla

Se incorpora un cliente mensual o se necesita planear su contenido.

## Método

1. Crear la nota hub del cliente y las notas: contexto/branding, estrategia, parrilla, pendientes, bitácora y guiones.
2. Leer el hub y las notas de contexto **antes** de escribir.
3. Llenar solo con material entregado; lo faltante queda marcado y listado como pendiente.
4. Etapas: contexto → diagnóstico → estrategia → plan mensual → parrilla → guiones → aprobación → envío (solo con visto bueno).
5. Escribir solo las piezas pedidas; el resto queda como ideas en la parrilla.
6. Marcar `[x]` una etapa únicamente cuando la nota enlazada tenga contenido real.

## Principios

- No inventar técnicas, credenciales, precios ni tiempos del cliente.
- Sectores sensibles (salud): consentimiento, sin promesas de resultado.
- Una corrección de tipo de cliente toca **todos** los registros que lo mencionan.

## Plantilla / código base

```text
Clientes/<Cliente>/
  <Cliente>.md   (hub)
  00 Fuente · 01 Contexto · 02 Estrategia · 03 Parrilla · 04 Pendientes · 05 Bitácora
  Guiones/  (_Plantilla de guion.md)
```

## Para replicarla en otro negocio

Sirve a cualquier agencia o consultoría con clientes recurrentes.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Documento de voz y estilo construido con al menos 10 muestras reales.
- [ ] Tres piezas generadas que el cliente reconoce como suyas.

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
