#!/usr/bin/env bash
# cross-compile the riscv64-linux runtime smoke test against this checkout's std
# and run it under qemu-riscv64, asserting its exit code. proves the riscv64
# runtime (_start + the syscall stubs) links and runs end to end.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
#
# requires: qemu-riscv64 (or qemu-riscv64-static).
set -euo pipefail

# the exit code main returns; the qemu run asserts it.
expect_code=42

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

# copy the dependency inside the fixture project
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -R ../../src dep/std/src

echo "cross-compiling the riscv64 runtime smoke test with $mach"
rm -rf out
mach_run build . --target linux-riscv64 --profile debug
exe="$(find out -name rvprobe -type f -print -quit)"
[ -n "$exe" ] || fail "no rvprobe binary produced"

echo "running $exe under qemu-riscv64"
qemu="$(command -v qemu-riscv64 || command -v qemu-riscv64-static || true)"
[ -n "$qemu" ] || fail "qemu-riscv64 not found"
set +e
"$qemu" "$exe"
code=$?
set -e
[ "$code" -eq "$expect_code" ] || fail "exit code $code, expected $expect_code"

echo "OK: riscv64-linux runtime reaches main and exits $expect_code"
