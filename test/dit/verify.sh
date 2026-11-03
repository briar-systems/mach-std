#!/usr/bin/env bash
# the aarch64 data-independent-timing mode, end to end: std publishes
# `__mach_timing_available` from the processor before main, std.system.timing
# answers from it, and nothing turns PSTATE.DIT on at start or per thread, so
# outside a soft constant-time function the mode is off on the main thread and
# on a thread std spawned. a program with a soft function computes through it
# and finds the mode off again after it returns. qemu-aarch64 -cpu cortex-a57
# models a processor without the mode wherever qemu is on the path. no case
# refuses to start.
#
# usage: verify.sh <mach> <target> [runner]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-aarch64}"
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        1) echo "the main thread's PSTATE.DIT is on outside a constant-time function" ;;
        2) echo "thread spawn failed" ;;
        3) echo "thread join failed" ;;
        4) echo "the spawned thread's PSTATE.DIT is on outside a constant-time function" ;;
        10) echo "__mach_timing_available does not match what the OS reports" ;;
        11) echo "the secret multiply computed a wrong product" ;;
        12) echo "std.system.timing does not answer from the availability byte" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

"$mach" dep pull . --quiet

echo "building the dit probes with $mach (target $target)"
rm -rf out
mach_run build . --target "$target"
secret="$(find out -name 'secret' -type f -print -quit)"
plain="$(find out -name 'plain' -type f -print -quit)"
[ -n "$secret" ] && [ -n "$plain" ] || fail "no probe binaries produced"

run() {
    set +e
    if [ -n "$runner" ]; then $runner "$1"; else "$1"; fi
    code=$?
    set -e
    echo "$code"
}

code="$(run "$secret")"
[ "$code" -eq 0 ] || fail "secret: $(decode "$code")"
echo "OK: a soft constant-time function runs and leaves PSTATE.DIT off behind it on every thread"

code="$(run "$plain")"
[ "$code" -eq 0 ] || fail "plain: $(decode "$code")"
echo "OK: a program without one runs with PSTATE.DIT off"

if [ "$target" = linux-aarch64 ] && command -v qemu-aarch64 >/dev/null; then
    runner="qemu-aarch64 -cpu cortex-a57"
    code="$(run "$secret")"
    [ "$code" -eq 0 ] || fail "secret under $runner: $(decode "$code")"
    echo "OK: under $runner a soft constant-time function runs without the mode"
fi
