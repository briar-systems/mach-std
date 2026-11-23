[std](../README.md) / [io](README.md) / **writer**

# std.io.writer

generic writer interface

backend-agnostic write interface using ctx + fn_ptr dispatch. concrete
sinks (fd, buffer, etc.) build a Writer from their context and write callback.

a sink hands over what it knows: the bytes it accepted, or the native
failure it hit. this module classifies the outcome once, in write(): zero
bytes accepted for a nonzero request is a stall, and a native failure whose
kind is WOULD_BLOCK is a would_block. a sink may also spell those cases
itself; write() passes them through unchanged. write_all and write_str carry
the persisted prefix in the error payload, so a caller always knows how many
bytes the sink accepted before the outcome.

Source: [`src/io/writer.mach`](../../../src/io/writer.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.io.error`](error.md).

| Type | | |
| :--- | :--- | :--- |
| [`WriteFailure`](#writefailure) | `rec` | a native failure and the bytes persisted before it |
| [`WriteError`](#writeerror) | `tag` | every way a write can fail |
| [`WriteFun`](#writefun) | `def` | write callback type |
| [`Writer`](#writer) | `rec` | generic write interface |
| [`Buffered`](#buffered) | `rec` | a writer that stages bytes in a caller-provided buffer |
| [`Memory`](#memory) | `rec` | a writer into memory |

| On `WriteError` | |
| :--- | :--- |
| [`native_failure`](#native_failure) | a native failure as a write error |
| [`persisted`](#persisted) | the bytes the sink persisted before the failure |
| [`classify`](#classify) | a stall reported as a native error is the would_block case, which write() applies to every sink's failure and a caller that writes past a Writer applies to its own |
| [`advance`](#advance) | add the bytes persisted by earlier calls to the error's prefix |
| [`reprefix`](#reprefix) | the same failure with its persisted prefix replaced |

| On `Writer` | |
| :--- | :--- |
| [`write`](#write) | write up to len bytes from buf |
| [`write_all`](#write_all) | write exactly len bytes from buf |
| [`write_str`](#write_str) | write a null-terminated string |

| On `Buffered` | |
| :--- | :--- |
| [`buffered`](#buffered-1) | wire a buffered writer over inner |
| [`flush`](#flush) | hand every staged byte to the inner writer |
| [`pushed`](#pushed) | bytes the inner writer has taken over this buffer's life |

| On `Memory` | |
| :--- | :--- |
| [`memory`](#memory-1) | wire a writer into caller storage |
| [`memory_growing`](#memory_growing) | wire a writer into storage it grows through alloc |
| [`memory_dnit`](#memory_dnit) | release the storage a growing memory holds; a fixed memory holds none |
| [`memory_text`](#memory_text) | the written bytes as text, terminated in place; empty before any write |

---

## WriteFailure

```mach
pub rec WriteFailure {
    written: usize;
    error:   std.io.error.Error;
}
```

a native failure and the bytes persisted before it

## WriteError

```mach
pub tag WriteError: u8 {
    stalled:     usize;
    would_block: usize;
    native:      WriteFailure;
}
```

every way a write can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `stalled` | `usize` | the sink accepted nothing; payload is the persisted prefix |
| `would_block` | `usize` | the sink stalled natively (EAGAIN); payload is the prefix |
| `native` | `WriteFailure` | the sink failed; payload carries the failure and the prefix |

### native_failure

```mach
pub fun native_failure(written: usize, error: std.io.error.Error) WriteError
```

a native failure as a write error

| Parameter | |
| :--- | :--- |
| `written` | bytes persisted before the failure |
| `error` | the native failure |
| **returns** | the native case carrying both |

### persisted

```mach
pub fun persisted(error: WriteError) usize
```

the bytes the sink persisted before the failure

### classify

```mach
pub fun classify(error: WriteError) WriteError
```

a stall reported as a native error is the would_block case, which write()
applies to every sink's failure and a caller that writes past a Writer applies
to its own

### advance

```mach
pub fun advance(error: WriteError, written: usize) WriteError
```

add the bytes persisted by earlier calls to the error's prefix

### reprefix

```mach
pub fun reprefix(error: WriteError, written: usize) WriteError
```

the same failure with its persisted prefix replaced

## WriteFun

```mach
pub def WriteFun: fun(ptr, *u8, usize) res[usize, WriteError]
```

write callback type

| Field | Type | |
| :--- | :--- | :--- |
| `ptr` |  | opaque context passed to the write callback |
| `buf` |  | buffer to write from |
| `len` |  | number of bytes to write, never zero |
| `ret` |  | bytes accepted (zero when the sink stalls) or the failure |

## Writer

```mach
pub rec Writer {
    ctx:      ptr;
    fn_write: WriteFun;
}
```

generic write interface

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to the write callback |
| `fn_write` | `WriteFun` | write callback (ctx, buf, len) -> res[usize, WriteError] |

### write

```mach
pub fun write(w: *Writer, buf: *u8, len: usize) res[usize, WriteError]
```

write up to len bytes from buf

| Parameter | |
| :--- | :--- |
| `w` | writer to write to |
| `buf` | buffer to write from |
| `len` | maximum number of bytes to write |
| **returns** | bytes accepted, or stalled, would_block or the native failure; ok{0} only for a zero-length request |

### write_all

```mach
pub fun write_all(w: *Writer, buf: *u8, len: usize) err[WriteError]
```

write exactly len bytes from buf

| Parameter | |
| :--- | :--- |
| `w` | writer to write to |
| `buf` | buffer to write from |
| `len` | number of bytes to write |
| **returns** | the failure with the persisted prefix, or ok |

### write_str

```mach
pub fun write_str(w: *Writer, s: str) err[WriteError]
```

write a null-terminated string

| Parameter | |
| :--- | :--- |
| `w` | writer to write to |
| `s` | string to write |
| **returns** | the failure with the persisted prefix, or ok |

## Buffered

```mach
pub rec Buffered {
    inner:  *Writer;
    buf:    *u8;
    cap:    usize;
    len:    usize;
    taken:  usize;
    pushed: usize;
    failed: bool;
    error:  WriteError;
}
```

a writer that stages bytes in a caller-provided buffer

ctx for a Writer whose sink batches into `buf` and forwards full buffers to
`inner`. the caller owns the storage and the flush: nothing leaves the
buffer until it fills, a request at least as large as the capacity goes
straight through, or flush() is called.

accounting. a byte count returned by the staging sink is provisional: the
bytes are in the buffer, not at the inner writer. `pushed` is the
authoritative count of bytes the inner writer took over this buffer's life,
and a caller that must report a true total reads it after flush(). the
staging sink still reports a per-call prefix the way an unbuffered sink
does, measured against the bytes it had already handed back, so a failure
that loses only bytes from the current call is exact; a failure that loses
bytes acknowledged by an earlier call cannot be spelled as a negative prefix
and reports zero, which is why `pushed` exists.

a failure is sticky. the first refusal from the inner writer is retained,
every later staging call and flush() replays it with a zero prefix, and the
staged bytes are dropped, so a caller driving a long format stops at the
failure instead of formatting into a buffer that will never reach the sink.

| Field | Type | |
| :--- | :--- | :--- |
| `inner` | `*Writer` | the writer full buffers are forwarded to |
| `buf` | `*u8` | caller-owned staging storage |
| `cap` | `usize` | capacity of buf in bytes |
| `len` | `usize` | bytes currently staged |
| `taken` | `usize` | bytes the staging sink has handed back as accepted |
| `pushed` | `usize` | bytes the inner writer has persisted over this buffer's life |
| `failed` | `bool` | true once the inner writer has refused |
| `error` | `WriteError` | the first refusal, retained for replay |

### buffered

```mach
pub fun buffered(b: *Buffered, inner: *Writer, buf: *u8, cap: usize) Writer
```

wire a buffered writer over inner

| Parameter | |
| :--- | :--- |
| `b` | buffer state, owned by the caller for the writer's whole life |
| `inner` | writer full buffers are forwarded to |
| `buf` | staging storage, owned by the caller |
| `cap` | capacity of buf in bytes; zero degrades to an unbuffered passthrough |
| **returns** | a Writer staging into b |

### flush

```mach
pub fun flush(b: *Buffered) err[WriteError]
```

hand every staged byte to the inner writer

| Parameter | |
| :--- | :--- |
| `b` | buffer to drain |
| **returns** | the refusal with the prefix of the staged bytes it took, or ok |

### pushed

```mach
pub fun pushed(b: *Buffered) usize
```

bytes the inner writer has taken over this buffer's life

## Memory

```mach
pub rec Memory {
    alloc: *std.allocator.Allocator;
    buf:   *u8;
    cap:   usize;
    len:   usize;
    limit: opt[usize];
}
```

a writer into memory

ctx for a Writer whose sink appends to `buf`. a fixed memory writes into
caller storage and accepts what fits, so a full one stalls; a growing memory
owns `buf` and grows it through `alloc`, failing natively when the allocator
refuses. either keeps one byte past the written bytes free, so text() can
terminate them. a limit scripts a refusal: once `limit` bytes are held, every
write fails natively, and a write that crosses it is cut at the limit.

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | grows buf; nil for a fixed memory |
| `buf` | `*u8` | the written bytes |
| `cap` | `usize` | capacity of buf in bytes |
| `len` | `usize` | bytes written |
| `limit` | `opt[usize]` | the bytes held before every write is refused, or none |

### memory

```mach
pub fun memory(m: *Memory, buf: *u8, cap: usize) Writer
```

wire a writer into caller storage

| Parameter | |
| :--- | :--- |
| `m` | memory state, owned by the caller for the writer's whole life |
| `buf` | storage, owned by the caller |
| `cap` | capacity of buf in bytes; at most cap - 1 bytes are written |
| **returns** | a Writer appending to m |

### memory_growing

```mach
pub fun memory_growing(m: *Memory, alloc: *std.allocator.Allocator) Writer
```

wire a writer into storage it grows through alloc

| Parameter | |
| :--- | :--- |
| `m` | memory state, owned by the caller for the writer's whole life |
| `alloc` | grows the storage; released with memory_dnit |
| **returns** | a Writer appending to m |

### memory_dnit

```mach
pub fun memory_dnit(m: *Memory)
```

release the storage a growing memory holds; a fixed memory holds none

### memory_text

```mach
pub fun memory_text(m: *Memory) str
```

the written bytes as text, terminated in place; empty before any write

