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
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

# vendor this checkout's std as the path dependency (dep/std -> repo root).
mkdir -p dep
ln -sfn "$(cd ../.. && pwd)" dep/std

targets=(
    linux-x86_64
    linux-arm64
    linux-riscv64
    windows-x86_64
    darwin-x86_64
    darwin-aarch64
)
profiles=(debug release)

for target in "${targets[@]}"; do
    rm -rf "out/$target"
    for profile in "${profiles[@]}"; do
        echo "cross-compiling the $profile backend smoke test for $target with $mach"
        log="$("$mach" build . --target "$target" --profile "$profile" \
            --emit-ir --emit-asm --verify-ir -vv 2>&1)" \
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
        [ -f "$secret_ir" ] || fail "$target $profile: secret OS IR missing"
        [ -f "$secret_asm" ] || fail "$target $profile: secret OS assembly missing"
        grep -q 'fn @std.system.os.secret.allocate' "$secret_ir" \
            || fail "$target $profile: secret allocation boundary missing"
        grep -q 'fn @std.system.os.secret.deallocate' "$secret_ir" \
            || fail "$target $profile: secret release boundary missing"
        grep -q 'fn @std.system.os.secret.random_fill' "$secret_ir" \
            || fail "$target $profile: secret entropy boundary missing"
        if grep -Eq 'ptrtoint|inttoptr' "$secret_ir"; then
            fail "$target $profile: secret boundary materialized an integer pointer alias"
        fi
        release_ir="$(sed -n '/fn @std.system.os.secret.release_all/,/^  fn /p' "$secret_ir")"
        if [ "$profile" = debug ]; then
            wipe_ir_line="$(echo "$release_ir" | grep -n -m1 'call void @std.system.os.secret.wipe' | cut -d: -f1 || true)"
        else
            wipe_ir_line="$(echo "$release_ir" | grep -n -m1 'store 0: i8' | cut -d: -f1 || true)"
        fi
        release_ir_line="$(echo "$release_ir" | grep -n -m1 'call i64 %p3' | cut -d: -f1 || true)"
        [ -n "$wipe_ir_line" ] || fail "$target $profile: secret release wipe missing from IR"
        [ -n "$release_ir_line" ] || fail "$target $profile: native release call missing from IR"
        [ "$wipe_ir_line" -lt "$release_ir_line" ] \
            || fail "$target $profile: native release call precedes secret wipe in IR"
        case "$target" in
            linux-*)
                grep -q 'syscall\|ecall\|svc' "$secret_asm" \
                    || fail "$target $profile: secret boundary omitted native syscalls"
                if grep -Eq 'malloc|free|getrandom' "$secret_asm"; then
                    fail "$target $profile: secret boundary gained a libc dependency"
                fi
                ;;
            darwin-*)
                grep -q 'calloc' "$secret_asm" \
                    || fail "$target $profile: secret allocator omitted libSystem calloc"
                grep -q 'getentropy' "$secret_asm" \
                    || fail "$target $profile: secret entropy omitted libSystem getentropy"
                grep -q 'free' "$secret_asm" \
                    || fail "$target $profile: secret release omitted libSystem free"
                ;;
            windows-*)
                grep -q 'VirtualAlloc' "$secret_asm" \
                    || fail "$target $profile: secret allocator omitted VirtualAlloc"
                grep -q 'BCryptGenRandom' "$secret_asm" \
                    || fail "$target $profile: secret entropy omitted BCryptGenRandom"
                if llvm-readobj --coff-imports "$exe" | grep -q 'SystemFunction036'; then
                    fail "$target $profile: legacy RtlGenRandom import remains"
                fi
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
                    release_line="$(echo "$release_body" | grep -n -m1 'free' | cut -d: -f1 || true)"
                    ;;
                windows-*)
                    release_line="$(echo "$release_body" | grep -n -m1 'VirtualFree' | cut -d: -f1 || true)"
                    ;;
            esac
            [ -n "$wipe_line" ] || fail "$target release: secret release wipe missing from assembly"
            [ -n "$release_line" ] || fail "$target release: native release missing from assembly"
            [ "$wipe_line" -lt "$release_line" ] \
                || fail "$target release: native release precedes secret wipe in assembly"
        fi

        echo "OK: $target $profile backends compile ($exe)"
    done
done
