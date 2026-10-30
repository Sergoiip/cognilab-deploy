# cognilab-deploy

Paquetes instalables para dejar el equipo de un cliente listo, según el modelo de **entregables en 90 días**.
Repo público (solo lectura, sin token). Es el producto técnico; **los precios, cuotas y condiciones viven en Cadence**, no aquí:
`Cadence/Services/Paquete Del caos al sistema en 90 días`.

## Dos ejes
- **Paquete** (qué módulos entran): `Esencial` o `Integral` → `paquetes/`.
- **Escala del cliente** (qué profundidad): 1 individuo, 2 negocio, 3 equipo → `escalas.md`.

## Estructura
```
modulos/       22 entregables en 5 bloques (A a E), cada uno con SKILL.md, modulo.yaml y variantes/1,2,3
paquetes/      esencial.yaml, integral.yaml (escalera de oferta en escalera.md)
fases/         las 3 fases de 90 días y su hito
fichas/        ficha de ingreso y de cierre
criterios/     criterios de "hecho" para aprobar
stack/         catálogo de apps gratis, perfiles por escala, plantilla del CRM
bootstrap/     instala.sh: PC listo desde un manifiesto (skills + apps)
manifiestos/   ejemplo; el del cliente real NO se versiona
tools/         verificar.py: estructura + sincronía con Cadence
```

## Flujo con un cliente
0. **Radiografía** (`fases/0-radiografia.md`, 1 semana): entrevistas, observación, `tools/inventario.sh` (con permiso), línea base, Mapa vivo v1. Sale `radiografia.yaml`.
   `python3 tools/plan.py radiografia.yaml --inventario inventario.yaml --salida manifiestos/cliente-X.yaml` propone el manifiesto y explica cada decisión (dolor → módulo → escala). Es propuesta, no decisión.
1. Fase 1 — el manifiesto (paquete + módulos + escala + acompañamiento + agente) sale de una encuesta, no se escribe el YAML a mano:
   - **El cliente la llena solo, antes de la sesión:** abrir `bootstrap/encuesta.html` (doble clic, cualquier navegador, sin internet ni servidor) y enviar el YAML resultante (copiarlo o descargarlo) a Sergio.
   - **O se llena en vivo junto al cliente:** `python3 tools/encuesta_manifiesto.py` — mismo cuestionario por terminal, guarda directo en `manifiestos/cliente-X.yaml`.
   - La encuesta web se regenera con `python3 tools/generar_encuesta_html.py` cada vez que cambien `modulos/` o `paquetes/` (lee los datos reales, nunca queda con una lista vieja).
2. Fase 2: `bootstrap/instala.sh manifiestos/cliente-X.yaml --dry-run`, revisar, y correr sin `--dry-run`. `--sin-apps` instala solo los skills.
   Si el cliente ya tiene Hermes, él mismo puede correr el setup: la instrucción lista para pegar está en `bootstrap/INSTRUCCION-HERMES.md`.
   La bóveda se personaliza **desde el momento en que existe el manifiesto, no al final**: el paso 3/6 de `instala.sh` (`tools/scaffold_vault.py`) escribe `00 - Bienvenida.md` con el nombre del cliente, su agente y sus módulos elegidos, y crea las carpetas que esos módulos ya necesitan. Si el manifiesto es preliminar y cambia durante la Radiografía, correr `instala.sh` de nuevo (o solo `scaffold_vault.py`) refleja el cambio de inmediato — nunca hay que esperar a la semana completa para que se vea algo personalizado.
   Justo después de instalar: `bootstrap/PRIMEROS-PASOS.md` — qué verificar y, si el manifiesto es preliminar (vino de la encuesta, no de una Radiografía completa), cómo afinarlo esa misma semana.
3. Fase 3: `fichas/cierre.md`, medición contra línea base, aceptación.
4. Anotar en Cadence la versión instalada (`VERSION` en el equipo del cliente).

## El universo de agentes (empleados-agente del cliente)

Además del agente principal (B1/B2, el que coordina), el manifiesto puede activar
**empleados-agente** por departamento — Bot Mode de Hermes (perfiles con su propio rol, modelo,
memoria y skills, que se mencionan entre sí), no un orquestador externo. La línea base
replicable vive en `stack/roles-agentes.yaml` (Finanzas, Crecimiento, Edición y Producción —
cada uno se activa solo si el manifiesto trae los módulos correspondientes).

`python3 tools/roster_sugerido.py manifiestos/cliente-X.yaml --radiografia <radiografia.yaml>`
propone el roster y, si la radiografía ya tiene `identidad_agentes` (narrativa/lore, motivación,
estética — se capturan en el día 1 de la Fase 0), muestra cómo ese cliente en particular debería
flavorizar el SOUL.md de cada Bot. Solo propone — crear los perfiles de verdad (`hermes profile
create <rol>`) es una decisión aparte, confirmada con el cliente.

## Configuración dual (dos equipos, un solo agente)

