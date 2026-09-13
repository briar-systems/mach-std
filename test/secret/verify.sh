#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
root="$(cd "$here/../.." && pwd)"

fail() { echo "FAIL: $1" >&2; exit 1; }

rm -rf "$here/dep"
mkdir -p "$here/dep/std"
cp "$root/mach.toml" "$here/dep/std/mach.toml"
cp -R "$root/src" "$here/dep/std/src"

cd "$here"
set +e
log="$(mach_run build . 2>&1)"
code=$?
set -e
[ "$code" -ne 0 ] || fail "refusals unexpectedly erased secret-welded pointers"
echo "$log" | grep -q 'expected ptr, found \*\^u8' \
    || { echo "$log" >&2; fail "pointer erasure failed for the wrong reason"; }
echo "$log" | grep -q 'cannot add or drop the secret qualifier' \
    || { echo "$log" >&2; fail "integer erasure failed for the wrong reason"; }
echo "$log" | grep -q 'expected ptr, found \*SecretRecord' \
    || { echo "$log" >&2; fail "typed pointer erasure failed for the wrong reason"; }
[ "$(echo "$log" | grep -c 'cannot add or drop the secret qualifier')" = 2 ] \
    || { echo "$log" >&2; fail "borrow aliasing was not refused as a qualifier drop"; }
echo "$log" | grep -q 'ret key::\*u8' \
    || { echo "$log" >&2; fail "borrow aliasing was not refused"; }
echo "$log" | grep -q 'a secret-welded pointer cannot be erased to the untyped `ptr`' \
    || { echo "$log" >&2; fail "borrow holder erasure failed for the wrong reason"; }
echo "OK: byte and typed pointer erasures preserve secret storage boundaries"

# negative alias census (std #550): the welded file lane and the secret OS
# boundary offer no function that returns a public view of a borrow. every
# `pub fun` taking a `*^u8` or a `Borrow` must return an integer, a tag or
# nothing, never `*u8`, `ptr` or a record; and no signature in either module
# converts a welded pointer with `::`.
census_file() {
    local file="$1"
    local hits
    hits="$(grep -nE '^\s*pub fun [a-z_]+(\[[A-Z]\])?\([^)]*(\*\^u8|Borrow|SecretBorrow)[^)]*\)\s*(\*u8|ptr|\*[A-Z])' "$file" || true)"
    [ -z "$hits" ] || { echo "$hits" >&2; fail "$file offers a public view of a borrow"; }
    hits="$(grep -nE '[a-z_]+::\*u8|[a-z_]+::ptr' "$file" | grep -E 'secret|borrow|\^' || true)"
    [ -z "$hits" ] || { echo "$hits" >&2; fail "$file converts welded storage"; }
}
census_file "$root/src/system/os/secret.mach"
census_file "$root/src/io/file/adapter.mach"
census_file "$root/src/io/file.mach"
grep -qE '^pub fun submit_secret_read\(.*buffer: \*\^u8' "$root/src/io/file/adapter.mach" \
    || fail "the secret read lane does not take a welded borrow"
grep -qE '^pub fun submit_secret_write\(.*buffer: \*\^u8' "$root/src/io/file/adapter.mach" \
    || fail "the secret write lane does not take a welded borrow"
grep -qE '^pub fun borrow_(read|write)_at\(' "$root/src/system/os/secret.mach" \
    || fail "the positioned transfers left the secret OS boundary"
if grep -nE 'borrow_(read|write)_at' "$root/src" -r | grep -vE 'src/system/os/secret\.mach|src/system/os\.mach|src/io/file/adapter\.mach' | grep -q .; then
    grep -nE 'borrow_(read|write)_at' "$root/src" -r | grep -vE 'src/system/os/secret\.mach|src/system/os\.mach|src/io/file/adapter\.mach' >&2
    fail "a positioned secret transfer is issued outside the adapter"
fi
echo "OK: no public view of a welded borrow exists in the secret OS boundary or the file lane"
