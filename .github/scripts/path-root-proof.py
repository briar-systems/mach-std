import datetime
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess

root = Path.cwd()
source_commit = '55c0fd706c341b47e83a8b8d0ccf858180e06196'
source = root / 'src/types/path.mach'
pristine = subprocess.check_output(['git', 'show', source_commit + ':src/types/path.mach'])
assert source.read_bytes() == pristine
windows = os.name == 'nt'
compiler = root / '.mach-seed' / ('mach.exe' if windows else 'mach')
target = 'windows-x86_64' if windows else 'linux-x86_64'
fixture = root / 'test/native'
evidence = root / 'path-root-evidence'
evidence.mkdir(exist_ok=True)
identity = dict(source_commit=source_commit, target=target, seed=os.environ['SEED_TAG'])
(evidence / 'identity.json').write_text(json.dumps(identity, indent=2))
assert identity['seed'] == 'v4.26.5', identity
results = []
borrowed = 'std.types.path.root: borrowed prefixes preserve ownership and spelling'
anchors = 'std.types.path.root: platform anchors are indivisible'
depth = 'std.types.path.seg_count: excludes platform root units'


def census():
    if windows:
        query = ("Get-CimInstance Win32_Process | Where-Object { "
                 "$_.Name -match '^(mach|m[0-9A-Za-z]*|A|B|C|D)\\.exe$' -and "
                 "$_.CommandLine -match '\\s(build|test)(\\s|$)' } | "
                 "Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress")
        output = subprocess.check_output(['powershell', '-NoProfile', '-Command', query], text=True)
        assert not output.strip(), output
    else:
        pattern = r'^(\S*/)?(mach|m[0-9A-Za-z]*|A|B|C|D)(\.exe)? (build|test)( |$)'
        result = subprocess.run(['pgrep', '-af', pattern], capture_output=True, text=True)
        output = result.stdout
        assert result.returncode == 1, output
    with (evidence / 'process-census.log').open('a') as log:
        log.write(datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n' + output)


def run(name, selected, expected, assertion=None):
    dependency = fixture / 'dep/std'
    shutil.rmtree(dependency, ignore_errors=True)
    dependency.mkdir(parents=True)
    shutil.copy2(root / 'mach.toml', dependency / 'mach.toml')
    shutil.copytree(root / 'src', dependency / 'src')
    shutil.rmtree(fixture / 'out', ignore_errors=True)
    census()
    command = [str(compiler), 'test', '.', '--target', target, '--include-deps', '--filter', selected]
    process = subprocess.Popen(command, cwd=fixture, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, start_new_session=not windows)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=180)
    except subprocess.TimeoutExpired:
        timed_out = True
        if windows:
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(process.pid)], capture_output=True)
        else:
            os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate(timeout=15)
    text = output.decode('utf-8', errors='replace')
    (evidence / (name + '.log')).write_text(text, encoding='utf-8')
    summaries = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', text)
    counts = list(map(int, summaries[-1])) if len(summaries) == 1 else None
    exits = re.findall(r'\(exit ([^)]+)\)', text)
    passed = not timed_out and counts == expected
    if assertion is None:
        passed = passed and process.returncode == 0
    else:
        passed = passed and process.returncode == 1 and set(exits) == {str(assertion)}
    result = dict(name=name, selected=selected, counts=counts, exits=exits,
                  compiler_exit=process.returncode, timeout=timed_out, verified=passed)
    results.append(result)
    (evidence / 'results.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(result), flush=True)
    return passed


variants = [
    ('empty-length', borrowed, 1, False,
     'if (is_empty(p)) { ret view.view(p, 0); }',
     'if (is_empty(p)) { ret view.view(p, 1); }'),
    ('relative-anchor', borrowed, 3, False,
     'if (leading > 0 && (n == 0 || p[leading] == 0)) { n = 1; }',
     'if (n == 0 || p[leading] == 0) { n = 1; }'),
    ('separator-root', borrowed, 4, False,
     'if (leading > 0 && (n == 0 || p[leading] == 0)) { n = 1; }',
     'if (leading > 0 && p[leading] == 0) { n = 1; }'),
    ('borrowed-pointer', borrowed, 3, False,
     'ret view.view(p, n);', 'ret view.view(nil, n);'),
    ('separator-only-unc', borrowed, 5, True,
     'if (leading > 0 && (n == 0 || p[leading] == 0)) { n = 1; }',
     'if (leading > 0 && n == 0) { n = 1; }'),
    ('missing-platform-root', anchors, 1, True,
     'var n: usize = root_len(p);', 'var n: usize = 0;'),
    ('old-segment-origin', depth, 1, True,
     'var i: usize = anchor.len;', 'var i: usize = 0;'),
]
try:
    assert run('baseline-root', 'std.types.path.root:', [2, 0, 2])
    assert run('baseline-depth', 'std.types.path.seg_count:', [3, 0, 3])
    for name, selected, assertion, needs_windows, before, after in variants:
        if needs_windows and not windows:
            print(name + ': native Windows proof required', flush=True)
            continue
        text = pristine.decode()
        assert text.count(before) == 1, name
        source.write_bytes(text.replace(before, after, 1).encode())
        run(name, selected, [0, 1, 1], assertion)
        source.write_bytes(pristine)
finally:
    source.write_bytes(pristine)
    subprocess.run(['git', 'diff', '--exit-code', '--', 'src/types/path.mach'], check=True)
assert all(result['verified'] for result in results), 'a mutation lacks runtime assertion proof'
