"""Exportador documental. Solo biblioteca estándar; no instala ni migra equipos."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def export(reference, sources, state, inventory, output, approve=False, coverage=None, sensitive_pattern=None):
    reference, sources, state, inventory, output = map(Path, (reference, sources, state, inventory, output))
    registry = load(sources/'Registro.json').get('skills', {})
    old_state = load(state)
    old_tools = load(inventory)
    hashes = {}
    for name, entry in registry.items():
        if entry['creator'] not in {'agent-created-this-task','learn','local-extension-reviewed'}:
            raise ValueError('Fuente no autorizada: '+name)
        text = (sources/entry['source']).read_text(encoding='utf-8').replace('\r\n','\n').replace('\r','\n')
        hashes[name] = digest(text.encode())[:12]
    pending = sorted(name for name, h in hashes.items() if old_state.get(name) != h)
    if pending and not approve:
        raise ValueError('Abstracción pendiente de auditoría y aprobación: '+', '.join(pending))
    entries = {}
    omitted = []
    private = re.compile(r'(?<![A-Za-z0-9:/])/(?:home|Users)/[^\s]+|(?:\d{1,3}\.){3}\d{1,3}|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk-[A-Za-z0-9]{20,}', re.I)
    identities = re.compile(Path(sensitive_pattern).read_text(encoding='utf-8').strip() if sensitive_pattern else r'(?!)', re.I)
    brands = re.compile(r'\b(?:hermes|tailscale|cognilab|obsidian|tasknotes|syncthing|lenovo|mint|cachyos)\b', re.I)
    allowed_dirs = {'Skills replicables','Métodos','Referencias','Herramientas'}
    secret_names = {'.env','auth.json','data.json','config.yaml','connections.json','known_hosts','COBERTURA-EXTENDIDAS.md','COBERTURA-EXTENDIDAS.json'}
    for path in sorted(reference.rglob('*')):
        name = path.relative_to(reference).as_posix()
        if path.is_symlink():
            raise ValueError('Enlace simbólico rechazado: '+name)
        if not path.is_file():
            continue
        if any(part.startswith('.') or part in {'__pycache__','node_modules','vendor','Copias de lectura','Pruebas'} for part in path.relative_to(reference).parts) or path.name in secret_names or path.suffix.lower() in {'.pem','.key','.db','.sqlite','.mp3','.wav','.mp4','.png','.jpg','.zip','.pyc'}:
            omitted.append({'ruta':name,'motivo':'configuración, secreto o material excluido'})
            continue
        if name!='LEEME.md' and name.split('/')[0] not in allowed_dirs:
            raise ValueError('Contenido no autorizado: '+name)
        data = path.read_bytes()
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError('Binario no autorizado: '+name) from exc
        if private.search(text):
            raise ValueError('Auditoría: posible dato sensible en '+name)
        if identities.search(text):
            raise ValueError('Auditoría: identidad de origen en '+name)
        if (name.endswith('/SKILL.md') or name.startswith('Métodos/')) and brands.search(text):
            raise ValueError('Auditoría: marca fuera de implementación de referencia en '+name)
        if name.endswith('/SKILL.md'):
            match = re.match(r'---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\nversion: ([^\n]+)\n---\n',text)
            if not match or match[1]!=path.parent.name or not match[2].strip("\"'").startswith('Use when ') or len(match[2].strip("\"'"))>60 or not text.rstrip().splitlines()[-1].startswith('Origen:'):
                raise ValueError('Formato de skill inválido: '+name)
        entries[name] = data
    coverage_summary = {}
    if coverage is not None:
        raw = load(Path(coverage))
        source_rows = [{key: row[key] for key in ('name','classification','status','output','sha256') if key in row} for row in raw.get('skills',[])]
        tool_rows = [{key: row[key] for key in ('id','decision','review','extension','reason') if key in row} for row in raw.get('tools',[])]
        coverage_summary = {'skills_inventariadas':len(source_rows),'skills_por_clase':dict(Counter(row.get('classification','unknown') for row in source_rows)),'skills_por_estado':dict(Counter(row.get('status','unknown') for row in source_rows)),'herramientas_inventariadas':len(tool_rows),'herramientas_por_decision':dict(Counter(row.get('decision','unknown') for row in tool_rows))}
        generated = json.dumps({'totales':coverage_summary,'skills':source_rows,'tools':tool_rows},ensure_ascii=False,indent=2)+'\n'
        if private.search(generated) or identities.search(generated):
            raise ValueError('Auditoría: dato privado en cobertura')
        entries['Referencias/Cobertura de fuentes.json'] = generated.encode()
    skills = [n for n in entries if n.endswith('/SKILL.md') and n.startswith('Skills replicables/')]
    if {n.split('/')[1] for n in skills} != set(registry):
        raise ValueError('Registro y skills abstractas no coinciden')
    tools = {n:digest(b) for n,b in entries.items() if n.startswith('Herramientas/')}
    changes = {
        'nuevas': sorted(set(tools)-set(old_tools)),
        'modificadas': sorted(n for n in tools if n in old_tools and tools[n]!=old_tools[n]),
        'quitadas': sorted(set(old_tools)-set(tools))}
    manifest = {'generado_utc':datetime.now(timezone.utc).isoformat(), 'archivos':[{'ruta':n,'bytes':len(b),'sha256':digest(b)} for n,b in entries.items()]}
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = output.with_suffix('.zip.part')
    with zipfile.ZipFile(staging,'w',zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items(): z.writestr(name,data)
        z.writestr('Manifiesto.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(staging) as z:
        if z.testzip() is not None or len(z.namelist())!=len(set(z.namelist())):
            raise ValueError('ZIP inconsistente')
        for item in manifest['archivos']:
            if digest(z.read(item['ruta']))!=item['sha256']: raise ValueError('Hash no coincide')
        prefixes = dict(Counter(n.split('/')[0] for n in z.namelist() if n.endswith('/SKILL.md')))
    staging.replace(output)
    save(state, hashes)
    save(inventory, tools)
    return {'zip':output.name,'bytes':output.stat().st_size,'sha256':digest(output.read_bytes()),'archivos':len(entries)+1,'cobertura':coverage_summary,'skills_instalables':len(skills),'skills_por_prefijo':prefixes,'pendientes_antes':pending,'pendientes':[],'herramientas':changes,'omitidos':omitted,'alcance':'aprendizaje local revisado; terceros completos excluidos','entregable_periodo':output.name}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['reference','sources','state','inventory','output']:
        p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--sensitive-pattern',type=Path,help='Regex privada de auditoría, fuera del paquete')
    p.add_argument('--coverage',type=Path,help='Inventario de cobertura sanitizable; opcional')
    p.add_argument('--approve',action='store_true',help='Confirmar revisión humana de abstracción; no omite auditoría')
    args=p.parse_args()
    try:
        print(json.dumps(export(**vars(args)),ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError) as exc:
        p.exit(1,str(exc)+'\n')

if __name__=='__main__':
    main()
