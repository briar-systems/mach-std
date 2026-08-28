#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
known="${3:-$here/known-failures/$target.txt}"
root="$(cd "$here/../.." && pwd)"
result="$here/results/$target.log"

fail() { echo "FAIL: $1" >&2; exit 1; }

[ -f "$known" ] || fail "$target has no known-failure policy at $known"
grep -qE '^# owner: .+' "$known" || fail "$known has no owner"
grep -qE '^# baseline: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$known" \
    || fail "$known has no baseline date"

rm -rf "$here/dep"
mkdir -p "$here/dep/std" "$here/results"
cp "$root/mach.toml" "$here/dep/std/mach.toml"
cp -R "$root/src" "$here/dep/std/src"

cd "$here"

list="$here/results/$target-list.txt"
expected_file="$(mktemp)"
actual_file="$(mktemp)"
trap 'rm -f "$expected_file" "$actual_file"' EXIT

"$mach" test . --target "$target" --include-deps --list \
    | tr '\134' '/' > "$list" \
    || fail "$target suite could not be listed"

required=(
    'src/sync/thread.mach'
    'src/process/exec.mach'
    'src/filesystem.mach'
    'src/io/file/tests.mach'
    'src/io/runtime.mach'
    'src/net/tcp.mach'
    'src/net/udp.mach'
    'src/net/local.mach'
    'src/net/async.mach'
    'src/net/async/local.mach'
    'src/chrono/time.mach'
    'src/sync/channel.mach'
    'src/sync/worker_pool.mach'
)
for source in "${required[@]}"; do
    grep -qF "$source" "$list" || fail "$target omitted required tests from $source"
done

{ grep -vE '^[[:space:]]*(#|$)' "$known" || true; } \
    | sed 's/[[:space:]]*$//' | sort -u > "$expected_file"

set +e
"$mach" test . --target "$target" --include-deps 2>&1 | tee "$result"
code=${PIPESTATUS[0]}
set -e

[ "$code" -le 1 ] || fail "$target suite did not run to completion (exit $code)"

summary="$(grep -E '[0-9]+ passed, [0-9]+ failed, [0-9]+ total' "$result" | tail -1)"
[ -n "$summary" ] || fail "$target suite produced no result line"

failed="$(printf '%s\n' "$summary" \
    | sed -n 's/.* passed, \([0-9][0-9]*\) failed,.*/\1/p')"
[ -n "$failed" ] || fail "$target suite result could not be parsed"

sed -n 's/^[[:space:]]*FAIL[[:space:]]\{1,\}\(.*\)[[:space:]]\{2,\}[^[:space:]]*:[0-9][0-9]*[[:space:]]*(.*)[[:space:]]*$/\1/p' "$result" \
    | sed 's/[[:space:]]*$//' | sort -u > "$actual_file"

actual_count="$(wc -l < "$actual_file" | tr -d '[:space:]')"
[ "$actual_count" = "$failed" ] \
    || fail "$target reported $failed failures but $actual_count failure names were parsed"

unexpected="$(comm -13 "$expected_file" "$actual_file")"
if [ -n "$unexpected" ]; then
    echo "::error::$target has failures outside its known-failure policy:"
    while IFS= read -r name; do printf '  %s\n' "$name"; done <<< "$unexpected"
    exit 1
fi

fixed="$(comm -23 "$expected_file" "$actual_file")"
if [ -n "$fixed" ]; then
    echo "::error::$target has known failures that passed and must be removed:"
    while IFS= read -r name; do printf '  %s\n' "$name"; done <<< "$fixed"
    exit 1
fi

expected_count="$(wc -l < "$expected_file" | tr -d '[:space:]')"
echo "OK: $target ran the complete native suite with $expected_count known failures"
echo "OK: thread, process, file, socket, and timer coverage is present"

release_result="$here/results/$target-ownership-release.log"
"$mach" test . --target "$target" --profile release --include-deps \
    --filter 'ownership query' 2>&1 | tee "$release_result" \
    || fail "$target release ownership suite failed"
grep -qE '[0-9]+ passed, 0 failed, [0-9]+ total' "$release_result" \
    || fail "$target release ownership suite produced no clean result"
echo "OK: $target release ownership tests passed"
