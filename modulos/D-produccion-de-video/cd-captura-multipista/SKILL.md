---
name: cd-captura-multipista
description: Use when delivering 'Captura multipista y respaldo' to a client. Skeleton,
  scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-D
    - d1
    - ms-01
---

# D1 · Captura multipista y respaldo

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Grabar con una fuente 'limpia' por persona y un respaldo consolidado, para poder mezclar después sin perder nada.

## Cuándo usarla

Cualquier grabación en vivo con más de una voz o fuente (podcast, entrevista, evento, clase).

## Método

1. Definir qué dispositivo captura **cada fuente por separado** (mezclador, grabadora, interfaz) y cuál captura la **mezcla de seguridad** (switcher, cámara).
2. Verificar la ruta de señal con el equipo encendido: medidores en movimiento, niveles sin saturar (el nivel línea llega mucho más fuerte a una entrada de micrófono).
3. Grabar todo a la vez; no depender de un único dispositivo.
4. En postproducción, alinear por forma de onda y mezclar desde las pistas limpias; el respaldo queda intacto.
5. Diagnosticar conectividad primero a nivel de red (misma subred, IP estática si no hay DHCP) antes de culpar al software.

## Principios

- El respaldo consolidado no se toca.
- Medir antes de comparar: normalizar a la misma sonoridad.
- Separar el problema de hardware del de software.

## Plantilla / código base

```bash
# Unir dos fuentes mono a un estéreo con canales independientes
ffmpeg -y -i VIDEO -i MIC1.wav -i MIC2.wav \
  -filter_complex "[1:a]aformat=channel_layouts=mono[a1];[2:a]aformat=channel_layouts=mono[a2];[a1][a2]join=inputs=2:channel_layout=stereo[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 320k salida.mp4
```

## Para replicarla en otro negocio

Sustituye los equipos por los tuyos. Lo que se replica es la regla: una fuente limpia por voz + un respaldo consolidado.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Set grabando multipista, con prueba de 10 minutos.
- [ ] Respaldo automático verificado.
- [ ] Checklist previo al set entregado.

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
