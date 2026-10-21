---
name: cd-reportes
description: Use when delivering 'Reportes periódicos con marca' to a client. Skeleton,
  scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c3
    - ms-06
---

# C3 · Reportes periódicos con marca

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Convertir lo hecho en la semana en un informe claro, priorizado y bien diseñado.

## Cuándo usarla

Cierre semanal o mensual, o cuando llega un reporte que hay que mejorar.

## Método

1. Extraer el texto del reporte (o reunir las fuentes) y **renderizar las páginas** para verlas.
2. Detectar problemas: espacio muerto, tablas desordenadas, ruido técnico (IDs internos), pendientes sin prioridad.
3. Reconstruir todo en un solo HTML y generar PDF; no editar el PDF.
4. Usar solo hechos de la fuente; **señalar inconsistencias** (p. ej. un KPI que no cuadra) en lugar de arreglarlas en silencio.
5. Guardar como la siguiente versión y entregar.

## Principios

- Portada con el resumen; pendientes por orden de prioridad.
- Nunca corregir datos sin avisar.

## Plantilla / código base

```bash
chrome --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=salida.pdf file:///ruta/absoluta/reporte.html
```

## Para replicarla en otro negocio

Aplica a cualquier informe periódico a clientes o a uno mismo.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Un reporte generado con datos reales.
- [ ] KPIs definidos sobre la línea base.
- [ ] El cliente lo regenera sin ayuda.

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
