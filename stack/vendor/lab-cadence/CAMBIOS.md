# Lab Cadence — cambios sobre Cadence original

Base: https://github.com/wesswart77/obsidian-cadence v0.15.0 (MIT, Copyright (c) 2026 Wesley Swart). Licencia en `LICENSE`.
Id del plugin: `lab-cadence` (el original usa `cadence-planner`; no se activan los dos a la vez). Vista: `lab-cadence-app`.

## Qué agrega
- **Reports → Finanzas (v2):** cobrado, por cobrar, egresos, utilidad neta y proyectada; comparación con el mes anterior, margen, gasto diario; barras de 6 meses; egresos por categoría y recurrentes vs puntuales; cobrado por cliente; filtro por mes; botón «Sin pagos al socio».
  Lee los tratos ganados (`value`, `paid`, `paymentDate`, `closeBy`) y los gastos (`amount`, `date`, `category`, `recurring`).
- **Estancados:** deals y contactos sin tocar pasan de 30 a 15 días (el reporte de Productivity sigue en 30).

## Configuración (`data.json`, clave `lab`)
| Clave | Por defecto | Para qué |
|---|---|---|
| `staleDays` | 15 | Días para marcar estancado |
| `expensesFolder` | `Cadence/Gastos` | Carpeta de egresos |
| `ownerPaymentPattern` | `^pago a (socio\|socia\|propietari[oa]\|due[ñn][oa]\|titular\|fundador\|fundadora)` | Regex (sin distinguir mayúsculas) de los gastos que son pagos al dueño y se excluyen con el botón |
| `ownerLabel` | `socio` | Reservado para etiquetas |

Cada bóveda de cliente ajusta estos valores sin tocar el código. Una actualización de Cadence original no borra el fork: se fusiona desde `upstream` y se vuelve a copiar.

## Pendiente
- Probar Finanzas y la vista fijada dentro de Obsidian (verificado solo con `node --check`).
- Pantalla de ajustes para la clave `lab` (hoy se edita en `data.json`).
