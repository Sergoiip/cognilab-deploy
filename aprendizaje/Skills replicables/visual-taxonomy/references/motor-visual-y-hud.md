# Motor visual y HUD: técnica y lecciones

## Personaje del motor
- **Canon primero:** parte de las hojas del canon de `{{PERSONAJE}}` (de frente, de lado, poses, rediseño). El canon manda sobre reglas genéricas de estilo. Las versiones antiguas del personaje no se usan.
- **Modelo:** piezas rígidas emparentadas a huesos, segmentadas estilo consola de época (sin pesos). Cara pintada en texturas por expresión generadas por script. Funciones: `construir()`, `pose()`, `caminar()`, `expresion()`.
- **Validación:** compara silueta del render contra la máscara del canon (IoU) + nota de visión. Para la máscara del canon, rellena huecos (p. ej. con scipy): prendas oscuras se confunden con el fondo y sin relleno salen piernas «vacías» (IoU falso).
- No rediseñes a ciegas: pregunta qué molesta o parte de un dibujo de rediseño aprobado. Mientras no se apruebe el 3D, el manual usa el canon 2D con la nota «en rediseño».

## Lecciones del motor (Blender EEVEE)
- **Contorno:** Freestyle no escala a una ciudad (se cuelga en «too many occluding levels»). Haz la tinta en posproceso: render de color + pases con material de reemplazo: **View Z Depth** (no View Distance, que tiñe el suelo) y normal codificada como n·0,5+0,5 (si no, la emisión recorta los negativos).
  - Borde = laplaciano de 1/z + quiebre de normales.
  - En los pases de datos apaga DOF, niebla y AA. Con primer plano desenfocado, anula la tinta cerca (`dmin`).
- **Exportar:** en versiones recientes, `MULTI_LAYER_IMAGE` + `OPEN_EXR_MULTILAYER` puede no guardar Z ni Normal; por eso se usan pases con material de reemplazo.
- **Niebla:** un volumen de mundo en EEVEE se come el cielo. Usa un cubo con Principled Volume y `visible_shadow=False`, y apaga `use_volumetric_shadows`, o se pierden las sombras.
- **Cúpula/techo de cielo:** como geometría le tapa el sol a la escena: `visible_shadow=False` en ella y sus costillas. Desde la calle, el cielo se lee como techo solo con costillas en geometría que convergen en perspectiva, no con textura.
- **Animación «en dos»** (12 poses/s → 24 fps): mitad de costo y lenguaje de anime/videojuego cel. Video final AV1 10-bit + audio PCM en MP4.
- **Encuadre:** no preguntes a la visión «¿se ve bien?»; pregunta «¿está el personaje en cuadro?». En un plano que sube hacia un objetivo, calcula la mira como el ángulo medio entre la cabeza del personaje y el objetivo.
- **Corredor de rodaje:** una variable que excluya utilería y peatones del recorrido de cámara.
- **Velocidad:**
  - Un solo pase de datos en un EXR: R = normal.x, G = normal.z, B = View Z Depth; borde de normales como distancia entre normales.
  - `render.use_persistent_data = True`.
  - Por debajo de ~1 s/cuadro el costo es la carga de la escena + los renders por cuadro: el siguiente paso es prerrenderizar el fondo en planos de cámara fija.
- **Look de época (480p):** texturas con interpolación Closest y escalado a 1080p en la capa de cámara. Se leen como época intencional 480 + VHS (aberración, scanlines) y 640×480 4:3 + máscara CRT. El escalado en bloque sin capa de cine se lee como «baja calidad»; 240p, como degradado.
- **Recorrido de distritos:** una panorámica por bloques de color se lee como maqueta, no como plano bonito.
- **Matriz «vive en»:** calcúlala desde las fichas de técnicas + un registro explícito de lo que implementa el motor. Al agregar una técnica al mundo, regístrala ahí.

## Decisiones típicas de look (patrón)
- Un look principal para escenas (p. ej. 854×480 Closest + bilineal + bloom amplio + VHS + aberración + scanlines).
- Un look complementario para idents y pantallas (p. ej. 4:3 + CRT).
- El render final a 1080p sin capa de época es la **referencia de cada elemento aprobado**.
- Si explorar el mundo se alarga, prioriza llegar al manual.

## Pipeline F4–F7
- **F4 HUD:** compón sobre cuadros del motor con un JSON de rastreo (proyecta cabeza, pie, cuadriláteros de anuncios y vehículos con `world_to_camera_view`).
  - Para que la interfaz «viva en la pantalla», aberración y scanlines van DESPUÉS de componerla; antes, se lee pegada.
  - Paneles oscuros detrás de barras y registros; elige la esquina más oscura.
  - Un rótulo bilingüe debe agregar información, no repetir el texto del anuncio.
- **F5 láminas:** las bases son los distritos donde vive cada estética; las de Mundo son evidencia del render del motor. Módulos importables con guard `__main__`.
- **F6 recetas:** mide sobre el motor; las estéticas sin distrito propio construido quedan lejos de rango.
- **F7 manual:** HTML + CSS → PDF con auditoría (desbordes, pt mínimo, contraste).
  - Láminas compuestas con texto adentro son ilegibles en PDF: arma comparaciones en HTML (imágenes sueltas + figcaption + chips).
  - `figure img` necesita `max-width:100%`.
  - Textos de planos y cortes del mundo ≥36 px en un PNG de 2560 para leerse en A4 apaisado.

## Interfaz de sistema: veredicto por elemento (patrón de revisión)
| Elemento | Decisión típica |
|---|---|
| franjas-de-peligro | puede quedar fuera de la marca (se conserva en la taxonomía general) |
| marco-de-esquinas | uso secundario |
| barras-de-estado | animadas y con valores leídos de la escena o la imagen |
| mira-de-blanco | rehacer desde sus referencias; que siga objetos reales |
| dial-polar | si no se entiende: explicar mejor o retirar |
| rotulo-bilingue | dinámico, colocado según la composición |
| color-por-funcion | principales + complementaria + funcionales, con tabla de significados |
| oscilograma | reactivo: audio de la pista o perfil de luz del cuadro |
| registro-hex | reactivo: valores reales de píxel o coordenadas |
