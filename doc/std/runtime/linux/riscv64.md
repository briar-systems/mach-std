[std](../../README.md) / [runtime](../README.md) / [linux](README.md) / **riscv64**

# std.runtime.linux.riscv64

riscv64 (lp64) linux entrypoint

Source: [`src/runtime/linux/riscv64.mach`](../../../../src/runtime/linux/riscv64.mach)

Uses types from [`std.runtime.native.view`](../native/view.md).

| Functions | |
| :--- | :--- |
| [`native_args`](#native_args) | the arguments as the kernel passed them, for std.runtime.native |
| [`_start`](#_start) | |

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

