import json
import os
import re
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import zipfile

host, arch = sys.argv[1:]
census = runpy.run_path('.github/scripts/std-583-census.py')['census']
evidence = Path('std-583-evidence')
snapshot = Path('test/native/dep/std')
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
transaction = snapshot / 'src/filesystem/transaction.mach'
ownership = snapshot / 'src/filesystem/transaction/ownership.mach'
original = {p: p.read_text() for p in (transaction, ownership)}

def dump(label, pointer, typename):
    marker = '\nSTATE-' + label + '\n'
    end = '\nENDSTATE\n'
    return ('\n    os.write(2, ' + json.dumps(marker) + ', ' + str(len(marker)) + ');'
            '\n    os.write(2, ' + pointer + '::str, $size_of(' + typename + '));'
            '\n    os.write(2, ' + json.dumps(end) + ', ' + str(len(end)) + ');\n')

changed = dict(original)
start = changed[transaction].index('fun t_reserve(')
end = changed[transaction].index('\n}', start) + 2
region = changed[transaction][start:end]
region = region.replace('    @owned = Claim{};', dump('before-init', 'owned', 'Claim') +
                        '    @owned = Claim{};' + dump('after-init', 'owned', 'Claim'))
changed[transaction] = changed[transaction][:start] + region + changed[transaction][end:]
needle = 'pub fun claim(out: *Claim, alloc: *A.Allocator, held: *Lock, leaf: str) O.Option[Error] {'
changed[transaction] = changed[transaction].replace(needle, needle + dump('claim-entry', 'out', 'Claim'))
needle = 'fun register(out: *Borrow, held: *Lock) i64 {'
changed[ownership] = changed[ownership].replace(needle, needle + dump('register-entry', 'out', 'Borrow'))
results = []
case_index = None
try:
    for version, compiler in [('released', 'mach'), ('audited', os.environ['MACH_583_COMPILER'])]:
        for variant, contents in [('baseline', original), ('state', changed)]:
            for path, text in contents.items():
                path.write_text(text)
            for directory in ('test/native/out', 'test/native/.cache'):
                shutil.rmtree(directory, ignore_errors=True)
            label = version + '-' + variant
            census(label, host)
            args = [compiler, 'test', 'test/native', '--target', host + '-' + arch,
                    '--include-deps', '--profile', 'windows-opt0' if host == 'windows' else 'debug',
                    '--filter', 'copied and invalid commits preserve', '--emit-ir', '--emit-asm']
            run = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=360)
            (evidence / (label + '.log')).write_bytes(run.stdout)
            print(label, 'exit', run.returncode, flush=True)
            print(run.stdout.decode(errors='backslashreplace'), flush=True)
            with zipfile.ZipFile(evidence / (label + '-emitted.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
                for path in Path('test/native').rglob('*'):
                    if path.is_file() and (path.suffix in ('.s', '.ir') or
                                           ('out' in path.parts and path.suffix in ('', '.exe'))):
                        archive.write(path, str(path))
            results.append(dict(version=version, variant=variant, code=run.returncode, args=args))
            if version == 'released':
                match = re.search(rb'rerun: [^\n]+ (\d+)\r?\n', run.stdout)
                assert match is not None, (label, 'runtime rerun index absent')
                case_index = match.group(1).decode()
            if variant == 'state':
                binaries = [p for p in Path('test/native/out').rglob('*') if p.is_file() and p.name in ('native-suite', 'native-suite.exe')]
                assert len(binaries) == 1, binaries
                census(label + '-direct', host)
                direct = subprocess.run([str(binaries[0].resolve()), case_index], stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, timeout=60)
                (evidence / (label + '-direct.log')).write_bytes(direct.stdout)
                assert b'STATE-after-init' in direct.stdout, (label, 'runtime state was not emitted')
                assert direct.returncode == (5 if version == 'released' else 0), (label, direct.returncode)

            if version == 'audited':
                assert run.returncode == 0, (label, run.returncode)
            else:
                assert b'exit 5' in run.stdout or b'exit: 5' in run.stdout, (label, 'expected runtime refusal missing')
    (evidence / 'seed-state-summary.json').write_text(json.dumps(results, indent=2))
finally:
    for path, text in original.items():
        path.write_text(text)
    (evidence / 'seed-state-restored.txt').write_text('production source restored\n')
