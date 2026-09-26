#!/usr/bin/env bash
# std.system.cpu's aes and carry-less multiply fields against the host.
#
# the probe program prints what std.system.cpu.features() reports and what
# os.cpu_features reads. both must match the OS's own view of the processor:
# /proc/cpuinfo on linux, sysctl on darwin. windows has no OS view of these x86
# bits, so there the two answers must agree and hold across runs.
#
# on a linux host with qemu-user on the path, the x86_64 probe also runs under
# `qemu-x86_64 -cpu max` (both present) and `-cpu qemu64` (both absent, read
# false with no error), and the arm64 probe under `qemu-aarch64 -cpu max`. no
# qemu aarch64 model lacks AES, so the arm64 false case is not exercised. on a
# compiler that knows the extensions (mach 5.12.2 and later), a build that
# selects aes and pclmul reports both under qemu64 while the probe reads them
# absent, which is the build-time half of features().
#
# usage: verify.sh <mach> <target>
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

rm -rf dep out
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

case "$target" in
    *x86_64) names=(aes pclmul) ;;
    *) names=(aes pmull) ;;
esac

build() {
    mach_run build . --target "$1" >/dev/null
    local bin
    bin="$(find "out/$1" -name 'cpu' -type f -print -quit)"
    [ -z "$bin" ] && bin="$(find "out/$1" -name 'cpu.exe' -type f -print -quit)"
    [ -n "$bin" ] || fail "no probe binary for $1"
    echo "$bin"
}

# runs the probe and prints "<features line>|<probed line>"
probe() {
    local out code
    set +e
    out="$("$@")"
    code=$?
    set -e
    [ "$code" -eq 0 ] || fail "probe exited $code under: $*"
    local have probed
    have="$(echo "$out" | tr -d '\r' | sed -n 's/^features //p')"
    probed="$(echo "$out" | tr -d '\r' | sed -n 's/^probed //p')"
    [ -n "$have" ] && [ -n "$probed" ] || fail "no probe output under: $*"
    echo "$have|$probed"
}

# the expected "a=0 b=1" line from the OS's own view
os_view() {
    local flags=() line=""
    case "$target" in
        linux-x86_64)
            grep -qw aes /proc/cpuinfo && flags+=(1) || flags+=(0)
            grep -qw pclmulqdq /proc/cpuinfo && flags+=(1) || flags+=(0) ;;
        linux-arm64)
            grep -qw aes /proc/cpuinfo && flags+=(1) || flags+=(0)
            grep -qw pmull /proc/cpuinfo && flags+=(1) || flags+=(0) ;;
        darwin-aarch64)
            [ "$(sysctl -n hw.optional.arm.FEAT_AES 2>/dev/null || echo 0)" = 1 ] && flags+=(1) || flags+=(0)
            [ "$(sysctl -n hw.optional.arm.FEAT_PMULL 2>/dev/null || echo 0)" = 1 ] && flags+=(1) || flags+=(0) ;;
        darwin-x86_64)
            sysctl -n machdep.cpu.features | grep -qw AES && flags+=(1) || flags+=(0)
            sysctl -n machdep.cpu.features | grep -qw PCLMULQDQ && flags+=(1) || flags+=(0) ;;
        *) return 0 ;;
    esac
    line="${names[0]}=${flags[0]} ${names[1]}=${flags[1]}"
    echo "$line"
}

bin="$(build "$target")"
first="$(probe "$bin")"
have="${first%%|*}" probed="${first##*|}"
echo "$target: features $have, probed $probed"
[ "$have" = "$probed" ] || fail "features() and the OS probe disagree on $target: $have vs $probed"
[ "$(probe "$bin")" = "$first" ] || fail "a second run on $target reports differently"
expected="$(os_view)"
if [ -n "$expected" ]; then
    [ "$have" = "$expected" ] || fail "$target reports $have but the OS reports $expected"
    echo "OK: $target matches the OS ($expected)"
else
    echo "OK: $target is consistent across the probe, features() and a second run (no OS view of these bits)"
fi

# qemu models where this host can run them
if [ "$target" = linux-x86_64 ] && command -v qemu-x86_64 >/dev/null; then
    [ "$(probe qemu-x86_64 -cpu max "$bin")" = "aes=1 pclmul=1|aes=1 pclmul=1" ] \
        || fail "qemu-x86_64 -cpu max does not report aes and pclmul"
    echo "OK: qemu-x86_64 -cpu max reports aes=1 pclmul=1"
    [ "$(probe qemu-x86_64 -cpu qemu64 "$bin")" = "aes=0 pclmul=0|aes=0 pclmul=0" ] \
        || fail "qemu-x86_64 -cpu qemu64 does not read aes and pclmul absent"
    echo "OK: qemu-x86_64 -cpu qemu64 reads aes=0 pclmul=0 without error"

    version="$("$mach" info | sed -n '1s/^mach \([0-9]*\)\.\([0-9]*\)\.\([0-9]*\).*/\1 \2 \3/p')"
    read -r major minor patch <<<"$version"
    [ -n "$major" ] || fail "cannot read the compiler version"
    if [ "$major" -gt 5 ] || { [ "$major" -eq 5 ] && { [ "$minor" -gt 12 ] || { [ "$minor" -eq 12 ] && [ "$patch" -ge 2 ]; }; }; }; then
        # the selecting target lives in a copy, so the manifest older compilers
        # read never names an extension they do not know
        sel="$here/out/selected"
        mkdir -p "$sel"
        cp -r mach.toml src dep "$sel/"
        cat >>"$sel/mach.toml" <<'EOF'

[target.linux-x86_64-aes]
isa = "x86_64"
os  = "linux"
abi = "sysv64"
extensions = ["aes", "pclmul"]
EOF
        selected="$(cd "$sel" && build linux-x86_64-aes)"
        selected="$sel/$selected"
        [ "$(probe qemu-x86_64 -cpu qemu64 "$selected")" = "aes=1 pclmul=1|aes=0 pclmul=0" ] \
            || fail "a build selecting aes and pclmul does not report them under qemu64"
        echo "OK: a build selecting aes and pclmul reports both under qemu64, where the probe reads them absent"
    else
        echo "SKIP: mach $major.$minor.$patch predates the aes and pclmul extensions, so no build can select them"
    fi
fi
if [ "$target" = linux-x86_64 ] && command -v qemu-aarch64 >/dev/null; then
    arm="$(build linux-arm64)"
    [ "$(probe qemu-aarch64 -cpu max "$arm")" = "aes=1 pmull=1|aes=1 pmull=1" ] \
        || fail "qemu-aarch64 -cpu max does not report aes and pmull"
    echo "OK: qemu-aarch64 -cpu max reports aes=1 pmull=1"
fi
