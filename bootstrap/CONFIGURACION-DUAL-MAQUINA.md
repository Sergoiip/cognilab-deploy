# Configuración dual: dos equipos, un solo agente

Para cuando un cliente tiene **dos máquinas** y quiere un solo agente — ej. un Linux que queda
siempre encendido (servidor) y un equipo más potente (Mac, otro Linux, lo que sea) que se usa
cuando está prendido, con programas/GPU propios que el servidor no tiene.

**Principio:** un solo gateway es dueño del perfil (sesiones, memoria, skills). El otro equipo
es siempre **cliente** de ese gateway — nunca corre su propia copia del mismo perfil. Lo único
que puede cambiar según el equipo es **dónde se ejecutan las herramientas** (terminal backend),
no dónde vive la memoria.

## Caso típico: ya hay algo configurado en un equipo, el otro está vacío

Ej.: Hermes ya quedó parcialmente configurado en una Mac, y el Linux (el que va a quedar
siempre encendido) todavía no tiene nada. Se migra TODO lo de la Mac al Linux, una sola vez:

### 1. Exportar el perfil de donde ya está configurado
```bash
# En la máquina que ya tiene el perfil (ej. la Mac)
hermes profile export <perfil> -o cliente.tar.gz
```
Empaqueta skills, memoria, persona, crons, plugins y config — **sin** API keys ni `.env`
(se excluyen siempre, por seguridad). También disponible como `/export` en el chat, o
**⌘K → Export profile…** en el Desktop.

### 2. Importar en la máquina que va a ser el servidor 24/7
```bash
# Pasar cliente.tar.gz al Linux (scp, USB, lo que haya) y ahí:
hermes profile import cliente.tar.gz --name <nombre>
```
No se puede importar como `default` — usar `--name`. Volver a poner las API keys
(Anthropic/Codex/lo que usen) a mano en el `.env` del Linux; no vienen en el export.

### 3. Apagar el gateway de la máquina de origen para ese perfil
```bash
# En la máquina de origen (ej. la Mac) — para que no sigan dos historiales en paralelo
hermes gateway stop
```
Si quedó instalado como servicio (LaunchAgent/systemd), desinstalarlo para ese perfil con
`hermes uninstall` del lado del gateway, no solo `stop` — si se reinicia la máquina y el
servicio se vuelve a levantar solo, se bifurca la memoria sin que nadie lo note.

## Levantar el servidor 24/7 (el que se queda siempre encendido)

Ver también `bootstrap/INSTRUCCION-HERMES.md`. Resumen:
```bash
curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up   # en AMBOS equipos
hermes gateway install && hermes gateway start                          # en el servidor
hermes config set platforms.api_server.host <ip-tailscale-del-servidor>
```
Fijar usuario/contraseña del backend (o `HERMES_DASHBOARD_BASIC_AUTH_SECRET`) para no pedir
login en cada reinicio. **Nunca** enlazar a todas las interfaces (bind-all) expuesto directo a
internet — Tailscale es la opción limpia, documentada por Hermes mismo para este caso exacto.

## Conectar el otro equipo como CLIENTE — Desktop y terminal, las dos

- **Desktop:** `Settings → Gateways → Add connection → Remote gateway` → URL del servidor +
  login. Queda guardado **por perfil** — no hay que repetirlo cada vez; cambiar de perfil
  cambia solo a qué gateway apunta esa ventana.
- **Terminal:** en el `.zshrc`/`.bashrc` del equipo cliente:
  ```bash
  export HERMES_TUI_GATEWAY_URL="http://<ip-tailscale-del-servidor>:9119"
  ```
  Así `hermes` / `hermes chat` desde esa terminal también se conecta al gateway remoto en vez
  de levantar uno local — la documentación lo marca explícito: *"An explicit
  HERMES_TUI_GATEWAY_URL remains remote-only: failed connection or authentication never
  launches a local replacement."*

**Por qué esto resuelve "que lo que se haga en un equipo se guarde en el otro":** el gateway
remoto no es una copia — es el mismo proceso. *"Opening an agent dials its own gateway: chats,
sessions, and memory live on the machine that owns the profile, exactly as if you were using
that instance directly."* No hay nada que sincronizar porque solo hay un sitio donde algo se
escribe.

## Aprovechar el hardware/software del equipo que no es el servidor (ej. Adobe, GPU)

Esto es un eje aparte, y solo aplica si de verdad necesitan que los COMANDOS (no el chat) se
ejecuten con el hardware/software de la otra máquina — renders, ediciones, lo que pida
software que el servidor no tiene.

`terminal.backend` decide dónde corren las herramientas de terminal del agente — totalmente
independiente de dónde vive la memoria (eso sigue siendo del servidor, sin excepción):
```yaml
# En el config.yaml del SERVIDOR (el dueño del perfil)
terminal:
  backend: ssh   # local | ssh | docker | modal | daytona | vercel_sandbox
  # host/usuario del equipo remoto — VERIFICAR el nombre exacto de estas claves contra
  # `hermes config --help` / la doc de Configuration en la máquina real antes de usar en
  # producción: la documentación pública solo confirma TERMINAL_SSH_HOST y TERMINAL_SSH_USER
  # como variables de entorno obligatorias para el backend ssh, no el nombre exacto de la
  # clave de config.yaml equivalente.
```
`tools/elegir_terminal_backend.py` (nuevo) prueba si el equipo secundario responde por SSH y
alterna `terminal.backend` entre `ssh` (apuntando a esa máquina) y `local` (en el servidor) —
pensado para correr como cron cada pocos minutos. Ver cabecera del script para cómo activarlo
por cliente (el host/usuario son específicos de cada instalación, no van hardcodeados aquí).

**Límite real, no cosmético:** si la tarea ya estaba corriendo en una máquina y esa máquina se
apaga a mitad de camino, esa tarea específica no "migra" sola — hay que relanzarla en el nuevo
backend. El switch solo decide dónde arrancan las tareas NUEVAS.

## Cuando el cliente es más de una persona — perfiles por rol, no por nombre

Un negocio de dos o más socios que comparten una sola máquina/instalación necesita más de un
perfil de Hermes, pero **nunca se decide por nombre propio** — se decide por lo que ya está en
`personas:` del manifiesto (`fichas/radiografia.yaml`), que ya se captura por **rol**, no por
nombre.

**El patrón:**
- **Un perfil por cada persona con `usa_pc: true`** — su propio contexto, su propia memoria,
  sus propios skills. Lo que uno gestiona no se mezcla con lo que gestiona el otro.
- **Un perfil compartido adicional** (`agencia`/`negocio`) cuando `tipo: negocio` y hay más de
  una persona — es el que redacta hacia clientes externos según directrices conjuntas de
  ambos, igual que un equipo comparte una sola cuenta de WhatsApp de atención aunque cada
  persona tenga la suya propia.
- Los perfiles personales **alimentan** al compartido (las decisiones que cada persona toma en
  su propio perfil pueden terminar reflejadas en lo que el perfil de agencia le dice al
  cliente), pero el compartido no sustituye a ninguno de los dos.

**Por qué por rol y no por nombre:** el manifiesto vive fuera del repo y nunca lleva nombres
propios de clientes (ver `criterios/`) — pero el PATRÓN de cuántos perfiles crear y cómo se
relacionan entre sí sí es reusable, y vive aquí en genérico.

`tools/perfiles_equipo.py manifiesto.yaml` lee `personas:` y `tipo:` y propone los perfiles a
crear (solo propone, igual que `roster_sugerido.py` — crear el perfil de verdad en la máquina
del cliente es una decisión aparte).
