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
| [`Resource`](#resource) | `rec` |  |
| [`Protocol`](#protocol) | `rec` | what a backend brings to the engine |
| [`Backend`](#backend) | `rec` |  |

| On `Backend` | |
| :--- | :--- |
| [`operation_at`](#operation_at), [`resource_at`](#resource_at), [`aliases`](#aliases) | |
| [`token_context`](#token_context) | the wire context is a 16-bit source id, a 32-bit resource index and a 16-bit generation |
| [`context_token`](#context_token), [`operation_any`](#operation_any), [`resource_for`](#resource_for), [`resource_lookup`](#resource_lookup), [`resource_acquire`](#resource_acquire), [`resource_release_unwatched`](#resource_release_unwatched) | |
| [`set_watched`](#set_watched) | every registration change goes through here, so destroy can prove it gave up each one before the runtime recycles the source id they carry |
| [`operation_claim`](#operation_claim), [`operation_release`](#operation_release) | |
| [`trim_locked`](#trim_locked) | give back what a peak grew |
| [`finish`](#finish) | a finished operation carries its own completion and the queue links them, so the finished queue is never a table that has to be sized |
| [`stale`](#stale) | whether a handle under opening names a socket this backend knows was closed and reused, or detached |
| [`begin`](#begin) | a refused submission may have dropped a stale resource, so it trims too |
| [`submission_done`](#submission_done) | |
| [`init`](#init) | initial is the size the backend starts at: the operation, resource and ready tables grow on demand and the resource map rehashes with them |
| [`submit_read`](#submit_read) | |
| [`submit_readable`](#submit_readable) | wait for the stream to be readable without a buffer: the completion reports end_of_stream at orderly EOF, and nothing is read |
| [`submit_write`](#submit_write), [`submit_shutdown_write`](#submit_shutdown_write), [`begin_close_locked`](#begin_close_locked), [`submit_close`](#submit_close) | |
| [`cancel`](#cancel) | cancel an operation |
| [`flush`](#flush), [`dispatch`](#dispatch) | |
| [`poll`](#poll) | one thread owns poll and completion retrieval |
| [`completion`](#completion), [`dnit`](#dnit) | |

| Functions | |
| :--- | :--- |
| [`invalid`](#invalid) | |
| [`would_block`](#would_block) | a connect in flight is the contract's CONNECT_PENDING, never this |
| [`socket_close`](#socket_close) | |

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
    context:        usize;
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

### operation_at

```mach
pub fun operation_at(backend: *Backend, index: usize) *Operation
```

### resource_at

```mach
pub fun resource_at(backend: *Backend, index: usize) *Resource
```

### aliases

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

### token_context

```mach
pub fun token_context(backend: *Backend, token: std.net.async.types.Token) usize
```

the wire context is a 16-bit source id, a 32-bit resource index and a 16-bit
generation. the index is wide enough that memory bounds the table before it
does; the generation is what makes a stale completion detectable, and 16 bits
means an index must be recycled a multiple of 65535 times between a context
being orphaned and arriving for a stale one to pass as live

### context_token

```mach
pub fun context_token(backend: *Backend, context: usize, token: *std.net.async.types.Token) bool
```

### operation_any

```mach
pub fun operation_any(backend: *Backend, token: std.net.async.types.Token) *Operation
```

### resource_for

```mach
pub fun resource_for(backend: *Backend, token: std.net.async.types.Token) *Resource
```

### resource_lookup

```mach
pub fun resource_lookup(backend: *Backend, resource: usize) *Resource
```

### resource_acquire

```mach
pub fun resource_acquire(backend: *Backend, native: usize, opening: u64, created: *bool) *Resource
```

### resource_release_unwatched

```mach
pub fun resource_release_unwatched(backend: *Backend, resource: *Resource)
```

### set_watched

```mach
pub fun set_watched(backend: *Backend, resource: *Resource, watched: bool)
```

every registration change goes through here, so destroy can prove it gave up
each one before the runtime recycles the source id they carry

### operation_claim

```mach
pub fun operation_claim(backend: *Backend, kind: std.io.runtime.Kind, native: usize, context: usize, token: *std.net.async.types.Token) *Operation
```

### operation_release

```mach
pub fun operation_release(backend: *Backend, index: u32)
```

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
pub fun begin(backend: *Backend, native: usize, opening: u64, kind: std.io.runtime.Kind, context: usize, lane: u8, token: *std.net.async.types.Token, resource_out: **Resource, operation_out: **Operation) i64
```

a refused submission may have dropped a stale resource, so it trims too

### submission_done

```mach
pub fun submission_done(backend: *Backend, resource: *Resource)
```

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
pub fun submit_read(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_readable

```mach
pub fun submit_readable(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

wait for the stream to be readable without a buffer: the completion reports
end_of_stream at orderly EOF, and nothing is read

### submit_write

```mach
pub fun submit_write(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

### begin_close_locked

```mach
pub fun begin_close_locked(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token, resource_out: **Resource) i64
```

### submit_close

```mach
pub fun submit_close(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

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

### dispatch

```mach
pub fun dispatch(
    backend: *Backend,
    context: usize,
    events: u32,
    status: i64,
    flags: u64,
    claimed: *bool,
) i64
```

### poll

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion retrieval

### completion

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

### dnit

```mach
pub fun dnit(backend: *Backend) i64
```

## Functions

### invalid

```mach
pub fun invalid() i64
```

### would_block

```mach
pub fun would_block(status: i64) bool
```

a connect in flight is the contract's CONNECT_PENDING, never this

### socket_close

```mach
pub fun socket_close(resource: usize) i64
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANCEL_NEEDS_NATIVE_CONTROL` | `bool` | `true` | cancel ends native access synchronously, so it runs while no thread is inside the native wait |
| `LANE_NONE` | `u8` | `0` |  |
| `LANE_READ` | `u8` | `1` |  |
| `LANE_WRITE` | `u8` | `2` |  |
| `NONE` | `u32` | `0xffffffff` |  |

