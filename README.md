# cognilab-deploy

Paquetes instalables para dejar el equipo de un cliente listo, según el modelo de **entregables en 90 días**.
Repo privado. Es el producto técnico; **los precios, cuotas y condiciones viven en Cadence**, no aquí:
`Cadence/Services/Paquetes por entregables — modelo 90 días`.

## Dos ejes
- **Paquete** (qué módulos entran): `Esencial` o `Integral` → `paquetes/`.
- **Escala del cliente** (qué profundidad): 1 individuo, 2 negocio, 3 equipo → `escalas.md`.

## Estructura
```
modulos/       22 entregables en 5 bloques (A a E), cada uno con SKILL.md, modulo.yaml y variantes/1,2,3
paquetes/      esencial.yaml, integral.yaml
fases/         las 3 fases de 90 días y su hito
fichas/        ficha de ingreso y de cierre
criterios/     criterios de "hecho" para aprobar
bootstrap/     instala.sh: PC listo desde un manifiesto
manifiestos/   ejemplo; el del cliente real NO se versiona
tools/         verificar.py: estructura + sincronía con Cadence
```

## Flujo con un cliente
1. Fase 1: llenar `fichas/ingreso.md` → sale el manifiesto (paquete + módulos + escala).
2. Fase 2: `bootstrap/instala.sh manifiestos/cliente-X.yaml` (usa `--dry-run` antes).
3. Fase 3: `fichas/cierre.md`, medición contra línea base, aceptación.
4. Anotar en Cadence la versión instalada (`VERSION` en el equipo del cliente).

## Mantener la sincronía
`python3 tools/verificar.py` falla si hay precios, nombres de clientes o rastros de otros clientes en el repo,
o si el menú de Cadence menciona una meta-skill que ningún módulo implementa. Avisa si el entregable de Cadence
cambió desde el último `--sellar`.

## Reglas
- Sin credenciales, sin precios, sin datos de clientes.
- Un módulo no es "hecho" hasta cumplir su criterio y los comunes (`criterios/`).
