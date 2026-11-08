# Render y puertas de verificación (detalle)

Complemento de `SKILL.md`: snippets de auditoría, pipeline de fuentes y pitfalls de CSS,
render y generadores. La regla general vive en `SKILL.md`; aquí está el *cómo medir*.

## 1. CSS base de página

```css
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4;margin:0}
.page{width:210mm;height:297mm;padding:18mm 20mm 16mm;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
```

- **One-pager / tarjetas / propuesta**: `height:297mm` fijo + `overflow:hidden`. Con `min-height`
  el contenido se derrama y Chromium añade una página fantasma.
- **Documento que fluye** (manual, informe, conversión desde Markdown): `min-height:297mm`, dejar
  que fluya y usar `page-break-before:always` solo entre secciones MAYORES. En este modo el chequeo
  de desborde debe medirse contra la altura de la hoja (sección 3), no contra el elemento.

## 2. Pipeline de fuentes (que lo que se ve sea lo que se embebe)

1. **Una cara estática por peso**, nunca el archivo variable: el navegador carga todos los pesos
   pero el exportador PDF solo embebe la instancia por defecto (`pdffonts` muestra `Type 3`).
   Generar instancias con fontTools:
   `instantiateVariableFont(font, {"wght": 600}, updateFontNames=True)` — sin `updateFontNames`
   `pdffonts` muestra los nombres viejos. Un solo `.ttf` Black para todos los pesos pone todo en negrita.
2. **Embeber como data URI**: `file://` en `@font-face` puede reportarse cargado y aun así no llegar
   al PDF; una ruta relativa equivocada cae en silencio a una serif del sistema.
   ```bash
   python3 scripts/inline_fonts.py in.html out.html --base {{RUTA_TIPOGRAFIAS}} --drop FamiliaSinUso1 FamiliaSinUso2
   ```
   `--base` es la carpeta contra la que se resuelven los `url()` relativos; `--drop` elimina las
   reglas `@font-face` de familias que el documento no usa (adelgaza el HTML).
3. **Comprobar en el DOM** que cargaron: `document.fonts.forEach(f => f.status==='loaded' && ...)`
   debe dar una entrada por peso declarado; una familia que colapsa a un peso = ruta equivocada.
4. **Cobertura de glifos** (✓ ✕ ≥ α) contra el cmap de la fuente (fontTools `getBestCmap`); si falta
   un glifo, escribirlo con palabras o dibujarlo en SVG.
5. **Comprobar en el PDF**: `pdffonts OUT.pdf` → un subset por peso, CID TrueType, ningún `Type 3`.
6. Sin fuentes embebidas, `--virtual-time-budget` corto imprime el fallback (las webfonts por red
   no llegan a tiempo): 10–15 s, y mantener siempre una pila de fallback de sistema robusta.

## 3. Auditoría DOM antes de imprimir (Playwright/CDP o `--dump-dom`)

Salir con código distinto de 0 si algo falla; el render solo corre con auditoría limpia.

- **Desborde por página**: `scrollHeight - clientHeight > 0` en `.page`/`.cuerpo` (> 4 px para
  localizar bloques comprimidos por flex).
- **Desborde contra la HOJA** (obligatorio con `min-height`, donde el elemento se compara consigo
  mismo y el chequeo nunca dispara). 297 mm ≈ 1122,5 px a 96 dpi:
  ```javascript
  const CAJA = 1122.5; let alto = 0;
  el.querySelectorAll('*').forEach(n => { const r = n.getBoundingClientRect();
    if (r.height > 0) alto = Math.max(alto, r.bottom - el.getBoundingClientRect().top); });
  if (alto > CAJA + 3) out.push(`${i+1}:+${Math.round(alto-CAJA)}px`);
  ```
- **Solapamiento de hermanos**: `prev.bottom > next.top`. "Sin overflow" no es "sin solape": flex
  encoge bloques en vez de scrollear. Filtrar capas decorativas `inset:0` (cuentan como solapes
  fantasma) limitando la búsqueda al contenedor de contenido.
- **Tamaño mínimo calculado** en pt (HTML y texto SVG): nada < 9,5 pt en etiquetas, nada < 9 pt.
- **Espacio libre bajo el último bloque** y suma de spacers sin texto: > 20–25 mm (o > 25–30 % de
  la altura) = añadir contenido real. "Desborde" y "margen inferior" son signos opuestos de la misma resta.
- **Texto SVG fuera de su caja**.
- **Conteo de páginas** en el HTML con `class="page[ \"]` (tolera `class="page cover"`).

## 4. Auditorías sobre el PDF final (scripts incluidos)

