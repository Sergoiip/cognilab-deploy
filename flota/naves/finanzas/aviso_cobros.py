#!/usr/bin/env python3
"""Faro «Aviso de cobros próximos» (Flota · sector finanzas).

Lee las tablas de pagos de las notas del CRM y avisa los cobros pendientes que vencen
pronto o que ya vencieron. Si no hay nada que avisar, no imprime nada (el cron se queda en silencio).

Uso:
  aviso_cobros.py --raiz <carpeta del CRM> [--dias 3] [--hoy AAAA-MM-DD]

Convención de la tabla (dentro de una sección «## Pagos», «## Cobros» o «## Cuotas»):
  | Fecha | Monto | Cubre | Estado |
Fecha admite «12 nov 2026», «2026-11-12» o «12/11/2026». Estado que empieza por
Pagado, Cobrado, Anulado o Cancelado no se avisa.
"""
import argparse, datetime as dt, pathlib, re, sys

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7,
         "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12}
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
CERRADO = re.compile(r"^\s*\**\s*(pagad|cobrad|anulad|cancelad)", re.I)
SECCION = re.compile(r"^#{2,3}\s*(pagos|cobros|cuotas)\b", re.I)


def fecha(txt):
    t = re.sub(r"[*_`]", "", txt).strip().lower()
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
    if m:
        return dt.date(int(m[3]), int(m[2]), int(m[1]))
    m = re.match(r"(\d{1,2})\s*(?:de\s+)?([a-zé]{3})[a-zé]*\.?\s*(?:de\s+)?(\d{4})", t)
    if m and m[2][:3] in MESES:
        return dt.date(int(m[3]), MESES[m[2][:3]], int(m[1]))
    return None


def celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def cobros(nota):
    lineas = nota.read_text(encoding="utf-8", errors="ignore").splitlines()
    dentro, cab = False, None
    for ln in lineas:
        if ln.startswith("#"):
            dentro, cab = bool(SECCION.match(ln)), None
            continue
        if not dentro or not ln.strip().startswith("|"):
            continue
        c = celdas(ln)
        if cab is None:
            low = [x.lower() for x in c]
            if any("fecha" in x for x in low) and any("estado" in x for x in low):
                cab = {k: next(i for i, x in enumerate(low) if k in x)
                       for k in ("fecha", "estado") }
                cab["monto"] = next((i for i, x in enumerate(low) if "monto" in x or "valor" in x), None)
                cab["cubre"] = next((i for i, x in enumerate(low) if "cubre" in x or "concepto" in x), None)
            continue
        if set("".join(c)) <= set("-: "):
            continue
        if max(cab["fecha"], cab["estado"]) >= len(c):
            continue
        f = fecha(c[cab["fecha"]])
        if f and not CERRADO.match(c[cab["estado"]]):
            yield {"fecha": f,
                   "monto": c[cab["monto"]] if cab["monto"] is not None and cab["monto"] < len(c) else "",
                   "cubre": c[cab["cubre"]] if cab["cubre"] is not None and cab["cubre"] < len(c) else "",
                   "nota": nota.stem}


def corto(d):
    return f"{DIAS[d.weekday()]} {d.day}-{[k for k, v in MESES.items() if v == d.month and k != 'set'][0]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--dias", type=int, default=3)
    ap.add_argument("--hoy")
    a = ap.parse_args()
    hoy = dt.date.fromisoformat(a.hoy) if a.hoy else dt.date.today()
    raiz = pathlib.Path(a.raiz)
    if not raiz.is_dir():
        print(f"⚠️ Aviso de cobros: no encuentro el registro en {raiz}")
        return
    vistos, avisos = set(), []
    for nota in sorted(raiz.rglob("*.md")):
        for c in cobros(nota):
            clave = (c["fecha"], c["monto"], c["cubre"])
            if clave in vistos:          # la misma tabla copiada en Pipeline y Projects
                continue
            vistos.add(clave)
            dias = (c["fecha"] - hoy).days
            if dias <= a.dias:
                avisos.append((dias, c))
    if not avisos:
        return
    avisos.sort(key=lambda x: x[0])
    out = [f"💸 Cobros · {corto(hoy)}"]
    for dias, c in avisos:
        if dias < 0:
            cuando = f"VENCIDO hace {-dias} día{'s' if dias != -1 else ''}"
        elif dias == 0:
            cuando = "VENCE HOY"
        else:
            cuando = f"vence en {dias} día{'s' if dias != 1 else ''}"
        out.append(f"\n• {cuando} ({corto(c['fecha'])}) · {c['monto'] or 'monto sin registrar'}\n  {c['nota']}"
                   + (f"\n  Cubre: {c['cubre']}" if c["cubre"] else ""))
        periodo = f" del periodo {c['cubre']}" if c["cubre"] else ""
        out.append(f"  Texto listo: «Hola, te recuerdo que la cuota{periodo} por {c['monto'] or '[monto]'} "
                   f"vence el {corto(c['fecha'])}. Quedo atento. ¡Gracias!»")
    out.append("\nCuando entre el pago, marca la fila como «Pagado» y este aviso se apaga.")
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
