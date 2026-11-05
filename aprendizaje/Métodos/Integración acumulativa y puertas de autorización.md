---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Integración acumulativa y puertas de autorización

## Parámetros
| Parámetro | Configuración requerida |
|---|---|
| RAICES_AUTORIZADAS | Directorios propios expresamente autorizados |
| INVENTARIO_PRIVADO | Fuera del paquete; fuentes exactas, hashes y evidencias |
| DESTINO_REVISION | Árbol preparado, separado de la instalación |
| ESTADO_ANTERIOR | Manifiesto verificado de la entrega anterior |
| AUDIENCIA | Interna o externa y permisos de uso |
| RESPONSABLE_APROBACION | Persona que autoriza cada activación |

## Propósito y límites
Acumular mejoras sin confundir descubrimiento con revisión, paquete con instalación o prueba sintética con operación real. Una conversación, un nombre de archivo o una copia local no demuestra titularidad. El método no autoriza copiar plugins, datos de terceros ni activar servicios.

## Flujo
1. Enumerar únicamente las raíces autorizadas y registrar las carpetas podadas. Separar herramientas, métodos, referencias, datos operativos y resultados históricos. Conservar originales.
2. Mantener en privado por archivo: ruta exacta, tamaño, SHA-256 cuando esté permitido leerlo, nivel de revisión, evidencia de autoría/licencia, decisión y motivo. No leer credenciales para inventariarlas; registrar exclusión sin hash. No publicar este inventario.
3. Comparar identidades relativas y hashes contra el estado anterior: nuevo, modificado, sin cambio o retirado. Un archivo ausente no se borra automáticamente del historial ni del despliegue. Primera ejecución: declarar línea base, no inventar una diferencia histórica.
4. Autorizar el código solo con procedencia comprobada, lectura completa de todas sus dependencias propias y derecho de redistribución. Si falta una condición: pendiente, nunca copia preventiva. Dependencias de terceros se documentan mediante enlaces técnicos; no se incluyen bundles ni parches sin autorización de licencia.
5. Extraer la capacidad genérica antes de conservar una implementación. Sustituir rutas y ajustes por parámetros explícitos; eliminar reglas de negocio, nombres privados, identificadores, hosts, correos, tokens y estados reales. No basta reemplazar una marca si quedan datos en fixtures o referencias.
6. Construir en staging aislado y probar primero fallos: entrada incompleta, duplicados, corrupción, ruta insegura y reintento. No probar contra tareas, grabaciones, calendarios o sincronizadores reales. Evitar imports con efectos laterales.
7. Escanear texto, referencias, nombres y manifiesto; revisar manualmente coincidencias. Cada artefacto exportable debe tener alcance de pruebas y origen. Rechazar symlinks, archivos ocultos, binarios y runtime.
8. El empaquetador general usa una lista positiva de artefactos aprobados, recalcula hashes, evita duplicados y verifica CRC y bytes del ZIP. El inventario privado y resultados de pruebas permanecen fuera. Este módulo no crea un ZIP por separado: lo integra el empaquetador del paquete principal.
9. Actualizar el estado de abstracción solo tras pasar controles. Registrar pendientes por fuente cambiada. La aceptación del paquete no habilita instalación, cron, sincronización, envío ni promoción de un respaldo.
10. Para integrar en otro equipo: revisión del plan, copia de seguridad, prueba aislada, permiso de activación, lectura del destino exacto y reversión verificada. Detenerse si los permisos o APIs no coinciden.

## Matriz de estado
Descubierto → estructura inspeccionada → contenido revisado → derechos comprobados → generalizado → probado → empaquetado → instalación autorizada → verificado en destino. Cada paso requiere evidencia distinta; no promover por inferencia.

## Aceptación
Conteos calculados, decisiones sin huecos, ausencia de datos privados en el árbol exportable, referencias separadas, fixture reproducible y lista explícita de pendientes. Cobertura declarada por raíz y por nivel; nunca «todo el equipo» por haber enumerado algunas carpetas.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
