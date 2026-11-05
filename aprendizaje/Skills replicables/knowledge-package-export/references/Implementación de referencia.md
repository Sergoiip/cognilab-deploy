# Implementación de referencia

## Formato y separación
La referencia usa carpetas `SKILL.md` con frontmatter YAML, subcarpeta `references/` y entrega ZIP. Un exportador Python puede trabajar con `pathlib`, `hashlib` y `zipfile`; esta skill no incluye ni copia un exportador existente. Resolver {{EXPORTADOR}}, inspeccionarlo y ejecutar pruebas sintéticas antes de usarlo sobre datos autorizados. No confundir con la instalación en un runtime de Hermes Agent: esa sería una acción separada con autorización y verificación de descubrimiento.

Mantener el mapa exacto de orígenes y metadatos privados fuera del árbol distribuible si contiene rutas o identidades. En el paquete solo colocar nombres y enlaces relativos genéricos. El inventario privado decide alcance; no debe filtrarse como un manifiesto público. Los metadatos `created_by` o creador equivalente tienen que estar respaldados por registros reales; el valor de una línea Origen no es sustituto.

## Huellas y estado
La referencia utiliza SHA-256 del `SKILL.md` fuente normalizado a LF y los primeros 12 dígitos hexadecimales para estado de abstracción. Para integridad del paquete, conservar hashes completos y tamaños por entrada del manifiesto; los 12 dígitos de estado no sustituyen estos hashes. Releer fuentes cambiadas antes de abstractarlas y recalcular estado al final. No copiar las huellas de un inventario anterior si hubo modificaciones durante el trabajo.

## Exportación segura
Preservar entrega anterior y publicar archivo nuevo. Seleccionar archivos por lista permitida; rechazar enlaces simbólicos, nombres absolutos, componentes de ascenso de directorio y duplicados normalizados. No confiar solo en extensión. Verificar `ZipFile.testzip()` para CRC, reabrir cada entrada y comparar tamaño y SHA-256 con manifiesto; contar entradas y skills desde lectura del ZIP. Los fixtures deben cubrir recorrido de rutas, colisión de nombre, corrupción, secreto excluido y conservación de entrega anterior ante fallo.

Los resultados de prueba y estados permanecen fuera del árbol público. Para ejecución recurrente, bloquear fuentes pendientes de auditoría y conservar el último artefacto válido. No crear cron ni modificar runtime al abstraer documentos. Si solo se encarga un subconjunto de fuentes, reportar al coordinador esa cobertura sin renombrarla como inventario global completo.

## Evidencia y límites
Separar propuesta de exportador, pruebas de fixtures, exportación real y prueba de instalación. Ninguno implica automáticamente los otros. Una referencia técnica no concede derechos sobre código de terceros ni permite incluir configuraciones o credenciales.

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
