# Cambios sobre Cadence original

Base: https://github.com/wesswart77/obsidian-cadence v0.15.0 (MIT, Copyright (c) 2026 Wesley Swart). La licencia va en `LICENSE`.

## Qué agrega este fork
- **Reporte de Finanzas:** ingresos cobrados, por cobrar, egresos y utilidad neta. Lee los gastos de la carpeta `Cadence/Gastos/` (campos `amount`, `date`, `category`, `recurring`) y los tratos ganados (`value`, `paid`, `paymentDate`, `closeBy`).
- **Contactos estancados:** el aviso pasa de 30 a 15 días sin contacto.

## Qué cambió para el repo
- Id del plugin: `cognilab-cadence` (el original usa `cadence-planner`; no se instalan los dos a la vez).
- Id de vista: `cognilab-cadence-app`.
- El reporte de Finanzas excluye de los egresos los gastos cuyo nombre empieza por «Pago a socio», «Pago a propietario/a», «Pago a dueño/a» o «Pago a titular». Antes la regla estaba fijada a un nombre propio. **Este cambio de comportamiento no está probado dentro de Obsidian.**
- Se quitó de un texto de ayuda un nombre de persona.

## Pendiente
- Probar el reporte de Finanzas en una bóveda real con gastos.
- Hacer el nombre de la regla de pago configurable en ajustes.
