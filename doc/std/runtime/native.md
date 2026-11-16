[std](../README.md) / [runtime](README.md) / **native**

# std.runtime.native

the process arguments as the host passed them, before any conversion

main's argv is UTF-8 on every host. on linux, darwin and wasi it is the bytes the
host passed, so the native view holds the same arguments. on windows argv is
converted from the wide command line and an unpaired surrogate, which a file
name may hold, becomes U+FFFD, so such a name does not survive in argv. the
native view there holds each argument as the UTF-16 code units the command
line held, split by the same walker as argv (std.runtime.windows.cmdline), so
both views have the same count and each index names the same argument.

a program that must reopen a name exactly as it was given reads it here, in
the host's own units, through one shape on every host. the runtime that owns
the arguments keeps the view and is its only writer, so it is read only here
and lives as long as the process.

Source: [`src/runtime/native.mach`](../../../src/runtime/native.mach)

| Functions | |
| :--- | :--- |
| [`args`](#args) | the process arguments in native units |
| [`get`](#get) | the argument at an index |

| Forwards | |
| :--- | :--- |
| [`Unit`](#unit), [`Args`](#args-1) | |

---

## Functions

### args

```mach
pub fun args() Args
```

the process arguments in native units

| Parameter | |
| :--- | :--- |
| **returns** | the view the selected runtime keeps for the life of the process |

### get

```mach
pub fun get(a: Args, idx: usize) opt[*Unit]
```

the argument at an index

| Parameter | |
| :--- | :--- |
| `a` | the arguments |
| `idx` | argument index, 0 the program name |
| **returns** | the argument's units, or none when the index is out of range |

## Forwards

### Unit

Forwards [`std.runtime.native.view.Unit`](native/view.md#unit).

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub def Unit: u16
```

Otherwise:

```mach
pub def Unit: u8
```

one unit of a native argument: a UTF-16 code unit on windows, a byte elsewhere

### Args

Forwards [`std.runtime.native.view.Args`](native/view.md#args).

```mach
pub rec Args {
    count: usize;
    argv:  **Unit;
}
```

the process arguments in native units

