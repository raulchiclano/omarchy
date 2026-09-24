#!/usr/bin/env python3
"""Omarchy Lavanda: explicit plan, transactional backup, conservative restore."""
import argparse
import copy
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / 'payload'
STATE = '.local/state/omarchy-lavanda'
CONFIG = '.config/omarchy-lavanda'
COMPONENTS = {'desktop', 'terminal', 'shell', 'icons', 'workspaces'}
DEFAULT = 'desktop,terminal,shell,icons'
SERVICES = ('osd', 'notifications', 'menu')


class Problem(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def target(home, name):
    """Reject symlinks (including ancestor links), special files and path traversal."""
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise Problem(f'Ruta no válida: {name}')
    current = home
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise Problem(f'No se sobrescriben enlaces simbólicos: {current}')
        if current.exists() and not (current.is_file() or current.is_dir()):
            raise Problem(f'No es un archivo normal: {current}')
    return current


def read(home, name, default=b''):
    p = target(home, name)
    if p.exists() and not p.is_file():
        raise Problem(f'Se esperaba un archivo: {p}')
    return p.read_bytes() if p.exists() else default


def managed(text, label, body, comment='#'):
    begin, end = f'{comment} BEGIN OMARCHY LAVANDA {label}', f'{comment} END OMARCHY LAVANDA {label}'
    block = f'{begin}\n{body.rstrip()}\n{end}'
    if begin in text or end in text:
        if text.count(begin) != 1 or text.count(end) != 1:
            raise Problem(f'Bloque {label} incompleto o repetido; no se modifica.')
        return re.sub(re.escape(begin) + r'.*?' + re.escape(end), lambda _: block, text, flags=re.S)
    return text.rstrip() + '\n\n' + block + '\n'


def merge_foot(text):
    """Edit only owned INI keys, preserving comments and unrelated settings."""
    settings = {
        'main': {'font': 'JetBrainsMono Nerd Font:size=10', 'pad': '14x14'},
        'scrollback': {'lines': '10000', 'multiplier': '7.0'},
        'cursor': {'style': 'beam', 'beam-thickness': '2px', 'blink': 'no'},
        'colors-dark': {'alpha': '0.94'},
    }
    if not text.strip():
        text = '[main]\ninclude=~/.local/state/omarchy/current/theme/foot.ini\nterm=xterm-256color\n'
    for section, keys in settings.items():
        for key, value in keys.items():
            lines = text.splitlines(keepends=True)
            headers = [(i, re.fullmatch(r'\s*\[([^]]+)\]\s*', line.strip())) for i, line in enumerate(lines)]
            starts = [i for i, m in headers if m and m[1] == section]
            if len(starts) > 1:
                raise Problem(f'Foot tiene una sección duplicada: {section}')
            if not starts:
                text = text.rstrip() + f'\n\n[{section}]\n{key}={value}\n'
                continue
            start = starts[0]
            end = next((i for i, m in headers if m and i > start), len(lines))
            matches = [i for i in range(start + 1, end) if re.match(r'\s*' + re.escape(key) + r'\s*=', lines[i])]
            if len(matches) > 1:
                raise Problem(f'Foot tiene una clave duplicada: {section}.{key}')
            if matches:
                lines[matches[0]] = f'{key}={value}\n'
            else:
                if end and not lines[end - 1].endswith('\n'):
                    lines[end - 1] += '\n'
                lines.insert(end, f'{key}={value}\n')
            text = ''.join(lines)
    return text


def merge_bar(data, stock):
    """Use our layout; keep non-stock widgets, service options and unrelated keys."""
    if not isinstance(data, dict) or not isinstance(data.get('bar', {}), dict):
        raise Problem('shell.json debe ser un objeto con configuración bar válida.')
    if not isinstance(data.get('plugins', []), list) or any(not isinstance(x, dict) for x in data.get('plugins', [])):
        raise Problem('La lista de plugins de shell.json tiene un formato desconocido.')
    data = copy.deepcopy(data)
    bar = json.loads((PAYLOAD / 'bar.json').read_text())
    old_bar = data.get('bar', {})
    native = {'omarchy.' + n for n in ('menu', 'workspaces', 'clock', 'weather', 'indicators',
              'keyboard-layout', 'system-update', 'tray', 'agents', 'bluetooth', 'network', 'audio', 'monitor', 'power')}
    owned = {'lavanda.' + p.name.split('.', 1)[1] for p in (PAYLOAD / 'plugins').iterdir()}
    previous = {x.replace('lavanda.', 'raulchiclano.') for x in owned}
    for section in ('left', 'center', 'right'):
        for entry in old_bar.get('layout', stock['bar']['layout']).get(section, []):
            if not isinstance(entry, dict) or not isinstance(entry.get('id'), str):
                raise Problem('Formato de widget desconocido; revisar shell.json.')
            name = entry['id']
            if name not in native | owned | previous:
                bar['layout'][section].append(entry)
            else:
                # Keep e.g. network widget options, but use our compact clock format.
                mapped = name.replace('omarchy.', 'lavanda.').replace('raulchiclano.', 'lavanda.')
                for widgets in bar['layout'].values():
                    for item in widgets:
                        if item['id'] in (name, mapped):
                            item.update({k: v for k, v in entry.items() if k not in ('id', 'format')})
    data['bar'] = {**old_bar, **bar}
    data.setdefault('version', 1)
    service_names = {prefix + n for prefix in ('omarchy.', 'raulchiclano.', 'lavanda.') for n in SERVICES}
    options = {entry['id'].split('.', 1)[1]: entry for entry in data.get('plugins', [])
               if entry.get('id') in service_names}
    data['plugins'] = [x for x in data.get('plugins', []) if x.get('id') not in service_names]
    data['plugins'] += [{**options.get(n, {}), 'id': 'lavanda.' + n} for n in SERVICES]
    # On an existing personalized source machine, disable old clones too (IPC collisions).
    disabled = [x for x in data.get('disabledPlugins', []) if x not in owned]
    for n in SERVICES:
        for prefix in ('omarchy.', 'raulchiclano.'):
            if prefix + n not in disabled:
                disabled.append(prefix + n)
    data['disabledPlugins'] = disabled
    restores = [x for x in data.get('cloneSourceRestores', []) if x not in previous]
    data['cloneSourceRestores'] = list(dict.fromkeys(restores + ['lavanda.' + n for n in SERVICES]))
    return data


def merge_bash(text):
    # Migrate only the exact earlier integration from this project, never arbitrary shell code.
    previous = '''# ble.sh is enabled only for interactive terminal sessions.
if [[ -t 0 && -t 1 && ${TERM:-dumb} != dumb && -r /usr/share/blesh/ble.sh ]]; then
  source "$HOME/.config/bash/omarchy-blesh.sh"
else
  source "$OMARCHY_PATH/default/bash/rc"
fi'''
    if previous in text:
        text = text.replace(previous, 'source "$OMARCHY_PATH/default/bash/rc"', 1)
        text = text.replace('# Lavender history picker (Ctrl+R).\nsource "$HOME/.config/bash/fzf-history.sh"\n', '')
        text = text.replace('# Attach after the prompt, shortcuts and user settings are ready.\n[[ ! ${BLE_VERSION-} ]] || ble-attach\n', '')
    init = '''export STARSHIP_CONFIG="$HOME/.config/omarchy-lavanda/starship.toml"
if [[ -t 0 && -t 1 && ${TERM:-dumb} != dumb && -r /usr/share/blesh/ble.sh ]]; then
  source "$HOME/.config/omarchy-lavanda/bash/omarchy-blesh.sh"
else
  source "$OMARCHY_PATH/default/bash/rc"
fi'''
    if '# BEGIN OMARCHY LAVANDA INIT' not in text:
        pattern = r'^source "\$OMARCHY_PATH/default/bash/rc"\s*$'
        if len(re.findall(pattern, text, re.M)) != 1:
            raise Problem('Bash: no se encuentra una única carga estándar de Omarchy. Consulta docs/compatibilidad.md.')
        if re.search(r'^[^#\n]*(?:ble\.sh|ble-attach|STARSHIP_CONFIG)', text, re.M):
            raise Problem('Bash ya tiene otra integración de ble.sh/Starship; requiere revisión manual.')
        text = re.sub(pattern, '# BEGIN OMARCHY LAVANDA INIT\n' + init + '\n# END OMARCHY LAVANDA INIT', text, count=1, flags=re.M)
    else:
        text = managed(text, 'INIT', init)
    return managed(text, 'FINISH', '''source "$HOME/.config/omarchy-lavanda/bash/fzf-history.sh"
[[ ! ${BLE_VERSION-} ]] || ble-attach''')


def check_compatibility(parts, base):
    meta = json.loads((ROOT / 'compatibility.json').read_text())
    groups = set()
    if parts & {'desktop', 'workspaces'}:
        groups.add('desktop')
    if 'shell' in parts:
        groups.add('shell')
    failures = []
    for group in sorted(groups):
        changed = [name for name, expected in meta[group].items()
                   if not (base / name).is_file() or digest((base / name).read_bytes()) != expected]
        if changed:
            failures.append(f'{group}: {len(changed)} archivos distintos/ausentes ({", ".join(changed[:3])})')
    if failures:
        raise Problem('Base no validada para estos componentes. No se ha escrito nada.\n' + '\n'.join(failures) +
                      '\nConsulta docs/compatibilidad.md; no se fuerza la instalación.')


def plan(home, parts, base):
    check_compatibility(parts, base)
    files = {}
    def put(name, data):
        files[name] = data.encode() if isinstance(data, str) else data
    if 'desktop' in parts:
        main = read(home, '.config/hypr/hyprland.lua').decode()
        if 'require("hypr.looknfeel")' not in main:
            raise Problem('Hyprland: se necesita la configuración Lua de Omarchy que carga hypr.looknfeel.')
        for p in sorted((PAYLOAD / 'plugins').rglob('*')):
            if p.is_file():
                put('.config/omarchy/plugins/' + str(p.relative_to(PAYLOAD / 'plugins')), p.read_bytes())
        put(CONFIG + '/looknfeel.lua', (PAYLOAD / 'looknfeel.lua').read_bytes())
        name = '.config/hypr/looknfeel.lua'
        put(name, managed(read(home, name).decode(), 'LOOK',
                         'dofile(os.getenv("HOME") .. "/.config/omarchy-lavanda/looknfeel.lua")', '--'))
        # Commit shell.json last, after all plugin payloads are present.
        name = '.config/omarchy/shell.json'
        stock = json.loads((base / 'config/omarchy/shell.json').read_text())
        data = json.loads(read(home, name, json_bytes(stock)))
        put(name, json_bytes(merge_bar(data, stock)))
    if 'terminal' in parts:
        name = '.config/foot/foot.ini'
        put(name, merge_foot(read(home, name).decode()))
    if 'shell' in parts:
        for p in sorted((PAYLOAD / 'bash').glob('*.sh')):
            put(CONFIG + '/bash/' + p.name, p.read_bytes())
        put(CONFIG + '/starship.toml', (PAYLOAD / 'starship.toml').read_bytes())
        put('.bashrc', merge_bash(read(home, '.bashrc').decode()))
    if 'icons' in parts:
        if not (base / 'themes/tokyo-night').is_dir():
            raise Problem('No existe el tema Tokyo Night en esta instalación.')
        put('.config/omarchy/themes/tokyo-night/icons.theme', 'Adwaita\n')
    if 'workspaces' in parts:
        main = read(home, '.config/hypr/hyprland.lua').decode()
        if 'require("hypr.bindings")' not in main:
            raise Problem('Hyprland no carga hypr.bindings.')
        put(CONFIG + '/workspace-bindings.lua', (PAYLOAD / 'workspace-bindings.lua').read_bytes())
        name = '.config/hypr/bindings.lua'
        put(name, managed(read(home, name).decode(), 'WORKSPACES',
                         'dofile(os.getenv("HOME") .. "/.config/omarchy-lavanda/workspace-bindings.lua")', '--'))
    # Snapshot both content and mode so the apply step can detect intervening edits.
    result = []
    for name, after in files.items():
        before = read(home, name, None)
        if before != after:
            p = target(home, name)
            mode = stat.S_IMODE(p.stat().st_mode) if p.exists() else 0o644
            result.append({'path': name, 'before': before, 'after': after, 'mode': mode})
    result.sort(key=lambda e: e['path'] == '.config/omarchy/shell.json')
    return result


def show(changes, detailed=False):
    if not changes:
        print('Todo está al día; no hay cambios.')
        return
    for item in changes:
        action = 'CREAR' if item['before'] is None else ('BORRAR' if item['after'] is None else 'EDITAR')
        print(f'  {action:7} ~/{item["path"]}')
        if detailed:
            print(''.join(difflib.unified_diff((item['before'] or b'').decode().splitlines(True),
                  (item['after'] or b'').decode().splitlines(True),
                  fromfile='antes/' + item['path'], tofile='después/' + item['path'])), end='')
    print(f'\n{len(changes)} archivos. Monitores, red, claves, sesiones e historial no se copian.')


def atomic_write(path, data, mode=0o644):
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.lavanda-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def transaction(home, changes, operation='apply'):
    if not changes:
        return None
    # All path and content checks happen before creating the backup or writing config.
    for item in changes:
        if read(home, item['path'], None) != item['before']:
            raise Problem(f'Ha cambiado durante la revisión: {item["path"]}. Repite el plan.')
    state = target(home, STATE)
    state.mkdir(parents=True, exist_ok=True)
    lock_path = target(home, STATE + '/install.lock')
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for item in changes:
            if read(home, item['path'], None) != item['before']:
                raise Problem('Otro proceso ha cambiado la configuración. Repite el plan.')
        identifier = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        backup = target(home, f'{STATE}/backups/{identifier}')
        backup.mkdir(parents=True, mode=0o700)
        metadata = {'version': 1, 'operation': operation, 'status': 'prepared', 'files': []}
        for index, item in enumerate(changes):
            if item['before'] is not None:
                atomic_write(backup / str(index), item['before'], 0o600)
            metadata['files'].append({'path': item['path'], 'saved': str(index) if item['before'] is not None else None,
                                      'before_hash': digest(item['before']) if item['before'] is not None else None,
                                      'after_hash': digest(item['after']) if item['after'] is not None else None,
                                      'mode': item['mode']})
        atomic_write(backup / 'manifest.json', json_bytes(metadata), 0o600)
        done = []
        try:
            for item in changes:
                atomic_write(target(home, item['path']), item['after'], item['mode'])
                done.append(item)
        except BaseException:
            for item in reversed(done):
                atomic_write(target(home, item['path']), item['before'], item['mode'])
            metadata['status'] = 'rolled-back'
            atomic_write(backup / 'manifest.json', json_bytes(metadata), 0o600)
            raise
        metadata['status'] = 'complete'
        atomic_write(backup / 'manifest.json', json_bytes(metadata), 0o600)
        return identifier


def restore_plan(home, identifier):
    if not re.fullmatch(r'\d{8}T\d{6}\.\d{6}Z', identifier):
        raise Problem('Indica el identificador de una copia mostrado por «backups».')
    backup = target(home, f'{STATE}/backups/{identifier}')
    metadata = json.loads(read(home, f'{STATE}/backups/{identifier}/manifest.json'))
    if metadata.get('status') not in ('complete', 'prepared'):
        raise Problem('Esta copia ya fue revertida durante un error.')
    changes = []
    for item in reversed(metadata['files']):
        current = read(home, item['path'], None)
        before_hash = digest(current) if current is not None else None
        saved = item['saved']
        if saved is not None and not re.fullmatch(r'\d+', saved):
            raise Problem('Copia no válida.')
        original = read(home, f'{STATE}/backups/{identifier}/{saved}') if saved is not None else None
        if (digest(original) if original is not None else None) != item['before_hash']:
            raise Problem(f'Copia dañada: {item["path"]}')
        if current == original:
            continue
        if before_hash != item['after_hash']:
            raise Problem(f'Se ha editado después de instalar: {item["path"]}.\n'
                          'No se borran tus cambios: compara con la copia y restaura manualmente ese archivo.')
        changes.append({'path': item['path'], 'before': current, 'after': original, 'mode': item['mode']})
    return changes


def dependencies(parts):
    required = set()
    if 'desktop' in parts:
        required.update(['omarchy-shell', 'hyprctl', 'jq', 'timeout', 'fc-match'])
    if 'terminal' in parts:
        required.update(['foot', 'fc-match'])
    if 'shell' in parts:
        required.update(['bash', 'starship', 'fzf', 'sed'])
    missing = [name for name in sorted(required) if not shutil.which(name)]
    if missing:
        raise Problem('Faltan dependencias: ' + ', '.join(missing) + '. Consulta README.md.')
    if 'shell' in parts:
        version = subprocess.check_output(['fzf', '--version'], text=True).split()[0]
        if tuple(map(int, version.split('.')[:3])) < (0, 74, 4):
            raise Problem('El historial se validó con fzf >= 0.74.4. Instala una versión compatible.')
        if not Path('/usr/share/blesh/ble.sh').exists():
            print('AVISO: ble.sh no está instalado; Bash funcionará sin sus sugerencias.')
    fonts = []
    if 'desktop' in parts:
        fonts.append('Adwaita Sans')
    if parts & {'desktop', 'terminal'}:
        fonts.append('JetBrainsMono Nerd Font')
    for font in fonts:
        found = subprocess.check_output(['fc-match', '-f', '%{family}', font], text=True)
        if font not in found:
            raise Problem(f'Falta la fuente {font}; se encontró {found}. Consulta README.md.')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Omarchy Lavanda — revisar, instalar y restaurar sin sudo.')
    parser.add_argument('action', nargs='?', choices=['plan', 'apply', 'doctor', 'backups', 'restore'], default='plan')
    parser.add_argument('backup', nargs='?', help='Identificador para restore')
    parser.add_argument('--only', default=DEFAULT, help='desktop,terminal,shell,icons,workspaces (este último opcional)')
    parser.add_argument('--diff', action='store_true', help='Mostrar el contenido de cada cambio')
    parser.add_argument('--yes', action='store_true', help='Aplicar sin la pregunta final')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Otro HOME, para preparar y probar sin recargar la sesión')
    args = parser.parse_args(argv)
    if os.geteuid() == 0:
        raise Problem('Ejecuta como tu usuario habitual, sin sudo.')
    home = args.home.expanduser().absolute()
    if home.is_symlink() or not home.is_dir():
        raise Problem('HOME debe ser un directorio existente y no un enlace.')
    # Reject alternate XDG roots rather than accidentally writing inactive files.
    if home == Path.home():
        for key, expected in [('XDG_CONFIG_HOME', home / '.config'), ('XDG_STATE_HOME', home / '.local/state')]:
            if os.environ.get(key) and Path(os.environ[key]) != expected:
                raise Problem(f'{key} personalizado: esta edición usa las rutas estándar de Omarchy.')
    base = Path('/usr/share/omarchy')
    if args.action not in ('backups', 'restore') and os.environ.get('OMARCHY_PATH', str(base)) != str(base):
        raise Problem('Esta edición requiere Omarchy en /usr/share/omarchy; no es para dev link.')
    if args.action == 'backups':
        directory = target(home, STATE + '/backups')
        for entry in sorted(directory.glob('*/manifest.json')) if directory.exists() else []:
            record = json.loads(entry.read_text())
            print(f'{entry.parent.name}  {record["operation"]}  {record["status"]}')
        return
    if args.action == 'restore':
        if not args.backup:
            raise Problem('Usa: ./install.sh restore ID; obtén ID con ./install.sh backups.')
        changes = restore_plan(home, args.backup)
    else:
        parts = set(args.only.split(','))
        if not parts or not parts <= COMPONENTS:
            raise Problem('Componentes válidos: ' + ','.join(sorted(COMPONENTS)))
        dependencies(parts)
        changes = plan(home, parts, base)
        if args.action == 'doctor':
            print('Dependencias, formato y base compatibles con esta edición. No se ha escrito nada.')
            print('La prueba visual en la máquina de destino se realiza después de instalar.')
            return
    show(changes, args.diff)
    if args.action not in ('apply', 'restore') or not changes:
        return
    if not args.yes:
        if not sys.stdin.isatty():
            raise Problem('Sin terminal interactivo: revisa el plan y usa --yes para aplicar.')
        if input('¿Aplicar estos cambios y guardar una copia? [s/N] ').strip().lower() not in ('s', 'si', 'sí'):
            print('Cancelado. No se ha escrito nada.')
            return
    identifier = transaction(home, changes, args.action)
    print(f'\nHecho. Copia local: {identifier}\nDeshacer: ./install.sh restore {identifier}')
    print('Los paneles se recargan al guardar; abre una terminal nueva para probar Bash/Foot.')
    if any(x['path'].startswith('.config/hypr/') for x in changes) and home == Path.home():
        if os.environ.get('HYPRLAND_INSTANCE_SIGNATURE'):
            subprocess.run(['hyprctl', 'reload'], check=True)
            result = subprocess.run(['hyprctl', 'configerrors'], capture_output=True, text=True, check=True)
            if result.stdout.strip() and result.stdout.strip().lower() != 'ok':
                print('Revisa Hyprland; conserva la copia para deshacer:\n' + result.stdout)
                return 1
        else:
            print('Sin sesión Hyprland activa: al entrar, comprueba «hyprctl configerrors».')
    if any(x['path'].endswith('icons.theme') for x in changes):
        print('Adwaita se aplicará al elegir Tokyo Night: omarchy theme set tokyo-night')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main() or 0)
    except (Problem, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
