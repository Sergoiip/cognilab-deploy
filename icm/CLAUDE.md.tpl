# Espacio de trabajo: {{CLIENTE}}

Paquete **{{PAQUETE}}** · escala **{{ESCALA}}** · deploy {{VERSION}} · creado {{FECHA}}

Este espacio ordena el trabajo en 90 días en tres etapas. Tú (el agente) preparas; la persona decide.

## Dónde está cada cosa
```
CLAUDE.md          este archivo: dónde estoy
CONTEXT.md         a dónde voy según la tarea
etapas/            tres etapas, cada una con CONTEXT.md y output/
referencias/       fichas, criterios de hecho y escalas (estables)
```

## Cómo leer
1. Lee este archivo y luego `CONTEXT.md`.
2. Entra a la etapa que toca y lee **solo** su `CONTEXT.md`. La tabla de Entradas dice qué más cargar.
3. No cargues nada que la etapa no pida. Más contexto no mejora el resultado.

## Reglas
- **La persona está al centro.** Tú organizas y preparas lo mecánico; lo que decide, forma o se comunica a otras personas lo revisa y lo envía ella.
- **No pases a la etapa siguiente sin aceptación escrita** de la anterior (archivo `aceptacion-hito-N.md` en su `output/`).
- **Escribe solo en el `output/` de la etapa en curso.** No edites salidas de etapas anteriores: señala el problema y pregunta.
- **Faltante declarado:** lo que no quedó hecho se escribe, no se omite.
- **Nunca** guardes contraseñas, tokens ni claves en este espacio.
- **Sin datos de otras personas o clientes** en ningún archivo.

## Atajos
| Palabra | Acción |
|---|---|
| `estado` | Di qué salidas existen en cada etapa y cuál sigue |
| `siguiente` | Abre la etapa que corresponde y resume qué se necesita |
