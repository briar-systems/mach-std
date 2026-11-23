[std](README.md) / **print**

# std.print

formatted output to stdout/stderr

print, println, eprint and eprintln hand their text, and the newline, to the
file in one gather write. the rest format through std.format into a staging
buffer drained to the file. checked printing stays checked: every function
reports the writer's outcome, and the printf family adds the format string's
failures on top.

Source: [`src/print.mach`](../../src/print.mach)

| Functions | |
| :--- | :--- |
| [`print`](#print) | write s to stdout |
| [`println`](#println) | write s followed by a newline to stdout |
| [`eprint`](#eprint) | write s to stderr |
| [`eprintln`](#eprintln) | write s followed by a newline to stderr |
| [`u64`](#u64) | write unsigned 64-bit integer to stdout |
| [`eu64`](#eu64) | write unsigned 64-bit integer to stderr |
| [`printf`](#printf) | formatted output to stdout |
| [`eprintf`](#eprintf) | formatted output to stderr |
| [`printlnf`](#printlnf) | formatted output to stdout followed by a newline |
| [`eprintlnf`](#eprintlnf) | formatted output to stderr followed by a newline |

---

## Functions

### print

```mach
pub fun print(s: str) res[usize, WriteError]
```

write s to stdout

| Parameter | |
| :--- | :--- |
| `s` | string to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### println

```mach
pub fun println(s: str) res[usize, WriteError]
```

write s followed by a newline to stdout

| Parameter | |
| :--- | :--- |
| `s` | string to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### eprint

```mach
pub fun eprint(s: str) res[usize, WriteError]
```

write s to stderr

| Parameter | |
| :--- | :--- |
| `s` | string to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### eprintln

```mach
pub fun eprintln(s: str) res[usize, WriteError]
```

write s followed by a newline to stderr

| Parameter | |
| :--- | :--- |
| `s` | string to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### u64

```mach
pub fun u64(n: u64) res[usize, WriteError]
```

write unsigned 64-bit integer to stdout

| Parameter | |
| :--- | :--- |
| `n` | value to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### eu64

```mach
pub fun eu64(n: u64) res[usize, WriteError]
```

write unsigned 64-bit integer to stderr

| Parameter | |
| :--- | :--- |
| `n` | value to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### printf

```mach
pub fun printf(fmt: str, va: ...) res[usize, FormatError]
```

formatted output to stdout

| Parameter | |
| :--- | :--- |
| `fmt` | format string (see std.format.vformat for hole syntax) |
| `va` | comptime variadic argument pack |
| **returns** | bytes written, or the format's failure |

### eprintf

```mach
pub fun eprintf(fmt: str, va: ...) res[usize, FormatError]
```

formatted output to stderr

| Parameter | |
| :--- | :--- |
| `fmt` | format string (see std.format.vformat for hole syntax) |
| `va` | comptime variadic argument pack |
| **returns** | bytes written, or the format's failure |

### printlnf

```mach
pub fun printlnf(fmt: str, va: ...) res[usize, FormatError]
```

formatted output to stdout followed by a newline

| Parameter | |
| :--- | :--- |
| `fmt` | format string (see std.format.vformat for hole syntax) |
| `va` | comptime variadic argument pack |
| **returns** | bytes written, or the format's failure |

### eprintlnf

```mach
pub fun eprintlnf(fmt: str, va: ...) res[usize, FormatError]
```

formatted output to stderr followed by a newline

| Parameter | |
| :--- | :--- |
| `fmt` | format string (see std.format.vformat for hole syntax) |
| `va` | comptime variadic argument pack |
| **returns** | bytes written, or the format's failure |

