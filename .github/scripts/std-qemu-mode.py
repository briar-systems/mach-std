from pathlib import Path
import subprocess

evidence = Path('std-qemu-evidence')
evidence.mkdir()

def run(label, args, **kwargs):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    (evidence / (label + '.log')).write_bytes(result.stdout)
    print(label, result.returncode, result.stdout.decode(errors='replace'), flush=True)
    result.check_returncode()

run('native-build', ['gcc', '-Wall', '-Wextra', '-Werror', '.github/scripts/std-qemu-mode.c', '-o', str(evidence / 'native')])
run('riscv-build', ['riscv64-linux-gnu-gcc', '-static', '-Wall', '-Wextra', '-Werror', '.github/scripts/std-qemu-mode.c', '-o', str(evidence / 'riscv')])
run('native', [str((evidence / 'native').resolve())])
run('old-version', ['qemu-riscv64', '--version'])
run('old-syscall', ['qemu-riscv64', '-strace', str(evidence / 'riscv'), 'enosys'])
run('clone', ['git', 'clone', '--depth', '1', '--branch', 'v10.1.0', 'https://github.com/qemu/qemu', '.qemu-mode'])
actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd='.qemu-mode', text=True).strip()
assert actual == 'f8b2f64e2336a28bf0d50b6ef8a7d8c013e9bcf3', actual
(evidence / 'qemu-source.txt').write_text(actual + '\n')
run('configure', ['./configure', '--target-list=riscv64-linux-user', '--disable-system', '--disable-docs', '--disable-tools', '--disable-guest-agent'], cwd='.qemu-mode', timeout=600)
run('build', ['make', '-j2'], cwd='.qemu-mode', timeout=900)
run('new-version', ['.qemu-mode/build/qemu-riscv64', '--version'])
run('new-syscall', ['.qemu-mode/build/qemu-riscv64', '-strace', str(evidence / 'riscv')])
