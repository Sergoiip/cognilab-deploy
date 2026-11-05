# Operación dual

## Parámetros antes de usar

Completar en un registro privado de la instalación; estos marcadores no contienen valores reales ni autorizan cambios. No incorporar secretos al método ni a las evidencias.

| Placeholder | Qué poner | Tipo |
|---|---|---|
| `{{PRINCIPAL}}` | Equipo que tendrá la autoridad operativa | Identificador |
| `{{SECUNDARIO}}` | Equipo cliente y posible sustituto | Identificador |
| `{{ALCANCE}}` | Instancias incluidas, exclusiones y fuente canónica | Inventario |
| `{{ACCESO}}` | Conectividad privada, identidad comprobable y permisos | Descripción sin secretos |
| `{{CAPACIDADES}}` | Acciones necesarias, dependencias y equipo ejecutor | Matriz |
| `{{ESCRITORES}}` | Productores de estado, mensajes y automatizaciones | Inventario |
| `{{COPIAS}}` | Destino privado, consistencia, retención y restauración | Referencia protegida |
| `{{OBJETIVOS}}` | Pérdida tolerable y recuperación deseada | Duraciones |
| `{{AISLAMIENTO}}` | Medida comprobable para impedir operación y reactivación | Procedimiento |
| `{{CORTE}}` | Ventana, alcance, responsable y autorización expresa | Registro |
| `{{CONTROL_ALTERNATIVO}}` | Coordinación que funciona al detener el servicio de origen | Procedimiento |
| `{{ACEPTACION}}` | Responsable, pruebas requeridas y registro de evidencia | Lista y rol |

## Propósito

Operar un agente en dos equipos sin confundir cliente remoto, ejecución local y respaldo. El principal conserva el estado canónico y es el único autorizado para producir efectos operativos; el secundario puede actuar como cliente y, tras aislamiento y autorización, como sustituto manual. Los roles pueden cambiar, pero la autoridad no puede duplicarse.

Es un método documental sin herramientas concretas ni instrucciones de instalación. No afirma pruebas reales de despliegue, recuperación automática, pérdida cero ni disponibilidad continua.

## Cuándo usar y entradas

Usar para preparar conexión remota, trasladar operación o habilitar recuperación manual. No usar para dos escritores activos sobre el mismo estado ni para promoción automática basada en conectividad.

Reunir inventario de ambos equipos, estado de origen acordado, compatibilidad del sistema elegido, documentación vigente, responsables, acceso seguro, pruebas inocuas autorizadas y mecanismo de respaldo recuperable. Acordar previamente qué depende de sesión gráfica, presencia física, energía y disponibilidad del secundario.

## Secuencia con puertas de avance

### 1. Descubrir antes de cambiar

Confirmar identidad, roles actuales y deseados, instancias, versiones, dependencias y ubicación lógica del estado. Inventariar también tareas y servicios que podrían reactivarse tras reinicio. No fusionar historiales ni incluir otras instancias por proximidad.

**Avance:** alcance y fuente canónica aprobados; cada escritor tiene responsable y forma comprobable de detenerse.

### 2. Establecer confianza y conexión

Asegurar acceso privado autenticado; contrastar identidad del destino por un medio confiable. Comprobar permisos de aplicación además del acceso de red. Mantener separadas la conexión al principal y la operación local del secundario, sin exposición pública innecesaria.

**Avance:** conexión funcional con identidad contrastada y límites de acceso documentados; no basta una respuesta de red.

### 3. Capturar y demostrar recuperación

Respaldar ambos estados antes de sobrescribir. Utilizar captura consistente compatible con el almacenamiento; detener escritores si el mecanismo lo requiere. No copiar un almacenamiento transaccional activo como un archivo corriente. Registrar origen, generación y antigüedad de cada copia, comprobar integridad y restaurar en aislamiento sin canales ni tareas con efectos externos. Un fallo de copia no debe destruir el último éxito.

**Avance:** ambos estados cuentan con punto de retorno restaurable, acceso restringido y retención definida. Integridad sin restauración no alcanza esta puerta.

### 4. Preparar y probar sin promover

Mantener origen operativo durante la preparación. Adaptar dependencias y referencias por equipo; impedir en el candidato mensajes, tareas y reactivaciones automáticas. Comprobar contexto reciente y respuesta real del agente en entorno aislado.

Probar por separado cada capacidad incluida: ejecución de acciones, acceso a archivos, navegación e interacción gráfica. Registrar equipo ejecutor, resultado y límite. Una conexión remota no demuestra todas las capacidades locales.

Si se comparten documentos, establecer versionado, exclusiones y un único mecanismo por ámbito. Probar cambios en ambas direcciones, borrado y restauración. Excluir secretos y estado vivo del agente; no confundir sincronización con respaldo.

**Avance:** candidato compatible y matriz de capacidades comprobada, sin duplicar autoridad operativa.

### 5. Autorizar y ejecutar el corte

Presentar riesgos, pausa prevista, posible pérdida, punto de retorno y condiciones de aborto. Obtener autorización explícita antes de detener servicios, sobrescribir o transferir operación. La autorización para preparar no autoriza el corte. Mantener control y contacto alternativos independientes del servicio que se detendrá.

