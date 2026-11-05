---
name: dual-node-agent-operations
description: Use when deploying an agent across two computers.
version: 0.1.0
---

# Operación de un agente en dos equipos

## Parámetros obligatorios

Completar fuera de la plantilla antes de actuar. Los marcadores no son valores utilizables; no guardar secretos en este documento.

| Placeholder | Qué poner | Tipo |
|---|---|---|
| `{{EQUIPO_PRINCIPAL}}` | Identificador del dueño operativo previsto | Identificador |
| `{{EQUIPO_SECUNDARIO}}` | Identificador del cliente y candidato de recuperación | Identificador |
| `{{AMBITO}}` | Instancias y perfiles autorizados; exclusiones | Lista |
| `{{FUENTE_CANONICA}}` | Estado que debe conservarse y dueño actual | Identificador y descripción |
| `{{ACCESO_PRIVADO}}` | Mecanismo privado, identidad verificable y alcance permitido | Descripción sin secretos |
| `{{CAPACIDADES}}` | Acciones requeridas y equipo ejecutor de cada una | Matriz |
| `{{ESCRITORES}}` | Procesos, canales y tareas que escriben o producen efectos | Inventario |
| `{{RESPALDO}}` | Destino privado, retención y mecanismo de captura consistente | Referencia protegida |
| `{{OBJETIVOS}}` | Pérdida tolerable y tiempo objetivo de recuperación | Duraciones |
| `{{VENTANA_Y_AUTORIZACION}}` | Responsable, ventana y permiso explícito para corte y pruebas | Registro |
| `{{AISLAMIENTO}}` | Cómo impedir operación y reactivación del dueño anterior | Procedimiento verificable |
| `{{COORDINACION}}` | Control del corte y contacto alternativo independientes del servicio detenido | Procedimiento |
| `{{EVIDENCIAS}}` | Destino autorizado y responsable de aceptación | Referencia y rol |

## Propósito y alcance

Preparar principal, cliente con capacidades locales y recuperación manual manteniendo un único dueño del estado operativo. No promete disponibilidad continua, pérdida cero ni promoción automática. Este documento es un procedimiento reutilizable: no acredita un despliegue real ni instala componentes por sí mismo.

## Cuándo usar

- Al conectar un cliente a un agente alojado en otro equipo, trasladar el dueño operativo o preparar sustitución manual.
- No usar como sistema de consenso, operación activa simultánea ni sincronización de estado vivo entre escritores.
- Si faltan identidad, permiso, captura recuperable o aislamiento comprobable, limitarse a diagnóstico y preparación no destructiva.

## Dos niveles y entradas

**Nivel 1 (desidentificar):** sustituir datos específicos por parámetros sin valores de origen. **Nivel 2 (generalizar):** expresar decisiones, criterios y variantes transferibles. Las referencias amplían las fases; la implementación concreta queda separada y no convierte una propuesta en prueba. Cargar la referencia pertinente antes de actuar.

- `references/Procedimiento operativo.md`: detalle de fases y dependencias.
- `references/Aceptación y evidencia.md`: pruebas y registro de resultados.
- `references/Recuperación y rollback.md`: promoción, reversión y retorno.
- `references/Implementación de referencia.md`: ejemplo separado, nunca valores predeterminados ni prueba de esta instalación.

Entradas adicionales: inventario de ambos equipos, documentación vigente del sistema elegido, permisos de acceso, fuente de estado acordada y pruebas inocuas autorizadas. Comprobar que las cuatro referencias estén presentes en el paquete; si falta una necesaria, declarar el bloqueo antes de su fase. Mantener juntas la skill y su carpeta de referencias al distribuirlas; la instalación posterior requiere autorización y no implica ejecutar el procedimiento.

## Procedimiento y criterios de avance

