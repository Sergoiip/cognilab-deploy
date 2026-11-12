# Obsidian Git

**Versión del catálogo:** 2.42.0 · MIT · repo Vinzent03/obsidian-git

## Metodología (según el plugin)
Lleva Git a la bóveda: commit, pull y push automáticos con un intervalo, auto-pull al abrir Obsidian, vista de control de cambios, historial, diferencias línea a línea y resolución de conflictos dentro del editor.

## Recomendación CogniLab
- **Un repositorio privado por bóveda.** Es el respaldo y el historial de cambios.
- **Commit y sincronización automáticos cada 10 a 30 minutos** y auto-pull al abrir. Si el cliente trabaja en dos equipos, esto evita conflictos.
- **Antes de un cambio grande** (reorganizar carpetas, plantillas, scripts) hacer un commit manual con mensaje. Es el punto de retorno.
- **`.gitignore` obligatorio:** `.obsidian/workspace*.json`, carpetas de caché y cualquier archivo con claves o credenciales.
- Enseñar al cliente a leer el historial: es la forma más simple de que confíe en que nada se pierde.

## Cuidado
- **Nunca** guardar contraseñas, tokens ni claves de API en la bóveda. Si entran en el historial, borrar el archivo no las quita.
- En móvil el propio plugin avisa que es inestable. No prometer sincronización móvil con él.
- No es copia de seguridad fuera del equipo hasta que exista el remoto (GitHub u otro).
