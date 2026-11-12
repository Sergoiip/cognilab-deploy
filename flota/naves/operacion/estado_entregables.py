#!/usr/bin/env python3
"""Faro «Estado de entregables por cliente» (Flota · sector operación).

Lee los proyectos ACTIVOS del CRM (frontmatter `status: active`) y arma, por cliente:
atrasados, lo que vence en la ventana, entregados y sin fecha. Si no hay nada atrasado
ni por vencer, no imprime nada (silencio).

Fuentes que entiende, sin pedir que se dupliquen datos:
  1. Listas de tareas dentro de «## Milestones» (o «## Hitos» / «## Entregables»):
       - [ ] Revisión de entregables del mes 1 (27 nov 2026).     -> fecha en la línea
       - [ ] 20-nov: renegociar el contrato                       -> año inferido del proyecto
       **Mes 2 · 28 nov – 27 dic · Producción**                   -> los ítems debajo vencen el 27 dic
       - [x] ...                                                  -> entregado
  2. Una tabla «## Entregables» con columnas Fecha | Entregable | Estado.

Uso:  estado_entregables.py --raiz <carpeta de proyectos> [--incluir <texto>]... [--dias 7] [--hoy AAAA-MM-DD] [--todo]
      --todo imprime el informe aunque no haya nada urgente (para revisarlo a mano).
"""
import argparse, datetime as dt, pathlib, re, sys

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7,
         "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12}
NOMBRE_MES = {v: k for k, v in MESES.items() if k != "set"}
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
SECCION = re.compile(r"^##\s*(milestones|hitos|entregables)\b", re.I)
HECHO_TXT = re.compile(r"^\s*\**\s*(hech|entregad|listo|pagad|cerrad)", re.I)
M = (r"(ene(?:ro)?|feb(?:rero)?|mar(?:zo)?|abr(?:il)?|may(?:o)?|jun(?:io)?|jul(?:io)?|ago(?:sto)?"
     r"|sep(?:tiembre)?|set(?:iembre)?|oct(?:ubre)?|nov(?:iembre)?|dic(?:iembre)?)\.?(?![a-záéíóúñ])")
_ISO = r"(\d{4})-(\d{2})-(\d{2})"
_LARGA = r"(\d{1,2})\s*(?:de\s+)?" + M + r"\s*(?:de\s+)?(\d{4})"
_CORTA = r"(\d{1,2})[-\s]" + M
RX_RANGO = re.compile(r"(\d{1,2})\s*" + M + r"\s*[–-]\s*(\d{1,2})\s*" + M, re.I)
# Solo cuenta como fecha de ENTREGA la que va al inicio del ítem («20-nov: …», «2026-10-10 — …»)
# o sola entre paréntesis («(27 nov 2026)»). Una fecha suelta en el texto («corrección 5-nov»,
# «pedido del 09-nov») es historia, no vencimiento: ahí manda la fecha del bloque del mes.
FORMAS = [(_ISO, "iso"), (_LARGA, "larga"), (_CORTA, "corta")]
INICIO = [(re.compile(r"^\W*" + rx + r"\s*[:—–-]", re.I), k) for rx, k in FORMAS]
PARENT = [(re.compile(r"\(\s*" + rx + r"\s*\)", re.I), k) for rx, k in FORMAS]


def frontmatter(txt):
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    out = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln and not ln.startswith(" "):
                k, v = ln.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def anio_base(fm):
    for k in ("started", "inicio", "created"):
        m = re.match(r"(\d{4})-(\d{2})", fm.get(k, ""))
        if m:
            return int(m[1]), int(m[2])
    return dt.date.today().year, 1


def con_anio(dia, mes, base):
    y, m0 = base
    return dt.date(y + (1 if mes < m0 else 0), mes, dia)


def _a_fecha(m, k, base):
    if k == "iso":
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    if k == "larga":
        return dt.date(int(m[3]), MESES[m[2][:3].lower()], int(m[1]))
    return con_anio(int(m[1]), MESES[m[2][:3].lower()], base)


def fecha_en(texto, base, celda=False):
    """Fecha de entrega de un ítem. En una celda de tabla vale cualquier forma."""
    t = re.sub(r"[*_`]", "", texto)
    pruebas = ([(re.compile(r"^\s*" + rx, re.I), k) for rx, k in FORMAS] if celda else INICIO + PARENT)
    for rx, k in pruebas:
        if (m := rx.search(t)):
            try:
                return _a_fecha(m, k, base)
            except ValueError:
                return None
    return None


def limpiar(txt):
    t = re.sub(r"\[\[([^\]|]+)\|?([^\]]*)\]\]", lambda m: m[2] or m[1], txt)
    t = re.sub(r"[*_`]", "", t).strip()
    t = re.split(r"\s+[—–-]{1,2}\s+(?=\S)", t)[0] if len(t) > 90 else t
    return (t[:87] + "…") if len(t) > 90 else t


