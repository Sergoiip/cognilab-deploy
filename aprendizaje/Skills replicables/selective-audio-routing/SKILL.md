---
name: selective-audio-routing
description: Use when fixing per-device microphone routing.
version: 0.1.0
---

# Enrutamiento selectivo de dispositivos de audio

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{DISPOSITIVO_OBJETIVO}} | Identificador exacto del dispositivo a exceptuar |
| {{FUENTE_MICROFONO}} | Micrófono que debe recibir la aplicación |
| {{RUTA_CONFIG_USUARIO}} | Configuración no perteneciente al proveedor |
| {{RUTA_SCRIPT_USUARIO}} | Hook local y reversible, si es necesario |
| {{PERFIL_REPRODUCCION}} | Perfil de salida esperado |
| {{VOLUMEN_ORIGINAL}} | Nivel medido antes del cambio |
| {{APLICACION_CAPTURA}} | Aplicación cuya ruta se verifica |
| {{VENTANA_MUESTRA}} | Duración autorizada de muestra efímera |
| {{BACKUP_CONFIG}} | Copia privada de configuración anterior |

## Propósito
Resolver una selección errónea de micrófono o excepción de un dispositivo sin inutilizar micrófonos de otros equipos ni desactivar la conmutación global. Mantener audio de prueba efímero por defecto.

## Cuándo usar
Cuando un altavoz se ofrece como micrófono, una aplicación toma la fuente equivocada o la ganancia cambia al reconectar. No usar para reemplazar el sistema completo de audio ni grabar contenido sin autorización.

## Entradas
Inventario de fuentes, tarjetas, flujos de captura y perfiles activos; identificador físico objetivo; versiones del gestor y sus scripts instalados; mezcladores y configuración anterior. Distinguir selección incorrecta, silencio, saturación y fallo de aplicación antes de editar.

## Pasos
1. Inspeccionar inventario y estado real con herramientas del servidor de audio y del mezclador. Medir una captura cruda corta en memoria, sin guardar grabación por defecto. Señal presente no demuestra voz inteligible.
2. Si solo un altavoz debe quedar sin entrada, inspeccionar cómo crea nodos el gestor instalado. Un nodo sintético puede quedar fuera de reglas de monitor convencionales; no repetir reglas que no alcanzan ese ciclo de creación.
3. Si la API compatible lo permite, crear hook de usuario previo a la creación del micrófono sintético que bloquee únicamente el sujeto cuyo identificador coincide exactamente. Registrar componente y dependencia necesarios; no editar scripts del proveedor. Respaldar archivos y documentar reversión.
4. Reiniciar el gestor solo en una ventana autorizada sin capturas importantes. Reconectar dispositivo, restaurar perfil de reproducción de alta calidad y volumen original. El reinicio puede desconectar o seleccionar un perfil manos libres.
5. Verificar fuente por defecto y fuente efectiva por ID del flujo activo en la aplicación. Si existe preferencia de fuente fijada, limpiar solo esa preferencia para permitir selección normal de auriculares, no todas las preferencias.
6. Confirmar que la conmutación global a micrófono de auricular permanezca habilitada y repetir tras otra reconexión. La ausencia de un ensayo físico con auriculares se declara pendiente, no se infiere de una opción configurada.
7. Para saturación, ajustar ganancia en el servidor de audio, no solo en mezclador; la activación de ruta puede revertir este último. Repetir medición tras reconexión: pico, RMS, cantidad de muestras y proporción recortada. No tocar micrófono externo para corregir uno interno.
8. Probar reversión retirando únicamente los archivos de excepción propios y restaurando estado respaldado si corresponde. Reiniciar/reconectar con los mismos controles y verificar ruta sin excepción.

## Decisiones
Sin identificador inequívoco, no instalar excepción. Sin API confirmada de versión, detener el hook y declarar incompatibilidad. Si no se puede probar habla inteligible o auricular físico, limitar afirmación a métricas/configuración comprobadas.

## Verificación
Inventario antes/después, excepción aplicada solo al objetivo, ruta efectiva de captura, perfil y volumen restaurados, reconexión adicional y conmutación global preservada. Medir ganancia con herramientas y señalar si la inteligibilidad fue o no revisada. Confirmar que no se guardó audio incidental sin permiso.

## Pitfalls
Reglas de monitor no siempre abarcan nodos sintéticos. Un reinicio puede alterar perfil y volumen. Preferencias fijadas ocultan prioridad normal. Desactivar todos los micrófonos inalámbricos para excluir uno rompe auriculares. Una medición eléctrica no prueba calidad del habla.

## Variantes
Corrección de fuente sin código; excepción selectiva mediante hook de usuario; ajuste de ganancia; regresión después de actualización. Revalidar compatibilidad al cambiar versión.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
