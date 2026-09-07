#!/usr/bin/env bash
# build and run the SIGPIPE suppression probe against this checkout's std.
# normal exit is part of the assertion: without the POSIX disposition change,
# the closed-reader write terminates the probe by SIGPIPE before main returns.
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
        10) echo "ignore_sigpipe setup failed" ;;
        11) echo "pipe creation failed" ;;
        12) echo "closing the read end failed" ;;
        13) echo "closing the write end failed" ;;
        20) echo "the protected write did not return EPIPE" ;;
        141) echo "the process was terminated by SIGPIPE" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

# copy this checkout into the fixture rather than relying on symlink behaviour
# under the native windows runner.
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the SIGPIPE probe with $mach (target $target)"
rm -rf out
mach_run build . --target "$target" --profile "$profile"
exe="$(find out -name 'sigpipe_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no sigpipe_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

echo "running $exe"
set +e
if [ -n "$runner" ]; then "$runner" "$exe"; else "$exe"; fi
code=$?
set -e
[ "$code" -eq 0 ] || fail "$(decode "$code")"

echo "OK: the protected broken-pipe write returned EPIPE and the process exited normally"
