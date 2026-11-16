[std](../README.md) / [runtime](README.md) / **wasi**

# std.runtime.wasi

wasi program entrypoint

provides `_start`, the export a wasi host calls with no arguments and no
stack of the program's own to read. mirl's prologues run from the stack
pointer global, so mach code runs from the first instruction. this entrypoint:
  1. takes the arguments and the environment from the host
  2. calls user-supplied `main(argc, argv)`
  3. ends the process through proc_exit with the code from main

user code must define:
  #[symbol("main")]
  fun main(argc: i64, argv: **u8) i64 { ... }

Source: [`src/runtime/wasi.mach`](../../../src/runtime/wasi.mach)

Uses types from [`std.runtime.native.view`](native/view.md).

| Functions | |
| :--- | :--- |
| [`_start`](#_start) | |
| [`native_args`](#native_args) | the arguments as the host passed them, which are the bytes main's argv holds |

---

## Functions

### _start

```mach
#[symbol("_start")]
pub fun _start()
```

### native_args

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the host passed them, which are the bytes main's argv holds

