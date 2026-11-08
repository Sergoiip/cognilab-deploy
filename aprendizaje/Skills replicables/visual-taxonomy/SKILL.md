---
name: visual-taxonomy
description: Use when classifying visual references or briefs. Builds a technique-first taxonomy (Operación > Dominio > Técnica > Ejecución), a living catalog, a taste-driven reference corpus and a render chain that turns techniques into brand pieces.
version: 1.0.0
license: MIT
---
# Taxonomía visual (técnica primero)

## Parámetros a configurar

| Placeholder | Qué poner | Ejemplo genérico |
|---|---|---|
| `{{MARCA}}` | Nombre de la marca o cliente | «Marca X» |
| `{{DECISOR}}` | Persona que aprueba el gusto y las fases | «el director creativo» |
| `{{DIR_TRABAJO}}` | Carpeta raíz del proyecto de taxonomía (catálogo, corpus, núcleo, manual) | `./taxonomia-visual/` |
| `{{DIR_CATALOGO}}` | Carpeta con el catálogo fuente de verdad | `{{DIR_TRABAJO}}/catalogo/` |
| `{{DIR_NOTAS}}` | Base de notas donde vive la evidencia y la idea original | `./notas/marca/` |
| `{{CANON_MARCA}}` | Documento(s) con el canon de marca: personaje, mundo, facciones, paleta | «documento de lore en la nube» |
| `{{MANUAL_MARCA}}` | Manual de identidad (paleta, tipografías, elementos permitidos) | `manual-de-marca.pdf` |
| `{{PERSONAJE}}` | Personaje/mascota canónico de la marca, si existe | «mascota antropomórfica» |
| `{{MUNDO}}` | Mundo o ciudad ficticia de la marca, si existe | «ciudad ficticia de marca» |
| `{{GPU}}` | Hardware de render, para medir presupuestos | «GPU de gama media» |
| `{{VENV}}` | Entorno Python persistente para CLIP y scripts | `{{DIR_TRABAJO}}/.venv-clip` |

## Propósito
Clasificar imágenes por el **mecanismo** que usan, no por su estética, y usar esa misma clasificación para diseñar: de un mensaje a una operación, a una técnica, a una ejecución. Sirve para cualquier marca; la selección de marca va encima de una taxonomía general que no se borra.

## Cuándo usar
- Analizar referencias visuales (imagen → mecanismo).
- Convertir un brief o una idea de contenido en decisiones de diseño (brief → operación → técnica → ejecución).
- Armar un corpus de referencias por estética y destilar el gusto de `{{DECISOR}}`.
- Construir una cadena técnica → receta → universo → manual de marca, incluido un motor de render propio y un HUD.

## Entradas
- Imágenes de referencia, piezas propias de la marca o un brief.
- `{{CANON_MARCA}}` y `{{MANUAL_MARCA}}` (solo lectura).
- Opcional: herramientas de render (Blender/EEVEE), CLIP en `{{VENV}}`, un modelo con visión para revisar.

## Núcleo (4 niveles, en orden)
1. **Operación:** qué hace la imagen (Differentiate, Infer, Group, Sequence; lista abierta).
2. **Dominio:** dónde actúa (Feature, Grouping, Space, Social, Semantic, Cultural).
3. **Técnica:** mecanismo concreto y reutilizable (Semantic contrast, Complementary pairing, Contextual metaphor, Closure, Figure-ground reversal, Rim light, Color blocking, etc.).
4. **Ejecución:** ejemplos reales que prueban la técnica. Sin ejemplos, la técnica no cuenta.

Capa de uso (opcional, por marca): etiquetas transversales (idea, emoción, paleta, luz, pilar de marca, decisión: tomar / adaptar / inspiración / descartar). Van encima del núcleo, nunca dentro.

## Pasos

### 1. Catálogo vivo
- En `{{DIR_CATALOGO}}`: un `catalogo.yaml` (fuente de verdad: operaciones, dominios, técnicas, ejecuciones, sistema de etiquetas) y un script `construir.py` que regenera el catálogo de técnicas, el sistema de etiquetas y un mapa visual (p. ej. un canvas).
- Para ampliar: añade la técnica (id, nombre, original, operación, dominio, definición, origen, asignación) o la ejecución (pieza, archivo, técnicas, etiquetas, uso) y vuelve a construir.
- Marca siempre `origen` (fuente externa o propuesta del agente) y `asignacion` (observada o inferida).
- Etiquetas con formato `espacio/valor` (idea, emoción, medio, época, luz, paleta, pilar, uso). Describen ejecuciones, no definen técnicas.

