---
name: paginated-report-integrity
description: Use when fixed-page exports may hide content.
version: 0.1.0
---

# Integridad de reportes paginados

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{FUENTE}} | Contenido y hechos aprobados para el reporte |
| {{EDITABLE}} | Documento de maquetación editable |
| {{PDF}} | Salida paginada versionada |
| {{MARCADORES_CIERRE}} | Textos esperados al final de cada sección o página |
| {{INDICE}} | Registro que enlaza fuente editable y salida |

## Propósito
Detectar recortes y solapamientos silenciosos de reportes de altura fija sin confundir presencia de texto con legibilidad.

## Cuándo usar
Conversión de un documento maquetado a PDF, en especial páginas con pie absoluto, cajas finales o tablas extensas.

## Entradas
{{FUENTE}}, {{EDITABLE}}, {{MARCADORES_CIERRE}} y motor real de exportación. El método no autoriza corregir datos de la fuente.

## Pasos
1. Identificar elementos al final de cada página y fijar {{MARCADORES_CIERRE}} desde la fuente, antes de exportar.
2. Generar {{PDF}} como versión nueva, conservando {{EDITABLE}} y versiones anteriores. No usar número de páginas como criterio suficiente.
3. Renderizar todas las páginas e inspeccionar recuadros de cierre, totales y notas junto al pie. Revisar especialmente altura fija, overflow y posicionamiento absoluto.
4. Extraer texto del PDF y comparar cierres normalizando espacios y saltos de línea. Un marcador ausente bloquea entrega; uno presente no excusa solapamiento visual.
5. Ajustar tipografía o espaciado sin ocultar contenido, regenerar y repetir ambas pruebas. Si no cabe, revisar paginación en lugar de recortar silenciosamente.
6. Enlazar editable y salida desde {{INDICE}}. Separar medición declarada, estimación y método desconocido; no sumar categorías como horas exactas o facturables.

## Reglas de decisión
- overflow:hidden puede ocultar párrafos sin alterar páginas; no es validación de ajuste.
- Texto extraíble no demuestra que sea visible debajo de un pie superpuesto.
- Inconsistencias numéricas se reportan, no se reparan silenciosamente.

## Verificación
Inspección visual de todas las páginas, comparación de todos los marcadores y vínculos a editable/PDF. Declarar herramientas usadas y límites de la prueba; no afirmar que el destinatario puede regenerar si no se ejercitó esa operación.

## Pitfalls
Validar una portada no cubre últimas cajas. No convertir duraciones mezcladas en indicadores exactos. No sustituir fuente editable por un PDF corregido sin trazabilidad.

## Variantes
HTML con paginación fija: doble control texto/imagen. Maquetación fluida: revalidar saltos y cierres en cada generación. Datos de tiempo: separar clases de evidencia.

## Referencias y alcance de evidencia
- [Procedencia y criterios de prueba](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
