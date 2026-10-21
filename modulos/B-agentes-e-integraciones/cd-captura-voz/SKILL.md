---
name: cd-captura-voz
description: Use when delivering 'Captura por voz' to a client. Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-B
    - b3
    - ms-03
---

# B3 · Captura por voz

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Convertir notas de voz del dueño del negocio en registros estructurados sin teclear.

## Cuándo usarla

El usuario dicta pedidos (sesiones, gastos, tareas, ideas) por mensajería.

## Método

1. Transcribir localmente el audio (privacidad y costo).
2. Interpretar la intención y **confirmar lo ambiguo** antes de registrar.
3. Registrar en el sistema de registro (ver MS-09) y devolver un resumen corto.
4. Si el adjunto no baja, buscar el archivo en la carpeta de descargas de la app de mensajería.

## Principios

- Transcripción local = datos del cliente no salen del equipo.
- Lo dictado se vuelve registro; lo dudoso se pregunta.

## Plantilla / código base

```bash
# Transcribir con faster-whisper (modelo grande, GPU si hay, CPU si no)
python transcribe.py "audio.ogg" --lang es
```

## Para replicarla en otro negocio

Cualquier negocio con un dueño que dicta: cambia el destino del registro.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Transcripción local funcionando.
- [ ] Al menos 5 notas de voz convertidas en registros estructurados.
- [ ] Errores revisados con el cliente y glosario propio dejado.

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
