---
name: cd-instagram
description: Use when delivering 'Flujo de Instagram' to a client. Skeleton, scale
  1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c5
    - ms-16
---

# C5 · Flujo de Instagram

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Que el contenido de una cuenta salga de un sistema vivo en Obsidian, no de ideas sueltas: banco de ideas → estrategia → parrilla → texto aprobado → render → publicación → medición.

## Método

1. **Banco de ideas**: una nota por idea (pilar, formato, fuente, estado) enlazada a pilares y marca. El grafo y los enlaces entrantes muestran huecos. Fuentes: sesiones reales, preguntas de la audiencia, metodología propia, clientes con permiso, datos, reciclaje.
2. **Estrategia mensual**: objetivo, reparto por pilar, reglas, pendientes.
3. **Parrilla mensual**: pieza por pieza con idea del banco, día, producción y estado. Aprobada el día 8 del mes anterior.
4. **Texto antes que diseño**: el dueño aprueba el texto; después se renderiza.
5. **Registro y medición**: códigos C/R/S; guardados y alcance se anotan a mano.
6. **Publica una persona del equipo; el agente nunca publica.**

## Para replicarla

Cambia pilares, reglas de marca y canal. Plugins sugeridos para generar ideas: Smart Connections, InfraNodus, Templater, Dataview.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Banco de al menos 30 ideas.
- [ ] Parrilla de 4 semanas.
- [ ] Cuatro piezas producidas y medición base.

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
