---
name: cd-manifiesto-en-vivo
description: "Use when installing CogniLab on a client: build the manifest live."
version: 1.0.0
author: CogniLab
license: personal
metadata:
  hermes:
    tags: [cognilab, instalacion, manifiesto, onboarding]
---

# Manifiesto en vivo (durante la instalación)

El manifiesto del cliente ya no se llena antes. Se arma **durante la instalación**, cuando
Hermes ya está corriendo en el equipo: tú le haces las preguntas con tus ventanas de respuesta
(la herramienta `clarify`) y el script escribe el YAML. El cliente nunca ve YAML.

## Cuándo
- Acaban de correr `bootstrap/instala.sh --base` y el cliente (o Sergio a su lado) te dice
  «arma mi manifiesto», «sigamos con la instalación» o algo equivalente.
- Hay que cambiar un manifiesto ya hecho (después de la sesión de mapeo del Ecosistema):
  mismas rondas, empezando con las respuestas actuales como recomendadas.

## Qué ya está instalado
Los 22 módulos (`cd-*`) ya están en el equipo desde `--base`. El manifiesto no instala ni
bloquea módulos: decide cuáles quedan **activos** (archivo `ACTIVOS` junto a esta skill) según
el paquete. Solo usa como entregable del cliente un módulo activo; si el cliente pide algo de un
módulo inactivo, dile que está fuera de su paquete y que se lo comentas a Sergio.

## Procedimiento

1. **Lee las opciones reales del repo, nunca de memoria:**
   `python3 ~/cognilab-deploy/tools/manifiesto_en_vivo.py opciones`
   De ahí salen los paquetes (Esencial, Ecosistema) y los módulos con su nombre.

2. **Pregunta en rondas cortas con `clarify`, varias preguntas por llamada.** En cada pregunta
   cerrada pon como `choices` las opciones del JSON, en el lenguaje del cliente: nombres
   funcionales, no IDs ni jerga. Si la respuesta ya se dijo en la conversación, no la vuelvas a
   preguntar.
   - **Ronda 1 · quién y qué:** nombre corto del cliente o negocio; paquete (Esencial = 1 mes,
     un solo frente; Ecosistema = todas las metas, 3 a 4 meses, empieza con sesión de mapeo);
     tamaño (solo yo / un negocio / un equipo → escala 1, 2, 3).
   - **Ronda 2 · el frente:** en Esencial, UNA pregunta de opción única: «¿qué es lo que más
     urge resolver?», con máximo 4 opciones sacadas de `entre` según lo que ya contó; el resto
     cabe en «Otro». En Ecosistema, una de selección múltiple (`multi_select`) con los frentes
     que ya se sabe que van, y aclara que la sesión de mapeo puede ajustarlos.
   - **Ronda 3 · su agente y su forma de trabajar:** cómo quiere llamar a su agente y con qué
     personalidad (abiertas, opcionales); acompañamiento (quiero entender cómo funciona →
     `tecnico` / quiero resultados sin tecnicismo → `integral`); dónde va su bóveda (propón
     `~/Documents/Obsidian/<Negocio>`).
   - **Ronda 4 · herramientas:** ¿ya sabe qué apps quiere usar o se las proponemos?
     (`cliente` / `asignar`); qué cuentas va a crear a mano (Telegram, WhatsApp Business, Google
     Drive; `multi_select`). El ritmo de trabajo (`ritmo:`) es opcional: solo si el cliente
     tiene el módulo A3 o lo pide, y entonces siguiendo `bootstrap/ORGANIZACION-TEMPORAL.md`.

3. **Escribe las respuestas en un JSON y guárdalo con el script** (nunca escribas el YAML a mano):
   `python3 ~/cognilab-deploy/tools/manifiesto_en_vivo.py guardar /tmp/respuestas.json`
   Si responde «NO SE GUARDÓ», el mensaje dice qué falta o qué no cuadra (por ejemplo, un
   Esencial con dos frentes). Pregunta solo eso y vuelve a guardar.

4. **Muestra un resumen de 5 líneas en lenguaje del cliente** (paquete, frente o frentes, nombre
   del agente, bóveda, cuentas a mano) y corre la simulación:
   `bash ~/cognilab-deploy/bootstrap/instala.sh <manifiesto> --dry-run`
   Pide aprobación con un `clarify` de dos opciones («Aprobado, instalar» / «Cambiar algo»).

5. **Solo con «Aprobado»:** `bash ~/cognilab-deploy/bootstrap/instala.sh <manifiesto>`.
   Es idempotente: encima de la base agrega lo que el manifiesto pide. Al terminar reporta lo que
   salió de verdad (versión, qué se instaló, qué falló, la lista «a mano») y sigue con
   `bootstrap/PRIMEROS-PASOS.md`.

## Reglas
- El manifiesto tiene datos del cliente: se queda en `manifiestos/` (git lo ignora), no se pega
  en un chat de grupo ni se sube a ningún lado.
- No modifiques `config.yaml`, `.env` ni claves. Si algo pide `sudo`, di cuál comando y espera.
- No inventes respuestas para cerrar el manifiesto rápido: lo que el cliente no sepa queda con el
  valor recomendado y se marca para revisar en la sesión de mapeo o en la Radiografía.
- Un manifiesto del Ecosistema es provisional hasta la sesión de mapeo. Después del mapeo se
  repiten las rondas que cambien y se corre `instala.sh` de nuevo.
