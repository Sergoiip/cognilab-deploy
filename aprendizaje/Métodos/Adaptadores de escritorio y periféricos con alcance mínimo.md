---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Adaptadores de escritorio y periféricos con alcance mínimo

## Parámetros
| Parámetro | Decisión previa |
|---|---|
| SUPERFICIE | Elemento concreto de interfaz, ventana o evento de dispositivo |
| IDENTIDAD | Propiedad técnica verificada; nunca nombre supuesto |
| API_COMPATIBLE | Versión, ciclo de vida y callbacks disponibles |
| ACCION | Efecto autorizado y mecanismo de reversión |
| ENTORNO_EJECUCION | Sesión gráfica y variables necesarias, sin copiar sus valores |
| PRUEBA_CONTROL | Caso no destinatario que debe permanecer intacto |

## Método
1. Distinguir una personalización visual de una modificación del producto. Delimitar selector y texto exactos; no reemplazar indiscriminadamente mensajes o nombres en todo el documento.
2. Para una interfaz dinámica, observar únicamente los tipos de cambio necesarios, agrupar callbacks y conservar los elementos realmente modificados. Al descargar, desconectar observadores y restaurar solo elementos aún conectados cuyo valor siga siendo el que puso el adaptador; no sobrescribir ediciones posteriores del usuario.
3. Para enfocar o lanzar, descubrir identificadores reales de ventanas. Probar por separado ventana existente y ventana ausente. Que un mecanismo de despacho responda no demuestra que apareció la aplicación. No registrar títulos de ventana en evidencia pública.
4. Separar credenciales de sesión y entorno gráfico de configuración portable. Un lanzador puede vivir fuera de la sesión gráfica y carecer de variables necesarias. Elegir el ejecutor que recibe el entorno vigente; no fijar rutas efímeras de autorización.
5. Verificar eventos disponibles antes de prometer controles de pulsar y soltar. Un callback de pulsación no implementa la liberación; registrar el atajo o describirlo como mantener pulsado no prueba una captura completa ni su detención. Un borrador con esa carencia se excluye, no se empaqueta como funcional.
6. En periféricos, preferir una excepción por identidad exacta y tipo de evento antes que desactivar globalmente una capacidad. Si el gestor crea nodos sintéticos fuera del filtro habitual, localizar el evento de creación y situar el control antes de ese paso, sin modificar el código instalado de terceros.
7. Probar el dispositivo objetivo, otro que no coincide, reconexión y reversión. Presencia de señal no demuestra voz inteligible. Conservar ajustes globales que no pertenecen al problema.

## Verificación y límites
Un harness de DOM puede acreditar selección, callbacks y desmontaje; no compatibilidad con toda versión del escritorio. Una prueba sintética de evento no sustituye reconexión física. Anotar por separado sintaxis, contrato, efecto observado, aceptación y reversión. No activar atajos, micrófonos ni servicios por incluir este método.

Origen: síntesis nueva del comportamiento y las carencias de adaptadores locales revisados; sin código, identificadores de dispositivos ni configuración privada de las fuentes.
