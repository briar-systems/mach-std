[std](../../README.md) / [runtime](../README.md) / [freestanding](README.md) / **riscv32**

# std.runtime.freestanding.riscv32

riscv32 freestanding entrypoint

Source: [`src/runtime/freestanding/riscv32.mach`](../../../../src/runtime/freestanding/riscv32.mach)

| Functions | |
| :--- | :--- |
| [`_start`](#_start) | the image entry, the steps the module comment lists |

---

## Functions

### _start

```mach
#[naked]
#[section(".start")]
#[symbol("_start")]
pub fun _start()
```

the image entry, the steps the module comment lists

