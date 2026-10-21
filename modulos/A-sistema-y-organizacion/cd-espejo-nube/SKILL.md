---
name: cd-espejo-nube
description: Use when delivering 'Espejo local ↔ nube' to a client. Skeleton, scale
  1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-A
    - a5
    - ms-10
---

# A5 · Espejo local ↔ nube

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Mantener la misma estructura en el disco y en la nube, con inventario, verificación y registro.

## Cuándo usarla

Cuando hay material pesado que debe estar respaldado y compartible.

## Método

1. Diseñar primero la estructura (cliente/etapa/fecha) y reflejarla igual en ambos lados.
2. Subir por lotes y **contar**: origen = destino.
3. Verificar con hash cuando se vaya a borrar algo local.
4. Registrar el emparejamiento (carpeta local ↔ ID en la nube) en una nota viva.
5. Mantener fuera de la nube lo que debe quedar solo local (p. ej. RAW de varios GB).

## Principios

- No se borra nada local sin MD5 coincidente + confirmación.
- El mapa de IDs es parte de la documentación.

## Plantilla / código base

```text
local:  <año>/<mes>/Semana-NN/Dia-DD/<cliente>/
nube:   CLIENTES/<cliente>/<AAAA-MM-DD>/
```

## Para replicarla en otro negocio

Cambia Drive por OneDrive/Dropbox; la lógica no cambia.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Misma estructura en disco y en la nube.
- [ ] Verificación por conteo y tamaño: cero diferencias, o diferencias listadas.
- [ ] Restauración probada de una carpeta.

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
