---
name: knowledge-package-export
description: Use when exporting reusable knowledge packages.
version: 0.1.0
---

# Exportación y abstracción de conocimiento reutilizable

## Parámetros a configurar
| Parámetro | Propósito |
|---|---|
| {{FUENTES_AUTORIZADAS}} | Raíces de skills, métodos, referencias y herramientas a revisar |
| {{METADATOS_CREACION}} | Evidencia fiable para distinguir propio, ampliado y ajeno |
| {{REGISTRO_ALCANCE}} | Intención explícita y cobertura inventariada |
| {{DESTINO_ABSTRACCION}} | Árbol genérico separado de origen y runtime |
| {{EXPORTADOR}} | Herramienta reproducible revisada y probada |
| {{ARCHIVO_ENTREGA}} | Archivo nuevo sin destruir historial |
| {{ESTADO_ABSTRACCION}} | Estado privado de skill a huella fuente |
| {{ESTADO_HERRAMIENTAS}} | Inventario anterior para diferencias |
| {{EXCLUSIONES}} | Copias de lectura, dependencias, secretos y datos no autorizados |
| {{CRITERIO_TITULARIDAD}} | Criterio documentado de autorización de herramientas |
| {{CARPETAS_METODOS}} | Métodos agnósticos a empaquetar |
| {{CARPETAS_HERRAMIENTAS}} | Herramientas propias permitidas |
| {{PATRON_SENSIBLE}} | Patrones privados y revisión manual asociados |
| {{AUDIENCIA}} | Destinatarios y nivel de distribución |

## Propósito
Exportar conocimiento autorizado, reproducible y sin contexto privado. Determinar alcance por la intención explícita, no por el último ejemplo: «todo lo hecho y aprendido» o actualización global exige inventario de todas las skills locales, aportes a skills instaladas, referencias, métodos y herramientas revisables. No equivale a permiso de redistribuir todo ni de instalarlo.

## Cuándo usar
Exportación, regeneración, abstracción externa e inventario de conocimiento acumulado. No usar para transferir credenciales ni como respaldo privado de una operación. Un pedido acotado a un kit conserva ese alcance; un pedido global no se reduce al último kit.

## Entradas
Fuentes reales, metadatos fiables de creación, intención de alcance, destino, exportador y estados anteriores. Si faltan registros, construir evidencia de lo revisable y declarar huecos; no fabricar autoría ni inventario. Un lote delegado solo cubre su subconjunto dentro del inventario global.

## Pasos
1. Recuperar contexto e inspeccionar fuentes reales. Inventariar según alcance explícito y clasificar propio, ampliación y ajeno/no confirmado con metadatos de creación fiables. Preservar originales y entregas anteriores; no borrar ni limpiar sin permiso.
2. Nivel 1: retirar personas, organizaciones, clientes, precios, rutas personales, direcciones de red, correos, teléfonos, identificadores y secretos. Convertir valores configurables en tokens nombrados sin valores; poner tabla de parámetros al inicio. No incluir datos reales de prueba.
3. Nivel 2: reescribir capacidad, propósito, cuándo usar, entradas, pasos, decisiones, verificación, pitfalls y variantes como método completo. Mantener marcas, productos y hardware solo en implementación de referencia, también auditada y sin identidades.
4. Crear una carpeta instalable por skill con nombre genérico, descripción corta que comience por «Use when», versión y última línea de origen genérico. No atribuir autoría humana ni licencias nuevas. Referencias acompañan el método, no lo reemplazan por un índice vacío.
5. Dividir lotes manejables con fuentes y destinos explícitos. Verificar personalmente los archivos entregados; un resumen delegado no basta. En ejecución programada procesar secuencialmente sin preguntas y bloquear fuentes no auditadas.
6. Auditar texto y referencias con búsquedas insensibles a mayúsculas y revisión manual. No marcar abstraído con hallazgos reales. Diferenciar marcas técnicas permitidas en referencia de identidades privadas prohibidas en cualquier nivel.
7. Probar exportador con datos sintéticos y casos de fallo. Justo antes de entregar, ejecutarlo para recalcular inventario y manifiesto, evitar duplicados y rutas peligrosas, excluir secretos y fuentes no autorizadas y verificar integridad de archivo y huellas por entrada.
8. Solo tras auditoría satisfactoria registrar estado contra huella del archivo fuente normalizado. Informar fuentes nuevas/cambiadas pendientes y herramientas nuevas, modificadas o retiradas a partir de comparación real de inventarios, no memoria.
9. Emitir mapa fuente→destino, archivos y exclusiones, cobertura, conteo y tamaño derivados de ejecución. Adjuntar archivo verificado solo si se produjo. Distinguir entrega documental, instalación y actualización real del despliegue; no afirmar estas últimas sin ejecutarlas y probarlas.

## Decisiones
Los metadatos fiables determinan clasificación; una línea Origen de una copia no acredita titularidad. Un inventario acotado no demuestra cobertura global. Excluir plugins/scripts ajenos sin autorización; incluso una herramienta propia debe quedar sin datos locales. Herramientas no abstraídas se etiquetan o excluyen en entrega externa. Cambiar exportador o programación exige respaldo y validación; no programar tareas sin pedido.

## Verificación
Una sola copia por skill, manifiesto contra bytes, inventario contra fuentes actuales, mapa y exclusiones completos, auditoría sin hallazgos reales y estado actualizado solo después de éxito. Probar rechazo de rutas inseguras, duplicados, corrupción y material prohibido. Verificar que el archivo contiene todos los métodos autorizados, no solo que abre. La prueba de empaquetado no prueba despliegue.

## Pitfalls
Los auditores pueden coincidir con sus propios patrones: revisar en contexto sin desactivar controles de referencias. Excluir cachés compiladas, estados privados, resultados de ensayo, archivos ocultos, enlaces simbólicos y binarios no autorizados. La extracción puede carecer de fuentes privadas para regenerar: declararlo. No dar por abstraído todo por un archivo válido ni limitar alcance global a la última tarea.

Distinguir enumeración, hash calculado, estructura inspeccionada y lectura completa: calcular una huella no demuestra revisión ni titularidad. Inventariar exclusiones sensibles sin abrir ni calcular su hash. Descubrir también extensiones de herramientas menos obvias y unidades de servicio; hallarlas no autoriza su distribución. Separar una herramienta nueva escrita para la entrega de una herramienta antigua parametrizada y probar cada una por su alcance real.

## Variantes
Interna con contenido autorizado; externa con doble abstracción; periódica no interactiva conservando última entrega válida; kit documental sin instalación; actualización global con inventario transversal y subconjuntos explícitos por procedencia.

## Referencia técnica
Consultar [Implementación de referencia](references/Implementación%20de%20referencia.md) solo al concretar herramientas; el método no depende de esa implementación. Esta entrega es documental e instalable como carpeta de skill; no acredita instalación ni prueba del entorno receptor. Resolver los parámetros antes de ejecutar; no pegar tokens sin sustituir.

Origen: aprendizaje operativo abstraído y desidentificado; sin atribución de autoría humana ni licencia nueva.
