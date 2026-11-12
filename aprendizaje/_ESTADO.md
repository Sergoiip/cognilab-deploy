# Estado de este paquete en el repo

Llegó el 2026-11-03 como «CogniLab Deploy - Aprendizaje acumulado.zip» y se incorporó en 0.23.0 tal cual (los 66 archivos coinciden con `Manifiesto.json`).
Es **material para revisar e integrar por módulo**, no una actualización: las skills de ese paquete no están enlazadas todavía desde `modulos/` (las adoptadas después se listan abajo).

Para adoptar una: seguir `Métodos/Integración del aprendizaje acumulado.md` (Adopción por módulo), copiarla al módulo que la necesite, agregarla a `requiere_skills_hermes` en su `modulo.yaml` y anotarlo en `stack/CHANGELOG.md`.

## Adoptadas (0.24.0)
- `designed-pdf-deliverables`, `svg-brand-assets` y `visual-taxonomy`: llegaron aparte del paquete del 2026-11-03, ya abstraídas en dos niveles, y están enlazadas desde C1 (Identidad de marca), C2 (Propuestas y cobros), C3 (Reportes) y E2 (Entrega verificada). Siguen siendo plantillas con `{{PARÁMETROS}}`: cada instalación las completa con la marca del cliente.

## Adoptadas (0.30.0): las skills que pedían los módulos y no viajaban
Antes vivían solo en el Hermes del consultor; ahora están aquí, desidentificadas (sin nombres, rutas personales, precios, contactos ni IDs) y con sus comandos y pitfalls concretos:
- Propias abstraídas: `agent-playbook-and-handoff` (B1), `bandeja-social-respuestas-composio` (C5), `bot-whatsapp-atencion-clientes` y `formulario-reserva-a-crm` (B2), `daily-startup-today-plan` y `daily-close-wrapup` (A3), `edicion-reels-ffmpeg-subtitulos` (C6), `metricas-retencion-y-reciclaje-de-contenido` (C3), `obsidian-mcp-integration` (B4), `propuestas-persuasivas-neuroventa` (C2).
- Fusionadas: `messaging-gateway-qr-link` absorbe `messaging-customer-bot-profile` (B2); `storage-cleanup-organization` absorbe `storage-optimizer-approval-workflow` (A4, A5); `local-meeting-transcription` (0.2.0) suma la transcripción de archivos con Whisper local que traía `local-audio-transcription` (B3, C6).
- `docx` y `xlsx` (E2): copia tal cual de las skills MIT de Nous Research (con su `LICENSE`). Ya no vienen en el paquete de Hermes y en el hub solo aparecen versiones de otros autores, así que viajan desde aquí.
- `capcut` (D2) no se copia: es de un tercero y se instala del hub con su identificador exacto (`stack/skills_hermes.yaml`).
`instala.sh` (paso 6/7) instala las de los módulos activos en `$HERMES_HOME/skills/cognilab-replicables/`. `tools/skills_hermes.py auditar` comprueba que ninguna skill pedida quede sin fuente.
