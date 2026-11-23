[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / **linux**

# std.system.os.linux

linux OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need linux-specific functionality import this module
directly rather than going through std.system.os.

The directory's root module is [`std.system.os.linux`](../linux.md).

| Module | |
| :--- | :--- |
| [`aarch64`](aarch64.md) | aarch64-specific linux OS primitives |
| [`hosted`](hosted.md) | thread creation in a loader-hosted process |
| [`riscv32`](riscv32.md) | riscv32-specific linux OS primitives |
| [`riscv64`](riscv64.md) | riscv64-specific linux OS primitives |
| [`shared`](shared.md) | code shared across all linux ISA implementations |
| [`x86_64`](x86_64.md) | x86_64-specific linux OS primitives |

