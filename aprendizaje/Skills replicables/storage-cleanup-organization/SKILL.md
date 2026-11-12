---
name: storage-cleanup-organization
description: Use when freeing disk space or tidying folders.
version: 1.0.0
---

# Limpieza de espacio y organización de carpetas

## Cuándo usar
Poco espacio libre; limpiar/organizar Descargas, discos externos o estructuras desordenadas;
diseñar una jerarquía de carpetas; antes de enlazar una carpeta local a sincronización en la nube;
liberar espacio en varias unidades cruzando local vs nube vs estado de proyectos, cuando el
borrado no debe decidirse solo por tamaño/antigüedad sino con el visto bueno explícito del
responsable por cada lote.

**Propósito:** diagnosticar qué ocupa el espacio, clasificar archivos y reorganizarlos (disco
local, descargas, unidades externas, nube) sin perder nada y sin borrar sin verificación explícita.
**Nunca se elimina nada sin aprobación final del responsable.**

## Flujo base (en este orden)
1. **Medir antes de actuar.** `df -h` por unidad y `du -sh */` por carpeta de primer nivel. Casi
   siempre el grueso son una o dos carpetas enormes, no las muchas pequeñas que sospecha el usuario.
2. **Nunca borrar un zip (o carpeta "ya extraída") por tamaño o nombre.** Verificar byte a byte:
   mismo número de archivos y mismo tamaño por archivo entre el zip y la carpeta (Python `zipfile`
   + `os.path.getsize`; los totales de `du` pueden coincidir por azar). Revisar la papelera del
   sistema por nombre+tamaño antes de concluir que el zip es la única copia.
3. **Clasificar por patrón de nombre antes de mover.** Script con regex por categoría (proyecto,
   exportaciones genéricas tipo `SinTituloN`, nombres UUID, marcadores de duplicado `- copia`/`(n)`);
   imprimir resumen por categoría (conteo+tamaño) y guardar el plan en JSON. Si el usuario pidió
   "prepáralo para decidir", no ejecutar movimientos en la misma pasada: entregar el plan y esperar
   el visto bueno.
   - Fecha real de un archivo: tomarla de metadatos cuando existan (`ffprobe`/EXIF para media),
     `mtime` solo como respaldo.
   - Confirmar la profundidad del árbol deseado con un ejemplo concreto de ruta antes de mover
     cientos de archivos.
4. **Mover con un script idempotente** (no comandos shell ad-hoc sueltos): crea destinos, omite lo
   que ya está en destino, registra cada movimiento, imprime conteo final. Renombrar en lote a una
   secuencia nueva: hacerlo en dos pasadas (todo a nombre temporal, luego al definitivo) para evitar
   colisiones.
5. **Respetar la jerarquía de trabajo real del usuario, no una taxonomía genérica impuesta.**
6. **Antes de enlazar una carpeta a la nube**, terminar la organización local primero.
7. **Candidatos a borrar porque "ya están en la nube": verificar en dos etapas.** Etapa 1:
   inventario paginado de la nube (`fields` con `id,name,size,md5Checksum`) cruzado por
   nombre+tamaño exacto. Etapa 2: solo para esa lista corta, hash MD5 local por bloques vs el de
   la nube. Solo el MD5 igual justifica recomendar borrar. Pedir confirmación explícita aun con
   100% de coincidencia.
   - Inventarios grandes: procesar en lotes acotados (p. ej. 5 páginas), persistiendo `all_files`
     + `pageToken` en JSON tras cada lote para poder reanudar sin perder progreso.

## Flujo de aprobación antes de borrar
Úsalo cuando el borrado implica varias unidades o proyectos activos/cerrados.

### Reglas que no se rompen
- **Solo lectura hasta la aprobación.** Escanear, hashear y reportar no modifica nada. Borrar
  solo tras OK explícito para ESA corrida y ESE lote.
- **Borrar = enviar a la papelera del sistema** (reversible), nunca borrado permanente. Excepción:
  unidades sin papelera fiable (exFAT externo) → mover a una carpeta de cuarentena fechada.
- **Prueba de "ya está en la nube" = nombre + tamaño exacto + MD5 igual.** Nombre+tamaño solo
  preselecciona.
- **Nunca tocar:** proyectos activos, trabajo más reciente, carpetas de sistema, carpetas del
  propio agente, la bóveda de notas, la unidad de nube montada, papelera del sistema.
