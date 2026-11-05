# Runtime y voz: lecciones de diagnóstico

## Árbol de decisión
- Si funciona en terminal pero falla en escritorio, comprobar primero el intérprete del backend empaquetado. La presencia de una dependencia en un venv no demuestra su presencia en otro.
- Si la distribución usa un bootstrap de dependencias, cargarlo antes de una prueba de imports; no diagnosticar paquetes ausentes desde un intérprete sin inicializar.
- Si hay un entorno de transcripción ya operativo, evaluar un proveedor de comando soportado antes de introducir ruedas nativas incompatibles en el paquete. Inspeccionar el contrato instalado, usar rutas parametrizadas y llamar al motor local directamente para evitar recursión del dispatcher.
- Un proveedor de comando debe diferenciar silencio legítimo de error. Un archivo de salida vacío puede ser rechazado; probar la traducción de esa condición en la ruta de subida, no maquillar fallos como transcripciones vacías.
- El formato del ensayo debe coincidir con el de entrada real: voz de mensajería y grabación del escritorio pueden usar contenedores diferentes.
- Una lengua fijada incorrectamente puede producir traducción en vez de transcripción. Ensayar un clip conocido en la lengua objetivo antes de cambiar de motor.
- Ante ausencia de bibliotecas GPU y fallback CPU comprobado, preferir fijar dispositivo y cómputo soportados antes de instalar una pila GPU por reflejo.

## Gateway y escritorio con versiones diferentes
Un servicio persistente antiguo puede revivir mientras un escritorio nuevo intenta reemplazarlo. Contrastar ruta del ejecutable, versión, unidad, señales y contador de reinicios. Respaldar la unidad; regenerarla solo mediante la CLI verificada de la superficie que la controla. Comprobar estabilidad y conexión, sin equiparar eso a un chat nuevo exitoso.

## Navegador y escritorio remoto
Un perfil bloqueado requiere cierre consentido, no extracción cruda de bases SQLite. Un navegador empaquetado puede existir aunque el descubridor no encuentre el binario. Si se autoriza un adaptador de lanzamiento, limitar el permiso de acceso a la copia concreta del perfil y evitar permisos persistentes amplios. Verificar una navegación real y luego cada aplicación solicitada. Un listado de ventanas no prueba acceso a la página; un bridge de accesibilidad no prueba autorización de input global.

## Personalización mínima
Inspeccionar el renderer instalado antes de atribuir un texto fijo al tema. Si se autoriza una extensión de presentación, delimitar el nodo exacto, conservar estructuras duplicadas de medición, restaurar solo lo que la extensión posee y desconectar observadores al retirarla. Prueba sintáctica no demuestra ejecución; usar diagnóstico temporal acotado y eliminarlo al terminar.

Origen: abstracción de incidentes locales de runtimes y superficies; sin redistribución de extensiones originales.
