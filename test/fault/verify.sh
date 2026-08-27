#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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

"$mach" build "$scratch/repo" -O2 --target "$target"
production="$scratch/repo/out/$target/debug/lib/std"
[ -f "$production" ] || fail "production archive was not built"
if ar t "$production" | grep -q '^fault\.'; then
    fail "test-only module entered the production archive"
fi

"$mach" dep pull "$scratch/repo/test/fault"
"$mach" build "$scratch/repo/test/fault" -O2 --target "$target"
explicit="$scratch/.mach-out/std-fault/$target/debug/lib/fault"
[ -f "$explicit" ] || fail "explicit fault archive was not built"

members="$(ar t "$explicit")"
for module in script reader writer allocator clock datagram race; do
    printf '%s\n' "$members" | grep -q "^fault\.$module$" \
        || fail "explicit fault archive omitted fault.$module"
done

echo "OK: production archive excludes the separate fault source root"
echo "OK: explicit fault artifact contains every deterministic facility"
