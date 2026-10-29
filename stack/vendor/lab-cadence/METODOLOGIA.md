# Lab Cadence — metodología y recomendaciones de uso

Este documento explica el **por qué** detrás de Lab Cadence (qué problema resuelve y cómo usarlo
bien), no el qué cambió en el código — eso está en `CAMBIOS.md`.

## Qué problema resuelve

Un negocio de servicios tiene cuatro cosas que se pierden si no viven en un solo lugar: quién es
cliente, qué se le vendió, qué pasó en cada sesión/actividad, y cuánto entró o salió de dinero.
Lab Cadence es la **fuente única de verdad transaccional** del negocio dentro de la bóveda: no
hay un Excel aparte de plata, ni una libreta aparte de clientes. Si algo no está en Cadence, para
el negocio no pasó.

## Principios de uso (heredados del método A2 — Second Brain)

1. **Una fuente de verdad por dato.** El dinero se anota en Cadence, no en el chat ni en una nota
   suelta "para después pasarlo". Si se dictó por chat, la primera acción es registrarlo aquí.
2. **Campos fijos, no texto libre donde hay una lista.** `status`, `paid`, `category` etc. deben
   usar exactamente los valores del esquema — un valor inventado ("pagado parcial" en vez de un
   estado real) rompe los reportes y los filtros silenciosamente, sin error visible.
3. **Anotar lo dicho tal cual, confirmar lo ambiguo.** No inferir que algo "ya se pagó" porque
   suena lógico; si no es explícito, se pregunta antes de marcarlo.
4. **Una nota en la carpeta equivocada es invisible.** Los reportes leen por carpeta
   (`Cadence/Gastos`, deals, contactos); un gasto guardado fuera de su carpeta no aparece en
   Finanzas aunque el archivo exista.
5. **Revisión periódica, no solo al cerrar un trato.** El valor de tener esto en un solo lugar se
   pierde si solo se mira una vez al mes — ver "Cuándo revisar" abajo.

## El reporte de Finanzas (v2) — cómo leerlo

- **Cobrado vs. por cobrar:** separa lo que ya entró de lo que está comprometido pero pendiente.
  Un negocio con mucho "por cobrar" y poco "cobrado" tiene un problema de flujo de caja aunque las
  ventas se vean bien.
- **Utilidad neta vs. proyectada:** la neta es con lo ya cobrado; la proyectada asume que cobra
  todo lo pendiente. La diferencia entre ambas es el riesgo real del mes.
- **Egresos por categoría, recurrentes vs. puntuales:** los recurrentes son el piso de gasto fijo
  del mes (lo que sale sí o sí); los puntuales son la parte que se puede ajustar.
- **Botón "Sin pagos al socio":** sirve para ver la utilidad operativa real del negocio,
  separando los retiros del dueño/socio del gasto operativo — sin este filtro, un mes con un
  retiro grande se ve como un mes de pérdidas aunque el negocio esté sano.
- **Cobrado por cliente:** sirve para identificar concentración de ingresos en pocos clientes
  (riesgo) y para decidir dónde poner atención comercial.

## Estancados (15 días)

Un deal o contacto sin edición en 15 días aparece marcado. **La acción correcta no es ignorarlo**
ni cerrarlo por default: es decidir en ese momento si sigue vivo (y escribir el siguiente paso) o
si se cierra como perdido con una razón. Dejarlo estancado sin decisión es la forma más común en
que el pipeline se llena de ruido con el tiempo.

## Cuándo revisar (recomendación de cadencia)

- **Diario (rápido, 2-3 min):** ¿algo que se dictó por chat hoy ya quedó registrado?
- **Semanal:** revisar Finanzas del mes en curso y la lista de estancados; decidir cada uno.
- **Mensual/cierre:** comparar con el mes anterior (el propio reporte lo hace), y archivar
  decisiones tomadas sobre estancados y proyecciones.

## Qué NO hacer

- No dejar un campo "a medias" esperando completarlo después — si falta un dato, se marca
  explícitamente como pendiente, nunca se deja vacío sin aviso.
- No registrar plata en dos lugares (Cadence y otra hoja/app) "por si acaso": genera
  discrepancias que nadie sabe cuál es la verdadera.
- No ajustar manualmente un total que el reporte calcula — si el número parece mal, el error está
  en el dato de origen (un campo mal puesto), no en el reporte.

## Configuración por cliente

Los valores en `data.json > lab` (`staleDays`, `expensesFolder`, `ownerPaymentPattern`,
`ownerLabel`) se ajustan por bóveda sin tocar código — ver la tabla en `CAMBIOS.md`. Cambiar
`staleDays` cambia la disciplina de seguimiento, no solo un número: bajarlo a menos de 15 días en
negocios de ciclo de venta largo puede generar ruido falso.
