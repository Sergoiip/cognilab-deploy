#!/usr/bin/env python3
"""Genera `bootstrap/encuesta.html`, una encuesta estática (sin servidor, abre con doble clic)
para que el CLIENTE la llene solo antes de la instalación. Al final arma el texto del
manifiesto (YAML) y lo muestra para copiar o descargar.

No depende de red ni de ninguna cuenta: todo corre en el navegador del cliente, en su propio
equipo. El archivo generado es autocontenido (HTML+CSS+JS en un solo archivo).

Lee los módulos y paquetes reales del repo — regenerar este archivo cada vez que cambien
modulos/ o paquetes/, para que la encuesta nunca quede desincronizada (igual que avisa
tools/verificar.py sobre otras partes del repo).

Uso:
    tools/generar_encuesta_html.py
"""
import json
import pathlib

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
SALIDA = REPO / "bootstrap" / "encuesta.html"


def cargar_modulos():
    mods = []
    for f in sorted(REPO.glob("modulos/*/*/modulo.yaml")):
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
        mods.append({"id": m["id"], "nombre": m["nombre"], "bloque": m["bloque"]})
    return mods


def cargar_paquetes():
    paq = {}
    for f in sorted((REPO / "paquetes").glob("*.yaml")):
        p = yaml.safe_load(f.read_text(encoding="utf-8"))
        paq[f.stem] = {
            "nombre": p["paquete"],
            "obligatorios": p.get("obligatorios", []),
            "elegir": p.get("principal", {}).get("elegir", 0),
            "entre": p.get("principal", {}).get("entre", []),
        }
    return paq


