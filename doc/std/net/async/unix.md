[std](../../README.md) / [net](../README.md) / [async](README.md) / **unix**

# std.net.async.unix

bounded linux and darwin readiness backend for internet sockets
backend for std.net.async, signatures may change in a minor release (README, API surface)
the engine is std.net.async.readiness, and std.net.async.linux and .darwin hold
the control-message layout that differs between the two.
a local socket carries descriptor rights this byte backend cannot observe; std.net.async.local owns those.
attached handles remain exclusively owned by this backend through completion and close.

Source: [`src/net/async/unix.mach`](../../../../src/net/async/unix.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.async.readiness`](readiness.md), [`std.net.async.types`](types.md), [`std.net.ip`](../ip.md), [`std.system.os.shared`](../../system/os/shared.md).

| Functions | |
| :--- | :--- |
| [`init`](#init) | initial is the size the backend starts at: the operation, resource and ready tables grow on demand and the resource map rehashes with them |
| [`submit_accept`](#submit_accept), [`submit_connect`](#submit_connect), [`submit_write_vector`](#submit_write_vector), [`submit_receive_batch`](#submit_receive_batch), [`submit_send_batch`](#submit_send_batch) | |
| [`detach`](#detach) | give up a socket with nothing queued on it, so another backend can take it |
| [`adopt`](#adopt) | take a socket another backend detached, under the opening its handle now carries, so a handle with an older opening is refused as stale |

| Forwards | |
| :--- | :--- |
| [`Vector`](#vector), [`Packet`](#packet), [`Token`](#token), [`NativeCompletion`](#nativecompletion), [`CANCEL_NEEDS_NATIVE_CONTROL`](#cancel_needs_native_control), [`Backend`](#backend), [`aliases`](#aliases), [`submit_read`](#submit_read), [`submit_readable`](#submit_readable), [`submit_write`](#submit_write), [`submit_shutdown_write`](#submit_shutdown_write), [`submit_close`](#submit_close), [`cancel`](#cancel), [`flush`](#flush), [`dispatch`](#dispatch), [`poll`](#poll), [`completion`](#completion), [`dnit`](#dnit) | |

---

## Functions

### init

```mach
pub fun init(backend: *std.net.async.readiness.Backend, queue: *std.system.os.shared.IoQueue, a: *std.allocator.Allocator, initial: usize, source_id: u16) i64
```

initial is the size the backend starts at: the operation, resource and ready
tables grow on demand and the resource map rehashes with them

| Parameter | |
| :--- | :--- |
| `a` | where the tables, the resource map and the completion batch come from; the backend keeps a copy, so a's context must outlive it |

### submit_accept

```mach
pub fun submit_accept(backend: *std.net.async.readiness.Backend, listener: usize, opening: u64, peer: *std.net.ip.Endpoint, context: usize, token: *std.net.async.types.Token) i64
```

### submit_connect

```mach
pub fun submit_connect(backend: *std.net.async.readiness.Backend, native: usize, opening: u64, peer: std.net.ip.Endpoint, context: usize, token: *std.net.async.types.Token) i64
```

### submit_write_vector

```mach
pub fun submit_write_vector(backend: *std.net.async.readiness.Backend, native: usize, opening: u64, vectors: *std.net.async.types.Vector, count: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_receive_batch

```mach
pub fun submit_receive_batch(backend: *std.net.async.readiness.Backend, native: usize, opening: u64, packets: *std.net.async.types.Packet, count: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_send_batch

```mach
pub fun submit_send_batch(backend: *std.net.async.readiness.Backend, native: usize, opening: u64, packets: *std.net.async.types.Packet, count: usize, context: usize, token: *std.net.async.types.Token) i64
```

### detach

```mach
pub fun detach(backend: *std.net.async.readiness.Backend, native: usize, opening: u64) i64
```

give up a socket with nothing queued on it, so another backend can take it.
its registration goes and the socket stays open. its resource is kept, retired
under opening, so a handle still carrying opening is refused as stale until a
newer opening reuses the value

| Parameter | |
| :--- | :--- |
| **returns** | 0, EBUSY while an operation or a close is queued on it, STATUS_STALE for a handle this backend already knows to be stale, ENOMEM when no resource can be kept, or the native refusal to deregister, which leaves the resource as it was |

### adopt

```mach
pub fun adopt(backend: *std.net.async.readiness.Backend, native: usize, opening: u64) i64
```

take a socket another backend detached, under the opening its handle now
carries, so a handle with an older opening is refused as stale. the socket is
registered with its first operation

| Parameter | |
| :--- | :--- |
| **returns** | 0, STATUS_STALE when this backend knows the value under a newer opening, the refusal of a socket that is not an internet socket, or ENOMEM |

## Forwards

### Vector

Forwards [`std.net.async.types.Vector`](types.md#vector).

```mach
pub rec Vector {
    data:   *u8;
    length: usize;
}
```

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

### NativeCompletion

Forwards [`std.net.async.types.NativeCompletion`](types.md#nativecompletion).

```mach
pub rec NativeCompletion {
    context:       usize;
    kind:          std.io.runtime.Kind;
    bytes:         usize;
    items:         usize;
    resource:      usize;
    status:        i64;
    end_of_stream: bool;
}
```

### CANCEL_NEEDS_NATIVE_CONTROL

Forwards [`std.net.async.readiness.CANCEL_NEEDS_NATIVE_CONTROL`](readiness.md#constants).

```mach
pub val CANCEL_NEEDS_NATIVE_CONTROL: bool = true
```

cancel ends native access synchronously, so it runs while no thread is
inside the native wait

### Backend

Forwards [`std.net.async.readiness.Backend`](readiness.md#backend).

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

### aliases

Forwards [`std.net.async.readiness.aliases`](readiness.md#aliases).

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

### submit_read

Forwards [`std.net.async.readiness.submit_read`](readiness.md#submit_read).

```mach
pub fun submit_read(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_readable

Forwards [`std.net.async.readiness.submit_readable`](readiness.md#submit_readable).

```mach
pub fun submit_readable(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

wait for the stream to be readable without a buffer: the completion reports
end_of_stream at orderly EOF, and nothing is read

### submit_write

Forwards [`std.net.async.readiness.submit_write`](readiness.md#submit_write).

```mach
pub fun submit_write(backend: *Backend, native: usize, opening: u64, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_shutdown_write

Forwards [`std.net.async.readiness.submit_shutdown_write`](readiness.md#submit_shutdown_write).

```mach
pub fun submit_shutdown_write(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

### submit_close

Forwards [`std.net.async.readiness.submit_close`](readiness.md#submit_close).

```mach
pub fun submit_close(backend: *Backend, native: usize, opening: u64, context: usize, token: *std.net.async.types.Token) i64
```

### cancel

Forwards [`std.net.async.readiness.cancel`](readiness.md#cancel).

```mach
pub fun cancel(backend: *Backend, token: std.net.async.types.Token, finished: *opt[std.net.async.types.NativeCompletion]) i64
```

cancel an operation. one that already finished and waits to be published is
withdrawn and handed back through finished, whatever it moved included, so the
caller reports it with the cancellation: an accepted socket in it is the
caller's to hand over or close

### flush

Forwards [`std.net.async.readiness.flush`](readiness.md#flush).

```mach
pub fun flush(backend: *Backend) i64
```

### dispatch

Forwards [`std.net.async.readiness.dispatch`](readiness.md#dispatch).

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

Forwards [`std.net.async.readiness.poll`](readiness.md#poll).

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion retrieval

### completion

Forwards [`std.net.async.readiness.completion`](readiness.md#completion).

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

### dnit

Forwards [`std.net.async.readiness.dnit`](readiness.md#dnit).

```mach
pub fun dnit(backend: *Backend) i64
```

