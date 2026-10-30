# Fase 0 · Radiografía (1 semana, antes del paquete)

> BORRADOR. Es la entrada de la escalera (ver `escalera.md`). Precio y condiciones: Cadence. Los entregables exactos están por confirmar con Sergio; esto es la propuesta de trabajo.

**Entregable:** Mapa vivo v1 · línea base medida · causas de raíz priorizadas · qué arreglar primero · manifiesto borrador.
**Principio:** no se adivina qué falla, se mide. Solo se afirma lo que se observó. Con una semana de datos no se modelan ni se estiman parámetros: es lectura cualitativa con evidencia.

## Antes de empezar (día 0)
- Autorización escrita del cliente para mirar su equipo, archivos y conversaciones **solo lo necesario**. Datos sensibles: se acuerda dónde viven y no se copian.
- Elegir la persona del cliente que responde dudas durante la semana.
- Crear la carpeta del cliente (fuera del repo) y `radiografia.yaml` desde `fichas/radiografia.yaml`.
- Activar el seguimiento: `python3 tools/radiografia_activa.py start "<cliente>" <ruta-radiografia.yaml>` y reanudar el cron **"Radiografía — guía diaria"** (`cronjob_manage` → `resume`, id en Hermes). Cada día hábil 9am avisa qué toca ese día y qué quedó incompleto del anterior, leyendo esta misma tabla y el `radiografia.yaml` real — nunca inventa avances.

## Semana
| Día | Qué se hace | Sale con |
|---|---|---|
| 1 | Entrevista al dueño (contexto, dolores con ejemplo real, qué ya intentó). Un día normal contado paso a paso. También: cómo se imaginan su "equipo de agentes" (narrativa/lore, si ya tienen una idea), qué los mueve de verdad y sus referencias estéticas favoritas (`identidad_agentes` de la ficha) — sin inventar nada que no digan ellos. | Dolores con evidencia dicha, borrador del flujo, `identidad_agentes` con lo que de verdad dijeron (vacío si no dijeron nada) |
| 2 | Observar el trabajo real (ver cómo lo hace, no cómo dice que lo hace). Entrevista corta a cada rol. | Evidencia mostrada, diferencias entre lo dicho y lo hecho |
| 3 | Inventario del equipo (`tools/inventario.sh`, con permiso) y de herramientas que ya usa. | `inventario.yaml`, tabla «ya usa» |
| 4 | Línea base: máximo 5 indicadores medibles, con fecha y fuente (E1). Causas de raíz: por cada dolor, preguntar «¿por qué?» hasta llegar a algo que se pueda arreglar. | Línea base, causas priorizadas |
| 5 | Mapa vivo v1, `tools/plan.py` → manifiesto borrador, sesión de devolución con el cliente. | Mapa vivo, plan, decisión |

## Variante: Radiografía exprés (1 día)

Cuando el cliente no tiene margen para 5 días separados, se puede pasar por **todas** las
preguntas de los días 1 a 4 en una sola sesión larga (medio día a un día completo) y producir el
manifiesto borrador al cierre de esa misma sesión — el manifiesto preliminar de Fase 1 nace ahí
mismo, no después.

Lo que NO cambia:
- El **cron "Radiografía — guía diaria" sigue corriendo toda la semana igual**, aunque la
  sesión presencial ya haya terminado. Activarlo igual (`tools/radiografia_activa.py start`) —
  su trabajo ahora es **complementar** lo que se capturó en un solo día: observación real (lo que
  el día 2 normalmente cubre sin prisa), evidencia que no salió en la entrevista, e indicadores
  de línea base que necesitan unos días de uso real para medirse bien.
- El criterio de 3 evidencias por dolor y el test humano (`Cómo se decide qué entra`, abajo) se
  mantienen exactos — exprés no significa menos evidencia, significa comprimir el calendario.
- El manifiesto que sale ese mismo día sigue siendo **preliminar**: se afina igual durante la
  semana con `tools/plan.py` si el cron detecta evidencia nueva relevante (ver `bootstrap/PRIMEROS-PASOS.md`).

Cuándo NO usar la exprés: si el cliente tiene más de ~5 personas tocando el trabajo, o si los
dolores declarados no coinciden con lo observable en una sola visita — ahí el día 2 (observación
separada) sí hace falta para no decidir el manifiesto solo con lo dicho.

## Cómo se decide qué entra
1. Cada dolor lleva **3 evidencias** (dichas o mostradas) y una prioridad 1–3. Sin evidencia no entra.
2. `criterios/dolor-a-modulo.yaml` propone módulos por categoría de dolor.
3. La escala se decide **por módulo** con dos preguntas: cuántas personas lo tocan y qué pasa si falla (`escalas.md`).
4. Herramientas: modo `cliente` si ya sabe qué usa, `asignar` si no; lo que no esté en el catálogo se anota y se decide si se migra o se integra.
5. Test humano de cada entregable: ¿libera tiempo para lo humano o reemplaza un esfuerzo que forma? Si reemplaza un esfuerzo que forma, no entra.
6. Lo que depende de sistema operativo no soportado (el instalador cubre pacman, apt y dnf) se marca «a mano» antes de prometerlo.

## Salida y camino
- El cliente decide: quedarse con el Mapa vivo, tomar un **Piloto** (un entregable) o pasar al **paquete de 90 días** (Esencial o Integral). El Mapa vivo sigue creciendo durante el piloto y el paquete.
- El manifiesto aprobado pasa a la Fase 1 y, de ahí, a la instalación (Fase 2).
