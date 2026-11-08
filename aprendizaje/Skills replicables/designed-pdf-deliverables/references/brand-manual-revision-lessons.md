# Revisar un manual de marca generado (HTML → PDF con Chromium): lecciones

Parámetros usados aquí: `{{RUTA_MANUAL}}` (carpeta del generador del manual), `{{COLOR_FONDO}}`,
`{{COLOR_ACENTO}}`…`{{COLOR_ACENTO_3}}`, `{{FUENTE_CUERPO}}`, `{{FUENTE_TITULOS}}`, `{{FUENTE_ETIQUETAS}}`.

## Una familia de manuales: el sistema que funcionó

**Estructura**
- **Varios manuales, un generador, un sistema visual.** Ejemplo de reparto: Marca (A4 vertical) ·
  Sistema visual (A4 horizontal) · Universo/mundo narrativo (16:9) · Negocio y operaciones (A4 vertical,
  procesos dentro) · Contenido y canales (16:9).
  - El sistema base: grid de 12 columnas, láminas tipo ventana (`.lam`), pies de figura numerados, barra
    de ciclo, encabezado y pie.
  - Las páginas vigentes de una versión anterior se importan con una función `capturar()`; todo lo demás
    son páginas nuevas sobre el mismo grid.
  - Nunca copiar el manual viejo ni inventar un look nuevo: la copia se lee como “parches / Frankenstein”,
    el look nuevo como “horroroso”.
- **Niveles por manual** en un YAML de familia (universo, atmósfera, cromo, texturas, color, gráficos, 0–4).
  Mostrarlos como barras en cada portada **y** usarlos para dirigir el CSS (`--atm`, `--tex`). Un % que solo
  se muestra cuenta como “no usado”.
- **Fondo:** gradiente atmosférico en CADA página (cielo nocturno que cae a un horizonte en el color de
  sección, vidrio suave en las láminas). Intensidad = `.45 + .55·nivel/4`, para que nunca sea invisible.
  Fondos rechazados: lámpara de lava, malla de partículas, grano de película superpuesto, banda de ruido aislada.
- **Marca vs. universo:** el manual de marca lleva universo 0 (el mundo narrativo solo como texto de
  referencia y una página puente); el universo es acabado solo en los manuales de universo y contenido.
- **Cada gráfico es replicable:** componente + técnicas en orden con dosis, mostrado como ficha bajo la
  figura. Componentes de contenido (lazo de retroalimentación, stock y flujo, capas concéntricas, carril
  de proceso, atractor, red adaptativa, medidores) en módulos reutilizables.
- **Reglas de contenido:** sin precios en los manuales; datos no medidos se muestran “por medir” (medidor
  punteado), nunca inventados; eliminar lo rechazado en vez de conservarlo.

**Un solo lenguaje de diagramas**
- Diagramas raster junto a láminas vectoriales se leen como “no son del mismo sistema”. Diagramas de
  contenido en SVG desde un módulo único: trazos finos, trazo con gradiente más copia difuminada, nodos
  anillo, conectores de un color fijo, tarjetas con radio pequeño, etiquetas en las fuentes del sistema.
  Raster solo para demos de técnica y renders.
- Usar el nombre del componente como título de la lámina, nunca un pie truncado.
- En portadas verticales, apilar isotipo y título.

**Tipografía**
- Tres familias con roles: `{{FUENTE_TITULOS}}` títulos, `{{FUENTE_ETIQUETAS}}` datos y etiquetas,
  `{{FUENTE_CUERPO}}` (una hiperlegible) para todo el texto corrido. Copiar las fuentes al proyecto.
- Encabezados corridos en monoespaciada a 9,5 pt se leyeron como ilegibles: títulos de sección grandes con su número en color.

**Paleta**
- Si el usuario recupera una paleta complementaria antes retirada, no hacer reemplazos globales de esos hex:
  el rechazo puede haber sido solo en un contexto (p. ej. cromo o gradiente), no en todo el sistema.
- Un solo gradiente para isotipo y cromo: el espectro de marca. Hacer que la auditoría falle si un
  complementario aparece en el cromo de página.
- Probar que un color eliminado no está en el render (no en el CSS): rasterizar cada página a 30 dpi y
  contar píxeles por HSV (amarillo/dorado ≈ h 0,09–0,17, s > 0,5, v > 0,6); las páginas con hits deben
  explicarse como obra de referencia.
