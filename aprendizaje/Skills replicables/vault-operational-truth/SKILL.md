---
name: vault-operational-truth
description: Use when vault workflows need canonical evidence.
version: 0.1.0
---

# Bóveda operativa con tareas, mapas y evidencia

## Parámetros
| Token | Qué debe resolver la implementación |
|---|---|
| {{BOVEDA}} | Raíz canónica resuelta antes de usar herramientas de archivos |
| {{REGISTRO_TAREAS}} | API o MCP que gobierna estados, fechas y tareas |
| {{INDICE}} | Nota de entrada y navegación |
| {{MODELO_MAPA}} | Modelo estructurado con IDs estables |
| {{PROTOCOLO_CIERRE}} | Regla aprobada para registrar respuestas y actualizar mapas |
| {{HISTORIAL}} | Destino privado o no indexable para respaldos |

## Propósito
Conservar una sola verdad operativa entre tareas, agendas, mapas y diarios, y recuperar sin pérdida ante sincronización o actualizaciones. Las vistas no crean compromisos por sí mismas.

## Cuándo usar
Organización de trabajo en una bóveda Markdown, revisión de agenda, integración de paneles, mapas de procesos, restauración de conflictos y retornos documentales.

## Entradas
{{BOVEDA}} y {{REGISTRO_TAREAS}} verificados, decisiones vigentes, fuentes completas, permisos por efecto y límites de sincronización. Resolver rutas concretas antes de read_file/write_file; los file tools no expanden variables de shell. Leer las referencias pertinentes antes de operar.

## Pasos
1. Descubrir la bóveda realmente abierta por registro y health del servicio, no por una ruta supuesta ni por el éxito del comando de apertura. Inspeccionar plugins ya instalados antes de proponer duplicados.
2. Declarar responsabilidades: registro de tareas para estados/fechas, relación de sesiones y proyectos, visualización de metas/dependencias, calendario temporal y cola técnica de agentes. No sustituir sistemas externos de trabajo ni crear trackers paralelos.
3. Enumerar tareas con paginación y deduplicar por ruta canónica. Antes de crear, buscar coincidencias; fijar campos explícitos y leer la ruta exacta después de cada escritura. Corregir defaults de fechas no solicitadas de modo local y verificado.
4. Vincular agendas y evidencias a las tareas existentes. Verificar por separado contenido visible, paridad de tareas y vínculos de proyectos en cada superficie. Today, calendario, home y nota diaria pueden tener selectores distintos.
5. Mantener mapas actuales separados de propuestas. Actualizar solo registros afectados en {{MODELO_MAPA}}, conservar IDs y geometría previa, y publicar detalles enlazados, no tarjetas saturadas. Validar estructura y renderizado como pruebas distintas.
6. Para cierres, guardar respuestas reales bajo {{PROTOCOLO_CIERRE}}, cotejar decisiones posteriores y registrar evidencia y corte temporal. Sin respuestas no hay trabajo inferido, nuevas tareas ni promoción automática de estado.
7. Ante conflicto de sincronización, pausar planificación, comprobar servicio detenido y conservar ambos lados antes de restaurar. Ante actualización, comparar tres vías, revisar licencias y preservar configuración privada. Seguir referencias especializadas.
8. Enlazar entregables editables y salidas desde {{INDICE}}; conservar originales y versiones previas. Verificar enlaces, no solo existencia de archivos. Registrar pendientes de visualización o ejecución real.

## Reglas de decisión
- Una tarea completada según estado canónico no se reabre por una agenda vieja; conservar contradicción como evidencia pendiente.
- Un mapa de dependencias no programa trabajo ni dispara automáticamente una cola técnica. No confundir orden de tabla con dependencia.
- No crear metas o fechas ficticias para llenar una vista vacía. Una propiedad en cuerpo de nota no es necesariamente campo consultable.
- No usar respaldos .md dentro de la bóveda si el indexador descubre tareas por tags; usar contenedor o extensión no indexable.
- Si no hay autorización de recarga/cierre, limitarse al staging y declarar verificación viva pendiente.

## Verificación
Contar rutas únicas frente a totales declarados. Leer cada tarea cambiada. Comprobar consultas de fecha, estados personalizados, vínculos y contenido de la agenda en cada superficie. En Canvas validar JSON, IDs, enlaces/encabezados, aristas y solapamientos; una imagen generada es preview, no captura nativa. En retornos validar contenido anterior, bloque completo y respaldo; en sync validar datos restaurados sin afirmar renderizado no observado.

## Pitfalls
- Notas diarias con today() pueden cambiar lo mostrado retrospectivamente; usar fecha fija expandida del día.
- Un refresco de panel completo puede destruir un diario en debounce. Proteger texto y descartar snapshots asíncronos obsoletos.
- API sana no prueba panel cargado; plugin habilitado en disco no prueba runtime. Esquemas MCP y HTTP pueden devolver envoltorios distintos.
- data.json de plugins puede contener credenciales. No copiarlo a staging compartible.
- Retornos append y locks cooperativos no son transacciones ante editores externos.

## Variantes
Bóveda individual: una autoridad de tareas. Equipo: explicitar permisos y separación de sistemas. Sin interfaz gráfica: validar datos y previews y declarar pendiente el renderizado nativo; nunca inventarlo.

## Referencias y alcance de evidencia
- [Tareas y superficies](references/tareas-y-superficies.md).
- [Mapas, diarios y evidencia](references/mapas-y-evidencia.md).
- [Conflictos de sincronización](references/conflictos-sync.md).
- [Actualización de plugins](references/actualizaciones-plugins.md).
- [Retornos seguros](references/retornos-seguros.md).
- [Implementación y procedencia](references/procedencia.md).
La evidencia de origen es documental: no se ha instalado, activado ni probado esta implementación durante la extracción. Parametrizar y ensayar en un entorno aislado antes de usarla con datos reales. Este paquete no incluye cuerpos de manuales ni código de terceros.

Origen: síntesis independiente de lecciones operativas locales; materiales de terceros excluidos.
