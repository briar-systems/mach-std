#!/usr/bin/env bash
# build the darwin runtime and process probe against this checkout's std and
# observe it from outside: exit statuses the kernel reports, stderr and stdout
# bytes, and the argument and environment blocks a child receives. the probe
# runs natively only, so this leg is executed by CI's macos jobs on both
# architectures; from linux it can be cross-built with --build-only.
#
# usage: verify.sh [path-to-mach] [target] [--build-only]
set -euo pipefail

mach="${1:-mach}"
target="${2:-darwin-aarch64}"
mode="${3:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

case "$target" in darwin-*) ;; *) fail "the darwin probe has no $target target" ;; esac

rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -r ../../src dep/std/src

for profile in debug release; do
    echo "building the darwin probe with $mach (target $target, profile $profile)"
    rm -rf "out/$target/$profile"
    mach_run build . --target "$target" --profile "$profile"
    exe="$(find "out/$target/$profile" -name 'darwin_probe' -type f -print -quit)"
    [ -n "$exe" ] || fail "no darwin_probe binary produced for $profile"
done

if [ "$mode" = "--build-only" ]; then
    echo "OK: the darwin probe cross-builds for $target in both profiles (not executed)"
    exit 0
fi

decode() {
    case "$1" in
        10|13|16|19|23|28|31) echo "spawning the child probe failed" ;;
        11|14|17|20|24|29|32) echo "waiting for the child probe failed" ;;
        12) echo "the child's main return did not arrive as its exit status" ;;
        15) echo "the child's os.terminate did not arrive as its exit status" ;;
        18) echo "the child's panic did not exit 255" ;;
        21) echo "the child's abort was not a SIGABRT death" ;;
        22) echo "creating the stdout pipe failed" ;;
        25) echo "the args child did not exit 0" ;;
        26|27) echo "the args child's argv/envp report did not match (printed above)" ;;
        30) echo "a missing program did not exit 127" ;;
        33) echo "a missing working directory did not exit 126" ;;
        34) echo "waiting for a foreign pid was not ECHILD" ;;
        *) echo "unexpected exit code $1" ;;
    esac
}

run_status() {
    set +e
    "$@"
    local code=$?
    set -e
    echo "$code"
}

for profile in debug release; do
    exe="$(cd "$(dirname "$(find "out/$target/$profile" -name 'darwin_probe' -type f -print -quit)")" && pwd)/darwin_probe"
    echo "== $profile: $exe"

    # runtime exit: main's return value is the process status, on both entry
    # conventions (LC_MAIN on arm64, LC_UNIXTHREAD on x86_64)
    for n in 0 3 200; do
        code="$(run_status "$exe" exit "$n")"
        [ "$code" = "$n" ] || fail "$profile: 'exit $n' reported status $code"
    done
    code="$(run_status "$exe" terminate 9)"
    [ "$code" = "9" ] || fail "$profile: 'terminate 9' reported status $code"

    # abort is a SIGABRT death: the shell reports 128 + 6
    code="$(run_status "$exe" abort)"
    [ "$code" = "134" ] || fail "$profile: 'abort' reported status $code, expected SIGABRT (134)"

    # panic writes to stderr and exits 255, with nothing on stdout
    err="$(mktemp)"; outp="$(mktemp)"
    code="$(run_status "$exe" panic 2>"$err" >"$outp")"
    [ "$code" = "255" ] || fail "$profile: 'panic' reported status $code"
    grep -q 'mach-std-415 panic reached stderr' "$err" \
        || { cat "$err"; fail "$profile: the panic message did not reach stderr"; }
    [ ! -s "$outp" ] || fail "$profile: the panic wrote to stdout"
    rm -f "$err" "$outp"

    # entry captured argc, argv and envp
    report="$(MACH_STD_415=hello "$exe" args one "two words" '')"
    expected="$(printf 'argc=5\nargv[0]=%s\nargv[1]=args\nargv[2]=one\nargv[3]=two words\nargv[4]=\nMACH_STD_415=hello' "$exe")"
    [ "$report" = "$expected" ] || { printf '%s\n' "$report"; fail "$profile: the argv/envp report did not match"; }
    report="$(env -u MACH_STD_415 "$exe" args)"
    expected="$(printf 'argc=2\nargv[0]=%s\nargv[1]=args\nMACH_STD_415 unset' "$exe")"
    [ "$report" = "$expected" ] || { printf '%s\n' "$report"; fail "$profile: the empty-environment report did not match"; }

    # process boundary observed by a parent: spawn, wait4, dup2, execve failure,
    # chdir failure, signal death, ECHILD
    code="$(run_status "$exe" child)"
    [ "$code" = "0" ] || fail "$profile: $(decode "$code")"
done

echo "OK: $target runtime exit, abort, panic, argv/envp capture and the spawned-child contracts hold in debug and release"
