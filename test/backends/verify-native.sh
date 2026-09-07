#!/usr/bin/env bash
set -euo pipefail

mach="${1:-mach}"
target="${2:-linux-x86_64}"
profile=debug
case "$target" in windows-*) profile=windows-opt0 ;; esac
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$here/../lib/compiler.sh"
root="$(cd "$here/../.." && pwd)"

fail() { echo "FAIL: $1" >&2; exit 1; }

rm -rf "$here/dep"
mkdir -p "$here/dep/std"
cp "$root/mach.toml" "$here/dep/std/mach.toml"
cp -R "$root/src" "$here/dep/std/src"

cd "$here"
rm -rf "out/$target"
mach_run build . --target "$target" --profile "$profile"
exe="$(find "out/$target" -type f \( -name backends -o -name 'backends.exe' \) -print -quit)"
[ -n "$exe" ] || fail "$target produced no native executable"

echo "running $exe"
"$exe"
echo

case "$target" in
    linux-x86_64)
        readelf -h -l -d "$exe"
        readelf -h "$exe" | grep -q 'Class:[[:space:]]*ELF64' \
            || fail "$target did not produce ELF64"
        readelf -h "$exe" | grep -q 'Machine:[[:space:]]*Advanced Micro Devices X86-64' \
            || fail "$target produced the wrong machine"
        ;;
    linux-arm64)
        readelf -h -l -d "$exe"
        readelf -h "$exe" | grep -q 'Class:[[:space:]]*ELF64' \
            || fail "$target did not produce ELF64"
        readelf -h "$exe" | grep -q 'Machine:[[:space:]]*AArch64' \
            || fail "$target produced the wrong machine"
        ;;
    darwin-x86_64|darwin-aarch64)
        otool -hv "$exe"
        otool -L "$exe"
        deps="$(otool -L "$exe" | tail -n +2 | grep -c 'libSystem' || true)"
        [ "$deps" = "1" ] || fail "$target expected one libSystem dependency, found $deps"
        otool -L "$exe" | grep -q '/usr/lib/libSystem.B.dylib' \
            || fail "$target does not name libSystem by its install path"

        undef="$(nm -u "$exe")"
        printf '%s\n' "$undef"
        if [ "$target" = "darwin-x86_64" ]; then
            printf '%s\n' "$undef" | grep -qF "_fstat\$INODE64" \
                || fail "$target does not bind _fstat\$INODE64"
            printf '%s\n' "$undef" | grep -qF "_fstatat\$INODE64" \
                || fail "$target does not bind _fstatat\$INODE64"
        else
            printf '%s\n' "$undef" | grep -qx '_fstat' \
                || fail "$target does not bind plain _fstat"
            ! printf '%s\n' "$undef" | grep -qF 'INODE64' \
                || fail "$target must not bind an INODE64 variant"
        fi
        ;;
    windows-x86_64)
        command -v llvm-readobj >/dev/null \
            || fail "llvm-readobj is unavailable on the native windows runner"
        llvm-readobj --file-headers --coff-imports "$exe"
        llvm-readobj --file-headers "$exe" | grep -q 'Format: COFF-x86-64' \
            || fail "$target did not produce x86-64 COFF"
        ;;
    *)
        fail "unsupported native evidence target $target"
        ;;
esac

echo "OK: $target native executable ran and matches its target format"
