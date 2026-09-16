#!/usr/bin/env bash
set -euo pipefail
case "$MACH_CI_LEG" in
    # the compiler census records that no other compiler shared this checkout
    # with the build that follows
    x86_64-linux|aarch64-darwin|x86_64-darwin)
        python3 test/lib/compiler-census.py test/native/results build .
        ;;
    # the stock qemu-user does not forward nofollow mode operations
    riscv64-linux)
        bash test/riscv64/setup-qemu.sh
        ;;
esac
