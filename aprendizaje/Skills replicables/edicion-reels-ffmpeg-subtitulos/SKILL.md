---
name: edicion-reels-ffmpeg-subtitulos
description: Use when burning ffmpeg captions/SFX into reels.
version: 1.0.0
---

# Edición de reels con ffmpeg (subtítulos, mezcla de audio, logo)

## Cuándo usarla
Necesitas subtítulos animados palabra-por-palabra, SFX, música de fondo mezclada y un logo de
cierre quemados en un video vertical (9:16), sin depender de un editor SaaS (CapCut, Opus Clip)
con límites de minutos/créditos ni de un NLE con GUI.

**Propósito:** producir lotes de reels verticales con subtítulos automáticos, mezcla de
voz/música/SFX y marca, renderizados con ffmpeg. Es un pipeline de "último kilómetro" para
shorts/reels, no para edición narrativa con cortes complejos (para eso, un editor con GUI como
DaVinci Resolve).

## Requisitos
ffmpeg, Python con `faster_whisper`, Pillow (para medir texto).

## Paso previo: fuentes decodificables
Clips HEVC 10-bit 4:2:0 a resoluciones altas pueden fallar o verse solo con audio en algunos
editores/reproductores. Comprobar con `ffprobe`; si hace falta compatibilidad amplia,
transcodificar a una subcarpeta `convertidos/` (dejando el original intacto) con
`libx264 -crf 16 -pix_fmt yuv420p -tag:v avc1 -c:a copy -movflags +faststart`. Si el pipeline
habitual ya usa un códec moderno (ej. AV1 NVENC), usarlo directo en vez de este transcode
intermedio.

## Pipeline
1. **Transcribir** con `faster_whisper` (`WhisperModel("small", device="cpu", compute_type="int8")`,
   `word_timestamps=True`, `vad_filter=True`); guardar tiempos por palabra en JSON. Mantener una
   lista de correcciones por regex para términos propios (nombres de marca, jerga técnica) que el
   modelo suele transcribir mal.
2. **Corregir** la transcripción contra la lista de términos propios; listar los términos
   inciertos para confirmación humana.
3. **Subtítulos (.ass):** un archivo por clip (PlayRes 1080×1920), centrados a la altura del
   pecho (Alignment 2, MarginV ~650 en 1920 de alto) para no tapar la cara — nunca texto sobre la
   cara. Fuentes en `fonts/` + `fontsdir=`. Colores ASS en formato BGR.
4. **Animación de subtítulos (receta probada):**
   - Frases de máx. 3 palabras (corte por puntuación o pausas > 0.45s), sin cajas, mayúsculas.
   - Palabra clave por frase en el color de marca, más grande; resto en blanco con contorno.
   - Un `Dialogue` ASS por palabra con `\move` + `\fad` + escala 88→100%.
   - **Medir con PIL** (`ImageFont.truetype(...).getlength(txt)`) para centrar cada frase en vez
     de dejar que libass centre cada palabra por separado (se desalinea).
   - Terminar cada frase en `fin_última_palabra+0.12`, tope en `inicio_siguiente-0.04`.
5. **SFX** sintetizados con `wave`/`math` (whoosh = ruido filtrado con envolvente senoidal; pop =
   barrido senoidal decreciente; ding = dos senos decrecientes) solo en momentos clave (inicio,
   dato destacado, firma/gancho). **Nunca sincronizar SFX palabra a palabra** (se rechaza
   visualmente). Mezclar con `adelay` por evento + `amix=normalize=0` + `alimiter`.
6. **Música de fondo** libre de derechos (preferir CC0 sobre CC BY). Mezcla: `atrim` a duración,
   fades, voz con `asplit` + `sidechaincompress` activado por la voz (calibrar midiendo — un
   ratio/threshold mal puesto deja la música inaudible o tapando la voz).
7. **Cadena de mejora de voz:** `highpass=f=90, afftdn=nf=-28, acompressor=threshold=-20dB:ratio=3,
   equalizer (-2dB@250, +3dB@3500), loudnorm=I=-14:TP=-1.5`. Ojo: `afftdn` + `loudnorm TP=-1.5`
   agresivos pueden comerse las sibilantes finales; si se detecta, usar
   `highpass=f=80, acompressor ratio=2, loudnorm TP=-1.0` y comprobar con RMS sobre 5kHz en los
   últimos 0.5s.
8. **Marca:** logo con placa blanca redondeada tras el gancho, visible los últimos ~2s. Con
   `-loop 1` en el PNG, siempre fijar `-t <duración>` en la salida o el proceso nunca termina.
9. **Render** en una sola llamada: `scale=1080:1920` + `subtitles='<ass>':fontsdir='<fonts>'`,
   libx264 (o el encoder habitual) crf 18–20, audio AAC, `+faststart`.
10. **Probar UN clip primero** (3 fotogramas en hoja de contactos + 1 a tamaño completo) antes
    del lote completo.

## Verificación por medición (no por ojo)
Renderizar el `.ass` solo sobre negro y medir con `ffmpeg -f lavfi color=black ... -vf
"subtitles=...,format=gray"`: umbral de píxeles encendidos para detectar texto fuera de cuadro,
y que eventos consecutivos no se solapen más de 1 fotograma.

## Pitfalls
- Sincronizar SFX palabra a palabra.
- Escala/caja heredadas de una plantilla de texto genérica.
- Cadena de voz que se come sibilantes.
- Música mal calibrada (demasiado alta o inaudible).
- Medir sonoridad final tras mezclar, no antes (-11 LUFS suele salir "caliente", objetivo social
  ≈ -14).
- Generar cadenas `.ass` por heredoc/replace corrompe los escapes `\n`/`\:`: construir el bloque
  de estilos con `chr(92)` y validar con `ast.parse` antes de ejecutar.
- Si se usa faster-whisper directo, puede haber conflictos de versión con el paquete `av`;
  fijar una versión compatible si la instalación falla.

## Variantes
- Sin GPU: todo el pipeline es CPU-only salvo que uses un encoder acelerado disponible (NVENC si
  hay GPU NVIDIA).
- Volumen bajo de clips (1-2 sueltos): subtítulos manuales en un NLE con GUI pueden ser más
  rápidos que montar el pipeline completo.
- Otro idioma: cambiar `language` y el glosario de correcciones.
