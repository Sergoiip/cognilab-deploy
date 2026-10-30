# Primeros pasos después de instalar (manifiesto preliminar)

Esto es lo que se hace justo después de correr `bootstrap/instala.sh` con un manifiesto que
salió de la encuesta (`bootstrap/encuesta.html` o `tools/encuesta_manifiesto.py`) — **antes**
de que termine la semana de Radiografía. Es normal que ese manifiesto sea preliminar: se afina
con datos reales durante la semana, no se decide todo de una sentada con el cliente.

## Justo después de instalar

1. **El agente responde y es quien debía ser.** Si el manifiesto traía `agente.nombre` /
   `agente.personalidad`, abrir una conversación y preguntarle su nombre — debe coincidir. Si no
   coincide, revisar que `tools/personalizar_agente.py` corrió (lo hace solo `instala.sh`, pero
   confirmar si algo falló en esa etapa).
2. **La bóveda ya refleja el manifiesto, no solo abre vacía.** `instala.sh` (paso 3/6) corre
   `tools/scaffold_vault.py`: crea la bóveda si falta, escribe `00 - Bienvenida.md` con el nombre
   del cliente, el agente y los módulos elegidos (checklist), y las carpetas base que los módulos
   elegidos ya necesitan (`Cadence/Gastos` si hay A2 a escala 2+, `TaskNotes/Tasks` y `daily/` si
   hay A3). Abrir Obsidian en la ruta de `vault` y confirmar que esa nota aparece — es la prueba
   de que la personalización llegó desde el primer momento, no después de una semana. La primera
   vez Obsidian pide desactivar el "modo restringido" a mano para que los plugins carguen.
3. **Versión registrada.** Confirmar que existe `~/.hermes/skills/cognilab-deploy/VERSION` con la
   versión del repo, y anotarla en Cadence junto al cliente.
4. **Resolver la lista "a mano".** `instala.sh` imprime al final qué no se puede automatizar
   (cuentas de Telegram/WhatsApp/Discord/Drive, plugins sin `vault:` resuelto, etc.) — cerrarla
   con el cliente antes de irse, no dejarla para después.
5. **Un caso real por módulo instalado**, no una demo vacía: por ejemplo, si se instaló A2
   (Second Brain), el cliente mismo crea una nota real y una tarea enlazada en la sesión — ese es
   el criterio C1 "Verificado" de todo módulo (`criterios/CRITERIOS-DE-HECHO.md`).

## Si el manifiesto es preliminar (vino de la encuesta, no de una Radiografía completa)

6. **Activar la Fase 0 esta misma semana** para afinarlo con datos reales, no con lo que el
   cliente contestó en una encuesta de 5 minutos:
   ```bash
   python3 tools/radiografia_activa.py start "<cliente>" <ruta-a-radiografia.yaml>
   ```
   y reanudar el cron **"Radiografía — guía diaria"** (`cronjob_manage` → `resume`) — da la guía
   del día que corresponde (ver `fases/0-radiografia.md`) y avisa si falta evidencia del día
   anterior.
7. **El manifiesto puede cambiar al final de la semana** (día 5): `tools/plan.py` puede proponer
   otra escala, otro módulo principal, u otro modo de herramientas según lo que de verdad se
   observó. Eso NO obliga a desinstalar nada: `bootstrap/instala.sh` es idempotente — correrlo de
   nuevo con el manifiesto ajustado solo agrega/actualiza lo que cambió, y el paso 3/6 regenera
   `00 - Bienvenida.md` y crea cualquier carpeta nueva que los módulos añadidos necesiten. No hace
   falta correr `tools/scaffold_vault.py` aparte — `instala.sh` ya lo incluye — pero si solo se
   quiere refrescar la bóveda sin tocar skills/apps, se puede correr suelto: `python3
   tools/scaffold_vault.py manifiestos/cliente-X.yaml`.
8. **Agendar la sesión de devolución del día 5** con el cliente desde ya, no al final de la
   semana.
9. **Al cerrar la semana:** `tools/radiografia_activa.py parar` y pausar el cron hasta el próximo
   cliente.

## Si el manifiesto ya viene de una Radiografía completa (no preliminar)

Pasos 1 a 5 igual; se omiten 6 a 9 — ya no hace falta afinar nada, se pasa directo a Fase 1
(`fases/1-diagnostico-y-base.md`).
