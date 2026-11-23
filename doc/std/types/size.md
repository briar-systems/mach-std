[std](../README.md) / [types](README.md) / **size**

# std.types.size

pointer-width-sized integer types

Source: [`src/types/size.mach`](../../../src/types/size.mach)

| Type | | |
| :--- | :--- | :--- |
| [`usize`](#usize) | `def` | unsigned integer for an unknown pointer width default to 64-bit size |
| [`isize`](#isize) | `def` |  |

---

## usize

Declared by the first of these arms whose condition holds.

Where `$mach.build.pointer_width == 2`:

```mach
pub def usize: u16
```

Where `$mach.build.pointer_width == 4`:

```mach
pub def usize: u32
```

Where `$mach.build.pointer_width == 8`:

```mach
pub def usize: u64
```

Otherwise:

```mach
pub def usize: u64
```

unsigned integer for an unknown pointer width
default to 64-bit size

## isize

Declared by the first of these arms whose condition holds.

Where `$mach.build.pointer_width == 2`:

```mach
pub def isize: i16
```

Where `$mach.build.pointer_width == 4`:

```mach
pub def isize: i32
```

Where `$mach.build.pointer_width == 8`:

```mach
pub def isize: i64
```

Otherwise:

```mach
pub def isize: i64
```

