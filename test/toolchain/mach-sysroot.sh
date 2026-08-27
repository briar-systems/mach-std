#!/usr/bin/env bash
set -euo pipefail

mach="${MACH_REAL:-mach}"
library_dir="${MACH_SYSROOT_LIB:?MACH_SYSROOT_LIB must name the target libc directory}"

case "${1:-}" in
    build|run|test) exec "$mach" "$@" -L "$library_dir" ;;
    *) exec "$mach" "$@" ;;
esac
