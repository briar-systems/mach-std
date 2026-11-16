[std](../README.md) / [runtime](README.md) / **linux**

# std.runtime.linux

linux program entrypoint, dispatched by architecture

Source: [`src/runtime/linux.mach`](../../../src/runtime/linux.mach)

| Forwards | |
| :--- | :--- |
| [`native_args`](#native_args) | |

---

## Forwards

### native_args

Forwards the first of these whose condition holds:

- [`std.runtime.linux.x86_64.native_args`](linux/x86_64.md#native_args), where not `$mach.build.sys != $mach.sys.linux` and `$mach.build.arch == $mach.arch.x86_64`
- [`std.runtime.linux.aarch64.native_args`](linux/aarch64.md#native_args), where not `$mach.build.sys != $mach.sys.linux` and `$mach.build.arch == $mach.arch.aarch64`
- [`std.runtime.linux.riscv64.native_args`](linux/riscv64.md#native_args), where not `$mach.build.sys != $mach.sys.linux` and `$mach.build.arch == $mach.arch.riscv64`
- [`std.runtime.linux.riscv32.native_args`](linux/riscv32.md#native_args), where not `$mach.build.sys != $mach.sys.linux` and `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the kernel passed them, for std.runtime.native

