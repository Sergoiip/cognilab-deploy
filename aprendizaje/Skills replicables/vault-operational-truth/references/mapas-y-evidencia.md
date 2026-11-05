# Mapas, diarios y evidencia

## Separar representaciones
Un panorama operativo solicitado como lienzo se entrega como archivo Canvas nativo y notas de soporte enlazadas. Mantener vistas AS-IS, TO-BE y puente estratégico separadas; no sobrescribir el panorama anterior con un borrador operativo. Las tarjetas resumen, las notas conservan fuentes y condiciones y el modelo estructurado conserva IDs estables. No atribuir a un método una plantilla exacta que no aparece en la fuente consultada.

Organizar por escalas: panorama, intervención, carriles y familias de detalle. Evitar embeds largos y tablas en tarjetas de overview. Mantener dimensiones coherentes y gutters; aristas largas de retorno y etiquetas superpuestas empeoran lectura. Al regenerar preservar geometría existente, revisar cambios sin guardar y conservar historial.

## Validación en capas
- JSON válido, IDs únicos y referencias de aristas existentes.
- Rectángulos sin solapamientos no intencionales y endpoints coherentes.
- Destinos de notas y encabezados resueltos. En tablas Markdown escapar separadores dentro de wikilinks; evitar encabezados con separadores ambiguos y revisar triple corchete.
- Preview etiquetada como tal, seguida de captura nativa cuando sea posible. Un render propio comprueba layout, no el comportamiento del editor.
- Contar archivos reales de un export excluyendo entradas de directorio. Comparar originales y ZIP por hash; inventario de encabezados no sustituye lectura completa ni prueba ejecución de procesos.

## Diario con corte explícito
Resolver fecha y zona desde el sistema y revisar convenciones existentes. Recuperar mensajes por sus timestamps, no solo fecha de inicio de sesión: una sesión antigua puede contener mensajes del día. Contrastar artefactos con mensajes; mtime no es historial de edición ni tiempo trabajado. Separar resultado histórico de salud actual de un servicio.

Registrar resultados, decisiones, preguntas, bloqueos y evidencia hasta el corte; enlazar tareas canónicas sin duplicar checkboxes ni completar tareas por inferencia. Guardar respuestas reales antes de actualizar modelo/mapa y reconocer hashes de diarios revisados solo al terminar. Si no hay respuestas, no inventar avance hacia un proceso ideal.

## Evidencia y consentimiento
Distinguir encontrado, estructura inspeccionada, contenido leído y resultado real verificado. Material externo privado solo aporta conceptos sanitizados, no filas de clientes, plantillas o credenciales. Un volumen no montado queda fuera de cobertura si falla una lectura autorizada; no escalar ni declarar inspección completa. Una intención narrada por un tercero no asigna un rol ni autoriza publicar la historia de otra persona.

## Notas auxiliares flotantes
Conservar Markdown canónico y visor de solo lectura opcional. No activar autoarranque ni atajos globales sin pedido. Probar el Exec real del launcher y sus imports; la shell y el escritorio pueden usar intérpretes distintos. Medir métricas de fuente, zoom y captura: el tamaño solicitado no demuestra legibilidad y una familia fallback puede ignorarlo.

Origen: síntesis de lecciones locales de mapas, registros y evidencia visual.
