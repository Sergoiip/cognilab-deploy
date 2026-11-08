# Material comercial para prospectos: patrones

## Dónde viven los hechos de la oferta (leer en este orden, siempre)

1. `{{NOTA_MODELO_NEGOCIO}}` — principios, gancho, escalera de oferta, precios aprobados, qué sigue sin decidir.
2. `{{NOTA_SERVICIO_PRINCIPAL}}` — fases, forma de pago (p. ej. por hito aceptado), menú de entregables (puede ser borrador).
3. `{{REPO_ENTREGA}}` — documentos de fases y módulos del servicio. Si el checkout local puede ir
   atrasado, leer `git show origin/main:<ruta>` en vez de hacer pull.
4. `{{ARCHIVO_CASOS}}` — solo casos con `publicable: true`; obedecer la nota y los comentarios de permiso
   de cada caso (validar testimonio, pedir permiso antes de nombrar clientes activos).
5. Contacto + QR: `{{CONTACTO}}` y su SVG de QR.

El vocabulario interno (jerga de método, términos técnicos de la casa) nunca aparece en una pieza.

## Forma de la oferta (escalera, cada peldaño con entregables)

Diagnóstico corto (pago único, deja un entregable tangible) → Piloto (un entregable) → Programa principal
en una o dos versiones, pagado por cuotas al aprobar cada hito. Ofertas online o 1:1 son adicionales.
Decir siempre que el cliente puede parar después de cualquier peldaño. Las cifras salen de la nota 1,
nunca de este archivo.

## Set de piezas (prospecto primero)

- Brochure principal, 4 páginas A4: portada + dolores (“¿Te suena?”) · qué hacemos (capas, ciclo, menú
  en lenguaje del cliente) · cómo empezar (escalera, tarjetas de precio, gráfico fases/cuotas) · casos +
  garantías + contacto/QR.
- One-pager del diagnóstico: los días como timeline, qué te llevas, precio, “y después decides”.
- Brochure de 2 páginas para la oferta de agentes de IA: hub (agente + herramientas), funciones, timeline
  de “un lunes cualquiera” sin cifras inventadas, antes/después, para quién, cómo contratar dentro de la escalera.
- One-pagers viejos que venden un modelo retirado están obsoletos: proponer reemplazarlos, no borrarlos en silencio.

## Build

- Generador en `{{RUTA_GENERADORES}}` que reutiliza el sistema del manual de marca (logo/isotipo como HTML,
  font-faces de `{{FUENTE_TITULOS}}`/`{{FUENTE_ETIQUETAS}}`, `{{FUENTE_CUERPO}}` para texto, vocabulario
  vectorial de diagramas, iconos). CSS compacto propio con tamaños legibles fijados directamente
  (cuerpo 12 pt, etiquetas 9,5 pt) — sin pasada de reescalado.
- Salida en `{{RUTA_ENTREGABLES}}`; el build genera en una carpeta ignorada (`_salida/`) y luego publica.
  Nunca editar a mano los PDFs publicados.
- Script de render (Playwright/Chromium) → PDF + PNG por página; sale con código ≠ 0 ante cualquier
  elemento fuera de `.cuerpo`, solapamiento de hermanos o texto < 9,5 pt (HTML y SVG). Corregir hasta que
  todas las páginas den ok; luego generar una tira JPG vertical por pieza multipágina para mensajería,
  `zbarimg` sobre los PNG y barrer el texto extraído por CJK / otro idioma / palabras internas.
- Etiquetas de diagramas: dimensionar el texto SVG para el ancho renderizado (viewBox ≈ px de columna);
  preferir un diagrama pequeño hecho a medida antes que encoger una figura del manual.
- Precios en un solo dict (`{{ARCHIVO_PRECIOS}}`); las notas pueden ir atrás de lo que dicta el usuario,
  así que confirmar precios con él antes de enviar.
- Si un catálogo se genera desde archivos de módulo del repositorio de entrega, reescribir los criterios
  de “hecho” de tercera persona (“el cliente”) a segunda (“tú”).

## Checklist de la respuesta

Listar lo que no pudiste decidir: validación de testimonios, menú en borrador, línea online sin
plataforma, clientes que requieren permiso, descuentos sin decidir.
