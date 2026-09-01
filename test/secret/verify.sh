#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"

fail() { echo "FAIL: $1" >&2; exit 1; }

mkdir -p "$here/dep"
ln -sfn "$root" "$here/dep/std"

cd "$here"
set +e
log="$("$mach" build . 2>&1)"
code=$?
set -e
[ "$code" -ne 0 ] || fail "refusals unexpectedly erased secret-welded pointers"
echo "$log" | grep -q 'expected ptr, found \*\^u8' \
    || { echo "$log" >&2; fail "pointer erasure failed for the wrong reason"; }
echo "$log" | grep -q 'cannot add or drop the secret qualifier' \
    || { echo "$log" >&2; fail "integer erasure failed for the wrong reason"; }
echo "$log" | grep -q 'expected ptr, found \*SecretRecord' \
    || { echo "$log" >&2; fail "typed pointer erasure failed for the wrong reason"; }
echo "OK: byte and typed pointer erasures preserve secret storage boundaries"
