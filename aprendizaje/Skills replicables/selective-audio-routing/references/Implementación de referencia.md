# Implementación de referencia

## Diagnóstico
La referencia usa Linux, PipeWire, compatibilidad PulseAudio y WirePlumber. Inspeccionar JSON de `pactl` para sources/cards/source-outputs, `wpctl status`, dirección Bluetooth, perfil activo, versión WirePlumber y `amixer`. Invocar CLI mediante la herramienta de ejecución; comprobar ayuda/versiones antes de construir comandos dependientes de opciones. Muestrear crudo con `parec` a memoria, sin crear archivos por defecto. Calcular pico, RMS, número de muestras y proporción recortada según formato PCM real; no inventar valores.

## Excepción técnica de versión
En la referencia WirePlumber 0.5.18 crea loopbacks de micrófono Bluetooth fuera de reglas de monitor. Leer `/usr/share/wireplumber/scripts/monitors/bluez/create-loopback-node.lua` instalado. Un `SimpleEventHook` anterior a `monitor/bluez/create-loopback-node` puede detener `create-bluez-device-loopback-node` exclusivamente para un sujeto con `api.bluez5.address == {{DISPOSITIVO_OBJETIVO}}`.

Registrar `script/lua` en `wireplumber.components` y requerir el hook que provee en el perfil `main`. Colocar scripts propios en `~/.local/share/wireplumber/scripts/` y configuración en `~/.config/wireplumber/wireplumber.conf.d/`, no editar vendor. No se incluye una implementación Lua ni la dirección, modelo, alias o nombres privados del dispositivo fuente. El diseño de hook debe comprobarse contra el API instalado antes de escribir código.

## Reconexión y ganancia
Tras reinicio, reconectar y seleccionar A2DP en vez de manos libres cuando ese sea el perfil esperado; restaurar volumen previo. Revisar fuente efectiva de un source-output activo, no solo default. La fuente documenta `wpctl clear-default 1` para limpiar solo preferencia de fuente fijada: confirmar semántica con la ayuda local antes de usarla. Confirmar `bluetooth.autoswitch-to-headset-profile` verdadero. Sin auricular físico no declarar su comportamiento ejercitado.

Preferir `pactl` para ganancia de micrófono cuando el mezclador sea revertido al activar ruta. Repetir métricas tras reconexión y no confundir dispositivos internos y externos.

## Reversión y evidencia
La excepción de la implementación original se ejercitó en la versión indicada; no acredita otras versiones ni el equipo receptor. Para deshacer, retirar solo el archivo de configuración y el script propios, reiniciar y reconectar bajo autorización. Conservar respaldo de configuración sin copiar datos privados a la entrega.

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