- Lotes acotados con progreso persistido en JSON (reanudable); una corrida larga sin persistir
  mata el proceso.

### Paso 0 · Descubrir unidades y la verdad de los proyectos
1. Unidades conectadas en tiempo de ejecución (`psutil.disk_partitions()`).
2. **Estado de proyectos desde el gestor de proyectos/CRM de la bóveda** (solo lectura): derivar
   por proyecto/caso activo / en curso / entregado / cerrado. Estado ambiguo → tratarlo como activo
   (no tocar) y listarlo en «Dudas».
3. Inventario completo de la nube paginado (persistiendo el `pageToken`).

### Modo A · Escaneo manual a demanda
1. `du` por unidad/carpeta de primer nivel.
2. Enumerar archivos grandes (>50MB) recursivamente, guardar `{ruta, tamaño, mtime, unidad}` en
   JSON.
3. Cruce con la nube en dos etapas (nombre+tamaño, luego MD5). Clasificar: `SEGURO-EN-NUBE`
   (candidato) / `NOMBRE-IGUAL-DISTINTO-HASH` (NO borrar) / `SOLO-LOCAL` (NO borrar, sugerir subir
   primero).
4. Otras categorías solo como propuesta: duplicados locales, zips ya extraídos (verificados
   archivo a archivo), caché/proxies de apps (solo reportar tamaño).

### Modo B · Depuración periódica (cada 3-6 meses)
Tabla de antigüedad editable por el responsable:

| Qué | Antigüedad mínima | Condiciones |
|---|---|---|
| Material original ya entregado/cerrado | 3 meses desde cierre | MD5 igual en nube **y** proyecto entregado/cerrado |
| Versiones intermedias/sincronizadas | 6 meses | MD5 igual en nube **y** sin correcciones abiertas |
| Proyecto activo / sin entregar | **Nunca** | Siempre excluido |

Cadencia: tarea programada trimestral que SOLO genera el reporte; nunca ejecuta borrado.

### Reporte y aprobación (obligatorio antes de borrar)
1. Resumen: espacio libre por unidad, GB liberables, nº de archivos.
2. Tabla: proyecto/categoría | archivos | GB | prueba (MD5✓) | antigüedad | acción propuesta.
3. Secciones aparte: «Dudas», «Copia única», «Versión distinta en nube».
4. Pregunta final explícita: «¿Apruebo el lote X?». Aprobación por lote; ejecutar solo lo
   aprobado, re-verificando tamaño justo antes de borrar.

## Notas de entorno
- Discos exFAT/macOS montados en Linux/Windows acumulan archivos `._*` (AppleDouble): pesan poco
  pero inflan conteos. Seguros de borrar, pero ofrecer cuarentena primero
  (`_MetadataMac_AppleDouble/`).
- Listados de más de ~2000 entradas se truncan: redirigir a archivo y paginar.

## Formato del informe
Tabla ordenada por tamaño (carpeta/categoría | tamaño | nº elementos | veredicto), de mayor a
menor. Toda recomendación destructiva termina con una pregunta de confirmación explícita; nunca
borrar/mover sin que el usuario lo diga, aun con verificación limpia.

## Pitfalls
- Borrar un zip sin verificar; mover en la misma pasada que clasificar; confiar solo en `mtime`;
  olvidar sidecars de archivos emparejados; bucles de paginación sin persistir progreso; imponer
  una taxonomía ajena al flujo real del usuario.
- Archivo "sincronizando" aún no subido: la API de la nube es la verdad, no la carpeta montada
  localmente.
- Archivos nativos de suites ofimáticas en la nube no tienen MD5: ignorarlos.

## Variantes
- **Producción de video/audio/foto:** aplican sidecars de cámara (XML/THM), prefijos de
  grabación y etapas tipo grabación→edición→entrega; cambiar solo los patrones de nombre y la
  jerarquía por las etapas del flujo real del usuario.
- **Automatización por evento** (al conectar un disco, cron periódico): en Linux, `udev`/`systemd`
  en vez de Task Scheduler.
- **Otra nube** (Dropbox, S3, NAS): mismo esquema inventario→nombre+tamaño→hash, sustituyendo el
  inventario por la API equivalente.
- **Sin gestor de proyectos:** el responsable declara a mano qué está activo; ante duda, activo.
