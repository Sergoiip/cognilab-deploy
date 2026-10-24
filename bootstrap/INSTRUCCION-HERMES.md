# Instrucción para el Hermes que instala (copiar y pegar)

Para cuando el equipo del cliente ya tiene Hermes y quieres que **él** corra el setup. Se pega tal cual en una sesión nueva de Hermes en ese equipo. Cambia solo `cliente-X` y elige la **Opción A** o la **B** según cómo le llegue el repo.

## Cómo le llega el repo al cliente (lo haces tú antes)

| Opción | Cuándo | Qué le entregas | Por qué canal |
|---|---|---|---|
| **A · Token de solo lectura** | El cliente tiene `git` y puede usar GitHub | Un *fine-grained token* limitado al repo `cognilab-deploy`, permiso *Contents: read-only*, vence en 14 a 30 días | Canal privado (no por chat de grupo ni correo abierto). Se revoca al terminar |
| **B · Paquete firmado** | El cliente no tiene GitHub, o prefieres cero credenciales | `cognilab-deploy-<versión>.tar.gz` y su `.sha256` (los genera `tools/empaquetar.sh`) | Enlace temporal (Drive, Syncthing). Lo borras al terminar |

Nunca pegues el token dentro de la instrucción ni lo mandes por el chat con el Hermes: el cliente lo escribe él mismo cuando git se lo pida.

## Instrucción · Opción A (token)

```
Vas a dejar este equipo listo con el paquete de CogniLab. Sigue estos pasos en orden y NO saltes la aprobación del paso 4.

1. Trae el repo: `git clone https://github.com/Sergoiip/cognilab-deploy.git ~/cognilab-deploy` (si ya existe, `git -C ~/cognilab-deploy pull`). Git pedirá usuario y contraseña: el usuario es `Sergoiip` y la contraseña es un token que escribiré yo en la terminal. NO guardes ni muestres ese token, no lo escribas en ningún archivo ni en la config de git. Si falla el acceso, detente y avísame.
2. Revisa que existan PyYAML y mi manifiesto `~/cognilab-deploy/manifiestos/cliente-X.yaml`. Si falta algo, dímelo y detente.
3. Corre en simulación, sin instalar nada:
   bash ~/cognilab-deploy/bootstrap/instala.sh ~/cognilab-deploy/manifiestos/cliente-X.yaml --dry-run
   Muéstrame la salida completa y resúmela en 5 líneas: qué skills, qué apps, qué plugins, qué pide sudo, qué queda «a mano».
4. ESPERA mi respuesta. Solo si digo «aprobado», corre:
   bash ~/cognilab-deploy/bootstrap/instala.sh ~/cognilab-deploy/manifiestos/cliente-X.yaml
   Si digo que sin apps, agrega `--sin-apps`.
5. Reglas mientras corre:
   - No modifiques mi config.yaml, mi .env ni mis claves.
   - No uses `--si` salvo que yo lo pida. Si el script pregunta qué apps instalar, pregúntame a mí.
   - Si un comando pide sudo, dime cuál es y espera.
   - Si algo falla, no improvises ni repitas con otros comandos: muéstrame el error y espera.
6. Al terminar dime: la versión que quedó registrada, qué se instaló, qué falló y la lista «a mano» (cuentas por crear, modo restringido de Obsidian). No inventes resultados: reporta lo que salió.
```

## Instrucción · Opción B (paquete firmado)

Sustituye los pasos 1 y 2 del bloque anterior por estos; los pasos 3 a 6 quedan igual.

```
1. Tengo en ~/Descargas el paquete `cognilab-deploy-<versión>.tar.gz` y su archivo `.sha256`. Verifica la integridad ANTES de abrir nada: `cd ~/Descargas && sha256sum -c cognilab-deploy-<versión>.tar.gz.sha256`. Si no dice OK, detente y avísame; no lo extraigas.
2. Extrae: `mkdir -p ~/cognilab-deploy && tar -xzf cognilab-deploy-<versión>.tar.gz -C ~/cognilab-deploy --strip-components=1`. Guarda el manifiesto que te pegaré en `~/cognilab-deploy/manifiestos/cliente-X.yaml` y revisa que exista PyYAML. Si falta algo, dímelo y detente.
```

Para comprobar el hash por otro canal, mándale el valor del `.sha256` por un medio distinto al del enlace (por ejemplo, el hash por WhatsApp y el archivo por Drive).

## Generar el paquete (Opción B)
```
cd ~/cognilab-deploy && tools/empaquetar.sh
```
Deja el `.tar.gz` y el `.sha256` en `~/Documents/cognilab-deploy-paquetes/`. Se niega a empaquetar si hay cambios sin commit o si `verificar.py` falla. Solo incluye lo que git versiona: nunca manifiestos de clientes ni archivos locales.

## Después de la instalación
- Opción A: revoca el token en GitHub (Settings → Developer settings → Fine-grained tokens) y pide al cliente borrar el clon si no lo necesita.
- Opción B: borra el enlace temporal.
- Anota en Cadence la versión instalada.

## Por qué esta forma
- **Dry-run primero y aprobación explícita:** el script instala software y puede pedir `sudo` en un equipo ajeno.
- **No tocar config ni claves:** el Hermes del cliente tiene sus propias claves; el setup solo agrega la carpeta `skills/cognilab-deploy/` y los plugins.
- **Sin `--si`:** las apps son opcionales y el cliente decide cuáles.
- **Token de solo lectura, por cliente y con vencimiento:** si se filtra, solo se puede leer ese repo y se revoca sin afectar a nadie más.

## Límites conocidos
- Solo se ha probado la simulación (`--dry-run`). La instalación real aún no se ha corrido en un equipo de cliente; la primera vez, hazla acompañando.
- La Opción A depende de que el token no quede en el historial de la conversación con el Hermes del cliente. Por eso lo escribe el cliente en la terminal, no el agente.
- El manifiesto no está en el repo ni en el paquete (lleva datos del cliente): se entrega aparte y se pega en el chat o se copia al equipo.
