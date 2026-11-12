# Espacio de trabajo por cliente (patrón ICM)

Adaptación de la *Interpretable Context Methodology* (Van Clief y McDermott, arXiv 2603.16021, MIT) al deploy. Qué se toma y qué no:

**Se toma**
- Capas de lectura: `CLAUDE.md` (dónde estoy) → `CONTEXT.md` (a dónde voy) → `CONTEXT.md` de la etapa (qué hago) → referencias → artefactos de la corrida. El agente se detiene cuando ya tiene lo que necesita.
- Etapas = carpetas numeradas, cada una con `output/`. La salida de una etapa es la entrada de la siguiente.
- Contrato fijo por etapa: **Entradas, Proceso, Salidas**.
- Referencias de un solo sentido: una etapa apunta a lo que necesita; nadie apunta de vuelta.
- Revisión humana entre etapas. Coincide con el principio de poner a la persona al centro.

**No se toma / límites**
- ICM es de un solo usuario. Un cliente de escala 3 con varias personas escribiendo a la vez necesita permisos y turnos que ICM no da; allí el espacio se usa como mapa de lectura, no como control de acceso.
- La evidencia que presenta el paper es informal (reportes de una comunidad cerrada, un solo tipo de modelo). Aquí es una **hipótesis a probar**, no un resultado.

## Uso
```
python3 tools/espacio.py crear manifiestos/cliente-X.yaml --destino <carpeta> [--dry-run] [--forzar]
python3 tools/espacio.py estado <carpeta>
```
`instala.sh ... --espacio` lo crea dentro de la bóveda del manifiesto (`vault:`). Nunca sobrescribe un archivo que ya existe, salvo con `--forzar`: lo que la persona editó se respeta.

## Qué genera
```
CLAUDE.md                  capa 0
CONTEXT.md                 capa 1
etapas/01-diagnostico-y-base/CONTEXT.md + output/
etapas/02-construccion/CONTEXT.md + output/
etapas/03-consolidacion/CONTEXT.md + output/
referencias/               fichas, criterios de hecho, escalas
```
Los textos son genéricos. Los datos del cliente solo se escriben en el equipo del cliente, nunca en este repo.
