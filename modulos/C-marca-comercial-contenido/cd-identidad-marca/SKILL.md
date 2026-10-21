---
name: cd-identidad-marca
description: Use when delivering 'Identidad de marca y kit de assets' to a client.
  Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c1
    - ms-04
---

# C1 · Identidad de marca y kit de assets

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Destilar una marca real y producir un kit coherente de piezas (manual, presentaciones, guías, redes).

## Cuándo usarla

Marca nueva, cliente nuevo o rediseño.

## Método

1. Pedir primero 1-2 piezas propias que el cliente considere su mejor estilo: el feed es una fuente de diseño.
2. Reunir fuentes (sitio, redes, logo) y **medir el color en píxeles** del logo; marcar qué es medido y qué es inferido.
3. Escribir la identidad (insight, valores, voz con ejemplos reales, paleta, tipografía, públicos, objetivos) **sin inventar datos**; lo que falta va a una lista de pendientes.
4. Construir con una hoja de estilo compartida y un archivo por documento; variar las imágenes por pieza.
5. Documentar cada activo en el sistema de registro con su fuente editable.

## Principios

- No repetir una misma foto (menos aún de personas) como portada de muchas piezas.
- Entregar siempre con lo que NO se inventó.
- Fuente editable junto a cada salida.

## Plantilla / código base

```python
# Color de marca real: píxel opaco más común del logo
from PIL import Image
from collections import Counter
im=Image.open('logo.png').convert('RGBA')
print(Counter(p[:3] for p in im.getdata() if p[3]>250).most_common(3))
```

## Para replicarla en otro negocio

Sirve a cualquier marca. Se adapta la paleta, voz y tipo de piezas.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] El cliente aprobó la dirección antes de producir variantes.
- [ ] Manual de marca: logo, paleta, tipografía y usos incorrectos.
- [ ] Kit en los formatos y tamaños que usa (perfil, portada, catálogo).
- [ ] Legible a tamaño de foto de perfil.
- [ ] Sin marcas de terceros ni afirmaciones que el cliente no pueda sustentar.

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
