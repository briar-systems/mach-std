import datetime
import json
from pathlib import Path
import subprocess
import sys
import time


def census(label, host):
    evidence = Path('std-613-evidence')
    evidence.mkdir(exist_ok=True)
    if host == 'windows':
        command = ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
            "$ErrorActionPreference = 'Stop'; @((Get-CimInstance Win32_Process) | Where-Object { $_.Name -match '^(mach|m[0-9A-Za-z]*|A|B|C|D)(\\.exe)?$' -and $_.CommandLine -match '\\s(build|test)(\\s|$)' } | Select-Object ProcessId, Name, CommandLine) | ConvertTo-Json -Compress"]
    else:
        command = ['bash', '-c', "pgrep -af '^(\\S*/)?(mach|m[0-9A-Za-z]*|A|B|C|D)(\\.exe)? (build|test)( |$)' || true"]
    while True:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stderr.strip():
            raise RuntimeError('process census failed: ' + result.stderr)
        raw = result.stdout.strip()
        active = bool(json.loads(raw)) if host == 'windows' and raw else bool(raw)
        record = dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            label=label, command=command, active=active, processes=raw or '(none)')
        encoded = json.dumps(record)
        print(encoded, flush=True)
        with (evidence / 'compiler-census.jsonl').open('a', encoding='utf-8') as output:
            output.write(encoded + '\n')
        if not active:
            return
        time.sleep(2)


if __name__ == '__main__':
    census(sys.argv[1], sys.argv[2])
