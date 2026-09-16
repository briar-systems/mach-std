#!/usr/bin/env bash
# builds a pinned riscv64 user emulator that forwards nofollow mode operations,
# which the stock qemu-user does not, and puts it on the job's PATH
set -euo pipefail
sudo apt-get update
sudo apt-get install -y ninja-build libglib2.0-dev libpixman-1-dev python3-venv
source_dir="$(mktemp -d "$RUNNER_TEMP/mach-qemu.XXXXXX")"
trap 'rm -rf -- "$source_dir"' EXIT
git clone --depth 1 --branch v10.1.0 https://github.com/qemu/qemu "$source_dir/source"
actual="$(git -C "$source_dir/source" rev-parse HEAD)"
expected=f8b2f64e2336a28bf0d50b6ef8a7d8c013e9bcf3
[ "$actual" = "$expected" ] || { echo 'QEMU source differs from the selected commit' >&2; exit 1; }
cd "$source_dir/source"
./configure --target-list=riscv64-linux-user --disable-system --disable-docs --disable-tools --disable-guest-agent
make -j2
mkdir -p "$GITHUB_WORKSPACE/.qemu-toolchain"
cp build/qemu-riscv64 "$GITHUB_WORKSPACE/.qemu-toolchain/qemu-riscv64"
printf '%s\n' "$actual" > "$GITHUB_WORKSPACE/.qemu-toolchain/source.txt"
"$GITHUB_WORKSPACE/.qemu-toolchain/qemu-riscv64" --version
echo "$GITHUB_WORKSPACE/.qemu-toolchain" >> "$GITHUB_PATH"
