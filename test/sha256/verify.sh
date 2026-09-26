#!/usr/bin/env bash
# runs the sha256 benchmark at -O2 and prints its ns/byte lines, then checks
# that the dispatcher's choice agrees with what the operating system says
# about the processor. usage: verify.sh <mach> <target> [runner]
set -euo pipefail
mach="$1" target="$2" runner="${3:-}"
args=(test . --target "$target" -O2 -vv --filter "sha256_benchmark")
[ -n "$runner" ] && args+=(--runner "$runner")
out="$("$mach" "${args[@]}" 2>&1)"
echo "$out" | grep -E "sha256 bench" || { echo "$out"; echo "FAIL: no benchmark output"; exit 1; }
accelerated="$(echo "$out" | sed -n 's/.*accelerated=\([01]\).*/\1/p' | head -1)"

# the OS's own view of the extension, where this script runs on that host
expected=""
case "$target" in
    linux-x86_64)
        grep -qw sha_ni /proc/cpuinfo && expected=1 || expected=0 ;;
    linux-arm64)
        [ -z "$runner" ] && { grep -qw sha2 /proc/cpuinfo && expected=1 || expected=0; } ;;
    darwin-aarch64)
        [ "$(sysctl -n hw.optional.arm.FEAT_SHA256 2>/dev/null || echo 0)" = 1 ] && expected=1 || expected=0 ;;
    darwin-x86_64)
        sysctl -n machdep.cpu.leaf7_features 2>/dev/null | grep -qw SHA && expected=1 || expected=0 ;;
esac
if [ -n "$expected" ] && [ "$accelerated" != "$expected" ]; then
    echo "FAIL: sha256 accelerated=$accelerated but the OS reports $expected for $target"
    exit 1
fi
echo "OK: sha256 backend choice matches the processor on $target (accelerated=$accelerated)"
