#!/usr/bin/env python3
"""Validación estructural de Canvas JSON; solo lectura, sin plugins ni red."""
import argparse
import json
import math
from pathlib import Path
import sys


def validate(document):
    if not isinstance(document, dict):
        return ['invalid-schema']
    nodes, edges = document.get('nodes'), document.get('edges')
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return ['invalid-schema']
    errors = []
    ids = set()
    edge_ids = set()
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get('id'), str) or not node['id']:
            errors.append('invalid-node')
            continue
        if node['id'] in ids:
            errors.append('duplicate-node-id')
        ids.add(node['id'])
        geometry = [node.get(k) for k in ('x', 'y', 'width', 'height')]
        if (not all(type(v) in (int, float) and math.isfinite(v) for v in geometry)
                or geometry[2] <= 0 or geometry[3] <= 0):
            errors.append('invalid-geometry')
    for edge in edges:
        if not isinstance(edge, dict) or not isinstance(edge.get('id'), str) or not edge['id']:
            errors.append('invalid-edge')
            continue
        if edge['id'] in edge_ids:
            errors.append('duplicate-edge-id')
        edge_ids.add(edge['id'])
        if any(not isinstance(edge.get(k), str) or edge[k] not in ids for k in ('fromNode', 'toNode')):
            errors.append('missing-endpoint')
    if 'invalid-geometry' not in errors and 'invalid-node' not in errors:
        cards = [node for node in nodes if node.get('type') != 'group']
        for i, a in enumerate(cards):
            for b in cards[i + 1:]:
                if (a['x'] < b['x'] + b['width'] and b['x'] < a['x'] + a['width']
                        and a['y'] < b['y'] + b['height'] and b['y'] < a['y'] + a['height']):
                    errors.append('overlapping-cards')
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('canvas', type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.canvas.read_text(encoding='utf-8'))
        errors = validate(document)
    except (OSError, ValueError, TypeError) as exc:
        errors = ['input:' + type(exc).__name__]
    print(json.dumps({'errors': errors, 'native_render': 'not_verified'}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