def main():
    modulos = cargar_modulos()
    paquetes = cargar_paquetes()
    datos_js = json.dumps({"modulos": modulos, "paquetes": paquetes}, ensure_ascii=False)

    html = HTML_TEMPLATE.replace("__DATOS__", datos_js)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(html, encoding="utf-8")
    print(f"Generado {SALIDA} ({len(modulos)} módulos, {len(paquetes)} paquetes)")


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Encuesta de ingreso — CogniLab</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
  h1 { font-size: 1.4rem; }
  fieldset { border: 1px solid #8884; border-radius: 8px; margin-bottom: 1.2rem; padding: 1rem; }
  legend { font-weight: 600; }
  label { display: block; margin: 0.6rem 0 0.2rem; }
  input[type=text], select, textarea { width: 100%; padding: 0.4rem; box-sizing: border-box; }
  .modulo-opcion { display: flex; align-items: baseline; gap: 0.5rem; margin: 0.3rem 0; }
  .ayuda { font-size: 0.85rem; opacity: 0.75; margin: 0.2rem 0 0.6rem; }
  button { padding: 0.6rem 1.2rem; font-size: 1rem; cursor: pointer; }
  pre { background: #8882; padding: 1rem; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; }
  .bloque-titulo { font-weight: 600; margin-top: 0.8rem; }
</style>
</head>
<body>
<h1>Encuesta de ingreso — tu sistema con CogniLab</h1>
<p class="ayuda">
  Esta página no envía nada a ningún servidor: todo queda en tu navegador. Al final te da un
  texto para copiar o un archivo para descargar — eso es lo que le mandas a Sergio.
</p>

<form id="f">
  <fieldset>
    <legend>Datos básicos</legend>
    <label for="cliente">Tu nombre o el de tu negocio</label>
    <input type="text" id="cliente" required>

    <label for="paquete">Paquete</label>
    <select id="paquete"></select>

    <label for="escala">¿Cómo trabajas?</label>
    <select id="escala">
      <option value="1">Solo yo (individuo)</option>
      <option value="2">Con mi negocio (1 a 5 personas)</option>
      <option value="3">Con un equipo (varios roles)</option>
    </select>

    <label for="vault">¿Dónde quieres que viva tu bóveda de notas? (ruta en tu equipo)</label>
    <input type="text" id="vault" value="~/Documents/Obsidian/Bóveda-cliente">
  </fieldset>

  <fieldset>
    <legend>Módulos principales</legend>
    <p class="ayuda" id="obligatorios-info"></p>
    <div id="opciones-modulos"></div>
  </fieldset>

  <fieldset>
    <legend>Nivel de acompañamiento</legend>
    <label><input type="radio" name="acompanamiento" value="tecnico" checked>
      Quiero entender mi agente y sacarle el máximo provecho (técnico)</label>
    <label><input type="radio" name="acompanamiento" value="integral">
      Quiero resultados, sin tecnicismo (integral)</label>
  </fieldset>

  <fieldset>
    <legend>Tu agente (opcional)</legend>
    <label for="nombre_agente">¿Cómo quieres llamar a tu agente?</label>
    <input type="text" id="nombre_agente" placeholder="ej. Vera, Argos, Nova...">
    <label for="personalidad">¿Qué personalidad/tono quieres que tenga?</label>
    <input type="text" id="personalidad" placeholder="ej. cálido, directo, sin jerga técnica">
  </fieldset>

  <fieldset>
    <legend>Herramientas</legend>
    <label><input type="checkbox" id="ya_sabe"> Ya sé qué apps quiero usar (si no marcas esto, te proponemos un paquete estándar)</label>
    <label for="ya_usa">Apps que ya usas y quieres conservar (separadas por coma, opcional)</label>
    <input type="text" id="ya_usa" placeholder="ej. obsidian, git">
    <label for="cuentas">Cuentas que vas a crear tú mismo (separadas por coma)</label>
    <input type="text" id="cuentas" value="telegram">
  </fieldset>

  <button type="button" onclick="generar()">Generar mi manifiesto</button>
</form>

<div id="resultado" style="display:none; margin-top:1.5rem;">
  <h2>Listo — esto es tu manifiesto</h2>
  <p class="ayuda">Copia este texto o descarga el archivo y envíaselo a Sergio.</p>
  <pre id="salida"></pre>
  <button type="button" onclick="descargar()">Descargar manifiesto.yaml</button>
  <button type="button" onclick="copiar()">Copiar texto</button>
</div>

<script>
const DATOS = __DATOS__;
let yamlTexto = "";

function poblar() {
  const selPaquete = document.getElementById("paquete");
  for (const slug in DATOS.paquetes) {
    const opt = document.createElement("option");
    opt.value = slug;
    opt.textContent = DATOS.paquetes[slug].nombre;
    selPaquete.appendChild(opt);
  }
  selPaquete.addEventListener("change", pintarModulos);
  pintarModulos();
}

function pintarModulos() {
  const slug = document.getElementById("paquete").value;
  const pq = DATOS.paquetes[slug];
  document.getElementById("obligatorios-info").textContent =
    "Siempre incluye: " + pq.obligatorios.join(", ") + ". Elige " + pq.elegir + " módulo(s) más:";
  const cont = document.getElementById("opciones-modulos");
  cont.innerHTML = "";
  for (const mid of pq.entre) {
    const m = DATOS.modulos.find(x => x.id === mid);
    if (!m) continue;
    const div = document.createElement("div");
    div.className = "modulo-opcion";
    const tipo = pq.elegir > 1 ? "checkbox" : "radio";
    div.innerHTML = `<input type="${tipo}" name="modulo_elegido" value="${m.id}" id="mod-${m.id}">
      <label for="mod-${m.id}" style="margin:0;">${m.id} — ${m.nombre}</label>`;
    cont.appendChild(div);
  }
}

function yamlEscape(s) {
  if (s === "" || s == null) return '""';
  if (/^[A-Za-z0-9 ,.áéíóúñÁÉÍÓÚÑ¿?¡!/()\\-]*$/.test(s) && !s.includes(": ")) return s;
  return JSON.stringify(s);
}

function generar() {
  const cliente = document.getElementById("cliente").value.trim() || "[cliente]";
  const paquete = document.getElementById("paquete").value;
  const escala = document.getElementById("escala").value;
  const vault = document.getElementById("vault").value.trim();
  const acompanamiento = document.querySelector('input[name="acompanamiento"]:checked').value;
  const nombreAgente = document.getElementById("nombre_agente").value.trim();
  const personalidad = document.getElementById("personalidad").value.trim();
  const yaSabe = document.getElementById("ya_sabe").checked;
  const yaUsa = document.getElementById("ya_usa").value.split(",").map(s => s.trim()).filter(Boolean);
  const cuentas = document.getElementById("cuentas").value.split(",").map(s => s.trim()).filter(Boolean);

  const pq = DATOS.paquetes[paquete];
  const elegidos = Array.from(document.querySelectorAll('input[name="modulo_elegido"]:checked')).map(el => el.value);
  const idsModulos = [...new Set([...pq.obligatorios, ...elegidos])];

  let lineas = [];
  lineas.push(`cliente: ${yamlEscape(cliente)}`);
  lineas.push(`paquete: ${paquete}`);
  lineas.push(`acompanamiento: ${acompanamiento}`);
  lineas.push(`vault: ${vault}`);
  lineas.push("modulos:");
  for (const id of idsModulos) lineas.push(`  - {id: ${id}, escala: ${escala}}`);
  lineas.push("herramientas:");
  lineas.push(`  modo: ${yaSabe ? "cliente" : "asignar"}`);
  lineas.push("  perfil: auto");
  lineas.push(`  ya_usa: [${yaUsa.join(", ")}]`);
  lineas.push("  extras: []");
  lineas.push("  excluir: []");
  lineas.push(`  cuentas: [${cuentas.join(", ")}]`);
  if (nombreAgente || personalidad) {
    lineas.push("agente:");
    if (nombreAgente) lineas.push(`  nombre: ${yamlEscape(nombreAgente)}`);
    if (personalidad) lineas.push(`  personalidad: ${yamlEscape(personalidad)}`);
  }

  yamlTexto = lineas.join("\\n") + "\\n";
  document.getElementById("salida").textContent = yamlTexto;
  document.getElementById("resultado").style.display = "block";
  document.getElementById("resultado").scrollIntoView({behavior: "smooth"});
}

function descargar() {
  const blob = new Blob([yamlTexto], {type: "text/yaml"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "manifiesto.yaml";
  a.click();
}

function copiar() {
  navigator.clipboard.writeText(yamlTexto).then(() => alert("Copiado."));
}

poblar();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
