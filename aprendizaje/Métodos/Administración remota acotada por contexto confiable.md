---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Administración remota acotada por contexto confiable

## Parámetros
AMBITO_AUTORIZADO, IDENTIDAD_OPERADOR, IDENTIDAD_SERVICIO, RUTAS_PERMITIDAS, CAMPOS_PERMITIDOS, ALMACEN_AUDITORIA y RESPONSABLE_RECUPERACION deben acordarse sin secretos en el paquete.

## Procedimiento
1. Separar permisos del transporte y política del adaptador. Que una cuenta tenga permisos amplios no convierte el adaptador en administrador general. Inventariar otras rutas de escritura que la misma política no cubre.
2. Resolver autorización desde un contexto que el ejecutor vincula a la sesión, nunca desde actor, ámbito o una confirmación suministrados por el modelo. Rechazar campos desconocidos y denegar por defecto contextos programados o delegados no autorizados.
3. Fijar origen, rutas y métodos; rechazar redirecciones y validar identificadores antes de interpolarlos. Obtener el secreto desde su almacén autorizado sin registrarlo y contrastar la identidad real del servicio antes de actuar.
4. Construir payloads explícitos solo con campos permitidos. Validar pertenencia y tipo de recursos enlazados antes de modificar, no solo sus identificadores. No ofrecer permisos, moderación o borrado general por comodidad.
5. Serializar operaciones y registrar intento y resultado de manera durable. Auditoría: acción, campos y resultado, sin texto de mensajes, secretos ni excepciones arbitrarias. Si no puede conservarse la evidencia protegida, detenerse antes del efecto.
6. Comprobar el recurso exacto tras cada escritura. Un timeout después de un envío es un estado ambiguo: inspeccionar antes de reintentar; no repetir automáticamente una creación o borrado.
7. Si se permite limpieza de pruebas, exigir prueba persistente de creación por ese adaptador, pertenencia, tipo y ausencia de contenido; comprobar después la desaparición. Un prefijo de nombre por sí solo no autoriza borrar. No presentar un script de prueba como garantía de limpieza si puede salir antes de ejecutarla.
8. Probar política y transporte con fixtures: identidad incorrecta, contexto no autorizado, ruta inválida, recurso ajeno, payload desconocido, error de lectura posterior y auditoría no disponible. Pruebas reales de escritura requieren permiso separado y plan de recuperación.

## Límites
Un marcador local protege de activación accidental, no de código que ya dispone de acceso local completo. La prueba del adaptador no demuestra que el servicio haya limitado otros clientes. Una bitácora existente no prueba que todas las operaciones previas estén cubiertas. No se incluye ni activa un plugin de administración de producción.

Origen: síntesis nueva de controles observados en un adaptador local de administración y su verificador; sin código ni identificadores privados de las fuentes.
