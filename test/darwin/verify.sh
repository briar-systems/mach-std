#!/usr/bin/env bash
# run the suite natively on darwin and gate it against known-failures.txt.
#
# darwin carries a set of failures that predate the libSystem migration (#415);
# they are enumerated, with evidence, in known-failures.txt. this script exists
# so that set can be tolerated WITHOUT tolerating anything else:
#
#   - a failure that is not on the list fails the build (a regression)
#   - a listed test that PASSES fails the build (the list has gone stale and
#     must shrink)
#
# both directions matter. only checking the first turns the list into a mute
# button that silently outlives the bugs it describes.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
set -uo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
cd "$root"

known="$here/known-failures.txt"

# strip comments and blank lines
expected="$(grep -vE '^[[:space:]]*(#|$)' "$known" | sed 's/[[:space:]]*$//' | sort -u)"

out="$(mktemp)"
"$mach" test . 2>&1 | tee "$out"

if ! grep -qE '[0-9]+ passed, [0-9]+ failed' "$out"; then
    echo "::error::the suite produced no result line -- it did not run to completion"
    exit 1
fi

# "  FAIL  <name>  <relative-path>:NN  (exit 1)" -> "<name>"
actual="$(sed -n 's/^[[:space:]]*FAIL[[:space:]]\{1,\}\([^[:space:]]*\)[[:space:]]\{2,\}[^[:space:]]*[[:space:]]*(exit [0-9]*)[[:space:]]*$/\1/p' "$out" \
          | sed 's/[[:space:]]*$//' | sort -u)"

rc=0

unexpected="$(comm -13 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual"))"
if [ -n "$unexpected" ]; then
    echo "::error::darwin test failures that are NOT known-pre-existing:"
    printf '  %s\n' $unexpected
    rc=1
fi

fixed="$(comm -23 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual"))"
if [ -n "$fixed" ]; then
    echo "::error::these are listed in known-failures.txt but PASSED -- remove them from the list:"
    printf '  %s\n' $fixed
    rc=1
fi

if [ "$rc" = "0" ]; then
    n="$(printf '%s\n' "$expected" | grep -c . || true)"
    echo "OK: no new darwin failures; $n known pre-existing failures still outstanding (#415)"
fi

rm -f "$out"
exit "$rc"
