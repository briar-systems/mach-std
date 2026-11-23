[std](../../README.md) / [net](../README.md) / [async](README.md) / **readiness**

# std.net.async.readiness

bounded readiness engine shared by the linux and darwin socket backends
engine for std.net.async.unix and std.net.async.local.unix, signatures may change in a minor release (README, API surface)
a backend brings a Protocol: its operation record, the one nonblocking try at
an operation, and how it admits a socket. everything else lives here once.
attached handles remain exclusively owned by the backend through completion and close.

Source: [`src/net/async/readiness.mach`](../../../../src/net/async/readiness.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.io.runtime`](../../io/runtime.md), [`std.memory.table`](../../memory/table.md), [`std.net.async.types`](types.md), [`std.sync.mutex`](../../sync/mutex.md), [`std.system.os.shared`](../../system/os/shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`Operation`](#operation) | `rec` | the part of an operation the engine owns |
| [`Resource`](#resource) | `rec` | one native socket the engine tracks: its queued operations and its registration |
| [`Protocol`](#protocol) | `rec` | what a backend brings to the engine |
| [`Backend`](#backend) | `rec` | a readiness backend: the native queue, the tables and the finished queue |

| On `Backend` | |
| :--- | :--- |
| [`operation_at`](#operation_at) | the operation record at a table index, which must be inside the table |
| [`resource_at`](#resource_at) | the resource record at a table index, which must be inside the table |
| [`aliases`](#aliases) | whether a caller range overlaps memory the backend owns |
| [`token_context`](#token_context) | the wire context is a 16-bit source id, a 32-bit resource index and a 16-bit generation |
| [`context_token`](#context_token) | decode a wire context back into the resource token it carries |
| [`operation_any`](#operation_any) | the operation a token names, active or finished and waiting to be published |
| [`resource_for`](#resource_for) | the active resource a token names |
| [`resource_lookup`](#resource_lookup) | the resource tracking a native socket |
| [`resource_acquire`](#resource_acquire) | the resource for a native socket, created when there is none |
| [`resource_release_unwatched`](#resource_release_unwatched) | free a resource whose native registration is already gone, removing it from the map |
| [`set_watched`](#set_watched) | every registration change goes through here, so destroy can prove it gave up each one before the runtime recycles the source id they carry |
| [`operation_claim`](#operation_claim) | claim a free operation, growing the table when none is free |
| [`operation_release`](#operation_release) | return an operation to the free pool |
| [`trim_locked`](#trim_locked) | give back what a peak grew |
| [`finish`](#finish) | a finished operation carries its own completion and the queue links them, so the finished queue is never a table that has to be sized |
| [`stale`](#stale) | whether a handle under opening names a socket this backend knows was closed and reused, or detached |
| [`begin`](#begin) | a refused submission may have dropped a stale resource, so it trims too |
| [`submission_done`](#submission_done) | end a submission: drive the resource once, trim, unlock and wake the waiter |
| [`init`](#init) | initial is the size the backend starts at: the operation, resource and ready tables grow on demand and the resource map rehashes with them |
| [`submit_read`](#submit_read) | queue a read into a borrowed buffer |
| [`submit_readable`](#submit_readable) | wait for the stream to be readable without a buffer: the completion reports end_of_stream at orderly EOF, and nothing is read |
| [`submit_write`](#submit_write) | queue a write from a borrowed buffer |
| [`submit_shutdown_write`](#submit_shutdown_write) | queue a shutdown of the write side, behind the writes already queued |
| [`begin_close_locked`](#begin_close_locked) | start a close: queued reads finish cancelled and the close waits for the writes to drain |
| [`submit_close`](#submit_close) | queue a close, which closes the native socket once its queued writes finish |
| [`cancel`](#cancel) | cancel an operation |
| [`flush`](#flush) | publish the finished operations without waiting |
| [`dispatch`](#dispatch) | handle one event the runtime's shared queue delivered |
| [`poll`](#poll) | one thread owns poll and completion retrieval |
| [`completion`](#completion) | copy out one completion the last publish made readable |
| [`dnit`](#dnit) | release the backend, its idle resources and their registrations |

| Functions | |
| :--- | :--- |
| [`invalid`](#invalid) | the status for an invalid argument |
| [`would_block`](#would_block) | a connect in flight is the contract's CONNECT_PENDING, never this |
| [`socket_close`](#socket_close) | close a native socket |

| Constants | |
| :--- | :--- |
| [`CANCEL_NEEDS_NATIVE_CONTROL`](#constants) | cancel ends native access synchronously, so it runs while no thread is inside the native wait |
| [`LANE_NONE`](#constants), [`LANE_READ`](#constants), [`LANE_WRITE`](#constants), [`NONE`](#constants) | |

---

## Operation

```mach
pub rec Operation {
    state:          u8;
    generation:     u32;
    index:          u32;
    completion:     std.net.async.types.NativeCompletion;
    kind:           std.io.runtime.Kind;
    resource:       usize;
    context:        u64;
    buffer:         *u8;
    length:         usize;
    sequence:       u64;
    previous:       u32;
    next:           u32;
    resource_index: u32;
    lane:           u8;
    stage:          u8;
    # the pool's free-list link while the operation is free
    pool_next: usize;
}
```

the part of an operation the engine owns. a backend's operation record starts
with one, and the rest of the record is the backend's, zeroed on every claim

## Resource

```mach
pub rec Resource {
    state:        u8;
    generation:   u32;
    index:        u32;
    resource:     usize;
    read_head:    u32;
    read_tail:    u32;
    write_head:   u32;
    write_tail:   u32;
    close_index:  u32;
    armed:        bool;
    watched:      bool;
    closing:      bool;
    write_closed: bool;
    # the handle's opening, 0 for a backend whose handles carry none
    opening:    u64;
    configured: bool;
    # detached under opening: the socket belongs to another driver, so a
    # handle still carrying opening is stale
    retired:   bool;
    next_free: usize;
}
```

one native socket the engine tracks: its queued operations and its registration

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `u8` | free or active |
| `generation` | `u32` | bumped on every acquire, the generation of its wire context |
| `index` | `u32` | its slot in the resource table |
| `resource` | `usize` | the native socket |
| `read_head` | `u32` | first queued read lane operation, NONE when empty |
| `read_tail` | `u32` | last queued read lane operation, NONE when empty |
| `write_head` | `u32` | first queued write lane operation, NONE when empty |
| `write_tail` | `u32` | last queued write lane operation, NONE when empty |
| `close_index` | `u32` | the close waiting for both lanes to drain, NONE when none |
| `armed` | `bool` | a native registration is armed for it |
| `watched` | `bool` | it holds a native registration |
| `closing` | `bool` | a close was submitted, so new operations are refused |
| `write_closed` | `bool` | the write side was shut down |
| `configured` | `bool` | the backend set its datagram packet options on the socket |
| `next_free` | `usize` | the pool's free-list link while the resource is free |

## Protocol

```mach
pub rec Protocol {
    # the size of the backend's operation record, whose first field is an Operation
    operation_size: usize;
    # one nonblocking try at a queued operation: true once it finished, false
    # while it would block
    attempt: fun(*Backend, *Resource, *Operation) bool;
    # the first sight of a native handle: 0 when the backend drives it
    admit: fun(*Backend, usize) i64;
    # handles carry openings, so a registration that vanished means the socket
    # was closed outside the driver and its operations complete stale
    openings: bool;
}
```

what a backend brings to the engine

## Backend

```mach
pub rec Backend {
    queue:     *std.system.os.shared.IoQueue;
    source_id: u16;
    protocol:  Protocol;
    # where every table's chunks come from
    allocator:      std.allocator.Allocator;
    operations:     std.memory.table.Table;
    resources:      std.memory.table.Table;
    ready:          std.memory.table.Table;
    resource_map:   *u32;
    native:         *sys.IoCompletion;
    map_capacity:   usize;
    live:           usize;
    resource_count: usize;
    # free operations and resources, lowest chunk first. each pool's floor is
    # the generation an entry of a regrown chunk starts from
    operation_pool: std.memory.table.Pool;
    resource_pool:  std.memory.table.Pool;
    queued_head:    u32;
    queued_tail:    u32;
    queued_count:   usize;
    ready_count:    usize;
    sequence:       u64;
    # registrations held, zero once destroy returns
    registered: usize;
    lock:       std.sync.mutex.Mutex;
}
```

a readiness backend: the native queue, the tables and the finished queue

| Field | Type | |
| :--- | :--- | :--- |
| `queue` | `*std.system.os.shared.IoQueue` | the native readiness queue, borrowed from the caller |
| `source_id` | `u16` | the runtime source id carried in every wire context |
| `protocol` | `Protocol` | what the backend brings |
| `operations` | `std.memory.table.Table` | the operation table, of protocol.operation_size records |
| `resources` | `std.memory.table.Table` | the resource table |
| `ready` | `std.memory.table.Table` | completions published by the last flush, dispatch or poll |
| `resource_map` | `*u32` | open addressed map from native socket to resource index plus one |
| `native` | `*sys.IoCompletion` | the batch the native wait fills |
| `map_capacity` | `usize` | slots in resource_map, a power of two |
| `live` | `usize` | operations claimed and not yet released |
| `resource_count` | `usize` | active resources |
| `queued_head` | `u32` | first finished operation waiting to be published |
| `queued_tail` | `u32` | last finished operation waiting to be published |
| `queued_count` | `usize` | finished operations waiting to be published |
| `ready_count` | `usize` | completions in ready |
| `sequence` | `u64` | the next submission order number |
| `lock` | `std.sync.mutex.Mutex` | guards every field |

### operation_at

```mach
pub fun operation_at(backend: *Backend, index: usize) *Operation
```

the operation record at a table index, which must be inside the table

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `index` | the operation index |
| **returns** | the record, valid until the table shrinks past it |

### resource_at

```mach
pub fun resource_at(backend: *Backend, index: usize) *Resource
```

the resource record at a table index, which must be inside the table

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `index` | the resource index |
| **returns** | the record, valid until the table shrinks past it |

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

### token_context

```mach
pub fun token_context(backend: *Backend, token: std.net.async.types.Token) u64
```

the wire context is a 16-bit source id, a 32-bit resource index and a 16-bit
generation. the index is wide enough that memory bounds the table before it
does; the generation is what makes a stale completion detectable, and 16 bits
means an index must be recycled a multiple of 65535 times between a context
being orphaned and arriving for a stale one to pass as live

### context_token

```mach
pub fun context_token(backend: *Backend, context: u64, token: *std.net.async.types.Token) bool
```

decode a wire context back into the resource token it carries

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `context` | the wire context from a native event |
| `token` | receives the index and generation |
| **returns** | false when the context belongs to another source, token is nil or the generation is 0 |

### operation_any

```mach
pub fun operation_any(backend: *Backend, token: std.net.async.types.Token) *Operation
```

the operation a token names, active or finished and waiting to be published

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `token` | the operation token |
| **returns** | nil when the token is stale or the operation was released |

### resource_for

```mach
pub fun resource_for(backend: *Backend, token: std.net.async.types.Token) *Resource
```

the active resource a token names

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `token` | the resource token, as decoded from a wire context |
| **returns** | nil when the token is stale or the resource was released |

### resource_lookup

```mach
pub fun resource_lookup(backend: *Backend, resource: usize) *Resource
```

the resource tracking a native socket

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| **returns** | nil when the backend tracks no resource for it |

### resource_acquire

```mach
pub fun resource_acquire(backend: *Backend, native: usize, opening: u64, created: *bool) *Resource
```

the resource for a native socket, created when there is none. a resource
under an older opening is dropped as stale first

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `native` | the native socket |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `created` | set true when a new resource was made, false when an existing one is returned or the handle is refused |
| **returns** | nil when the handle is older than the tracked socket or was retired, or the tables cannot grow |

### resource_release_unwatched

```mach
pub fun resource_release_unwatched(backend: *Backend, resource: *Resource)
```

free a resource whose native registration is already gone, removing it from the map

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `resource` | the active resource |

### set_watched

```mach
pub fun set_watched(backend: *Backend, resource: *Resource, watched: bool)
```

every registration change goes through here, so destroy can prove it gave up
each one before the runtime recycles the source id they carry

### operation_claim

```mach
pub fun operation_claim(backend: *Backend, kind: std.io.runtime.Kind, native: usize, context: u64, token: *std.net.async.types.Token) *Operation
```

claim a free operation, growing the table when none is free

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `kind` | the operation kind |
| `native` | the native socket it acts on |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | the claimed operation, nil when the table cannot grow |

### operation_release

```mach
pub fun operation_release(backend: *Backend, index: u32)
```

return an operation to the free pool

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `index` | the operation index |

### trim_locked

```mach
pub fun trim_locked(backend: *Backend)
```

give back what a peak grew. operations and resources release a chunk once it
and the chunk below it are free, the ready table follows the operations down
but never below what the last publish filled, and the resource map is
rehashed to the smaller table. only free entries are released, so no live
token, queued completion or registration context moves or goes stale

### finish

```mach
pub fun finish(backend: *Backend, resource: *Resource, operation: *Operation, status: i64, bytes: usize, items: usize, native_resource: usize, end_of_stream: bool)
```

a finished operation carries its own completion and the queue links them, so
the finished queue is never a table that has to be sized

### stale

```mach
pub fun stale(backend: *Backend, native: usize, opening: u64) bool
```

whether a handle under opening names a socket this backend knows was closed
and reused, or detached

### begin

```mach
pub fun begin(backend: *Backend, native: usize, opening: u64, kind: std.io.runtime.Kind, context: u64, lane: u8, token: *std.net.async.types.Token, resource_out: **Resource, operation_out: **Operation) i64
```

a refused submission may have dropped a stale resource, so it trims too

### submission_done

```mach
pub fun submission_done(backend: *Backend, resource: *Resource)
```

end a submission: drive the resource once, trim, unlock and wake the waiter

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked on entry and unlocked on return |
| `resource` | the resource the submission queued on |

### init

```mach
pub fun init(backend: *Backend, queue: *std.system.os.shared.IoQueue, a: *std.allocator.Allocator, initial: usize, source_id: u16, protocol: Protocol) i64
```

initial is the size the backend starts at: the operation, resource and ready
tables grow on demand and the resource map rehashes with them

| Parameter | |
| :--- | :--- |
| `a` | where the tables, the resource map and the completion batch come from; the backend keeps a copy, so a's context must outlive it |
| `protocol` | what the backend brings, kept by the engine |

### submit_read

```mach
pub fun submit_read(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a read into a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `native` | the native socket |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `buffer` | where the bytes go, borrowed until the operation completes |
| `length` | the buffer size in bytes |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error or STATUS_STALE |

### submit_readable

```mach
pub fun submit_readable(backend: *Backend, native: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

wait for the stream to be readable without a buffer: the completion reports
end_of_stream at orderly EOF, and nothing is read

### submit_write

```mach
pub fun submit_write(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a write from a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `native` | the native socket |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `buffer` | the bytes to send, borrowed until the operation completes |
| `length` | bytes to send |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error or STATUS_STALE. EPIPE after a write shutdown |

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *Backend, native: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

queue a shutdown of the write side, behind the writes already queued

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `native` | the native socket |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error or STATUS_STALE |

### begin_close_locked

```mach
pub fun begin_close_locked(backend: *Backend, native: usize, opening: u64, context: u64, token: *std.net.async.types.Token, resource_out: **Resource) i64
```

start a close: queued reads finish cancelled and the close waits for the writes to drain

| Parameter | |
| :--- | :--- |
| `backend` | the backend, locked |
| `native` | the native socket |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `context` | the caller's context, carried to the completion |
| `token` | receives the close operation's token |
| `resource_out` | receives the resource being closed |
| **returns** | 0 once started, or a negative native error or STATUS_STALE |

### submit_close

```mach
pub fun submit_close(backend: *Backend, native: usize, opening: u64, context: u64, token: *std.net.async.types.Token) i64
```

queue a close, which closes the native socket once its queued writes finish

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `native` | the native socket, owned by the backend from here |
| `opening` | the handle's opening, 0 for a backend whose handles carry none |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error or STATUS_STALE |

### cancel

```mach
pub fun cancel(backend: *Backend, token: std.net.async.types.Token, finished: *opt[std.net.async.types.NativeCompletion]) i64
```

cancel an operation. one that already finished and waits to be published is
withdrawn and handed back through finished, whatever it moved included, so the
caller reports it with the cancellation: an accepted socket in it is the
caller's to hand over or close

### flush

```mach
pub fun flush(backend: *Backend) i64
```

publish the finished operations without waiting

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

handle one event the runtime's shared queue delivered

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `context` | the event's wire context |
| `events` | the native readiness events |
| `status` | unused by this engine |
| `flags` | unused by this engine |
| `claimed` | set true when the context belongs to this backend |
| **returns** | the number of completions now readable through completion, or EINVAL |

### poll

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion retrieval

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

release the backend, its idle resources and their registrations

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| **returns** | 0, EBUSY while an operation is live or unpublished, EINVAL for nil |

## Functions

### invalid

```mach
pub fun invalid() i64
```

the status for an invalid argument

| Parameter | |
| :--- | :--- |
| **returns** | the native EINVAL |

### would_block

```mach
pub fun would_block(status: i64) bool
```

a connect in flight is the contract's CONNECT_PENDING, never this

### socket_close

```mach
pub fun socket_close(resource: usize) i64
```

close a native socket

| Parameter | |
| :--- | :--- |
| `resource` | the native socket |
| **returns** | 0, or a negative native error |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANCEL_NEEDS_NATIVE_CONTROL` | `bool` | `true` | cancel ends native access synchronously, so it runs while no thread is inside the native wait |
| `LANE_NONE` | `u8` | `0` |  |
| `LANE_READ` | `u8` | `1` |  |
| `LANE_WRITE` | `u8` | `2` |  |
| `NONE` | `u32` | `0xffffffff` |  |

