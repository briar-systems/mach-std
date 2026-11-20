[std](../../README.md) / [runtime](../README.md) / [windows](README.md) / **aarch64**

# std.runtime.windows.aarch64

aarch64 Windows entrypoint

provides `_start` (via `mainCRTStartup`), the PE entry point for aarch64
Windows executables.

windows does not pass argc/argv on the stack. this entrypoint:
  1. calls _rt_init to install the main thread's block
  2. calls _rt_args, which reads GetCommandLineW and splits it into UTF-8
     arguments and into the UTF-16 ones std.runtime.native reads, in
     storage it allocates, with no cap on their count
     (std.runtime.windows.cmdline holds the rules)
  3. calls user-supplied `main(argc, argv)`
  4. exits via ExitProcess with the return code from main

user code must define:
  #[symbol("main")]
  fun main(argc: i64, argv: **u8) i64 { ... }

Source: [`src/runtime/windows/aarch64.mach`](../../../../src/runtime/windows/aarch64.mach)

Uses types from [`std.runtime.native.view`](../native/view.md).

| Functions | |
| :--- | :--- |
| [`native_args`](#native_args) | the arguments as the UTF-16 units the command line held, for std.runtime.native |
| [`_start`](#_start) | the PE entry, the steps the module comment lists |

---

## Functions

### native_args

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the UTF-16 units the command line held, for std.runtime.native

| Parameter | |
| :--- | :--- |
| **returns** | the wide split _rt_args filled before main |

### _start

```mach
#[naked]
#[symbol("mainCRTStartup")]
pub fun _start()
```

the PE entry, the steps the module comment lists

