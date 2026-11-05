---
name: agent-runtime-boundaries
description: Use when agent runtimes or profiles diverge.
version: 0.1.0
---

# Diagnóstico de límites y runtimes de agentes

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{PERFIL}} | Perfil autorizado, sin extender el alcance a otros perfiles |
| {{RUNTIME}} | Ejecutable e intérprete realmente usados por la superficie afectada |
| {{SNAPSHOT_PRIVADO}} | Respaldo fuera de carpetas compartidas |
| {{PRUEBA_AUDIO}} | Clip autorizado para prueba de voz |
| {{JOB}} | Identificador del trabajo existente |
| {{DESTINO_PRUEBA}} | Entorno aislado sin credenciales de producción |

## Propósito
Diagnosticar discrepancias entre superficies y preservar identidad, datos y permisos al reparar. No es un manual de instalación del agente.

## Cuándo usar
Cuando un escritorio funciona distinto a la CLI, se migra un perfil, falla la voz o un cierre programado pierde continuidad.

## Entradas
Versiones instaladas, logs acotados, configuración efectiva sin secretos, autorización por cambio y muestras existentes. Leer references/runtime-y-voz.md y references/migracion-y-continuidad.md según el síntoma.

## Pasos
1. Resolver {{PERFIL}} y {{RUNTIME}} desde el proceso, logs y unidad de servicio; contrastar con la CLI del shell. Terminar con una matriz superficie → ejecutable → intérprete → estado, sin inferir equivalencia.
2. Leer la documentación y el código de la versión instalada antes de elegir una reparación. No ejecutar módulos principales para inspeccionarlos ni reiniciar el gateway que sostiene la sesión.
3. Separar fallo de modelo, herramienta, autenticación, transporte y representación. Un perfil nuevo puede heredar selección de proveedor sin heredar credenciales; revisar también auxiliares, delegación y fallbacks.
4. Preparar respaldo en {{SNAPSHOT_PRIVADO}} y una reversión. Aplicar únicamente cambios autorizados con la interfaz oficial de configuración, no reescrituras YAML completas.
5. Para voz, reproducir primero con {{PRUEBA_AUDIO}} en el intérprete real y después en la ruta de carga de la superficie. Ensayar habla y silencio por separado. No confundir una llamada de función con captura real de micrófono.
6. Para programación, leer {{JOB}}, reutilizarlo y verificar sus campos exactos después del cambio. La ejecución que pregunta no puede inventar las respuestas futuras.
7. Registrar evidencia por capa: configuración, prueba aislada, transporte real y respuesta humana. Lo no ejecutado queda pendiente, no aprobado.

## Reglas de decisión
- Cambiar de runtime solo si la divergencia está demostrada; no instalar dependencias en el entorno equivocado.
- Perfil lógico no significa aislamiento del sistema de archivos ni de credenciales de CLIs externas. Elegir aislamiento de HOME o de sistema según el riesgo.
- Una negativa de permiso o timeout de aprobación detiene esa escritura; no se elude por otra herramienta.
- Una migración debe permanecer offline o contenida en {{DESTINO_PRUEBA}} hasta cortar el emisor original.

## Verificación
Comprobar unidad e intérprete reales, estabilidad del proceso más allá del intervalo anterior de reinicio y logs de recuperación. Para voz, conservar resultado del clip y de la ruta de subida; declarar pendiente el primer mensaje real si no ocurrió. Para trabajos, leer horario, script, destinatario, habilitación y continuidad; exigir una respuesta real para afirmar el circuito conversacional.

## Pitfalls
- Importar un respaldo puede arrancar servicios y modificar bases o skills antes de que se revisen.
- Cookies preservadas de un sitio no demuestran sesión en otro; ciertas copias omiten almacenamiento de aplicaciones.
- Un aviso de clave desconocida no prueba que el runtime no la lea: contrastar fuente instalada y ejecución.
- No trasladar como hechos propios diagnósticos de límites de concurrencia ni promesas de autenticación de manuales sin procedencia local diferenciada.

## Variantes
Lectura diagnóstica sin cambios; reparación autorizada en una sola superficie; migración contenida con corte explícito. La matriz de evidencia es común.

## Referencias y alcance de evidencia
- [Runtime y voz](references/runtime-y-voz.md).
- [Migración y continuidad](references/migracion-y-continuidad.md).
- [Implementación de referencia y procedencia](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
