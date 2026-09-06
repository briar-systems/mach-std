import json
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

def run(name, selected, counts, changed=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    if changed is not None:
        (snapshot / identity_path).write_text(changed, encoding='utf-8', newline='')
    census(name, host)
    result = subprocess.run(['mach', 'test', 'test/native', '--target', host + '-' + arch,
        '--include-deps', '--filter', selected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
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

try:
    run('serialization', 'std.system.file_identity:', [2, 0, 2])
    run('native-observation', 'std.system.os.file_identity:', [1, 0, 1])
    before = 'for (i < 41) {\n        if (a.representation[i] != b.representation[i])'
    assert identity.count(before) == 1
    run('truncated-file-id', 'std.system.file_identity:', [1, 1, 2], identity.replace(before,
        'for (i < 33) {\n        if (a.representation[i] != b.representation[i])'))
    before = 'var i: usize = 0;\n    for (i < 41) {\n        if (a.representation[i] != b.representation[i])'
    assert identity.count(before) == 1
    run('missing-volume-domain', 'std.system.file_identity:', [1, 1, 2], identity.replace(before,
        'var i: usize = 17;\n    for (i < 41) {\n        if (a.representation[i] != b.representation[i])'))
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path in (root / 'src').rglob('*.mach'):
        assert path.read_bytes() == (snapshot / path.relative_to(root)).read_bytes()
    (evidence / 'source-restored.txt').write_text('exact production source restored\n')
