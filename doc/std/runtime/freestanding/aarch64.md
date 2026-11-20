[std](../../README.md) / [runtime](../README.md) / [freestanding](README.md) / **aarch64**

# std.runtime.freestanding.aarch64

aarch64 freestanding entrypoint

Source: [`src/runtime/freestanding/aarch64.mach`](../../../../src/runtime/freestanding/aarch64.mach)

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

