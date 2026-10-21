---
name: cd-orden-archivos
description: Use when delivering 'Orden de archivos y almacenamiento' to a client.
  Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-A
    - a4
    - ms-07
---

# A4 · Orden de archivos y almacenamiento

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Medir, clasificar y ordenar discos sin riesgo de perder nada.

## Cuándo usarla

Poco espacio, descargas desordenadas o una unidad de cámara llena.

## Método

1. **Medir antes de actuar** (por carpeta, no por intuición).
2. Clasificar con un script y guardar el plan en un archivo; **no mover en la misma pasada** si se pidió solo preparar.
3. Verificar duplicados con tamaño exacto y, en el segundo paso, con hash; nunca borrar por nombre ni por tamaño solo.
4. Reflejar las etapas reales del trabajo (grabar → editar → entregar) y la fecha de grabación.
5. Pedir confirmación explícita antes de borrar, aunque la verificación sea perfecta.

## Principios

- Cuarentena antes que borrado.
- Un script idempotente que registra cada movimiento.
- Nada se sincroniza a la nube antes de ordenar lo local.

## Plantilla / código base

```python
import hashlib
def md5(p):
    h=hashlib.md5()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()
```

## Para replicarla en otro negocio

Cambia la jerarquía por la de tu negocio; el método es el mismo.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Estructura acordada aplicada.
- [ ] Inventario antes y después (conteo y espacio).
- [ ] Respaldo verificado antes de mover nada; cero borrados.
- [ ] Duplicados en cuarentena hasta que el cliente acepte.

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
