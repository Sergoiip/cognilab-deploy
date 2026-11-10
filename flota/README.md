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
uv run --no-project --with pyyaml python3 tools/verificar.py                   # valida catálogo y planos
uv run --no-project --with pyyaml python3 tools/flota.py estado manifiestos/cliente-x.yaml   # cobertura por sector
python3 flota/naves/finanzas/aviso_cobros.py --raiz <CRM> --hoy 2026-11-12      # probar un faro
```

## Reglas
- Una estación se crea solo por frontera de privacidad, más de una voz de marca o atención pública. Nunca por sector.
- Un plano pasa a `validado` solo con evidencia (`verificar.py` lo exige).
- Una nave local que aparece en 2 clientes se promueve al catálogo.
- Sin precios, nombres de clientes ni credenciales en este directorio.
