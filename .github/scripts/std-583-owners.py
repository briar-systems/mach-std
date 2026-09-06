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
identity_path = 'src/filesystem/transaction/ownership.mach'
identity = (root / identity_path).read_text(encoding='utf-8')
results = []

def run(name, selected, counts, changed=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    if changed is not None:
        (snapshot / identity_path).write_text(changed, encoding='utf-8', newline='')
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
    for name in ('mach_583_owner_lifetime', 'mach_583_owner_namespace', 'mach_583_owner_recovery'):
        path = root / name
        if path.exists(): shutil.rmtree(path)
    if not valid:
        print(log, flush=True)
        raise AssertionError(record)

try:
    for profile in (['debug', 'release'] if host == 'darwin' else ['debug']):
        os.environ['MACH_583_PROFILE'] = profile
        run(profile + '-owners', 'std.filesystem.transaction.ownership:', [3, 0, 3])
        before = 'if (held.fd < 0 || held.borrowers != 0 || held.recovering || held.closing) {'
        assert identity.count(before) == 1
        run(profile + '-live-recovery-mutant', 'std.filesystem.transaction.ownership: live borrows', [0, 1, 1], identity.replace(before,
            'if (held.fd < 0 || held.recovering || held.closing) {'))
        before = 'if (root.address != root::usize) { ret os.EINVAL; }'
        assert identity.count(before) == 1
        run(profile + '-copied-owner-mutant', 'std.filesystem.transaction.ownership: live borrows', [0, 1, 1], identity.replace(before, ''))
        before = 'if (held.fd < 0 || held.closing || held.recovering || !held.initialized) {'
        assert identity.count(before) == 1
        run(profile + '-uninitialized-admission-mutant', 'std.filesystem.transaction.ownership: live borrows', [0, 1, 1], identity.replace(before,
            'if (held.fd < 0 || held.closing || held.recovering) {'))
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path in (root / 'src').rglob('*.mach'):
        assert path.read_bytes() == (snapshot / path.relative_to(root)).read_bytes()
    (evidence / 'source-restored.txt').write_text('exact production source restored\n')
