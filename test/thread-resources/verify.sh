#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"

rm -rf "$here/dep"
mkdir -p "$here/dep/std"
cp "$root/mach.toml" "$here/dep/std/mach.toml"
cp -R "$root/src" "$here/dep/std/src"

args=(test "$here" --target "$target")
if [ -n "$runner" ]; then args+=(--runner "$runner"); fi
"$mach" "${args[@]}"
