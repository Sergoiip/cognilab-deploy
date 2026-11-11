# Flota (núcleo, catálogo y planos)

El **Astillero** (este repo) arma la **Flota** de cada cliente con piezas estándar. Cuatro piezas que no se mezclan:

| Pieza | Responde a | Qué es en Hermes | Archivo |
|---|---|---|---|
| Estación | ¿De quién es la memoria y las credenciales? | Un perfil | `estaciones/{persona,negocio,servicio}.yaml` |
| Sector | ¿Qué área? | Una etiqueta. **Nunca un perfil** | `sectores.yaml` (núcleo, fijo) |
| Nave / faro | ¿Cómo se hace un trabajo concreto? | Ficha + skills + disparador, ejecutada por una estación | `naves/<sector>/<id>.yaml` |
| Plano | ¿Qué combinación sirve para este negocio? | Tipo de empresa × escala | `planos/<tipo>-e<escala>.yaml` |

**Sectores con dos lentes.** `pkm` (la persona: rueda PKM adaptada) y `apqc` (el negocio: APQC PCF cross-industry comprimido para pymes). Un dueño único usa las dos.

**Núcleo** (`nucleo.yaml`): código de navegación que se suma a todo `no_hace`, campos obligatorios de toda ficha, estados de plano y vocabulario hacia el cliente. No se personaliza.

**Manifiesto del cliente:** `manifiestos/cliente-<x>.yaml` (no se versiona). Elige un plano, nombra estaciones y capitanes, mapea los crons reales a sectores y sobrescribe lo personalizable.

## Comandos
```bash
U="uv run --no-project --with pyyaml python3"
$U tools/verificar.py                                         # valida catálogo, planos y sincronía con Cadence
$U tools/flota.py estado  manifiestos/cliente-x.yaml          # cobertura por sector, cruzada con los crons reales
$U tools/flota.py aplicar manifiestos/cliente-x.yaml          # simula: muestra lo que haría
$U tools/flota.py aplicar manifiestos/cliente-x.yaml --si     # instala/actualiza (solo en la máquina del manifiesto)
python3 flota/naves/finanzas/aviso_cobros.py --raiz <CRM> --hoy 2026-11-12          # probar un faro en una fecha
python3 flota/naves/operacion/estado_entregables.py --raiz <Projects> --todo         # informe completo sin filtro de urgencia
```

`aplicar` es idempotente. Describe las estaciones que existen y crea las que faltan **sin credenciales** (el responsable conecta su proveedor). Genera `flota_<nave>.py` en el directorio de scripts del perfil y da de alta el faro `Flota · <nombre>` si no existe. Nunca borra un faro.

## Coordinador y misiones
- El manifiesto declara `coordinador: <id de estación>`. El coordinador recibe lo que pide el capitán, decide quién lo hace y reparte misiones; las naves con `la_ejecuta: coordinador` corren en su perfil.
- `tools/flota.py mision <plantilla> <manifiesto> --var clave=valor [--si]` crea una misión con su contrato (tipo, criterio de hecho, rúbrica, topes, protocolo) y su «⛔ Visto bueno» si es un documento. En `presupuesto.modo: manual` nace bloqueada.
- Naves del Ágora (sin modelo): **Esperando tu OK** (aprobaciones del día), **Tareas atascadas**, **Respaldo de la Flota** y **Faro de misión** (crea una misión en una fecha; cada instancia del manifiesto lleva `instancia`, `nombre`, `faro`, `repetir` y `args`).

## Puente de mando (vista en vivo)
`tools/puente/servidor.py <manifiesto> [--puerto 7171]`: la portada (`/`) responde en lenguaje simple tres preguntas —qué necesita del capitán, qué hace cada agente ahora y qué pasa hoy— con la marca CogniLab (Outfit, Chakra Petch); `/mapa` es la vista avanzada. Servidor local (solo localhost, solo lectura, sin dependencias fuera de PyYAML) que muestra cómo está trabajando la Flota: estaciones y sus naves en órbita (activa, trabajando, falló, pausada), el Ágora con las misiones en curso y en tránsito, lo que espera al capitán, lo atascado, los próximos faros, el consumo del día y una bitácora de 24 h. Clic en una nave o misión abre su detalle y su última salida. Si el manifiesto no trae `alias`, muestra nombres funcionales (instalaciones de clientes). Las naves sin faro se declaran en `reserva:` del manifiesto. En la máquina de CogniLab corre como `cogsmos-puente.service`.

## Cómo agregar una nave al catálogo
1. `naves/<sector>/<id>.yaml` con los campos obligatorios del núcleo, más `script`, `argumentos` (admite `{crm.raiz}`, `{crm.proyectos}`) y `disparador.faro`.
2. El script va al lado. Si imprime vacío, el faro calla. Si necesita un modelo, todavía no se instala solo (`aplicar` lo avisa).
3. `verificar.py` en verde. Agregarla al plano y al manifiesto, y correr `aplicar`.

## Reglas
- Una estación se crea solo por frontera de privacidad, más de una voz de marca o atención pública. Nunca por sector.
- Un plano pasa a `validado` solo con evidencia (`verificar.py` lo exige).
- Una nave local que aparece en 2 clientes se promueve al catálogo.
- Sin precios, nombres de clientes ni credenciales en este directorio.