- Variantes de logo: verificar el nombre de la variante contra el fondo (una “una tinta clara” puede ser
  tinta OSCURA para fondos claros); sobre `{{COLOR_FONDO}}` usar la variante para fondo oscuro.

## Mecánica de layout que lo hizo funcionar

- **El helper de figura elige modo de imagen por tipo:** renders/fotos → `object-fit:cover`; arrays
  generados → recortados al contenido (máscara sobre canal máximo > ,09) y `mix-blend-mode:screen` sobre
  lámina transparente; mapas/hojas con fondo propio → sin estirar, con `aspect-ratio` de la fuente. El
  letterboxing dentro de un marco estirado fue la causa principal de que el manual 16:9 se viera mal.
- **Aspecto del diagrama = aspecto del marco:** en páginas verticales, renderizar diagramas altos
  (H≈1300–1500 para W≈1100–1400) y convertir filas de diales en 2×2.
- **Páginas de universo a sangre:** render bajo un scrim con panel de vidrio (rgba oscuro ~.84, blur,
  regla izquierda de acento) que contiene el texto.
- **Filas de mockups llenan la altura:** fila flex con ítems `height:100%` y aspect-ratio para 9:16/4:5;
  grid de N columnas iguales para fotos; 2×2 cuando aplique.
- **Índice horizontal:** dos columnas con `align-content:space-evenly`.
- Barras de título con `nowrap` ensanchan pistas del grid: usar `minmax(0,1fr)`.

## Pipeline de legibilidad para páginas importadas de letra pequeña

- Un script reasigna cada tamaño en pt (×1,38, piso 9,5 pt), aclara grises de texto a un gris legible y
  actualiza el descriptor; también escribe variantes ×1,26/1,16/1,08.
- Un script de paginación: recolorea texto SVG gris; sube texto SVG a ≥ 9,5 pt y lo encierra en su lámina;
  divide solo páginas apiladas verticalmente, en mitades ≥ 45 % llenas; cae a la variante más grande que
  quepa; reparte espacio sobrante entre bloques (≤ 9 mm por hueco) si > 20 % está libre; renumera y
  reconstruye el índice.
- Cortes manuales en el generador con `<!--SALTO-->`, rebalanceados a mano para que ninguna página quede con un bloque solo.
- **Pitfall:** dividir automáticamente “lo que desborda a la página siguiente” crea páginas fragmento. Nunca dividir grids lado a lado automáticamente.
- **Pitfall:** el texto del generador que enuncia tamaños (tabla de jerarquía) debe actualizarse al reescalar, o el manual documenta tamaños que ya no usa.

## Auditoría después de cada build

- Reportar por página % de relleno y área gráfica, marcar páginas solo-texto, detectar estructura rota
  (contenido fuera de `.cuerpo`, recortado en silencio por `overflow:hidden`) y validar cada ficha contra
  su YAML de fichas y el registro de componentes.
- Verificar páginas sueltas con un script de páginas; la visión sobre hojas de contacto lee mal los contadores.
- **Pitfall:** nunca editar HTML capturado con regex no codicioso `.*?</div>`: se detiene dentro de divs
  anidados, cierra `.cuerpo` antes de tiempo y el resto se recorta. Cortar entre marcadores conocidos con `str.find`.
- **Pitfall:** una figura de aspecto fijo en columna flex se encoge y su lámina pisa el texto siguiente:
  `figure{flex:none}`; figuras que crecen `flex:1 0 auto` (`1 1 0` solo dentro de columnas de grid).

## Pitfalls de revisión

- Veredictos de visión sobre hojas de contacto son pistas: cuenta mal páginas, llama ilegible el texto de
  miniaturas, marca tiles vacíos que están bien. Re-renderizar a 40–60 dpi y preguntar algo factual.
- Nunca etiquetar una ficha con un id de técnica que no esté en el registro.
- Formatear números raster a mano (si no, se cuelan reprs float32 como 13.3999996).
- Encerrar etiquetas raster dentro del canvas; dibujar marcas como formas, no glifos raros (dan tofu en algunas fuentes).
- f-strings anidadas del generador requieren Python ≥ 3.12. Si usas un venv distinto desde otra
  herramienta, limpiar `PYTHONPATH`/`PYTHONHOME` (`env -u PYTHONPATH -u PYTHONHOME`) para no importar otra copia de PIL.

