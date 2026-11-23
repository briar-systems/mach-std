[std](../README.md) / [runtime](README.md) / **darwin**

# std.runtime.darwin

darwin program entrypoint, dispatched by architecture

Source: [`src/runtime/darwin.mach`](../../../src/runtime/darwin.mach)

| Forwards | |
| :--- | :--- |
| [`native_args`](#native_args) | |

---

## Forwards

### native_args

Forwards the first of these whose condition holds:

- [`std.runtime.darwin.aarch64.native_args`](darwin/aarch64.md#native_args), where not `$mach.build.sys != $mach.sys.darwin` and `$mach.build.arch == $mach.arch.aarch64`
- [`std.runtime.darwin.x86_64.native_args`](darwin/x86_64.md#native_args), where not `$mach.build.sys != $mach.sys.darwin` and `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun native_args() std.runtime.native.view.Args
```

the arguments as the kernel passed them, for std.runtime.native

