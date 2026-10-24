# Instrucción para el Hermes que instala (copiar y pegar)

Para cuando el equipo del cliente ya tiene Hermes y quieres que **él** corra el setup. Se pega tal cual en una sesión nueva de Hermes en ese equipo. Cambia solo `cliente-X`.

```
Vas a dejar este equipo listo con el paquete de CogniLab. Sigue estos pasos en orden y NO saltes la aprobación del paso 4.

1. Trae el repo: `gh repo clone Sergoiip/cognilab-deploy ~/cognilab-deploy` (si ya existe, `git -C ~/cognilab-deploy pull`). Si pide acceso, detente y avísame; no uses otras credenciales.
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

## Por qué esta forma
- **Dry-run primero y aprobación explícita:** el script instala software y puede pedir `sudo` en un equipo ajeno.
- **No tocar config ni claves:** el Hermes del cliente tiene sus propias claves; el setup solo agrega la carpeta `skills/cognilab-deploy/` y los plugins.
- **Sin `--si`:** las apps son opcionales y el cliente decide cuáles.
- **Reportar solo lo que salió:** el cierre se registra en Cadence con la versión instalada.

## Variante con el manifiesto por mensaje
Si el manifiesto no está en el repo (no se versiona), el cliente o tú lo pegan en el chat y se agrega al paso 2: «Guarda este YAML en `~/cognilab-deploy/manifiestos/cliente-X.yaml`» seguido del contenido.

## Límite conocido
Solo se ha probado la simulación (`--dry-run`). La instalación real aún no se ha corrido en un equipo de cliente; la primera vez, hazla acompañando.
