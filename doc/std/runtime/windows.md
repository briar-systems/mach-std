[std](../README.md) / [runtime](README.md) / **windows**

# std.runtime.windows

windows program entrypoint, dispatched by architecture

Source: [`src/runtime/windows.mach`](../../../src/runtime/windows.mach)

| Forwards | |
| :--- | :--- |
| [`native_args`](#native_args) | |

---

## Forwards

### native_args

Forwards the first of these whose condition holds:

- [`std.runtime.windows.x86_64.native_args`](windows/x86_64.md#native_args), where not `$mach.build.sys != $mach.sys.windows` and `$mach.build.arch == $mach.arch.x86_64`
- [`std.runtime.windows.aarch64.native_args`](windows/aarch64.md#native_args), where not `$mach.build.sys != $mach.sys.windows` and `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the UTF-16 units the command line held, for std.runtime.native

