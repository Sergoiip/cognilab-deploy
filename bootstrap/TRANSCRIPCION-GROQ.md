# Transcripción de audios del gateway con Groq

**Cuándo:** justo después de configurar el gateway (Telegram, WhatsApp u otro canal) y de comprobar
que el agente responde un mensaje de texto. Sin este paso, las notas de voz que el cliente le manda
a su agente usan la transcripción local (lenta en equipos sin GPU) o no se transcriben.

**Por qué Groq:** Groq Whisper (`whisper-large-v3-turbo`) transcribe en uno o dos segundos y tiene
un plan gratuito que alcanza para el uso normal de un negocio. La cuenta y la clave son **del
cliente**, no de CogniLab.

## 1. El cliente crea su clave (a mano, 2 minutos)
1. Entra a <https://console.groq.com> con su correo y abre **API Keys → Create API Key**.
2. Le pone un nombre reconocible (por ejemplo, «Hermes · transcripción») y copia la clave. Groq
   solo la muestra una vez.

## 2. Guardar la clave sin que quede en el historial ni en el chat
El cliente la pega en **su propia terminal**. Ni el agente ni quien instala la teclean, y nunca se
pega en un chat:

```bash
read -rsp "Pega tu clave de Groq y presiona Enter: " K && hermes config set GROQ_API_KEY "$K"; unset K; echo
```

`hermes config set` la guarda en el `.env` del perfil (no en `config.yaml`). Si el cliente usa
varios perfiles, antepone `hermes -p <perfil>` o exporta `HERMES_HOME` del perfil que atiende el
gateway.

## 3. Activar Groq como proveedor de transcripción
Esto sí lo puede correr el agente o quien instala. No toca secretos:

```bash
hermes config set stt.enabled true
hermes config set stt.provider groq
hermes config set stt.groq.language es      # idioma del cliente; omitir para autodetectar
```

## 4. Reiniciar el gateway y probar con un audio real
El gateway lee el `.env` al arrancar, así que hay que reiniciarlo. El reinicio se pide con
aprobación del cliente y se corre desde una terminal fuera del gateway:

```bash
hermes gateway restart
```

Luego el cliente le manda a su agente **una nota de voz de 5 a 10 segundos**. El paso está hecho
cuando el agente responde al contenido del audio. Si responde como si no hubiera entendido:

```bash
grep -i -E "stt|groq|transcri" "$(hermes config path | xargs dirname)/logs/gateway.log" | tail
```

| Mensaje en el log | Causa | Arreglo |
|---|---|---|
| `GROQ_API_KEY not set` | La clave no quedó en el perfil del gateway | Repetir el paso 2 en ese perfil y reiniciar |
| `401` / `invalid_api_key` | Clave mal copiada o revocada | Crear otra en la consola y repetir el paso 2 |
| `STT provider 'groq' configured but unavailable` | Instalación de Hermes incompleta (el cliente de Groq usa el SDK `openai`, que viene con Hermes) | `hermes doctor`, arreglar lo que marque y reiniciar |
| `413` / archivo muy grande | Audio de más de 25 MB (plan gratuito) | Hermes lo parte solo; si persiste, audios más cortos |

## Criterio de hecho
- [ ] Clave guardada por el cliente en su terminal (no aparece en ningún chat ni archivo del repo).
- [ ] `hermes config get stt.provider` responde `groq`.
- [ ] Una nota de voz real fue respondida por el agente según su contenido.
