# Implementación de referencia

## Producto, configuración y límites
La fuente usa Voxtype con modelo local Whisper y un repositorio de notas. La política transferida es transcripción local obligatoria; no utilizar ChatGPT u otra API remota como reemplazo silencioso. La interpretación de una transcripción ya existente puede usar modelo conversacional autorizado y consumir tokens: no confundirlo con reconocimiento de audio.

Consultar ayuda y fuente oficial de la versión instalada antes de escribir claves. `audio.max_duration_secs` corresponde a dictado, no a reunión. La referencia habilita `[meeting]`, fragmentos de 30 segundos, duración máxima y almacenamiento explícitos. No asumir que esos nombres o valores son adecuados a otras versiones. Sesiones presenciales sin loopback ni cancelación de eco; diarización requiere prueba separada.

## Indicador y bibliotecas
La referencia necesita ambos ejecutables `voxtype-osd` y `voxtype-osd-gtk4` en PATH del servicio y `[osd] enabled = true`. Los assets oficiales tenían nombres `voxtype-VERSION-linux-x86_64-osd` y `...-osd-gtk4`: contrastar con publicación actual e instalada antes de descargar. Probar `--help` y `ldd` del frontend GTK4 con el `LD_LIBRARY_PATH` exacto del daemon.

Una dependencia faltante `libgtk4-layer-shell.so.0` impide arrancar aun si ambos binarios existen. Preferir paquete de distribución `gtk4-layer-shell`. Si la instalación privilegiada no es posible sin secretos, detener esa vía. Una alternativa de usuario requiere paquete oficial más firma separada verificada con llavero de distribución; extraer únicamente biblioteca versionada y symlink SONAME al directorio local ya contenido en el `LD_LIBRARY_PATH` del servicio. La ruta de referencia era `~/.local/share/voxtype/lib`; verificar {{DIRECTORIO_LIB_USUARIO}} en destino, no imponerla.

Con daemon ocioso, reiniciar y comprobar logs «OSD connected», luego `voxtype record start` y `voxtype record cancel`; verificar showing/hiding y recording→idle. Cancelar evita pegar transcripción incidental. Para capturar overlay con Spectacle desde shell sin entorno, transmitir únicamente valores reales `DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `XDG_SESSION_TYPE`, `XAUTHORITY` al subproceso. No publicar valores de autorización; inspeccionar captura visualmente.

## Reunión y respaldo
Voxtype inicia/para reuniones asíncronamente: consultar estado y metadatos completados, no solo exit status del comando. En ensayos referidos a versión 1.1.0 no se observaron chunks WAV tras terminar pese a `retain_audio=true`. Esto es una observación limitada, no prueba de imposibilidad en otras versiones.

Para sesiones importantes con permiso, `pw-record --rate=16000 --channels=1 {{RESPALDO_AUDIO}}` en servicio transitorio de usuario systemd con `RuntimeMaxSec` explícito y `KillSignal=SIGINT` permite respaldo independiente. Comprobar formato y límites requeridos por el caso, crecimiento real del archivo y detener tanto respaldo como reunión al finalizar. No se incluye audio real ni una garantía de retención.

## Recuperación y posprocesado
Patrón de recuperación: `voxtype --whisper-mode local --gpu-device {{DISPOSITIVO_COMPUTO}} --language {{IDIOMA}} transcribe {{ARCHIVO_AUDIO}}`, solo tras verificar ayuda e índices de GPU locales. El archivo se mantiene privado. Para audio largo, rangos continuos y checkpoints por chunk, salida de cada chunk y hash original sin cambios. Fragmentos en scratch, fuente y resultados finales en destino canónico.

La salida puede mezclar carga/progreso/ANSI con habla. En la versión de referencia, el texto reconocido se encontraba después de la línea `Transcription completed ...` y siguiente línea vacía: preservar raw, validar formato instalado y extraer con criterio explícito, nunca contar logs como voz. Los timestamps son por bloque. Whisper puede repetir o alucinar en silencio; marcar degradación y no fabricar decisiones desde repeticiones.

Si la sincronización renombra `.conflict*`, inspeccionar todas las variantes, cantidad de segmentos y cierre, conservarlas y usar explícitamente la completa. Para análisis se puede cargar una skill de acciones de reunión y protocolo autorizado del repositorio de notas; no se copia ese protocolo privado. Discord u otros canales permanecen en borrador hasta comprobar destinatarios y permiso. La autorización operativa de una organización de origen no se transfiere a otro entorno.

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
