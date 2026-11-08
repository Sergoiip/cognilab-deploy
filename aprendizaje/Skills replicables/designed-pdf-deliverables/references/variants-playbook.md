# Variantes: flujos de trabajo detallados

Complemento de `SKILL.md` (sección Variantes). Cada variante reutiliza los Pasos y la Verificación de la skill; aquí solo lo que cambia.

## Mini-deck 16:9 (informes de incidente, status, roadmaps internos)
`@page{size:338.67mm 190.5mm;margin:0}`, una `<section class="slide z">` por slide con variable `--z`
de zoom por slide, portada oscura alternando con contenido, una idea por slide. Renderizar a zoom 1 y
luego ajustar (~1,0 portada, ~1,2–1,35 slides escasos, ~1,1 con diagrama + dos tarjetas).

## Maestro + N one-pagers desde un dato
Agrupar por categoría/nivel (un conteo impar deja una página huérfana) y dar a la variante una clase
en `<body>` para agrandar precios/títulos. Verificar cada PDF por separado.

## Plan/roadmap para cliente
`lib.py` (fuentes, color, contraste), `figs.py` (SVG), `build.py` (páginas) → un HTML de secciones A4
fijas → `render.mjs` (Playwright) que imprime y reporta por página espacio sobrante, solapes, scroll y
texto SVG fuera de caja. Incluir decisiones pendientes y una página "primeros 7 días". Buscar primero
los briefs del cliente en disco (descargas incluidas).

## "Para compartir en línea"
Set: PDF + HTML autocontenido (fuentes inline, cero `file://`) + PNG de portada ~150 dpi + tarjeta
social 1200×630 (deviceScaleFactor 2) con kicker, claim y logo.

## Derivar la propuesta de un segundo cliente de una ya aprobada
- Fork, no reconstrucción: copiar el HTML aprobado, cambiar solo lo que identifica al cliente (nombre,
  fecha, lo específico), nuevo nombre de archivo. "Una versión de X" = el mismo tipo de artefacto que X.
- **Escribir la copia a disco antes de verificar**; verificar leyendo el archivo/PDF, no el string en memoria.
- Preguntar en una sola tanda: ¿misma oferta y precios?, ¿ciudad sí/no?, ¿aplica tal sección?
- Una persona no es cliente hasta que algo ha pasado: preguntar antes de crear entidades CRM.
- Un empleador institucional puede implicar restricciones (datos que salen del equipo, quién
  autoriza): son preguntas para el usuario, no hechos. Si se pide mencionarlo, redactarlo como
  capacidad del vendedor, condicional, con terminología consistente.
- No dejar las tarjetas de casos del cliente anterior sin avisar: señalarlo como decisión del usuario.

## Aplicar una estética aprobada o rehacer un documento ilegible
Trabajar sobre el HTML fuente, escribir a un nombre distinto y dejar el original para comparar. Para
uno ilegible, generador pequeño nuevo en vez de parchear la escala vieja; miniaturas reutilizadas por
captura de elemento a deviceScaleFactor 4 con `aspect-ratio` + `object-fit:cover`.

## Igualar un documento de referencia sin fuente
Si solo existe el PDF renderizado, no sustituir con una plantilla propia "con los mismos colores".
Renderizar 3–4 páginas representativas (portada, página densa, tabla/timeline, última) y pedir a
visión los tokens concretos: columnas, aspecto de página, tratamiento de logo/encabezado, dónde va la
barra de gradiente, estilo de tarjetas, patrón de pie. Listar **todas** las páginas del original antes
de rediseñar (anexos, factura, firma).

## Revisar un documento multipágina desde notas por página
1. Localizar la fuente, no solo el PDF (varios PDFs homónimos: elegir por mtime, luego
   `grep -rl <nombre-html> --include=*.py --include=*.sh` para hallar el generador). Editar el generador.
2. Respaldar generador + HTML + PDF en `respaldos/<versión>-<fecha>/`.
3. Renderizar y describir con visión cada página actual para mapear cada nota a un elemento.
4. Aplicar solo el lote pedido; correr el build propio del proyecto y corregir todo desborde que reporte.
5. Revisar con visión cada página cambiada con preguntas concretas; recorte a ~170 dpi si es ambiguo.
   Los veredictos de visión (sobre todo en hojas de contacto) son pistas, no hechos: re-renderizar a
   40–60 dpi y preguntar algo factual (% lleno, dónde está el vacío).
6. Cerrar con: qué cambió por página, qué es propuesta y defectos menores pendientes.

Detalle (sistema de manuales, overlays CRT, figuras como mini-monitores, índice clicable,
legibilidad de diagramas, reglas de copy): `brand-manual-revision-lessons.md`.

## Iterar el sistema de marca completo (manual + hoja + piezas derivadas)
- Orden: hoja de marca → nota canónica del isotipo → manual. Texto aprobado antes de renderizar.
- Un pedido grande de rediseño ("aplica X a todo") requiere un documento de dirección de arte aprobado
  antes de reconstruir; insertar módulos en un layout existente produce páginas "parchadas".
- La taxonomía visual se aplica diseñando desde el mensaje (qué debe entender el lector → operación →
  técnica de firma → gráfico), no etiquetando páginas ni convirtiendo técnicas en reglas tipográficas.
- "Retoma / itera la versión X" = usar el SISTEMA de X para reconstruir todo de forma coherente desde
  UN generador. Ni copiar X y parchar, ni inventar un look nuevo (ambos rechazados).
- Pedir referencia visual después de la PRIMERA ronda rechazada de un look descrito con metáforas;
  medir la imagen (grano, luma, correlación de color) antes de replicarla.
- Las figuras llenan su marco: renders/fotos `object-fit:cover`; diagramas generados recortados a su
  contenido y mezclados con `mix-blend-mode:screen`, al aspecto del marco; mapas con fondo propio con su
  `aspect-ratio`; filas de mockups llenan la altura; páginas fotográficas a sangre con panel de vidrio.
- Expandir una página del manual en varias: módulo propio con clases prefijadas, mockups de usos reales
  en HTML/CSS con placeholders genéricos para marcas de terceros, auditar desbordes antes de PNG,
  publicar solo después de una pasada de visión limpia.
- Mover/renombrar carpetas de marca o cambiar el contacto: grep de rutas y valores viejos, regenerar
  todo y comparar páginas, tamaño y `pdftotext` de la línea de contacto.

## Reconstruir material comercial para público general
1. Buscar por nombre de archivo (`*catalog*`, `*brochure*`, `one-pager*`) en los repositorios del
   usuario y localizar generador + archivo de datos; no confiar en rutas recordadas.
2. Reescribir para un desconocido conservando precios y alcance del archivo de datos: quitar notas de
   venta internas, reemplazar nombres de clientes por perfiles, categorías internas por áreas que
   entiende el lector; añadir camino de entrada ("si no sabes cuál, empieza por el 01") y condiciones de pago.
3. Aplicar el sistema de marca actual referenciando activos por ruta, no copiando CSS viejo.
4. Entregar PDF + PNG por página + una tira vertical para mensajería; archivar lo viejo en
   `_archivo-…/` en vez de borrar; barrer el texto extraído por nombres filtrados y palabras internas.
5. Señalar en la respuesta lo que no se pudo decidir (contacto, handles, piezas obsoletas).

Patrones del set de piezas, fuentes de verdad de la oferta y loop de build/auditoría:
`sales-collateral-patterns.md`.
