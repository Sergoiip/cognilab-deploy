---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Mapas verificables y tareas canónicas

## Parámetros
MODELO, CANVAS, NOTAS_DETALLE, FUENTES_AUTORIZADAS, GESTOR_CANONICO y MAPA_ANTERIOR.

## Procedimiento
1. Separar operación observada, secuencias propuestas y traducción estratégica. Una condición documentada no prueba un bloqueo activo; una flecha explicativa no crea dependencia en el gestor.
2. Reconstruir con fuentes autorizadas y citas precisas. No inferir lectura completa desde un índice o un inventario. No transferir plantillas de terceros ni datos operativos al extraer principios.
3. Usar IDs estables en el modelo. Dibujar un Canvas nativo por escalas: panorama, carriles y detalle enlazado; tarjetas cortas, grupos como contenedores y conexiones locales. Conservar posiciones/tamaños existentes al regenerar.
4. Mantener tareas y estados en su autoridad canónica. Las vistas de calendario, diario y roadmap leen o enlazan lo mismo; no añaden checkboxes paralelas ni crean tareas por representar un proceso.
5. Comprobar cada superficie por separado. Paridad de inventario no acredita paridad de Today, Calendar, Home y diario. Comparar conjuntos por identificador/ruta, no solo conteos o títulos; esperar la carga asíncrona.
6. Para diarios: fecha anclada al archivo y preservación de escritura personal; la fecha fija no convierte la consulta en snapshot histórico de estados. Probar expansión de plantillas en aislamiento y conservar respaldo.
7. Validar JSON, IDs, extremos, geometría, superposiciones, rutas y encabezados de wikilinks. Escapar separadores de alias dentro de tablas. Las pruebas de la herramienta adjunta cubren solo un subconjunto estructural; no resuelve enlaces.
8. Revisar vista previa y después renderizado nativo cuando sea posible. Etiquetar la primera como preview, no como captura de la aplicación. Probar comprensión humana antes de declarar aceptación.

## Herramienta preparada
`../Herramientas/validar-canvas.py` recibe un archivo explícito y no escribe resultados en él. Comprueba IDs, extremos, dimensiones y superposición entre tarjetas, ignorando grupos contenedores. No valida formato completo de JSON Canvas, enlaces, colores, autenticidad de fuentes o legibilidad. Un error de superposición es criterio de este flujo, no una prohibición del estándar.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
