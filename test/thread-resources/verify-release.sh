#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/mach-std-thread-release.XXXXXX")"
trap 'rm -rf -- "$scratch"' EXIT

if grep -REn 'failure_stage|THREAD_SPAWN_FAIL|thread_resource_count' "$root/src"; then
    echo "FAIL: production source contains thread test controls or resource probes" >&2
    exit 1
fi

fixture="$scratch/repo/test/thread-resources"
mkdir -p "$fixture/src" "$fixture/dep/std"
cp "$here/mach.toml" "$fixture/mach.toml"
cp -R "$here/src/." "$fixture/src"
cp "$root/mach.toml" "$fixture/dep/std/mach.toml"
cp -R "$root/src" "$fixture/dep/std/src"

"$mach" build "$fixture" --target "$target" -O2
out="$scratch/.mach-out/thread-resources/$target"
artifact="$(find "$out" -type f -path '*/bin/thread-resources' | head -1)"
object="$(find "$out" -type f -path '*/obj/std/system/os.o' | head -1)"
if [ -z "$artifact" ] || [ -z "$object" ]; then
    echo "FAIL: optimized artifact or OS object not found" >&2
    exit 1
fi
matches="$({ strings "$artifact"; strings "$object"; } \
    | grep -E 'injected .* failure|native (name|setup) failure aborts|test_map_hex_digit|test_name_worker|test_thread_mapped_bytes|test_thread_resources' || true)"
if [ -n "$matches" ]; then
    printf '%s\n' "$matches" >&2
    echo "FAIL: thread fixture code entered the optimized artifact" >&2
    exit 1
fi
echo "OK: optimized thread artifact excludes test controls and probes"
