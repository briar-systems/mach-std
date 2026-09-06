import json
from pathlib import Path
import shutil
import subprocess
import runpy
import os

root = Path.cwd()
evidence = root / 'std-583-evidence'
evidence.mkdir(exist_ok=True)
census = runpy.run_path('.github/scripts/std-583-census.py')['census']
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
census('released-seed-image', 'darwin')
result = subprocess.run(['mach', 'test', 'test/native', '--target', 'darwin-aarch64', '--include-deps', '--filter', 'std.system.file_identity:'], capture_output=True, timeout=180)
(evidence / 'released-seed-image.log').write_bytes(result.stdout + result.stderr)
image = root / 'test/native/out/darwin-aarch64/debug/test/native-suite'
if not image.is_file(): raise AssertionError('seed emitted no test image')
shutil.copy2(image, evidence / 'released-seed-native-suite')
headers = subprocess.run(['otool', '-l', str(image)], check=True, capture_output=True)
(evidence / 'released-seed-otool.txt').write_bytes(headers.stdout)
seed_info = subprocess.run(['mach', 'info'], check=True, capture_output=True)
(evidence / 'released-seed-info.txt').write_bytes(seed_info.stdout)
(evidence / 'profiles.txt').write_text('seed identity test: opt=0 debug=true\naudited compiler bootstrap: opt=0 debug=false\naudited identity test: opt=0 debug=true\n')
compiler = root / '.identity-compiler'
subprocess.run(['git', 'clone', '--quiet', 'https://github.com/briar-systems/mach', str(compiler)], check=True)
subprocess.run(['git', '-C', str(compiler), 'checkout', '--detach', '09af0c8da66b4b01501efd6f7732a6b4e111fe81'], check=True)
for label, args in [('dependencies', ['mach', 'dep', 'pull']), ('seed-build-a', ['mach', 'build', '.', '-o', 'a']), ('a-build-b', ['./a', 'build', '.', '-o', 'b']), ('b-build-c', ['./b', 'build', '.', '-o', 'c'])]:
    census(label, 'darwin')
    result = subprocess.run(args, cwd=compiler, capture_output=True, timeout=600)
    (evidence / (label + '.log')).write_bytes(result.stdout + result.stderr)
    if result.returncode != 0: raise AssertionError((label, result.returncode))
if (compiler / 'b').read_bytes() != (compiler / 'c').read_bytes(): raise AssertionError('compiler fixpoint differs')
actual_std = subprocess.check_output(['git', '-C', str(compiler / 'dep/std'), 'rev-parse', 'HEAD'], text=True).strip()
if actual_std != '3ee8e709a8ed7baff6e93780ce9b3582a907a91f': raise AssertionError(actual_std)
(evidence / 'audited-source.json').write_text(json.dumps(dict(mach='09af0c8da66b4b01501efd6f7732a6b4e111fe81', std=actual_std, fixpoint=True)))
shutil.rmtree(root / 'test/native/out', ignore_errors=True)
shutil.rmtree(root / 'test/native/.cache', ignore_errors=True)
census('audited-debug-image', 'darwin')
result = subprocess.run([str(compiler / 'b'), 'test', 'test/native', '--target', 'darwin-aarch64', '--profile', 'debug', '--include-deps', '--filter', 'std.system.file_identity:'], capture_output=True, timeout=180)
(evidence / 'audited-debug-image.log').write_bytes(result.stdout + result.stderr)
if not image.is_file(): raise AssertionError('audited compiler emitted no test image')
shutil.copy2(image, evidence / 'audited-debug-native-suite')
headers = subprocess.run(['otool', '-l', str(image)], check=True, capture_output=True)
(evidence / 'audited-debug-otool.txt').write_bytes(headers.stdout)
signature = subprocess.run(['codesign', '-d', '--verbose=4', str(image)], capture_output=True)
(evidence / 'audited-debug-codesign.txt').write_bytes(signature.stdout + signature.stderr)
if result.returncode != 0: raise AssertionError('corrected audited compiler did not execute debug tests')
(evidence / 'debug-image-status.json').write_text(json.dumps(dict(returncode=result.returncode, compiler='09af0c8da66b4b01501efd6f7732a6b4e111fe81', profile='debug', opt=0, debug=True)))
with Path(os.environ['GITHUB_ENV']).open('a') as output:
    output.write('MACH_583_COMPILER=' + str(compiler / 'b') + '\n')
    output.write('MACH_583_PROFILE=debug\n')
