---
name: bandeja-social-respuestas-composio
description: Use when answering IG/YouTube DMs or comments via MCP.
version: 1.0.0
---

# Bandeja social (comentarios + DMs) vía Composio MCP

**Propósito:** leer, clasificar y responder comentarios y mensajes directos de Instagram y YouTube con herramientas en vivo, con aprobación del dueño de la cuenta salvo reglas permanentes explícitas.

## Configuración que debe fijar el cliente (en su perfil o notas del agente)
- **Cuenta de Instagram** que se atiende (el handle de la marca del cliente).
- **Variable de entorno con la clave MCP** de Composio (por convención `COMPOSIO_API_KEY`, guardada en el `.env` del agente).
- **Frase de derivación**: respuesta fija para consultas de precio/información, que remite al canal de mensajería donde se atienden leads (por ejemplo, el WhatsApp del negocio).
- **Canal de contacto** al que se deriva y quién lo opera (el propio negocio o un tercero).
- **Página oficial de precios** del cliente (si la tiene).
- **Cuentas excluidas**: hilos que van en un cubo aparte y no se responden automáticamente.
- **Horario del barrido recurrente**: por defecto, uno diario al final de la jornada; configurable vía cron.
- **Destino de los resultados**: el tablero de tareas del agente (por ejemplo, Kanban) para aprobación.
- **Dónde registrar leads**: el CRM o la bóveda del cliente.

Si alguno de estos datos falta, preguntarlo antes de responder nada en nombre de la marca.

## Preparación
- Servidor MCP `composio` (`https://connect.composio.dev/mcp`, cabecera `x-consumer-api-key`, secreto en el `.env` del agente). Añadir con `hermes config set` (el asistente interactivo se cuelga en su prompt de auth). Verificar con `hermes mcp test composio`.
- La clave del panel `ck_` es de consumidor/MCP, no de SDK.
- Conectados típicamente: Instagram y YouTube (un 403 en `mine:true` indica permiso de canal faltante). TikTok no tiene auth gestionada (solo publica/lista estadísticas, sin comentarios/DMs).
- Regenerar cualquier clave pegada en el chat al terminar.

## Procedimiento interactivo
1. `COMPOSIO_SEARCH_TOOLS` (sesión `generate_id`) → `COMPOSIO_GET_TOOL_SCHEMAS` por slug → `COMPOSIO_MULTI_EXECUTE_TOOL`. Leer el esquema antes de ejecutar: fallos repetidos pausan el servidor alrededor de un minuto.
2. Comentarios: `INSTAGRAM_GET_IG_USER_MEDIA` → `INSTAGRAM_GET_IG_MEDIA_COMMENTS` por media id → `INSTAGRAM_POST_IG_COMMENT_REPLIES` (≤300 caracteres, ≤4 hashtags, ≤1 URL, sin mayúsculas sostenidas).
3. DMs: `INSTAGRAM_LIST_ALL_CONVERSATIONS` (`fields=id,updated_time,participants,messages.limit(4){message,from,created_time}`) → `INSTAGRAM_SEND_TEXT_MESSAGE`. Las respuestas solo funcionan dentro de las **24 h** del último mensaje del cliente final: indicar qué hilos califican y dar texto para copiar-pegar del resto.
4. Triage: tabla (usuario, texto, post/fecha) + respuesta propuesta por hilo; agrupar preguntas idénticas. Publicar SOLO lo aprobado.
5. Ofrecer registrar como lead a quien pregunte precio/info.

## Barrido diario (solo lectura)
- Invocar herramientas Composio vía `tool_call`/búsqueda de herramientas; pasar el `session_id` devuelto por SEARCH_TOOLS.
- Para barridos, usar celdas pequeñas separadas de `COMPOSIO_REMOTE_WORKBENCH` (DMs, lista de media, comentarios por media, YouTube) en lugar de una celda gigante: falla sin detalle si se junta todo.
- Un hilo requiere respuesta si el último mensaje NO es de la marca y está dentro de 24 h. Texto vacío = adjunto/story: "revisar en app". Autorespuestas propias y cuentas excluidas van a cubo aparte.
- YouTube: un 403 puede ser cuota diaria (`quotaExceeded`), no falta de permiso — leer el cuerpo del error.
- `username` suele venir nulo en comentarios: agrupar por post/tipo de pregunta, no por handle.
- Dejar el resultado como tarjeta en el tablero de tareas configurado para aprobación del dueño de la cuenta.

## Envío (verificado)
- `recipient_id` = `from.id` del último mensaje del cliente final. `INSTAGRAM_SEND_TEXT_MESSAGE` devuelve `message_id` si funcionó. Respuestas a comentarios con `INSTAGRAM_POST_IG_COMMENT_REPLIES`; traer los comentarios de nuevo justo antes de enviar para no duplicar.
- Trabajo recurrente (cron): si el dueño autorizó autorrespuesta sin aprobación previa, limitarla a DMs en ventana y comentarios de precio/info; lo demás se lista con texto sugerido.

## Reglas de contenido
- **Regla permanente configurable:** a consultas de precio/info se responde exactamente la frase de derivación configurada, remitiendo al canal de contacto. Prima sobre cualquier otra guía.
- Nunca enviar sin aprobación explícita del texto exacto, salvo la regla permanente.
- Precios (fuera de la regla permanente) solo desde la página oficial de precios recién consultada (curl, sin caché); nunca de memoria.
- Respuestas en el idioma de la audiencia, cortas, con una pregunta de vuelta para calificar. Nunca inventar descuentos.

## Verificación
Informar éxito por respuesta (message_id / reply id); volver a listar para confirmar que no quedan pendientes en ventana.

## Errores comunes
Responder fuera de ventana de 24 h; confundir cuota de YouTube con permisos; celdas gigantes en el workbench; contestar por handle nulo; citar precios de memoria.

## Variantes
- Facebook/Messenger o LinkedIn: misma estructura, cambian slugs y ventana de mensajería.
- Sin Composio: Graph API de Instagram con token propio, mismas restricciones.
- Con CRM: cada pregunta de precio crea un lead automáticamente.
