#!/usr/bin/env bash
# build the RELRO probes against this checkout's std and assert both paths of the
# post-#347 re-protection contract:
#   * happy   - a --pie binary with a relocated constant pointer runs fully hardened and
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
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }
run()  { if [ -n "$runner" ]; then "$runner" "$@"; else "$@"; fi; }

# vendor this checkout's std as the path dependency (dep/std -> repo root).
mkdir -p dep
ln -sfn "$(cd ../.. && pwd)" dep/std

echo "building the RELRO probes --pie with $mach (target $target)"
rm -rf out
"$mach" build . --target "$target" --pie --profile debug
happy="$(find out -name relro_happy -type f -print -quit)"
fault="$(find out -name relro_fault -type f -print -quit)"
[ -n "$happy" ] || fail "no relro_happy binary produced"
[ -n "$fault" ] || fail "no relro_fault binary produced"

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
echo "$err" | grep -q "start not aligned to the runtime page" \
    || fail "fault path missing the invariant panic message; got: $err"
echo "  OK: died by signal (exit $code), panic named the invariant"

echo "OK: RELRO re-protection is fatal on invariant breach and hardened on the happy path"
