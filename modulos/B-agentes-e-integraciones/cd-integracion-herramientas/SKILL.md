---
name: cd-integracion-herramientas
description: Use when delivering 'Integración de herramientas con el agente' to a
  client. Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-B
    - b4
    - ms-11
---

# B4 · Integración de herramientas con el agente

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Conectar apps (editor, bóveda, nube) para que el agente actúe sin intervención manual.

## Cuándo usarla

Se quiere automatizar una tarea que hoy se hace a mano en una app.

## Método

1. Buscar si existe API/MCP oficial; si no, evaluar uno comunitario y **decir la verdad** sobre qué es y qué no es.
2. Instalar de forma reproducible (clonar, registrar, reiniciar sesión).
3. Probar con una acción mínima antes de usarlo en serio.
4. Documentar variables, rutas y trampas (cachés, bloqueos, reinicios) en la Referencia.
5. Anotar qué pasos exigen una persona (activar un plugin en la app).

## Principios

- No prometer lo que la herramienta no hace.
- Todo cambio de configuración exige reiniciar el servidor.
- Los secretos nunca se documentan.

## Plantilla / código base

```bash
# Instalar un plugin de Obsidian sin GUI
mkdir -p "<vault>/.obsidian/plugins/<id>"  # descargar main.js, manifest.json, styles.css
# añadir <id> a .obsidian/community-plugins.json y activarlo una vez en la app
```

## Para replicarla en otro negocio

Aplicable a cualquier pila de herramientas.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Cada herramienta conectada con prueba de lectura y de escritura.
- [ ] Permisos mínimos documentados.
- [ ] Cómo revocar cada acceso, entregado por escrito.

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
