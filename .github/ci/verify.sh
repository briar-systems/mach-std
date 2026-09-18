#!/usr/bin/env bash
set -euo pipefail
mach="$MACH_COMPILER"

# native ELF, PE and Mach-O evidence beside the suite results
format_evidence() {
    bash test/backends/verify-native.sh "$mach" "$1" | tee "test/native/results/$1-format.log"
}

case "$MACH_CI_LEG" in
    x86_64-linux)
        bash test/native/verify.sh "$mach" linux-x86_64
        bash test/fault/verify.sh "$mach" linux-x86_64
        bash test/thread-resources/verify.sh "$mach" linux-x86_64
        bash test/thread-resources/verify-release.sh "$mach" linux-x86_64
        # the release archive carries no test-only fault module
        "$mach" build .
        bash test/fault/verify-release.sh out/linux-x86_64/debug/lib/std
        format_evidence linux-x86_64
        bash test/relro/verify.sh "$mach"
        bash test/symlink/verify.sh "$mach"
        bash test/sigpipe/verify.sh "$mach"
        bash test/terminate-child/verify.sh "$mach"
        bash test/process-status/verify.sh "$mach"
        # derive's refusals are `$error`s evidenced by a failing build, and the
        # classification is target-independent, so one leg is the whole signal
        bash test/derive/verify.sh
        bash test/secret/verify.sh
        bash test/deadline/verify.sh
        bash test/sha256/verify.sh "$mach" linux-x86_64
        ;;
    aarch64-linux)
        bash test/native/verify.sh "$mach" linux-arm64
        bash test/fault/verify.sh "$mach" linux-arm64
        bash test/thread-resources/verify.sh "$mach" linux-arm64
        format_evidence linux-arm64
        bash test/relro/verify.sh "$mach" linux-arm64
        bash test/sigpipe/verify.sh "$mach" linux-arm64
        bash test/terminate-child/verify.sh "$mach" linux-arm64
        bash test/process-status/verify.sh "$mach" linux-arm64
        bash test/sha256/verify.sh "$mach" linux-arm64
        ;;
    x86_64-windows)
        bash test/native/verify.sh "$mach" windows-x86_64
        AR=llvm-ar bash test/fault/verify.sh "$mach" windows-x86_64
        bash test/thread-resources/verify.sh "$mach" windows-x86_64
        bash test/thread-resources/verify-release.sh "$mach" windows-x86_64
        format_evidence windows-x86_64
        bash test/symlink/verify.sh "$mach" windows-x86_64
        bash test/sigpipe/verify.sh "$mach" windows-x86_64
        bash test/terminate-child/verify.sh "$mach" windows-x86_64
        CC=gcc bash test/process-status/verify.sh "$mach" windows-x86_64
        bash test/sha256/verify.sh "$mach" windows-x86_64
        ;;
    aarch64-darwin|x86_64-darwin)
        target="darwin-${MACH_CI_LEG%%-*}"
        bash test/native/verify.sh "$mach" "$target"
        bash test/fault/verify.sh "$mach" "$target"
        bash test/thread-resources/verify.sh "$mach" "$target"
        bash test/sigpipe/verify.sh "$mach" "$target"
        bash test/terminate-child/verify.sh "$mach" "$target"
        bash test/process-status/verify.sh "$mach" "$target"
        # the runtime's exit, abort, panic and argv/envp capture are only
        # observable from outside the process (#415)
        bash test/darwin/verify.sh "$mach" "$target"
        format_evidence "$target"
        bash test/sha256/verify.sh "$mach" "$target"
        ;;
    # the library suite under qemu-user is real coverage for logic and a weak
    # signal for ABI constants. it is what caught #436
    riscv64-linux)
        bash test/riscv64/verify.sh "$mach"
        python3 test/lib/compiler-census.py test/native/results test linux-riscv64
        "$mach" test . --target linux-riscv64 --runner qemu-riscv64
        python3 test/lib/compiler-census.py test/native/results test linux-riscv64 ownership
        "$mach" test . --target linux-riscv64 --runner qemu-riscv64 -O2 --filter 'ownership query'
        bash test/fault/verify.sh "$mach" linux-riscv64 qemu-riscv64
        bash test/thread-resources/verify.sh "$mach" linux-riscv64 qemu-riscv64
        bash test/relro/verify.sh "$mach" linux-riscv64 qemu-riscv64
        bash test/sigpipe/verify.sh "$mach" linux-riscv64 qemu-riscv64
        bash test/terminate-child/verify.sh "$mach" linux-riscv64 qemu-riscv64
        bash test/sha256/verify.sh "$mach" linux-riscv64 qemu-riscv64
        ;;
    cross-backends)
        bash test/backends/verify.sh
        bash test/darwin/verify.sh "$mach" darwin-x86_64 --build-only
        bash test/darwin/verify.sh "$mach" darwin-aarch64 --build-only
        ;;
    *)
        echo "verify.sh: no verifier for leg $MACH_CI_LEG" >&2
        exit 1
        ;;
esac
