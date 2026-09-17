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
grep -q 'expected ptr, found \*\^u8' <<< "$log" \
    || { echo "$log" >&2; fail "pointer erasure failed for the wrong reason"; }
grep -q 'cannot add or drop the secret qualifier' <<< "$log" \
    || { echo "$log" >&2; fail "integer erasure failed for the wrong reason"; }
grep -q 'expected ptr, found \*SecretRecord' <<< "$log" \
    || { echo "$log" >&2; fail "typed pointer erasure failed for the wrong reason"; }
[ "$(echo "$log" | grep -c 'cannot add or drop the secret qualifier')" = 2 ] \
    || { echo "$log" >&2; fail "borrow aliasing was not refused as a qualifier drop"; }
grep -q 'ret key::\*u8' <<< "$log" \
    || { echo "$log" >&2; fail "borrow aliasing was not refused"; }
grep -q 'a secret-welded pointer cannot be erased to the untyped `ptr`' <<< "$log" \
    || { echo "$log" >&2; fail "borrow holder erasure failed for the wrong reason"; }
echo "OK: byte and typed pointer erasures preserve secret storage boundaries"

# negative alias census (std #550): the secret primitives, the welded storage
# module and the file lane offer no function that returns a public view of a
# borrow. every `pub fun` taking a `*^u8` or a `Borrow` must return an integer,
# a tag or nothing, never `*u8`, `ptr` or a record, and no signature in these
# modules converts a welded pointer with `::`.
census_file() {
    local file="$1"
    local hits
    hits="$(grep -nE '^\s*pub fun [a-z_]+(\[[A-Z]\])?\([^)]*(\*\^u8|Borrow)[^)]*\)\s*(\*u8|ptr|\*[A-Z])' "$file" || true)"
    [ -z "$hits" ] || { echo "$hits" >&2; fail "$file offers a public view of a borrow"; }
    hits="$(grep -nE '[a-z_]+::\*u8|[a-z_]+::ptr' "$file" | grep -E 'secret|borrow|\^' || true)"
    [ -z "$hits" ] || { echo "$hits" >&2; fail "$file converts welded storage"; }
}
census_file "$root/src/system/os/secret.mach"
census_file "$root/src/memory/secret.mach"
census_file "$root/src/io/file/adapter.mach"
census_file "$root/src/io/file.mach"
grep -qE '^pub fun submit_secret_read\(.*buffer: \*\^u8' "$root/src/io/file/adapter.mach" \
    || fail "the secret read lane does not take a welded borrow"
grep -qE '^pub fun submit_secret_write\(.*buffer: \*\^u8' "$root/src/io/file/adapter.mach" \
    || fail "the secret write lane does not take a welded borrow"
grep -qE '^pub fun borrow_(read|write)_at\(' "$root/src/memory/secret.mach" \
    || fail "the positioned borrow transfers left std.memory.secret"
grep -qE '^pub fun (read|write)_at_secret\(' "$root/src/system/os.mach" \
    || fail "the positioned secret primitives left the os contract"
allowed='src/memory/secret\.mach|src/io/file/adapter\.mach'
if grep -nE 'borrow_(read|write)_at' "$root/src" -r | grep -vE "$allowed" | grep -q .; then
    grep -nE 'borrow_(read|write)_at' "$root/src" -r | grep -vE "$allowed" >&2
    fail "a positioned secret transfer is issued outside the adapter"
fi
native='src/system/os\.mach|src/memory/secret\.mach'
if grep -nE '(read|write)_at_secret' "$root/src" -r | grep -vE "$native" | grep -q .; then
    grep -nE '(read|write)_at_secret' "$root/src" -r | grep -vE "$native" >&2
    fail "a native secret transfer is issued outside std.memory.secret"
fi
echo "OK: no public view of a welded borrow exists in the secret OS boundary or the file lane"
