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
profiles=(debug release)

for target in "${targets[@]}"; do
    rm -rf "out/$target"
    for profile in "${profiles[@]}"; do
        echo "cross-compiling the $profile backend smoke test for $target with $mach"
        log="$("$mach" build . --target "$target" --profile "$profile" \
            --emit-ir --emit-asm --verify-ir -vv 2>&1)" \
            || { echo "$log" >&2; fail "$target $profile failed to compile"; }

        exe="$(find "out/$target/$profile" -name backends -type f -print -quit)"
        [ -n "$exe" ] || fail "$target $profile: no backends binary produced"

        # confirm the backend's shared module was actually compiled
        echo "$log" | grep -q "skipped .* target-gated modules" \
            && fail "$target $profile: target-gated modules were skipped"
        echo "$log" | grep -q "std.system.os.${target%%-*}.shared" \
            || fail "$target $profile: os backend was never compiled"
        echo "$log" | grep -q "std.net.async.${target%%-*}" \
            || fail "$target $profile: network backend was never compiled"

        echo "OK: $target $profile backends compile ($exe)"
    done
done
