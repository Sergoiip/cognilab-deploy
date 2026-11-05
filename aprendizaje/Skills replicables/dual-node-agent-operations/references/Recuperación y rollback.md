# Recuperación y rollback

## Preparar antes del corte
Identificar último estado válido, ubicación privada de respaldos, versiones compatibles, mecanismo de aislamiento del principal y canal alternativo. Registrar qué procesos escriben estado, envían mensajes o ejecutan cron. Proteger credenciales con permisos adecuados. No incluirlas en evidencias.

## Fallo antes de activar destino
Mantener origen como único principal. Si se detuvo, restaurar su operación solo después de confirmar que destino no opera ni puede reactivarse automáticamente. Preservar paquetes y logs fallidos para diagnóstico.

## Fallo después de activar destino
El destino puede contener cambios nuevos: no restaurar ciegamente un snapshot anterior. Aislar su operación, capturar de forma consistente el estado más reciente, verificar compatibilidad y restaurar en origen con ambos escritores detenidos. Activar únicamente el equipo elegido y probar canales y tareas.

## Caída real del principal
1. Determinar qué se sabe y qué no: falta de ping no prueba apagado.
2. Confirmar aislamiento efectivo del principal antes de promover el secundario. Si no es posible, mantener bloqueo y resolver; no correr el riesgo de dos principales.
3. Verificar generación, origen, integridad y antigüedad del respaldo. Informar posible pérdida desde esa captura y solicitar autorización de recuperación.
4. Restaurar consistentemente en runtime compatible, ajustar rutas y verificar dependencias.
5. Activar canales y cron solo en el sustituto y comprobar ejecución única.
6. Registrar el nuevo dueño. El equipo recuperado no debe reasumir automáticamente.

## Retorno
Respaldar el estado actualizado del sustituto, detener escritores y transferirlo al destino elegido. Aislar el sustituto antes de activar el otro. Comprobar continuidad y renovar copias en la dirección correcta. No fusionar bases ni historiales manualmente como sustituto de un procedimiento compatible.

## Ensayo y medidas
Probar restauración aislada, corrupción rechazada, fallo de transferencia sin perder el último éxito, promoción controlada y retorno. Medir antigüedad de datos y tiempo de recuperación. Un objetivo de copia cada minuto no demuestra pérdida máxima de un minuto.

## Límite físico
Si ambos equipos están apagados o no hay un sustituto utilizable, no hay continuidad. Este diseño de dos equipos con promoción manual no es por sí mismo alta disponibilidad ni recuperación automática.
