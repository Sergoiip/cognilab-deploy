---
name: formulario-reserva-a-crm
description: Use when wiring a booking form into a CRM/task pipeline.
version: 1.0.0
---

# Formulario de reserva → CRM, tareas y carpeta de cliente

**Propósito:** conectar un formulario de reserva (p. ej. Google Forms) que llena el cliente final
para que cada respuesta cree automáticamente contacto, oportunidad, sesión/actividad, tareas de
seguimiento y carpeta de entrega, con alerta al responsable. Es la capa de **captura e intake
automatizado**: una vez el registro llega al CRM, su escritura y mantenimiento sigue las reglas
del gestor destino.

## Datos a reunir
- Gestor destino: dónde viven contactos, pipeline, actividades y tareas (CRM, bóveda de notas,
  hoja de cálculo).
- Quién envía el enlace y atiende al cliente (equipo comercial interno o externo).
- Archivo de credenciales OAuth de Google ya guardado (p. ej. `google_token.json`); nunca
  imprimirlo.
- Carpeta de nube para sesiones/entregas (opcional).
- Nombre del script de sincronización (p. ej. `form_sync.py`).
- Canal de alerta para cada respuesta nueva (chat o correo).
- Frecuencia de consulta (por defecto 15 min, configurable).
- Persona responsable que aprueba.

## Reglas fijas
- Idioma del cliente, formulario corto (~3 min), tono cercano; preguntar solo lo que el flujo
  necesita (contacto, fecha/hora deseada, tipo de servicio, objetivo, consentimiento de datos).
- Nunca preguntar precio/horas al cliente en el formulario (eso lo llena quien cotiza); nunca
  lenguaje interno en el formulario.
- Si el enlace del formulario cambia: actualizar brief, lista de enlaces operativos, manual del
  equipo comercial, secuencia de bienvenida, y cerrar la tarea.
- Informar siempre: enlace del formulario, enlace de edición, y qué NO está conectado.

## Procedimiento
1. API de Forms con el token guardado. `POST /v1/forms` solo acepta `info.title`; todo lo demás va
   por `forms/{id}:batchUpdate`.
2. Ramificación condicional: crear primero los ítems, leer el `itemId` de cada sección DESPUÉS de
   crearla, luego `updateItem` con `goToSectionId` por opción — solo funciona si esa pregunta es el
   ÚLTIMO ítem antes de la primera sección condicional (usar `moveItem`).
3. Guardar id del formulario, `responderUri` y mapa `{título: questionId}` en un JSON; el script
   de sync lo usa para leer respuestas.
4. Script de sincronización: consulta `forms/{id}/responses`, deduplica por `responseId` en un
   archivo de estado, y por cada respuesta nueva escribe en el gestor destino: contacto (buscar
   existente antes de duplicar), oportunidad (etapa Lead), actividad/sesión (Por confirmar),
   tareas de seguimiento con responsable, carpeta de entrega, y un resumen para el canal de
   alerta.
5. Programar con cron/tarea periódica a la frecuencia elegida, sin agente en el loop; silencio si
   no hay respuestas nuevas (no spamear el canal).
6. Probar con una respuesta falsa (`--dry-run`), revisar lo generado, luego BORRAR los registros de
   prueba y reiniciar el archivo de estado. No afirmar un envío real probado si nadie llenó el
   formulario de verdad.

## Pitfalls
- Sheets/Forms puede estar deshabilitada en el proyecto de Google Cloud (403 con URL de
  activación): capturar el error, seguir con lo demás, dar la URL de activación.
- Las fechas de respuesta llegan `YYYY-MM-DD`: parsear defensivamente con respaldo hoy+7.
- La nube de destino puede no estar montada: envolver la creación de carpeta en try/except e
  informar.
- Si la rama condicional no se activa: revisar que la pregunta de opción sea el último ítem antes
  de la sección.

## Verificación
Respuesta de prueba → contacto, oportunidad, sesión y tareas creados sin duplicar; segunda
ejecución no repite (por el archivo de estado); datos de prueba eliminados; alerta solo con
respuestas nuevas.

## Variantes
- Otros formularios (Typeform, Tally): mismo patrón con webhook en vez de sondeo periódico.
- Otro gestor (Notion, Airtable, HubSpot, hoja, o una bóveda de notas tipo Obsidian): cambia solo
  la capa de escritura del paso 4. Si el destino es un CRM dentro de la bóveda del cliente,
  escribir solo en las carpetas que realmente lee su plugin, usar enums válidos y no inventar
  campos.
- Sin carpeta de entrega: omitir ese paso.

Técnica reutilizable para cualquier servicio con reserva/cita (consultoría, talleres, sesiones).