Cuando el cliente tiene un equipo siempre encendido (servidor) y otro más potente que se usa
solo cuando está prendido — ver `bootstrap/CONFIGURACION-DUAL-MAQUINA.md`: cómo migrar un
perfil ya configurado en uno de los dos al que va a quedar como servidor, cómo conectar el otro
como cliente (Desktop y terminal, sin bifurcar memoria), y `tools/elegir_terminal_backend.py`
para que las tareas de terminal usen el hardware/software del equipo secundario cuando está
disponible y caigan al servidor cuando no.

## Nivel de acompañamiento (independiente del paquete y la escala)
El manifiesto trae `acompanamiento: tecnico | integral`, decidido en la ficha de ingreso, no en el
paquete ni en la escala — dos clientes con el mismo paquete Esencial pueden querer acompañamientos
distintos:
- **tecnico:** el cliente quiere entender su agente y sacarle el máximo provecho. La entrega
  (criterio común C3 "Documentado") explica el cómo y el porqué de cada pieza, no solo el qué.
- **integral:** el cliente quiere resultados sin tecnicismo. La misma entrega se documenta como
  una hoja simple de "así se usa", sin explicar mecánica interna; Sergio sigue operando/ajustando
  lo técnico por su cuenta cuando haga falta.

Este campo no cambia qué módulos se instalan, solo cómo se explican y documentan al entregarlos.

## Nombre y personalidad del agente
El manifiesto admite un bloque opcional `agente: {nombre, personalidad}` (texto libre corto, p. ej.
"cálido, directo, sin jerga técnica"). `bootstrap/instala.sh` lo escribe en el `SOUL.md` del
cliente (vía `tools/personalizar_agente.py`) como un bloque marcado e idempotente — no reemplaza
el resto del `SOUL.md` por defecto de Hermes, solo inserta/actualiza ese bloque. Si el manifiesto
no trae ninguno de los dos campos, el `SOUL.md` no se toca.

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
| negocio | 2 | + TaskNotes, Cadence (CRM y finanzas), Syncthing, Pandoc, FFmpeg |
| equipo | 3 | + rclone (espejo en nube), Excalidraw |

Además, cada módulo suma lo suyo (por ejemplo C1 trae Inkscape y GIMP; D2 trae Kdenlive).

**Todo es opcional.** Los perfiles son una propuesta, no una obligación. `instala.sh` muestra la lista numerada y pregunta:
Enter instala todo, `3,5` quita esas, `n` no instala ninguna app. Sin terminal no instala nada salvo que pases `--si`.
Los skills del producto siempre se instalan; las apps nunca se imponen.

**Cómo se asigna.** En la ficha de ingreso se anota qué ya usa el cliente.
- `modo: cliente`: se respeta lo que ya usa (`ya_usa`) y solo se ofrece lo que los módulos piden.
- `modo: asignar`: el cliente no sabe qué usar; se le propone el perfil de su escala.

**Cadence modificado.** Va en `stack/vendor/lab-cadence/` (fork MIT de wesswart77, con reporte de Finanzas y alerta de estancados a 15 días). Es una versión neutra, sin nombres de clientes; cambios y pendientes en su `CAMBIOS.md`, metodología y recomendaciones de uso en su `METODOLOGIA.md`.

**Task Atlas.** Va en `stack/vendor/task-atlas/` (plugin propio de CogniLab). Metodología y recomendaciones de uso en su `METODOLOGIA.md`.

**Ampliar el stack con la operación.**
1. Agregar una app en `stack/extras.yaml` (hay un ejemplo comentado). Se funde con el catálogo al cargar.
2. Sumarla a un perfil o a un módulo desde el mismo archivo.
3. Cuando se consolide, pasarla a `stack/catalogo.yaml` y subir `version_catalogo`.
`tools/verificar.py` valida que lo agregado exista, tenga hash si es plugin y esté marcado opcional.

**Seguridad.** Los plugins de terceros no se copian al repo: se bajan del release oficial y se comparan por sha256 con el catálogo; si no coincide, no se instala. El fork de Cadence sí vive en el repo, también con hash, y el verificador falla si se altera sin actualizar el catálogo.

**Límites conocidos.**
- Los nombres de paquete están verificados solo en `pacman`. Los de `apt` y `dnf` están por probar en un equipo real.
- Los paquetes del sistema piden `sudo`.
- Las cuentas (Telegram, WhatsApp Business, Discord, Drive) las crea el cliente; el script las deja en una lista "a mano".
- Obsidian pide desactivar el modo restringido una vez, a mano, para activar plugins.
- Solo Linux (pacman/apt/dnf). Este instalador no soporta macOS ni Windows — si el cliente está en esos sistemas, los módulos siguen siendo entregables (manuales, con quien opere ahí), pero `instala.sh` no corre. Las apps del catálogo marcadas `tipo: manual` (ej. Wispr Flow) existen justo para documentar ese caso sin fingir automatización que no hay.
