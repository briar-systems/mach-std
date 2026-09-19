#!/usr/bin/env bash
# the aarch64 data-independent-timing mode, end to end: a program whose link
# admits a secret multiply starts with PSTATE.DIT on, on the main thread and
# on a thread std spawned; a program without one leaves the mode off; and on
# a processor without the mode the first program refuses to start with the
# contract's text and status 255. which of the first and last applies is what
# the OS says about FEAT_DIT; qemu-aarch64 -cpu cortex-a57 models a processor
# without it wherever qemu is on the path.
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

expected="std.runtime: this program contains a constant-time multiply that requires the processor's data-independent-timing mode (PSTATE.DIT), and this processor or kernel does not provide it (aarch64-linux: HWCAP_DIT absent; aarch64-darwin: hw.optional.arm.FEAT_DIT is 0); refusing to start"

# the secret probe must start with the mode on where the OS reports it, and
# refuse with the contract's text where it does not (a github arm64 runner is
# Neoverse N1, which predates FEAT_DIT, so the refusal is what CI exercises)
refuses() {
    set +e
    err="$(if [ -n "$2" ]; then $2 "$1" 2>&1 >/dev/null; else "$1" 2>&1 >/dev/null; fi)"
    code=$?
    set -e
    [ "$code" -eq 255 ] || fail "on a processor without the mode the secret probe exited $code, not 255"
    [ "$err" = "$expected" ] || { echo "$err"; fail "the refusal text differs from the contract"; }
}

has_dit=""
case "$target" in
    linux-arm64)
        if [ -n "$runner" ]; then has_dit=1; else grep -qw dit /proc/cpuinfo && has_dit=1 || has_dit=0; fi ;;
    darwin-aarch64)
        [ "$(sysctl -n hw.optional.arm.FEAT_DIT 2>/dev/null || echo 0)" = 1 ] && has_dit=1 || has_dit=0 ;;
esac
[ -n "$has_dit" ] || fail "no way to ask the OS about FEAT_DIT on $target"

if [ "$has_dit" = 1 ]; then
    code="$(run "$secret")"
    [ "$code" -eq 0 ] || fail "secret: $(decode "$code")"
    echo "OK: a link with a secret multiply starts with PSTATE.DIT on, on the main thread and a spawned one"
else
    refuses "$secret" "$runner"
    echo "OK: this processor lacks the mode and the runtime refuses to start with the contract's text"
fi

code="$(run "$plain")"
[ "$code" -eq 0 ] || fail "plain: $(decode "$code")"
echo "OK: a link without one leaves PSTATE.DIT off"

if [ "$target" = linux-arm64 ] && command -v qemu-aarch64 >/dev/null; then
    refuses "$secret" "qemu-aarch64 -cpu cortex-a57"
    echo "OK: under qemu-aarch64 -cpu cortex-a57 the runtime refuses to start with the contract's text"
fi
