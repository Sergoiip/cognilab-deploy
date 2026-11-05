---
name: calendar-and-sync-safety
description: Use when calendar edits or folder sync need proof.
version: 0.1.0
---

# Calendario y sincronización con identidad verificada

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{CUENTA}} | Identidad autorizada que debe comprobarse en destino |
| {{OCURRENCIA}} | Evento y alcance de recurrencia aprobados |
| {{ARBOLES}} | Raíces exactas autorizadas para sincronización |
| {{ESTADO_PERSISTENTE}} | Listados, locks y filtros fuera de cache podable |
| {{BACKUPS}} | Versiones de recuperación fuera de cada raíz sincronizada |
| {{SERVICIO}} | Unidad y temporizador concretos autorizados |

## Propósito
Evitar escrituras en otra identidad o serie y configurar sincronización recuperable sin exponer secretos. No es un manual general de suite ofimática ni autorización para conectar cuentas.

## Cuándo usar
Edición de una ocurrencia en navegador existente o configuración y reparación de sincronización recurrente de carpetas.

## Entradas
Cuenta y calendarios autorizados, {{OCURRENCIA}}, alcance unidireccional o bidireccional, {{ARBOLES}}, política de conflictos y exclusiones. Consultar references/sync-contrato.md para operaciones de archivos.

## Pasos
1. Verificar {{CUENTA}} en la página real antes de escribir. Un título de ventana o copia del navegador puede estar desconectada o en otro perfil. Usar solo un endpoint de depuración ya habilitado y consentido; no habilitarlo ni aceptar diálogos por rutina.
2. Esperar inputs reales del editor. Si el helper no cambia el campo, enfocar el input observado, seleccionar su contenido, insertar texto con la interfaz soportada y salir con Tab. Leer value antes de guardar: un evento sintético puede no actualizar el modelo.
3. Elegir explícitamente alcance de {{OCURRENCIA}}. Esperar cierre y leer evento guardado; si el organizador edita calendario secundario, comprobar también copia invitada antes de modificarla otra vez.
4. Para sync, inspeccionar herramientas y contrato de {{ARBOLES}}, identificar cuenta remota y excluir secretos por contenido y esquema, no solo nombre.
5. Preparar {{ESTADO_PERSISTENTE}}, filtros estables, sentinelas y {{BACKUPS}}; revisar dry-run después de la última edición de filtros, no una simulación anterior.
6. Automatizar únicamente si está autorizado {{SERVICIO}}. Ensayar ida, vuelta y borrado de un archivo de prueba propio mediante el servicio real; comprobar recuperación y siguiente disparo tras finalizar.
7. Documentar pausa, reanudación, límites y lectura de estado. Nunca sustituir una escritura bloqueada o permiso agotado por un camino alterno.

## Reglas de decisión
- Cuenta remota nombrada no prueba identidad autenticada.
- Eventos duplicados pueden ser reflejos de la misma invitación; verificar antes de editar ambos.
- Sincronización bidireccional, backup unidireccional y navegación de archivos son contratos diferentes.
- No activar resync/force automático ni nuevas cuentas, carpetas o autoarranque fuera del alcance aprobado.

## Verificación
Leer la ocurrencia exacta y preservar eventos ajenos. Para sync comprobar igualdad de archivo de ida/vuelta, borrado y versión de recuperación; ejecutar comparación completa con mismos filtros, ausencia de secretos en destino y salud/estado del timer. La autenticación actual no garantiza continuidad futura del cliente OAuth.

## Pitfalls
- Timeouts de autorización no equivalen a permiso para reintentar por otra ruta.
- Una API o montaje navegable no implementa sync recurrente.
- Un timer activo con oneshot en curso puede mostrar siguiente disparo desconocido; esperar resultado.
- Copiar data.json puede filtrar tokens aunque su nombre parezca inocuo.

## Variantes
Calendario: modificación puntual leída de vuelta. Sincronización: contrato y fixtures de ida/vuelta. Recuperación de notas y dibujos: consultar conflicts en la skill de bóveda del paquete.

## Referencias y alcance de evidencia
- [Contrato de sincronización](references/sync-contrato.md).
- [Procedencia e implementación](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