1. **Descubrir y acordar.** Confirmar identidad de ambos equipos, instancia activa, roles, compatibilidad, recursos, dependencias gráficas, canales y tareas. Elegir fuente canónica sin fusionar historiales por suposición. **Criterio:** inventario y alcance aprobados; cada escritor tiene dueño y forma de detenerse.
2. **Asegurar el acceso.** Verificar identidad remota por un medio confiable, autenticación y acceso restringido a red privada. Mantener separados permiso de red y permiso de aplicación. **Criterio:** acceso funcional y límites comprobados; ninguna exposición pública innecesaria ni comprobación de identidad omitida.
3. **Proteger ambos estados.** Antes de sobrescribir, capturar copias consistentes mediante un mecanismo compatible; suspender escritores cuando corresponda. Verificar integridad, generación, origen, permisos y restauración aislada. Preservar el último respaldo válido ante fallos. **Criterio:** ambos estados recuperables y restauración demostrada sin efectos externos.
4. **Preparar sin promover.** Adaptar dependencias y referencias por equipo; mantener desactivados en el candidato canales, tareas y reactivaciones automáticas. Probar contexto reciente y respuesta del agente en aislamiento. **Criterio:** candidato compatible sin segundo dueño operativo.
5. **Conectar y probar capacidades.** Distinguir conexión remota de operación local. Probar separadamente comandos, archivos, navegación e interacción de escritorio cuando estén incluidos, indicando dónde se ejecutan. Compartir documentos solo con alcance, exclusiones y versionado; excluir estado vivo y secretos. **Criterio:** matriz capacidad/equipo/prueba/límite; si hay sincronización, probar ida, vuelta, borrado y restauración sin sincronizadores solapados.
6. **Autorizar el corte.** Presentar alcance, riesgos, pausa esperada, pérdida posible y condiciones de aborto. Acordar coordinador independiente, canal alternativo y reversión. No interpretar autorización de preparación como permiso de corte. **Criterio:** autorización explícita registrada y aislamiento practicable para todos los escritores.
7. **Capturar y transferir.** Detener o aislar todos los escritores relevantes, capturar estado final consistente y comprobar transferencia e integridad. Impedir también reactivaciones del dueño anterior. **Criterio:** aislamiento efectivo comprobado antes de activar el destino; ante incertidumbre no promover.
8. **Activar y aceptar.** Activar solo el dueño elegido. Probar contexto, modelo, capacidades, una respuesta por mensaje y una ejecución por tarea de prueba autorizada. Separar configuración de energía y persistencia de pruebas físicas coordinadas: reinicio real, ausencia del secundario y condiciones de alimentación aplicables. **Criterio:** evidencia por prueba; faltantes críticos bloquean cierre completo.
9. **Ensayar recuperación y retorno.** Verificar respaldo vigente y pérdida posible; autorizar recuperación, aislar al principal y restaurar en el sustituto compatible antes de habilitar efectos. Medir antigüedad recuperable y duración. Para volver, conservar cambios nuevos del sustituto, detener escritores y transferir estado actualizado, no una copia antigua. **Criterio:** promoción y retorno controlados, dueño único registrado y copias orientadas al nuevo dueño.

## Reglas de decisión

- Falta de respuesta de red no prueba apagado ni aislamiento. Sin aislamiento efectivo, bloquear la promoción y pedir la intervención mínima necesaria.
- Identidad inesperada, integridad fallida, escritores desconocidos, incompatibilidad o duplicados: abortar avance, preservar evidencias y contener efectos; no activar otro dueño para compensar.
- Fallo antes de activar destino: reanudar origen solo si destino está inactivo e impedido de reactivarse. Fallo después: aislar destino y conservar sus cambios recientes antes de decidir retorno.
- Respaldo obsoleto: informar pérdida potencial y exigir autorización; no prometer el objetivo como resultado medido.
- Falta de acceso físico: registrar prueba física pendiente; una configuración correcta no la reemplaza.

## Verificación y entrega

Registrar por prueba: identificador, fecha y zona horaria, equipo/rol, instancia, versión, acción autorizada, esperado, observado, evidencia sin secretos, responsable y estado: pendiente, aprobada, fallida o no aplica con motivo. Separar propuesto, configurado, comprobado y aceptado.

Entregar dueño actual, capturas recuperables y su antigüedad, capacidades y límites, resultados, efectos laterales, pendientes y procedimiento de reversión. Diferenciar integridad documental, restauración aislada y conmutación real; ninguna acredita automáticamente las otras. No declarar migración completa con una prueba crítica pendiente.

## Pitfalls

- Copiar un almacenamiento transaccional activo como archivo corriente puede producir un respaldo incoherente.
- Cliente remoto conectado no demuestra ejecución local, continuidad de canales ni respaldo recuperable.
- Replicar documentos no replica de forma segura identidad, memoria y sesiones; no mezclar estados ni propagar secretos o configuración específica del dispositivo.
- Servicio habilitado no prueba reinicio físico; aislamiento de prueba no acredita conmutación real.
- Restaurar una captura antigua sobre un sustituto usado puede perder cambios; preservar ambas ramas y resolver con un procedimiento compatible, sin fusionar a mano.
- No interrumpir aplicaciones con trabajo abierto sin coordinación. Si ambos equipos están apagados, no hay continuidad.

## Variantes

- **Solo cliente remoto:** probar conexión y capacidades; no afirmar respaldo ni recuperación si no se prepararon y ensayaron.
- **Principal y sustituto manual:** completar captura, aislamiento, promoción y retorno; mantener cliente local claramente diferenciado.
- **Documentos compartidos:** añadir sincronización versionada independiente del estado del agente; no usarla como reemplazo del respaldo.
- **Intervención física pendiente:** entregar estado parcial y bloqueo explícito, sin aprobar pruebas de energía o reinicio por inferencia.

Origen: patrón operativo generalizado para dos equipos; adaptar parámetros antes de usar.
