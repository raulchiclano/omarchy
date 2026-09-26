import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import shutil
import os
import io
import tarfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'installer.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def supported_fzf():
    if not shutil.which('fzf'):
        return False
    version = subprocess.check_output(['fzf', '--version'], text=True).split()[0]
    return tuple(map(int, version.split('.')[:3])) >= (0, 74, 3)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'home'
        self.home.mkdir()
        # Default installation includes dock, but unit tests never need the network.
        payload_patch = patch.object(m, 'dock_payload', return_value={
            'shell.qml': b'import Quickshell\nShellRoot {}\n', 'LICENSE': b'MIT fixture\n'})
        payload_patch.start()
        self.addCleanup(payload_patch.stop)
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

    def test_new_services_migrate_without_duplicates_or_personal_data(self):
        personal = {
            '.local/state/omarchy/clipboard-history.json': '["private clipboard"]',
            '.local/state/omarchy/current/background': 'private wallpaper sentinel',
            '.config/hypr/monitors.lua': 'laptop monitor settings',
        }
        for path, content in personal.items():
            self.write(path, content)
        config = json.loads((self.home / '.config/omarchy/shell.json').read_text())
        for name in ('clipboard', 'emojis', 'lock'):
            config['plugins'].append({'id': 'raulchiclano.' + name})
        self.write('.config/omarchy/shell.json', json.dumps(config))
        changes = self.plan({'desktop'})
        m.transaction(self.home, changes)
        installed = json.loads((self.home / '.config/omarchy/shell.json').read_text())
        ids = [x['id'] for x in installed['plugins']]
        for name in ('clipboard', 'emojis', 'lock'):
            self.assertEqual(ids.count('lavanda.' + name), 1)
            self.assertNotIn('raulchiclano.' + name, ids)
            self.assertIn('omarchy.' + name, installed['disabledPlugins'])
            self.assertIn('raulchiclano.' + name, installed['disabledPlugins'])
            self.assertIn('lavanda.' + name, installed['cloneSourceRestores'])
        for path, content in personal.items():
            self.assertEqual((self.home / path).read_text(), content)
        self.assertEqual(self.plan({'desktop'}), [])

    def test_lock_guard_rejects_locked_or_unknown_session_before_writes(self):
        changes = self.plan({'desktop'})
        before = self.snapshot()
        with patch.object(m.Path, 'home', return_value=self.home), \
             patch.dict(os.environ, {'HYPRLAND_INSTANCE_SIGNATURE': 'test'}):
            for result in ('true', 'unknown', ''):
                with patch.object(m.subprocess, 'check_output', return_value=result):
                    with self.assertRaisesRegex(m.Problem, 'Desbloquea'):
                        m.transaction(self.home, changes)
            with patch.object(m.subprocess, 'check_output', side_effect=subprocess.TimeoutExpired('lock', 3)):
                with self.assertRaisesRegex(m.Problem, 'No se pudo comprobar'):
                    m.transaction(self.home, changes)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.home / m.STATE).exists())

    def test_lock_guard_accepts_unlocked_and_skips_unrelated_files(self):
        changes = [{'path': '.config/omarchy/plugins/lavanda.lock/LockView.qml'}]
        with patch.object(m.Path, 'home', return_value=self.home), \
             patch.dict(os.environ, {'HYPRLAND_INSTANCE_SIGNATURE': 'test'}), \
             patch.object(m.subprocess, 'check_output', return_value='false\n') as check:
            m.check_live_lock(self.home, changes)
            check.assert_called_once()
            check.reset_mock()
            m.check_live_lock(self.home, [{'path': '.config/foot/foot.ini'}])
            m.check_live_lock(self.home / 'other', changes)
            check.assert_not_called()

    def test_lock_authentication_service_matches_validated_omarchy(self):
        expected = json.loads((ROOT / 'compatibility.json').read_text())['desktop']['shell/plugins/lock/Service.qml']
        self.assertEqual(m.digest((ROOT / 'payload/plugins/lavanda.lock/Service.qml').read_bytes()), expected)

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

    def test_compatibility_accepts_an_alternative_validated_base(self):
        compatibility_root = Path(self.tmp.name) / 'compatibility'
        compatibility_root.mkdir()
        current = (self.base / 'config/omarchy/shell.json').read_bytes()
        metadata = {
            'desktop': {'config/omarchy/shell.json': [m.digest(b'try runtime'), m.digest(current)]},
            'shell': {},
        }
        (compatibility_root / 'compatibility.json').write_text(json.dumps(metadata))
        with patch.object(m, 'ROOT', compatibility_root):
            m.check_compatibility({'desktop'}, self.base)
            (self.base / 'config/omarchy/shell.json').write_text('unknown future base')
            with self.assertRaisesRegex(m.Problem, 'Base no validada'):
                m.check_compatibility({'desktop'}, self.base)

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

    def test_dock_is_default_and_only_dock_is_isolated(self):
        changes = self.plan({'dock'})
        self.assertTrue(any(x['path'] == '.local/bin/hyprland-dock' for x in self.plan()))
        self.assertFalse(any(x['path'].startswith(('.config/hypr/', '.config/omarchy/')) for x in changes))
        before = self.snapshot()
        identifier = m.transaction(self.home, changes)
        launcher = self.home / '.local/bin/hyprland-dock'
        self.assertEqual(launcher.stat().st_mode & 0o777, 0o755)
        settings = json.loads((self.home / '.config/hyprland-dock/dock.json').read_text())
        self.assertEqual(settings, json.loads((ROOT / 'payload/dock/dock.json').read_text()))
        self.assertIn('--daemonize', (self.home / '.config/autostart/hyprland-dock.desktop').read_text())
        self.assertEqual(self.plan({'dock'}), [])
        m.transaction(self.home, m.restore_plan(self.home, identifier), 'restore')
        self.assertEqual(before, self.snapshot())

    def test_dock_preserves_pins_and_unknown_settings_but_applies_style(self):
        self.write('.config/hyprland-dock/dock.json', json.dumps({'pinned': ['my.app'], 'position': 'left', 'future': 42}))
        m.transaction(self.home, self.plan({'dock'}))
        settings = json.loads((self.home / '.config/hyprland-dock/dock.json').read_text())
        self.assertEqual(settings['pinned'], ['my.app'])
        self.assertEqual(settings['future'], 42)
        self.assertEqual(settings['position'], 'bottom')
        self.assertTrue(settings['intelligentHide'])

    def test_dock_mode_only_change_restores_original_mode(self):
        m.transaction(self.home, self.plan({'dock'}))
        launcher = self.home / '.local/bin/hyprland-dock'
        launcher.chmod(0o600)
        changes = self.plan({'dock'})
        self.assertEqual(len(changes), 1)
        identifier = m.transaction(self.home, changes)
        self.assertEqual(launcher.stat().st_mode & 0o777, 0o755)
        m.transaction(self.home, m.restore_plan(self.home, identifier), 'restore')
        self.assertEqual(launcher.stat().st_mode & 0o777, 0o600)

    def test_mode_change_during_review_refused(self):
        changes = self.plan({'shell'})
        (self.home / '.bashrc').chmod(0o600)
        with self.assertRaisesRegex(m.Problem, 'durante la revisión'):
            m.transaction(self.home, changes)

    def test_dock_invalid_pins_refused(self):
        for value in ['bad', [1]]:
            self.write('.config/hyprland-dock/dock.json', json.dumps({'pinned': value}))
            with self.assertRaisesRegex(m.Problem, 'lista de aplicaciones'):
                self.plan({'dock'})

    def test_dock_launcher_syntax_and_update_does_not_download(self):
        script = ROOT / 'payload/dock/hyprland-dock'
        subprocess.run(['bash', '-n', str(script)], check=True)
        result = subprocess.run(['bash', str(script), 'update'], text=True, capture_output=True, check=True)
        self.assertIn('./install.sh apply --only dock', result.stdout)

    def test_stop_dock_accepts_empty_quickshell_output(self):
        self.write('.local/share/hyprland-dock/shell.qml', 'ShellRoot {}')
        for output in ['', '[]\n', 'No running instances for /dock/shell.qml\nUse --all to list all instances.\n']:
            with patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, output, '')):
                m.stop_live_dock(self.home)

    def test_fresh_install_does_not_stop_other_shells(self):
        with patch.object(m.subprocess, 'run') as run:
            m.stop_live_dock(self.home)
            run.assert_not_called()

    def test_managed_restart_waits_for_stop_before_starting(self):
        fake_bin = Path(self.tmp.name) / 'bin'
        fake_bin.mkdir()
        qs = fake_bin / 'qs'
        qs.write_text('#!/bin/sh\ncase "$1" in\nkill) exit 0;;\nlist) echo "No running instances for /dock/shell.qml"; exit 0;;\n*) printf "STARTED\\n";;\nesac\n')
        qs.chmod(0o755)
        result = subprocess.run(['bash', str(ROOT / 'payload/dock/hyprland-dock'), 'restart'],
                                env={**os.environ, 'PATH': str(fake_bin) + ':' + os.environ['PATH']},
                                text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, 'STARTED\n')

    def test_dock_write_failure_restores_previous_launcher_permissions(self):
        self.write('.local/bin/hyprland-dock', 'original')
        launcher = self.home / '.local/bin/hyprland-dock'
        launcher.chmod(0o600)
        before = self.snapshot()
        real_write = m.atomic_write
        def fail(path, data, mode=0o644):
            if str(path).endswith('/autostart/hyprland-dock.desktop'):
                raise OSError('autostart failure')
            return real_write(path, data, mode)
        with patch.object(m, 'atomic_write', side_effect=fail):
            with self.assertRaisesRegex(OSError, 'autostart'):
                m.transaction(self.home, self.plan({'dock'}))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(launcher.stat().st_mode & 0o777, 0o600)

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

    @unittest.skipUnless(supported_fzf(), 'fzf >= 0.74.3 is optional in CI')
    def test_history_preserves_exact_selected_bytes(self):
        for sample in [b'1\tls -la', b'2\techo "two words"', b'3\techo $(date)',
                       b'4\tprintf "a\\nb"\nnext line', b'5\tprintf "tabs\there"']:
            # Apply the same options fzf's Ctrl+R integration uses, including the dimmed numbers.
            env_cmd = 'source "$1"; export FZF_DEFAULT_OPTS="$FZF_CTRL_R_OPTS"; fzf --read0 --print0 --filter=""'
            result = subprocess.run(['bash', '-c', env_cmd, '_', str(ROOT / 'payload/bash/fzf-history.sh')],
                                    input=sample + b'\0', capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, sample + b'\0')


class DockDownloadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.revision = 'a' * 40
        self.lock = {'repository': 'raulchiclano/hyprland-dock', 'revision': self.revision,
                     'files': {'shell.qml': m.digest(b'good')}}
        (self.root / 'dock.lock.json').write_text(json.dumps(self.lock))

    def archive(self, contents=b'good', name='shell.qml', symlink=False, duplicate=False):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            member = tarfile.TarInfo('hyprland-dock-' + self.revision + '/' + name)
            member.size = len(contents)
            if symlink:
                member.type = tarfile.SYMTYPE
                member.linkname = '/etc/passwd'
                member.size = 0
            archive.addfile(member, io.BytesIO(contents))
            if duplicate:
                archive.addfile(member, io.BytesIO(contents))
        return buffer.getvalue()

    def fetch(self, data):
        with patch.object(m, 'ROOT', self.root), patch.object(m.urllib.request, 'urlopen', return_value=io.BytesIO(data)):
            return m.dock_payload()

    def test_verified_download(self):
        self.assertEqual(self.fetch(self.archive()), {'shell.qml': b'good'})

    def test_hash_mismatch(self):
        with self.assertRaisesRegex(m.Problem, 'huella'):
            self.fetch(self.archive(b'bad'))

    def test_missing_member(self):
        with self.assertRaisesRegex(m.Problem, 'Faltan archivos'):
            self.fetch(self.archive(name='different.qml'))

    def test_symlink_and_duplicate_rejected(self):
        for kwargs in [{'symlink': True}, {'duplicate': True}]:
            with self.assertRaisesRegex(m.Problem, 'no válido'):
                self.fetch(self.archive(**kwargs))

    def test_network_failure_reported(self):
        with patch.object(m, 'ROOT', self.root), patch.object(m.urllib.request, 'urlopen', side_effect=OSError('offline')):
            with self.assertRaisesRegex(m.Problem, 'no se ha instalado nada'):
                m.dock_payload()


if __name__ == '__main__':
    unittest.main()
