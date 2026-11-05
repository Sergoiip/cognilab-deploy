---
name: activity-process-evidence
description: Use when reporting work from activity intervals.
version: 0.1.0
---

# Informes de procesos a partir de actividad

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{API_ACTIVIDAD}} | Origen autorizado de eventos; no incluir credenciales |
| {{EQUIPO}} | Equipo único que se analiza |
| {{ZONA_HORARIA}} | Zona usada para fechas y cortes |
| {{PERIODO}} | Inicio, fin y corte de la observación |
| {{DESTINO_INFORME}} | Carpeta canónica de informes |
| {{GENERADOR}} | Generador local inspeccionado y autorizado |
| {{NOTAS_PROCESO}} | Notas desde las que se enlaza la entrega |
| {{REGLAS_ATRIBUCION}} | Reglas candidatas y validaciones explícitas |

## Propósito
Transformar intervalos de ventana y presencia en evidencia agregada de procesos, sin convertir tiempo de pantalla en productividad, facturación o ingreso. Mantener títulos y eventos privados en procesamiento local.

## Cuándo usar
Para un informe de actividad por proceso o una revisión de cobertura. No usar como vigilancia individual, liquidación automática de horas ni prueba de rentabilidad.

## Entradas
Inventario real de fuentes, eventos de ventana y presencia del mismo equipo, zona horaria, período, reglas de atribución y permisos de divulgación. Inspeccionar el generador existente antes de reutilizarlo; no se incluye uno en esta carpeta.

## Pasos
1. Consultar el inventario de fuentes antes de pedir eventos. Elegir un equipo y fuentes compatibles de ventana/presencia. Si se agregan equipos, diseñar primero la reconciliación de simultaneidad y documentar su resultado.
2. Fijar fecha local, zona, inicio, fin y corte. Para un primer pedido sin período, usar el día actual parcial y rotularlo como parcial; acordar período antes de conclusiones longitudinales.
3. Recortar eventos al intervalo solicitado; unir los intervalos de presencia activa y cruzarlos con los de ventana. Detectar solapes entre ventanas, resolver o declarar su ambigüedad y reconciliar los totales. No sumar recolectores como si fueran trabajo independiente.
4. Procesar títulos localmente. Clasificar coincidencias como candidatas, conservar categoría desconocida y emitir agregados por defecto. No enviar títulos de clientes, direcciones web ni eventos crudos a modelos sin permiso explícito.
5. Separar en el informe: observaciones medibles, hipótesis de atribución y validaciones del usuario. Las reglas de título no confirman un cliente ni un proyecto por sí solas.
6. Diferenciar tiempo trabajado, registrado, aprobado, facturado por una organización y remunerado a una persona. No calcular las últimas categorías desde tiempo de pantalla.
7. Si la cobertura desconocida es alta, detener atribución fuerte y diagnosticar compatibilidad de sesión/recolector antes de permisos o instalaciones. No deducir el tipo de sesión por síntomas.
8. Guardar evidencia agregada reproducible con período, reglas, filtros y limitaciones; enlazar desde notas del proceso, probar enlaces y marcar si es informe manual o automatización realmente instalada.

## Decisiones
- Desconocido o no coincidente no equivale a desperdicio ni a cero trabajo.
- Un período parcial no demuestra una tendencia. Ausencia de eventos puede ser fallo de captura.
- Sin reconciliación entre equipos, informar cada uno por separado.
- Sin permisos de datos, limitar salida al mínimo agregado que no reidentifique.

## Verificación
Recalcular intersecciones y totales con herramientas, verificar que el total no exceda el período reconciliado, contar eventos excluidos y revisar solapes. Comprobar cobertura de fuentes, zona y corte en el texto, separación de hipótesis y evidencia, enlaces y ausencia de títulos privados. Una salida generada no demuestra que una tarea periódica funcione.

## Pitfalls
Sumar presencia y ventanas duplica tiempo. Inferir cliente por una palabra del título sobreasigna trabajo. Cambiar permisos sin diagnóstico puede ampliar exposición sin resolver cobertura. Un agregado pequeño aún puede identificar a alguien: revisar audiencia y granularidad.

## Variantes
Informe manual de un día parcial; informe de período cerrado con reglas validadas; informe multiequipo solo con reconciliación; automatización únicamente tras autorización, instalación y prueba de ejecución.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
