[std](../README.md) / [io](README.md) / **reader**

# std.io.reader

generic reader interface

backend-agnostic read interface using ctx + fn_ptr dispatch. concrete
sources (fd, buffer, etc.) build a Reader from their context and read callback.

a source hands over what it knows: the bytes it delivered, or the native
failure it hit. this module classifies the outcome once, in read(): zero
bytes for a nonzero request is the end of the stream, and a native failure
whose kind is WOULD_BLOCK is a stall. a source may also spell those cases
itself; read() passes them through unchanged. the composite operations
(read_exact, read_all, read_str) carry the bytes delivered before the outcome
in the error payload, so a caller always knows how far the stream advanced.

Source: [`src/io/reader.mach`](../../../src/io/reader.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.io.error`](error.md).

| Type | | |
| :--- | :--- | :--- |
| [`ReadFailure`](#readfailure) | `rec` | a native failure and the bytes delivered before it |
| [`ReadError`](#readerror) | `tag` | every way a read can fail |
| [`ReadFun`](#readfun) | `def` | read callback type |
| [`Reader`](#reader) | `rec` | generic read interface |

| On `ReadError` | |
| :--- | :--- |
| [`native_failure`](#native_failure) | a native failure as a read error |
| [`advance`](#advance) | add the bytes delivered by earlier calls to the error's progress |

| On `Reader` | |
| :--- | :--- |
| [`read`](#read) | read up to len bytes into buf |
| [`read_exact`](#read_exact) | read exactly len bytes into buf |
| [`read_all`](#read_all) | read until EOF into a fresh vector |
| [`read_str`](#read_str) | read until EOF and return the content as an owned, null-terminated string |

---

## ReadFailure

```mach
pub rec ReadFailure {
    delivered: usize;
    error:     std.io.error.Error;
}
```

a native failure and the bytes delivered before it

## ReadError

```mach
pub tag ReadError: u8 {
    eof:         usize;
    would_block: usize;
    native:      ReadFailure;
    alloc:       std.allocator.Error;
}
```

every way a read can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `eof` | `usize` | the stream ended; payload is the bytes delivered before the end |
| `would_block` | `usize` | the source stalled (EAGAIN); payload is the bytes delivered first |
| `native` | `ReadFailure` | the source failed; payload carries the failure and the bytes delivered before it |
| `alloc` | `std.allocator.Error` | growth was refused (read_all, read_str); nothing is delivered and the caller's allocator is exactly as it was |

### native_failure

```mach
pub fun native_failure(delivered: usize, error: std.io.error.Error) ReadError
```

a native failure as a read error

| Parameter | |
| :--- | :--- |
| `delivered` | bytes delivered before the failure |
| `error` | the native failure |
| **returns** | the native case carrying both |

### advance

```mach
pub fun advance(error: ReadError, delivered: usize) ReadError
```

add the bytes delivered by earlier calls to the error's progress

## ReadFun

```mach
pub def ReadFun: fun(ptr, *u8, usize) res[usize, ReadError]
```

read callback type

| Field | Type | |
| :--- | :--- | :--- |
| `ptr` |  | opaque context passed to the read callback |
| `buf` |  | buffer to read into |
| `len` |  | maximum number of bytes to read, never zero |
| `ret` |  | bytes delivered (zero at the end of the stream) or the failure |

## Reader

```mach
pub rec Reader {
    ctx:     ptr;
    fn_read: ReadFun;
}
```

generic read interface

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to the read callback |
| `fn_read` | `ReadFun` | read callback (ctx, buf, len) -> res[usize, ReadError] |

### read

```mach
pub fun read(r: *Reader, buf: *u8, len: usize) res[usize, ReadError]
```

read up to len bytes into buf

| Parameter | |
| :--- | :--- |
| `r` | reader to read from |
| `buf` | buffer to read into |
| `len` | maximum number of bytes to read |
| **returns** | bytes delivered, or eof, would_block or the native failure; ok{0} only for a zero-length request |

### read_exact

```mach
pub fun read_exact(r: *Reader, buf: *u8, len: usize) err[ReadError]
```

read exactly len bytes into buf

| Parameter | |
| :--- | :--- |
| `r` | reader to read from |
| `buf` | buffer to fill |
| `len` | number of bytes to read |
| **returns** | the failure with the bytes delivered before it, or ok |

### read_all

```mach
pub fun read_all(a: *std.allocator.Allocator, r: *Reader) res[Vector[u8], ReadError]
```

read until EOF into a fresh vector

the caller owns the returned vector. on failure nothing is returned and the
vector's storage has already been released; the error carries the bytes the
source delivered before it failed.

| Parameter | |
| :--- | :--- |
| `a` | allocator to use |
| `r` | reader to read from |
| **returns** | the content, or the failure |

### read_str

```mach
pub fun read_str(a: *std.allocator.Allocator, r: *Reader) res[OwnedString, ReadError]
```

read until EOF and return the content as an owned, null-terminated string

the vector's buffer is terminated in place and adopted whole: the string's
extent is the buffer's capacity and owned_dnit returns it all at once.

| Parameter | |
| :--- | :--- |
| `a` | allocator to use |
| `r` | reader to read from |
| **returns** | the content as an owned string, or the failure |

