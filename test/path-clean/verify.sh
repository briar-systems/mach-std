#!/usr/bin/env bash
# build and run the portable lexical path-cleaning probe against this checkout.
#
# usage: verify.sh [path-to-mach] [target]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        10) echo "repeated separator/dot collapse failed" ;;
        11|12) echo "relative dotdot preservation failed" ;;
        13|14) echo "empty normalized result was not dot" ;;
        20|21) echo "windows drive-root normalization failed" ;;
        22|23) echo "windows drive-relative normalization failed" ;;
        24) echo "windows drive root did not clamp dotdot" ;;
        25|26|27) echo "windows UNC root normalization failed" ;;
        28) echo "windows rooted path did not clamp dotdot" ;;
        30|31) echo "posix root normalization failed" ;;
        32) echo "posix treated backslash as a separator" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

# copy this checkout rather than relying on symlink behaviour on Windows.
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the path-clean probe with $mach (target $target)"
rm -rf out
"$mach" build . --target "$target" --profile debug
exe="$(find out -name 'path_clean_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no path_clean_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

echo "running $exe"
set +e
"$exe"
code=$?
set -e
[ "$code" -eq 0 ] || fail "$(decode "$code")"

echo "OK: lexical cleaning preserves native roots and resolves safe segments"
