# Conectar Composio (prioridad del setup)

**Cuándo:** en la misma sesión de instalación, en cuanto el agente responde (antes de los
módulos). Composio es el puente con las cuentas del cliente: Instagram, Facebook, Gmail, Google
Calendar y Drive, YouTube, WhatsApp Business, Meta Ads y otras. Con un solo servidor MCP, el agente
llega a todas las cuentas que el cliente autorice, sin un token distinto por app. Sin Composio, los
módulos de marca y comercial (C5 bandeja social, Meta Ads, reportes de redes) no tienen de dónde
leer.

**La cuenta es del cliente**, no de CogniLab: así las autorizaciones y los datos quedan a su nombre
y se pueden revocar sin tocar a nadie más.

## 1. El cliente crea su cuenta y su clave (a mano, 3 minutos)
1. Entra a <https://composio.dev> con su correo y abre el panel de **MCP / Connect**.
2. Copia la **API key** del consumidor MCP. Solo se ve completa una vez; si se pierde, se genera otra.

## 2. Agregar el servidor en Hermes (lo corre el cliente en su terminal)
```bash
hermes mcp add composio --url https://connect.composio.dev/mcp --auth header
```
- A «Does this server require authentication?» responde que sí. Cuando pida
  «API key / Bearer token», pega la clave: no se ve en pantalla.
- Hermes la guarda en el `.env` del perfil como `MCP_COMPOSIO_API_KEY` y en `config.yaml` deja
  solo la plantilla `Authorization: Bearer ${MCP_COMPOSIO_API_KEY}`. La clave nunca se pega en un
  chat ni en un archivo del repo.
- Al terminar ofrece activar todas las herramientas: **sí** (son pocas meta-herramientas;
  `COMPOSIO_SEARCH_TOOLS` encuentra el resto bajo demanda).
- Si hay varios perfiles: `hermes -p <perfil> mcp add ...` en el perfil que atiende al cliente.

**Si el asistente se queda colgado** (pasa cuando lo corre el agente, sin terminal interactiva), la
misma configuración a mano. La primera línea la corre el cliente; las otras tres no tocan secretos:
```bash
read -rsp "Pega tu clave de Composio y presiona Enter: " K && hermes config set MCP_COMPOSIO_API_KEY "$K"; unset K; echo
hermes config set mcp_servers.composio.url https://connect.composio.dev/mcp
hermes config set mcp_servers.composio.headers.Authorization 'Bearer ${MCP_COMPOSIO_API_KEY}'
hermes config set mcp_servers.composio.enabled true
```

## 3. Probar la conexión
```bash
hermes mcp test composio
```
Debe listar herramientas como `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_MANAGE_CONNECTIONS` y
`COMPOSIO_MULTI_EXECUTE_TOOL`. Después, reiniciar el gateway (con aprobación) o abrir una sesión
nueva para que el agente vea el servidor.

## 4. Conectar las cuentas del cliente (desde el chat con su agente)
El cliente le dice a su agente, por ejemplo, «conecta mi Instagram y mi Gmail con Composio». El
agente usa `COMPOSIO_MANAGE_CONNECTIONS`: devuelve un enlace por app, el cliente lo abre en su
navegador y autoriza con su cuenta. El agente espera con `COMPOSIO_WAIT_FOR_CONNECTIONS` y
confirma cuáles quedaron activas.

Qué conectar primero, según los módulos activos (`ACTIVOS`):
| Módulo | Cuentas |
|---|---|
| C5 bandeja social / C3 reportes | Instagram, Facebook (página), YouTube si aplica |
| B2 atención por mensajería | WhatsApp Business (si no va por el gateway), Gmail |
| A5 nube / A3 organización temporal | Google Drive, Google Calendar |
| Pauta (Meta Ads) | Meta Ads, con permiso de lectura primero |

## 5. Prueba real
Una lectura, nunca una escritura, como prueba: «¿cuáles fueron mis últimos 3 posts de Instagram?»
o «¿qué tengo mañana en el calendario?». El paso está hecho cuando el agente responde con datos
reales de la cuenta del cliente.

## Errores comunes
| Síntoma | Causa | Arreglo |
|---|---|---|
| `401` en `hermes mcp test` | Clave mal copiada o revocada | Generar otra en el panel y repetir el paso 2 (`hermes mcp remove composio` primero) |
| El agente no ve las herramientas `COMPOSIO_*` | La sesión o el gateway arrancaron antes de agregar el servidor | Sesión nueva o reiniciar el gateway |
| «No connected account» al usar una app | La app no se autorizó en el paso 4 | Pedirle al agente el enlace de esa app y autorizar |
| Una acción pide permisos que no tiene | La conexión se hizo con permisos de solo lectura | Reconectar esa app desde el agente aceptando el permiso que falta |

## Reglas
- Todo lo que publica, envía o gasta (posts, respuestas, correos, pauta) sale como borrador y lo
  aprueba el cliente. Composio da el acceso; la decisión sigue siendo humana.
- Revocar una app: desde el panel de Composio o desde la configuración de la app (por ejemplo,
  Meta → Integraciones comerciales).

## Criterio de hecho
- [ ] `hermes mcp test composio` lista las herramientas.
- [ ] Las cuentas que piden los módulos activos aparecen conectadas.
- [ ] Una lectura real respondida con datos de la cuenta del cliente.
