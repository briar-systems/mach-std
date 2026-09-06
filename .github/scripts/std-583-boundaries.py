import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

host, arch = sys.argv[1:]
census = runpy.run_path('.github/scripts/std-583-census.py')['census']
root = Path.cwd()
evidence = root / 'std-583-evidence'
evidence.mkdir(exist_ok=True)
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
identity_path = 'src/system/file_identity.mach'
identity = (root / identity_path).read_text(encoding='utf-8')
results = []

def run(name, selected, counts, changed=None, extra=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    if changed is not None:
        (snapshot / identity_path).write_text(changed, encoding='utf-8', newline='')
    for path, body in (extra or {}).items():
        (snapshot / path).write_text(body, encoding='utf-8', newline='')
    shutil.rmtree(root / 'test/native/out', ignore_errors=True)
    shutil.rmtree(root / 'test/native/.cache', ignore_errors=True)
    census(name, host)
    result = subprocess.run([os.environ.get('MACH_583_COMPILER', 'mach'), 'test', 'test/native', '--target', host + '-' + arch,
        '--include-deps', '--profile', os.environ.get('MACH_583_PROFILE', 'debug'), '--filter', selected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    log = result.stdout.decode('utf-8', errors='replace')
    (evidence / (name + '.log')).write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    found = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    actual = list(map(int, found[-1])) if found else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    valid = actual == counts and ((result.returncode == 0) == (counts[1] == 0))
    valid = valid and len(exits) == counts[1] and all(x.isdigit() and int(x) != 0 for x in exits)
    record = dict(name=name, profile=os.environ.get('MACH_583_PROFILE', 'debug'), counts=actual, exits=exits, code=result.returncode, verified=valid)
    results.append(record)
    print(json.dumps(record), flush=True)
    (evidence / 'summary.json').write_text(json.dumps(results, indent=2))
    if not valid:
        print(log, flush=True)
        raise AssertionError(record)


owner_path = 'src/filesystem/transaction/ownership.mach'
owner = (root / owner_path).read_text(encoding='utf-8')
windows_path = 'src/system/os/windows/shared.mach'
windows = (root / windows_path).read_text(encoding='utf-8')
os_path = 'src/system/os.mach'
os_source = (root / os_path).read_text(encoding='utf-8')

def command(args):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=90)
    with (evidence / 'backend-setup.log').open('a', encoding='utf-8') as log:
        log.write(repr(args) + '\n' + result.stdout + '\n')
    print(result.stdout, flush=True)
    result.check_returncode()
    return result.stdout

def powershell(code):
    return command(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', "$ErrorActionPreference='Stop'; " + code])

mount = root / 'mach_583_ext4'

def namespace_setup():
    if host == 'windows':
        powershell("foreach($mode in @('sensitive','folded')) { $p=Join-Path (Get-Location) ('mach_583_'+$mode); if(Test-Path $p) { Remove-Item -Recurse -Force $p }; New-Item -ItemType Directory $p | Out-Null; $setting=if($mode -eq 'sensitive') {'enable'} else {'disable'}; fsutil.exe file setCaseSensitiveInfo $p $setting; if($LASTEXITCODE -ne 0) { throw 'case mode setup refused' }; $child=Join-Path $p '.machtxn.claims'; New-Item -ItemType Directory $child | Out-Null; $opposite=if($mode -eq 'sensitive') {'disable'} else {'enable'}; fsutil.exe file setCaseSensitiveInfo $child $opposite; if($LASTEXITCODE -ne 0) { throw 'stale mode setup refused' }; fsutil.exe file queryCaseSensitiveInfo $p; fsutil.exe file queryCaseSensitiveInfo $child }")
        return [root / 'mach_583_sensitive', root / 'mach_583_folded']
    for mode in ('sensitive', 'folded'):
        path = mount / mode
        command(['sudo', 'rm', '-rf', str(path)])
        path.mkdir()
        command(['chattr', '+F' if mode == 'folded' else '-F', str(path)])
        child = path / '.machtxn.claims'
        child.mkdir()
        command(['chattr', '-F' if mode == 'folded' else '+F', str(child)])
        command(['lsattr', '-d', str(path), str(child)])
    return [mount / 'sensitive', mount / 'folded']

def namespace_body(paths):
    # Verify fixture case behavior independently before comparing native claim creation.
    probe = owner.replace('fun t_namespace(base: str) i32 {', 'fun t_namespace(base: str, folded: bool) i32 {')
    probe = probe.replace('    var held: Lock;\n    if (acquire(?held, ?root) < 0) { ret 5; }\n    fin { release_lock(?held); }\n    if (begin_recovery(?held) < 0) { ret 6; }',
        '    if (folded && lower != os.EEXIST) { ret 31; }\n    if (!folded && lower < 0) { ret 32; }\n    var held: Lock;\n    if (acquire(?held, ?root) < 0) { ret 5; }\n    fin { release_lock(?held); }\n    if (begin_recovery(?held) < 0) { ret 6; }')
    probe = probe.replace('ret t_namespace(base);', 'ret t_namespace(base, false);')
    for path, mode in zip(paths, ('sensitive', 'folded')):
        probe += '\ntest "std583 native namespace ' + mode + '" { ret t_namespace(' + json.dumps(path.as_posix()) + ', ' + ('true' if mode == 'folded' else 'false') + '); }\n'
    return probe

remote_fixture = r"""
$if ($mach.build.os == $mach.os.windows) {
    test "std583 remote identity qualification" {
        val base: str = "//localhost/mach583";
        val directory: i64 = impl.open(impl.AT_FDCWD, base, impl.O_RDONLY | impl.O_DIRECTORY, 0);
        if (directory < 0) { ret 1; }
        val root: i32 = directory::i32;
        fin { impl.close(root); }
        val created: i64 = impl.open(root, "file", impl.O_CREAT | impl.O_RDWR, 0o600);
        if (created < 0) { ret 2; }
        val fd: i32 = created::i32;
        fin { impl.close(fd); }
        var st: impl.stat_t;
        if (impl.stat(fd, ?st) < 0 || (impl.stat_mode(?st) & impl.S_IFMT) != impl.S_IFREG) { ret 3; }
        if (impl.publication_capabilities(root) != 0) { ret 4; }
        var observed: identities.Identity = identities.native(identities.WINDOWS_LOCAL, 31, 59);
        val original: identities.Identity = observed;
        if (impl.file_identity(fd, ?observed) != impl.ENOTSUP || !identities.equal(observed, original)) { ret 5; }
        if (impl.identity_at(root, "file", ?observed) != impl.ENOTSUP || !identities.equal(observed, original)) { ret 6; }
        var i: usize = 0;
        for (i < 512) {
            if (impl.retain_identity_at(root, "file", ?observed) != impl.ENOTSUP || !identities.equal(observed, original)) { ret 7; }
            i = i + 1;
        }
        ret 0;
    }
}
"""
try:
    if host == 'linux':
        command(['truncate', '-s', '256M', 'mach_583_ext4.img'])
        command(['mkfs.ext4', '-F', '-O', 'casefold', 'mach_583_ext4.img'])
        mount.mkdir(exist_ok=True)
        command(['sudo', 'mount', '-o', 'loop', str(root / 'mach_583_ext4.img'), str(mount)])
        command(['sudo', 'chown', str(os.getuid()) + ':' + str(os.getgid()), str(mount)])
    paths = namespace_setup()
    fixture = namespace_body(paths)
    run('native-namespace', 'std583 native namespace', [2, 0, 2], extra={owner_path: fixture})
    paths = namespace_setup()
    fixture = namespace_body(paths)
    before = '        val closed: i64 = os.close(prior::i32);\n        if (cleared < 0) { ret cleared; }'
    assert fixture.count(before) == 1
    mutant = fixture.replace(before, '        if (cleared >= 0) { held.claims_fd = prior::i32; held.initialized = true; ret 0; }\n' + before)
    run('stale-namespace-mutant', 'std583 native namespace', [0, 2, 2], extra={owner_path: mutant})
    if host == 'windows':
        (root / 'mach_583_smb').mkdir(exist_ok=True)
        powershell("$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name; New-SmbShare -Name mach583 -Path (Resolve-Path mach_583_smb).Path -FullAccess $user | Out-Null")
        run('remote-refusal', 'std583 remote identity', [1, 0, 1], extra={os_path: os_source + remote_fixture})
        before = 'if ((device.characteristics & FILE_REMOTE_DEVICE) != 0) { ret ENOTSUP; }'
        assert windows.count(before) == 1
        run('unqualified-remote-mutant', 'std583 remote identity', [0, 1, 1], extra={os_path: os_source + remote_fixture, windows_path: windows.replace(before, '')})
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path in (root / 'src').rglob('*.mach'):
        assert path.read_bytes() == (snapshot / path.relative_to(root)).read_bytes()
    (evidence / 'source-restored.txt').write_text('exact production source restored\n')
    if host == 'linux':
        command(['sudo', 'umount', str(mount)])
    if host == 'windows':
        powershell("if(Get-SmbShare -Name mach583 -ErrorAction SilentlyContinue) { Remove-SmbShare -Name mach583 -Force }")
