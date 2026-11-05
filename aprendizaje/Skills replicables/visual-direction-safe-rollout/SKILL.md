---
name: visual-direction-safe-rollout
description: Use when visual references become environment changes.
version: 0.1.0
---

# Dirección visual y aplicación reversible

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{REFERENCIA}} | Archivo o captura autorizado para análisis visual |
| {{VERSION_BASE}} | Versión concreta desde la que se solicita iterar |
| {{IDENTIDAD_CANONICA}} | Decisiones vigentes y aprobaciones verificables |
| {{APLICACIONES}} | Superficies incluidas y compatibilidad por toolkit |
| {{RESPALDO}} | Ubicación de recuperación de ajustes |
| {{EVIDENCIA}} | Pruebas y capturas de ejecución |

## Propósito
Convertir una referencia visual en una composición propia y separar exploración, maqueta y tematización real. No exportar una identidad particular ni imponer preferencias personales.

## Cuándo usar
Iteraciones visuales de escritorios o aplicaciones, solicitudes de volver a una versión y propuestas con movimiento ambiental.

## Entradas
{{REFERENCIA}}, {{VERSION_BASE}}, {{IDENTIDAD_CANONICA}}, permiso para reutilizar activos y alcance de {{APLICACIONES}}.

## Pasos
1. Inspeccionar la referencia accesible e identificar lenguaje visual sin incorporarla como imagen final. Si un enlace no abrió, declarar que solo se analizó la captura aportada.
2. Leer identidad y aprobación vigentes. Distinguir dirección exploratoria de paleta aprobada. Si se pide volver, preservar composición de {{VERSION_BASE}} y cambiar solo lo solicitado.
3. Preparar composición original. Validar grado de dinamismo deseado: calma no equivale a inmovilidad. Situar movimiento en fondo, manteniendo lectura y controles estables.
4. Incluir pausa y movimiento reducido. Ejecutar y comprobar avance de fotogramas y pausa en {{EVIDENCIA}}, no inferir animación desde el código o una captura fija.
5. Inventariar compatibilidad y efectos en cada superficie de {{APLICACIONES}}. Entregar maqueta separada del plan de aplicación; una demo web no cambia nativamente todas las apps.
6. Antes de aplicar, solicitar autorización del cambio concreto, guardar {{RESPALDO}} y probar reversión. Verificar resultado real en cada superficie modificada y registrar lo no probado.

## Reglas de decisión
- Referencia no equivale a permiso de incrustación ni de copiar configuraciones ajenas.
- Cambiar una apariencia no autoriza migrar compositor, escritorio ni dotfiles.
- No usar aceptación de una maqueta como aprobación tácita de cambios runtime.

## Verificación
Conservar versión base y editable; comprobar composición solicitada, lectura estable, animación/pausa ejecutadas y compatibilidad por aplicación. Marcar consumo, uniformidad y tematización nativa como pendientes si solo hay maqueta.

## Pitfalls
No convertir gustos de una sesión en una identidad aprobada. No declarar dinámica por una imagen fija. No sustituir un enlace bloqueado por una lectura imaginada.

## Variantes
Exploración solo en archivo; demo interactiva; despliegue autorizado por aplicación. Cada variante declara su nivel de evidencia.

## Referencias y alcance de evidencia
- [Procedencia y límites](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
