#!/usr/bin/env bash
# every test std holds runs under some `mach test` selection, on every target
#
# mach 5.12 tests one artifact's closure (mach#3813), so a module no artifact
# reaches has its tests dropped without a word. this lists, per target, what an
# entry reaching every module with a test collects, and fails on any test that
# neither `mach test .` nor `mach test . --lib tests` collects.
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
root="$(cd "$here/../.." && pwd)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/mach-std-selections.XXXXXX")"
trap 'rm -rf -- "$scratch"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

repo="$scratch/repo"
mkdir -p "$repo"
cp "$root/mach.toml" "$repo/mach.toml"
cp -R "$root/src" "$repo/src"
python3 "$here/entry.py" "$repo/src" "$repo/src/lib/every_test.mach" "$scratch/modules.txt"
link="$(sed -n '/^\[artifact\.std\]/,/^\[/s/^link *= *//p' "$root/mach.toml")"
[ -n "$link" ] || fail "mach.toml has no link list for the std artifact"
printf '\n[artifact.every-test]\nkind = "static"\nentry = "lib/every_test.mach"\nout = "lib/every-test"\ntargets = ["*"]\nlink = %s\nneed = []\n' \
    "$link" >> "$repo/mach.toml"

targets="$(sed -n 's/^\[target\.\([^]]*\)\]$/\1/p' "$root/mach.toml")"
[ -n "$targets" ] || fail "mach.toml declares no targets"

list() {
    local out="$1"
    shift
    local listed
    listed="$(mach_run test "$repo" "$@" --list)" || fail "could not list: mach test $*"
    # each line is `<module>#<name> <test object>`, and the name alone identifies the test
    cut -d' ' -f1 <<< "$listed" > "$out"
}

: > "$scratch/reached.txt"
missing=0
for target in $targets; do
    list "$scratch/$target-std.txt" --target "$target"
    list "$scratch/$target-tests.txt" --lib tests --target "$target"
    list "$scratch/$target-every.txt" --lib every-test --target "$target"
    sort -u "$scratch/$target-std.txt" "$scratch/$target-tests.txt" > "$scratch/$target-union.txt"
    sort -u "$scratch/$target-every.txt" > "$scratch/$target-all.txt"
    sed -E 's|^std\.([^#]*)#.*$|\1|' "$scratch/$target-all.txt" | tr . / | sed 's|.*|src/&.mach|' >> "$scratch/reached.txt"
    dropped="$(comm -23 "$scratch/$target-all.txt" "$scratch/$target-union.txt")"
    printf '%s: std %d, tests %d, both %d of %d\n' "$target" \
        "$(wc -l < "$scratch/$target-std.txt")" "$(wc -l < "$scratch/$target-tests.txt")" \
        "$(wc -l < "$scratch/$target-union.txt")" "$(wc -l < "$scratch/$target-all.txt")"
    if [ -n "$dropped" ]; then
        echo "::error::$target collects tests that no selection runs; reach their modules from src/lib/tests.mach:"
        while IFS= read -r name; do printf '  %s\n' "$name"; done <<< "$dropped"
        missing=1
    fi
done

# a module that holds a test but that no target collects from is outside this check
unreached="$(comm -23 <(sort -u "$scratch/modules.txt") <(sort -u "$scratch/reached.txt"))"
if [ -n "$unreached" ]; then
    echo "::error::these modules hold tests that no target collects:"
    while IFS= read -r name; do printf '  %s\n' "$name"; done <<< "$unreached"
    missing=1
fi

[ "$missing" = 0 ] || exit 1
echo "OK: every test std holds runs under mach test . or mach test . --lib tests, on every target"
