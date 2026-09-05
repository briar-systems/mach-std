import json
import pathlib
import re
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[2]
source = root / 'src/filesystem/transaction.mach'
subprocess.run(['git', 'diff', '--exit-code', '46b8d96', '--', 'src', 'mach.toml'], cwd=root, check=True)
pristine = source.read_bytes()
text = source.read_text(encoding='utf-8')
evidence = root / 'mutation-evidence'
evidence.mkdir(exist_ok=True)
fixture = root / 'test/native'
dependency = fixture / 'dep/std'
dependency.mkdir(parents=True, exist_ok=True)
anchor = '                    str_free(alloc, copied);'
if text.count(anchor) != 1:
    raise SystemExit('pending-name release anchor must be unique')
variants = [
    ('baseline', text, [1, 0, 1], []),
    ('omit-pending-release', text.replace(anchor, '', 1), [0, 1, 1], ['17']),
    ('omit-later-growth-release', text.replace(anchor,
        '                    if (out.len == 0) { str_free(alloc, copied); }', 1), [0, 1, 1], ['17']),
]
results = []
try:
    for name, body, expected, expected_exits in variants:
        source.write_text(body, encoding='utf-8', newline='')
        shutil.copy2(root / 'mach.toml', dependency / 'mach.toml')
        shutil.copytree(root / 'src', dependency / 'src', dirs_exist_ok=True)
        command = [sys.argv[1], 'test', str(fixture), '--target', sys.argv[2], '--include-deps',
            '--filter', 'list_entries: every allocation failure retains exact name ownership']
        process = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        log = process.stdout.decode('utf-8', errors='replace')
        (evidence / (name + '.log')).write_text(log, encoding='utf-8')
        clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
        counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
        counts = list(map(int, counts[-1])) if counts else None
        exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
        valid = counts == expected and exits == expected_exits
        valid = valid and ((process.returncode == 0) == (expected[1] == 0))
        result = dict(name=name, counts=counts, exits=exits, compiler_exit=process.returncode, verified=valid)
        results.append(result)
        print(json.dumps(result), flush=True)
        (evidence / 'summary.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
finally:
    source.write_bytes(pristine)
    subprocess.run(['git', 'diff', '--exit-code', '--', str(source.relative_to(root))], cwd=root, check=True)
if not all(result['verified'] for result in results):
    raise SystemExit('listing mutation did not produce the exact expected runtime outcome')
