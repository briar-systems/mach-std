[std](../../../README.md) / [net](../../README.md) / [async](../README.md) / [local](README.md) / **unix**

# std.net.async.local.unix

bounded local unix readiness backend
backend for std.net.async.local, signatures may change in a minor release (README, API surface)
the engine is std.net.async.readiness. a local handle carries no opening.

Source: [`src/net/async/local/unix.mach`](../../../../../src/net/async/local/unix.mach)

Uses types from [`std.allocator`](../../../allocator.md), [`std.net.async.readiness`](../readiness.md), [`std.net.async.types`](../types.md), [`std.net.local.endpoint`](../../local/endpoint.md), [`std.net.local.types`](../../local/types.md), [`std.system.os.shared`](../../../system/os/shared.md).

| Functions | |
| :--- | :--- |
| [`init`](#init) | initial is the size the backend starts at: the operation, resource and ready tables grow on demand and the resource map rehashes with them |
| [`create_connect`](#create_connect) | create a nonblocking local stream socket to connect to an endpoint |
| [`cleanup_listener`](#cleanup_listener) | remove a listener's socket file when it is still the node the listener bound |
| [`rename_listener`](#rename_listener) | move a listener's socket file to another path |
| [`close_resource`](#close_resource) | close a native socket outside any operation |
| [`detach`](#detach) | give up a socket with nothing queued on it, so another backend can take it: its registration and record go and the socket stays open |
| [`submit_accept`](#submit_accept) | queue an accept on a listening socket |
| [`submit_connect`](#submit_connect) | queue a connect of a socket to a local endpoint |
| [`submit_read`](#submit_read) | queue a read into a borrowed buffer |
| [`submit_readable`](#submit_readable) | queue a wait for the stream to be readable, reading nothing |
| [`submit_write`](#submit_write) | queue a write from a borrowed buffer |
| [`submit_shutdown_write`](#submit_shutdown_write) | queue a shutdown of the write side, behind the writes already queued |
| [`submit_close`](#submit_close) | queue a close, which closes the native socket once its queued writes finish |

| Forwards | |
| :--- | :--- |
| [`Token`](#token), [`NativeCompletion`](#nativecompletion), [`CANCEL_NEEDS_NATIVE_CONTROL`](#cancel_needs_native_control), [`Backend`](#backend), [`aliases`](#aliases), [`cancel`](#cancel), [`flush`](#flush), [`dispatch`](#dispatch), [`poll`](#poll), [`completion`](#completion), [`dnit`](#dnit) | |

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

### create_connect

```mach
pub fun create_connect(value: std.net.local.endpoint.Endpoint, resource: *usize) i64
```

create a nonblocking local stream socket to connect to an endpoint

| Parameter | |
| :--- | :--- |
| `value` | the endpoint it will connect to |
| `resource` | receives the socket, owned by the caller |
| **returns** | 0, or a negative native error |

### cleanup_listener

```mach
pub fun cleanup_listener(listener: *std.net.local.types.Listener) i64
```

remove a listener's socket file when it is still the node the listener bound

| Parameter | |
| :--- | :--- |
| `listener` | the listener |
| **returns** | 0, also when nothing is there, EBUSY when the path is not the listener's node, or a negative native error |

### rename_listener

```mach
pub fun rename_listener(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) i64
```

move a listener's socket file to another path

| Parameter | |
| :--- | :--- |
| `listener` | the listener |
| `replacement` | the new endpoint |
| **returns** | 0, EEXIST when the new path is taken, EBUSY when the old path is not the listener's node, or a negative native error |

### close_resource

```mach
pub fun close_resource(backend: *std.net.async.readiness.Backend, resource: usize) i64
```

close a native socket outside any operation

| Parameter | |
| :--- | :--- |
| `backend` | unused |
| `resource` | the native socket |
| **returns** | 0, or a negative native error |

### detach

```mach
pub fun detach(backend: *std.net.async.readiness.Backend, resource_value: usize) i64
```

give up a socket with nothing queued on it, so another backend can take it:
its registration and record go and the socket stays open

| Parameter | |
| :--- | :--- |
| `resource_value` | the socket to give up |
| **returns** | 0, EBUSY while an operation or a close is queued on it, or the native refusal to deregister, which leaves the record as it was |

### submit_accept

```mach
pub fun submit_accept(backend: *std.net.async.readiness.Backend, listener: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue an accept on a listening socket

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `listener` | the native listening socket |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error. the completion's resource is the accepted socket, nonblocking and owned by the caller |

### submit_connect

```mach
pub fun submit_connect(backend: *std.net.async.readiness.Backend, resource_value: usize, peer: std.net.local.endpoint.Endpoint, context: u64, token: *std.net.async.types.Token) i64
```

queue a connect of a socket to a local endpoint

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket |
| `peer` | the endpoint to connect to, copied |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

### submit_read

```mach
pub fun submit_read(backend: *std.net.async.readiness.Backend, resource_value: usize, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a read into a borrowed buffer. descriptor rights sent with the bytes are
closed on linux and fail the read with ENOTSUP on darwin

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket |
| `buffer` | where the bytes go, borrowed until the operation completes |
| `length` | the buffer size in bytes |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

### submit_readable

```mach
pub fun submit_readable(backend: *std.net.async.readiness.Backend, resource_value: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a wait for the stream to be readable, reading nothing

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

### submit_write

```mach
pub fun submit_write(backend: *std.net.async.readiness.Backend, resource_value: usize, buffer: *u8, length: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a write from a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket |
| `buffer` | the bytes to send, borrowed until the operation completes |
| `length` | bytes to send |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *std.net.async.readiness.Backend, resource_value: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a shutdown of the write side, behind the writes already queued

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

### submit_close

```mach
pub fun submit_close(backend: *std.net.async.readiness.Backend, resource_value: usize, context: u64, token: *std.net.async.types.Token) i64
```

queue a close, which closes the native socket once its queued writes finish

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource_value` | the native socket, owned by the backend from here |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once queued, or a negative native error |

## Forwards

### Token

Forwards [`std.net.async.types.Token`](../types.md#token).

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

names one operation a backend holds, refused once the slot is reused

### NativeCompletion

Forwards [`std.net.async.types.NativeCompletion`](../types.md#nativecompletion).

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

### CANCEL_NEEDS_NATIVE_CONTROL

Forwards [`std.net.async.readiness.CANCEL_NEEDS_NATIVE_CONTROL`](../readiness.md#constants).

```mach
pub val CANCEL_NEEDS_NATIVE_CONTROL: bool = true
```

cancel ends native access synchronously, so it runs while no thread is
inside the native wait

### Backend

Forwards [`std.net.async.readiness.Backend`](../readiness.md#backend).

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

### aliases

Forwards [`std.net.async.readiness.aliases`](../readiness.md#aliases).

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

whether a caller range overlaps memory the backend owns

### cancel

Forwards [`std.net.async.readiness.cancel`](../readiness.md#cancel).

```mach
pub fun cancel(backend: *Backend, token: std.net.async.types.Token, finished: *opt[std.net.async.types.NativeCompletion]) i64
```

cancel an operation. one that already finished and waits to be published is
withdrawn and handed back through finished, whatever it moved included, so the
caller reports it with the cancellation: an accepted socket in it is the
caller's to hand over or close

### flush

Forwards [`std.net.async.readiness.flush`](../readiness.md#flush).

```mach
pub fun flush(backend: *Backend) i64
```

publish the finished operations without waiting

### dispatch

Forwards [`std.net.async.readiness.dispatch`](../readiness.md#dispatch).

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

### poll

Forwards [`std.net.async.readiness.poll`](../readiness.md#poll).

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion retrieval

### completion

Forwards [`std.net.async.readiness.completion`](../readiness.md#completion).

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

copy out one completion the last publish made readable

### dnit

Forwards [`std.net.async.readiness.dnit`](../readiness.md#dnit).

```mach
pub fun dnit(backend: *Backend) i64
```

release the backend, its idle resources and their registrations

