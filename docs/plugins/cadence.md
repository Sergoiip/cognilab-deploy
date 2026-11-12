# Cadence (fork CogniLab)

**Versión del catálogo:** 0.15.0-cognilab.1 · MIT (base: wesswart77/obsidian-cadence) · cambios en `stack/vendor/cognilab-cadence/CAMBIOS.md`

## Metodología (según el plugin)
Un solo espacio de trabajo para CRM, PRM, proyectos, planificación diaria y recordatorios, todo sobre Markdown. Cada contacto, trato, proyecto y actividad es una nota con frontmatter. Pantallas: Inicio, Hoy, Semana, Pipeline (kanban por etapa), Contactos, Proyectos, Bandeja de entrada y Reportes. Los módulos CRM, PRM y Planner se pueden apagar. Permite propiedades propias por entidad, sincronización bidireccional entre proyecto y contacto, e importar CSV.

## Qué cambia en el fork
Reporte de Finanzas (cobrado, por cobrar, egresos, utilidad) y aviso de contactos estancados a 15 días sin contacto en lugar de 30.

## Recomendación CogniLab
- **Empezar solo con lo que el cliente usa:** si no tiene alianzas, apagar PRM.
- **Una etapa de pipeline por paso real de venta**, no por costumbre. Máximo de 5 a 6.
- **Registrar cada contacto con fecha** y mirar los estancados una vez por semana.
- **Cargar la lista actual por CSV** al inicio para que arranque con datos y no vacío.
- **Gastos** en `Cadence/Gastos/` con `amount`, `date`, `category`, `recurring`, para que el reporte de Finanzas funcione.
- Una nota por cliente con su bitácora, y el cierre de cada sesión anotado ahí.

## Cuidado
- **No instalar junto al Cadence original:** el fork tiene otro id (`cognilab-cadence`).
- La regla que excluye «Pago a socio/propietario» de los egresos **no está probada dentro de Obsidian**.
- Los datos de clientes nunca van al repositorio del deploy.
