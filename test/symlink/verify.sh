#!/usr/bin/env bash
# build and run the relative-target directory symlink probe against this
# checkout's std, on the host. see src/main.mach for what it asserts.
#
# this runs on the host because the property is a filesystem fact, not a
# codegen one: the link has to be created by a real kernel and traversed by a
# real kernel. wine cannot stand in for windows here, its filesystem is
# unix-backed so it creates a genuine unix symlink and reports a false pass on
# precisely this bug (#454).
#
# usage: verify.sh [path-to-mach] [target] [runner]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux}"
profile=debug
case "$target" in windows-*) profile=windows-opt0 ;; esac
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        10|11|12|13) echo "setting up the probe tree failed (code $1)" ;;
        20|30) echo "fs.symlink reported an error (code $1)" ;;
        21|31) echo "the link does not report as a symlink (code $1)" ;;
        22|32) echo "the link is not traversable as a directory: fs.is_dir is false (code $1)" ;;
        23|33) echo "opening a file THROUGH the link failed (code $1)" ;;
        24|25|26|34|35|36) echo "reading through the link returned the wrong bytes (code $1)" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

# vendor this checkout's std by copying rather than by the `dep/std -> repo root`
# symlink the other probes use. a probe for symlinks must not need a working
# symlink to set itself up, and on a windows host `ln -s` under msys silently
# produces a copy anyway.
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the symlink probe with $mach (target $target)"
rm -rf out work
mach_run build . --target "$target" --profile "$profile"
exe="$(find out -name 'symlink_probe*' -type f -print -quit)"
[ -n "$exe" ] || fail "no symlink_probe binary produced"
exe="$(cd "$(dirname "$exe")" && pwd)/$(basename "$exe")"

mkdir -p work
echo "running $exe in a scratch tree"
set +e
if [ -n "$runner" ]; then (cd work && "$runner" "$exe"); else (cd work && "$exe"); fi
code=$?
set -e
[ "$code" -eq 0 ] || fail "$(decode "$code")"

echo "OK: a relative, /-separated directory symlink is traversable and reads through"
