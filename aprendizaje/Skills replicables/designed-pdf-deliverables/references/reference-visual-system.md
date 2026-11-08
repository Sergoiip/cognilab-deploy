# Implementación de referencia: sistema visual oscuro con acento neón

Complemento de `SKILL.md` (Implementación de referencia). Un sistema que funcionó en producción, descrito genéricamente; adaptar paleta y fuentes con los placeholders de la skill.

- **Estética insignia "sobria y profesional":** fondo casi negro (`{{COLOR_FONDO}}`, no negro puro), un
  acento eléctrico (`{{COLOR_ACENTO}}`) y un segundo acento neón (`{{COLOR_ACENTO_2}}`) que se gana su
  lugar: gradiente de la regla superior, línea de claim, offset cromático del `h1` y el único elemento
  que debe vender. Sans legible para el cuerpo, monoespaciada para etiquetas en versalitas, una regla
  vertical del acento por página. Se ve como consultoría de alto nivel, no como cotización.
- **Fondos de marca oscura con acento neón:** nunca documento blanco ni páginas de color plano (ambos
  rechazados); fondo casi negro iluminado por uno o dos glows suaves de la paleta (el par cambia por
  página), paneles de vidrio, halación fílmica como emanando de un monitor CRT, glow en la luz/fondo y
  NO en los títulos, gradientes desaturados, isotipo siempre sobre oscuro. La legibilidad se gana con
  contraste y tamaño, no cambiando a una variante clara.
- **Glow moderado por defecto:** sin `text-shadow` en títulos/etiquetas, drop-shadow corto de baja alfa
  en el isotipo, sin halos en puntos/barras.
- **Un solo gradiente:** el espectro de marca (acento → … → acento 3) para isotipo y todo el cromo; no
  extenderlo con complementarios (un "gradiente editorial" terminado en dorado fue rechazado).
- **Marco CRT 9-slice:** PNG 240×240, slice 60, banda de scanlines claras + línea de bisel, centro
  transparente, en `.lam::after` con `border-image: url(x.png) 60 / 6mm / 0 stretch repeat`; la altura
  del tile central múltiplo del periodo de scanline.
- **Look 3D de época (era PS2):** renderizarlo, no dibujarlo. Escena pequeña en Blender (niebla por
  material según distancia, texturas pintadas de baja resolución con filtrado Closest, sin AA, ~448 px)
  y post en numpy (upscale bilineal, bloom aditivo solo en emisivos, dither Bayer de 5 bits, HUD).
  Sobreexposición: < ~1 % de píxeles > 245. Solo para video.
- **QR desde una captura:** decodificar con `zbarimg`, regenerar vectorial con `qrencode -t SVG`, zona
  de silencio blanca ≥ 4,5 mm (3 mm decodificó en PDF pero falló en el PNG 2×), verificar ambos.
- **Módulo único de gráficos SVG reutilizables** (hub, función, antes/después, timeline, perfil)
  importado por todos los generadores, para que todas las piezas compartan dibujos.
