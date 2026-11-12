---
name: agent-playbook-and-handoff
description: Use when handing work or a kickoff prompt to another agent.
version: 1.0.0
---

# Manual operativo y traspaso a otro agente

## Cuándo usarla
El usuario pide documentar un proceso "para el agente", preparar un texto para enviarlo a un
cliente/colaborador, o "dame lo que falta y ordena los archivos". Hay que archivar una secuencia
operativa nueva y referenciarla en el mapa de métodos. Muy relevante al instalar o configurar
agentes de IA en otra máquina: esta skill produce el manual y el texto de traspaso que el
receptor pega en su propio Hermes.

## Dónde vive cada cosa (ajustar a la bóveda del cliente)
- **Base de conocimiento:** la raíz de la bóveda del cliente, donde se archivan los documentos
  operativos.
- **Manuales/secuencias:** una subcarpeta de operaciones, por defecto `Operaciones/Secuencias/`.
- **Métodos reutilizables:** por defecto `Metodos/<categoría>/`.
- **Notas sueltas:** por defecto `Ideas/` con su índice.
- **Mapa de métodos:** la nota índice global de métodos de la bóveda.
- **Canal:** el canal que operará el receptor (mensajería, correo, chat web).
- **Responsables:** la persona con nombre que resuelve precios y la que resuelve escalados.
  Pregúntalas si no están en la bóveda; nunca pongas "el equipo".
- **Idioma:** el de los documentos existentes del cliente.

## Propósito
Dejar por escrito un flujo de trabajo para que lo ejecute alguien distinto del dueño (agente de
IA de terceros, nuevo miembro, colaborador externo) sin que el dueño intervenga. Entregables: un
manual operativo archivado, un texto de traspaso pegable y la lista de lo que aún bloquea la
activación.

## Entradas
- Descripción del flujo y del canal.
- Lo que ya existe en la bóveda (secuencias, catálogos, activos, formularios, enlaces, precios).
- Límite de autoridad que se quiere delegar.

## Pasos
1. **Mapear el estado actual antes de escribir.** Listar lo que ya existe y leer los documentos
   vigentes. Buscar por nombre la secuencia/activo antes de redactar uno nuevo; un manual que
   reinventa un paso ya cubierto se rechaza.
2. **Redactar el manual** en la carpeta de secuencias con el orden de secciones de abajo.
3. **Redactar el texto de traspaso** como bloque corto aparte: qué archivos leer y en qué orden,
   reglas duras y límites explícitos. Es lo que el usuario pega en el otro agente.
4. **Archivar los activos** que el manual referencia (logos, fuentes, PDF, formularios, enlaces)
   y crear las notas de apoyo (definición de campos, índice de recursos) para que no quede
   ninguna referencia colgando.
5. **Listar lo que falta** como checklist numerada, un responsable por ítem.
6. **Reportar** en el chat: texto de traspaso, archivos creados y dónde viven, bloqueos y
   decisiones que aún debe tomar el usuario. Si el manual es largo, enviarlo como adjunto.

## Estructura del manual (orden que funciona)
1. **Línea de propósito** — una frase: quién lo ejecuta, de dónde a dónde, qué reemplaza.
2. **Quién es quién** — personas y autoridad; quién aprueba qué.
3. **Herramientas** — tabla necesidad → cómo (herramienta, registro o "pendiente"). Marcar
   explícitamente las integraciones no disponibles.
4. **Tabla de precios/tarifas** — solo cifras confirmadas. Lo no confirmado = "escalar al
   responsable de precios" (con su nombre). El agente nunca inventa cifras.
5. **Fases/pasos** — tabla disparador → acción → activo. Una fila por momento, con el activo
   exacto a adjuntar.
6. **Reglas de oro** — 4 a 6 reglas inquebrantables, cada una con su razón en una cláusula.
7. **Mensajes listos** — bloques copiar/pegar por momento (apertura, cierre, cobro, recordatorio,
   recompra), cortos y con el tono de la marca del cliente.
8. **Pendiente antes de activar** — checklist de bloqueos.

## Formato del texto de traspaso
```
Vas a operar <canal> de <negocio>. <alcance: decide X, escala Y>.

Lee estos N archivos antes de empezar:
1. <ruta>  <- <para qué>
...

Reglas:
- <regla dura>
- <límite explícito: qué NO puede ver/hacer y qué hace en su lugar>
- <todo se registra en la base de conocimiento>
```
Los `<...>` se rellenan con los datos reales al redactar; el texto entregado no lleva huecos.

## Reglas de decisión
- **El traspaso debe llegar más lejos que el manual anterior, no copiarlo.** Si el dueño dice "ya
  no quiero que me entregue X", el receptor ahora *decide* ese paso (cerrar la venta, agendar,
  confirmar pago) y el manual nombra explícitamente la nueva decisión que posee.
- **Declarar los límites del agente** en el manual y en la respuesta. Nunca insinuar que ve algo
  que no ve (cuentas bancarias, bandeja de entrada, calendario del dueño): decir qué hace en su
  lugar (recibe un comprobante, marca un registro, escala).
