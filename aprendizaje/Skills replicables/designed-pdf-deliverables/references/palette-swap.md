# Cambiar la paleta de un documento sin romperlo

Para una revisión en la que el usuario conserva la composición y cambia los colores. El riesgo es
silencioso: un hex sobrante de la paleta vieja sigue renderizando, y un acento declarado puede ser
invisible contra el fondo.

## Procedimiento

1. **Mapear la paleta vieja antes de tocar nada.** Listar cada literal de color y cada token derivado.
   Un sistema con variables CSS tiene pocos literales más tintes `rgba()` de los mismos tonos — los
   tintes son los que se escapan:

   ```python
   cols = sorted(set(re.findall(r"#[0-9a-fA-F]{6}", t)))
   for m in re.finditer(r"rgba\([\d,\s.]+\)", t): ...   # los residuos silenciosos
   ```

2. **Reemplazar las variables y luego los literales.** Cambiar solo `:root` deja colores fijos en
   títulos, glows y sombras. Dos pasadas: el bloque de variables, luego un escaneo por cada hex viejo
   y cada tinte `rgba()` viejo.

3. **Probar que el cambio es total.** Volver a buscar los valores viejos tras editar. Cero
   coincidencias es el resultado a reportar:

   ```python
   print("residuos:", len(re.findall(r"{{HEX_VIEJO_1}}|{{HEX_VIEJO_2}}|R,G,B", t)))   # esperar 0
   ```

4. **Confirmar que cada acento es perceptible.** Declarado ≠ visto. En fondo casi negro un acento de
   luminancia media desaparece. Dos chequeos independientes:

   - **Muestreo de píxeles** — renderizar a PNG y contar píxeles dentro del rango RGB del acento:

     ```python
     from PIL import Image
     from collections import Counter
     im = Image.open('page.png').convert('RGB')
     c = Counter()
     for y in range(0, im.size[1], 4):
         for x in range(0, im.size[0], 4):
             r, g, b = im.getpixel((x, y))
             if r > 120 and b > 90 and g < 90:      # ejemplo: rango magenta/rosa; ajustar al acento
                 c[(r//40*40, g//40*40, b//40*40)] += 1
     print("pixeles del acento:", sum(c.values()))
     ```

   - **Pasada de visión con verbo obligatorio** — preguntar si el acento se ve y *dónde*. Una
     respuesta con titubeo (“un leve tinte lila, más matiz que acento”) es un fallo: re-renderizar
     más fuerte antes de entregar.

5. **Gastar el acento donde trabaja.** Cuatro ubicaciones cargan una paleta de marca: la regla
   superior (gradiente de acento a segundo acento), la línea de claim, el offset cromático del `h1` y
   el único elemento que debe vender. Reforzar el acento solo en el bloque de variables produce un
   documento donde el usuario no encuentra su color.

   ```css
   .rule{ background:linear-gradient(90deg, var(--accent-2) 0%, var(--accent) 62%, transparent 100%);
          box-shadow:0 0 10px rgba(R,G,B,.45); }
   ```

6. **Dar al elemento que debe vender un marco que los otros no tienen.** En una lista de precios,
   marcar el nivel recomendado con borde del acento más glow interior; los demás neutros. El revisor
   debe identificar el plan de entrada sin leer una palabra.

## Nunca

- Re-proponer la estética cuando el usuario la aprobó y está corrigiendo un color.
- Repartir el segundo acento por todas partes “para equilibrar”; dos acentos con el mismo peso compiten.
- Reportar la paleta como aplicada hasta que los hex viejos no estén en la fuente *y* el acento nuevo sea perceptible en el render.
