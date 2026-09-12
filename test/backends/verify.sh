#!/usr/bin/env bash
# cross-compile a program that references std.system.os (and, through it,
# std.runtime) for every supported target against this checkout's std. proves
# target-gated backend modules compile instead of being skipped as dead $if
# branches. compile only; nothing here is run.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

command -v llvm-nm >/dev/null || fail "llvm-nm is required"
command -v llvm-readobj >/dev/null || fail "llvm-readobj is required"

# copy the dependency inside the fixture project
rm -rf dep
mkdir -p dep/std
cp ../../mach.toml dep/std/mach.toml
cp -R ../../src dep/std/src

# the supported-boundary shape of a cross-built darwin image (#415)
#
# independent of the assembly checks above: this reads the linked Mach-O the
# way dyld and the kernel will. exactly one dylib dependency, spelled by its
# install path; the dynamic linker; the entry convention each architecture's
# runtime is written against; the segments the writer lays out; every
# libSystem import the migrated domains bind, by its exact spelling; none of
# the symbols the migration refuses; and no trap instruction anywhere in the
# text, which is the property the whole boundary exists to guarantee.
inspect_macho() {
    local target="$1" profile="$2" exe="$3"
    command -v llvm-objdump >/dev/null || fail "llvm-objdump is required"

    local needed
    needed="$(llvm-readobj --needed-libs "$exe" | sed -n '/NeededLibraries \[/,/^\]/p' \
        | grep -v 'NeededLibraries\|^\]' | sed 's/^[[:space:]]*//')"
    [ "$needed" = "/usr/lib/libSystem.B.dylib" ] \
        || fail "$target $profile: expected exactly one dependency, /usr/lib/libSystem.B.dylib, got: $(echo "$needed" | tr '\n' ' ')"

    local headers
    headers="$(llvm-objdump --macho --private-headers "$exe")"
    [ "$(echo "$headers" | grep -c 'cmd LC_LOAD_DYLIB$')" = 1 ] \
        || fail "$target $profile: expected one LC_LOAD_DYLIB command"
    echo "$headers" | grep -q 'cmd LC_LOAD_DYLINKER$' \
        || fail "$target $profile: no LC_LOAD_DYLINKER"
    echo "$headers" | grep -q 'name /usr/lib/dyld' \
        || fail "$target $profile: the dynamic linker is not /usr/lib/dyld"
    local fileheader
    fileheader="$(llvm-readobj --file-header "$exe")"
    echo "$fileheader" | grep -q 'FileType: Executable' \
        || fail "$target $profile: not an MH_EXECUTE image"
    echo "$fileheader" | grep -q 'MH_DYLDLINK' \
        || fail "$target $profile: not a dyld-linked image"
    echo "$fileheader" | grep -q 'MH_TWOLEVEL' \
        || fail "$target $profile: not a two-level-namespace image"
    case "$target" in
        darwin-aarch64)
            # the arm64 runtime reads argc/argv/envp from x0/x1/x2: LC_MAIN
            echo "$fileheader" | grep -q 'MH_PIE' \
                || fail "$target $profile: arm64 image is not MH_PIE"
            echo "$headers" | grep -q 'cmd LC_MAIN$' \
                || fail "$target $profile: arm64 image has no LC_MAIN entry"
            echo "$headers" | grep -q 'cmd LC_BUILD_VERSION$' \
                || fail "$target $profile: arm64 image has no LC_BUILD_VERSION"
            ;;
        darwin-x86_64)
            # the x86_64 runtime reads argc/argv off the stack: LC_UNIXTHREAD
            echo "$headers" | grep -q 'cmd LC_UNIXTHREAD$' \
                || fail "$target $profile: x86_64 image has no LC_UNIXTHREAD entry"
            ;;
    esac

    local segments seg
    segments="$(llvm-readobj --macho-segment "$exe")"
    for seg in __PAGEZERO __TEXT __DATA __STUBS __GOT __LINKEDIT; do
        echo "$segments" | grep -q "Name: $seg\$" \
            || fail "$target $profile: segment $seg is missing"
    done

    local imports sym
    imports="$(llvm-nm -u "$exe" | awk '{print $NF}')"
    local required=(
        # process (#415 S5)
        _fork _vfork _execve _wait4 _waitid _kill _getpid _setpgid _getpgid
        _dup2 _chdir _getrlimit __exit
        # runtime exit and panic
        _write
        # directory
        _closedir
        # secret OS
        _calloc _free _getentropy
        # errno
        ___error
    )
    case "$target" in
        darwin-x86_64) required+=('_fdopendir$INODE64' '_readdir$INODE64' '_fstat$INODE64') ;;
        darwin-aarch64) required+=(_fdopendir _readdir _fstat) ;;
    esac
    for sym in "${required[@]}"; do
        echo "$imports" | grep -Fxq "$sym" \
            || fail "$target $profile: libSystem import $sym is missing or misspelled"
    done
    # `_exit` here is C `exit(3)`, which must not be bound: the runtime and the
    # panic path end the process through `_exit(2)` (`__exit`) only
    local refused=(
        _exit _syscall _bsdthread_create _bsdthread_register _bsdthread_terminate
        ___ulock_wait ___ulock_wake ___open ___fcntl
    )
    for sym in "${refused[@]}"; do
        ! echo "$imports" | grep -Fxq "$sym" \
            || fail "$target $profile: refused symbol $sym is bound"
    done
    if echo "$imports" | grep -Eq '^[^_]'; then
        fail "$target $profile: an import without the Mach-O underscore prefix remains"
    fi

    local traps
    traps="$(llvm-objdump --macho -d "$exe" | grep -cE '^[[:space:]]*[0-9a-f]+:.*[[:space:]](svc|syscall)([[:space:]]|$)' || true)"
    [ "$traps" = 0 ] \
        || fail "$target $profile: $traps trap instruction(s) remain in the text"

    echo "OK: $target $profile Mach-O binds libSystem alone, enters as expected and traps nowhere"
}

