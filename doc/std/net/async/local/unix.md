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
| [`create_connect`](#create_connect), [`cleanup_listener`](#cleanup_listener), [`rename_listener`](#rename_listener), [`close_resource`](#close_resource) | |
| [`detach`](#detach) | give up a socket with nothing queued on it, so another backend can take it: its registration and record go and the socket stays open |
| [`submit_accept`](#submit_accept), [`submit_connect`](#submit_connect), [`submit_read`](#submit_read), [`submit_readable`](#submit_readable), [`submit_write`](#submit_write), [`submit_shutdown_write`](#submit_shutdown_write), [`submit_close`](#submit_close) | |

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

### cleanup_listener

```mach
pub fun cleanup_listener(listener: *std.net.local.types.Listener) i64
```

### rename_listener

```mach
pub fun rename_listener(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) i64
```

### close_resource

```mach
pub fun close_resource(backend: *std.net.async.readiness.Backend, resource: usize) i64
```

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
pub fun submit_accept(backend: *std.net.async.readiness.Backend, listener: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_connect

```mach
pub fun submit_connect(backend: *std.net.async.readiness.Backend, resource_value: usize, peer: std.net.local.endpoint.Endpoint, context: usize, token: *std.net.async.types.Token) i64
```

### submit_read

```mach
pub fun submit_read(backend: *std.net.async.readiness.Backend, resource_value: usize, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_readable

```mach
pub fun submit_readable(backend: *std.net.async.readiness.Backend, resource_value: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_write

```mach
pub fun submit_write(backend: *std.net.async.readiness.Backend, resource_value: usize, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *std.net.async.readiness.Backend, resource_value: usize, context: usize, token: *std.net.async.types.Token) i64
```

### submit_close

```mach
pub fun submit_close(backend: *std.net.async.readiness.Backend, resource_value: usize, context: usize, token: *std.net.async.types.Token) i64
```

## Forwards

### Token

Forwards [`std.net.async.types.Token`](../types.md#token).

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

### NativeCompletion

Forwards [`std.net.async.types.NativeCompletion`](../types.md#nativecompletion).

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

### aliases

Forwards [`std.net.async.readiness.aliases`](../readiness.md#aliases).

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

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

### dispatch

Forwards [`std.net.async.readiness.dispatch`](../readiness.md#dispatch).

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

### dnit

Forwards [`std.net.async.readiness.dnit`](../readiness.md#dnit).

```mach
pub fun dnit(backend: *Backend) i64
```

