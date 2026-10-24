# Fase 0 · Radiografía (1 semana, antes del paquete)

> BORRADOR. Es la entrada de la escalera (ver `escalera.md`). Precio y condiciones: Cadence. Los entregables exactos están por confirmar con Sergio; esto es la propuesta de trabajo.

**Entregable:** Mapa vivo v1 · línea base medida · causas de raíz priorizadas · qué arreglar primero · manifiesto borrador.
**Principio:** no se adivina qué falla, se mide. Solo se afirma lo que se observó. Con una semana de datos no se modelan ni se estiman parámetros: es lectura cualitativa con evidencia.

## Antes de empezar (día 0)
- Autorización escrita del cliente para mirar su equipo, archivos y conversaciones **solo lo necesario**. Datos sensibles: se acuerda dónde viven y no se copian.
- Elegir la persona del cliente que responde dudas durante la semana.
- Crear la carpeta del cliente (fuera del repo) y `radiografia.yaml` desde `fichas/radiografia.yaml`.

## Semana
| Día | Qué se hace | Sale con |
|---|---|---|
| 1 | Entrevista al dueño (contexto, dolores con ejemplo real, qué ya intentó). Un día normal contado paso a paso. | Dolores con evidencia dicha, borrador del flujo |
| 2 | Observar el trabajo real (ver cómo lo hace, no cómo dice que lo hace). Entrevista corta a cada rol. | Evidencia mostrada, diferencias entre lo dicho y lo hecho |
| 3 | Inventario del equipo (`tools/inventario.sh`, con permiso) y de herramientas que ya usa. | `inventario.yaml`, tabla «ya usa» |
| 4 | Línea base: máximo 5 indicadores medibles, con fecha y fuente (E1). Causas de raíz: por cada dolor, preguntar «¿por qué?» hasta llegar a algo que se pueda arreglar. | Línea base, causas priorizadas |
| 5 | Mapa vivo v1, `tools/plan.py` → manifiesto borrador, sesión de devolución con el cliente. | Mapa vivo, plan, decisión |

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
