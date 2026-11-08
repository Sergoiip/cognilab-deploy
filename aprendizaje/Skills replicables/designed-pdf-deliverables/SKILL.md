---
name: designed-pdf-deliverables
description: "Use when a PDF must look designed, not just be text. Construye entregables (propuestas, briefs, one-pagers, manuales de marca, brochures) en HTML+CSS impreso con Chromium headless y los verifica con puertas numéricas: tamaño de letra, contraste, desborde y fuentes embebidas."
version: 1.1.0
author: comunidad
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [pdf, html, css, chromium, design, proposals, briefs, brand-manual, legibility]
  category: productivity
  related_skills: [pdf, docx, vault-crm-records, visual-taxonomy, humanizer]
---

# designed-pdf-deliverables

## Parámetros a configurar

| Placeholder | Qué poner | Ejemplo genérico |
|---|---|---|
| `{{CHROMIUM_BIN}}` | Binario de Chromium/Chrome con `--headless` | `chromium`, `google-chrome` |
| `{{RUTA_SCRATCH}}` | Carpeta temporal para HTML, PNG de prueba y builds | `./build/tmp` |
| `{{RUTA_ENTREGABLES}}` | Carpeta donde se publican los PDFs finales (fuera de la base de notas) | `<repositorio-de-operaciones>/comercial/piezas/` |
| `{{RUTA_DOCS_CLIENTE}}` | Carpeta de documentos por cliente | `<repositorio-de-operaciones>/clientes/<cliente>/documentos/` |
| `{{RUTA_GENERADORES}}` | Carpeta con generadores, datos (YAML/JSONL) y scripts de render | `<proyecto>/_fuentes/` |
| `{{RUTA_TALLER}}` | Carpeta pesada fuera del repositorio de notas (venvs, node_modules, corpus) | `<workspace>/taller/` |
| `{{RUTA_TIPOGRAFIAS}}` | Carpeta con los `.ttf/.otf/.woff2` de la marca | `./marca/fuentes` |
| `{{RUTA_MANUAL}}` | Carpeta del generador del manual de marca | `<taller>/manual/` |
| `{{SKILL_PDF_SCRIPTS}}` | Scripts de la skill `pdf` (render de páginas a PNG) | `<skills>/pdf/scripts/` |
| `{{SKILL_VOZ}}` | Skill o guía de voz para pulir la prosa | `humanizer` + guía de estilo |
| `{{PALETA_MARCA}}` | Archivo/nota donde vive la paleta oficial (hex) y sus tokens CSS | `marca/tokens.css` |
| `{{MANUAL_MARCA}}` | Documento con las reglas de marca vigentes (legibilidad, logo, tipografía) | `marca/manual.md` |
| `{{LOGO_VIGENTE}}` | Origen confiable del logo/isotipo (el embebido en el último entregable) | `entregables/hoja-marca.html` |
| `{{FONDO_PREFERIDO}}` | Política de fondo de página aprobada por el dueño de la marca | "oscuro con glow" / "alternar claro-oscuro" |
| `{{COLOR_FONDO}}` | Fondo casi negro de la marca (hex) | un casi-negro azulado, no `#000` |
| `{{COLOR_ACENTO}}` / `{{COLOR_ACENTO_2}}` / `{{COLOR_ACENTO_3}}` | Acentos primario, secundario y terciario opcional (hex) | azul eléctrico / magenta neón / coral |
| `{{COLOR_PROBLEMA}}` / `{{COLOR_SOLUCION}}` | Colores funcionales "antes/después" | naranja / verde |
| `{{HEX_VIEJO_n}}` | Hex de la paleta que se reemplaza (en `palette-swap.md`) | valores de la versión anterior |
| `{{FUENTE_CUERPO}}` | Sans legible para texto corrido | Atkinson Hyperlegible, Inter |
| `{{FUENTE_TITULOS}}` | Familia de títulos | una geométrica (Outfit) |
| `{{FUENTE_ETIQUETAS}}` | Monoespaciada/técnica para etiquetas y cifras | JetBrains Mono, Chakra Petch |
| `{{IDIOMA_ENTREGABLE}}` | Idioma único del documento (afecta el barrido de palabras extrañas) | `español` |
| `{{TRATAMIENTO_FORMAL}}` / `{{TRATAMIENTO_PUBLICO}}` | Tratamiento en propuestas formales / piezas públicas | `usted` / `tú` |
| `{{LECTOR_REFERENCIA}}` | Perfil del lector para la puerta de legibilidad | lector de 60 años |
| `{{ARCHIVO_DATOS}}` | Archivo de datos único (YAML/JSON) del que salen todos los documentos | `datos/servicios.yaml` |
| `{{ARCHIVO_CASOS}}` | Datos de casos publicables | `casos.yaml` |
| `{{ARCHIVO_PRECIOS}}` | Único lugar donde viven los precios en el generador | dict `PRECIOS` en `brochures.py` |
| `{{NOTA_MODELO_NEGOCIO}}` | Nota fuente de la oferta vigente y precios aprobados | `modelo-de-negocio.md` |
| `{{NOTA_SERVICIO_PRINCIPAL}}` / `{{REPO_ENTREGA}}` | Nota del servicio insignia y repo con fases/módulos | `servicio-principal.md`, repo git |
| `{{MONEDA}}` | Moneda del mercado del cliente | `USD`, `EUR`, `MXN` |
| `{{CONTACTO}}` | Canal de contacto y QR del vendedor | `[ SU CORREO ]` hasta que el usuario lo dé |
| `{{NOMBRE_CLIENTE}}` / `{{FECHA}}` | Datos de portada de la plantilla | "Empresa Ejemplo" / fecha completa |
| `{{NOMBRE_EMISOR}}` / `{{ORGANIZACION}}` | Quién propone y su organización | nombre y marca del vendedor |
| `{{PRECIO_*}}` | Cifras de opciones/planes/referencia (solo si el usuario las dio) | `[ PRECIO ]` visible |