Detener o aislar todos los escritores relevantes; capturar el estado final consistente, transferirlo y comprobar integridad. Verificar que el dueño anterior no puede seguir operando ni reactivarse, incluidos sus canales y automatizaciones. Solo entonces habilitar al destino elegido.

**Avance:** captura final verificada, aislamiento efectivo del anterior y un único dueño registrado. Si el estado es ambiguo, no promover.

### 6. Verificar operación y condiciones físicas

Comprobar contexto, respuesta del agente, integraciones y capacidades declaradas. Usar mensajes y tareas inocuos autorizados para verificar una sola respuesta y una sola ejecución, conservando evidencia de ambos equipos y del canal cuando corresponda.

Separar dos registros:

- **Configuración:** persistencia, políticas de energía, dependencia de sesión y reactivación previstas.
- **Prueba física:** reinicio real coordinado, operación sin el secundario y condiciones de alimentación o cierre físico aplicables. No interrumpir trabajo abierto sin autorización. Si falta intervención presencial, dejar la prueba pendiente.

**Avance:** pruebas críticas aprobadas con evidencia; los límites y pendientes permanecen visibles. Una configuración correcta no acredita una prueba física.

### 7. Recuperar, volver y mantener

Ante caída, distinguir observación de hipótesis: no responder a la red no demuestra apagado. Confirmar aislamiento efectivo del principal antes de promover al secundario. Si no puede garantizarse, bloquear promoción y solicitar la intervención necesaria.

Verificar origen, integridad, generación, compatibilidad y antigüedad de la copia elegida. Informar cambios potencialmente perdidos y obtener autorización de recuperación. Restaurar de forma consistente, habilitar efectos solo en el sustituto y comprobar operación única. Registrar nuevo dueño e impedir que el equipo recuperado reasuma solo.

Para retorno, conservar cambios posteriores del sustituto: capturar su estado actualizado, detener escritores, transferir y aislar al sustituto antes de habilitar el otro equipo. No sobrescribir con una copia antigua ni fusionar estados manualmente como atajo.

Ensayar restauración aislada, rechazo de copia dañada, transferencia interrumpida conservando el último éxito, promoción manual y retorno. Medir por separado antigüedad recuperable y duración real; la frecuencia deseada no es una garantía observada. Definir responsables de copias, actualizaciones, energía, alertas y revisiones; cambiar la dirección de respaldo al cambiar el dueño.

**Avance:** recuperación y retorno acreditados solo al ejecutarse; el ensayo aislado se registra como tal y no como conmutación real.

## Reglas de decisión y aborto

| Situación | Decisión obligatoria |
|---|---|
| Identidad inesperada o acceso sin autenticar | Suspender conexión y resolver confianza; no omitir controles |
| Copia incoherente, incompatible o sin restauración | No sobrescribir ni cortar; preservar estados y preparar copia recuperable |
| Actividad desconocida o aislamiento no comprobado | No promover; contener y resolver autoridad |
| Fallo antes de activar destino | Mantener o reanudar origen solo tras comprobar destino inactivo y sin reactivación |
| Fallo tras activar destino | Aislarlo, conservar cambios nuevos y decidir retorno con ambos escritores detenidos |
| Duplicados | Contener emisores, preservar evidencia y restablecer dueño único antes de reanudar |
| Copia demasiado antigua | Informar pérdida potencial y solicitar decisión explícita |
| Falta de acceso o intervención física | Mantener estado seguro; solicitar lo mínimo y registrar prueba pendiente |
| Ambos equipos no disponibles | Declarar interrupción; no prometer continuidad |

## Verificación y entrega

Por prueba registrar identificador, fecha con zona horaria, equipo y rol, instancia y versión, acción autorizada, esperado, observado, evidencia sin secretos, responsable y estado: pendiente, aprobada, fallida o no aplica con motivo. Separar aprobación técnica de aceptación del responsable.

Entregar dueño actual, último respaldo válido y antigüedad, límites por capacidad, autorización de corte, pruebas de captura, conexión, aislamiento, operación única, recuperación y retorno, mediciones, efectos laterales y pendientes. Distinguir propuesto, configurado, comprobado y aceptado. No cerrar como completo con pendientes críticos; verificar documentos no certifica una instalación.

## Pitfalls

- Replicar configuración específica de un equipo puede romper permisos o dependencias del otro; revisar por instancia y conservar exclusiones.
- Compartir documentos no equivale a compartir memoria, identidad o sesiones de forma consistente.
- Conexión, copia íntegra, restauración aislada y conmutación real son evidencias distintas.
- Un proceso habilitado no demuestra que sobreviva a un reinicio físico ni que opere sin sesión gráfica.
- Un retorno apresurado puede perder cambios producidos en el sustituto; preservar ambos estados antes de resolver divergencias.
- Respaldos y evidencias no deben difundir credenciales ni datos privados; usar acceso restringido y registros redactados.

## Variantes

- **Cliente remoto sin recuperación:** aceptar solo conexión y capacidades; no presentar el secundario como respaldo recuperable.
- **Recuperación manual preparada:** exigir copia consistente, aislamiento, promoción autorizada y retorno probado.
- **Documentos compartidos:** añadir sincronización versionada independiente, con borrado y restauración comprobados.
- **Validación física diferida:** entregar configuración y pruebas lógicas con el estado parcial explícito; completar aceptación cuando exista evidencia física.

Origen: patrón operativo generalizado para dos equipos; adaptar parámetros antes de usar.
