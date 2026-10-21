# cognilab-deploy

Paquetes instalables para dejar el equipo de un cliente listo, según el modelo de **entregables en 90 días**.
Repo privado. Es el producto técnico; **los precios, cuotas y condiciones viven en Cadence**, no aquí:
`Cadence/Services/Paquetes por entregables — modelo 90 días`.

## Dos ejes
- **Paquete** (qué módulos entran): `Esencial` o `Integral` → `paquetes/`.
- **Escala del cliente** (qué profundidad): 1 individuo, 2 negocio, 3 equipo → `escalas.md`.

## Estructura
```
modulos/       22 entregables en 5 bloques (A a E), cada uno con SKILL.md, modulo.yaml y variantes/1,2,3
paquetes/      esencial.yaml, integral.yaml
fases/         las 3 fases de 90 días y su hito
fichas/        ficha de ingreso y de cierre
criterios/     criterios de "hecho" para aprobar
stack/         catálogo de apps gratis, perfiles por escala, plantilla del CRM
bootstrap/     instala.sh: PC listo desde un manifiesto (skills + apps)
manifiestos/   ejemplo; el del cliente real NO se versiona
tools/         verificar.py: estructura + sincronía con Cadence
```

## Flujo con un cliente
1. Fase 1: llenar `fichas/ingreso.md` → sale el manifiesto (paquete + módulos + escala).
2. Fase 2: `bootstrap/instala.sh manifiestos/cliente-X.yaml --dry-run`, revisar, y correr sin `--dry-run`. `--sin-apps` instala solo los skills.
3. Fase 3: `fichas/cierre.md`, medición contra línea base, aceptación.
4. Anotar en Cadence la versión instalada (`VERSION` en el equipo del cliente).

## Mantener la sincronía
`python3 tools/verificar.py` falla si hay precios, nombres de clientes o rastros de otros clientes en el repo,
o si el menú de Cadence menciona una meta-skill que ningún módulo implementa. Avisa si el entregable de Cadence
cambió desde el último `--sellar`.

## Reglas
- Sin credenciales, sin precios, sin datos de clientes.
- Un módulo no es "hecho" hasta cumplir su criterio y los comunes (`criterios/`).

## Stack de aplicaciones (todo gratis)
`stack/catalogo.yaml` define las apps, los 3 perfiles y qué módulo necesita qué.

| Perfil | Escala | Incluye |
|---|---|---|
| ligero | 1 | Hermes, Obsidian, Git, GitHub CLI, plugins obsidian-git y Templater |
| negocio | 2 | + TaskNotes, Cadence (CRM), Syncthing, Pandoc, FFmpeg |
| equipo | 3 | + rclone (espejo en nube), Excalidraw |

Además, cada módulo suma lo suyo (por ejemplo C1 trae Inkscape y GIMP; D2 trae Kdenlive).

**Cómo se asigna.** En la ficha de ingreso se anota qué ya usa el cliente.
- `modo: cliente`: se respeta lo que ya usa (`ya_usa`) y solo se instala lo que los módulos piden.
- `modo: asignar`: el cliente no sabe qué usar; se le da el perfil de su escala.

**Seguridad.** Los plugins de Obsidian no se copian al repo: se bajan del release oficial y se comparan por sha256 con el catálogo; si no coincide, no se instala. Cadence se instala desde el original (MIT) de su autor, con la plantilla de CRM de este repo (sin token ni datos).

**Límites conocidos.**
- Los nombres de paquete están verificados solo en `pacman`. Los de `apt` y `dnf` están por probar en un equipo real.
- Los paquetes del sistema piden `sudo`.
- Las cuentas (Telegram, WhatsApp Business, Discord, Drive) las crea el cliente; el script las deja en una lista "a mano".
- Obsidian pide desactivar el modo restringido una vez, a mano, para activar plugins.
