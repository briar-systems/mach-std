[std](../../README.md) / [runtime](../README.md) / [native](README.md) / **view**

# std.runtime.native.view

the shape of the native argument view, shared by std.runtime.native and the runtimes that own the arguments

Source: [`src/runtime/native/view.mach`](../../../../src/runtime/native/view.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Unit`](#unit) | `def` | one unit of a native argument: a UTF-16 code unit on windows, a byte elsewhere |
| [`Args`](#args) | `rec` | the process arguments in native units |
| [`NativeName`](#nativename) | `rec` | a nul-terminated string in native units, owned by whoever allocated it |

---

## Unit

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

## Args

```mach
pub rec Args {
    count: usize;
    argv:  **Unit;
}
```

the process arguments in native units

| Field | Type | |
| :--- | :--- | :--- |
| `count` | `usize` | number of arguments, the program name included |
| `argv` | `**Unit` | the arguments, each nul-terminated, and a closing nil |

## NativeName

```mach
pub rec NativeName {
    units:  *Unit;
    length: usize;
}
```

a nul-terminated string in native units, owned by whoever allocated it

| Field | Type | |
| :--- | :--- | :--- |
| `units` | `*Unit` | the units, length + 1 with the terminator |
| `length` | `usize` | its length in units |