### 2. Firma de la identidad
- (A) Ficha cada pieza PROPIA de `{{MARCA}}` como ejecución: brief → una operación → técnicas → por qué. De ahí sale la firma.
- (B) Diseña cada idea de contenido así: qué tiene que entender el lector → operación → técnica de la firma → gráfico. Guárdalo en un `identidad.yaml` + script.

### 3. Corpus por estética
- Cosecha por tipo de fuente (ver Reglas de decisión), revisa en una galería, ordena por gusto (parecido de imagen a lo aprobado vs. lo rechazado).
- Cuando las rondas dejan de mover la confianza, pide a `{{DECISOR}}` las **definitorias** (ejemplares que fijan la estética) con su «por qué», en una hoja numerada que responde por chat → `definitorias.yaml`.
- Descompón cada definitoria en técnicas del catálogo.

### 4. Motor (antes de cualquier filtro)
Orden de fases: taxonomía de técnicas → **motor** (personaje, sombreado, mundo, presupuesto de render) → filtros y HUD encima del motor. Plan típico: M1 personaje (canon 2D a 3D) → M2 sombreado cel → M3 mundo (lo elige `{{DECISOR}}`) → M4 modos borrador/final/héroe con s/cuadro medido → M5 escena animada de prueba. Detalle técnico: `references/motor-visual-y-hud.md`.

### 5. Cadena de render (técnica → receta → universo → manual)
Un script maestro (`construir_todo.sh`) corre: bases en Blender → laboratorio (fichas + láminas en varias dosis × bases) → recetas (réplica + rango CLIP) → universo (capas + contraste medido) → plantilla de cliente → integración al catálogo → manual en HTML → PDF con auditoría (desbordes, pt mínimo, contraste).
- **Otro cliente:** copia la plantilla de universo; técnicas y recetas no cambian.

### 6. Mundo de marca (si aplica)
1. **Canon:** lee `{{CANON_MARCA}}` en solo lectura; copia los originales a una carpeta de investigación y anota inconsistencias como preguntas, sin resolverlas.
2. **Investigación con fuentes** (en paralelo, con subagentes): método de worldbuilding (narración ambiental, elementos de Lynch, un hito visible por zona, orden de mapa por hitos, kits modulares); capa subterránea e infraestructura (megaestructuras de anime/manga, ciudades amuralladas densas, colectores pluviales); cada estética del corpus llevada a una capa del mundo.
3. **Biblia** del mundo: premisa, regla del mundo, **estratos verticales** del cielo al núcleo (más abajo = más acceso restringido), la capa de sistema como kit único en todos los estratos, la huella visual de cada facción. Marca cada afirmación como [canon], [aprobado] o [propuesta].
4. `{{DECISOR}}` aprueba la biblia → mapa en planta **y corte vertical** (HTML/SVG con las fuentes de la marca, generados desde un JSON) → renders con piezas modulares. Técnica de mockups: `references/mockups-de-mundo-en-blender.md`.

### 7. Repaso de fases
- Primero el entregable que resume la fase (un `RESUMEN-Fn.html` generado por script), luego los periféricos.
- Muestra siempre la ruta absoluta exacta de cada archivo producido o usado (entrada, script, salida, vista de revisión), con fecha.
- Los cambios de un repaso se propagan en escalera: F1 → F2 → … → Fn.

