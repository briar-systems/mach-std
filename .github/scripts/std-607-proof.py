import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

host = sys.argv[1]
census = runpy.run_path('.github/scripts/std-607-census.py')['census']
root = Path.cwd()
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
census('held-destination-baseline', host)
result = subprocess.run(['mach', 'test', 'test/native', '--target', host + '-x86_64',
    '--include-deps', '--filter', 'held destinations'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = result.stdout.decode('utf-8', errors='replace')
Path('std-607-evidence/baseline.log').write_text(log, encoding='utf-8')
print(log, flush=True)
clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
counts = list(map(int, counts[-1])) if counts else None
exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
expected = [0,3,3] if host == 'windows' else [3,0,3]
expected_exits = ['73','73','74'] if host == 'windows' else []
record = dict(counts=counts, exits=exits, compiler_exit=result.returncode)
Path('std-607-evidence/summary.json').write_text(json.dumps(record, indent=2))
assert counts == expected and sorted(exits) == expected_exits, record
assert (result.returncode == 0) == (host != 'windows'), record
