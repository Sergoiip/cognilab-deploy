---
name: product-evidence-consolidation
description: Use when consolidating product evidence into catalogs.
version: 0.1.0
---

# Consolidación verificable de evidencia de productos

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{FUENTES_AUTORIZADAS}} | Documentos, imágenes y entrevistas revisables |
| {{ARCHIVO_ORIGINALES}} | Archivo privado separado de las salidas |
| {{MANIFIESTO}} | Registro de fuentes y huellas |
| {{DATOS_ESTRUCTURADOS}} | Productos, variantes, precios y procedencia |
| {{DESTINO_CATALOGO}} | Entrega canónica de producto sin información privada |
| {{AUDIENCIA}} | Permisos y destinatarios previstos |
| {{CRITERIOS_PRECIOS}} | Moneda, vigencia, impuestos y tipo de precio confirmados |
| {{FUENTES_TIPOGRAFICAS}} | Fuentes disponibles descubiertas |
| {{GENERADOR}} | Script propio autorizado que se conserva con la entrega |

## Propósito
Unificar evidencia heterogénea en un catálogo trazable, sin confundir tarjetas con referencias comerciales ni convertir afirmaciones impresas en verificaciones independientes. Preservar originales y límites de distribución.

## Cuándo usar
Al recibir fichas, fotografías y entrevistas que deben consolidarse en material visual revisable. No usar para certificar registros, legalidad, aptitud clínica, márgenes ni autorización de redistribución.

## Entradas
Fuentes autorizadas, entrevistas originales, imágenes, contexto y permisos de uso. Separar entrevistas originales de síntesis y recomendaciones desde el inicio; no modificar originales para resolver ambigüedades.

## Pasos
1. Inventariar imágenes y documentos con identificadores estables y huellas criptográficas; comprobar cantidad recibida. Deduplicar tanto bytes como documentos equivalentes con distinto archivo, conservando relación de procedencia.
2. Crear hojas de contacto para visión global y luego reabrir originales con recortes de alta resolución para referencias, capacidades y precios. La miniatura no basta para transcribir texto pequeño.
3. Modelar familias/modelos, variantes de tamaño, fichas duplicadas y fotos sin etiqueta por separado. Contar tarjetas y referencias comerciales de forma independiente. Mantener como incierto cualquier token poco claro, sin repararlo silenciosamente.
4. Asociar precio solo a referencias que la evidencia soporte explícitamente. Conservar ambigüedad de compra/venta, moneda, impuestos, vigencia y disponibilidad; no deducir pagos de producto ni márgenes a partir de recibos no relacionados.
5. Archivar material sensible en privado. Excluir capturas bancarias y chats de documentos compartibles y activos embebidos; producir recortes de producto con procedencia. Atribuir imágenes de terceros sin afirmar que la atribución concede distribución.
6. Marcar identificadores regulatorios impresos y afirmaciones de desempeño como no verificados salvo comprobación independiente trazable. No inferir legalidad o idoneidad clínica desde una ficha.
7. Diseñar contexto e investigación concisos y tarjetas visuales donde aporten. Distinguir preferencias del entrevistado, estrategia aprobada y recomendaciones abiertas; no convertir sugerencias del investigador en decisiones.
8. Descubrir fuentes disponibles en el sistema; generar documento con datos estructurados y script preservado, sin rutas de fuentes supuestas. Renderizar todas las páginas, revisar hojas de contacto y páginas densas a tamaño completo.
9. Validar cantidad de páginas, presencia de cada tarjeta/referencia en texto extraído, cobertura completa de fuentes, enlaces y límites de texto. Guardar documento, script, datos, procedencia y verificación en destino canónico. No enviar al destinatario sin autorización.

## Decisiones
Texto ilegible se declara ilegible y se conserva token original. Foto sin etiqueta no se asigna por semejanza sin evidencia. Si no hay permiso de distribución de una imagen, excluirla o conservarla solo en archivo privado según autorización. Ninguna declaración de catálogo constituye certificación.

## Verificación
Contar fuentes originales, documentos deduplicados, elementos pendientes, tarjetas y referencias con herramientas; reconciliar cobertura y explicar cada exclusión. Revisar visualmente todas las páginas y densas en alta resolución, extraer texto y probar enlaces y desbordamientos. Inspeccionar activos embebidos para que recortar visualmente no deje datos sensibles ocultos.

## Pitfalls
Dos archivos distintos pueden ser la misma ficha. Una familia puede tener varios tamaños; una tarjeta no es una unidad comercial. Una imagen atribuida puede seguir restringida. Una etiqueta regulatoria no acredita vigencia. Fuentes tipográficas y métricas varían entre sistemas.

## Variantes
Inventario sin catálogo; catálogo visual con pendientes; dossier de investigación separado; entrega externa solo con productos y fuentes autorizadas. Cualquier comprobación regulatoria adicional exige su propio alcance y evidencia.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
