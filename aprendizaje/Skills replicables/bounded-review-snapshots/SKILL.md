---
name: bounded-review-snapshots
description: Use when weekly snapshots need confirmed task states.
version: 0.1.0
---

# Revisión acotada y snapshot semanal verificable

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{VENTANA}} | Periodo y alcance aprobados por la persona |
| {{PREGUNTAS}} | Confirmación de progreso y dudas antes de exportar |
| {{TAREAS}} | API/MCP del registro canónico |
| {{EDITABLE}} | Nota fuente versionada y fechada |
| {{PDF}} | Snapshot de entrega |
| {{CANAL}} | Destino de archivo autorizado |

## Propósito
Cerrar una revisión de periodo sin ampliar compromisos ni convertir respuestas ambiguas en progreso; generar un snapshot fiel a estados canónicos.

## Cuándo usar
Entrega de un plan semanal o PDF después de confirmar qué se hizo, especialmente cuando hay estados dudosos o alcance restringido.

## Entradas
{{VENTANA}}, {{PREGUNTAS}}, tareas reales, propietarios explícitos y permisos de actualización/entrega.

## Pasos
1. Preguntar por terminado/en curso antes de cambiar estados si ese orden fue solicitado. Agrupar opciones claras cuando se pida y terminar con pregunta abierta; evitar opciones que unan dos herramientas o dos logros.
2. Mantener dudas explícitas. Instalación operativa, autenticación y acceso remoto probado son estados distintos; una respuesta compuesta no confirma todos.
3. Recortar al alcance de {{VENTANA}}. No arrastrar cada tarea histórica ni añadir ejecución operativa a una semana reservada a registros. Separar infraestructura de trabajo propio si no hay dueño asignado.
4. Consultar {{TAREAS}}, deduplicar y verificar estados/fechas exactos. Limpiar fechas inferidas mediante escritura aprobada y readback; no alterar defaults globales ni usar checkboxes paralelos como autoridad.
5. Construir {{EDITABLE}} fechado y {{PDF}} como snapshot, no como fuente viva del gestor. Guardarlos en el registro canónico y enlazarlos desde su índice.
6. Validar texto, número de páginas y una página renderizada como mínimo. Si hay maquetación fija aplicar inspección exhaustiva de la skill de integridad paginada.
7. Entregar {{PDF}} como archivo por {{CANAL}} autorizado y comprobar evidencia de envío; no presentar una ruta local como archivo recibido.

## Reglas de decisión
- Alcance semanal confirmado prevalece sobre inventario histórico.
- Una respuesta ambigua mantiene estados separados hasta aclaración.
- El PDF es foto fechada; futuras modificaciones pertenecen a la autoridad de tareas.

## Verificación
Contrastar cada estado del documento con lectura de tarea canónica. Verificar vínculos a editable/salida, texto y render; declarar cobertura visual exacta. Registrar entrega por canal solo si ocurrió realmente.

## Pitfalls
No confundir herramienta instalada con login ni login con operación remota. No asignar trabajo de infraestructura a la persona por omisión. No afirmar que una pregunta enviada ya obtuvo respuesta.

## Variantes
Solo preguntas; snapshot sin cambios de tareas; actualización aprobada seguida de snapshot. La falta de confirmación conserva incertidumbre, no fuerza completitud.

## Referencias y alcance de evidencia
- [Procedencia y límites](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
