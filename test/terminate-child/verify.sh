#!/usr/bin/env bash
# build and run the tracked-child force-termination probe against this checkout.
#
# usage: verify.sh [path-to-mach] [target] [runner]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        10|11) echo "failed to spawn blocking child $(( $1 - 9 ))" ;;
        20) echo "high-level terminate_child failed" ;;
        21) echo "terminating the first child disturbed the second" ;;
        22|23) echo "the terminated first child was not waitable with force-stop status" ;;
        24) echo "an already-reaped child was not ECHILD" ;;
        25) echo "an unknown child was not ECHILD" ;;
        26) echo "the unknown-child operation disturbed the second child" ;;
        27) echo "low-level terminate_child failed" ;;
        28|29) echo "the terminated second child was not waitable with force-stop status" ;;
        30) echo "failed to spawn after earlier terminate/reap cycles" ;;
        31) echo "repeated terminate/reap cycle failed" ;;
        32) echo "an invalid child PID was not EINVAL" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

# copy this checkout rather than relying on symlink behaviour on Windows.
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the terminate-child probe with $mach (target $target)"
rm -rf out
"$mach" build . --target "$target" --profile debug
exe="$(find out -name 'terminate_child_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no terminate_child_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

echo "running $exe"
set +e
if [ -n "$runner" ]; then "$runner" "$exe"; else "$exe"; fi
code=$?
set -e
[ "$code" -eq 0 ] || fail "$(decode "$code")"

echo "OK: force-stop is exact, non-reaping, repeatable, and rejects stale children"
