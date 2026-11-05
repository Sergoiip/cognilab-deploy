# Aceptación y evidencia

Usar una copia por instalación. No marcar casillas por haber leído este documento.

## Registro mínimo por prueba
ID; fecha y zona horaria; equipo/rol; perfil; versión; acción autorizada; resultado esperado; resultado observado; evidencia sin secretos; estado (pendiente/aprobada/fallida/no aplica); responsable. «No aplica» requiere motivo. Separar evidencia técnica de aceptación del cliente.

## Comprobaciones
- [ ] Roles, alcance y fuente canónica confirmados.
- [ ] Identidad SSH contrastada y acceso por Tailscale comprobado.
- [ ] Backend autenticado y no expuesto públicamente; puertos documentados.
- [ ] Ambos estados respaldados; integridad y restauración aislada comprobadas.
- [ ] Compatibilidad, rutas, skills y dependencias verificadas.
- [ ] Desktop remoto conserva conexión local diferenciada.
- [ ] Historial reciente y respuesta real del modelo comprobados.
- [ ] Comandos, archivos, navegador y escritorio probados por separado, o límites declarados.
- [ ] Integraciones requeridas probadas; conexión MCP no sustituye prueba funcional.
- [ ] Sincronización sin solapamiento, con exclusiones, borrado y restauración probados.
- [ ] Corte autorizado; todos los escritores inventariados y principal anterior aislado.
- [ ] Canal real: una sola respuesta, sin duplicados.
- [ ] Automatización de prueba autorizada: una sola ejecución.
- [ ] Reinicio real y dependencias de sesión gráfica comprobados.
- [ ] Principal funciona sin el secundario; capacidades ausentes se declaran.
- [ ] Respaldo periódico reciente y alerta por obsolescencia comprobados.
- [ ] Conmutación manual real, aislamiento y recuperación probados.
- [ ] Retorno preserva cambios posteriores y no reactiva dos principales.
- [ ] Antigüedad recuperable y duración de recuperación medidas.
- [ ] Efectos laterales, pendientes y rollback entregados.
- [ ] Aceptación expresa del cliente registrada.

## Reglas de cierre
«Configurado» no equivale a «probado». Servicio habilitado no prueba recuperación tras reboot. Snapshot íntegro no prueba continuidad de canales. Un ensayo aislado no demuestra una conmutación real. Una prueba pendiente crítica impide declarar la migración completa.

## Evidencia del kit, no del despliegue
La verificación del ZIP comprueba contenido, hashes y ausencia de rutas peligrosas; no certifica funcionalidad de Hermes, conectividad entre equipos ni resultados de un cliente.
