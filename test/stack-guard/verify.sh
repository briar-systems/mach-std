#!/usr/bin/env bash
# build and run the spawned-thread stack overflow probe against this checkout's
# std. the probe's thread recurses past the bottom of its stack, and the process
# must die by the OS's stack fault: SIGSEGV on linux, SIGSEGV or SIGBUS on darwin,
# STATUS_STACK_OVERFLOW on windows. a normal exit means the overflow ran on.
#
# usage: verify.sh [path-to-mach] [target] [runner]
set -euo pipefail

# the probe dies by signal; keep its core dump out of the working tree
ulimit -c 0 2>/dev/null || true

mach="${1:-mach}"
target="${2:-linux-x86_64}"
profile=debug
case "$target" in windows-*) profile=windows-opt0 ;; esac
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the stack guard probe with $mach (target $target)"
rm -rf out
mach_run build . --target "$target" --profile "$profile"
exe="$(find out -name 'stack_guard_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no stack_guard_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

echo "running $exe"
set +e
if [ -n "$runner" ]; then "$runner" "$exe"; else "$exe"; fi
code=$?
set -e

case "$code" in
    0 | 1) fail "the thread ran past the bottom of its stack without faulting (exit $code)" ;;
    2) fail "the thread could not be spawned or joined" ;;
    3) fail "the victim region below the guard could not be mapped" ;;
    4) fail "the thread's stack bounds are unknown" ;;
esac
case "$target" in
    linux-*) expected="139" ;;          # SIGSEGV
    darwin-*) expected="138 139" ;;     # SIGBUS or SIGSEGV
    windows-*) expected="253" ;;        # STATUS_STACK_OVERFLOW, 0xC00000FD, low byte
esac
for e in $expected; do
    if [ "$code" -eq "$e" ]; then
        echo "OK: the overflowing thread died by the stack fault (exit $code)"
        exit 0
    fi
done
fail "exit $code, expected one of: $expected"
