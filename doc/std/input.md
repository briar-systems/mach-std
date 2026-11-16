[std](README.md) / **input**

# std.input

line input from stdin

the read-side twin of std.print: convenience wrappers that read whole lines
from stdin, backed by the filesystem stdin file. this is plain canonical
input -- it works on ttys, pipes, and file redirects with no tty required
(raw single-key polling is std.terminal's concern).

a line read has two failure classes: the reader's own outcome (the end of
the stream, a stall, a native failure), which passes through as the ReadError
with the bytes buffered so far as its progress, and a line the caller's
buffer cannot hold, which is this module's own case.

Source: [`src/input.mach`](../../src/input.mach)

Uses types from [`std.io.reader`](io/reader.md).

| Type | | |
| :--- | :--- | :--- |
| [`InputError`](#inputerror) | `tag` | every way a line read can fail |

| On `InputError` | |
| :--- | :--- |
| [`read_line_from`](#read_line_from) | read one line from a reader into buf, up to cap bytes including the terminator |
| [`read_line`](#read_line) | read one line from stdin into buf, up to cap bytes including the terminator |

---

## InputError

```mach
pub tag InputError: u8 {
    read:     ReadError;
    too_long: usize;
}
```

every way a line read can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `read` | `ReadError` | the reader failed; the payload's progress is the bytes buffered before the outcome, and eof{0} is the end of input with nothing buffered (a final line without a newline is not an error) |
| `too_long` | `usize` | the line does not fit; payload is the bytes buffered. the byte that overflowed was consumed from the reader and dropped, so the next call continues after it |

### read_line_from

```mach
pub fun read_line_from(r: *std.io.reader.Reader, buf: *u8, cap: usize) res[usize, InputError]
```

read one line from a reader into buf, up to cap bytes including the terminator

reads a byte at a time until a newline, EOF, or the buffer fills. strips a
trailing "\\r\\n" or "\\n" and null-terminates; the returned length excludes the
terminator. a line longer than cap-1 bytes is too_long rather than a silent
truncation: the bytes that fit are in buf, the byte that overflowed has been
consumed and dropped (a reader has no pushback), and the next call continues
with the rest of the line. a read at end of input with no bytes buffered is
read{eof{0}} -- distinct from an empty line, which is ok{0}.

| Parameter | |
| :--- | :--- |
| `r` | reader to draw from |
| `buf` | destination buffer |
| `cap` | buffer capacity in bytes (at least 1 for the terminator; a zero cap holds no line, so it is too_long{0} before anything is read) |
| **returns** | line length excluding the terminator, or the failure |

### read_line

```mach
pub fun read_line(buf: *u8, cap: usize) res[usize, InputError]
```

read one line from stdin into buf, up to cap bytes including the terminator

a thin wrapper over read_line_from drawing from the stdin file; see there for
the trimming, truncation, and end-of-input semantics.

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `cap` | buffer capacity in bytes (must be at least 1 for the terminator) |
| **returns** | line length excluding the terminator, or the failure |

