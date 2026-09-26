#!/usr/bin/env bash
# builds every std module for a freestanding target and holds the result to
# expected-pass.txt exactly: a listed module that stops building, a building
# module missing from the list, and a listed module that does not exist all fail
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
expected="$here/expected-pass.txt"
jobs="${FREESTANDING_JOBS:-$(nproc)}"
[ "$jobs" -gt 4 ] && jobs=4

fail() { echo "FAIL: $1" >&2; exit 1; }

[ -f "$expected" ] || fail "no expected-pass list at $expected"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/std" "$work/logs"
cp "$root/mach.toml" "$work/std/mach.toml"
cp -R "$root/src" "$work/std/src"

# depth one and two modules, lib/ excluded: lib is the artifact entry, not a module
(cd "$root/src" && find . -maxdepth 2 -name '*.mach' -not -path './lib/*') \
    | sed 's|^\./||; s|\.mach$||; s|/|.|g; s|^|std.|' | sort > "$work/modules.txt"

cat > "$work/mach.toml" <<'TOML'
[project]
id = "freestanding_probe"
version = "0.0.0"
mach = "^6"
src = "src"
out = "out/{target.name}/{profile.name}"

[target.freestanding-x86_64]
isa = "x86_64"
os = "freestanding"
abi = "sysv64"
of = "elf"

[profile.debug]
default = true
opt = 0
debug = false
simd = "scalarize"
vectorize = false
float_reassoc = false

[artifact.probe]
kind = "static"
entry = "probe.mach"
out = "lib/probe"
targets = ["*"]
link = []
need = []

[dep.std]
path = "dep/std"
TOML

probe() {
    local module="$1" dir="$work/runs/$1"
    mkdir -p "$dir/src" "$dir/dep"
    cp "$work/mach.toml" "$dir/mach.toml"
    # hard links keep dep/std a physical directory without copying std per module
    cp -al "$work/std" "$dir/dep/std"
    printf 'use m: %s;\n\npub fun probe() i64 {\n    ret 0;\n}\n' "$module" > "$dir/src/probe.mach"
    if (cd "$dir" && "$mach" build . --emit obj) > "$work/logs/$module.log" 2>&1; then
        echo "$module" > "$work/logs/$module.pass"
    fi
    rm -rf "$dir"
}
export -f probe
export work mach

xargs -P "$jobs" -I{} bash -c 'probe "$1"' _ {} < "$work/modules.txt"

cat "$work"/logs/*.pass 2>/dev/null | sort > "$work/actual.txt" || true
{ grep -vE '^[[:space:]]*(#|$)' "$expected" || true; } | sort > "$work/expected.txt"

status=0
while read -r module; do
    if ! grep -qxF "$module" "$work/modules.txt"; then
        echo "FAIL: $module is listed but is not a std module" >&2
        status=1
    elif ! grep -qxF "$module" "$work/actual.txt"; then
        echo "FAIL: $module no longer builds freestanding:" >&2
        grep -m 5 'error' "$work/logs/$module.log" | sed 's/^/    /' >&2 || true
        status=1
    fi
done < "$work/expected.txt"
while read -r module; do
    if ! grep -qxF "$module" "$work/expected.txt"; then
        echo "FAIL: $module now builds freestanding; add it to $(basename "$expected")" >&2
        status=1
    fi
done < "$work/actual.txt"

# a module that does not build refuses with exactly one diagnostic naming what
# it needs, so a freestanding user learns the missing capability from one line
while read -r module; do
    grep -qxF "$module" "$work/actual.txt" && continue
    log="$work/logs/$module.log"
    count="$(grep -cE '^error:' "$log" || true)"
    if [ "$count" != 1 ] || ! grep -qE '^error: .* needs ' "$log"; then
        echo "FAIL: $module refuses freestanding with $count diagnostics, not one naming what it needs:" >&2
        grep -m 5 -E '^error:' "$log" | sed 's/^/    /' >&2 || true
        status=1
    fi
done < "$work/modules.txt"

built="$(wc -l < "$work/actual.txt")"
total="$(wc -l < "$work/modules.txt")"
[ "$status" -eq 0 ] || exit "$status"
echo "OK: $built of $total std modules build freestanding-x86_64, matching $(basename "$expected"), and every other module refuses with one diagnostic"
