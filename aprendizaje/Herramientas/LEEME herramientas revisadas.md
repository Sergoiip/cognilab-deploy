---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Herramientas revisadas

## Parámetros
ARCHIVO_CANVAS: ruta explícita del JSON a validar. Python 3.10+; biblioteca estándar únicamente. TMPDIR: directorio de scratch para fixtures de la suite.

## Incluido
`validar-canvas.py` y `probar-canvas.py` son código nuevo escrito durante esta preparación, no copias ni parches de plugins. La procedencia de esta edición es trazable a esta ejecución; no se atribuye autoría humana ni se adjudican licencias de fuentes antiguas.

Desde esta carpeta:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 probar-canvas.py
python3 validar-canvas.py /ruta/configurada/ejemplo.canvas
```

Exit 0: controles implementados pasan. Exit 1: errores estructurales o de lectura; exit 2: uso CLI incorrecto. Solo emite códigos de error, sin contenidos, rutas, títulos ni nombres de nodos. No inicia red, aplicaciones, servicios ni APIs. Lee exclusivamente la ruta solicitada; elegirla es responsabilidad del operador. No resuelve enlaces ni audita secretos del documento de entrada.

Las pruebas usan archivos sintéticos temporales y comprueban que no cambian sus bytes. No ejercen una bóveda real. No se incluyen resultados de pruebas en el paquete.

## No incluido
Los originales permanecen fuera del paquete. La carpeta Medición añade una versión revisada y reducida de un agregador propio cuya procedencia se comprobó; leer su guía y ejecutar sus pruebas. Los originales con rutas privadas, efectos reales o derechos no confirmados quedan excluidos con motivos en el inventario privado. La presencia en el disco no demuestra permiso de redistribución.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
