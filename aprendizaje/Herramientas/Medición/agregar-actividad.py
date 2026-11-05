"""Agregación offline de intervalos autorizados; no lee títulos ni conecta servicios.

Entrada explícita: windows=[{start,end,...}], active=[[start,end],...], start, end.
Todos los extremos comparten unidad y eje temporal (p. ej. segundos Unix).
Origen: reimplementación portable de un reporte generado en sesión propia,
con eliminación de reglas privadas, consulta de red y dependencia de hora local.
"""
import json
import math
import sys


def aggregate(windows, active, start, end):
    def interval(a, b):
        if any(type(v) not in (int, float) or abs(v) > 1e15 or not math.isfinite(v) for v in (a, b)) or b <= a:
            raise ValueError('invalid numeric interval')
        return a, b
    interval(start, end)
    try:
        if not isinstance(windows, list) or not isinstance(active, list):
            raise ValueError('invalid input arrays')
        checked = [interval(e['start'], e['end']) for e in windows]
        presence = [interval(*pair) for pair in active]
    except (KeyError, TypeError) as exc:
        raise ValueError('invalid interval schema') from None
    spans = sorted((max(start, a), min(end, b)) for a, b in checked
                   if min(end, b) > max(start, a))
    if any(a < previous for (_, previous), (a, _) in zip(spans, spans[1:])):
        raise ValueError('window overlap')
    periods = []
    for a, b in sorted((max(start, a), min(end, b)) for a, b in presence):
        if b <= a:
            continue
        if periods and a <= periods[-1][1]:
            periods[-1] = (periods[-1][0], max(periods[-1][1], b))
        else:
            periods.append((a, b))
    observed = sum(sum(max(0, min(end, event['end'], b) - max(start, event['start'], a))
                       for a, b in periods) for event in windows)
    present = sum(b - a for a, b in periods)
    return {'active_seconds': present, 'active_window_seconds': observed,
            'active_without_window_seconds': present - observed,
            'limitations': ['Intervalos observados; no demuestra productividad ni facturabilidad.',
                            'No identifica proyectos, personas, aplicaciones ni cobertura fuera del periodo.']}


def main():
    from pathlib import Path
    if len(sys.argv) != 2:
        print('Uso: python3 agregar-actividad.py ENTRADA.json', file=sys.stderr)
        return 2
    try:
        with Path(sys.argv[1]).open('rb') as source:
            raw = source.read(10000001)
        if len(raw) > 10000000:
            raise ValueError('input too large')
        data = json.loads(raw)
        report = aggregate(data['windows'], data['active'], data['start'], data['end'])
        print(json.dumps(report, ensure_ascii=False, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, OverflowError, RecursionError):
        print('Entrada inválida, inaccesible, excesiva o intervalos solapados; sin resultado.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