def entregables(nota):
    txt = nota.read_text(encoding="utf-8", errors="ignore")
    fm = frontmatter(txt)
    if fm.get("status", "").lower() not in ("active", "activo", "in-progress", "en curso"):
        return None, []
    base = anio_base(fm)
    items, dentro, fecha_bloque, cab = [], False, None, None
    for ln in txt.splitlines():
        if ln.startswith("#"):
            dentro, fecha_bloque, cab = bool(SECCION.match(ln)), None, None
            continue
        if not dentro:
            continue
        s = ln.strip()
        if s.startswith("**") and (r := RX_RANGO.search(s)):
            fecha_bloque = con_anio(int(r[3]), MESES[r[4][:3].lower()], base)
            continue
        if (m := re.match(r"^\s*[-*]\s*\[( |x|X)\]\s*(.+)$", ln)):
            hecho = m[1].lower() == "x"
            f = fecha_en(m[2], base) or fecha_bloque
            txt = m[2]
            for rx, _ in INICIO:                 # «20-nov: renegociar…» -> «renegociar…»
                txt = rx.sub("", re.sub(r"[*_`]", "", txt), count=1) if rx.search(re.sub(r"[*_`]", "", txt)) else txt
            items.append({"txt": limpiar(txt), "fecha": f, "hecho": hecho})
            continue
        if s.startswith("|"):
            c = [x.strip() for x in s.strip("|").split("|")]
            low = [x.lower() for x in c]
            if cab is None:
                if any("fecha" in x for x in low) and any("estado" in x for x in low):
                    cab = {"fecha": next(i for i, x in enumerate(low) if "fecha" in x),
                           "estado": next(i for i, x in enumerate(low) if "estado" in x),
                           "txt": next((i for i, x in enumerate(low) if "entregable" in x), None)}
                continue
            if set("".join(c)) <= set("-: ") or max(cab["fecha"], cab["estado"]) >= len(c):
                continue
            items.append({"txt": limpiar(c[cab["txt"]] if cab["txt"] is not None else c[0]),
                          "fecha": fecha_en(c[cab["fecha"]], base, celda=True),
                          "hecho": bool(HECHO_TXT.match(c[cab["estado"]]))})
    nombre = re.sub(r"^.*?—\s*", "", nota.stem) if "—" in nota.stem else nota.stem
    return nombre, items


def corto(d):
    return f"{DIAS[d.weekday()]} {d.day}-{NOMBRE_MES[d.month]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--hoy")
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--incluir", action="append", default=[],
                    help="solo proyectos cuyo nombre contenga este texto (repetible); lo define el manifiesto")
    a = ap.parse_args()
    hoy = dt.date.fromisoformat(a.hoy) if a.hoy else dt.date.today()
    raiz = pathlib.Path(a.raiz)
    if not raiz.is_dir():
        print(f"⚠️ Estado de entregables: no encuentro los proyectos en {raiz}")
        return
    bloques, urgente = [], False
    for nota in sorted(raiz.glob("*.md")):
        if a.incluir and not any(x.lower() in nota.stem.lower() for x in a.incluir):
            continue
        cliente, items = entregables(nota)
        if not cliente or not items:
            continue
        abiertos = [i for i in items if not i["hecho"]]
        atras = sorted([i for i in abiertos if i["fecha"] and i["fecha"] < hoy], key=lambda i: i["fecha"])
        pronto = sorted([i for i in abiertos if i["fecha"] and 0 <= (i["fecha"] - hoy).days <= a.dias],
                        key=lambda i: i["fecha"])
        sinf = [i for i in abiertos if not i["fecha"]]
        hechos = len(items) - len(abiertos)
        if atras or pronto:
            urgente = True
        elif not a.todo:
            continue
        b = [f"\n▸ {cliente} · {hechos}/{len(items)} entregados"]
        for i in atras:
            b.append(f"  🔴 atrasado desde {corto(i['fecha'])}: {i['txt']}")
        for i in pronto:
            d = (i["fecha"] - hoy).days
            b.append(f"  🟡 {'hoy' if d == 0 else corto(i['fecha'])}: {i['txt']}")
        if sinf:
            b.append(f"  ⚪ {len(sinf)} sin fecha" + (": " + "; ".join(i["txt"] for i in sinf[:3]) if sinf else "")
                     + (" …" if len(sinf) > 3 else ""))
        bloques.append("\n".join(b))
    if not urgente and not a.todo:
        return
    print(f"📦 Entregables · semana del {corto(hoy)}" + "".join(bloques))
    print("\nMarca [x] en Milestones cuando algo se entregue; el faro lo deja de mostrar.")


if __name__ == "__main__":
    sys.exit(main())
