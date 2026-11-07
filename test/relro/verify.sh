#!/usr/bin/env bash
# build the RELRO probes against this checkout's std and assert both paths of the
# post-#347 re-protection contract:
#   * happy   - a static-PIE with a relocated constant pointer runs fully hardened and
#               returns 42 (self-relocation + re-protection succeeded, no panic).
#   * fault   - forcing relro_reprotect down a fatal-invariant branch aborts loudly:
#               the panic message reaches stderr and the process dies by signal.
#
# the fault path is compiler-independent (it calls relro_reprotect with a forced misaligned
# start), so it exercises the fatal branch even under a mach seed whose writer predates the
# max-page layout - see the PR's CI-seed note.
#
# usage: verify.sh [path-to-mach] [target] [runner]
#   target defaults to linux (native x86_64); runner wraps execution (e.g. qemu-aarch64).
set -euo pipefail

# the fault probe dies by signal (SIGTRAP/SIGSEGV from the panic trap); suppress the core
# dump it would otherwise leave in the working tree.
ulimit -c 0 2>/dev/null || true

expect_happy=42

mach="${1:-mach}"
target="${2:-linux}"
runner="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }
run()  { if [ -n "$runner" ]; then "$runner" "$@"; else "$@"; fi; }

# copy the dependency inside the fixture project
"$mach" dep pull . --quiet

echo "building the RELRO probes with $mach (target $target)"
rm -rf out
# the manifest declares two bins; a plain build is intentionally ambiguous, so
# select each probe explicitly.
mach_run build . -a relro_happy --target "$target" --profile debug
mach_run build . -a relro_fault --target "$target" --profile debug
happy="$(find out -name relro_happy -type f -print -quit)"
fault="$(find out -name relro_fault -type f -print -quit)"
[ -n "$happy" ] || fail "no relro_happy binary produced"
[ -n "$fault" ] || fail "no relro_fault binary produced"

# the manifest's gnu targets link a PIE that names an interpreter, and no target links
# one that does not. nulling the Elf64 PT_INTERP header makes the static-PIE, which the
# kernel starts directly
python3 - "$happy" <<'EOF_PY'
import struct, sys
with open(sys.argv[1], 'r+b') as f:
    image = bytearray(f.read())
    phoff = struct.unpack_from('<Q', image, 32)[0]
    phentsize, phnum = struct.unpack_from('<HH', image, 54)
    for i in range(phnum):
        at = phoff + i * phentsize
        if struct.unpack_from('<I', image, at)[0] == 3:
            struct.pack_into('<I', image, at, 0)
    f.seek(0)
    f.write(image)
EOF_PY

echo "happy path: running $happy (expect exit $expect_happy, fully hardened)"
set +e
run "$happy"
code=$?
set -e
[ "$code" -eq "$expect_happy" ] || fail "happy path exit $code, expected $expect_happy"
echo "  OK: ran hardened, exit $expect_happy"

echo "negative path: running $fault (expect panic on stderr + death by signal)"
set +e
err="$(run "$fault" 2>&1 1>/dev/null)"
code=$?
set -e
# death by signal surfaces as exit 128+signo both natively and under qemu-user.
[ "$code" -ge 128 ] || fail "fault path exit $code, expected death by signal (>=128)"
grep -q "start not aligned to the runtime page" <<< "$err" \
    || fail "fault path missing the invariant panic message; got: $err"
echo "  OK: died by signal (exit $code), panic named the invariant"

echo "OK: RELRO re-protection is fatal on invariant breach and hardened on the happy path"
