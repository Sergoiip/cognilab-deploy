---
name: cd-diagnostico
description: Use when delivering 'Diagnóstico del caos al sistema' to a client. Skeleton,
  scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-A
    - a1
---

# A1 · Diagnóstico del caos al sistema

> Estado: **borrador-v1 (método escrito, sin probar con un cliente real)**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Entender el negocio o proyecto antes de tocar nada: dónde duele, por qué, y qué arreglar primero. Es la Radiografía (`fases/0-radiografia.md`) y su entregable, el **Mapa vivo**, que sigue creciendo durante el piloto y el paquete.

## Método (todas las escalas)
1. **Contexto y dolores.** Entrevista: qué hace, qué le duele (máx. 5 dolores), qué ya intentó. Cada dolor lleva un ejemplo real.
2. **Evidencia.** Por dolor, 3 evidencias: dichas por el cliente o mostradas en su trabajo. Lo observado pesa más que lo contado. Sin 3 evidencias, el dolor no entra al plan.
3. **Flujo actual.** Un día normal, paso a paso, en una página: quién hace qué, con qué herramienta, dónde se espera, dónde se pierde información.
4. **Causa de raíz.** Por cada dolor, «¿por qué?» hasta llegar a algo arreglable (proceso, herramienta, hábito, falta de decisión). Separar síntoma de causa.
5. **Línea base (E1).** Máximo 5 indicadores medibles, con fecha y fuente.
6. **Inventario.** Equipo (`tools/inventario.sh`, con permiso) y herramientas que ya usa.
7. **Plan.** `tools/plan.py` propone módulos y escala por módulo; la decisión final es de Sergio con el cliente.
8. **Devolución.** Se presenta el Mapa vivo y qué arreglar primero. Se afirma solo lo observado.

Test humano para todo entregable propuesto: ¿libera tiempo para lo humano o reemplaza un esfuerzo que forma?

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Mapa del flujo actual en una página, validado con el cliente.
- [ ] Dolores priorizados, cada uno con al menos 3 evidencias dichas o mostradas por el cliente.
- [ ] Plan de entregables con paquete y escala (1, 2 o 3) elegida por módulo.
- [ ] Línea base: mínimo 3 indicadores medidos y fechados (ver E1).

**Comunes a todo módulo:**

- [ ] Verificado: se probó en real antes de entregar, con evidencia (captura, log o archivo).
- [ ] Faltante declarado: lista escrita de lo que no quedó hecho y de las limitaciones.
- [ ] Documentado: una página de uso con los nombres, rutas y tono del cliente.
- [ ] Aceptado: el cliente confirma por escrito (mensaje o acta). Esa aceptación dispara el hito.
- [ ] Sin datos ajenos: nada de otro cliente ni de Sergio en lo entregado.

## Escalas

- `variantes/1-individuo.md`
- `variantes/2-negocio.md`
- `variantes/3-equipo.md`
