# Estado de este paquete en el repo

Llegó el 2026-11-03 como «CogniLab Deploy - Aprendizaje acumulado.zip» y se incorporó en 0.23.0 tal cual (los 66 archivos coinciden con `Manifiesto.json`).
Es **material para revisar e integrar por módulo**, no una actualización: las skills de ese paquete no están enlazadas todavía desde `modulos/` (las adoptadas después se listan abajo).

Para adoptar una: seguir `Métodos/Integración del aprendizaje acumulado.md` (Adopción por módulo), copiarla al módulo que la necesite, agregarla a `requiere_skills_hermes` en su `modulo.yaml` y anotarlo en `stack/CHANGELOG.md`.

## Adoptadas (0.24.0)
- `designed-pdf-deliverables`, `svg-brand-assets` y `visual-taxonomy`: llegaron aparte del paquete del 2026-11-03, ya abstraídas en dos niveles, y están enlazadas desde C1 (Identidad de marca), C2 (Propuestas y cobros), C3 (Reportes) y E2 (Entrega verificada). Siguen siendo plantillas con `{{PARÁMETROS}}`: cada instalación las completa con la marca del cliente.
