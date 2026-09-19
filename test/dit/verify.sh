#!/usr/bin/env bash
# the aarch64 data-independent-timing mode, end to end: a program whose link
# admits a secret multiply starts with PSTATE.DIT on, on the main thread and
# on a thread std spawned; a program without one leaves the mode off; and on
# a processor without the mode the first program refuses to start with the
# contract's text and status 255. the last case needs a runner that can model
# such a processor (qemu-aarch64 -cpu cortex-a57), so it runs only where
# qemu-aarch64 is on the path.
#
# usage: verify.sh <mach> <target> [runner]
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-arm64}"
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

decode() {
    case "$1" in
        1) echo "the main thread's PSTATE.DIT is not what the link requires" ;;
        2) echo "thread spawn failed" ;;
        3) echo "thread join failed" ;;
        4) echo "the spawned thread's PSTATE.DIT is not what the link requires" ;;
        10) echo "__mach_dit_required does not match the link" ;;
        11) echo "the secret multiply computed a wrong product" ;;
        255) echo "the runtime refused to start" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

echo "building the dit probes with $mach (target $target)"
rm -rf out
mach_run build . --target "$target"
secret="$(find out -name 'secret' -type f -print -quit)"
plain="$(find out -name 'plain' -type f -print -quit)"
[ -n "$secret" ] && [ -n "$plain" ] || fail "no probe binaries produced"

run() {
    set +e
    if [ -n "$runner" ]; then "$runner" "$1"; else "$1"; fi
    code=$?
    set -e
    echo "$code"
}

code="$(run "$secret")"
[ "$code" -eq 0 ] || fail "secret: $(decode "$code")"
echo "OK: a link with a secret multiply starts with PSTATE.DIT on, on the main thread and a spawned one"

code="$(run "$plain")"
[ "$code" -eq 0 ] || fail "plain: $(decode "$code")"
echo "OK: a link without one leaves PSTATE.DIT off"

if [ "$target" = linux-arm64 ] && command -v qemu-aarch64 >/dev/null; then
    set +e
    err="$(qemu-aarch64 -cpu cortex-a57 "$secret" 2>&1 >/dev/null)"
    code=$?
    set -e
    [ "$code" -eq 255 ] || fail "on a processor without the mode the secret probe exited $code, not 255"
    expected="std.runtime: this program contains a constant-time multiply that requires the processor's data-independent-timing mode (PSTATE.DIT), and this processor or kernel does not provide it (aarch64-linux: HWCAP_DIT absent; aarch64-darwin: hw.optional.arm.FEAT_DIT is 0); refusing to start"
    [ "$err" = "$expected" ] || { echo "$err"; fail "the refusal text differs from the contract"; }
    echo "OK: on a processor without the mode the runtime refuses to start with the contract's text"
fi
