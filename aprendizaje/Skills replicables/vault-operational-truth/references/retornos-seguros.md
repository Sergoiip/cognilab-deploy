# Retornos documentales trazables

## Contrato
Un retorno agrega un hallazgo autorizado a un proyecto existente; no reescribe contenido anterior, no crea un gestor de tareas alterno y no publica avisos. Resolver catálogo de proyectos permitido, política de destino y backup antes de escribir. Bundle de evidencia inmutable y acuse de aplicación son artefactos separados.

## Preparación
1. Reutilizar la implementación canónica y leer sus límites en vez de crear otro posprocesador. La presente skill no distribuye ese programa ni presupone que esté instalado.
2. Deduplicar por sesión y proyecto, no por revisión o hash de fuente. Una revisión divergente conserva el retorno previo y abre revisión humana.
3. Guardar respaldo verificable por hash fuera de rutas indexadas. Enlazar fuente/bloque, hallazgo, decisión o pregunta, proyecto/proceso y resultado; tareas solo mediante autoridad aprobada.
4. Probar recuperación con archivos reales en scratch antes de escribir en proyectos. Los reintentos de aplicación deben poder usar análisis ya persistido, sin volver a invocar un modelo.

## Concurrencia y fallos
flock protege solo escritores que cooperan. Si el contrato exige impedir escrituras externas durante append local, evaluar leases del sistema operativo y detenerse si no están disponibles; no prometer portabilidad ni atomicidad distribuida. En Linux verificar soporte y manejo de ruptura del lease.

Rechazar enlaces simbólicos en cada componente, comparar inode y ruta y comprobar bytes después. Un directorio reemplazado durante la operación puede cambiar el objetivo aun conservando el mismo nombre. Ante esa carrera registrar estado parcial y no sobrescribir el archivo nuevo.

## Prueba de éxito
No basta con encontrar un marcador: verificar el bloque completo, el prefijo original byte a byte y el respaldo. Registrar por destino aplicado, ya presente, pendiente o parcial. Mantener acuses separados del bundle para que un reintento no modifique la evidencia original. No elevar estado de una tarea, asignar responsables o enviar mensajes desde un retorno ambiguo.

Origen: generalización de lecciones locales de append seguro y recuperación documental.
