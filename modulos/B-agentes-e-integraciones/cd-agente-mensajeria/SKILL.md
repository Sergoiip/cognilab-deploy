---
name: cd-agente-mensajeria
description: Use when delivering 'Agente conectado a Telegram o WhatsApp Business'
  to a client. Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-B
    - b2
    - ms-17
---

# B2 · Agente conectado a Telegram o WhatsApp Business

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Un agente en WhatsApp o Telegram que califica, cotiza, cobra, agenda, captura datos y hace seguimiento, bajo las reglas del negocio.

## Cuándo usarla

Cuando el dueño cierra a mano por mensajes y se le pierden clientes o tiempo.

## Método

Ocho fases. En cada una se define qué dice el agente, qué registra y cuándo escala a una persona.
1. **Apertura:** saludar, entender qué busca, enviar presentación, clasificar el interés, capturar nombre y contacto.
2. **Cotización:** detectar el servicio y cotizar solo con la tabla del negocio; si no está, escalar.
3. **Datos:** crear ficha del cliente y oportunidad en el sistema de registro.
4. **Cobro:** generar cuenta de cobro, recibir el pago, marcar como pagado.
5. **Agenda:** proponer horarios, confirmar, crear evento y tareas.
6. **Pre-servicio:** guía y recordatorios.
7. **Post-servicio:** seguimiento, métricas, reseña, recompra.
8. **Cierre de ciclo:** revisión a los 30 días.

> Esqueleto: el manual detallado de cada fase está en la fuente original y falta generalizarlo (ver `pendiente_generalizar` en `modulo.yaml`).

## Principios

- No inventar precios: si no está en la tabla, se escala.
- No prometer resultados que no estén publicados y respaldados.
- No entregar material a quien no pagó.
- Todo se registra en el sistema del cliente.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Conectado al canal real del negocio.
- [ ] Probado con al menos 10 casos, incluidas 3 derivaciones a humano.
- [ ] Cada conversación queda registrada en el sistema del cliente.
- [ ] Regla probada: si el dato no está en la tabla, no lo inventa y escala.

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