```bash
python3 scripts/pdf_font_audit.py OUT.pdf [otros.pdf ...]           # puerta: mediana >= 11 pt, nada < 9 pt
python3 scripts/pdf_font_audit.py *.pdf --no-gate                    # solo informe (dimensionar un rehacer)
python3 scripts/pdf_font_audit.py OUT.pdf --min-median 11.5 --min-size 9.5   # puerta más estricta
python3 scripts/check_pdf_text.py OUT.pdf                            # caracteres por página, huérfanas, scripts extraños
python3 scripts/check_pdf_text.py OUT.pdf --orphan-chars 150 --hints-file pistas.txt
python3 scripts/check_spanish_text.py borrador.txt                   # prosa que se entrega fuera del PDF
cat respuesta.txt | python3 scripts/check_spanish_text.py - --words-file extranjeras.txt --markers-file marcadores.txt --extend
pdffonts OUT.pdf                                                     # un subset por peso, CID TrueType, no Type 3
pdftoppm -r 110 -png OUT.pdf {{RUTA_SCRATCH}}/pg                     # páginas para revisión visual
```

- `pdf_font_audit.py` usa `pdftohtml` (poppler); sale con código 1 si falla la puerta (salvo
  `--no-gate`). Correrlo sobre **todos** los PDF existentes antes de prometer un rehacer. El texto
  dentro de miniaturas raster queda exento: decirlo.
- `check_pdf_text.py` marca como huérfana una página con menos de `--orphan-chars` caracteres
  (por defecto 200); `--hints-file` = subcadenas a avisar, una por línea (nombres del cliente
  anterior, nombres internos, jerga de taller).
- `check_spanish_text.py` audita texto candidato (respuestas, mensajes de contacto) contra CJK,
  cirílico, palabras extranjeras sueltas (palabra completa), marcadores de nota y caracteres de
  control invisibles. `--words-file`/`--markers-file` reemplazan los valores por defecto salvo con
  `--extend`. Código 1 ante cualquier problema. Correrlo sobre un archivo escrito, no sobre memoria.
- Metadatos (pypdf `add_metadata`) **después** del último render; tras reescribir, volver a revisar
  `pdfinfo` y `pdffonts`.

## 5. Contraste medido en píxeles

- **Método sin texto**: ocultar el texto, capturar y tomar el percentil 95 de luminancia del fondo
  detrás de cada caja; contraste contra la tinta declarada.
- **Método con texto**: fondo = p20, núcleo del glifo = p99,5. Nunca p95 sobre texto con bloom: mide
  el halo (un caso reportó 1,22:1 en un documento que medía 6,66:1).
- **Pares calculados en el build**: helper WCAG `cr(fg,bg)`, juntar todos los pares tinta/fondo en una
  lista y fallar el build si alguno no pasa. Los tonos medios de marca (violeta, magenta, coral) fallan
  con blanco; los acentos sobre oscuro suelen necesitar variantes más claras, sobre claro más profundas.
- **Variables "secundarias"** (gris medio sobre casi negro) rondan 2:1: en callouts oscuros usar la
  tinta completa.
- **Fondo oscuro que sale blanco**: muestrear un píxel de esquina antes de tocar la paleta:
  `convert pg-1.png -crop 30x30+5+5 -resize 1x1 txt:`.
- **Perceptibilidad de acentos**: contar píxeles con el tono en el render; un color en el CSS no
  prueba que se vea. Efectos: scanline ~.028 de alfa es invisible, ~.075 compite con el texto.
- Detalle de temas oscuros: `dark-theme-legibility.md`.

## 6. Revisión visual dirigida

`vision_analyze` por página o por pares a ~100–110 dpi, con preguntas factuales: "¿qué % de la
página está vacío?", "¿hay tarjetas con borde o es fluido?", "¿se lee como documento profesional o
como terminal hacker?", "¿se lee bien o es casi ilegible?", "¿alguna afirmación contradice a otra o a
una etiqueta?". Recorte a ~170 dpi si es ambiguo. Si la visión contradice una medición, medir el
elemento concreto. La visión parafrasea: antes de "corregir" un texto señalado, grep en el HTML y
`pdftotext`; si el texto sí está, el comentario editorial suele ser válido.

## 7. Pitfalls de CSS, capas y SVG

- **Capa de textura** (`body::before` fixed, z-index alto) pinta sobre las tarjetas: arreglar el
  apilado (contenido `position:relative; z-index` mayor), no la opacidad. Probar con un conteo de
  bloques planos dentro del área de contenido, muestreando ventanas demostrablemente vacías.
- **Glow en `.page::before/::after` con offsets negativos** desplaza la paginación de Chromium y
  recorta contenido en otros elementos: poner los blobs en un `<div class="glow">` real con
  `position:absolute;inset:0;overflow:hidden`.
- **Regla transversal que repite `position:`** (`.pg .cab{position:relative}`) gana en especificidad y
  rompe cabecera/cuerpo/pie absolutos: declarar solo la propiedad que se añade (`z-index`).
  Diagnosticar con `getComputedStyle(el).position` y `scrollWidth` vs `clientWidth`.
- **Selector compuesto** (`.tile.tile-s`) gana a una sola clase escrita antes: auditar reglas de
  altura con colisiones de selector compuesto. Figura SVG recortada = cascada, no viewBox.
- **SVG sin width/height** dentro de un contenedor de alto fijo se desborda sobre lo siguiente:
  `.contenedor svg{height:100%;width:auto;display:block}`; revisar con un recorte alto en el borde.
