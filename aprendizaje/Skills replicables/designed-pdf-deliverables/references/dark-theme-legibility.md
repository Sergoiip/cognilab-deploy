# Legibilidad en tema oscuro: medir en vez de adivinar

Para cualquier documento de fondo oscuro con glow, viñeta, scanlines o aberración cromática. El
usuario pide el efecto y la legibilidad a la vez; la única forma de cumplir ambas es medir el ratio
tras cada cambio y reportarlo.

## La medición que importa y la que miente

Una región de texto contiene dos poblaciones: el glifo y el halo. Un percentil que las confunda da un
número equivocado con total seguridad.

```python
from PIL import Image

def lum(c):
    r, g, b = c
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def region(im, x0, y0, x1, y1):
    vals = []
    for y in range(y0, min(y1, im.size[1])):
        for x in range(x0, min(x1, im.size[0])):
            vals.append(lum(im.getpixel((x, y))))
    vals.sort()
    fondo = vals[int(len(vals) * 0.20)]    # fondo: cola baja, letras excluidas
    texto = vals[int(len(vals) * 0.995)]   # núcleo del glifo: cola alta, halo excluido
    return (texto + 5) / (fondo + 5)
```

**Por qué esos percentiles.** p20 cae dentro del fondo, muy por debajo del pequeño porcentaje de
píxeles que son letra. p99.5 cae en el núcleo del glifo, por encima del bloom. Se suma 5 a cada uno
(como en la fórmula WCAG) para que un fondo casi negro no haga explotar ni colapsar la división.

**El fallo, concreto.** Una primera pasada usó p95 como “texto” y p50 como “fondo” y reportó todo
fallando — título 1,22:1, cuerpo 3,29:1, centro 1,12:1 — en un documento cuyo título medía 6,66:1. p95
en una región con bloom es el halo, no la letra. Dos señales de muestreo erróneo: el percentil “texto”
queda *por debajo* de lo que debe medir un título blanco puro, y una página con tres pesos de tinta
reporta ratios casi idénticos.

**Chequeo de cordura antes de citar un ratio.** Un título blanco puro sobre casi negro debe dar un valor
de texto cercano a 255. Si no, estás muestreando el glow.

## Objetivos

- Texto de cuerpo: 4,5:1 (WCAG AA) como piso; apuntar muy por encima (la regla de la skill pide ≥ 7:1),
  porque estos documentos se proyectan e imprimen.
- Display grande (títulos, precios): 3:1 es el piso AA, pero tratar < 4,5:1 como defecto.
- Etiquetas en versalitas y pies: las víctimas habituales, porque se estilizaron tenues a propósito.
  Medirlas explícitamente.

Reportar los números en tabla antes/después cuando cambies algo.

## Las tres causas de un documento que brilla pero no se lee

Independientes, mismo síntoma. Diagnosticar cuál está presente.

1. **Viñeta radial.** Un `radial-gradient` que oscurece los bordes come el contraste justo donde termina
   el bloque de texto. Bajar la alpha exterior y empujar la caída hacia afuera:

   ```css
   /* demasiado agresiva */
   radial-gradient(circle at 50% 50%, transparent 50%, rgba(0,0,0,.68) 100%)
   /* corregida */
   radial-gradient(circle at 50% 50%, transparent 72%, rgba(0,0,0,.34) 100%)
   ```

2. **`text-shadow` global en el cuerpo.** Un glow en `html,body` vuelve lechoso cada párrafo. Va solo en títulos.

3. **Tintas secundarias demasiado tenues.** `--ink-2` / `--ink-3` se eligen a ojo contra la muestra de
   fondo, no contra texto renderizado. Subirlas hasta que midan bien.

## Glow en capas, no un blur ancho

Un solo `text-shadow` de radio grande se lee como mancha. La halación de una pantalla de fósforo son
varios radios apilados, que mantienen el núcleo blanco nítido:

```css
h1{
  color:#ffffff;                                     /* núcleo blanco puro */
  text-shadow:
    1px 0 rgba(ACENTO_2,.55), -1px 0 rgba(ACENTO,.50), /* offset cromático, solo 1px */
    0 0 6px  rgba(190,225,255,.42),                  /* halación corta */
    0 0 16px rgba(ACENTO,.30),                       /* caída media */
    0 1px 0  rgba(ACENTO,.20),                       /* reflejo de lente */
    0 3px 10px rgba(ACENTO,.14);                     /* bloom ambiental */
}
```

El offset lateral de 1 px es toda la referencia CRT; ensancharlo convierte una aberración deliberada en glitch.

## Scanlines: finas, frías y fuera del fondo

Periodo 1 px encendido / 3 px transparente, alpha baja, tinte desaturado del acento:

```css
repeating-linear-gradient(to bottom,
  rgba(150,205,255,.075) 0px, rgba(150,205,255,.075) 1px,
  transparent 1px, transparent 4px)
```

A bajo DPI el periodo de 4 px colapsa en un lavado plano: renderizar a 110+ DPI antes de concluir que
la capa no imprimió.

## Orden de trabajo

1. Renderizar y medir cada zona de texto en la página más cargada.
2. Diagnosticar cuál de las tres causas aplica.
3. Corregir la causa en CSS, no empujando valores de color.
4. Re-renderizar, re-medir, reportar la tabla.
5. Solo entonces añadir o reforzar capas decorativas, y volver a medir — cada capa cuesta contraste.
