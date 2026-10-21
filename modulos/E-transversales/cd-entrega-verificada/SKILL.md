---
name: cd-entrega-verificada
description: Use when delivering 'Entrega verificada' to a client. Skeleton, scale
  1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-E
    - e2
    - ms-13
---

# E2 · Entrega verificada

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Nada sale sin comprobar visualmente y sin declarar lo que falta.

## Cuándo usarla

Antes de entregar cualquier documento, imagen o archivo.

## Método

1. Contar páginas/elementos y comparar con lo diseñado.
2. Revisar una hoja de contactos y ampliar las zonas de riesgo.
3. Comparar hashes de lo copiado al destino.
4. Listar lo que es provisional o no verificado (precios, métricas, derechos de imagen).
5. Nunca afirmar que una imagen no tiene personas sin haberla mirado.

## Principios

- Si la verificación no dio resultado, se dice 'sin confirmar'.
- El archivo viejo se borra antes de publicar el nuevo.

## Plantilla / código base

```python
import pypdfium2 as p
pdf=p.PdfDocument('salida.pdf')
for i in range(len(pdf)): pdf[i].render(scale=1).to_pil().save(f'p{i+1}.png')
```

## Para replicarla en otro negocio

Universal.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Lista de verificación aplicada en cada hito, con evidencia.
- [ ] Lo faltante declarado antes de pedir la aceptación.

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
