# Templater

**Versión del catálogo:** 2.26.0 · AGPL-3.0 · repo SilentVoid13/Templater

## Metodología (según el plugin)
Define un lenguaje de plantillas que inserta variables y resultados de funciones en las notas (fechas, títulos, texto, lógica). Permite ejecutar JavaScript y comandos del sistema.

## Recomendación CogniLab
- **Plantillas por tipo de nota:** ficha de cliente, nota de sesión, entrega, nota diaria, idea. Una plantilla por tipo y no más de las necesarias.
- **Frontmatter coherente:** las plantillas deben escribir exactamente los campos que lee Cadence, TaskNotes y Task Atlas. Así el cliente no escribe propiedades a mano.
- **Empezar sin JavaScript.** Con variables de fecha y título se cubre la mayoría. Añadir lógica solo si hace falta.
- Guardar las plantillas en una sola carpeta y documentar para qué sirve cada una.

## Cuidado
- **Puede ejecutar código arbitrario y comandos del sistema.** El propio plugin lo advierte: solo usar plantillas propias o de fuentes de confianza, y nunca instalar plantillas de terceros sin leerlas.
- La licencia es AGPL-3.0. Se instala el plugin tal cual; no se modifica ni se redistribuye modificado en este repo.