## Igualar un look desde referencias (fondos, texturas)

- Si el look se describe con metáforas (“lámpara de lava”, “grano”, “que fluya”, “más cibernético”), pedir
  1–3 imágenes de referencia tras la PRIMERA ronda rechazada, no la cuarta.
- Medir antes de replicar: desviación del grano tras high-pass gaussiano a un ancho común; histograma y
  media de luma; correlación de ruido R–G (≈ 1 = grano monocromo). Comparar recortes a la MISMA escala.
- Grano “que es parte de la malla” = ruido que tramea la caída y posición de color del gradiente, no una capa encima.
- Recorrer un espectro con `% 1` deja una costura dura; usar una onda triangular.
- Mostrar continuidad entre páginas en una hoja por columnas (cada página bajo la anterior).

## Dirección de arte antes de reconstruir un manual

- Preguntar en UNA tanda: lector y número de documentos, formato, dirección visual, densidad, método de
  aprobación. Luego entregar documento de dirección de arte + páginas de muestra.
- Revisar en bloques de varias partes del índice, con las páginas de las versiones candidatas lado a lado
  por tema; el usuario decide qué vuelve, qué queda, qué se combina.
- Regla de página: 2–3 ideas por página, 3:2 gráfico/texto.
- Documentar la receta de luz del isotipo (gradiente de marca, luz blanca y borde con sus porcentajes, color de glow, radios de blur) como “espectro de resplandor documentado”.

## Iterar el sistema de marca (manual, hoja, piezas derivadas)

El manual es la raíz de todas las demás piezas: prioridad coherencia, no volumen.
1. **Leer antes de proponer:** manual, notas de contexto para IA, brief, modelo de negocio, visión,
   catálogo de taxonomía. Luego buscar en el repositorio los taglines/descriptores viejos (`grep -rlE`
   excluyendo `.bak` y `_archivo`) para obtener la lista real de propagación.
2. **Entregar tabla de diagnóstico (sección → incoherencia) y propuesta de estructura; parar para aprobación.**
   Agrupar decisiones abiertas en una lista; decidir tú las de bajo riesgo.
3. **Orden: hoja de marca → nota canónica del isotipo → manual.** Texto aprobado antes de renderizar — salvo
   que el usuario pida generar todo el PDF; entonces tomar la opción recomendada en cada pregunta abierta y
   listar esos defaults en el reporte para que pueda revertirlos.
4. **Los precios nunca viven en el manual ni en la hoja**, solo nombres de producto y estructura de escalera.
5. **Los términos propios del usuario se quedan** aunque una lectura técnica choque; no proponer reemplazarlos.
6. **No renombrar términos establecidos para resolver ambigüedad:** desambiguar con un calificativo.
7. **Revisar pies y encabezados corridos** por descriptores retirados: se repiten en cada página, no solo en la portada.

**Verificar que los “archivos fuente aprobados” muestran la marca actual.** Renderizar cada SVG citado
(`rsvg-convert -w 400 -b '{{COLOR_FONDO}}' f.svg -o f.png`, `magick a.png b.png +append`) y revisarlos lado a
lado: un manual puede seguir apuntando a archivos del logo anterior. Si la anatomía no tiene una fuente única,
crear una nota canónica externa (anatomía con medidas desde el JSON del rig, reglas, una ruta canónica,
archivos viejos marcados como archivados) y que manual y hoja la citen.

**Taxonomía visual dentro del manual:** cada pilar estético conserva su nombre y se explica por las técnicas
que usan sus referencias; el checklist de pieza abre con “¿qué tiene que hacer la pieza?” (operación → técnica)
antes de piel, paleta, tipo y textura/luz.
- Calcular tablas de taxonomía desde el catálogo en el build (técnicas top por pilar, ideas por uso), no a
  mano: las tablas escritas a mano derivaron del catálogo.
- No afirmar vetos, reglas “solo como contraste” ni reclasificaciones sin aprobación: proponerlas.

## La taxonomía es el método de todo el manual, aplicada ANTES de construir

Parchar bloques nuevos en páginas ya maquetadas produjo un manual “remendado” (seis tipos de tarjeta,
cuatro formas de decir “no”, tres tratamientos de icono, miniaturas recortadas, zonas muertas).
1. **Auditoría completa de director de arte:** renderizar todas las páginas (`pdftoppm -r 55`, 6 por imagen con
   `magick +append`) y preguntar a visión por recortes, bloques parchados, iconos genéricos, espacio
   desbalanceado. Mapear cada queja a una causa.
