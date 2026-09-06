import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

host = sys.argv[1]
census = runpy.run_path('.github/scripts/std-613-census.py')['census']
root = Path.cwd()
evidence = root / 'std-613-evidence'
evidence.mkdir(exist_ok=True)
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
windows_path = 'src/system/os/windows/shared.mach'
windows = (root / windows_path).read_text(encoding="utf-8")
results = []


def run(name, selected, counts, edits=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path, body in (edits or {}).items():
        (snapshot / path).write_text(body, encoding='utf-8', newline='')
    census(name, host)
    result = subprocess.run(['mach', 'test', 'test/native', '--target', host + '-x86_64',
        '--include-deps', '--filter', selected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    log = result.stdout.decode('utf-8', errors='replace')
    (evidence / (name + '.log')).write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    found = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    actual = list(map(int, found[-1])) if found else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    valid = actual == counts and ((result.returncode == 0) == (counts[1] == 0))
    valid = valid and len(exits) == counts[1] and all(x.isdigit() and int(x) != 0 for x in exits)
    record = dict(name=name, counts=actual, exits=exits, code=result.returncode, verified=valid)
    results.append(record)
    print(json.dumps(record), flush=True)
    (evidence / 'summary.json').write_text(json.dumps(results, indent=2))
    if not valid:
        print(log, flush=True)
        raise AssertionError(record)


def cleanup():
    names = ['mach_613_remove_tree', 'mach_613_remove_outside', 'mach_613_readonly_tree', 'mach_613_readonly_alias']
    if host == 'windows':
        code = "$ErrorActionPreference='Stop'; " + '; '.join("if (Test-Path -LiteralPath '" + n + "') {Remove-Item -LiteralPath '" + n + "' -Recurse -Force}" for n in names)
        subprocess.run(['powershell.exe', '-NoProfile', '-Command', code], check=True)
    else:
        for name in names:
            p = root / name
            if p.is_dir(): shutil.rmtree(p)
            elif p.exists(): p.unlink()


try:
    run('baseline', 'std.filesystem.remove_all:', [2, 0, 2] if host == 'windows' else [1, 0, 1])
    if host == 'windows':
        before = 'ret unlink_relative(dirfd, path, flags, true);'
        assert windows.count(before) == 1
        run('strict-mutation', 'std.filesystem.remove_all: forces readonly', [0, 1, 1],
            {windows_path: windows.replace(before, 'ret unlink_relative(dirfd, path, flags, false);')})
        cleanup()
        before = 'var options: u32 = FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT;'
        assert windows.count(before) == 1
        mutant = windows.replace(before, before + '\n    if ((desired_override & DELETE_ACCESS) != 0) { options = options & ~FILE_OPEN_REPARSE_POINT; }')
        run('follow-mutation', 'std.filesystem.remove_all: forces readonly', [0, 1, 1], {windows_path: mutant})
        cleanup()
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path in (root / 'src').rglob('*.mach'):
        assert path.read_bytes() == (snapshot / path.relative_to(root)).read_bytes()
    (evidence / 'source-restored.txt').write_text('exact production source restored\n')
