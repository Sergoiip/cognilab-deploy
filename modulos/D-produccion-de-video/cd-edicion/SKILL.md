---
name: cd-edicion
description: Use when delivering 'Edición asistida y automatizada' to a client. Skeleton,
  scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-D
    - d2
    - ms-02
---

# D2 · Edición asistida y automatizada

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Convertir material grabado en piezas editadas con un flujo repetible que un agente pueda ejecutar.

## Cuándo usarla

Contenido recurrente (varios videos por semana, formato fijo).

## Método

1. Localizar el material por fecha de grabación, no por nombre de archivo.
2. Escoger la vía: **editor con API/MCP** (borradores editables) o **línea de comandos** (lotes de clips con subtítulos).
3. Cerrar el editor antes de escribir sobre sus archivos; trabajar sobre copia/backup.
4. Armar, **validar**, guardar; y avisar al usuario qué abrir para previsualizar.
5. Para lotes verticales con subtítulos: transcripción automática + ffmpeg en lugar de borradores manuales.

## Principios

- Nunca editar un proyecto abierto en la app.
- Validar antes de guardar.
- Documentar el límite de la herramienta (p. ej. no exporta) y cubrirlo con otra.

## Plantilla / código base

```bash
# Localizar lo grabado hoy (excluyendo la papelera en Windows)
find /UNIDAD -type f -newermt "$(date +%Y-%m-%d)" \( -iname "*.mp4" -o -iname "*.mov" \) ! -path "*RECYCLE.BIN*"
```

## Para replicarla en otro negocio

Aplica a cualquier editor (Premiere, DaVinci, CapCut). Cambia solo cómo se arma el proyecto.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Proceso documentado de crudo a entrega.
- [ ] Un video real entregado con ese proceso.
- [ ] Tiempo medido contra la línea base.

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
