import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import shutil
import os

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'installer.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def supported_fzf():
    if not shutil.which('fzf'):
        return False
    version = subprocess.check_output(['fzf', '--version'], text=True).split()[0]
    return tuple(map(int, version.split('.')[:3])) >= (0, 74, 4)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'home'
        self.home.mkdir()
        self.base = Path(self.tmp.name) / 'omarchy'
        (self.base / 'themes/tokyo-night').mkdir(parents=True)
        (self.base / 'config/omarchy').mkdir(parents=True)
        self.stock = {'version': 1, 'bar': {'layout': {'left': [{'id': 'omarchy.menu'}],
                      'center': [{'id': 'omarchy.clock'}], 'right': []}}, 'plugins': []}
        (self.base / 'config/omarchy/shell.json').write_text(json.dumps(self.stock))
        self.write('.bashrc', '[[ $- != *i* ]] && return\nsource "$OMARCHY_PATH/default/bash/rc"\nalias mine="echo kept"\n')
        self.write('.config/hypr/hyprland.lua', 'require("hypr.looknfeel")\nrequire("hypr.bindings")\n')
        self.write('.config/hypr/monitors.lua', 'DO NOT TOUCH')
        self.write('.ssh/private-sentinel', 'DO NOT TOUCH')
        self.write('.bash_history', 'DO NOT TOUCH')
        self.write('.config/omarchy/shell.json', json.dumps({
            **self.stock, 'idle': {'lock': 888, 'screensaver': 444}, 'future': {'keep': 1},
            'plugins': [{'id': 'someone.service', 'keep': True}],
            'bar': {'height': 42, 'layout': {'left': [{'id': 'someone.widget', 'option': 7}], 'center': [], 'right': []}}
        }))

    def write(self, name, content):
        p = self.home / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def snapshot(self):
        return {str(p.relative_to(self.home)): p.read_bytes() for p in self.home.rglob('*')
                if p.is_file() and not str(p.relative_to(self.home)).startswith(m.STATE)}

    def plan(self, parts=None):
        with patch.object(m, 'check_compatibility'):
            return m.plan(self.home, parts or set(m.DEFAULT.split(',')), self.base)

    def test_plan_is_read_only(self):
        before = self.snapshot()
        self.assertGreater(len(self.plan()), 40)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.home / m.STATE).exists())

    def test_roundtrip_idempotence_and_preservation(self):
        before = self.snapshot()
        changes = self.plan()
        identifier = m.transaction(self.home, changes)
        self.assertEqual(self.plan(), [])
        merged = json.loads((self.home / '.config/omarchy/shell.json').read_text())
        self.assertEqual(merged['idle'], {'lock': 888, 'screensaver': 444})
        self.assertEqual(merged['future'], {'keep': 1})
        self.assertEqual(merged['bar']['height'], 42)
        self.assertIn({'id': 'someone.widget', 'option': 7}, merged['bar']['layout']['left'])
        self.assertIn({'id': 'someone.service', 'keep': True}, merged['plugins'])
        for p in ('.ssh/private-sentinel', '.bash_history', '.config/hypr/monitors.lua'):
            self.assertEqual((self.home / p).read_bytes(), before[p])
        m.transaction(self.home, m.restore_plan(self.home, identifier), 'restore')
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(m.restore_plan(self.home, identifier), [])

    def test_restore_refuses_later_user_edits(self):
        identifier = m.transaction(self.home, self.plan())
        self.write('.bashrc', 'My newer edits')
        before = self.snapshot()
        with self.assertRaisesRegex(m.Problem, 'editado después'):
            m.restore_plan(self.home, identifier)
        self.assertEqual(self.snapshot(), before)

    def test_partial_write_failure_rolls_back(self):
        before = self.snapshot()
        changes = self.plan()
        real_write = m.atomic_write
        failed = False
        def fail_once(path, data, mode=0o644):
            nonlocal failed
            if str(path).endswith('lavanda.audio/Panel.qml') and not failed:
                failed = True
                raise OSError('simulated disk error')
            return real_write(path, data, mode)
        with patch.object(m, 'atomic_write', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'simulated'):
                m.transaction(self.home, changes)
        self.assertTrue(failed)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_and_path_traversal_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        (self.home / '.config/foot').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(m.Problem, 'enlaces'):
            self.plan({'terminal'})
        with self.assertRaises(m.Problem):
            m.target(self.home, '../outside/secret')
        self.assertFalse(list(outside.iterdir()))

    def test_intervening_change_refused_before_backup(self):
        changes = self.plan()
        self.write('.bashrc', 'new')
        with self.assertRaisesRegex(m.Problem, 'durante la revisión'):
            m.transaction(self.home, changes)
        self.assertFalse((self.home / m.STATE).exists())

    def test_unknown_runtime_rejected_without_writes(self):
        before = self.snapshot()
        with self.assertRaisesRegex(m.Problem, 'Base no validada'):
            m.plan(self.home, {'desktop'}, self.base)
        self.assertEqual(before, self.snapshot())

    def test_unknown_bash_integration_rejected(self):
        self.write('.bashrc', 'source ~/.my-custom-init')
        with self.assertRaisesRegex(m.Problem, 'carga estándar'):
            self.plan({'shell'})

    def test_foot_preserves_unowned_keys_and_comments(self):
        old = '# header\n[main]\nfont=old\npad=1x1\nworkers=3\n[key-bindings]\ncustom=keep\n'
        self.write('.config/foot/foot.ini', old)
        changes = self.plan({'terminal'})
        new = changes[0]['after'].decode()
        self.assertIn('workers=3', new)
        self.assertIn('custom=keep', new)
        self.assertTrue(new.startswith('# header'))
        self.assertEqual(m.merge_foot(new), new)

    def test_duplicate_foot_key_rejected(self):
        self.write('.config/foot/foot.ini', '[main]\nfont=a\nfont=b\n')
        with self.assertRaisesRegex(m.Problem, 'duplicada'):
            self.plan({'terminal'})

    def test_original_file_mode_and_private_backup(self):
        (self.home / '.bashrc').chmod(0o600)
        identifier = m.transaction(self.home, self.plan({'shell'}))
        self.assertEqual((self.home / '.bashrc').stat().st_mode & 0o777, 0o600)
        backup = self.home / m.STATE / 'backups' / identifier
        self.assertEqual(backup.stat().st_mode & 0o777, 0o700)
        for p in backup.iterdir():
            self.assertEqual(p.stat().st_mode & 0o777, 0o600)

    def test_restore_detects_damaged_backup(self):
        identifier = m.transaction(self.home, self.plan({'shell'}))
        backup = self.home / m.STATE / 'backups' / identifier
        meta = json.loads((backup / 'manifest.json').read_text())
        entry = next(x for x in meta['files'] if x['saved'] is not None)
        (backup / entry['saved']).write_text('damaged')
        with self.assertRaisesRegex(m.Problem, 'dañada'):
            m.restore_plan(self.home, identifier)

    def test_optional_workspaces_not_installed_by_default(self):
        paths = [x['path'] for x in self.plan()]
        self.assertNotIn('.config/hypr/bindings.lua', paths)
        self.assertIn('.config/hypr/bindings.lua', [x['path'] for x in self.plan({'workspaces'})])

    def test_syntax_of_generated_bash(self):
        data = next(x['after'] for x in self.plan({'shell'}) if x['path'] == '.bashrc')
        result = subprocess.run(['bash', '-n'], input=data, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b'alias mine="echo kept"', data)

    def test_blesh_update_falls_back_before_loading(self):
        folder = self.base / 'default/bash'
        folder.mkdir(parents=True)
        (folder / 'init').write_text('# changed by a future Omarchy update\n')
        (folder / 'rc').write_text('printf "%s\\n" DEFAULT_BASH_LOADED\n')
        result = subprocess.run(['bash', '-c', 'source "$1"', '_', str(ROOT / 'payload/bash/omarchy-blesh.sh')],
                                env={**os.environ, 'OMARCHY_PATH': str(self.base)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'DEFAULT_BASH_LOADED\n')
        self.assertIn('Bash estándar', result.stderr)

    def test_plugin_manifest_entrypoints_exist(self):
        for manifest in (ROOT / 'payload/plugins').glob('*/manifest.json'):
            data = json.loads(manifest.read_text())
            self.assertEqual(data['id'], manifest.parent.name)
            for filename in data['entryPoints'].values():
                self.assertTrue((manifest.parent / filename).is_file(), str(manifest))

    @unittest.skipUnless(supported_fzf(), 'fzf >= 0.74.4 is optional in CI')
    def test_history_preserves_exact_selected_bytes(self):
        for sample in [b'1\tls -la', b'2\techo "two words"', b'3\techo $(date)',
                       b'4\tprintf "a\\nb"\nnext line', b'5\tprintf "tabs\there"']:
            # Apply the same options fzf's Ctrl+R integration uses, including the dimmed numbers.
            env_cmd = 'source "$1"; export FZF_DEFAULT_OPTS="$FZF_CTRL_R_OPTS"; fzf --read0 --print0 --filter=""'
            result = subprocess.run(['bash', '-c', env_cmd, '_', str(ROOT / 'payload/bash/fzf-history.sh')],
                                    input=sample + b'\0', capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, sample + b'\0')


if __name__ == '__main__':
    unittest.main()