2. **Documento de dirección de arte** y parar para aprobación: qué falló + causa + cambio; la ficha del propio
   manual; un set cerrado de componentes justificado por técnicas del catálogo (grid, encabezado-con-ficha,
   UNA tarjeta, UN “así no”, marco de figura, dato, tag, icono); tabla de fichas por página; preguntas agrupadas.
3. **Cada página muestra su ficha en el encabezado**, generada desde datos.
4. **Figuras no recortadas por accidente:** obra de referencia y diagramas enteros (`contain` o recortados y
   mezclados); renders y fotos pueden llenar con `cover`. El espacio negativo se diseña a un lado.
5. Reconstruir sección por sección desde cero, revisando cada una antes de la siguiente.

## Reglas de estructura y visuales

- **Agrupar por tipo, taxonomía primero.** Manifiesto/operativo junto (fundamentos, voz y escritura); todo lo
  visual en una sección ordenada taxonomía → receta con parámetros → subpilares → lo que une/lo que no →
  repertorio → mockups.
- **Taxonomía como receta aplicable:** operación → pilar que manda → técnica de firma → una transversal →
  acabado (solo si suma) → ejecución de referencia. Defaults propuestos para aprobación: una operación manda;
  ≤ 3 técnicas; un pilar manda, nunca todos; ideas de caos solo para el “antes”; cada pieza propia recibe ficha.
- **Todo lo que puede ser visual, lo es.** Cada contenedor de texto que actúa como mini-pilar, tarjeta, paso o
  categoría lleva icono o gráfico, incluidas páginas heredadas. Páginas de filosofía → diagramas (nodo central +
  satélites, círculos para capas). Escribir la regla en el propio manual.
- **Los iconos son una ejecución de un pilar estético, nunca un UI kit.** Iconos de línea genéricos en chips
  redondeados se rechazaron como corporativos. Derivar la familia del pilar que manda, prototipar 2–3
  direcciones sobre los mismos 6 conceptos en una hoja, verificar que cada concepto tenga silueta propia a
  tamaño pequeño, aprobar antes de aplicar. Ejemplo que funcionó: bitmap 16×16 tipo fósforo + esquinas HUD +
  scanlines; wireframe isométrico solo para ilustraciones grandes; un color fijo del espectro por concepto.
- **Cambiar la familia de iconos en todo un generador:** mantener la firma del módulo viejo (`ic(nombre,c1,c2,tam)`,
  `chip(...)`, el helper usado dentro de SVG) y hacer que delegue al nuevo. Sembrar los bitmaps rasterizando los
  iconos de línea existentes a una grilla 16×16 en un canvas de Playwright (umbral ~0,30, trazo 2,3, caps cuadrados),
  revisar en una hoja, dibujar a mano solo los ilegibles como filas de 16 caracteres (assert 16×16). Verificar en
  recortes ≥ 300 dpi: a 55–110 dpi el glow difumina y visión reporta “iconos de línea suaves”.
- **Pequeñas adiciones de copy desbordan páginas llenas:** re-correr la auditoría y acortar entradas vecinas.
- **Mockups más allá del PDF en una biblioteca compañera** (HTML oscuro, filtrable por operación/pilar/uso,
  generada desde el catálogo, mockups capturados del HTML del manual con `element.screenshot()` a 3×). Reconstruirla
  en el mismo run para que los conteos no deriven.
- **Tras renombrar el descriptor**, buscar en generadores *y* en el texto extraído (`pdftotext | grep -i`): se
  esconde en la hoja, pies, copy de bumpers y láminas SVG. Las entradas históricas del changelog conservan la versión vieja a propósito.

## Verificar en la fuente el copy nuevo antes de construir

Cada frase añadida debe rastrearse a las notas fuente (manual, modelo de negocio, visión, brief, taxonomía).
Antes de renderizar, buscar cada frase clave (`grep -rlis -- "$frase" ...`); lo que no tenga coincidencia se
reescribe desde una línea con fuente o se elimina. Lo que el modelo de negocio lista como “por decidir” se
enuncia solo como lo hace esa nota. Re-correr scripts de medición antes de citar un número.

## Extender el generador con páginas nuevas

