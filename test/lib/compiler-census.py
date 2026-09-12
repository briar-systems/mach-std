import datetime
import json
import os
from pathlib import Path
import subprocess
import sys


# the census guards one checkout's evidence: a compiler working in another checkout on
# the same host (a peer worktree, a sibling clone) cannot interleave with this leg's
# builds, so only processes whose working directory lies under this checkout count. a
# process whose cwd cannot be read is kept, so a vanished or foreign-user compiler
# still refuses rather than passing silently. `seen` in the record keeps the unfiltered
# list for the evidence
def within_checkout(listing):
    root = Path(__file__).resolve().parents[2]
    kept = []
    for line in listing.splitlines():
        pid = line.split(' ', 1)[0]
        try:
            cwd = Path(os.readlink('/proc/' + pid + '/cwd')).resolve()
        except OSError:
            kept.append(line)
            continue
        if cwd == root or root in cwd.parents:
            kept.append(line)
    return '\n'.join(kept)


def census(label, evidence):
    if os.name == 'nt':
        command = ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                   "$ErrorActionPreference = 'Stop'; @((Get-CimInstance Win32_Process) | "
                   "Where-Object { $_.Name -match '^(mach|m[0-9A-Za-z]*|A|B|C|D)(\\.exe)?$' "
                   "-and $_.CommandLine -match '\\s(build|test)(\\s|$)' } | "
                   'Select-Object ProcessId, Name, CommandLine) | ConvertTo-Json -Compress']
    else:
        command = ['pgrep', '-af',
                   r'^(\S*/)?(mach|m[0-9A-Za-z]*|A|B|C|D)(\.exe)? (build|test)( |$)']
    result = subprocess.run(command, capture_output=True, text=True)
    valid = not result.stderr.strip() and result.returncode in ((0,) if os.name == 'nt' else (0, 1))
    processes = result.stdout.strip()
    if os.name != 'nt':
        processes = within_checkout(processes)
    active = processes not in ('', '[]', 'null')
    record = dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  label=label, command=command, active=active, processes=processes,
                  seen=result.stdout.strip(), valid=valid, status=result.returncode,
                  stderr=result.stderr)
    with (evidence / 'census.jsonl').open('a') as output:
        output.write(json.dumps(record) + '\n')
    print(json.dumps(record), file=sys.stderr, flush=True)
    if not valid:
        raise RuntimeError('compiler process census failed')
    if active:
        raise RuntimeError('another compiler build or test is active')



if __name__ == "__main__":
    evidence = Path(sys.argv[1])
    evidence.mkdir(parents=True, exist_ok=True)
    census(" ".join(sys.argv[2:]), evidence)
