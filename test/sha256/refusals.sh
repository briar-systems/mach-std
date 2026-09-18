#!/usr/bin/env bash
# the secret hash contract, pinned by a build that must fail: every function
# in refusals/src/refusals.mach breaks one line of the module doc, and each
# must be refused for its own reason. usage: refusals.sh <mach>
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/refusals"
source "$here/../../lib/compiler.sh"
root="$(cd "$here/../../.." && pwd)"

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
[ "$code" -ne 0 ] || fail "the secret hash refusals compiled"
expect() {
    grep -q "$1" <<< "$log" || { echo "$log" >&2; fail "$2"; }
}
expect 'expected \*\^u8, found \*u8' "update_secret or final_secret accepted a public pointer"
[ "$(grep -c 'expected \*\^u8, found \*u8' <<< "$log")" -ge 3 ] \
    || { echo "$log" >&2; fail "not every public-pointer call was refused (update_secret, final_secret, update_secret384)"; }
expect 'cannot add or drop the secret qualifier' "a State was cast to a SecretState"
expect 'a secret-welded pointer cannot be erased to the untyped `ptr`' "a record holding a SecretState erased to ptr"
echo "OK: the secret hash contract holds (public bytes, public digest, state aliasing, holder erasure all refused)"
