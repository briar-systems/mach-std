#!/usr/bin/env bash
# build and run the process completion probe against this checkout: a native
# C child supplies exit values, signals and a stop; the mach parent checks
# run, output, wait_any and the typed exec.Error surface.
#
# usage: verify.sh [path-to-mach] [target] [runner]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
profile=debug
case "$target" in windows-*) profile=windows-opt0 ;; esac
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        2) echo "the probe was not given the native child path" ;;
        10) echo "run failed" ;;
        11) echo "run reported the wrong exit value" ;;
        12) echo "output failed" ;;
        13) echo "the captured output could not be released" ;;
        14) echo "output reported the wrong exit value or captured bytes" ;;
        15|16) echo "failed to spawn the wait_any children" ;;
        17) echo "wait_any failed" ;;
        18) echo "wait_any reaped an unexpected child or status" ;;
        19) echo "a no-child probe consumed or disturbed the status output" ;;
        20) echo "the signalled child could not be run" ;;
        21) echo "signal termination was not observed as such" ;;
        22) echo "the stopped child could not be spawned" ;;
        23|24) echo "the stop was not observed as a non-consuming stopped state" ;;
        25) echo "a no-event probe consumed or disturbed the stopped child" ;;
        26) echo "the stopped child could not be terminated" ;;
        27|28) echo "the terminated child did not reap with the kill signal" ;;
        30|31|32) echo "wait_any with no children was not the native ECHILD without a retained child" ;;
        94|95|96|97|98) echo "the native child rejected its arguments (exit $1)" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

# copy this checkout rather than relying on symlink behaviour on Windows.
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

cc="${CC:-cc}"
child="$here/out/native-child"
case "$target" in windows-*) child="$child.exe" ;; esac
mkdir -p out
echo "building the native child with $cc"
"$cc" -O1 -o "$child" native-child.c

echo "building the process-status probe with $mach (target $target)"
rm -rf "out/$target"
mach_run build . --target "$target" --profile "$profile"
exe="$(find out -name 'process_status_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no process_status_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

echo "running $exe $child"
set +e
if [ -n "$runner" ]; then "$runner" "$exe" "$child"; else "$exe" "$child"; fi
code=$?
set -e
[ "$code" -eq 0 ] || fail "$(decode "$code")"

echo "OK: complete exit values, signal and stop observations, and typed wait ownership hold"
