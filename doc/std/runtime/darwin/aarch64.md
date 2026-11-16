[std](../../README.md) / [runtime](../README.md) / [darwin](README.md) / **aarch64**

# std.runtime.darwin.aarch64

aarch64 darwin entrypoint

provides `_start` (via `start`), the Mach-O entry point for aarch64 darwin executables.

darwin arm64 executables are PIE `LC_MAIN` images: dyld enters the program like a
C `main(argc, argv, envp)`, with the arguments in registers, not on the stack:
  x0 = argc
  x1 = argv
  x2 = envp

this entrypoint:
  1. captures argc/argv/envp from x0/x1/x2 for the runtime
  2. calls `_rt_init` then `main(argc, argv)` (the stack dyld hands the LC_MAIN
     entry is already 16-byte aligned, an arm64 invariant)
  3. exits through `_rt_exit`, which is `_exit(2)` via libSystem, with the
     return code from main. the entry never returns to dyld: `exit(3)` would
     run atexit handlers std never registers, and a raw exit trap is exactly
     the unsupported surface this runtime no longer touches.

user code must define:
  #[symbol("main")]
  fun main(argc: i64, argv: **u8) i64 { ... }

Source: [`src/runtime/darwin/aarch64.mach`](../../../../src/runtime/darwin/aarch64.mach)

Uses types from [`std.runtime.native.view`](../native/view.md).

| Functions | |
| :--- | :--- |
| [`native_args`](#native_args) | the arguments as the kernel passed them, for std.runtime.native |
| [`_start`](#_start) | the asm names each symbol as mach-o spells it, with a leading underscore |

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
#[symbol("start")]
pub fun _start()
```

the asm names each symbol as mach-o spells it, with a leading underscore

