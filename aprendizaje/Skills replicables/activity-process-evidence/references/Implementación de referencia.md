# Implementación de referencia

## Herramientas y descubrimiento
La fuente utiliza ActivityWatch y entrega notas enlazadas en un repositorio de conocimiento. Consultar el inventario mediante `GET {{API_ACTIVIDAD}}/api/0/buckets/` y seleccionar los buckets `currentwindow` y `afkstatus` correspondientes al mismo host. La unión de eventos `not-afk` define la máscara activa, no una segunda medida que sumar. Resolver localmente el endpoint; no se conserva la dirección del entorno original.

El generador previo no forma parte de la exportación: localizar {{GENERADOR}}, leerlo y comprobar formatos antes de ejecución. La persistencia puede ser en cualquier sistema de notas con enlaces comprobables; no depende de un repositorio particular.

## Intervalos
Usar intervalos semiabiertos, recortar al período y unir presencia antes de intersectar. Registrar regla de resolución de ventanas simultáneas; si no es defendible, reportar el solape como ambigüedad, no asignarlo dos veces. Si se cambia de recolector o sesión gráfica, verificar que realmente produce títulos utilizables sin elevar permisos a ciegas.

## Límites de evidencia
El conocimiento transferido es un procedimiento, no la certificación de un equipo o recolector receptor. No contiene eventos, títulos ni resultados de informes previos. Las hipótesis asistidas por modelos deben recibir solo datos autorizados.

## Documentación pública
- FAQ técnica: https://docs.activitywatch.net/en/latest/faq.html
- Fuente alternativa si falla la extracción: https://raw.githubusercontent.com/ActivityWatch/docs/master/src/faq.rst

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
