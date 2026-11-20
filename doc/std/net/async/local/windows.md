[std](../../../README.md) / [net](../../README.md) / [async](../README.md) / [local](README.md) / **windows**

# std.net.async.local.windows

bounded windows iocp backend for af_unix streams
backend for std.net.async.local, signatures may change in a minor release (README, API surface)

Source: [`src/net/async/local/windows.mach`](../../../../../src/net/async/local/windows.mach)

Uses types from [`std.allocator`](../../../allocator.md), [`std.net.async.iocp.port`](../iocp/port.md), [`std.net.async.types`](../types.md), [`std.net.local.endpoint`](../../local/endpoint.md), [`std.net.local.types`](../../local/types.md), [`std.system.os.shared`](../../../system/os/shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`Operation`](#operation) | `rec` | a local stream request needs nothing beyond the completion port layer's part |

| Functions | |
| :--- | :--- |
| [`init`](#init) | initial is the size the backend starts at: every table grows on demand |
| [`submit_read`](#submit_read) | post an overlapped read into a borrowed buffer |
| [`submit_readable`](#submit_readable) | wait for the stream to be readable without a buffer: an overlapped zero-byte receive, settled on completion by the queued byte count |
| [`submit_write`](#submit_write) | post an overlapped write from a borrowed buffer |
| [`create_connect`](#create_connect) | create a nonblocking local stream socket to connect to an endpoint |
| [`cleanup_listener`](#cleanup_listener) | remove a listener's socket file when it is still the node the listener bound |
| [`rename_listener`](#rename_listener) | move a listener's socket file to another path |
| [`close_resource`](#close_resource) | close a native socket without a completion |
| [`detach`](#detach) | give up a socket with nothing on it, so another backend can take it: the socket leaves the completion port and stays open |
| [`submit_accept`](#submit_accept) | post an overlapped accept on a listening socket, into a socket made for it here |
| [`submit_connect`](#submit_connect) | post an overlapped connect to a local endpoint, binding the socket first when it is unbound |
| [`submit_shutdown_write`](#submit_shutdown_write) | a shutdown waits for the socket's writes, and runs once none is left |
| [`submit_close`](#submit_close) | a close aborts the socket's requests and completes once they have all left |

| Constants | |
| :--- | :--- |
| [`CANCEL_NEEDS_NATIVE_CONTROL`](#constants) | cancel only requests the abort and its packet settles it through dispatch, so it never needs the native wait to yield |

| Forwards | |
| :--- | :--- |
| [`Token`](#token), [`NativeCompletion`](#nativecompletion), [`Backend`](#backend), [`aliases`](#aliases), [`cancel`](#cancel), [`flush`](#flush), [`dispatch`](#dispatch), [`poll`](#poll), [`completion`](#completion), [`dnit`](#dnit), [`awaiting_cancellations`](#awaiting_cancellations) | |

---

## Operation

```mach
pub rec Operation {
    header: std.net.async.iocp.port.Header;
}
```

a local stream request needs nothing beyond the completion port layer's part

## Functions

### init

```mach
pub fun init(backend: *Backend, queue: *std.system.os.shared.IoQueue, a: *std.allocator.Allocator, initial: usize, source_id: u16) i64
```

initial is the size the backend starts at: every table grows on demand

### submit_read

```mach
pub fun submit_read(backend: *Backend, resource: usize, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

post an overlapped read into a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `buffer` | where the bytes go, borrowed until the operation completes |
| `length` | the buffer size in bytes, at most 0xffffffff |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted or held behind an earlier readiness wait, or a negative native error |

### submit_readable

```mach
pub fun submit_readable(backend: *Backend, resource: usize, context: usize, token: *std.net.async.types.Token) i64
```

wait for the stream to be readable without a buffer: an overlapped zero-byte
receive, settled on completion by the queued byte count

### submit_write

```mach
pub fun submit_write(backend: *Backend, resource: usize, buffer: *u8, length: usize, context: usize, token: *std.net.async.types.Token) i64
```

post an overlapped write from a borrowed buffer

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `buffer` | the bytes to send, borrowed until the operation completes |
| `length` | bytes to send, at most 0xffffffff |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error |

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
| **returns** | 0, also when nothing is there, EBUSY when the path is not the listener's node or its identity cannot be read, or a negative native error |

### rename_listener

```mach
pub fun rename_listener(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) i64
```

move a listener's socket file to another path

| Parameter | |
| :--- | :--- |
| `listener` | the listener |
| `replacement` | the new endpoint |
| **returns** | 0, or a negative native error |

### close_resource

```mach
pub fun close_resource(backend: *Backend, resource: usize) i64
```

close a native socket without a completion. its outstanding requests settle in the background

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| **returns** | 0, or a negative native error |

### detach

```mach
pub fun detach(backend: *Backend, resource: usize) i64
```

give up a socket with nothing on it, so another backend can take it: the
socket leaves the completion port and stays open. a local stream is told
apart by its driver's tokens, so no record is kept

### submit_accept

```mach
pub fun submit_accept(backend: *Backend, listener: usize, context: usize, token: *std.net.async.types.Token) i64
```

post an overlapped accept on a listening socket, into a socket made for it here

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `listener` | the native listening socket |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error. the completion's resource is the accepted socket, owned by the caller |

### submit_connect

```mach
pub fun submit_connect(backend: *Backend, resource: usize, peer: std.net.local.endpoint.Endpoint, context: usize, token: *std.net.async.types.Token) i64
```

post an overlapped connect to a local endpoint, binding the socket first when it is unbound

| Parameter | |
| :--- | :--- |
| `backend` | the backend |
| `resource` | the native socket |
| `peer` | the endpoint to connect to |
| `context` | the caller's context, carried to the completion |
| `token` | receives the operation's token |
| **returns** | 0 once posted, or a negative native error. ENOTSUP or EINVAL for an endpoint with no socket address |

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(backend: *Backend, resource: usize, context: usize, token: *std.net.async.types.Token) i64
```

a shutdown waits for the socket's writes, and runs once none is left

### submit_close

```mach
pub fun submit_close(backend: *Backend, resource: usize, context: usize, token: *std.net.async.types.Token) i64
```

a close aborts the socket's requests and completes once they have all left

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANCEL_NEEDS_NATIVE_CONTROL` | `bool` | `false` | cancel only requests the abort and its packet settles it through dispatch, so it never needs the native wait to yield |

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
    context:       usize;
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

Forwards [`std.net.async.iocp.port.Backend`](../iocp/port.md#backend).

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

Forwards [`std.net.async.iocp.port.aliases`](../iocp/port.md#aliases).

```mach
pub fun aliases(backend: *Backend, data: *u8, len: usize) bool
```

whether a caller range overlaps memory the backend owns

### cancel

Forwards [`std.net.async.iocp.port.cancel`](../iocp/port.md#cancel).

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

Forwards [`std.net.async.iocp.port.flush`](../iocp/port.md#flush).

```mach
pub fun flush(backend: *Backend) i64
```

publish the settled controls without waiting

### dispatch

Forwards [`std.net.async.iocp.port.dispatch`](../iocp/port.md#dispatch).

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

handle one packet the runtime's shared queue delivered

### poll

Forwards [`std.net.async.iocp.port.poll`](../iocp/port.md#poll).

```mach
pub fun poll(backend: *Backend, timeout_ms: i32) i64
```

one thread owns poll and completion storage

### completion

Forwards [`std.net.async.iocp.port.completion`](../iocp/port.md#completion).

```mach
pub fun completion(backend: *Backend, index: usize, out: *std.net.async.types.NativeCompletion) i64
```

copy out one completion the last publish made readable

### dnit

Forwards [`std.net.async.iocp.port.dnit`](../iocp/port.md#dnit).

```mach
pub fun dnit(backend: *Backend) i64
```

a cancelled operation keeps the backend busy until its packet is consumed

### awaiting_cancellations

Forwards [`std.net.async.iocp.port.awaiting_cancellations`](../iocp/port.md#awaiting_cancellations).

```mach
pub fun awaiting_cancellations(backend: *Backend) usize
```

cancelled operations whose packet has not arrived yet

