#!/usr/bin/env python3
"""Faro de misión: crea una misión del Ágora a partir de una plantilla del catálogo, en la fecha del faro.
La crea `tools/flota.py mision`, así que respeta el presupuesto del manifiesto (en modo manual nace
bloqueada y aparece en «Esperando tu OK»). Es idempotente: si la misión ya existe, no la duplica.

Uso: lanzar_mision.py <plantilla> <manifiesto> [clave=valor ...]"""
import os, shutil, subprocess, sys
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if len(sys.argv) < 3:
    print("⚠️ Faro de misión mal configurado: falta la plantilla o el manifiesto"); sys.exit(0)
plantilla, manifiesto, pares = sys.argv[1], sys.argv[2], sys.argv[3:]
uv = shutil.which("uv") or os.path.expanduser("~/.local/bin/uv")
cmd = [uv, "run", "-q", "--no-project", "--with", "pyyaml", "python3", os.path.join(RAIZ, "tools", "flota.py"),
       "mision", plantilla, manifiesto, "--si"]
for kv in pares:
    cmd += ["--var", kv]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=RAIZ)
salida = (r.stdout + r.stderr).strip()
if r.returncode != 0 or "✗" in salida:
    print(f"⚠️ No pude crear la misión «{plantilla}»:\n{salida[-600:]}")
else:
    import glob
    rutina = any("rutina_aprobada: true" in open(f, encoding="utf-8").read() and f"id: {plantilla}\n" in open(f, encoding="utf-8").read()
                 for f in glob.glob(os.path.join(RAIZ, "flota", "misiones", "*", "*.yaml")))
    if rutina and "Tope diario" not in salida:
        pass   # rutina aprobada: entra lista a la estación, en silencio; el aviso llega con el resultado
    else:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_comun"))
        from agora import con_codigos
        salida = con_codigos(salida)
        print(f"🧭 Misión nueva en el Ágora («{plantilla}»):\n{salida}\n\nEstá bloqueada hasta que la sueltes: dile a ARG.OS «suelta» y el número entre corchetes.")
