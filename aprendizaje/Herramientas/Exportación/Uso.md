# Regenerar la entrega acumulada

Desde la carpeta de trabajo que contiene `Paquete` y `Fuentes`:

```text
python3 -B Paquete/Herramientas/Exportación/probar-exportador.py
python3 -B Paquete/Herramientas/Exportación/exportar.py --reference Paquete --sources Fuentes --state estado-abstraccion.json --inventory estado-herramientas.json --output exportacion.zip --coverage cobertura.json --sensitive-pattern patrones-privados.txt --approve
```

Usar `--approve` únicamente después de revisar y auditar las abstracciones nuevas o cambiadas. Las corridas siguientes omiten ese flag: cambios fuente quedan bloqueados hasta revisión. No ejecutar corridas simultáneas. Preservar estados previos antes de cambiar el exportador o aprobar una nueva generación.

`Fuentes/Registro.json` relaciona cada skill exportada con el SKILL.md fuente y procedencia revisada. Los valores permitidos de creator son `learn` (metadato de creación local), `local-extension-reviewed` (aporte local aislado de un cuerpo tercero) y `agent-created-this-task` (fuente nueva creada para esta entrega). No atribuir esos valores a material desconocido. El registro no viaja dentro del ZIP; no contiene credenciales y debe mantenerse junto a las fuentes privadas autorizadas.

Cada estado de abstracción es un hash del SKILL.md fuente normalizado a LF. Las herramientas se comparan con su inventario anterior; informe y manifiesto se recalculan, no se escriben a mano. Todas las referencias exportadas se revisan aunque el hash de abstracción solo represente el archivo principal.

`--coverage` permite generar cobertura recalculada desde listas de fuentes y herramientas. El archivo contiene arrays `skills` y `tools`: se publican únicamente campos permitidos y se calculan totales por clasificación y decisión. No introducir rutas privadas en campos públicos. `--sensitive-pattern` carga una regex insensible a mayúsculas desde un archivo privado externo al paquete; aportar los identificadores de cada entorno y revisarlos sin incrustarlos en el exportador. Si no se aporta, solo se aplican los controles genéricos: no declarar anonimización exhaustiva.

El control automático busca patrones conocidos y no reemplaza revisión de privacidad, titularidad y licencia. Las marcas técnicas se permiten en referencias, no en el método genérico. Se rechazan enlaces simbólicos y contenido fuera de los directorios autorizados y se omiten configuraciones, bases, multimedia, caches y archivos ocultos.

Una extracción contiene código genérico ejecutable y pruebas sintéticas, pero no fuentes originales privadas, inventario completo de la máquina ni estados operativos. Para reutilizar el exportador hay que crear un registro verdadero del nuevo alcance, adaptar patrones sensibles y revisar autorizaciones. No instala skills, no configura servicios y no crea cron.