- **Todo ítem indecidible se enruta a una persona con nombre**, no a "el equipo". Tablas de
  precios y filas de escalado llevan nombre.
- **"Lo que falta" es entregable de primera clase**: cerrar el reporte con la checklist numerada
  y responsable por ítem.
- Si ya existe una secuencia (p. ej. incorporación), el nuevo manual apunta a ella y añade solo
  los pasos nuevos.
- Un manual no aprobado lleva `status: Draft` en el frontmatter; se cambia solo cuando el usuario
  lo indica, y el manual dice qué pasos bloquea mientras tanto.

## Verificación
- Comprobar que cada activo referenciado existe realmente en disco antes de entregar.
- Comprobar que ninguna cifra, política o dato de contacto está inventado.
- Comprobar que cada campo que el agente pide al cliente tiene: nombre exacto, dónde se guarda y
  qué hacer si falta.
- Comprobar que el reporte nombra las decisiones pendientes del usuario.

## Pitfalls
- Precios/políticas/contactos inventados: peor que escalar. Lo no confirmado va a la lista de
  bloqueos con responsable.
- Un manual que termina en "el agente pide los datos al cliente" está incompleto: especificar
  campos, almacenamiento y caso de dato faltante.
- Duplicar una secuencia existente hace que ambas diverjan.
- Referenciar un PDF/archivo que nunca se archivó es el fallo más común de esta tarea.
- En pasos de dinero, decir qué puede y qué no puede verificar el agente (recibe comprobante y
  marca registro; el dueño confirma el dinero). No describirlo como "recibe transferencias" si
  no ve la cuenta.
- Si el flujo es de cara al cliente por mensajería, el despliegue (perfil restringido,
  herramienta de agenda, renovación de credenciales caducadas) se documenta aparte; esta skill
  posee la documentación y el traspaso.

## Variantes
- **Receptor humano** (nuevo empleado, freelancer): el texto de traspaso es una guía de
  bienvenida; los límites se expresan como permisos de acceso.
- **Receptor agente de IA**: añadir límites de herramientas y reglas de escalado; el texto de
  traspaso se pega en su chat.
- **Actualización v2 de un manual**: actualizar las notas que apuntan a la v1 y borrar la versión
  obsoleta en lugar de conservar ambas.

## Variante: prompt de arranque para otra sesión (proyecto grande de software/producto)
Cuando el usuario pide "el prompt exacto para crear la tarea en otra sesión", el entregable es un
prompt pegable más sus parámetros. No se crea el tablero ni se lanza nada sin que lo pida.
1. **Preguntar con formularios numerados y con opciones** (clarify, máximo 5 por tanda, la
   opción recomendada primero), no con preguntas abiertas en prosa. Primera tanda: alcance del
   MVP, convivencia con datos y herramientas existentes, usuarios y distribución, partes que
   necesitan servidor, ejecutor. Segunda tanda: sincronización del equipo, alcance de cada
   módulo, apps de referencia, nombre.
2. **No entregar el prompt mientras falte un insumo que el usuario anunció** (boceto,
   documento). Resumir lo decidido y pedir lo que falta; un prompt a medias no sirve.
3. **Boceto en imagen:** vision_analyze sobre la imagen completa y después sobre recortes
   (`region`) para el texto manuscrito. Las palabras ambiguas se preguntan como opciones; no se
   adivinan. Si aparecen siglas de métodos propios del usuario, cargar la skill de ese método
   para cruzar los términos.
4. **Investigar antes de escribir:** licencia de cada código que se va a reutilizar (manifest de
   `.obsidian/plugins/*`, repo upstream); choque de nombres (web + para plugins de Obsidian
   `community-plugins.json` de obsidianmd/obsidian-releases); ubicación del código fuente y del
   repo de la bóveda (`git remote -v`, `gh repo view --json visibility`).
5. **Reglas que el prompt debe llevar siempre:** skills exactas que se cargan; rutas reales;
   límite legal (código MIT/propio se reutiliza conservando el aviso; apps privativas solo por
   documentación pública y observación pasiva); compuerta de aprobación tras la especificación
   (tarjetas sin assignee hasta aprobar, goal mode solo después); desarrollo en copia de prueba y
   nunca sobrescribir campos puestos a mano; datos personales jamás en un repo compartido por
   el equipo; preguntas finales en formulario numerado.
6. **Archivar:** el prompt va a la carpeta de método/producto de la bóveda del cliente, en una
   subcarpeta por proyecto. Los archivos pesados (bocetos >5 MB) van a una carpeta de trabajo
   fuera de la bóveda (una por proyecto) y en la bóveda queda una copia WebP liviana
   (`magick ... -resize 3200x -quality 88`).
7. **Verificar** con un script: existen todas las rutas citadas y cada skill nombrada tiene un
   `SKILL.md` en `~/.hermes/skills` (o en el directorio de skills del perfil activo). Después se
   entrega el archivo (MEDIA:) con las decisiones que se tomaron sin preguntar y una pregunta
   final: ¿lo lanzo yo o lo pegas tú?
