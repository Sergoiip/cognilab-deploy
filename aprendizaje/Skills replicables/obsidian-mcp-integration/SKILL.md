---
name: obsidian-mcp-integration
description: Use when wiring Hermes to Obsidian via MCP or plugins.
version: 1.0.0
---

# Integración de Obsidian por MCP

## Cuándo usarla
- El usuario pide "instalar el MCP de Obsidian", conectar un agente de IA a su bóveda, o
  instalar/activar un plugin comunitario de Obsidian.
- Una llamada MCP contra un servidor de Obsidian falla o falta, y el arreglo está en el cableado
  plugin/servidor, no en el contenido de las notas.

Es la capa de instalación por debajo del CRUD de notas (que se hace una vez la conexión existe):
encontrar la bóveda, instalar los archivos del plugin, activarlo y registrar el servidor MCP.

## Encontrar la bóveda
Leer `obsidian.json` para obtener la ruta de la bóveda activa antes de tocar nada:

- Windows: `%APPDATA%\obsidian\obsidian.json`
- macOS: `~/Library/Application Support/obsidian/obsidian.json`
- Linux: `~/.config/obsidian/obsidian.json`

Su forma es `{"vaults": {"<id>": {"path": "...", "open": true}}}`: usar la entrada con
`"open": true` (o preguntar si hay varias).

## Instalar un plugin comunitario sin GUI (para los archivos)
1. Obtener las URL de los assets de la última release en GitHub:
   `https://api.github.com/repos/<owner>/<repo>/releases/latest` → tomar los
   `browser_download_url` de `main.js`, `manifest.json`, `styles.css`.
2. `mkdir -p "<ruta-de-la-bóveda>/.obsidian/plugins/<plugin-id>"` (el id es el campo `"id"`
   dentro de `manifest.json`, p. ej. `obsidian-local-rest-api`, `cadence-planner`) y descargar
   ahí los tres archivos.
3. Añadir el id a `<ruta-de-la-bóveda>/.obsidian/community-plugins.json`, un array JSON simple
   de ids. Crear el archivo (`["<plugin-id>"]`) si no existe: la bóveda puede no haber instalado
   nunca un plugin comunitario.
4. **La activación necesita una ventana de Obsidian viva una vez**: Ajustes → Plugins de la
   comunidad → activar el interruptor (y en plugins que generan un secreto, como la API key de
   Local REST API, el valor solo aparece dentro de la app en marcha). Editar archivos deja el
   plugin *instalado*, no *activado* con credencial usable: pedir al usuario que active el
   interruptor y entregue la clave, o manejarlo con `computer_use` si la app ya está abierta
   (`list_windows` → capturar por `pid`+`window_id`, no por nombre `app=`, porque Obsidian suele
   abrir una ventana secundaria de "Preferencias").

## Conectar el plugin Local REST API a un servidor MCP
1. Verificar que el plugin está vivo antes de configurar nada más:
   ```
   curl -s -k -H "Authorization: Bearer ***" https://localhost:27124/
   ```
   Esperar `"authenticated": true`. El puerto 27124 escucha en loopback por HTTPS con
   certificado autofirmado (`-k` obligatorio); el puerto HTTP plano 27123 es otro endpoint,
   desactivado por defecto: no asumir que está abierto.
2. Registrar el servidor: `hermes mcp add <nombre> --command npx --env KEY=VAL ... --args -y <paquete>`.
   **`--args` debe ser la ÚLTIMA opción de la línea**: el CLI consume todo lo que va después,
   así que un `--env` puesto tras `--args` acaba en silencio dentro de los args de npx.
3. La prueba de conexión de `hermes mcp add` está acotada (~30 s) y puede expirar con un servidor
   válido que tarda en instalarse por npm la primera vez. Validar aparte primero:
   ```
   KEY=val OTHER=val npx -y <paquete>
   ```
   y confirmar que registra una línea limpia de "server ready"/lista de herramientas antes de
   fiarse del resultado de `hermes mcp add`.
4. Si el paquete MCP "natural" exige un runtime que no está en el equipo (p. ej. el
   `mcp-obsidian` canónico pide `uvx`), no instalar un runtime nuevo por un nombre de paquete:
   buscar un equivalente publicado en npm que hable con la misma API local y solo necesite
   `npx`/Node (p. ej. `obsidian-mcp-server` sirve tal cual con Local REST API).
5. Si la prueba falla, `hermes mcp add` pregunta "Save config anyway? [y/N]". No responder `y`
   por reflejo: eso guarda el servidor *desactivado*. Aceptar solo si la prueba aislada del
   paso 3 demostró que comando/env funcionan; si no, `hermes mcp remove <nombre>` y corregir
   el comando primero.

