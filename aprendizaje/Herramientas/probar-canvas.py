"""Pruebas aisladas; no lee bóvedas ni inicia aplicaciones."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).with_name('validar-canvas.py')

class CanvasTests(unittest.TestCase):
    def run_tool(self, canvas):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'ejemplo.canvas'
            before = json.dumps(canvas).encode()
            path.write_bytes(before)
            result = subprocess.run([sys.executable, str(TOOL), str(path)], capture_output=True, text=True)
            self.assertEqual(path.read_bytes(), before)
            return result

    def test_valid_empty_document_is_read_only(self):
        result = self.run_tool({'nodes': [], 'edges': []})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['errors'], [])

    def test_rejects_duplicate_ids_missing_endpoints_and_bad_geometry(self):
        nodes = [{'id': 'a', 'type': 'text', 'x': 0, 'y': 0, 'width': 20, 'height': 20},
                 {'id': 'a', 'type': 'text', 'x': 0, 'y': 0, 'width': 0, 'height': 20}]
        result = self.run_tool({'nodes': nodes, 'edges': [{'id': 'e', 'fromNode': 'a', 'toNode': 'missing'}]})
        self.assertEqual(result.returncode, 1)
        errors = json.loads(result.stdout)['errors']
        self.assertIn('duplicate-node-id', errors)
        self.assertIn('missing-endpoint', errors)
        self.assertIn('invalid-geometry', errors)

    def test_overlapping_cards_fail_but_group_containment_passes(self):
        card = {'id': 'a', 'type': 'text', 'x': 0, 'y': 0, 'width': 20, 'height': 20}
        other = dict(card, id='b', x=10)
        result = self.run_tool({'nodes': [card, other], 'edges': []})
        self.assertEqual(result.returncode, 1)
        self.assertIn('overlapping-cards', json.loads(result.stdout)['errors'])
        group = dict(card, id='g', type='group', width=100, height=100)
        self.assertEqual(self.run_tool({'nodes': [card, group], 'edges': []}).returncode, 0)

    def test_invalid_schema_and_nonfinite_geometry_fail_without_traceback(self):
        cases = [[], {}, {'nodes': [None], 'edges': []},
                 {'nodes': [{'id': 'a', 'x': float('nan'), 'y': 0, 'width': 2, 'height': 2}], 'edges': []}]
        for case in cases:
            with self.subTest(case=case):
                result = self.run_tool(case)
                self.assertEqual(result.returncode, 1)
                self.assertTrue(json.loads(result.stdout)['errors'])
                self.assertNotIn('Traceback', result.stderr)

if __name__ == '__main__':
    unittest.main()
