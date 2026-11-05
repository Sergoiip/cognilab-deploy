---
tipo: metodo-replicable
version: 1.0.0
estado: preparado-no-instalado
---
# Medición local sin atribución inventada

## Parámetros
PERIODO con zona horaria, DISPOSITIVO, BUCKET_VENTANAS, BUCKET_AFK, CONSENTIMIENTO y DESTINO_AGREGADO.

## Método
1. Seleccionar un solo dispositivo y emparejar sus fuentes de ventanas y presencia. No sumar equipos sin conciliación de solapamientos.
2. Delimitar periodo y cobertura reales. Recortar intervalos a sus extremos, unir presencia y detectar ventanas solapadas antes de sumar.
3. Calcular intersección de ventanas con presencia activa, separar actividad sin ventana y ausencias. Comprobar igualdad de totales por agrupación y que la actividad atribuida no exceda presencia.
4. Conservar análisis de títulos localmente solo con consentimiento. Las reglas configuradas producen candidatos, no trabajo de cliente confirmado. Coincidencias múltiples quedan ambiguas y ausencia de coincidencia queda sin atribución.
5. Publicar únicamente agregados permitidos. Excluir títulos, URLs, eventos crudos e identificadores de equipo. Incluso nombres de aplicaciones y categorías pueden ser sensibles: revisar audiencia.
6. Contrastar con entregables, decisiones y aceptación para evaluar procesos. Tiempo observado, horas aprobadas e ingreso son magnitudes distintas.

## Pruebas necesarias antes de implementar
Intervalos vacíos, adyacentes, solapados, límites del día, cambio horario, múltiples hosts y ausencia de fuente AFK. La implementación local revisada tiene reglas particulares y selección horaria dependiente del entorno; no se incluye ni se certifica portable. No se consultó telemetría real en esta exportación.

Origen: síntesis nueva de prácticas locales revisadas; no incorpora fuentes privadas ni código de terceros.