## Reglas de decisión
- La estética (Y2K, surrealismo, etc.) NO es un eje: cambia por moda. Se clasifica el mecanismo; las imágenes cuelgan de la técnica, no al revés.
- Fundamentos: Gestalt, semiótica, clasificación biológica. Afirma solo lo observado y declara límites (evidencia y limitaciones).
- La taxonomía diseña desde el mensaje; **no es un reglamento de maquetación**: no conviertas técnicas en reglas tipográficas ni en etiquetas de página. La legibilidad es condición de cada ejecución, no una capa aparte.
- Lo que fija `{{DECISOR}}` (definitorias) manda sobre el conteo de imágenes; contar solo propone.
- Los elementos visuales de marca son solo los que entran en `{{MANUAL_MARCA}}` + `identidad.yaml`, no un catálogo general.
- Un solo catálogo: no lo partas en «anteriores/nuevas» por cómo se programó (se lee como descarte).
- Separa **taxonomía general** (conserva todo, replica cualquier estética) de **selección de marca** (sacar algo de la marca no lo borra del catálogo).
- Dos niveles de salida: **render** (universo de marca, sobre todo video) y **pieza** (carrusel, historia, PDF). Capas de un render: Mundo · Sistema · Shader.
- La capa **Sistema** (infraestructura: cables, conductos de luz, rieles elevados, registros abiertos, terminales, maquinaria en corte) atraviesa TODO el mundo: suelo, fachadas, cielo. Nunca la conviertas en un barrio o un hito aparte.
- Cada técnica es capa / construcción / escena; las de construcción se descomponen en sub-técnicas geométricas con `madre`. Fusiona estéticas que son subconjuntos (p. ej. una estética de consola dentro de Y2K).
- Toda técnica lleva columna **«vive en»**: Mundo (geometría/material) · Cámara (posproceso por cuadro) · Pantalla (HUD sobre la escena) · Pieza (maquetación 2D HTML/SVG). Escena = Mundo→Cámara→Pantalla; pieza = cuadro del motor o fondo → componentes → texto. **Una pieza nunca es un filtro sobre una foto.**
- Muestra cada técnica en su vertiente (escena sobre cuadros del motor, pieza en maquetas reales), nunca sobre bases genéricas inventadas.
- Las técnicas de escena NO se fingen con filtros 2D: quedan con ficha pendiente hasta que exista el motor. El cel-shading es render 3D, no filtro.
- El HUD/interfaz debe ser **reactivo**: cada elemento lee la imagen o la escena de debajo; colocado al azar se ve pegado.
- **Antes de construir personaje o mundo, recupera el canon** (`{{PERSONAJE}}`, `{{MUNDO}}`), no lo inventes. La fuente de verdad es siempre la más reciente. Versiones antiguas del personaje no se usan.
- Si las referencias traen colores fuera de la paleta de marca, retíñelas y márcalo como pendiente para `{{DECISOR}}`. No lo resuelvas en silencio.

### Fuentes por tipo (corpus)
- Idents y bumpers de TV: compilaciones de canales generalistas; las de canales de animación traen metraje de series.
- Degradados mesh: fondos «animated 2D gradient» (lo «liquid/hydrochrome» suele no servir).
- Íconos: sets reales con licencia libre renderizados como láminas, no fotos.
- Estéticas de época: fotogramas de ensayos en video y compilaciones de comerciales de la época.
- **Identifica la fuente de una definitoria antes de cosechar** (visión: «¿de qué juego o medio es?»); los longplays de ese medio rinden más que buscar por nombre de estética.

## Verificación
- Cada técnica del catálogo tiene al menos una ejecución real, `origen` y `asignacion`.
- El manual: texto siempre en HTML (nunca dentro de imágenes) para que la auditoría mida tamaño y contraste reales; 0 desbordes; después, revisión de hojas de contacto con visión.
- Fidelidad mínima = la de las definitorias: arma una hoja de contacto con ellas y compara antes de renderizar.
- No afirmes una propiedad visual («terminador duro», «se ve el trazo») sin medirla en píxeles.
- Revisa mapas densos con visión sobre un recorte de la zona densa, no sobre la imagen completa.

