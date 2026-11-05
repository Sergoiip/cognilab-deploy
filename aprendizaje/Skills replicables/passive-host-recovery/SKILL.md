---
name: passive-host-recovery
description: Use when designing passive host recovery.
version: 0.1.0
---

# Recuperación pasiva de un host

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{REVISION_FUENTE}} | Revisión exacta y verificable del programa |
| {{FUENTES_DEPENDENCIAS}} | Bloqueos y dependencias requeridas |
| {{HOST_PRIMARIO}} | Identificador privado resuelto fuera del documento |
| {{IDENTIDAD_CONEXION}} | Referencia a credencial existente; nunca su contenido |
| {{CLAVES_HOST_FIJADAS}} | Archivo persistente de claves de host verificadas |
| {{LISTA_PERMITIDA}} | Estado del perfil autorizado para respaldar |
| {{STAGING_PRIVADO}} | Directorio de preparación restringido |
| {{DESTINO_GENERACIONES}} | Repositorio de generaciones y último éxito |
| {{POLITICA_RETENCION}} | Límites y frecuencias medidos |
| {{HOGAR_RECUPERACION}} | Destino nuevo, nunca el perfil activo |
| {{EVIDENCIA_AISLAMIENTO}} | Prueba positiva reciente de aislamiento físico |
| {{RESPONSABLE_REANUDACION}} | Rol que autoriza promoción y envíos |

## Propósito
Mantener una copia pasiva recuperable de un agente con estado, sin ejecutar un segundo actor ni producir entregas duplicadas. El respaldo puede contener secretos y exige controles privados; esta skill solo contiene el método, no copias ni credenciales.

## Cuándo usar
Para recuperación entre hosts con un primario y un repuesto pasivo. No usar para alta disponibilidad con promoción automática ni sincronización bidireccional de bases activas.

## Entradas
Revisión exacta, dependencias congeladas, conectividad ya autorizada, lista permitida de un único perfil, inventario de bases y archivos, política de retención y evidencia física para una eventual promoción.

## Pasos
1. Inspeccionar revisión instalada y construir un runtime aislado desde un archivo de fuente de esa revisión con dependencias congeladas y extras de mensajería necesarios. Comparar hashes del archivo y bytes de fuentes instaladas. Probar importaciones y CLI con un hogar temporal aislado; evitar comandos que puedan iniciar servicios por efecto lateral.
2. Configurar extracción con identidad existente y claves de host fijadas fuera del directorio temporal. Probar bajo el mismo contexto restringido que tendrá la tarea, no solo en una consola interactiva. No recopilar contraseñas ni desactivar validación del host.
3. Respaldar cada base con su API de copia consistente y conexiones de origen de solo lectura; ejecutar integridad y contar filas por tabla. No copiar bases activas con sus archivos de diario mediante sincronización ciega. La consistencia es por base, no una transacción global de todo el hogar.
4. Aplicar lista permitida: identidad, configuración, autenticación, claves de bóveda, memorias, skills, scripts, extensiones, programación y sesiones del perfil autorizado. Excluir otros perfiles, cachés, ejecutables administrados, bloqueos, identificadores de proceso y espacios de trabajo duplicados de tableros. Revisar sensibilidad de cada inclusión.
5. Medir transferencia, tamaño y carga antes de fijar cadencia. Preparar en directorio privado, generar manifiesto completo con tamaño y huella criptográfica por archivo y verificarlo antes de publicar atómicamente generación y puntero de último éxito. Un fallo conserva el último éxito anterior.
6. Restringir directorios a acceso exclusivo y archivos a lectura/escritura del propietario. Mantener retención acotada frecuente, horaria y diaria según coste. El temporizador de copia no puede promover ni iniciar el agente.
7. Para promover exigir evidencia física positiva, reciente y verificable de aislamiento del primario. Un fallo de conexión o ping nunca basta. Rechazar si hay puertos del primario accesibles o si ya existe una puerta de enlace del agente en el repuesto.
8. Restaurar en un hogar nuevo. Poner en cuarentena tareas programadas, tableros, bandejas de salida y hooks; arrancar pausado hasta revisar entregas pendientes, arrendamientos activos, rutas absolutas, autenticación y extensiones. Reanudar solo con autorización explícita.
9. Hacer simulacros sin conexión: integridad y conteos restaurados, huellas de memoria y skills, rechazo de corrupción, conservación del último éxito ante transferencia fallida y negativa de promoción con primario vivo. Etiquetarlos como simulación, no como caída real.
10. Al regresar el primario, mantenerlo aislado, capturar ambos estados y reconciliar manualmente sesiones, entregas y tareas autoritativas. No mezclar bases bidireccionalmente ni promover hardware retornado automáticamente.

## Decisiones
Sin evidencia de aislamiento, no promover. Sin validación de manifiesto o integridad, no publicar. Sin hogar de recuperación separado, bloquear restauración. Sin consentimiento para datos sensibles, limitar lista permitida y declarar recuperación incompleta.

## Verificación
Confirmar bytes del runtime, integridad y conteos por base, manifiesto completo, permisos, publicación atómica y conservación ante fallos. Verificar que el repuesto permanezca pasivo y que los controles de promoción rechacen escenarios inseguros. Separar pruebas simuladas, pruebas reales y aspectos no ejercitados; no garantizar recuperación por un simulacro exitoso.

## Pitfalls
La conexión interactiva puede cargar configuración prohibida en un servicio restringido. Un hogar copiado puede activar cron, reenvíos o plugins al arrancar. Una copia consistente de cada base no garantiza consistencia cruzada. Retenciones ilimitadas pueden llenar el disco. Un reinicio de red no prueba aislamiento físico.

## Variantes
Solo copia pasiva; ensayo de restauración desconectada; promoción supervisada con pausa; retorno al primario con reconciliación manual. No se incluye failover automático.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
