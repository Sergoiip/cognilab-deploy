---
name: local-meeting-transcription
description: Use when configuring local meeting transcription.
version: 0.1.0
---

# Captura de reuniones y transcripción local

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{MODELO_LOCAL}} | Modelo ya disponible para transcripción sin API remota |
| {{IDIOMA}} | Idioma confirmado de transcripción |
| {{DISPOSITIVO_COMPUTO}} | Dispositivo y índice reales comprobados |
| {{DESTINO_SESIONES}} | Archivo canónico privado de sesiones |
| {{PROTOCOLO_CIERRE}} | Procedimiento de análisis y distribución autorizado |
| {{DURACION_FRAGMENTO}} | Duración de fragmento confirmada con herramienta |
| {{DURACION_MAXIMA}} | Límite explícito de reunión y respaldo |
| {{MODO_CAPTURA}} | Presencial o remoto, entradas y loopback autorizados |
| {{CONFIGURACION}} | Archivo y claves compatibles de la versión instalada |
| {{DIRECTORIO_LIB_USUARIO}} | Ubicación local ya usada para bibliotecas, si aplica |
| {{RESPALDO_AUDIO}} | Archivo privado independiente y autorizado |
| {{DESTINATARIOS}} | Canales y receptores verificados, sin direcciones aquí |
| {{SCRATCH}} | Área temporal autorizada para fragmentos y ensayos |
| {{ARCHIVO_AUDIO}} | Fuente de audio privada y autorizada |

## Propósito
Capturar sesiones y obtener transcripción mediante un modelo local, con estado visible, respaldo cuando se requiera y análisis posterior separado. No gastar cuota de transcripción remota ni enviar audio por fallback silencioso. El análisis semántico de texto existente es una fase distinta que puede consumir tokens si está autorizado.

## Cuándo usar
Configurar reuniones, indicador de grabación, recuperación local de audio o cierre de sesión. No confundir dictado con reunión ni instalar automatización de distribución sin verificar su alcance.

## Entradas
Versión y ayuda CLI reales, configuración, servicio de usuario, modelo descargado, límites y modo de captura, protocolo de cierre y permisos. Identificar si hay grabación activa antes de toda modificación.

## Pasos
1. Inspeccionar versión, ayuda, claves aceptadas y servicio; contrastar con fuente oficial de esa versión. Confirmar transcripción local. Ante fallo local, exponer bloqueo y mantener pendiente; nunca cambiar silenciosamente a API remota.
2. Separar límites de dictado y reunión. Habilitar reunión con fragmentos acotados, duración máxima explícita y destino canónico. Para presencial desactivar loopback y cancelación de eco; para remoto definir qué señales se autorizan. No prometer identificación de hablantes sin ensayo.
3. Si el indicador está configurado pero ausente, probar ejecutables y dependencias con el mismo entorno de bibliotecas del daemon antes de tocar preferencias. Comprobar tanto despachador como frontend y sus nombres esperados por la versión.
4. Preferir paquete oficial del sistema para bibliotecas faltantes. Si requiere credenciales de elevación, no pedir secretos ni elevar por otra vía. Como alternativa solo autorizada, descargar paquete oficial y firma separada, validar con llavero de distribución y extraer únicamente biblioteca versionada y enlace de nombre de biblioteca a un directorio local ya previsto por el servicio; no ejecutar el paquete completo ni modificar proveedor.
5. Reiniciar solo con dictado ocioso y sin reunión activa. Verificar frontend iniciado, conexión del indicador en logs y ensayo breve iniciar/cancelar con mostrando/ocultando y grabando→ocioso. Cancelar evita pegar voz incidental en la aplicación del usuario.
6. Para captura visual desde herramienta sin entorno de pantalla, transmitir al subproceso solo variables gráficas reales del daemon y verificar overlay en imagen. No copiar su entorno completo ni secretos.
7. Inicio y parada de reunión son asíncronos: esperar y leer estado más metadatos terminados antes de reiniciar o afirmar fin. Ensayar más de un fragmento y revisar transcripción completada. Declarar claramente si la grabación real está activa o detenida.
8. No confiar solo en una opción de retención de audio. Para sesiones importantes y con autorización, iniciar respaldo independiente con límite temporal y cierre por señal ordenada; comprobar crecimiento real del archivo. Al acabar detener tanto reunión como respaldo y verificar ambos estados.
9. Recuperar audio existente exclusivamente con transcripción local y opciones/dispositivos comprobados. Para audio largo, dividir en fragmentos acotados reanudables, conservar texto y rangos por fragmento, comprobar continuidad de cobertura completa y huella intacta del original. Temporales en scratch y artefactos definitivos en archivo canónico.
10. Separar salida reconocida de logs de carga, progreso y control de terminal; preservar salida cruda privada. Rangos por fragmento son de bloque, no marcas por palabra. Una cobertura completa no acredita exactitud: marcar bloques degradados, repetición o alucinación en silencio y revisar compromisos ambiguos antes de crear tareas.
11. Si la sincronización crea variantes en conflicto, inspeccionar número de segmentos y finalización, conservar todas y seleccionar explícitamente la fuente completa. No afirmar pérdida ni sobrescribir por defecto.
12. Para cierre, verificar fin efectivo de captura y texto estable. Procesar automáticamente solo reuniones y solo dentro de autorización explícita; no cada dictado. Un texto ausente queda pendiente visible. Mantener notificaciones como borradores hasta confirmar canal, destinatarios, permisos y autorización de envío; separar análisis, borrador y entrega real comprobada.

## Decisiones
Sin fin confirmado no procesar cierre. Sin texto completo no marcar análisis terminado. Sin diarización no inferir hablante por un nombre pronunciado. Sin prueba de audio retenido no afirmar respaldo. No reiniciar durante una grabación real. No reproducir voz incidental en chat.

## Verificación
Comprobar ejecutables, bibliotecas y conexión del indicador, ensayo iniciar/cancelar, captura de más de un fragmento, estado final y metadatos completos; verificar crecimiento y parada del respaldo cuando aplique. Conciliar rangos y cantidad de fragmentos con duración, huella del original y calidad revisada. Distinguir pruebas, sesión real, configuración, cobertura textual y exactitud; reportar bloqueos y ramas pendientes sin convertirlas en garantías.

## Pitfalls
Límites de dictado no limitan reuniones. Dos binarios presentes pueden fallar por una biblioteca ausente. Un acuse de parada no significa finalización. Retener audio configurado no demuestra archivos existentes. Logs pueden parecer texto de transcripción; repetición puede ser alucinación. Una variante de conflicto no significa necesariamente pérdida.

## Variantes
Solo dictado local; reunión presencial; reunión remota con señales autorizadas; recuperación por fragmentos; respaldo independiente; cierre con análisis autorizado y distribución inicialmente en borrador. Activar únicamente variantes dentro del pedido y permisos.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