- Páginas nuevas en un módulo aparte con funciones que reciben los helpers del generador (página, abrir
  sección, h3, espaciados, figura) y un string CSS con clases prefijadas que se añade al CSS de páginas.
- Reproducir un generador archivado: copiar los `.py` del respaldo más los helpers actuales que importan,
  redirigir la salida y rutas de scripts a una copia de trabajo fuera del repositorio, inyectar `<base href=…>`
  porque el HTML usa rutas relativas. Comparar rasters de página contra el PDF archivado para probar fidelidad.
- Láminas SVG de página completa: clase `lamina` en la lista de clases sin encabezado/pie (`portada`, `contra`, `lamina`).
- Loop de build: generador + medición de láminas dos veces (las alturas convergen), generador, auditoría (buscar
  `desborde [1-9]`), render.
- Etiquetas SVG en figuras pequeñas caen bajo 9 pt en silencio: medir como fontSize × ancho renderizado / ancho del viewBox.
- Cuando cambia un conteo (p. ej. “cuatro preguntas”), buscar todas las menciones: se repite en 5+ lugares.

## Overlay de borde CRT (portada)

- PNG RGBA de página completa a 2× px CSS de A4 (1588×2246) con numpy/PIL, como capa superior absoluta
  (`pointer-events:none`, z-index sobre el contenido).
- Máscara: distancia squircle `e=(|u|^5+|v|^5)^(1/5)`, presencia `smoothstep(0.50,1.0,e)^1.35`, el centro (logo, título) intacto.
- Contenido: color del gradiente de marca recorriendo el perímetro (ángulo → paradas), alpha ≈ 0,34·borde,
  multiplicado por scanlines (cada 3 px CSS, la línea oscura conserva 25 %), esquinas oscurecidas como vidrio curvo.
- Aceptar solo tras muestrear: el píxel de borde debe diferir claramente del interior. A alpha 0,16 fue
  invisible; ~0,34 se leyó como “sutil, elegante”.

## Figuras como mini monitores CRT

- Los contenedores de figura toman texturas de la biblioteca del manual — **seleccionar por figura, nunca todas a la vez**.
- Implementar como divs overlay dentro del marco (`overflow:hidden`, redondeado, sombra interior, brillo diagonal
  tenue); el bloom va *dentro* del SVG (duplicado difuminado bajo trazos nítidos). Sin etiqueta visible que nombre las texturas.

## Ilustraciones SVG en tiles de altura fija

- `preserveAspectRatio="xMidYMid slice"` recorta el eje sobrante. Calcular la proporción del tile (ancho de
  columna / alto en mm) y fijar el viewBox a la misma proporción, con el texto ≥ 10 unidades hacia adentro.

## Índice clicable

- Cada página `<section id="pNN">`, filas del índice `<a href="#pNN">`, título del encabezado corrido enlazado
  al índice. Verificar con pypdf que las anotaciones listan `/Dest /pNN`.

## Legibilidad de diagramas (lo que la revisión de visión sigue marcando)

- Llamadas numeradas en el gráfico y los mismos números en la leyenda; el color solo no vincula símbolo y explicación.
- Cada símbolo donde su pie dice que está.
- Si un modelo es una simplificación (ciclo de 4 pasos), mostrarlo como **mapa vs. territorio** (ciclo limpio vs.
  trayectorias reales con repeticiones, saltos y retroalimentación); no presentar el ciclo como toda la verdad.
- Las líneas de leyenda no chocan con otros overlays; reservar una banda inferior.

## Reglas de copy para textos de marca

- Español llano y conversacional; evitar cadencia de IA (cadenas “No es X, es Y”, aperturas “Todo lo que X comunica…”). Frases cortas y concretas.
- Líneas escritas para iniciados se reescriben para un desconocido que lee en frío.
- Etiquetas de concepto densas necesitan una frase humana explícita y un glifo pequeño.

## Capa de identidad para video (intermisiones tipo TV)

- Receta genérica: fondo de gradiente oscuro, logo circular con relleno del gradiente de marca + glow, texto
  grande tipo “ESTÁS VIENDO” en peso 900, chips de barras de prueba, scanlines cada 3 unidades, grano
  feTurbulence ~0,08. Variantes: “estás viendo”, “ahora”, “volvemos”, zócalo.
- Para transiciones, pantallas finales y cortes de segmento; 2–5 s; nunca sobre el isotipo. Solo video, nunca impresos.
