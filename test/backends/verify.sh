#!/usr/bin/env bash
# cross-compile a program that references std.system.os (and, through it,
# std.runtime) for the windows and darwin targets, against this checkout's
# std. proves the target-gated backend modules actually compile instead of
# being skipped as dead $if branches -- see #426. compile only; nothing here
# is run.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

# vendor this checkout's std as the path dependency (dep/std -> repo root).
mkdir -p dep
ln -sfn "$(cd ../.. && pwd)" dep/std

targets=(windows-x86_64 darwin-x86_64 darwin-aarch64)

for target in "${targets[@]}"; do
    echo "cross-compiling the backend smoke test for $target with $mach"
    rm -rf "out/$target"
    log="$("$mach" build . --target "$target" --profile debug -vv 2>&1)" \
        || { echo "$log" >&2; fail "$target failed to compile"; }

    exe="$(find "out/$target" -name backends -type f -print -quit)"
    [ -n "$exe" ] || fail "$target: no backends binary produced"

    # confirm the backend's shared module was actually compiled, not skipped
    # as a target-gated dead branch.
    echo "$log" | grep -q "skipped .* target-gated modules" \
        && fail "$target: target-gated modules were skipped"
    echo "$log" | grep -q "std.system.os.${target%%-*}.shared" \
        || fail "$target: std.system.os.${target%%-*}.shared was never compiled"

    echo "OK: $target backend compiles ($exe)"
done
