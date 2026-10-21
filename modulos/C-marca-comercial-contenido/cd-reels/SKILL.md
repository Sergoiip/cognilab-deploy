---
name: cd-reels
description: Use when delivering 'Reels con subtítulos, sonido y marca' to a client.
  Skeleton, scale 1-3.
version: 0.1.0
metadata:
  hermes:
    tags:
    - cognilab-deploy
    - bloque-C
    - c6
    - ms-15
---

# C6 · Reels con subtítulos, sonido y marca

> Estado: **esqueleto-desde-meta-skill**. Se elige la variante según la escala del cliente (ver `variantes/`).

## Propósito

Convertir clips verticales de un cliente en piezas terminadas (subtítulos, audio limpio, música, efectos y logo) en lote y sin editor manual.

## Cuándo usarla

Varios reels por semana con formato repetido, donde un editor tradicional haría el mismo trabajo cada vez.

## Método

1. Reunir los clips y la marca del cliente (logo, colores, tipografía) antes de tocar nada.
2. Transcribir con reconocimiento de voz y **corregir los términos del negocio** con una lista de reemplazos; avisar al cliente de los que queden dudosos.
3. Subtítulos de 2 palabras por línea, la palabra hablada en el color de marca, a la altura del pecho. **Nunca sobre la cara.** Gancho arriba, etiquetas abajo.
4. Voz: filtro de graves, reducción de ruido, compresión, EQ y nivelado de volumen. Música en bucle bajo la voz, con atenuación automática cuando hablan. Efectos en el gancho, en cada etiqueta y al final.
5. Logo sobre una placa clara los últimos segundos.
6. **Probar con un solo video**, sacar fotogramas y revisar a ojo antes de renderizar el resto.
7. Subir a la carpeta de entrega y volver a listar para comparar. Solo borrar lo que tú creaste.

## Principios

- Un video de prueba antes del lote.
- Los errores de transcripción en nombres de marca y términos técnicos son la mayor fuente de fallas; lista todo lo no confirmado al entregar.
- Si el editor visual no tiene subtítulos automáticos, dilo y usa la línea de comandos.

## Plantilla / código base

```text
transcribir (es, tiempos por palabra) → corregir términos → archivo de subtítulos (2 palabras) →
cadena de audio + música con atenuación → render vertical 1080x1920 → revisión de fotogramas → entrega
```

## Para replicarla en otro negocio

Sirve para cualquier agencia o creador con clips verticales. Cambia el motor de transcripción, el idioma y la identidad visual.

## Criterio de hecho (BORRADOR, pendiente de aprobar)

- [ ] Lote de al menos 5 reels reproducidos y revisados.
- [ ] Plantilla reutilizable entregada.

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
