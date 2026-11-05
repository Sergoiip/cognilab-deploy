# Agregación de actividad sin telemetría implícita

## Parámetros
| Campo | Contenido |
|---|---|
| ENTRADA.json | Archivo autorizado, explícito; no se descubre configuración local |
| start, end | Inicio y fin exclusivos del periodo en segundos de un mismo eje temporal |
| windows | Lista de objetos con start y end; campos adicionales se ignoran |
| active | Lista de pares inicio-fin de presencia activa del mismo dispositivo |

```json
{"start":0,"end":10,"windows":[{"start":2,"end":5}],"active":[[0,8]]}
```

```sh
python3 -B agregar-actividad.py ENTRADA.json
python3 -B probar-actividad.py
```

La salida JSON se escribe únicamente en stdout; la entrada no se modifica. Un error devuelve código 2 y mensaje fijo en stderr sin contenido ni ruta privada. No importa servicios, crea red, recolecta eventos ni consulta secretos. Solo biblioteca estándar de Python 3.

Recorta intervalos al periodo, une presencia, rechaza ventanas superpuestas y calcula presencia con ventana y sin ella. No incluye nombres de aplicación, títulos, URLs, proyectos, hosts ni eventos crudos. El input debe proceder de un único dispositivo ya seleccionado; este script no lo descubre ni lo acredita. Todos los números deben ser finitos, no booleanos, de magnitud no superior a 10^15 y con fin mayor que inicio. Entrada CLI limitada a 10 MB.

No transforma fechas: el adaptador autorizado debe convertirlas correctamente a segundos absolutos y resolver zona horaria y cambios estacionales antes de llamar. Tampoco prueba suficiencia de cobertura, calidad del trabajo, facturabilidad ni atribución de proyectos. La ausencia de fuente de presencia no se interpreta como presencia total. Con arrays vacíos informa cero observado, no cero trabajo real.

Pruebas sintéticas reproducibles: recorte, unión de presencia, adyacencia, rechazo de solapamiento, intervalos inválidos/no finitos, periodos vacíos, huecos de presencia, eliminación de campos privados, CLI y preservación de entrada. No certifican operación con un recolector real.

Origen: versión revisada y reducida de un reporte generado por el agente en una sesión propia; procedencia y comprobación por hash conservadas únicamente en el inventario privado. No se atribuye autoría humana ni licencia de terceros.