Nunca rellenar estos valores inventándolos: si falta uno, dejarlo como marcador visible.

## Propósito

Producir documentos que alguien va a **mirar y juzgar** (propuesta, brief, one-pager, portafolio,
ficha de servicio, informe, SOW, handout, brochure, manual de marca). Texto *correcto* no es lo mismo
que documento *presentable*. El método: contenido resuelto primero → un HTML autocontenido + CSS con
un sistema de diseño → Chromium headless → verificación con mediciones (DOM, `pdffonts`,
`pdftohtml`, píxeles) y por lectura del contenido, no a ojo.

## Cuándo usar

- Un documento que un cliente, prospecto o empleador va a ver y evaluar por su apariencia.
- Cualquier PDF cuyo texto ya está decidido pero cuyo aspecto no se ha diseñado.
- Hace falta portada, tarjetas, columnas, control de página o tratamiento visual por sección.
- El usuario dice que el resultado se ve "feo", "básico", "plano", "poco profesional" o "no es
  llamativo": **eso es señal de pipeline equivocado, no petición de pulido.** Cambiar de pipeline,
  no retocar el spec.

No usar para formularios, merges, splits, extracción de texto, marcas de agua, metadatos o
cualquier PDF que leerá una máquina: eso es de la skill `pdf` (constructor por spec).

## Entradas

- Contenido (texto, datos, cifras) y su lector; idealmente en `{{ARCHIVO_DATOS}}`.
- Sistema de marca: `{{PALETA_MARCA}}` (`{{COLOR_*}}`), `{{RUTA_TIPOGRAFIAS}}` (`{{FUENTE_*}}`),
  `{{LOGO_VIGENTE}}`, `{{MANUAL_MARCA}}`, activos SVG de logo/isotipo.
- Tipo de documento: one-pager/tarjetas (alto fijo) vs. documento que fluye.
- Destinatario y registro (`{{TRATAMIENTO_FORMAL}}`/`{{TRATAMIENTO_PUBLICO}}`), y si hay un
  entregable previo que se está bifurcando.
- Datos de oferta si es comercial: `{{NOTA_MODELO_NEGOCIO}}`, `{{ARCHIVO_CASOS}}`, `{{ARCHIVO_PRECIOS}}`.
- Si es revisión: el generador fuente (no solo el PDF) y las notas por página del usuario.
- Herramientas: `{{CHROMIUM_BIN}}` headless (o Playwright), `pypdf`, PIL, poppler (`pdftoppm`,
  `pdffonts`, `pdftohtml`, `pdftotext`, `pdfinfo`), fontTools, `vision_analyze`; opcionales `zbarimg`,
  `qrencode`, `rsvg-convert`, ImageMagick. Scripts incluidos en `scripts/`.

## Decisión de ruta (tomarla primero)

**Un constructor por spec no puede diseñar.** El generador "JSON spec → PDF" emite títulos,
párrafos, tablas e imágenes sobre página blanca: sin color, sin layout, sin jerarquía.

| El usuario quiere | Ruta |
|---|---|
| Formulario, merge, split, extracción | scripts de la skill `pdf` |
| Algo que una persona va a mirar | **HTML + CSS → Chromium headless** |
| "Arregla este PDF que ya tengo" | Editar la fuente/generador, nunca regenerar a ciegas |

"Se ve feo" no se arregla subiendo tamaños en un spec: se reconstruye en HTML.

## Pasos

1. **Localizar las fuentes de verdad.** Paleta, tipografías, logo y manual vigentes. Si hay varias
   versiones, ordenarlas por mtime real (`stat -c '%Y %y %n' a b c | sort -n`), nunca por el nombre
   de la carpeta. El logo necesita su propia verificación de procedencia (ver Pitfalls).
2. **Escribir el contenido como spec en prosa.** Qué es la oferta, qué recibe el cliente, cuánto
   cuesta, cuál es el siguiente paso. El diseño no rescata una oferta confusa. Aterrizarlo en
   trabajo realmente entregado (ver "Vender un servicio").
