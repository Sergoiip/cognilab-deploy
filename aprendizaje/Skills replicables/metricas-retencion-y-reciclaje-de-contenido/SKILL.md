---
name: metricas-retencion-y-reciclaje-de-contenido
description: Use when analyzing retention metrics or recycling a reel.
version: 1.0.0
---

# Métricas de retención y reciclaje de contenido ganador

## Cuándo usarla
Leer retención real (no solo vistas/likes) en Instagram/YouTube/TikTok para saber dónde se
pierde la audiencia, o reutilizar un video ganador como variantes nuevas sin grabar de nuevo.

**Propósito:** leer retención real, detectar dónde se pierde la audiencia, y reutilizar los
videos ganadores como variantes nuevas **sin grabar de nuevo y sin perder calidad de origen**.

## 1. Qué métrica da cada fuente
- **Instagram por reel (Graph API):** `views, reach, saved, shares, ig_reels_avg_watch_time` (ms),
  `reels_skip_rate` (% que abandona en los primeros 3s), `ig_reels_video_view_total_time`.
- **Instagram cuenta:** insights `metric_type:total_value` para reach/profile_views/website_clicks.
- **YouTube:** la API de Analytics (`channel==MINE`, dimensión `video`, métricas
  views/averageViewDuration/averageViewPercentage) solo aparece tras reautorizar OAuth con scope
  de analytics; antes solo hay conteos de la Data API. `averageViewPercentage > 100` = repeticiones.
- **TikTok:** la retención no se expone vía API pública; usar capturas/export de TikTok Studio.

## 2. Patrón de análisis
Ordenar por tiempo medio de visualización, skip rate, y (guardados+compartidos)/alcance —
guardados y compartidos señalan intención real, no solo entretenimiento. Un skip rate alto
(~50%+) en los mejores videos indica que el hook (primeros 3s) es la palanca a mejorar primero.
Decir explícitamente qué no se pudo leer en vez de adivinar un número.

## 3. Calidad de fuente para reciclar (el hallazgo clave)
- La `media_url` de la Graph API de Instagram es **solo** la transcodificación a 720p — no sirve
  para reciclar. Verificar siempre con `ffprobe` antes de usar cualquier archivo
  (resolución/bitrate reales).
- Fuentes de calidad real: (a) exportación oficial "descarga tu información" de la cuenta (solo
  la puede pedir el titular, calidad "Alta"); (b) material en bruto original (cámara/disco); (c)
  el archivo final exportado en 4K antes de subirlo a la plataforma.
- Si no hay acceso al material original: no bloquear — trabajar con la mejor copia disponible,
  decir explícitamente qué pérdida de calidad implica.
- Hacer una hoja de contactos de la fuente antes de planear variantes
  (`ffmpeg -vf fps=1/4.5,scale=270:-1,tile=6x2 -frames:v 1`).

## 4. Plan de reciclaje
Por cada video ganador, 2-3 variantes ligeramente distintas (plano de apertura diferente, 1-2
cortes reordenados, otra música, reencuadre, tarjeta de hook distinta) manteniendo voz y mensaje
intactos. Mostrar siempre antes de publicar nada — nunca auto-publicar reciclaje.

## Pitfalls
- Reciclar desde la copia 720p re-descargada de la plataforma.
- Interpretar un skip rate sin saber que solo mide los primeros 3 segundos.
- Confundir correlación con causa en una muestra pequeña de posts.

## Variantes
- Podcast/entrevista: sustituir "reel ganador" por "clip ganador de un episodio largo"; mismas
  reglas de calidad de fuente.
- Sin acceso a API: trabajar con capturas/CSV exportados nativamente de cada plataforma.
