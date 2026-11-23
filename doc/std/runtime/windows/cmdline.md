[std](../../README.md) / [runtime](../README.md) / [windows](README.md) / **cmdline**

# std.runtime.windows.cmdline

the windows command line split into arguments, as UTF-8 or as raw UTF-16,
and joined back from UTF-16 arguments

the rules are the post-2008 msvcrt rules, which the universal C runtime keeps,
so main sees what a C program's main would. arguments part at spaces and tabs outside double quotes. a run of
backslashes is literal unless a double quote follows it, and then each pair
is one backslash and an odd one left over makes the quote literal. inside
quotes a doubled quote is one literal quote. the program name, the first
argument, ends at the first space or tab outside quotes and takes every
backslash literally. an empty command line holds no arguments.

measure and fill convert each argument to UTF-8. a surrogate pair is one code
point and an unpaired surrogate becomes U+FFFD, one per code unit, so every
argument is valid UTF-8. measure_wide and fill_wide keep each argument's code
units as the line held them, unpaired surrogates included. both forms come
from one walker, so they always agree on where each argument starts and ends.

join writes arguments as a line the wide split gives back unit for unit, so
the spawns encode by the same rules the runtime decodes by.

the split and the join are pure, so they compile and are tested on every
host. the windows runtime sizes the storage it owns with the measures and then
the fills write it.

Source: [`src/runtime/windows/cmdline.mach`](../../../../src/runtime/windows/cmdline.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Size`](#size) | `rec` | the storage a command line splits into as UTF-8 |
| [`WideSize`](#widesize) | `rec` | the storage a command line splits into as UTF-16 |
| [`Joined`](#joined) | `tag` | how joining arguments into a command line ended |

| On `Size` | |
| :--- | :--- |
| [`measure`](#measure) | measure the storage a command line splits into as UTF-8 |

| On `WideSize` | |
| :--- | :--- |
| [`measure_wide`](#measure_wide) | measure the storage a command line splits into as UTF-16 |

| On `Joined` | |
| :--- | :--- |
| [`join`](#join) | join UTF-16 arguments into a command line that measure_wide and fill_wide split back into the same units |

| Functions | |
| :--- | :--- |
| [`fill`](#fill) | split a command line into UTF-8 arguments |
| [`fill_wide`](#fill_wide) | split a command line into UTF-16 arguments that keep the line's code units |

---

## Size

```mach
pub rec Size {
    count: usize;
    bytes: usize;
}
```

the storage a command line splits into as UTF-8

| Field | Type | |
| :--- | :--- | :--- |
| `count` | `usize` | number of arguments |
| `bytes` | `usize` | UTF-8 bytes of every argument, each terminator included |

### measure

```mach
pub fun measure(line: *u16) Size
```

measure the storage a command line splits into as UTF-8

| Parameter | |
| :--- | :--- |
| `line` | the command line, nul-terminated UTF-16 |
| **returns** | the argument count and their UTF-8 bytes |

## WideSize

```mach
pub rec WideSize {
    count: usize;
    units: usize;
}
```

the storage a command line splits into as UTF-16

| Field | Type | |
| :--- | :--- | :--- |
| `count` | `usize` | number of arguments |
| `units` | `usize` | UTF-16 code units of every argument, each terminator included |

### measure_wide

```mach
pub fun measure_wide(line: *u16) WideSize
```

measure the storage a command line splits into as UTF-16

| Parameter | |
| :--- | :--- |
| `line` | the command line, nul-terminated UTF-16 |
| **returns** | the argument count and their code units |

## Joined

```mach
pub tag Joined: u8 {
    unrepresentable;
    overflow;
    done: usize;
}
```

how joining arguments into a command line ended

| Case | Payload | |
| :--- | :--- | :--- |
| `unrepresentable` |  | the program name holds a double quote, which its rule cannot carry |
| `overflow` |  | the line and its terminator do not fit |
| `done` | `usize` | the units written, the terminator excluded |

### join

```mach
pub fun join(argv: **u16, buf: *u16, cap: usize) Joined
```

join UTF-16 arguments into a command line that measure_wide and fill_wide
split back into the same units

the program name follows its own rule: its units are written as they are,
quoted when it is empty or holds a space or tab, and a double quote cannot be
written at all. every later argument is quoted when it is empty or holds a
space, tab or quote, a quote is written as \\", and a run of backslashes is
doubled before a quote or the closing quote. any other unit, an unpaired
surrogate included, is copied unchanged

| Parameter | |
| :--- | :--- |
| `argv` | null-terminated array of nul-terminated UTF-16 arguments |
| `buf` | destination, nul-terminated on success |
| `cap` | size of buf in units |
| **returns** | the units written, or why the line could not be joined (buf is then unspecified) |

## Functions

### fill

```mach
pub fun fill(line: *u16, argv: **u8, bytes: *u8)
```

split a command line into UTF-8 arguments

| Parameter | |
| :--- | :--- |
| `line` | the command line, nul-terminated UTF-16 |
| `argv` | room for measure's count plus one, given the arguments and a closing nil |
| `bytes` | room for measure's bytes, given the arguments' UTF-8 |

### fill_wide

```mach
pub fun fill_wide(line: *u16, argv: **u16, units: *u16)
```

split a command line into UTF-16 arguments that keep the line's code units

| Parameter | |
| :--- | :--- |
| `line` | the command line, nul-terminated UTF-16 |
| `argv` | room for measure_wide's count plus one, given the arguments and a closing nil |
| `units` | room for measure_wide's units, given the arguments' code units |

