#!/usr/bin/env bash
# who owns the thread pointer (#915): a static image, where std owns it, and a
# dynamic image, where the loader owns the main thread's and C code creates
# threads that call back into mach. every cell checks current_token on each
# thread it runs: direct, stable, and distinct among the threads live at once.
#
# usage: verify.sh [path-to-mach] [target] [runner]
#   CC builds the C fixture for the target (default cc). under a qemu runner,
#   QEMU_LD_PREFIX names the target's sysroot, as qemu-user reads it.
set -euo pipefail
ulimit -c 0 2>/dev/null || true

mach="${1:-mach}"
target="${2:-linux-x86_64}"
runner="${3:-}"
cc="${CC:-cc}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

rm -rf dep out c/out
mkdir -p dep/std c/out
cp ../../mach.toml dep/std/mach.toml
cp -R ../../src dep/std/src

# the fixture is C, so it is built by a C compiler and linked by pthread_create's owner
$cc -shared -fPIC -O1 -Wl,-soname,libprobe.so -o c/out/libprobe.so c/probe.c -lpthread

mach_run build . --bin static --target "$target" --profile debug
mach_run build . --bin dynamic --target "$target" --profile debug
static="$(find out -name static -type f -print -quit)"
dynamic="$(find out -name dynamic -type f -print -quit)"

run() {
    if [ -n "$runner" ]; then "$runner" -E "LD_LIBRARY_PATH=$here/c/out" "$@"
    else LD_LIBRARY_PATH="$here/c/out" "$@"; fi
}

failed=0
cell() {
    local name="$1"; shift
    set +e
    run "$@"
    local code=$?
    set -e
    if [ "$code" -eq 0 ]; then echo "PASS $target $name"
    else echo "FAIL $target $name: exit $code"; failed=1; fi
}

cell static            "$static"
cell dynamic-std-threads "$dynamic" spawn
cell loader-main       "$dynamic" main
cell c-thread-callback "$dynamic" cthread
exit "$failed"
