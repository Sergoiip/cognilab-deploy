# Ficha de ingreso (Fase 1)

**Cliente:** ______  **Fecha:** ______  **Quién la llena:** ______

## Contexto
- Qué hace el negocio / la persona, en una frase:
- Qué le duele hoy (3 cosas, con un ejemplo real de cada una):
- Qué ya intentó:

## Equipo
- Sistema operativo (Linux Arch/CachyOS, Debian/Ubuntu/Mint, Fedora, otro), RAM, disco libre, GPU:
- ¿Hay permiso de administrador (sudo)? Sí / No
- ¿IA local o en la nube? ¿Por qué?

## Herramientas (esto decide qué instala el script)

**¿El cliente ya tiene herramientas con las que trabaja?**

| Función | Opciones del stack gratis | Ya usa (anotar) | Decisión |
|---|---|---|---|
| Notas y conocimiento | Obsidian | | mantener / asignar |
| Respaldo y versiones | Git + GitHub | | mantener / asignar |
| Tareas | TaskNotes (en Obsidian) | | mantener / asignar |
| CRM / clientes | Cadence (en Obsidian) | | mantener / asignar |
| Archivos y nube | Syncthing (sin nube) · rclone + Drive | | mantener / asignar |
| Agente de IA | Hermes | | mantener / asignar |
| Mensajería con clientes | Telegram · WhatsApp Business | | mantener / asignar |
| Documentos y cotizaciones | LibreOffice · Pandoc | | mantener / asignar |
| Diseño y fotos | Inkscape · GIMP | | mantener / asignar |
| Video | OBS Studio · Kdenlive | | mantener / asignar |

**Regla para decidir el modo (`herramientas.modo` del manifiesto):**
- Si el cliente **sabe qué quiere usar** y es del catálogo → modo `cliente`: se respeta; lo que ya usa se anota en `ya_usa` y no se instala.
- Si **no tiene idea o no tiene nada** → modo `asignar`: se le da el perfil según su escala (`ligero`, `negocio` o `equipo`, en `stack/catalogo.yaml`).
- Si usa algo **que no está en el catálogo** (Notion, Excel, etc.): no se instala nada para esa función; se anota aquí y se decide si se migra o se integra.

**Cuentas que el cliente crea él mismo** (marcar): [ ] Telegram  [ ] WhatsApp Business  [ ] Discord  [ ] Google Drive

## Escala por módulo
| Módulo | ¿Cuántas personas lo tocan? | ¿Qué pasa si falla? | Escala (1/2/3) |
|---|---|---|---|

## Línea base (máx. 5 indicadores, medibles)
| Indicador | Valor hoy | Fecha | Fuente |
|---|---|---|---|

## Permisos y datos
- ¿Qué datos son sensibles y dónde deben vivir?
- ¿Autoriza usar su caso en el portafolio? (por defecto: no)

## Decisión
Paquete: ______  Módulos: ______  Modo de herramientas: asignar / cliente  Manifiesto: `manifiestos/cliente-____.yaml`
