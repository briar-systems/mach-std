[std](../README.md) / [args](README.md) / **help**

# std.args.help

a neutral help page rendered from the records std.args reads a command line against

the page of a command is its usage line, its help text, the commands nested
under it and its flag table, wrapped at word boundaries to the width given,
clamped to 56 through 240 columns. it is written straight to a writer and
nothing is allocated, so a program that writes to an unbuffered stream wraps
it in io.writer.buffered first. the page is opt-in: a program decides when to
print it and what follows.

Source: [`src/args/help.mach`](../../../src/args/help.mach)

Uses types from [`std.args`](../args.md).

| Functions | |
| :--- | :--- |
| [`terminal_width`](#terminal_width) | the terminal width COLUMNS names, clamped to 56 through 240, and 100 when it is unset or not a number |
| [`render`](#render) | write the page of the command a parsed line matched, wrapped to a width: the usage line of the path's command words, the command's help text, its nested commands and its flags |

---

## Functions

### terminal_width

```mach
pub fun terminal_width() usize
```

the terminal width COLUMNS names, clamped to 56 through 240, and 100 when it is unset or not a
number

### render

```mach
pub fun render(p: *std.args.Parsed, w: *Writer, width: usize) err[WriteError]
```

write the page of the command a parsed line matched, wrapped to a width: the usage line of the
path's command words, the command's help text, its nested commands and its flags

| Parameter | |
| :--- | :--- |
| `p` | the parsed line |
| `w` | the destination |
| `width` | columns, clamped to 56 through 240 |
| **returns** | ok, or the write that failed |

