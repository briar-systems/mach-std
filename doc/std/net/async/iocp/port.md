[std](../../../README.md) / [net](../../README.md) / [async](../README.md) / [iocp](README.md) / **port**

# std.net.async.iocp.port

the completion port layer shared by the windows net.async backends
backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface)

everything here makes a native call: posting, aborting, settling and
harvesting packets. std.net.async.iocp decides what is due, and this layer
acts on it. a backend's operation record starts with a Header, so one
address names both, and the backend hands in Hooks for what only it knows

Source: [`src/net/async/iocp/port.mach`](../../../../../src/net/async/iocp/port.mach)

Uses types from [`std.allocator`](../../../allocator.md), [`std.io.runtime`](../../../io/runtime.md), [`std.memory.table`](../../../memory/table.md), [`std.net.async.iocp`](../iocp.md), [`std.net.async.types`](../types.md), [`std.sync.mutex`](../../../sync/mutex.md), [`std.system.os.shared`](../../../system/os/shared.md), [`std.system.os.windows`](../../../system/os/windows.md).

| Type | | |
| :--- | :--- | :--- |
| [`NativeOverlapped`](#nativeoverlapped) | `rec` | the native OVERLAPPED a request posts with, laid out as the kernel reads it |
| [`NativeBuffer`](#nativebuffer) | `rec` | the native WSABUF a send or receive borrows |
| [`Header`](#header) | `rec` | the part of an operation this layer owns |
| [`Hooks`](#hooks) | `rec` | what differs between the backends |
| [`Backend`](#backend) | `rec` | a bounded completion port backend |

| On `NativeOverlapped` | |
| :--- | :--- |
| [`zero_overlapped`](#zero_overlapped) | clear a native request before it is posted |

| On `Header` | |
| :--- | :--- |
| [`cancelled`](#cancelled) | whether the driver cancelled the operation while its request was outstanding |

| On `Backend` | |
| :--- | :--- |
| [`header_at`](#header_at) | the operation record at a table index, which must be inside the table |
| [`socket_record`](#socket_record) | the core's socket record at an index |
| [`aliases`](#aliases) | whether a caller range overlaps memory the backend owns |
| [`operation_for`](#operation_for) | the operation a token names, in any state but free |
| [`trim_locked`](#trim_locked) | give back what a peak grew |
| [`unlock`](#unlock) | every hold of backend.lock that may have freed something ends here, so what a drained peak grew goes back as soon as the lock is let go |
| [`claim_locked`](#claim_locked) | a free operation joins the socket record sock in state |
| [`release_locked`](#release_locked) | the operation leaves its own socket record, never one found by socket value |
| [`push_completion_locked`](#push_completion_locked) | append a completion to those the current publish makes readable |
| [`init`](#init) | initial is the size the backend starts at: the operation, completion and socket tables grow on demand |
| [`acquire_locked`](#acquire_locked) | the socket record a submit joins, associated with the completion port once per opening when associate is set |
| [`controlled_locked`](#controlled_locked) | a socket with a shutdown or close submitted takes no further requests |
| [`admit`](#admit) | the socket record a request joins, or the refusal |
| [`submit_buffer`](#submit_buffer) | a read, readiness wait or write over one borrowed buffer |
| [`submit_shutdown_write`](#submit_shutdown_write) | a shutdown waits for the socket's writes, and runs once none is left |
| [`submit_close`](#submit_close) | a close aborts the socket's requests and completes once they have all left |
| [`close_socket`](#close_socket) | close a socket without a completion |
| [`detach`](#detach) | give up a socket with no operation on it, so another completion port can take it |
| [`adopt`](#adopt) | take a socket another backend detached, under the opening its handle now carries, so a handle with an older opening is refused as stale |
| [`cancel`](#cancel) | cancellation is asynchronous for a request the kernel holds |
| [`settle_locked`](#settle_locked) | publish the operation's result and release it |
| [`finish_locked`](#finish_locked) | a request settled with status: an accept's socket is finished or closed, a readiness wait reads the queued byte count, and the rest report their bytes |
| [`flush`](#flush) | publish the settled controls without waiting |
| [`dispatch`](#dispatch) | handle one packet the runtime's shared queue delivered |
| [`poll`](#poll) | one thread owns poll and completion storage |
| [`completion`](#completion) | copy out one completion the last publish made readable |
| [`dnit`](#dnit) | a cancelled operation keeps the backend busy until its packet is consumed |
| [`awaiting_cancellations`](#awaiting_cancellations) | cancelled operations whose packet has not arrived yet |

| Functions | |
| :--- | :--- |
| [`invalid`](#invalid) | the status for an invalid argument |

| Constants | |
| :--- | :--- |
| [`INVALID_SOCKET`](#constants) | |

---

## NativeOverlapped

```mach
pub rec NativeOverlapped {
    internal:      usize;
    internal_high: usize;
    offset:        u32;
    offset_high:   u32;
    event:         usize;
}
```

the native OVERLAPPED a request posts with, laid out as the kernel reads it

| Field | Type | |
| :--- | :--- | :--- |
| `internal` | `usize` | the request's status, written by the kernel |
| `internal_high` | `usize` | bytes transferred, written by the kernel |
| `offset` | `u32` | low half of a file offset, zero for sockets |
| `offset_high` | `u32` | high half of a file offset, zero for sockets |
| `event` | `usize` | an event handle to signal, zero here |

### zero_overlapped

```mach
pub fun zero_overlapped(overlapped: *NativeOverlapped)
```

clear a native request before it is posted

| Parameter | |
| :--- | :--- |
| `overlapped` | the request |

## NativeBuffer

```mach
pub rec NativeBuffer {
    length: u32;
    data:   *u8;
}
```

the native WSABUF a send or receive borrows

| Field | Type | |
| :--- | :--- | :--- |
| `length` | `u32` | bytes in data |
| `data` | `*u8` | the bytes |

## Header

```mach
pub rec Header {
    overlapped:   NativeOverlapped;
    link:         std.net.async.iocp.Link;
    generation:   u32;
    index:        u32;
    next_free:    usize;
    resource:     usize;
    auxiliary:    usize;
    context:      u64;
    buffer:       NativeBuffer;
    address:      [288]u8;
    transferred:  u32;
    native_flags: u32;
}
```

the part of an operation this layer owns. every field the kernel touches is
stable until the operation's packet is consumed

| Field | Type | |
| :--- | :--- | :--- |
| `overlapped` | `NativeOverlapped` | the native request, whose address is the packet's context |
| `link` | `std.net.async.iocp.Link` | state, kind and socket membership, owned by the iocp core |
| `auxiliary` | `usize` | the socket an accept fills, closed unless handed to the caller |
| `buffer` | `NativeBuffer` | the one buffer a read or write borrows |
| `address` | `[288]u8` | native address storage for accept and connect |

### cancelled

```mach
pub fun cancelled(operation: *Header) bool
```

whether the driver cancelled the operation while its request was outstanding

## Hooks

```mach
pub rec Hooks {
    clear:    fun(*Header);
    accepted: fun(*Header) i64;
    finish:   fun(ptr, *Header, i64, usize, u32);
    stale:    bool;
}
```

what differs between the backends

| Field | Type | |
| :--- | :--- | :--- |
| `clear` | `fun(*Header)` | resets the backend's own fields and drops what they borrow |
| `accepted` | `fun(*Header) i64` | finishes an accept once its context is set, 0 or a native code |
| `finish` | `fun(ptr, *Header, i64, usize, u32)` | settles an active packet of a kind this layer does not know, or nil |
| `stale` | `bool` | whether a request aborted outside the driver reports STATUS_STALE |

## Backend

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

| Field | Type | |
| :--- | :--- | :--- |
| `operations` | `std.memory.table.Table` | operation records, each starting with a Header |
| `core` | `std.net.async.iocp.Core` | the socket records, their map and the control lists |
| `operation_pool` | `std.memory.table.Pool` | free operations, lowest chunk first. its floor is the generation an operation of a regrown chunk starts from |
| `awaiting` | `usize` | cancelled operations whose packet has not arrived |

### header_at

```mach
pub fun header_at(backend: *Backend, index: usize) *Header
```

the operation record at a table index, which must be inside the table

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `index` | the operation index |
| **returns** | the record's Header |

### socket_record

```mach
pub fun socket_record(backend: *Backend, sock: u32) *std.net.async.iocp.Socket
```

the core's socket record at an index

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `sock` | the record index |
| **returns** | the record |

### aliases

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

whether a caller range overlaps memory the backend owns

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `data` | start of the range |
| `len` | bytes in the range |
| **returns** | true on overlap, and also when the range or the backend is not valid |

### operation_for

```mach
pub fun operation_for(backend: *Backend, token: std.net.async.types.Token) *Header
```

the operation a token names, in any state but free

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `token` | the operation token |
| **returns** | nil when the token is stale or the operation was released |

### trim_locked

```mach
pub fun trim_locked(backend: *Backend)
```

give back what a peak grew. operations release a chunk once it and the chunk
below it are free, the completion table follows them down but never below
what the last publish filled, and the socket records trim with their map.
only free operations are released, and a free operation owes no packet, so
no overlapped address the kernel still holds moves. runs where a lock hold
ends, never inside a publish, so the completions being filled stay put

### unlock

```mach
pub fun unlock(backend: *Backend)
```

every hold of backend.lock that may have freed something ends here, so what
a drained peak grew goes back as soon as the lock is let go

### claim_locked

```mach
pub fun claim_locked(backend: *Backend, sock: u32, kind: std.io.runtime.Kind, resource: usize, context: u64, state: u8, token: *std.net.async.types.Token) *Header
```

a free operation joins the socket record sock in state

### release_locked

```mach
pub fun release_locked(backend: *Backend, operation: *Header)
```

the operation leaves its own socket record, never one found by socket value

### push_completion_locked

```mach
pub fun push_completion_locked(
    backend: *Backend,
    context: u64,
    kind: std.io.runtime.Kind,
    bytes: usize,
    items: usize,
    resource: usize,
    status: i64,
    end_of_stream: bool,
) bool
```

append a completion to those the current publish makes readable

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `context` | the caller's context from the submission |
| `kind` | the operation kind |
| `bytes` | bytes moved |
| `items` | packets moved by a batch operation |
| `resource` | the native socket, or the accepted socket for an accept |
| `status` | 0, a negative native error or a STATUS_ value |
| `end_of_stream` | a read or readable wait saw the orderly end of the stream |
| **returns** | false when the completion table is full and nothing was added |

### init

```mach
pub fun init(backend: *Backend, queue: *std.system.os.shared.IoQueue, a: *std.allocator.Allocator, initial: usize, source_id: u16, operation_size: usize, hooks: Hooks) i64
```

initial is the size the backend starts at: the operation, completion and
socket tables grow on demand

| Parameter | |
| :--- | :--- |
| `a` | where the tables, the socket map and the completion batch come from; the backend keeps a copy, so a's context must outlive it |
| `operation_size` | bytes per operation record, which starts with a Header |

### acquire_locked

```mach
pub fun acquire_locked(backend: *Backend, resource: usize, opening: u64, associate: bool, sock: *u32) i64
```

the socket record a submit joins, associated with the completion port once
per opening when associate is set. a socket value mapped under a newer
opening makes this handle stale, and one mapped under an older opening
belongs to a socket closed outside the driver, whose record the core drops.
associating a socket that is still associated fails, so a handle wrapped
twice from one live socket is refused rather than taken over

### controlled_locked

```mach
pub fun controlled_locked(backend: *Backend, sock: u32) bool
```

a socket with a shutdown or close submitted takes no further requests

### admit

```mach
pub fun admit(backend: *Backend, resource: usize, opening: u64, sock: *u32) i64
```

the socket record a request joins, or the refusal. backend.lock stays held on success

### submit_buffer

```mach
pub fun submit_buffer(backend: *Backend, resource: usize, opening: u64, buffer: *u8, length: usize, context: u64, kind: std.io.runtime.Kind, token: *std.net.async.types.Token) i64
```

a read, readiness wait or write over one borrowed buffer

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *Backend, resource: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

a shutdown waits for the socket's writes, and runs once none is left

### submit_close

```mach
pub fun submit_close(backend: *Backend, resource: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

a close aborts the socket's requests and completes once they have all left.
the record is unmapped at once, so a reused socket value attaches fresh

### close_socket

```mach
pub fun close_socket(backend: *Backend, resource: usize, opening: u64) i64
```

close a socket without a completion. its outstanding requests settle on the
unmapped record, so a reused socket value attaches fresh

### detach

```mach
pub fun detach(backend: *Backend, resource: usize, opening: u64, retire: bool) i64
```

give up a socket with no operation on it, so another completion port can
take it. the socket leaves this port, and its record goes, or with retire
stays mapped under opening so a handle still carrying that opening is refused
as stale until a newer opening reuses the value. a socket this backend never
took under opening is not attached to its port

| Parameter | |
| :--- | :--- |
| **returns** | 0, EBUSY while an operation is on the socket, STATUS_STALE for a handle this backend already knows to be stale, ENOMEM when a retired record cannot be kept, or the native refusal to leave the port, which leaves the socket as it was |

### adopt

```mach
pub fun adopt(backend: *Backend, resource: usize, opening: u64) i64
```

take a socket another backend detached, under the opening its handle now
carries, so a handle with an older opening is refused as stale. the socket
attaches to the port with its first request

| Parameter | |
| :--- | :--- |
| **returns** | 0, STATUS_STALE when this backend knows the value under a newer opening, or ENOMEM |

### cancel

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

### settle_locked

```mach
pub fun settle_locked(backend: *Backend, operation: *Header, bytes: usize, items: usize, resource: usize, status: i64, end_of_stream: bool)
```

publish the operation's result and release it. a cancelled operation reports
STATUS_CANCELLED with the transfer that finished before the cancellation. the
only socket it hands over is one an accept had already taken (#927)

### finish_locked

```mach
pub fun finish_locked(backend: *Backend, operation: *Header, status: i64, bytes: usize)
```

a request settled with status: an accept's socket is finished or closed, a
readiness wait reads the queued byte count, and the rest report their bytes.
an accept whose abort landed after it took a connection still finishes it, and
its cancellation hands the socket over

### flush

```mach
pub fun flush(backend: *Backend) i64
```

publish the settled controls without waiting

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| **returns** | the number of completions now readable through completion, or EINVAL |

### dispatch

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

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `context` | the packet's context, an operation's overlapped address |
| `events` | the native event bits |
| `status` | the packet's status |
| `flags` | the packet's transferred byte count |
| `claimed` | set true when the packet belongs to a live operation of this backend |
| **returns** | the number of completions now readable through completion, or EINVAL |

### poll

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion storage

### completion

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

copy out one completion the last publish made readable

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `index` | below the count the last flush, dispatch or poll returned |
| `out` | receives the completion |
| **returns** | 0, or EINVAL for a bad argument or an index past the count |

### dnit

```mach
pub fun dnit(backend: *Backend) i64
```

a cancelled operation keeps the backend busy until its packet is consumed

### awaiting_cancellations

```mach
pub fun awaiting_cancellations(backend: *Backend) usize
```

cancelled operations whose packet has not arrived yet

## Functions

### invalid

```mach
pub fun invalid() i64
```

the status for an invalid argument

| Parameter | |
| :--- | :--- |
| **returns** | the native EINVAL |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `INVALID_SOCKET` | `usize` | `(-1)::usize` |  |

