---
name: session-evidence-propagation
description: Use when session findings must reach live records.
version: 0.1.0
---

# Propagación documental de sesiones con evidencia

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{PROTOCOLO}} | Política aprobada de análisis y límites de propagación |
| {{FUENTES}} | Grabación o transcripción completa con bloques identificables |
| {{REGISTROS}} | Proyectos y procesos existentes autorizados |
| {{TAREAS}} | Autoridad vigente de tareas y estados |
| {{HANDOFF_PUBLICO}} | Extracto sanitizado de contexto compartido |
| {{BORRADORES}} | Destino de avisos no enviados separados por audiencia |

## Propósito
Llevar hallazgos de sesiones a registros existentes con trazabilidad y autorización, sin reinterpretar audio ambiguo como asignación, cambio laboral o publicación.

## Cuándo usar
Cierre de una sesión grabada con política autorizada, reconciliación de agendas históricas o traspaso entre perfiles con audiencias diferentes.

## Entradas
{{PROTOCOLO}}, {{FUENTES}}, decisiones posteriores, registros y permisos. La política de analizar una sesión no incluye automáticamente dictados breves ni demuestra ejecución de una automatización.

## Pasos
1. Leer protocolo y operación canónicos antes de activar análisis. Distinguir sesión, dictado y fragmento; registrar límites de transcripción y fuente/bloque de cada hallazgo.
2. Trazar hallazgo → decisión o pregunta → proyecto/proceso → tarea canónica si procede → resultado → aviso autorizado. Esto es un contrato documental, no el nombre de una integración técnica ya probada.
3. Recuperar {{REGISTROS}} existentes y decisiones más recientes antes de distribuir. Un resumen aislado no completa propagación. No restaurar estados históricos contradichos por registros vigentes.
4. Si una solicitud está truncada, abrir la tarjeta raíz exacta y contrastar agenda: el título puede conservar requisitos ausentes del body. No rellenar lagunas por intuición.
5. Comparar frontmatter actual de {{TAREAS}} con agendas antiguas. Quitar de inventario accionable lo que está terminado canónicamente, conservando contradicción como brecha y sin inferir cobro, aceptación o éxito operativo.
6. En traspasos, generar {{HANDOFF_PUBLICO}} sin datos privados que puedan inyectarse a hijos/coordinadores. Enviar hallazgos privados solo a continuación autorizada; separar archivos no basta si comparten board o contexto.
7. Preparar {{BORRADORES}} por destinatario y necesidad, no enviarlos. Verificar IDs, permisos, contenido compartible y autorización antes de habilitar un circuito externo.
8. Verificar enlaces de propagación y leer registros modificados según el alcance; dejar explícito qué fue análisis, borrador, escritura aprobada y resultado real.

## Reglas de decisión
- Análisis interno autorizado no equivale a permiso de envío, asignación o promoción de estados.
- Una tarea done no demuestra aprobación externa o pago; no reabrirla solo por prosa vieja.
- Ante fuente ambigua, guardar pregunta con evidencia, no convertirla en compromiso.

## Verificación
Cada hallazgo enlaza a bloque y destino; cada contradicción conserva evidencia vigente e histórica; cada aviso mantiene estado borrador o evidencia de autorización y readback. Handoff común sanitizado antes de delegar.

## Pitfalls
No convertir el rótulo de un puente de evidencia en promesa de API. No asumir aislamiento por perfiles o directorios cuando los resúmenes se comparten. No equiparar política aprobada con posprocesado ejecutado.

## Variantes
Solo análisis; propagación interna aprobada; comunicación externa tras control por audiencia. Para append concurrente usar el contrato de retornos seguros de la skill de bóveda.

## Referencias y alcance de evidencia
- [Procedencia y exclusiones](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
