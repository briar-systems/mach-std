#!/usr/bin/env bash
# a deadline is a monotonic time.Instant. a wall-clock time.Time handed to any
# deadline surface must fail to build, which the in-process suite cannot show.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
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
[ "$code" -ne 0 ] || fail "a wall-clock Time was accepted as a deadline"
for call in 'cancel.make_root(scope' 'cancel.expire(scope, wall)' \
    'runtime.submit_timer(r, wall, 0)' 'time.remaining(wall)'; do
    grep -qF "$call" <<< "$log" \
        || { echo "$log" >&2; fail "no refusal at $call"; }
done
[ "$(grep -cE 'expected (opt\[)?Instant\]?, found (opt\[)?Time' <<< "$log")" = 4 ] \
    || { echo "$log" >&2; fail "a deadline refusal failed for the wrong reason"; }
echo "OK: a wall-clock Time is refused by every deadline surface"
