[std](../../README.md) / [net](../README.md) / [async](README.md) / **windows**

# std.net.async.windows

bounded windows IOCP backend and overlapped socket operations
backend for std.net.async, signatures may change in a minor release (README, API surface)

Source: [`src/net/async/windows.mach`](../../../../src/net/async/windows.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.async.iocp.port`](iocp/port.md), [`std.net.async.types`](types.md), [`std.net.ip`](../ip.md), [`std.system.os.shared`](../../system/os/shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`Operation`](#operation) | `rec` | every field touched by the kernel is stable until its IOCP packet is consumed |

| Functions | |
| :--- | :--- |
| [`init`](#init) | initial is the size the backend starts at: every table grows on demand |
| [`detach`](#detach) | give up a socket with nothing on it, so another backend can take it: the socket leaves the completion port and stays open, and its record is retired under opening so a handle still carrying it is refused as stale |
| [`submit_read`](#submit_read) | post an overlapped read into a borrowed buffer |
| [`submit_readable`](#submit_readable) | wait for the stream to be readable without a buffer: an overlapped zero-byte receive, settled on completion by the queued byte count |
| [`submit_write`](#submit_write) | post an overlapped write from a borrowed buffer |
| [`submit_write_vector`](#submit_write_vector) | post an overlapped vectored write |
| [`submit_accept`](#submit_accept) | post an overlapped accept on a listening socket, into a socket made for it here |
| [`submit_connect`](#submit_connect) | post an overlapped connect, binding the socket first when it is unbound |
| [`submit_receive_batch`](#submit_receive_batch) | post a receive of up to count datagrams |
| [`submit_send_batch`](#submit_send_batch) | post a send of count datagrams, one after another, each to its own peer |

| Constants | |
| :--- | :--- |
| [`CANCEL_NEEDS_NATIVE_CONTROL`](#constants) | cancel only requests the abort and its packet settles it through dispatch, so it never needs the native wait to yield |

| Forwards | |
| :--- | :--- |
| [`Packet`](#packet), [`Token`](#token), [`NativeCompletion`](#nativecompletion), [`Backend`](#backend), [`aliases`](#aliases), [`submit_shutdown_write`](#submit_shutdown_write), [`submit_close`](#submit_close), [`cancel`](#cancel), [`flush`](#flush), [`dispatch`](#dispatch), [`poll`](#poll), [`completion`](#completion), [`dnit`](#dnit), [`awaiting_cancellations`](#awaiting_cancellations), [`adopt`](#adopt) | |

---

## Operation

```mach
pub rec Operation {
    header:         std.net.async.iocp.port.Header;
    vectors:        [16]std.net.async.iocp.port.NativeBuffer;
    vector_count:   usize;
    peer:           *std.net.ip.Endpoint;
    packets:        *std.net.async.types.Packet;
    packet_count:   usize;
    packet_index:   usize;
    batch_bytes:    usize;
    address_length: i32;
    control:        [128]u8;
    message:        NativeMessage;
}
```

every field touched by the kernel is stable until its IOCP packet is consumed

| Field | Type | |
| :--- | :--- | :--- |
| `header` | `std.net.async.iocp.port.Header` | the part the completion port layer owns, first so one address names both |

## Functions

### init

```mach
pub fun init(backend: *Backend, queue: *std.system.os.shared.IoQueue, a: *std.allocator.Allocator, initial: usize, source_id: u16) i64
```

initial is the size the backend starts at: every table grows on demand

### detach

```mach
pub fun detach(backend: *Backend, resource: usize, opening: u64) i64
```

give up a socket with nothing on it, so another backend can take it: the
socket leaves the completion port and stays open, and its record is retired
under opening so a handle still carrying it is refused as stale

### submit_read

```mach
pub fun submit_read(backend: *Backend, resource: usize, opening: u64, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

post an overlapped read into a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `opening` | the handle's opening |
| `buffer` | where the bytes go, borrowed until the operation completes |
| `length` | the buffer size in bytes, at most 0xffffffff |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted or held behind an earlier readiness wait, or a negative native error or STATUS_STALE |

### submit_readable

```mach
pub fun submit_readable(backend: *Backend, resource: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

wait for the stream to be readable without a buffer: an overlapped zero-byte
receive, settled on completion by the queued byte count

### submit_write

```mach
pub fun submit_write(backend: *Backend, resource: usize, opening: u64, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

post an overlapped write from a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `opening` | the handle's opening |
| `buffer` | the bytes to send, borrowed until the operation completes |
| `length` | bytes to send, at most 0xffffffff |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error or STATUS_STALE |

### submit_write_vector

```mach
pub fun submit_write_vector(backend: *Backend, resource: usize, opening: u64, vectors: *std.system.os.shared.IoVector, count: usize, context: u64, token: *std.net.async.types.Token) i64
```

post an overlapped vectored write

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `opening` | the handle's opening |
| `vectors` | the buffers, copied into the operation. their bytes are borrowed until it completes |
| `count` | buffers in vectors, 1 to 16, totalling at most 0xffffffff bytes |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error or STATUS_STALE |

### submit_accept

```mach
pub fun submit_accept(backend: *Backend, listener: usize, opening: u64, peer: *std.net.ip.Endpoint, context: u64, token: *std.net.async.types.Token) i64
```

post an overlapped accept on a listening socket, into a socket made for it here

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `listener` | the native listening socket |
| `opening` | the handle's opening |
| `peer` | receives the peer's endpoint, nil to skip it. borrowed until the operation completes |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error or STATUS_STALE. the completion's resource is the accepted socket, owned by the caller |

### submit_connect

```mach
pub fun submit_connect(backend: *Backend, resource: usize, opening: u64, peer: std.net.ip.Endpoint, context: u64, token: *std.net.async.types.Token) i64
```

post an overlapped connect, binding the socket first when it is unbound

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `opening` | the handle's opening |
| `peer` | the endpoint to connect to, copied |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error or STATUS_STALE |

### submit_receive_batch

```mach
pub fun submit_receive_batch(backend: *Backend, resource: usize, opening: u64, packets: *std.net.async.types.Packet, count: usize, context: u64, token: *std.net.async.types.Token) i64
```

post a receive of up to count datagrams. after the first it takes only those already queued

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native datagram socket |
| `opening` | the handle's opening |
| `packets` | the packets to fill, borrowed until the operation completes |
| `count` | packets in the batch, at least 1 |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error or STATUS_STALE. the completion's items is the packets filled |

### submit_send_batch

```mach
pub fun submit_send_batch(backend: *Backend, resource: usize, opening: u64, packets: *std.net.async.types.Packet, count: usize, context: u64, token: *std.net.async.types.Token) i64
```

post a send of count datagrams, one after another, each to its own peer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native datagram socket |
| `opening` | the handle's opening |
| `packets` | the packets to send, borrowed until the operation completes |
| `count` | packets in the batch, at least 1 |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, a negative native error or STATUS_STALE, or the refusal of an invalid packet. the completion's items is the packets sent |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANCEL_NEEDS_NATIVE_CONTROL` | `bool` | `false` | cancel only requests the abort and its packet settles it through dispatch, so it never needs the native wait to yield |

## Forwards

### Packet

Forwards [`std.net.async.types.Packet`](types.md#packet).

```mach
pub rec Packet {
    buffer:                *u8;
    capacity:              usize;
    length:                usize;
    peer:                  std.net.ip.Endpoint;
    local_destination:     std.net.ip.Addr;
    interface_index:       u32;
    has_local_destination: bool;
    truncated:             bool;
    zero_length:           bool;
}
```

packet storage is borrowed until its operation completes

### Token

Forwards [`std.net.async.types.Token`](types.md#token).

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

names one operation a backend holds, refused once the slot is reused

### NativeCompletion

Forwards [`std.net.async.types.NativeCompletion`](types.md#nativecompletion).

```mach
pub rec NativeCompletion {
    context:       u64;
    kind:          std.io.runtime.Kind;
    bytes:         usize;
    items:         usize;
    resource:      usize;
    status:        i64;
    end_of_stream: bool;
}
```

what a backend reports for one finished operation

### Backend

Forwards [`std.net.async.iocp.port.Backend`](iocp/port.md#backend).

```mach
pub rec Backend {
    queue:     *std.system.os.shared.IoQueue;
    source_id: u16;
    # where every table's chunks come from
    allocator:      std.allocator.Allocator;
    operations:     std.memory.table.Table;
    completions:    std.memory.table.Table;
    core:           std.net.async.iocp.Core;
    native:         *std.system.os.windows.IoCompletion;
    hooks:          Hooks;
    operation_pool: std.memory.table.Pool;
    active:         usize;
    ready:          usize;
    awaiting:       usize;
    lock:           std.sync.mutex.Mutex;
}
```

a bounded completion port backend

### aliases

Forwards [`std.net.async.iocp.port.aliases`](iocp/port.md#aliases).

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

whether a caller range overlaps memory the backend owns

### submit_shutdown_write

Forwards [`std.net.async.iocp.port.submit_shutdown_write`](iocp/port.md#submit_shutdown_write).

```mach
pub fun submit_shutdown_write(backend: *Backend, resource: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

a shutdown waits for the socket's writes, and runs once none is left

### submit_close

Forwards [`std.net.async.iocp.port.submit_close`](iocp/port.md#submit_close).

```mach
pub fun submit_close(backend: *Backend, resource: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

a close aborts the socket's requests and completes once they have all left.
the record is unmapped at once, so a reused socket value attaches fresh

### cancel

Forwards [`std.net.async.iocp.port.cancel`](iocp/port.md#cancel).

```mach
pub fun cancel(backend: *Backend, token: std.net.async.types.Token, finished: *opt[std.net.async.types.NativeCompletion]) i64
```

cancellation is asynchronous for a request the kernel holds. the request is
aborted and cancel returns io.runtime.CANCELLATION_PENDING. its packet still
arrives, and dispatch then reports it with types.STATUS_CANCELLED, so its
borrowed storage stays with the kernel until that completion is published.
that completion carries whatever the request finished before the abort
landed: a read's bytes, a write's sent bytes, a batch's datagrams. a request
the kernel never held is released at once and cancel returns 0. no finished
completion is ever held back here, so finished is always none

### flush

Forwards [`std.net.async.iocp.port.flush`](iocp/port.md#flush).

```mach
pub fun flush(backend: *Backend) i64
```

publish the settled controls without waiting

### dispatch

Forwards [`std.net.async.iocp.port.dispatch`](iocp/port.md#dispatch).

```mach
pub fun dispatch(
    backend: *Backend,
    context: u64,
    events: u32,
    status: i64,
    flags: u64,
    claimed: *bool,
) i64
```

handle one packet the runtime's shared queue delivered

### poll

Forwards [`std.net.async.iocp.port.poll`](iocp/port.md#poll).

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion storage

### completion

Forwards [`std.net.async.iocp.port.completion`](iocp/port.md#completion).

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

copy out one completion the last publish made readable

### dnit

Forwards [`std.net.async.iocp.port.dnit`](iocp/port.md#dnit).

```mach
pub fun dnit(backend: *Backend) i64
```

a cancelled operation keeps the backend busy until its packet is consumed

### awaiting_cancellations

Forwards [`std.net.async.iocp.port.awaiting_cancellations`](iocp/port.md#awaiting_cancellations).

```mach
pub fun awaiting_cancellations(backend: *Backend) usize
```

cancelled operations whose packet has not arrived yet

### adopt

Forwards [`std.net.async.iocp.port.adopt`](iocp/port.md#adopt).

```mach
pub fun adopt(backend: *Backend, resource: usize, opening: u64) i64
```

take a socket another backend detached, under the opening its handle now
carries, so a handle with an older opening is refused as stale. the socket
attaches to the port with its first request

