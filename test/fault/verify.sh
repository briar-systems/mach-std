#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
profile=debug
case "$target" in windows-*) profile=windows-opt0 ;; esac
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
root="$(cd "$here/../.." && pwd)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/mach-std-fault.XXXXXX")"
trap 'rm -rf -- "$scratch"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# the production compiler source root cannot resolve the test-only project
case "$here/src/" in
    "$root/src/"*) fail "fault sources overlap the production source root" ;;
esac

mkdir -p "$scratch/repo/test/fault"
cp "$root/mach.toml" "$scratch/repo/mach.toml"
cp -R "$root/src" "$scratch/repo/src"
cp "$here/mach.toml" "$scratch/repo/test/fault/mach.toml"
cp -R "$here/src" "$scratch/repo/test/fault/src"
mkdir -p "$scratch/repo/test/fault/dep/std"
cp "$root/mach.toml" "$scratch/repo/test/fault/dep/std/mach.toml"
cp -R "$root/src" "$scratch/repo/test/fault/dep/std/src"
git init --quiet "$scratch/repo"
git -C "$scratch/repo" add -f mach.toml src test/fault

release_checked=0
if grep -qF "[target.$target]" "$scratch/repo/mach.toml"; then
    mach_run build "$scratch/repo" -O2 --target "$target"
    production="$scratch/repo/out/$target/debug/lib/std"
    bash "$here/verify-release.sh" "$production"
    release_checked=1
fi

test_args=(test "$scratch/repo/test/fault" --target "$target" --profile "$profile")
if [ -n "$runner" ]; then
    test_args+=(--runner "$runner")
fi
mach_run "${test_args[@]}"
mach_run "${test_args[@]}" -O2
mach_run build "$scratch/repo/test/fault" -O2 --target "$target" --profile "$profile"
explicit="$scratch/repo/test/fault/out/$target/$profile/lib/fault"
[ -f "$explicit" ] || fail "explicit fault archive was not built"

members="$("${AR:-ar}" t "$explicit")"
normalized_members="$(printf '%s\n' "$members" \
    | tr '\\' '/' \
    | sed -E 's#/$##; s#^.*/##; s#[.]o$##; s#[[:space:]]+$##')"
for module in script reader writer allocator clock datagram race; do
    if ! grep -Fxq "fault.$module" <<< "$normalized_members"; then
        printf '%s\n' "$members" >&2
        fail "explicit fault archive omitted fault.$module"
    fi
done

if [ "$release_checked" = 1 ]; then
    echo "OK: production archive excludes the separate fault source root"
else
    echo "OK: $target has no production release artifact to inspect"
fi
echo "OK: deterministic fault tests pass in debug and optimized modes"
echo "OK: explicit fault artifact contains every deterministic facility"
