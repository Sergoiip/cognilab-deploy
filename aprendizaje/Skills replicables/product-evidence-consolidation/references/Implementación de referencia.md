# Implementación de referencia

## Herramientas
La referencia utiliza herramientas de PDF y un repositorio de notas para la entrega. Si se usa un agente con skills de `pdf` y `obsidian`, cargar las aplicables antes de manipular esos formatos; no se requiere un repositorio privado concreto. No se exportan entrevistas, fichas, capturas ni datos de productos reales.

ReportLab permite generar el documento; PyMuPDF renderizar todas las páginas y extraer texto y límites. Descubrir tipografías con `fc-match`, no asumir rutas de una distribución. Sistemas Arch pueden instalarlas en `/usr/share/fonts/TTF/`; consultar sistema real antes de usar esa ruta.

## Manifiesto y datos
Para cada fuente registrar ID estable, ruta relativa autorizada, SHA-256, tipo y relación con documentos equivalentes; separar huella de archivo de identidad documental. Para cada producto registrar familia/modelo/variante, token de referencia literal, capacidades, precio y su alcance, IDs de procedencia, incertidumbres y permisos de imagen. No llenar campos desconocidos con valores plausibles.

Conservar entrevistas originales fuera de la síntesis; registrar evidencia, preferencia, recomendación y aprobación como tipos distintos. El registro de precio conserva alcance de compra/venta, moneda, impuestos, vigencia y disponibilidad; ninguno se deduce por contexto no explícito.

## Prueba del documento
Renderizar todas las páginas con PyMuPDF, crear hoja de contacto y abrir páginas densas individualmente. Comprobar por código número de páginas, presencia de cada referencia/tarjeta en texto, límites dentro del área y enlaces válidos. Los límites automáticos no reemplazan inspección visual de superposición o legibilidad.

Los recortes compartidos deben ser activos nuevos que contengan solo producto; ocultar un chat detrás de un rectángulo o recortar la vista sin limpiar el activo puede filtrar el original. Revisar activos realmente embebidos y atribución sin inferir derechos. Mantener script, datos y resultado de verificación junto al artefacto canónico privado/autorizado, no dentro de la skill distribuible.

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