- **Texto SVG que se escala** queda en 2–3 px reales: dimensionar cada figura a su caja en dos
  pasadas (render → medir caja → regenerar con viewBox = caja, hasta que no cambie). Etiquetas dentro
  de segmentos estrechos de barra se cortan: acortarlas.
- **Cromo de ventana dibujado en el borde** desaparece con `overflow:hidden` (recorta al padding box):
  `overflow:clip; overflow-clip-margin:<ancho del borde>`.
- **Grid que llena el resto de la página**: `flex:1 1 0; min-height:0` más `grid-auto-rows:1fr`.
  Una `height` fija se ignora en una columna flex si el ítem tiene `flex:1 1 0`: dar `flex:none`.
- **Lista que crece** con `grid-template-rows:repeat(N,…)` fijo derrama una columna entera.
- **Separadores** (`<i>` o `align-self:stretch`) en una fila flex sin altura de padre colapsan a un
  cuadrado: dar `min-height` explícita.
- **Clase de layout reutilizada** (`justify-content:center` + `margin-top:auto`) duplica el espacio:
  crear un modificador con margen explícito.
- **Nombres de clase genéricos** (`.pie`, `.card`, `.cl`) colisionan sin error de build: prefijar las
  clases de cada módulo (`cx-`).
- **Marco CRT para todas las figuras** en `border-image` 9-slice (PNG de centro transparente), no en
  `mask-image` (se rasteriza a baja resolución al imprimir).
- **Marca de agua con la silueta real del logo** se lee como forma dura aunque tenga blur: usar un
  `radial-gradient` puro.
- **Filtros CSS/SVG pesados** (blur, ruido, sombras) se rasterizan sin comprimir y engordan el PDF:
  capturar solo esas muestras a 3x en JPEG q90 y reemplazarlas; scanlines como teselas PNG.
- **Higiene de texto**: `&nbsp;` entre número y `%`; chips como lista alineada; garantías en grid de
  columnas iguales.

## 8. Pitfalls de generadores, datos y edición

- Cadena de `str.replace` con `assert`: atómica — si falla uno, no escribir nada. Un `str.replace`
  sin coincidencia "tiene éxito" en silencio. Releer la región justo antes de editar; calcular
  índices de slice *después* de todos los `replace`.
- Tras cualquier edición programática: asertar que el fragmento viejo ya no está **y** el nuevo sí,
  en el archivo en disco.
- No editar el generador con un heredoc `python3 - <<'EOF'`: escribir el script de edición como `.py`
  real y validar con `python3 -c "import ast; ast.parse(open('gen.py').read())"` antes del build.
- f-strings con CSS/JS/JSON: escapar llaves como `{{ }}` o usar `.format()`/plantillas.
- **YAML**: un valor inline con `: ` rompe `safe_load` (usar `>-`); un round-trip `safe_load` →
  `safe_dump` borra comentarios y puede renombrar claves. Releer el archivo y asertar claves/valores.
- **Conversor Markdown→HTML casero**: las líneas de continuación de un bullet envuelto cierran la lista
  y quedan como `<p>` huérfano; si se está en lista y la línea está indentada (`^\s{2,}\S`), añadirla
  al `<li>` anterior.
- **Mover/renombrar carpetas de marca**: los scripts tienen rutas absolutas; grep de nombres viejos,
  regenerar todo y comparar páginas, tamaño y `pdftotext` de la línea de contacto. Igual al cambiar
  datos de contacto.
- **Logo**: el único confiable es el embebido en el entregable final vigente (`{{LOGO_VIGENTE}}`);
  comparar parámetros numéricos (número de paradas del degradado, viewBox) con lo que documenta el
  manual. Extraer un `<svg>` de un HTML minificado grande con una lectura limitada por caracteres lo
  trunca sin error: preferir un `.svg` independiente y verificar el `</svg>` final.
- **Reusar un sistema de diseño grande**: extraer tokens, `@font-face` y clases de cromo a una hoja
  nueva mínima; no importar el HTML gigante. Si se reusa su CSS generado, cambiar solo la línea de
  fuente: un `:root` reconstruido a mano es donde se pierde la variable de fondo.
- Versiones múltiples de un activo: ordenar por mtime real (`stat -c '%Y %y %n' a b c | sort -n`),
  nunca por el nombre de la carpeta.
- Antes de ajustar un modelo paramétrico a una forma generada proceduralmente, buscar el generador
  original (reproduce al 100 %; el ajuste se estanca ~98 %).
- Comandos de build/render encadenados pueden quedarse esperando aprobación y no corren: correr
  build, auditoría y render por separado; si uno espera aprobación, reportarlo y esperar, sin
  reintentarlo por otra vía.
- Un chequeo que devuelve un número inverosímil está roto (p. ej. `grep` con rutas con espacios sin
  comillas).
- Rutas `file://` con caracteres no ASCII o espacios: `encodeURI(path)` en Playwright y
  `fileURLToPath(import.meta.url)` para el directorio del script; comprobar dónde cayó la salida.
