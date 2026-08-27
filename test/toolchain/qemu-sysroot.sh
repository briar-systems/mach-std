#!/usr/bin/env bash
set -euo pipefail

qemu="${QEMU_REAL:?QEMU_REAL must name the target qemu-user executable}"
sysroot="${QEMU_SYSROOT:?QEMU_SYSROOT must name the target runtime root}"

exec "$qemu" -L "$sysroot" "$@"
