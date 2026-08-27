#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"

if rg -n 'failure_stage|THREAD_SPAWN_FAIL|thread_resource_count' "$root/src"; then
    echo "FAIL: production source contains thread test controls or resource probes" >&2
    exit 1
fi

rm -rf "$here/dep"
mkdir -p "$here/dep/std"
cp "$root/mach.toml" "$here/dep/std/mach.toml"
cp -R "$root/src" "$here/dep/std/src"

"$mach" build "$here" --target "$target" -O2
out="$(cd "$here/../../.." && pwd)/.mach-out/thread-resources/$target"
artifact="$(find "$out" -type f -path '*/bin/thread-resources' | head -1)"
object="$(find "$out" -type f -path '*/obj/std/system/os.o' | head -1)"
if [ -z "$artifact" ] || [ -z "$object" ]; then
    echo "FAIL: optimized artifact or OS object not found" >&2
    exit 1
fi
if { strings "$artifact"; strings "$object"; } \
    | grep -qE 'injected failure releases|native name failure aborts|test_map_hex_digit|test_name_worker|test_thread_mapped_bytes|test_thread_resources'; then
    echo "FAIL: thread fixture code entered the optimized artifact" >&2
    exit 1
fi
echo "OK: optimized thread artifact excludes test controls and probes"
