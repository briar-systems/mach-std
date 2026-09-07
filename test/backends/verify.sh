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
            wipe_line="$(echo "$release_body" | grep -n -m1 -E 'mov byte \[[^]]+\], 0|strb wzr|sb zero' | cut -d: -f1 || true)"
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