## Pitfalls
- **El filtro semántico (texto→CLIP) no decide el gusto y puede esconder la dirección buena.** En un caso escondió 17 de 18 imágenes de la página de la estética que se buscaba. No pases por CLIP de texto las fuentes curadas por humanos (wikis de estéticas). Tras la primera revisión, ordena por parecido de imagen a lo aprobado/ejemplar contra lo rechazado (`filtro_gusto.py`).
- **Ancla en la página núcleo:** las páginas hermanas de una wiki traen ruido; ordénalas por parecido a la página núcleo validada.
- **Galería de revisión:** cada input necesita `name` único y `autocomplete=off`, o el navegador restaura comentarios en otras imágenes al regenerarla.
- **Filtros idempotentes:** que partan siempre del conjunto completo (pendientes + aprobadas + rechazadas + ocultas). Una corrida que leyó solo lo pendiente borró decisiones. Respalda (`candidatas.*.json`) antes de cada filtro.
- Los entornos en carpetas temporales pueden borrarse solos: usa `{{VENV}}` persistente.
- Cuadros de video: junta casi duplicados (coseno CLIP > .93; los degradados necesitan .985). Saca los de presentador o hardware con CLIP cero-shot antes de mostrarlos.
- **Probar filtros antes de tener motor** da láminas «filtro sobre foto genérica» que se rechazan: el decisor no juzga la técnica, juzga la base.
- **La auditoría numérica no ve fealdad:** una placa negra en una base (cara de edificio sin ventanas) contaminaba todas las recetas; se arregla en el render, no en cada pieza.
- **El posproceso no cambia de qué trata la imagen:** recetas de luz y trazo replican bien; estéticas de objeto/escena (Y2K, consola de época, estéticas corporales) necesitan base propia.
- Hueco en la última página de una grilla: llénalo con una tarjeta de leyenda.
- No uses «Debajo» ni «Identidad» como nombres de capa: los idents de TV son renders del Mundo.
- Valores de YAML con «: » dentro van entre comillas o se vuelven dict.
- Inventar nombres simbólicos o metáforas para el mundo («la ciudad es una mente») se rechazó por cursi; lee el canon antes de nombrar nada.
- Cajas con ventanas pintadas quedan «muy bajo detalle» frente a las definitorias: el mundo se arma con piezas modulares detalladas.
- Una técnica de trazo de 1 px sobre una máscara pequeña «no se ve» aunque se dibuje: mide qué fracción de píxeles cambia antes de reescribirla.
- Cel-shading de terminador duro: cáscara de casco invertido con `use_backface_culling_shadow=True` (si no, tapa el sol al cuerpo) y rampa CONSTANT sin Noise. Mide el área cubierta por los 2 tonos principales (objetivo ≥90 %).

## Variantes
- **Solo análisis:** usa únicamente el núcleo de 4 niveles + catálogo; sin corpus ni motor.
- **Solo piezas 2D:** núcleo + firma de identidad + técnicas de vertiente Pieza (HTML/SVG); salta motor y mundo.
- **Marca sin personaje ni mundo:** omite pasos 4 y 6; las técnicas de escena quedan en la taxonomía general.
- **Nuevo cliente sobre una cadena existente:** copia la plantilla de universo; técnicas y recetas se reutilizan tal cual.

## Implementación de referencia
Una implementación previa aplicó esto a una marca con **estética retrofuturista con HUD** y **una ciudad ficticia de marca**:
- Corpus de varias estéticas (cyberpunk, Y2K, neo-Frutiger Aero, mesh, idents de TV, interfaces de sistema, estéticas corporales); el gusto del decisor era: nada muy realista, abstracto y estilizado, «futurista pero nostálgico», sin kawaii ni capturas de UI real. Las definitorias revelaron un universo por capas, no estéticas en paralelo.
- Motor en Blender/EEVEE con cel-shading como base (lenguaje de videojuego cel-shaded de época), animación en dos, look final 480p + VHS para escenas y 4:3 + CRT para idents/pantallas.
- Mundo con cúpula como cielo, estratos verticales, facciones con huella visual, una red LED que recorre la ciudad portando los degradados mesh, y capa subterránea explícita.
- El personaje 3D no se aprobó tras varias direcciones de proporción: en el manual se usa el canon 2D con la nota «en rediseño». No rediseñes a ciegas sin un dibujo de rediseño aprobado.
- Manual de marca generado en HTML → PDF con auditoría.

Referencias técnicas:
- `references/motor-visual-y-hud.md` — motor de render, tinta en posproceso, velocidad, look de época, pipeline F3–F7 y veredicto por elemento de HUD.
- `references/mockups-de-mundo-en-blender.md` — pipeline y lecciones para mockups de ciudad/mundo.

Origen: abstraída de una skill interna de taxonomía visual (2026-11).
