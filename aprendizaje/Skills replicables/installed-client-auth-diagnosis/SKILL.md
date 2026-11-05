---
name: installed-client-auth-diagnosis
description: Use when installed clients disagree with source auth.
version: 0.1.0
---

# Diagnóstico de autenticación del cliente instalado

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{ARTEFACTO}} | Paquete instalado y metadatos reales del cliente |
| {{SCRATCH}} | Directorio aislado para inspección sin mutar instalación |
| {{REMOTO}} | Conexión exacta y rol final aprobado |
| {{EVIDENCIA}} | Logs acotados y observaciones sin secretos |

## Propósito
Investigar diferencias de autenticación entre versión instalada y checkout sin ejecutar ni mutar la aplicación empaquetada.

## Cuándo usar
Cuando un cliente instalado usa firmas IPC/preload o particiones de cookies distintas de las que sugiere la fuente local.

## Entradas
{{ARTEFACTO}}, versión, entrada main, autorización de lectura y {{REMOTO}}. No se necesitan contraseñas para inspección estática.

## Pasos
1. Inspeccionar metadatos del paquete instalado, entrada main, archivos empaquetados y recursos unpacked. Extraer solo a {{SCRATCH}} si hace falta; no ejecutar main como método de lectura.
2. Contrastar preload, IPC y contrato de autenticación reales con checkout. Una fuente local antigua no gobierna necesariamente el binario nuevo.
3. Distinguir formulario con sesión/cookie de cabecera HTTP Basic. El nombre visible del modo puede diferir del transporte; describir el contrato verificado, no inferirlo por etiqueta.
4. Si el rol Primary/secundario modifica partición de cookies, fijar {{REMOTO}} en el rol final aprobado antes de la prueba de login. Promover solo el registro no copia automáticamente cookies.
5. Para completar credenciales, usar almacén seguro soportado o interacción del usuario. Nunca escribir contraseña por DOM/CDP, ni intentar derivar una sesión desde tokens de otra partición.
6. Recoger {{EVIDENCIA}} de conexión en el contexto final, separando lectura estática, autenticación, recuperación de conexión y operación posterior. Sin prueba viva, informar diagnóstico y pendiente.

## Reglas de decisión
- Inspección read-only no autoriza activar depuración, relanzar app ni cambiar el remoto principal.
- Si no hay canal seguro de login, detenerse en vez de pedir una contraseña por chat.
- No aplicar equivalencias de modos de un cliente a otro sin contrastar versión instalada.

## Verificación
Artefacto y versión identificados; firmas verificadas sin ejecutar main; tipo de auth y partición final documentados; ninguna credencial en logs o automatización DOM. La revisión estática no prueba login exitoso.

## Pitfalls
No modificar instalación para inspeccionarla. No prometer que promoción de remoto traslada cookies. No confundir acceso a checkout con acceso al renderer instalado.

## Variantes
Diagnóstico estático; prueba viva con usuario presente; reproducción aislada si fue autorizada. Conservar el cliente real y sus sesiones intactos.

## Referencias y alcance de evidencia
- [Procedencia e implementación de referencia](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