targets=(
    linux-x86_64
    linux-arm64
    linux-riscv64
    windows-x86_64
    darwin-x86_64
    darwin-aarch64
)
for target in "${targets[@]}"; do
    profiles=(debug release)
    case "$target" in windows-*) profiles=(windows-opt0 release) ;; esac
    rm -rf "out/$target"
    for profile in "${profiles[@]}"; do
        echo "cross-compiling the $profile backend smoke test for $target with $mach"
        log="$(mach_run build . --target "$target" --profile "$profile" \
            --emit-ir --emit-asm -vv 2>&1)" \
            || { echo "$log" >&2; fail "$target $profile failed to compile"; }

        exe="$(find "out/$target/$profile" -name backends -type f -print -quit)"
        [ -n "$exe" ] || fail "$target $profile: no backends binary produced"

        # confirm the backend's shared module was actually compiled
        echo "$log" | grep -q "skipped .* target-gated modules" \
            && fail "$target $profile: target-gated modules were skipped"
        echo "$log" | grep -q "std.system.os.${target%%-*}.shared" \
            || fail "$target $profile: os backend was never compiled"
        echo "$log" | grep -q "std.net.async.${target%%-*}" \
            || fail "$target $profile: network backend was never compiled"

        secret_ir="out/$target/$profile/ir/std/system/os/secret.ir"
        secret_asm="out/$target/$profile/asm/std/system/os/secret.s"
        main_ir="out/$target/$profile/ir/backends/main.ir"
        main_asm="out/$target/$profile/asm/backends/main.s"
        [ -f "$secret_ir" ] || fail "$target $profile: secret OS IR missing"
        [ -f "$secret_asm" ] || fail "$target $profile: secret OS assembly missing"
        [ -f "$main_ir" ] || fail "$target $profile: typed boundary IR missing"
        [ -f "$main_asm" ] || fail "$target $profile: typed boundary assembly missing"
        python3 "$here/verify-ir.py" "$secret_ir" "$main_ir" "$profile" \
            || fail "$target $profile: secret IR contract failed"
        case "$target" in
            linux-*)
                grep -q 'syscall\|ecall\|svc' "$secret_asm" \
                    || fail "$target $profile: secret boundary omitted native syscalls"
                grep -q 'syscall\|ecall\|svc' "$main_asm" \
                    || fail "$target $profile: typed boundary omitted native syscalls"
                if grep -Eq 'malloc|free|getrandom' "$secret_asm"; then
                    fail "$target $profile: secret boundary gained a libc dependency"
                fi
                ;;
            darwin-*)
                grep -q '_calloc' "$secret_asm" \
                    || fail "$target $profile: secret allocator omitted libSystem calloc"
                grep -q '_getentropy' "$secret_asm" \
                    || fail "$target $profile: secret entropy omitted libSystem getentropy"
                grep -q '_free' "$secret_asm" \
                    || fail "$target $profile: secret release omitted libSystem free"
                undefined="$(llvm-nm -u "$exe")"
                echo "$undefined" | grep -Eq '(^|[[:space:]])_calloc$' \
                    || fail "$target $profile: Mach-O calloc import is misspelled"
                echo "$undefined" | grep -Eq '(^|[[:space:]])_getentropy$' \
                    || fail "$target $profile: Mach-O getentropy import is misspelled"
                echo "$undefined" | grep -Eq '(^|[[:space:]])_free$' \
                    || fail "$target $profile: Mach-O free import is misspelled"
                if echo "$undefined" | grep -Eq '(^|[[:space:]])(calloc|getentropy|free)$'; then
                    fail "$target $profile: unprefixed Mach-O secret import remains"
                fi
                grep -Eq '(jmp|b) _calloc' "$main_asm" \
                    || fail "$target $profile: typed allocator omitted libSystem calloc"
                grep -Eq '(jmp|b) _free' "$main_asm" \
                    || fail "$target $profile: typed release omitted libSystem free"
                inspect_macho "$target" "$profile" "$exe"
                ;;
            windows-*)
                grep -q 'VirtualAlloc' "$secret_asm" \
                    || fail "$target $profile: secret allocator omitted VirtualAlloc"
                grep -q 'BCryptGenRandom' "$secret_asm" \
                    || fail "$target $profile: secret entropy omitted BCryptGenRandom"
                if llvm-readobj --coff-imports "$exe" | grep -q 'SystemFunction036'; then
                    fail "$target $profile: legacy RtlGenRandom import remains"
                fi
                grep -q 'jmp VirtualAlloc' "$main_asm" \
                    || fail "$target $profile: typed allocator omitted VirtualAlloc"
                grep -q 'jmp VirtualFree' "$main_asm" \
                    || fail "$target $profile: typed release omitted VirtualFree"
                ;;
        esac
        if [ "$profile" = release ]; then
            release_body="$(sed -n '/std.system.os.secret.deallocate:/,/std.system.os.secret.random_fill:/p' "$secret_asm")"
            # the oblivious wipe stays a call under the v5 inlining policy (mach
            # N6, PR #3270), so the call site counts as the wipe here
            wipe_line="$(echo "$release_body" | grep -n -m1 -E 'mov byte \[[^]]+\], 0|strb wzr|sb zero|std\.system\.os\.secret\.wipe([^_]|$)' | cut -d: -f1 || true)"
            case "$target" in
                linux-*)
                    release_line="$(echo "$release_body" | grep -n -m1 -E 'syscall|ecall|svc' | cut -d: -f1 || true)"
                    ;;
                darwin-*)
                    release_line="$(echo "$release_body" | grep -n -m1 '_free' | cut -d: -f1 || true)"
                    ;;
                windows-*)
                    release_line="$(echo "$release_body" | grep -n -m1 'VirtualFree' | cut -d: -f1 || true)"
                    ;;
            esac
            [ -n "$wipe_line" ] || fail "$target release: secret release wipe missing from assembly"
            [ -n "$release_line" ] || fail "$target release: native release missing from assembly"
            [ "$wipe_line" -lt "$release_line" ] \
                || fail "$target release: native release precedes secret wipe in assembly"

            typed_release_body="$(sed -n '/# std.system.os.secret.release_typed\$backends.main.SecretRecord:/,/^# /p' "$main_asm")"
            typed_wipe_line="$(echo "$typed_release_body" | grep -n -m1 -E 'mov byte \[[^]]+\], 0|strb wzr|sb zero' | cut -d: -f1 || true)"
            case "$target" in
                *-x86_64)
                    typed_release_line="$(echo "$typed_release_body" | grep -n -E 'call r[0-9]+' | tail -1 | cut -d: -f1 || true)"
                    ;;
                *-arm64|*-aarch64)
                    typed_release_line="$(echo "$typed_release_body" | grep -n -E 'blr x[0-9]+' | tail -1 | cut -d: -f1 || true)"
                    ;;
                linux-riscv64)
                    typed_release_line="$(echo "$typed_release_body" | grep -n -E 'jalr ra, 0\(' | tail -1 | cut -d: -f1 || true)"
                    ;;
            esac
            [ -n "$typed_wipe_line" ] \
                || fail "$target release: typed full-layout wipe missing from assembly"
            [ -n "$typed_release_line" ] \
                || fail "$target release: typed native release missing from assembly"
            [ "$typed_wipe_line" -lt "$typed_release_line" ] \
                || fail "$target release: native typed release precedes full-layout wipe in assembly"
        fi

        echo "OK: $target $profile backends compile ($exe)"
    done
done
