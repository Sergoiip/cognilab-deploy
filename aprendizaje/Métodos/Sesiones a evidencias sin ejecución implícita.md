---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Sesiones a evidencias sin ejecución implícita

## Parámetros
FUENTES_CERRADAS, DIRECTORIO_RESULTADOS, ESTADO_PRIVADO, CATALOGO_DESTINOS, LIMITE_CONTEXTO, POLITICA_REINTENTOS y ANALIZADOR_SIN_HERRAMIENTAS deben definirse antes de implementar.

## Procedimiento
1. Inventariar formatos reales. Un estado «detenido» no prueba transcripción completa ni estabilidad de audio. Capturas manuales requieren adaptador explícito.
2. Conservar baseline histórico; no procesar automáticamente históricos que lleguen por sincronización. Exigir cierre declarado, fragmentos continuos, texto y rangos válidos.
3. Canonicalizar JSON y observar estabilidad en lecturas separadas; las huellas de tamaño/mtime del audio no certifican contenido acústico. Bloquear variantes divergentes sin elegir por mtime.
4. Dar al analizador solo datos delimitados como no confiables. Verificar que no disponga de herramientas; presupuesto interno y timeout externo separados. Exceso de contexto bloquea, no recorta silenciosamente.
5. Exigir salida estructurada, citas literales existentes, incertidumbres y destinos ya catalogados. Distinguir hecho, propuesta, decisión y compromiso. Un aviso sigue siendo borrador no enviado.
6. Releer la fuente después del análisis. Publicar un bundle versionado con recibo y hashes; staging y lectura posterior. Reinicio y reintento verifican el bundle sin repetir una petición ya completada.
7. Separar generación del resultado, distribución documental y ejecución operativa. Los retornos documentales requieren permiso aparte, respaldo previo y preservación exacta del prefijo.
8. No considerar flock protección frente a editores no cooperativos. Si se exige append concurrente seguro: rechazo de symlinks/hardlinks, verificación de ruta/inode/hash, protección efectiva de escritura disponible y comprobación posterior. Sin garantías, dejar parcial; no cerrar editores ni relajar controles.
9. Deduplicar retorno por sesión + destino, no por hash de revisión; revisión divergente queda para decisión humana. Un marcador solo no prueba append completo: contrastar bloque, prefijo y respaldo.

## Verificación y límites
Probar fuentes sintéticas, conflictos, escritura parcial, bundle corrupto, pérdida del acuse y recuperación sin LLM. No exportar transcripciones, logs del proveedor ni resultados históricos. Validación estructural no prueba suficiencia semántica, calidad de audio, actualización de tareas ni envío. No se entrega aquí un controlador de producción generalizado.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
