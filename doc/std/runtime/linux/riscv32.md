[std](../../README.md) / [runtime](../README.md) / [linux](README.md) / **riscv32**

# std.runtime.linux.riscv32

riscv32 (ilp32) linux entrypoint

Source: [`src/runtime/linux/riscv32.mach`](../../../../src/runtime/linux/riscv32.mach)

Uses types from [`std.runtime.native.view`](../native/view.md).

| Functions | |
| :--- | :--- |
| [`native_args`](#native_args) | the arguments as the kernel passed them, for std.runtime.native |
| [`_start`](#_start) | the ELF entry, the steps the module comment lists |

---

## Functions

### native_args

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the kernel passed them, for std.runtime.native

| Parameter | |
| :--- | :--- |
| **returns** | argc and argv, which are already the native bytes |

### _start

```mach
#[naked]
#[symbol("_start")]
pub fun _start()
```

the ELF entry, the steps the module comment lists

