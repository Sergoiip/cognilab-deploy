"""Pruebas sin red: solo fixtures sintéticos, no datos de clientes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).with_name('exportar.py')

class ExportTests(unittest.TestCase):
    def test_exporta_skill_unica_con_estado_y_hash(self):
        self.assertTrue(SCRIPT.exists(), 'Falta implementar exportador')
        spec = importlib.util.spec_from_file_location('exporter', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'Fuentes'
            ref = root / 'Paquete'
            skill = 'dual-node-agent-operations'
            body = '---\nname: dual-node-agent-operations\ndescription: Use when deploying an agent across two computers.\nversion: 0.1.0\n---\n\n# Patrón\n\nOrigen: método generalizado.\n'
            for directory in [source / skill, ref / 'Skills replicables' / skill]:
                directory.mkdir(parents=True)
                (directory / 'SKILL.md').write_text(body)
            (source / 'Registro.json').write_text(json.dumps({'skills':{skill:{'creator':'agent-created-this-task','source':skill+'/SKILL.md'}}}))
            tool = ref / 'Herramientas/ejemplo.py'
            tool.parent.mkdir()
            tool.write_text('print(1)\n')
            kwargs = dict(reference=ref, sources=source, state=root/'estado.json', inventory=root/'inventario.json', output=root/'salida.zip', approve=True)
            report = mod.export(**kwargs)
            self.assertEqual(report['skills_instalables'], 1)
            self.assertEqual(report['pendientes'], [])
            self.assertIn('Herramientas/ejemplo.py', report['herramientas']['nuevas'])
            expected = hashlib.sha256(body.encode()).hexdigest()[:12]
            self.assertEqual(json.loads(kwargs['state'].read_text())[skill], expected)
            with zipfile.ZipFile(kwargs['output']) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(sum(n.endswith('/SKILL.md') for n in z.namelist()),1)
                manifest = json.loads(z.read('Manifiesto.json'))
                for item in manifest['archivos']:
                    self.assertEqual(hashlib.sha256(z.read(item['ruta'])).hexdigest(),item['sha256'])
            tool.write_text('print(2)\n')
            second = mod.export(**kwargs)
            self.assertEqual(second['herramientas']['modificadas'], ['Herramientas/ejemplo.py'])

    def test_auditoria_bloquea_identidad_y_omite_configuracion(self):
        spec = importlib.util.spec_from_file_location('exporter', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref, source = root/'Paquete', root/'Fuentes'
            name = 'dual-node-agent-operations'
            body = '---\nname: dual-node-agent-operations\ndescription: Use when deploying an agent across two computers.\nversion: 0.1.0\n---\n\n# Patrón\n\nOrigen: método generalizado.\n'
            for parent in [ref/'Skills replicables'/name, source/name]:
                parent.mkdir(parents=True)
                (parent/'SKILL.md').write_text(body)
            (source/'Registro.json').write_text(json.dumps({'skills':{name:{'creator':'agent-created-this-task','source':name+'/SKILL.md'}}}))
            bad = ref/'Métodos/nota.md'
            bad.parent.mkdir()
            bad.write_text('/'+'home/'+'sample/private')
            args = dict(reference=ref,sources=source,state=root/'estado.json',inventory=root/'inventario.json',output=root/'salida.zip',approve=True)
            with self.assertRaisesRegex(ValueError,'Auditoría'):
                mod.export(**args)
            self.assertFalse(args['state'].exists())
            bad.write_text('Método genérico.')
            (ref/'.env').write_text('NO_EXPORTAR=fixture')
            (ref/'data.json').write_text('{}')
            report = mod.export(**args)
            self.assertEqual(len(report['omitidos']),2)
            with zipfile.ZipFile(args['output']) as z:
                self.assertNotIn('.env', z.namelist())
                self.assertNotIn('data.json', z.namelist())
            (ref/'enlace.md').symlink_to(bad)
            with self.assertRaisesRegex(ValueError,'simbólico'):
                mod.export(**args)

    def test_fuente_aprendida_y_frontmatter_citado(self):
        spec = importlib.util.spec_from_file_location('exporter', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref, source = root/'Paquete', root/'Fuentes'
            name = 'generic-local-learning'
            body = '---\nname: generic-local-learning\ndescription: "Use when applying reviewed local learning."\nversion: 0.1.0\n---\n\n# Método\n\nOrigen: aprendizaje generalizado.\n'
            for parent in [ref/'Skills replicables'/name, source/name]:
                parent.mkdir(parents=True)
                (parent/'SKILL.md').write_text(body)
            (source/'Registro.json').write_text(json.dumps({'skills':{name:{'creator':'learn','source':name+'/SKILL.md'}}}))
            args = dict(reference=ref,sources=source,state=root/'estado.json',inventory=root/'inventario.json',output=root/'salida.zip',approve=True)
            report = mod.export(**args)
            self.assertEqual(report['skills_instalables'],1)

    def test_cobertura_se_calcula_sin_incluir_rutas_privadas(self):
        spec = importlib.util.spec_from_file_location('exporter', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref, source = root/'Paquete', root/'Fuentes'
            name = 'generic-local-learning'
            body = '---\nname: generic-local-learning\ndescription: Use when applying reviewed local learning.\nversion: 0.1.0\n---\n\n# Método\n\nOrigen: aprendizaje generalizado.\n'
            for parent in [ref/'Skills replicables'/name, source/name]:
                parent.mkdir(parents=True)
                (parent/'SKILL.md').write_text(body)
            (source/'Registro.json').write_text(json.dumps({'skills':{name:{'creator':'learn','source':name+'/SKILL.md'}}}))
            coverage = root/'cobertura.json'
            coverage.write_text(json.dumps({'skills':[{'name':name,'classification':'own','status':'abstracted','output':name},{'name':'unknown','classification':'third-party-or-unconfirmed','status':'excluded'}], 'tools':[{'id':'tool-001','decision':'excluded','review':'metadata-only'}]}))
            report = mod.export(reference=ref,sources=source,state=root/'estado.json',inventory=root/'inventario.json',output=root/'salida.zip',approve=True,coverage=coverage)
            self.assertEqual(report['cobertura']['skills_inventariadas'],2)
            self.assertEqual(report['cobertura']['herramientas_inventariadas'],1)
            with zipfile.ZipFile(root/'salida.zip') as z:
                details = json.loads(z.read('Referencias/Cobertura de fuentes.json'))
                self.assertEqual(details['totales']['skills_inventariadas'],2)
                self.assertNotIn(str(root),json.dumps(details))

    def test_patron_privado_se_configura_fuera_del_paquete(self):
        spec = importlib.util.spec_from_file_location('exporter', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ref, source = root/'Paquete', root/'Fuentes'
            ref.mkdir(); source.mkdir()
            (source/'Registro.json').write_text('{"skills": {}}')
            (ref/'LEEME.md').write_text('PRIVATE_LABEL')
            pattern = root/'patron.txt'
            pattern.write_text('PRIVATE_LABEL')
            with self.assertRaisesRegex(ValueError,'Auditoría'):
                mod.export(reference=ref,sources=source,state=root/'estado.json',inventory=root/'inventario.json',output=root/'salida.zip',sensitive_pattern=pattern)

if __name__ == '__main__':
    unittest.main(verbosity=2)
