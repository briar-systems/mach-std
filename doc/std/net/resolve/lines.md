[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **lines**

# std.net.resolve.lines

bounded line iteration over resolver configuration files

Source: [`src/net/resolve/lines.mach`](../../../../src/net/resolve/lines.mach)

Uses types from [`std.io.error`](../../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Reader`](#reader) | `rec` | a buffered reader yielding one nul-terminated line at a time |

| On `Reader` | |
| :--- | :--- |
| [`open`](#open) | open path for reading and reset the reader |
| [`close`](#close) | release the descriptor |
| [`next`](#next) | copy the next line into output without its LF or CRLF ending, nul-terminated |

| Constants | |
| :--- | :--- |
| [`MAX_LINE`](#constants) | |

---

## Reader

```mach
pub rec Reader {
    fd:   usize;
    buf:  [1024]u8;
    len:  usize;
    pos:  usize;
    done: bool;
}
```

a buffered reader yielding one nul-terminated line at a time

| Field | Type | |
| :--- | :--- | :--- |
| `fd` | `usize` | open handle, or os.INVALID_HANDLE when closed |
| `buf` | `[1024]u8` | read-ahead storage |
| `len` | `usize` | valid bytes in buf |
| `pos` | `usize` | next unread byte in buf |
| `done` | `bool` | no more bytes will arrive from fd |

### open

```mach
pub fun open(reader: *Reader, path: str) err[std.io.error.Error]
```

open path for reading and reset the reader

a failed open leaves the reader untouched

| Parameter | |
| :--- | :--- |
| `reader` | the reader to open |
| `path` | the file, relative to the working directory when not absolute |
| **returns** | ok, or the open failure |

### close

```mach
pub fun close(reader: *Reader) err[std.io.error.Error]
```

release the descriptor. a reader that is already closed (its fd is
os.INVALID_HANDLE) closes as a success, a refused native close is the failure

### next

```mach
pub fun next(reader: *Reader, output: *u8, capacity: usize) res[opt[usize], std.io.error.Error]
```

copy the next line into output without its LF or CRLF ending, nul-terminated

a line longer than capacity - 1 bytes is consumed whole but truncated in
output; the returned length is the untruncated length so the caller can
detect and skip it. the end of the file is absence, a read failure is the
error, and a zero capacity is invalid use.

| Parameter | |
| :--- | :--- |
| `reader` | the reader to advance |
| `output` | destination for the line bytes |
| `capacity` | size of output in bytes |
| **returns** | the untruncated line length, absent when exhausted, or the failure |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_LINE` | `usize` | `512` |  |

