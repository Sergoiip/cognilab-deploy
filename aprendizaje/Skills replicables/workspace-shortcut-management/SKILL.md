---
name: workspace-shortcut-management
description: Use when reordering workspaces or adding shortcuts.
version: 0.1.0
---

# Gestión de espacios y atajos de escritorio

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{SESION_OBJETIVO}} | Sesión gráfica y versión descubiertas |
| {{ID_ESPACIO}} | Identificador estable del espacio a mover |
| {{POSICION_DESTINO}} | Posición validada en el orden final |
| {{SCRIPT_EXISTENTE}} | Mecanismo persistente de atajos a inspeccionar |
| {{ID_ACCION}} | Identificador único para cada atajo |
| {{TECLA}} | Combinación validada como disponible |
| {{CLASE_VENTANA}} | Clase exacta, sensible a mayúsculas |
| {{LANZADOR}} | Lanzador instalado o proceso principal real |
| {{NOTA_CANONICA}} | Documento de orden y atajos |
| {{DIRECTORIO_PRUEBA}} | Directorio temporal autorizado |
| {{PREFIJO_LOG}} | Marcador único de verificación |
| {{SCRIPT_PRUEBA}} | Archivo temporal de una sola ejecución |
| {{NOMBRE_PRUEBA}} | Nombre único del script temporal |
| {{DESKTOP_ID}} | Identificador de lanzador instalado |
| {{CODIGO_TECLA}} | Código de atajo calculado con herramientas |
| {{INTERPRETE}} | Ejecutable principal del visor |
| {{VISOR}} | Archivo propio del visor, si existe |

## Propósito
Cambiar orden de espacios y atajos conservando objetos, pertenencia de ventanas, preferencias ajenas y un único mecanismo de lanzamiento. Incluye diagnóstico de entorno gráfico y preferencias de captura sin confundir despacho con éxito visual.

## Cuándo usar
Reordenar escritorios, ampliar acciones de enfocar-o-lanzar o ajustar cierre tras copia en una herramienta de captura. No usar para recrear espacios ni reemplazar toda la configuración por una plantilla.

## Entradas
Sesión y versión reales, configuración vigente, API documentada para esa versión, orden con identificadores estables, ventanas y pertenencias, acciones existentes y nota canónica. Inspeccionar todo antes de modificar; guardar respaldo de los archivos afectados.

## Pasos
1. Descubrir entorno gráfico, tipo de sesión y versión. Leer configuración de ventanas, atajos y lanzadores; consultar orden e identificadores de espacios. No inferir capacidades desde otra versión.
2. Confirmar en fuente primaria instalada una operación de mover el objeto espacio. Preparar script de una sola ejecución que resuelva identificador y nombre, compruebe cantidad esperada y capture IDs de ventanas y espacios de pertenencia.
3. Mover el objeto a la posición solicitada, no intercambiar nombres ni borrar/recrear espacios. Afirmar en el script que las pertenencias no cambiaron y emitir resultado estructurado con marcador único.
4. Cargar y ejecutar temporalmente; leer orden real y log de la aserción. Descargar el script de prueba. Si falla una precondición, no modificar; si cambia una pertenencia, detener y revisar sin hacer más cambios automáticos.
5. Para atajos, ampliar el mecanismo persistente existente sin duplicarlo y sin sobrescribir acciones ajenas. Descubrir clases reales de ventanas y lanzadores instalados; validar combinación disponible y calcular códigos con herramientas, no a mano.
6. Recargar solo el mecanismo afectado y consultar registro real de acción y etiquetas. Invocar el callback y verificar ventana/log, tanto enfocar existente como lanzar ausente. No cerrar ventanas del usuario solo para crear la condición de prueba; declarar esa rama pendiente si no puede probarse de forma segura.
7. Si el servicio de lanzamiento carece de entorno gráfico, verificar variables de sesión en el gestor de usuario sin exponer contenido de autorización. Ejecutar el proceso principal real en servicio transitorio con entorno correcto; no fijar nombres de archivos de autorización ligados a sesión ni usar un lanzador que termine y deje hijos sujetos a limpieza.
8. Para preferencia de cerrar tras copia/guardado, confirmar semántica de versión y preservar auto-guardado y auto-copia no solicitados. Evitar edición concurrente con una instancia que pueda guardar valores viejos; cerrar únicamente la instancia de inspección ociosa, escribir y leer la clave exacta.
9. Actualizar nota canónica; si hay visor flotante sin recarga automática, activar actualización y comprobar contenido completo por accesibilidad más captura fresca. Respetar sistema de coordenadas explícito del controlador al recurrir a interacción por píxeles.

## Decisiones
Un acuse de despacho no demuestra que apareció una ventana. Si la inspección no ve una ventana que el gestor sí reconoce, no afirmar prueba de clic/copia/pegado. Probar con el backend gráfico real: una inicialización en otro backend puede dar falso positivo.

## Verificación
Comparar orden por ID, pertenencias antes/después, disponibilidad y registro del atajo, ramas enfocada/ausente y visualización del documento actualizado. Separar configuración leída de prueba visual extremo a extremo y declarar toda rama no ejercitada.

## Pitfalls
Renombrar no equivale a mover; mayúsculas de clases importan; un servicio previo a la sesión puede carecer de entorno; limpiar un servicio cuyo lanzador terminó puede matar el visor hijo. Un booleano de lectura puede comunicarse por código de salida y no texto. No aplicar offsets globales a coordenadas locales de ventana.

## Variantes
Solo orden de espacios; acción enfocar-o-lanzar; reparación de entorno de servicio; preferencia de captura. Aplicar únicamente las ramas autorizadas y registrar límites.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
