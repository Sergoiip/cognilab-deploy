"""Fixtures sintéticos; sin telemetría, red ni acceso al entorno operativo."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).with_name('agregar-actividad.py')

class ActivityTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.is_file(), 'Falta implementar agregador portable')
        spec = importlib.util.spec_from_file_location('activity', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_intersection_clips_and_preserves_private_fields(self):
        module = self.load()
        events = [{'start': -10, 'end': 8, 'app': 'editor', 'title': 'PRIVATE_SENTINEL'},
                  {'start': 8, 'end': 30, 'url': 'PRIVATE_SENTINEL'}]
        report = module.aggregate(events, [[0, 5], [4, 10]], 0, 20)
        self.assertEqual(report['active_seconds'], 10)
        self.assertEqual(report['active_window_seconds'], 10)
        self.assertEqual(report['active_without_window_seconds'], 0)
        self.assertNotIn('PRIVATE_SENTINEL', str(report))
        self.assertNotIn('editor', str(report))
        self.assertEqual(events[0]['start'], -10)

    def test_overlapping_windows_are_rejected_before_summing(self):
        module = self.load()
        with self.assertRaisesRegex(ValueError, 'overlap'):
            module.aggregate([{'start': 0, 'end': 8}, {'start': 7, 'end': 9}], [[0, 10]], 0, 10)
        self.assertEqual(module.aggregate([{'start': 0, 'end': 5}, {'start': 5, 'end': 10}], [[0, 10]], 0, 10)['active_window_seconds'], 10)

    def test_malformed_or_nonfinite_intervals_fail_closed(self):
        module = self.load()
        for start, end in [(True, 10), (0, float('inf')), (float('nan'), 10), (5, 5), (10, 1)]:
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                module.aggregate([], [], start, end)
        for windows, active in [([{'start': 5, 'end': 4}], []),
                                ([{'start': 'PRIVATE_SENTINEL', 'end': 4}], []),
                                ([{}], []), ([], [[0, float('nan')]]),
                                ([], [[0, 1, 2]]), ([], [[False, 2]])]:
            with self.subTest(windows=windows, active=active), self.assertRaises(ValueError):
                module.aggregate(windows, active, 0, 10)
        empty = module.aggregate([], [], 0, 10)
        self.assertEqual(empty['active_window_seconds'], 0)
        gaps = module.aggregate([{'start': 1, 'end': 3}], [[0, 5], [8, 10]], 0, 10)
        self.assertEqual(gaps['active_without_window_seconds'], 5)

    def test_cli_uses_only_explicit_input_and_sanitizes_errors(self):
        self.load()
        import json
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'synthetic.json'
            raw = json.dumps({'windows': [{'start': 2, 'end': 5, 'title': 'PRIVATE_SENTINEL'}],
                              'active': [[0, 8]], 'start': 0, 'end': 10}).encode()
            source.write_bytes(raw)
            result = subprocess.run(['python3', '-B', str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn('active_seconds', result.stdout, 'Falta CLI JSON')
            self.assertEqual(json.loads(result.stdout)['active_window_seconds'], 3)
            self.assertEqual(source.read_bytes(), raw)
            source.write_text('{"windows":"PRIVATE_SENTINEL"}')
            result = subprocess.run(['python3', '-B', str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('PRIVATE_SENTINEL', result.stderr)
            self.assertNotIn(str(source), result.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
