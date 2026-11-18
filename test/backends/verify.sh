#!/usr/bin/env bash
# cross-compile a program that reaches std's target-gated backends (os, network,
# secret storage) for every supported target and profile against this
# checkout's std, and read each linked image for the native imports std binds:
# a linux image binds nothing, a windows image takes its secret memory and
# entropy from VirtualAlloc and BCryptGenRandom, and a darwin image binds
# libSystem alone and traps nowhere. compile only; nothing here is run.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

command -v llvm-nm >/dev/null || fail "llvm-nm is required"
command -v llvm-readobj >/dev/null || fail "llvm-readobj is required"

# copy the dependency inside the fixture project
"$mach" dep pull . --quiet

# the supported-boundary shape of a cross-built darwin image (#415)
#
# this reads the linked Mach-O the way dyld and the kernel will. exactly one dylib dependency, spelled by its
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
    grep -q 'cmd LC_LOAD_DYLINKER$' <<< "$headers" \
        || fail "$target $profile: no LC_LOAD_DYLINKER"
    grep -q 'name /usr/lib/dyld' <<< "$headers" \
        || fail "$target $profile: the dynamic linker is not /usr/lib/dyld"
    local fileheader
    fileheader="$(llvm-readobj --file-header "$exe")"
    grep -q 'FileType: Executable' <<< "$fileheader" \
        || fail "$target $profile: not an MH_EXECUTE image"
    grep -q 'MH_DYLDLINK' <<< "$fileheader" \
        || fail "$target $profile: not a dyld-linked image"
    grep -q 'MH_TWOLEVEL' <<< "$fileheader" \
        || fail "$target $profile: not a two-level-namespace image"
    # the runtime enters by the load command the image kind selects: a PIE is an
    # LC_MAIN image dyld calls, anything else an LC_UNIXTHREAD image the kernel enters
    if grep -q 'MH_PIE' <<< "$fileheader"; then
        grep -q 'cmd LC_MAIN$' <<< "$headers" \
            || fail "$target $profile: a PIE image has no LC_MAIN entry"
    else
        [ "$target" = darwin-x86_64 ] || fail "$target $profile: arm64 image is not MH_PIE"
        grep -q 'cmd LC_UNIXTHREAD$' <<< "$headers" \
            || fail "$target $profile: a non-PIE image has no LC_UNIXTHREAD entry"
    fi
    if [ "$target" = darwin-aarch64 ]; then
        grep -q 'cmd LC_BUILD_VERSION$' <<< "$headers" \
            || fail "$target $profile: arm64 image has no LC_BUILD_VERSION"
    fi

    local segments seg
    segments="$(llvm-readobj --macho-segment "$exe")"
    for seg in __PAGEZERO __TEXT __DATA_CONST __DATA __LINKEDIT; do
        grep -q "Name: $seg\$" <<< "$segments" \
            || fail "$target $profile: segment $seg is missing"
    done
    # call stubs sit at the end of the code, in reach of every call (mach #3888)
    ! grep -q 'Name: __STUBS$' <<< "$segments" \
        || fail "$target $profile: call stubs sit in a __STUBS segment past the data"
    # the import GOT sits ahead of the zero-fill, in __DATA_CONST (mach #3903)
    ! grep -q 'Name: __GOT$' <<< "$segments" \
        || fail "$target $profile: the import GOT sits in a __GOT segment"
    local sections
    sections="$(llvm-readobj --sections "$exe" | awk '$1 == "Name:" { name = $2 } $1 == "Segment:" { print name, $2 }')"
    grep -qx '__stubs __TEXT' <<< "$sections" \
        || fail "$target $profile: no __TEXT,__stubs section"
    grep -qx '__got __DATA_CONST' <<< "$sections" \
        || fail "$target $profile: no __DATA_CONST,__got section"

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
        # secret OS: guarded, locked mappings and entropy
        _mmap _mprotect _mlock _munmap _getentropy
        # errno
        ___error
    )
    case "$target" in
        darwin-x86_64) required+=('_fdopendir$INODE64' '_readdir$INODE64' '_fstat$INODE64') ;;
        darwin-aarch64) required+=(_fdopendir _readdir _fstat) ;;
    esac
    for sym in "${required[@]}"; do
        grep -Fxq "$sym" <<< "$imports" \
            || fail "$target $profile: libSystem import $sym is missing or misspelled"
    done
    # `_exit` here is C `exit(3)`, which must not be bound: the runtime and the
    # panic path end the process through `_exit(2)` (`__exit`) only
    local refused=(
        _exit _syscall _bsdthread_create _bsdthread_register _bsdthread_terminate
        ___ulock_wait ___ulock_wake ___open ___fcntl
    )
    for sym in "${refused[@]}"; do
        ! grep -Fxq "$sym" <<< "$imports" \
            || fail "$target $profile: refused symbol $sym is bound"
    done
    # dyld's lazy binder is the one import spelled without the C prefix
    if grep -v '^dyld_stub_binder$' <<< "$imports" | grep -Eq '^[^_]'; then
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
    linux-aarch64
    linux-riscv64
    windows-x86_64
    darwin-x86_64
    darwin-aarch64
)
for target in "${targets[@]}"; do
    profiles=(debug release)
    case "$target" in windows-*) profiles=(windows-opt0 release) ;; esac
    for profile in "${profiles[@]}"; do
        echo "cross-compiling the $profile backend smoke test for $target with $mach"
        exe="out/$target/$profile/backends"
        log="$("$mach" build . --target "$target" --profile "$profile" -o "$exe" -vv 2>&1)" \
            || { echo "$log" >&2; fail "$target $profile failed to compile"; }

        [ -f "$exe" ] || fail "$target $profile: no backends binary produced"

        # confirm the backend's shared module was actually compiled
        grep -q "std.system.os.${target%%-*}.shared" <<< "$log" \
            || fail "$target $profile: os backend was never compiled"
        grep -q "std.net.async.${target%%-*}" <<< "$log" \
            || fail "$target $profile: network backend was never compiled"

        case "$target" in
            linux-*)
                # std links no libc on linux, so a static image leaves nothing undefined
                undefined="$(llvm-nm -u "$exe")"
                [ -z "$undefined" ] || { echo "$undefined" >&2; fail "$target $profile: the image binds external symbols"; }
                ;;
            darwin-*)
                inspect_macho "$target" "$profile" "$exe"
                ;;
            windows-*)
                imports="$(llvm-readobj --coff-imports "$exe")"
                grep -q 'Symbol: VirtualAlloc ' <<< "$imports" \
                    || fail "$target $profile: secret allocator omitted VirtualAlloc"
                grep -q 'Symbol: VirtualFree ' <<< "$imports" \
                    || fail "$target $profile: secret release omitted VirtualFree"
                grep -q 'Symbol: BCryptGenRandom ' <<< "$imports" \
                    || fail "$target $profile: secret entropy omitted BCryptGenRandom"
                ! grep -q 'SystemFunction036' <<< "$imports" \
                    || fail "$target $profile: legacy RtlGenRandom import remains"
                ;;
        esac

        echo "OK: $target $profile backends compile ($exe)"
    done
done
