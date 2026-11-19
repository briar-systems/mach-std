#!/usr/bin/env bash
# read std's secret boundary for a public view of a welded borrow. it builds nothing: the
# compiler's refusals of such views are checked by the compiler's own test corpus.
#
# usage: verify.sh
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"

fail() { echo "FAIL: $1" >&2; exit 1; }

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