3. **Datos → generador → HTML.** Si el documento se regenerará (precios, nombres), escribir un
   archivo de datos + un generador pequeño; el HTML es un artefacto de build. Un mismo script emite
   el maestro y cada one-pager desde el mismo registro.
4. **Escribir el HTML autocontenido** en `{{RUTA_SCRATCH}}`: un bloque `.page` por página impresa,
   en `mm` (A4 = `210mm × 297mm`, `@page{size:A4;margin:0}`, `print-color-adjust:exact`). Partir de
   `templates/a4-dark-layout.html` y sobrescribir sus variables `:root` con la paleta del usuario —
   nunca entregar los valores por defecto de la plantilla. One-pager/propuesta: `height:297mm;
   overflow:hidden`. Documento que fluye: `min-height:297mm` y saltos solo entre secciones mayores.
   CSS base completo: `references/render-and-verification-gates.md` §1.
5. **Embeber las fuentes** (una cara estática por peso, nunca el archivo variable) como data URI:
   ```bash
   python3 scripts/inline_fonts.py doc.html doc.inline.html --base {{RUTA_TIPOGRAFIAS}} --drop FamiliaSinUso
   ```
   `--base` resuelve los `url()` relativos; `--drop` quita `@font-face` de familias sin uso.
6. **Auditar el DOM antes de imprimir** (Playwright/CDP): desborde por página y contra la altura de
   la hoja, solapes entre hermanos, tamaño mínimo calculado en pt (HTML y SVG), espacio libre bajo el
   último bloque, fuentes realmente cargadas, texto SVG fuera de su caja. Salir con código distinto de
   0 si algo falla (snippets en §3 de la referencia).
7. **Renderizar headless:**
   ```bash
   {{CHROMIUM_BIN}} --headless --no-sandbox --disable-gpu \
     --no-pdf-header-footer --virtual-time-budget=15000 \
     --print-to-pdf={{RUTA_ENTREGABLES}}/OUT.pdf "file:///ruta/absoluta/doc.inline.html"
   ```
   `--virtual-time-budget` (10–15 s) deja que carguen fuentes y glows; sin él el texto refluye o sale
   en fallback. Éxito = `N bytes written to file`. Correr build, auditoría y render como comandos
   separados.
8. **Metadatos después del último render** (pypdf `add_metadata`); tras reescribir, volver a revisar
   `pdfinfo` y `pdffonts`.
9. **Medir el PDF final** (puertas numéricas; detalle en la referencia §4):
   ```bash
   python3 scripts/pdf_font_audit.py OUT.pdf            # mediana >= 11 pt, nada < 9 pt; código 1 si falla
   python3 scripts/check_pdf_text.py OUT.pdf --orphan-chars 150 --hints-file pistas.txt
   pdffonts OUT.pdf                                     # un subset por peso, CID TrueType, ningún Type 3
   ```
   `check_pdf_text.py` imprime caracteres por página y marca huérfanas (página con menos de
   `--orphan-chars`, por defecto 200) y scripts extraños; `--hints-file` lista subcadenas a vigilar
   (nombre del cliente anterior, nombres internos). Una página casi vacía = sección desbordada que dejó
   un huérfano: ajustar *esa* página.
10. **Mirarlo.** PNG por página y `vision_analyze` de cada una (o por pares):
    ```bash
    pdftoppm -r 110 -png OUT.pdf {{RUTA_SCRATCH}}/pg
    # alternativa: python {{SKILL_PDF_SCRIPTS}}/pdf_page_image.py OUT.pdf --pages 1-N --dpi 100 --out-dir ./pv
    ```
    Preguntar: ¿algo cortado, desbordado, superpuesto o desbalanceado?, ¿qué % está vacío?, ¿se lee
    bien? **Y también: ¿alguna afirmación contradice a otra en la misma página?** (p. ej. un párrafo
    dice "todos los trabajos previos fueron gratis" junto a una tarjeta marcada "primero cobrado"). La
    revisión de layout encuentra geometría; solo una lectura encuentra un documento que argumenta
    contra sí mismo. Pedir también balance y redacción (pronombre colgando al final, términos
    inconsistentes entre párrafos vecinos).
11. **Barrer contaminación** (texto extraído del PDF y prosa que acompaña la entrega) y **revisar la
    prosa** con `{{SKILL_VOZ}}`:
    ```bash
    python3 scripts/check_spanish_text.py respuesta.txt     # CJK, cirílico, palabras extranjeras, marcadores, invisibles
    ```
12. **Entregar** la ruta del PDF (y el set "para compartir" si se pidió). No enviarlo: entregar el
    archivo y dejar que el usuario lo despache. Señalar todo marcador que quede (`[ SU CORREO ]`).

## Reglas de decisión

**Contenido y voz**
- Tratamiento `{{TRATAMIENTO_FORMAL}}` en propuestas formales; `{{TRATAMIENTO_PUBLICO}}` en piezas
  públicas de la marca. Directo, sin jerga, una idea por párrafo, sin informalidad fabricada.
