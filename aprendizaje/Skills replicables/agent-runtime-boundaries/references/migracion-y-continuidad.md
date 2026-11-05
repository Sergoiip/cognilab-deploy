# Migración y continuidad sin efectos implícitos

## Respaldo y corte
1. Separar snapshot privado de informe compartible. Configuración de acceso, tokens y bases de sesión no van en notas sincronizadas.
2. Inspeccionar el importador de la versión destino: restaurar puede iniciar gateway, migrar SQLite y refrescar skills bundled. Deshabilitar una unidad antes no garantiza que el importador no arranque otro proceso.
3. Mantener destino sin salida o restaurar offline mientras el origen conserve mensajería y tareas programadas. Evitar dos consumidores de las mismas credenciales.
4. Verificar integridad SQLite, tablas y hashes antes de activar; una versión distinta no asegura rollback compatible. Conservar snapshot previo.
5. Confirmar huella de host remoto por un canal de confianza. No trasladar clave privada al servidor. Identificar qué gateway sostiene las herramientas antes de detener servicios.

## Perfiles
Revisar valores sembrados al crear un perfil: proveedor, modelo y URL base son campos independientes. Fijar auxiliares y delegación cuando el aislamiento de proveedor lo requiera, revisar fallbacks y adopción de logins externos. Verificación de auth no debe convertirse en una petición facturable innecesaria. Cambiar proveedor LLM tampoco limita los destinos de las herramientas.

Un board compartido puede exponer resultados al coordinador; archivos separados no aíslan un handoff inyectado en todos los hijos. Sanitizar contexto común antes de delegar.

## Trabajos con continuación humana
Un wrapper mínimo en el directorio de scripts permitido puede invocar lógica canónica del proyecto si la versión instalada rechaza rutas absolutas. Probar ese launcher y leer el job después de actualizarlo: rechazo atómico significa que ningún campo debe darse por aplicado.

Entregar preguntas y procesar respuestas son fases distintas. Guardar instrucciones de continuación y reutilizar el job existente. La lectura de configuración y un replay local no prueban que el próximo cierre recibido se haya enlazado a la conversación adecuada.

Origen: síntesis de lecciones locales de migración, perfiles y cierres programados.