## Manejar la app en vivo con el plugin REST
Con el plugin autenticado, el Obsidian en marcha se controla sin automatizar la GUI. La API key
es el campo `apiKey` de `.obsidian/plugins/obsidian-local-rest-api/data.json`: leerla en código
y no imprimirla nunca.

- `GET /commands/` lista ids de comandos; `POST /commands/<id>/` ejecuta uno (HTTP 204). Útiles:
  `app:reload` (recargar tras cambiar un tema o archivos de plugin), `editor:save-file`,
  `theme:toggle-light-dark`, `workspace:close`.
- `POST /open/<ruta de la bóveda url-encoded>` (cuerpo JSON `{"newLeaf":false}`) abre una nota o
  PDF en la app; úsalo para poner a la vista una nota concreta en vez de hacer scroll.
- `GET /active/` con `Accept: application/vnd.olrapi.note+json` devuelve la ruta de la nota
  activa; comprobarla y ejecutar `editor:save-file` antes de `app:reload`, porque recargar no
  guarda ediciones pendientes (un PDF o ninguna nota activa = nada que perder).
- Verificar cambios visuales en la ventana real: `computer_use` `list_windows`, luego `capture`
  con `pid` + `window_id` (capturar por `app=` no encuentra Obsidian). Las ventanas Electron
  descartan el scroll de rueda en segundo plano (piden entrega en primer plano, que requiere
  aprobación aparte), así que navegar con `/open/` a una nota que ya muestre el contenido, o
  crear una nota de prueba temporal, abrirla, capturar, cerrar la pestaña (`workspace:close`)
  y borrar el archivo.

## Plugins sin API propia (CRM/planificadores tipo Cadence)
Muchos plugins de "espacio de trabajo" no tienen superficie REST/MCP propia: guardan todo como
markdown de la bóveda con frontmatter (entidades, plantillas, notas diarias). No necesitan un
servidor MCP dedicado: con el MCP de Obsidian (vía Local REST API) cableado, sus herramientas de
leer/escribir notas, frontmatter y etiquetas ya cubren crear y editar esos registros. Confirmar
que el plugin está activo comprobando que sus comandos están registrados, en vez de suponer que
falta una integración:
```
curl -s -k -H "Authorization: Bearer ***" https://localhost:27124/commands/ | grep -i <plugin-id>
```

### Internos de Cadence (solo si la bóveda del cliente usa ese plugin)
Las entidades de Cadence son carpetas de markdown. Esquemas de campos, moneda y páginas
personalizadas viven en `.obsidian/plugins/cadence-planner/data.json` (`customEntities`,
`customPages`, `currency`). Editarlo con `json` de Python (mantener `ensure_ascii=False`); luego
el usuario debe recargar Obsidian (Ctrl+R). Un Obsidian abierto puede sobrescribir el archivo al
cerrarse.

- **Kanban/Deals leen `Cadence/Pipeline/` con `type: deal`; la etapa es un enum (Lead,
  Qualified, Proposal, Negotiation, Won, Lost).** Los campos enum rechazan otros valores (estado
  de lead: New/Contacted/Qualified/Disqualified/Converted): mapear lo que dice el usuario a las
  opciones permitidas. Una nota de lead sola nunca aparece en el Kanban: una cotización enviada
  necesita un deal en Pipeline en etapa Proposal.
- Añadir un campo: agregar `{key,label,type}` a la lista de la entidad en `customEntities` (tipo
  `currency` para dinero) y añadir la clave a `Templates/<entidad>.md`.
- **Entidad/página personalizada nueva:** la clave DEBE ser `<sección>_<singular>` (p. ej.
  `crm_servicio`) y necesita su entrada en `customPages` (`entityKey`, `sectionId`); si no, el
  plugin la borra como huérfana al cargar. Su carpeta es `Cadence/<etiqueta de la página>`, las
  notas llevan `type: <entityKey>` y la plantilla es `Templates/<entityKey>.md`.
- Las entidades núcleo (`project`, `deal`, `contact`, ...) tienen carpetas fijas; para
  reutilizar Projects, mover las notas a una entidad personalizada y reetiquetar los campos de
  `project` / `suggestionSource` (`folder:Cadence/<X>`). Los wikilinks van por nombre de nota,
  así que mover archivos no rompe enlaces.
- La moneda por defecto es USD; cambiar `currency` al código ISO de la moneda local del cliente.