- **Nunca inventar un dato para llenar un hueco** (precio, correo, teléfono, empresa, fecha, plazo,
  garantía, permanencia). Marcador visible (`[ SU CORREO ]`) y nombrar el hueco en la respuesta. Un
  número equivocado es peor que un blanco obvio.
- Si no hay precio para un esquema nuevo: proponer cifras derivadas, rotularlas "propuesta/hipótesis"
  y guardarlas en un único dict (`{{ARCHIVO_PRECIOS}}`) para cambiar y reconstruir. Decir en la
  respuesta qué no se pudo verificar. Conflictos con las restricciones del cliente → callout visible.
- Una sola fuente de datos; cuentas derivadas del campo estructurado, nunca de un regex sobre prosa.
  Mapear etiquetas internas (`status: potencial`) a etiquetas para el cliente al renderizar, y
  traducir el vocabulario interno (CRM, jerga de taller) antes de que llegue al cliente.
- Un cambio de precio/conteo se propaga: buscar el número viejo, el conteo, el total y el ahorro
  derivado en TODO el HTML antes de regenerar.
- Separar lo decidido de lo que es borrador: lo marcado "borrador / por decidir / supuesto" queda
  fuera del documento o va como pregunta en la respuesta.
- Mostrar lo que ES, no lo que se descartó. Las exploraciones rechazadas van a un changelog.
- No reescribir un claim o eslogan de marca aprobado.
- Cortar frases autorreferenciales ("no es una frase de venta"), "no es X sino Y" repetido, guiones
  extensos apilados, "ideal para"; cambiar evaluaciones por hechos medibles ("Alcance · 1 equipo ·
  sin costo de infraestructura"). Contar los tics antes/después.

**Ubicación de archivos**
- PDFs operativos y sus generadores viven en `{{RUTA_ENTREGABLES}}` / `{{RUTA_DOCS_CLIENTE}}`; HTML de
  trabajo en `{{RUTA_SCRATCH}}`; entornos pesados en `{{RUTA_TALLER}}`, fuera del repositorio de notas.
  Nunca dejar un final suelto en una carpeta genérica de documentos.

**Legibilidad (puerta obligatoria para todo PDF de lectura)**
- Cada PDF pasa "¿lo leería `{{LECTOR_REFERENCIA}}` sin esfuerzo?". Si no o hay duda, se rehace.
- Mínimos: cuerpo ≥ 11,5 pt, peso ≥ 400, interlineado 1,5, 55–75 caracteres por línea; etiquetas
  ≥ 9,5 pt peso ≥ 500; **nada < 9 pt** en ninguna parte (incluido texto dentro de SVG, medido
  impreso). Peso 300 solo en titulares ≥ 18 pt; sin Light en el cuerpo.
- Contraste del cuerpo ≥ 7:1 (mínimo absoluto AA 4,5:1), **calculado** con un helper WCAG `cr(fg,bg)`
  sobre todos los pares tinta/fondo; el build falla si alguno no pasa.
- **Verificar con los tamaños extraídos del PDF final** (`scripts/pdf_font_audit.py`: mediana, % bajo
  umbral), no con el CSS; contraste medido en píxeles (núcleo del glifo, no halo).
- Fondo por página según `{{FONDO_PREFERIDO}}`. Si es oscuro: degradado con glow suave y paneles de
  vidrio (rgba oscuro) detrás del texto denso; la legibilidad sale del contraste medido, no de aclarar
  el fondo. Si se alterna: páginas densas claras; portada, divisores y poco texto oscuras.
- La legibilidad es la restricción; el carácter (glow, scanlines, viñeta) se paga con lo que sobra, y
  "nada tacky" es el techo. Al aplicar un efecto, entregar efecto **y** ratio medido
  (`references/dark-theme-legibility.md`).
- Navegación: índice clicable si > 4 páginas, sección en cabecera, número en pie, una idea por
  página, título de figura + una línea de lectura, siguiente paso concreto al final.
- Si la legibilidad fue el motivo de rehacer: medir el PDF actual antes de proponer nada y abrir la
  respuesta con esos números contra la regla. Agrandar la letra convierte una hoja en varias: decirlo
  y renombrar "en una página" en títulos, notas y scripts.
- Rehacer muchos PDFs: auditar todos (`pdf_font_audit.py *.pdf --no-gate`) → escribir la regla en el
  manual de marca → rehacer UNO de muestra para aprobación → el resto. Documentos de uso interno
  pueden conservar su escala; los comerciales no.

**Layout**
- Página que desborda: recortar padding de página → espacio entre ítems → padding de callouts.
  Cortar prosa es lo último; arreglar márgenes antes que reducir tipografía.
- Página medio vacía (> 25 mm libres o > 25–30 % de la altura): añadir **contenido real** (párrafo de
  soporte, franja de resultados, tabla secundaria, frase-resumen grande de 24 pt/900 empujada con
  `margin-top:auto`), no un spacer. `zoom` por página es el recurso más barato: aplicarlo por página,
  re-chequear tablas extensas (la última fila cae bajo el pie) y nunca insertarlo con regex ciega.
- Llenar páginas de tabla/pasos haciendo crecer el contenido: `table{flex:1 1 auto}` con
  `vertical-align:middle`; listas de pasos `flex:1` con hijos `flex:1 1 auto`.
- "Mucho texto": convertir prosa en gráfico (barra proporcional apilada, línea de tiempo, fila icono +
  una línea, tarjetas de icono). Sin iconos de marca, crear un set pequeño (`ICONS` dict +
  `icon(name,size,color)`) con el grosor/linecap de la marca y `stroke="currentColor"`.
- Opciones paralelas (niveles de una oferta) lado a lado: `display:flex`, `flex:1 1 0`,
  `align-items:stretch`. Dos o tres opciones como tarjetas con peso visual persuaden; una tarjeta
  por bullet es ruido. Una caja se gana su lugar cuando carga una distinción (precio, nivel, plan).
- "Fluido, no en cajas" = demasiados bordes: fondo continuo, jerarquía por tamaño/peso/color, titular
  de sección 35–70 pt, kicker pequeño, números tipográficos grandes en vez de iconos, glow solo en UN
  elemento hero por página, imágenes a sangre con leyenda; tarjetas solo para datos tabulares (2–3 por
  documento).

**Diseño**
- Los gráficos cargan el mensaje y el texto da contexto: cada bloque = una ilustración + etiqueta en
  negrita de 2–4 palabras + una línea de contexto.
- Densidad gráfica según formato: PDF/informe ≈ 55 % gráfico (diagramas completos, etiquetas
  ≥ 9 pt); piezas estáticas (carrusel, story) ≈ 75 %; video ≈ 85 %. Estéticas propias de video
  (renders 3D de época, bumpers) no van a impresos.
- Un manual/guía "diseñado" incrusta los activos reales (SVG inline, chips de color nativos,
  especímenes con las fuentes reales, diagramas); reconstruir en HTML/CSS en vez de pegar capturas;
  raster solo para fotos/texturas. Mostrar la construcción (coordenadas, paradas de degradado,
  mediciones) da más dignidad que describir la conclusión: geometría en el SVG, valores en una tabla HTML.
- Referencia citada como "quiero que se vea así de digno": preguntar si se quiere la **estética** de la
  referencia o el **nivel de rigor** con la estética propia.
- El color tiene trabajo: `{{COLOR_PROBLEMA}}` marca "antes"/problemas, `{{COLOR_SOLUCION}}`
  "después"/garantías; complementarios solo puntuales, nunca como segunda paleta.
- Nunca añadir un color, parada de gradiente o estilo que el usuario no pidió: extender una paleta
  definida es una decisión, no pulido. La paleta es del dueño de la marca: buscarla primero
  (`{{PALETA_MARCA}}`, notas de diseño, artefactos previos); si no existe, decirlo y sugerir
  guardarla. Si aparece una nota con nombre de color, leerla antes de asumir que es una paleta.
- Corrección de paleta = veredicto ya dado: "se ve genial, pero mis colores son X e Y" aprueba
  composición y textura. Re-renderizar en la nueva paleta sin re-litigar la estética
  (`references/palette-swap.md`).
- Temas oscuros imprimen mal: con clientes externos, confirmar entrega en pantalla antes de
  comprometerse a fondo oscuro. Si la marca ya decidió fondo oscuro, no reabrirlo.
- Las barras de título de ventanas/terminales dan contexto o venden, nunca una ruta o nombre de
  archivo. `min-height` en vez de `height` fija; misma min-height para barras de la misma fila.
- Monoespaciada solo en títulos técnicos, etiquetas y cifras: el cuerpo en mono hace que el documento
  parezca "de los 90". La tipografía pesa más que la paleta.

## Verificación

Correr todo; un conteo de páginas no detecta un bloque recortado.

- [ ] Auditoría DOM limpia: `scrollHeight - clientHeight` = 0 por página, desborde contra la hoja
      (297 mm ≈ 1122,5 px), sin solapes entre hermanos, nada < 9,5 pt calculado (HTML y SVG),
      fuentes cargadas = una por peso declarado.
- [ ] `python3 scripts/pdf_font_audit.py OUT.pdf` pasa (mediana ≥ 11 pt, nada < 9 pt); con
      `--min-median 11.5 --min-size 9.5` para piezas comerciales. Texto en miniaturas raster exento: decirlo.
- [ ] `python3 scripts/check_pdf_text.py OUT.pdf` sin huérfanas ni scripts extraños; número de
      páginas correcto (en el HTML: `class="page[ \"]`).
- [ ] `pdffonts OUT.pdf`: un subset por peso, CID TrueType, ningún `Type 3`. Glifos especiales
      (✓ ✕ ≥ α) cubiertos por el cmap de la fuente.
- [ ] Contraste medido en píxeles (núcleo p99,5 contra fondo p20, o fondo p95 con texto oculto) y
      pares WCAG calculados en el build.
- [ ] Cada acento es *perceptible* en el render (conteo de píxeles o visión sin titubeo), no solo declarado.
- [ ] Revisión visual por página (corte, desborde, superposición, balance, % vacío) **y** lectura de
      contradicciones/redacción.
- [ ] Barrido de contaminación sobre el texto extraído (CJK, cirílico, palabras de otro idioma, tokens
      pegados, tildes perdidas como `segun`/`opcion`, nombres internos/de clientes) y
      `scripts/check_spanish_text.py` sobre la prosa que se entrega fuera del PDF.
- [ ] Al derivar un documento de otro: el nombre anterior ya no aparece en el texto **extraído del PDF
      en disco** (`check_pdf_text.py --hints-file`).
- [ ] Tras cualquier edición programática: el fragmento viejo ya no está **y** el nuevo sí, en disco.
- [ ] Variantes generadas en lote: cada PDF verificado por separado.
- [ ] QR: decodificado con `zbarimg` sobre el PNG final *y* el render del PDF.
- [ ] Respuesta: ruta del PDF, qué cambió, qué quedó como marcador y qué decisiones no se pudieron tomar.

Barrido rápido de tokens pegados (adaptar al par de idiomas; el resto lo cubren los scripts):
```bash
python3 -c "
from pypdf import PdfReader
import re
t=''.join(p.extract_text() for p in PdfReader('OUT.pdf').pages)
print('pegados:', re.findall(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]{3,}[A-ZÁÉÍÓÚ][a-z]',t)[:20])"
```

Snippets de auditoría DOM, métodos de contraste, muestreo de fondo y preguntas de visión:
`references/render-and-verification-gates.md`.

## Pitfalls

**Render, fuentes y paginación**
- `min-height:297mm` en una página fija deja derramar contenido y Chromium añade una página fantasma:
  `height:297mm; overflow:hidden` y apretar la página que desborda. Las páginas huérfanas no aparecen
  en el log de Chromium: solo el conteo de caracteres por página las delata.
- Con `min-height`, el chequeo de desborde contra el propio elemento nunca dispara: medir contra la hoja.
- Archivo de fuente variable → el PDF solo embebe la instancia por defecto (`Type 3`, todo en un peso):
  instancias estáticas con fontTools `updateFontNames=True`. `file://` en `@font-face` puede
  "cargar" y no llegar al PDF: data URI con `inline_fonts.py`.
- Glow en `.page::before/::after` con offsets negativos desplaza la paginación: blobs en un
  `<div class="glow">` real con `overflow:hidden`. Capa de textura fija con z-index alto pinta sobre
  las tarjetas: arreglar el apilado, no la opacidad.
- Convertir un artefacto web scrolleable (nav sticky, hero de viewport, layouts para pantalla ancha)
  rompe cosas: en `@media print` usar `nav{display:none}`, `break-inside:avoid` en contenedores de
  tarjeta (no en `section`s enteras), re-centrar wrappers flex/grid. Repetir verificación completa.
- Texto SVG escalado queda en 2–3 px reales; SVG sin width/height desborda su contenedor.
- Filtros CSS/SVG pesados se rasterizan sin comprimir y engordan el PDF.

**Contraste y efectos**
- "No se ve la letra" es un bug de contraste: fijar `color` explícito en cada `h1/h3/p/li` dentro de
  tarjetas, no confiar en herencia; nunca texto neón sobre bloque claro. Variables "secundarias" (gris
  medio sobre casi negro) rondan 2:1.
- Un color presente en el CSS no es un color que el lector ve: en fondo casi negro un acento de
  luminancia media se vuelve un tinte imperceptible. Reforzarlo donde carga significado (regla
  superior, línea de claim, offset cromático del `h1`, el elemento que debe vender).
- Glow, viñeta y scanlines degradan legibilidad de forma acumulativa e independiente; el usuario nombra
  el síntoma ("los textos se ven opacos") sin diagnosticar. Identificar la causa antes de tocar valores.
- Medir contraste en el núcleo del glifo, nunca en el halo (un p95 sobre texto con bloom reportó
  1,22:1 en un documento que medía 6,66:1). Fondo oscuro que sale blanco: muestrear la esquina del PNG
  antes de tocar la paleta.
- Un `text-shadow` ancho se lee como blur; un glow en capas (5–6 px, 12–16 px, 1 px de reflejo, 1 px de
  offset cromático) se lee como halación y conserva el núcleo blanco.
- En fondo casi negro, un efecto de borde hecho de oscuridad es invisible: el borde debe ser *luz*
  tenue cortada por scanlines. Verificar muestreando píxeles de borde vs. interior.
- Marca de agua con la silueta real del logo se lee como forma dura: usar un `radial-gradient` puro.
- Nunca imprimir metadatos de producción dentro de una figura ("TX 4.8 · scanline + bloom").

**CSS y layout** (lista completa en la referencia §7)
- "Sin overflow" no es "sin solapamiento": flex encoge bloques en vez de scrollear.
- Selectores compuestos y reglas transversales que repiten `position:` ganan en especificidad: declarar
  solo la propiedad que se añade; prefijar las clases de cada módulo (`cx-`).
- Cromo de ventana en el borde desaparece con `overflow:hidden`: `overflow:clip` +
  `overflow-clip-margin`. Separadores flex sin altura de padre colapsan: `min-height` explícita.
- Auditorías fantasma: capas decorativas `inset:0` cuentan como solapes; filtrar al contenedor de contenido.

**Generadores y edición** (lista completa en la referencia §8)
- Cadena de `str.replace` con `assert`, atómica; un `replace` sin coincidencia "tiene éxito" en
  silencio. Releer la región justo antes de editar.
- Editar el generador con un `.py` real (no heredoc) y validar con `ast.parse` antes del build;
  f-strings con CSS/JS: escapar llaves.
- La contaminación aparece en la parte del archivo que no se acaba de releer (frontmatter, tags,
  cuerpos escritos varias llamadas antes): barrer el **archivo completo** siempre. Generar muchos
  bloques extensos a la vez es lo que contamina: uno a la vez con chequeo entre medio.
- **Nunca afirmar una verificación que no se corrió.** Escribir el texto candidato a archivo, correr el
  barrido y recién entonces describirlo. Un chequeo con número inverosímil está roto.
- La visión parafrasea: antes de "corregir" un texto señalado, grep en el HTML y `pdftotext`.
- Logo: el único confiable es el embebido en `{{LOGO_VIGENTE}}`; un `<svg>` extraído de un HTML
  minificado con lectura limitada se trunca sin error.
- Un comando de render que espera aprobación no corre: reportarlo y esperar, sin reintentar por otra vía.

**Contenido sensible**
- Usar una evaluación previa del lector para persuadir está bien; citarla o insinuar que existe un
  archivo sobre él, no.
- Producir una propuesta no es enviarla: en el CRM registrarla como preparada y dejar el lead en su
  estado previo (`vault-crm-records`).
- Mockups de co-branding: marca invitada como placeholder genérico en su color, fuera del degradado de
  la marca propia; nunca sus logos.

## Variantes

Resumen; el procedimiento completo de cada una está en [`references/variants-playbook.md`](references/variants-playbook.md).

- **Mini-deck 16:9** (incidentes, status, roadmaps): `@page{size:338.67mm 190.5mm;margin:0}`, una `<section class="slide z">` por slide con `--z` de zoom por slide, una idea por slide.
- **Maestro + N one-pagers** desde un dato: agrupar por categoría/nivel y clase en `<body>` por variante; verificar cada PDF.
- **Plan/roadmap para cliente**: `lib.py` + `figs.py` + `build.py` → HTML A4 fijo → `render.mjs` (Playwright) con informe por página; incluir decisiones pendientes y "primeros 7 días".
- **"Para compartir en línea"**: PDF + HTML autocontenido + PNG de portada + tarjeta social 1200×630.
- **Derivar la propuesta de un segundo cliente**: fork del HTML aprobado, escribir a disco antes de verificar, preguntas en una sola tanda, no crear entidades CRM sin que algo haya pasado.
- **Aplicar una estética aprobada / rehacer un documento ilegible**: trabajar sobre la fuente con nombre nuevo; generador nuevo en vez de parchear la escala vieja.
- **Igualar una referencia sin fuente**: renderizar 3–4 páginas representativas, extraer tokens con visión, listar todas las páginas del original.
- **Revisar un multipágina desde notas por página**: localizar generador, respaldar, mapear notas a elementos con visión, aplicar solo el lote pedido (detalle de manuales en [`references/brand-manual-revision-lessons.md`](references/brand-manual-revision-lessons.md)).
- **Iterar el sistema de marca completo**: hoja de marca → isotipo → manual; dirección de arte aprobada antes de rediseños grandes; "itera la versión X" = reconstruir con el sistema de X desde un generador.
- **Reconstruir material comercial para público general**: localizar generador + datos, reescribir para un desconocido, entregar PDF + PNG + tira vertical, archivar lo viejo (patrones en [`references/sales-collateral-patterns.md`](references/sales-collateral-patterns.md)).

## Vender un servicio: reglas de contenido

- **Aterrizar en trabajo entregado, no en capacidad.** Cada línea abstracta ("optimización de
  procesos") se reemplaza por un flujo concreto: qué hace, con los datos de quién, qué devuelve.
- **Mostrar trabajo previo, anonimizado**, como tarjetas de caso: qué se construyó, sobre qué, qué
  prueba. Quitar nombres y relación ("hecho para un familiar, gratis" hunde el valor percibido).
  Estado honesto por tarjeta (`Completado`, `Cobrado`).
- **Anclar el costo de infraestructura con precios reales del mercado** del cliente (proveedor,
  `{{MONEDA}}`, mensual), consultados y citados: se paga el trabajo, el servidor es barato.
- **Nunca cotizar un precio que el usuario no dio.**
- Escribir en la voz del vendedor, concreta: qué le toca hacer al cliente, casos reales (o un honesto
  "todavía no hay un caso publicado"), cómo se cobra. Evitar eslóganes en tríadas y boilerplate
  repetido en cada página ("suena a IA"); conservar textualmente los eslóganes aprobados.
- Vender el modelo de oferta **vigente**, leído de las notas de negocio actuales, nunca de un PDF viejo.
- Para ofertas de agentes de IA: vender organización (flujos, orden de archivos, cuentas conectadas),
  no "un chat"; diagrama hub, un SVG por función, antes/después.

## Implementación de referencia

Un sistema que funcionó en producción, descrito genéricamente para adaptarlo:

- **Entorno:** binario `chromium` en el PATH (no `chromium-browser`); si falta, probar `google-chrome
  --headless --print-to-pdf` antes de concluir que no hay HTML→PDF. Paleta en un módulo de color del
  generador y en un archivo de tokens; datos comerciales (servicios, precios, contacto) en un único YAML.
- **Generador de documentos de marca por módulos** (`modulo_*.py`, cada uno exporta un `CSS_*` y una
  función que llama a helpers `pagina/abre_seccion/espacio/empuje`); cada documento registrado con un
  id en un diccionario `DOCS`. Bucle: generar → auditor DOM (desborde 0,0 mm, sin solapes) → render →
  `pdftoppm -r 100` → revisión visual. Respaldo del generador y del PDF previo antes de cada cambio.
  Espacio vacío medido sumando la altura de spacers sin texto (> 20 mm = añadir contenido); bloques
  comprimidos con `scrollHeight - clientHeight > 4`. Script de contraste por hoja (Node + Playwright)
  que oculta el texto, captura y toma el p95.
- **Lección de auditoría:** PDF comerciales con mediana 7–8 pt y > 80 % del texto bajo 10 pt (cuerpo
  9,2 pt Light, etiquetas 6,8 pt en mayúsculas espaciadas): no reutilizar escalas tipográficas "de
  manual" sin pasar `pdf_font_audit.py`.
- **Sistema visual** (estética oscura con acento neón, glow moderado, gradiente único, marco CRT 9-slice, look 3D de época solo para video, QR vectorial, módulo SVG compartido): [`references/reference-visual-system.md`](references/reference-visual-system.md).

## Archivos de soporte

- [`templates/a4-dark-layout.html`](templates/a4-dark-layout.html) — documento A4 oscuro completo: portada, tarjetas de opciones, alcance numerado, pasos, callout, desglose de costo, cierre. Paleta en variables `:root`.
- [`templates/a4-commercial-blocks.html`](templates/a4-commercial-blocks.html) — bloques de propuesta con precio: niveles con cifras a la derecha, tarjetas de caso anonimizadas, tabla de costos de mercado, lista de flujos concretos. Hereda las variables del layout.
- [`references/render-and-verification-gates.md`](references/render-and-verification-gates.md) — CSS base, pipeline de fuentes, snippets de auditoría DOM, uso detallado de los scripts, métodos de contraste en píxeles, preguntas de visión y pitfalls completos de CSS y generadores.
- [`references/variants-playbook.md`](references/variants-playbook.md) — procedimiento completo de cada variante (deck, one-pagers, roadmap, fork de propuesta, referencia sin fuente, revisión por notas, sistema de marca, material comercial).
- [`references/reference-visual-system.md`](references/reference-visual-system.md) — sistema visual de referencia: estética oscura con acento neón, glow, gradiente, marco CRT 9-slice, look 3D de época, QR vectorial, módulo SVG compartido.
- [`references/palette-swap.md`](references/palette-swap.md) — cambiar colores conservando la composición y probar que el cambio es total y perceptible.
- [`references/dark-theme-legibility.md`](references/dark-theme-legibility.md) — medir contraste en fondo oscuro (p20/p99.5), las tres causas de una página que brilla pero no se lee, receta de glow en capas.
- [`references/brand-manual-revision-lessons.md`](references/brand-manual-revision-lessons.md) — revisar un manual de marca generado: familia de manuales, modos de figura, pipeline de legibilidad y repaginación, overlays CRT, índice clicable, reglas de copy.
- [`references/sales-collateral-patterns.md`](references/sales-collateral-patterns.md) — piezas para prospectos: dónde viven los hechos de la oferta, set de piezas, loop de build y auditoría.
- [`scripts/pdf_font_audit.py`](scripts/pdf_font_audit.py) — tamaños de fuente del PDF final vía `pdftohtml`; puerta `--min-median` / `--min-size`, `--no-gate` para solo informe.
- [`scripts/check_pdf_text.py`](scripts/check_pdf_text.py) — caracteres por página, huérfanas (`--orphan-chars`), scripts extraños y subcadenas vigiladas (`--hints-file`).
- [`scripts/check_spanish_text.py`](scripts/check_spanish_text.py) — prosa candidata (archivo o `-`): CJK/cirílico, palabras extranjeras, marcadores de nota, invisibles (`--words-file`, `--markers-file`, `--extend`).
- [`scripts/inline_fonts.py`](scripts/inline_fonts.py) — embebe `@font-face` como data URI (`--base`, `--drop`).

Origen: abstraída y fusionada de dos skills internas de PDFs diseñados (2026-11).
