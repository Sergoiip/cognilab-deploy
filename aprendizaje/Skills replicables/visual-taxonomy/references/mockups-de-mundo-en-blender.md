# Mockups de mundo en Blender (técnica y lecciones)

Pipeline: `trazado.py` → `mundo.json` (un solo trazado para mapa y renders) → `mundo_mockup.py` (Blender EEVEE, `-- json salida escena estilo`) → `camara.py` (posproceso con las recetas de técnicas) → `hoja.py` (hoja de contacto HTML). Un `mockups.sh` corre todo. Referencia: 1–8 s por cuadro 1600×900 en `{{GPU}}`.

- Recalcula las normales (`bmesh.ops.recalc_face_normals`) antes del casco invertido (Solidify con flip y backface culling). Con mallas armadas a mano en `from_pydata`, el casco no se ve y la visión dice «sin contorno».
- Comprueba que ninguna cámara quede dentro de un edificio: un vidrio translúcido alrededor de la cámara lava toda la imagen (todos los percentiles por encima de 190). Haz que el script aborte si pasa.
- El hito héroe tiene que ser lo más alto de su entorno. Limita la altura de los vecinos con la distancia al hito, o la pantalla queda tapada.
- Un decal en un plano vertical debe mirar hacia afuera: `rot = atan2(ny, nx) + pi/2`. Si no, el texto sale en espejo.
- La niebla dentro del material se escala con la distancia cámara→objetivo de cada escena; con valores fijos, los planos cercanos y la panorámica no pueden compartir el mismo estilo.
- El dither de cámara borra el texto en 3D. No lo uses en escenas con rótulos.
- Pregunta a la visión por un elemento concreto («¿hay una pantalla con un personaje? ¿dónde?»). Las críticas generales mezclan problemas reales con detalles inventados.
