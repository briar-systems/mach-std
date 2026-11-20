[std](../../README.md) / [net](../README.md) / [async](README.md) / **local**

# std.net.async.local

portable bounded asynchronous local byte streams

reads follow std.net.local's byte-only receive contract, under this backend's
read lane ownership. a buffer stays borrowed until its completion, and a
darwin refusal completes with zero bytes and leaves the stream open. the
generic linux and darwin net.async backends accept only ip socket handles,
checked before registration, so a local handle never reaches a byte path that
does not own rights: use this backend for local streams.

cancellation follows std.net.async: on windows a cancelled operation completes
once its aborted request reports back, and a cancelled completion reports the
bytes a read took, which the caller must consume, or a write sent
(submit_read, submit_write)

Source: [`src/net/async/local.mach`](../../../../src/net/async/local.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.io.error`](../../io/error.md), [`std.io.lifecycle`](../../io/lifecycle.md), [`std.io.runtime`](../../io/runtime.md), [`std.memory.table`](../../memory/table.md), [`std.net.local.endpoint`](../local/endpoint.md), [`std.net.local.types`](../local/types.md), [`std.sync.cancel`](../../sync/cancel.md), [`std.sync.mutex`](../../sync/mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Listener`](#listener) | `rec` | listener tokens are resolved only by the driver that created them |
| [`Stream`](#stream) | `rec` | a stream token, resolved only by the driver that created it |
| [`Detached`](#detached) | `rec` | an accepted or connected stream taken out of its driver by detach, owning the socket and nothing of any driver |
| [`Driver`](#driver) | `rec` | an asynchronous local stream driver: a runtime source over the platform backend |

| On `Driver` | |
| :--- | :--- |
| [`aliases`](#aliases) | whether a byte range overlaps the driver, its platform backend or its borrowed runtime |
| [`init`](#init) | the driver starts at the runtime's initial size and grows with it |
| [`submit_bind`](#submit_bind) | bind a listener to a local endpoint |
| [`bound_listener`](#bound_listener) | the listener a bind completion made |
| [`submit_listen`](#submit_listen) | start listening on a bound listener |
| [`listening`](#listening) | whether a listen completion left its listener listening |
| [`listener_rename`](#listener_rename) | managed listeners must rename through their owning driver |
| [`submit_accept`](#submit_accept) | queue an accept on a listening listener |
| [`submit_connect`](#submit_connect) | create a stream socket and queue its connect to a local endpoint |
| [`submit_read`](#submit_read) | a read cancelled through its scope completes with has_error set and the cancel or timeout reason, and still reports in bytes and end_of_stream what it took before the cancellation took effect |
| [`submit_readable`](#submit_readable) | wait until the local stream is readable, at orderly end of stream, or failed, without holding a buffer |
| [`submit_write`](#submit_write) | cancelling a write does not unsend it |
| [`submit_shutdown_write`](#submit_shutdown_write) | queue a shutdown of the stream's write side, behind the writes already queued |
| [`submit_stream_close`](#submit_stream_close) | close a stream the driver holds |
| [`submit_listener_close`](#submit_listener_close) | close a listener, removing its socket file when the listener owns it |
| [`awaiting_cancellations`](#awaiting_cancellations) | operations cancelled on this driver whose native request has not yet reported back |
| [`wait`](#wait) | returns 0 only on timeout, a caller's io.runtime.wake, or a closed runtime |
| [`accepted`](#accepted) | the stream an accept completion hands over, whether it succeeded or was cancelled after its stream was already accepted |
| [`connected`](#connected) | the stream a connect completion opened |
| [`detach`](#detach) | take an open stream out of this driver, so another driver, on this thread or another, can adopt it |
| [`adopt`](#adopt) | register a detached stream with this driver |
| [`peer_identity`](#peer_identity) | the credentials of the process at the other end of a stream |
| [`dnit`](#dnit) | release the driver once no operation is in flight, closing every listener and stream it holds |

---

## Listener

```mach
pub rec Listener {
    index:      u32;
    generation: u32;
    owner:      u64;
}
```

listener tokens are resolved only by the driver that created them

## Stream

```mach
pub rec Stream {
    index:      u32;
    generation: u32;
    owner:      u64;
}
```

a stream token, resolved only by the driver that created it

| Field | Type | |
| :--- | :--- | :--- |
| `index` | `u32` | the stream's entry in the driver |
| `generation` | `u32` | the entry's generation, 0 once the stream was closed or detached |
| `owner` | `u64` | the instance of the driver that created it |

## Detached

```mach
pub rec Detached {
    stream: std.net.local.types.Stream;
}
```

an accepted or connected stream taken out of its driver by detach, owning the
socket and nothing of any driver. adopt hands it to a driver, and one never
adopted is closed with std.net.local.stream_close

## Driver

```mach
pub rec Driver {
    runtime: *std.io.runtime.Runtime;
    source:  std.io.runtime.SourceToken;
    backend: impl.Backend;
    # where every table's chunks come from
    allocator: std.allocator.Allocator;
    slots:     std.memory.table.Table;
    listeners: std.memory.table.Table;
    streams:   std.memory.table.Table;
    # active slots per chunk of the slot table, which is indexed by runtime
    # token index and so needs no generation floor of its own
    slot_live: [table.DIRECTORY]usize;
    # free entries, lowest chunk first, each pool's floor the generation a
    # regrown chunk's entries start from
    listener_pool:     std.memory.table.Pool;
    stream_pool:       std.memory.table.Pool;
    backend_destroyed: bool;
    cleanup_code:      i64;
    instance:          u64;
    lock:              std.sync.mutex.Mutex;
}
```

an asynchronous local stream driver: a runtime source over the platform backend

| Field | Type | |
| :--- | :--- | :--- |
| `runtime` | `*std.io.runtime.Runtime` | the runtime it is registered with, borrowed |
| `source` | `std.io.runtime.SourceToken` | its source registration in the runtime |
| `backend` | `impl.Backend` | the platform backend |
| `slots` | `std.memory.table.Table` | one slot per runtime token index routed here |
| `listeners` | `std.memory.table.Table` | listener entries |
| `streams` | `std.memory.table.Table` | stream entries |
| `backend_destroyed` | `bool` | dnit has already released the backend |
| `cleanup_code` | `i64` | the first native failure while closing at dnit |
| `instance` | `u64` | this driver's process-unique number, stamped on its tokens |
| `lock` | `std.sync.mutex.Mutex` | guards the tables and the backend |

### aliases

```mach
pub fun aliases(driver: *Driver, data: *u8, len: usize) bool
```

whether a byte range overlaps the driver, its platform backend or its
borrowed runtime. the contract is std.io.runtime.aliases's

### init

```mach
pub fun init(driver: *Driver, runtime: *std.io.runtime.Runtime) err[std.io.error.Error]
```

the driver starts at the runtime's initial size and grows with it

### submit_bind

```mach
pub fun submit_bind(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    bound: std.net.local.endpoint.Endpoint,
    options: std.net.local.types.BindOptions,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

bind a listener to a local endpoint. the bind runs now and its completion
carries the result for bound_listener

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `bound` | the endpoint to bind |
| `options` | how to bind |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, or the refusal: INVALID for a nil argument or an unsupported endpoint, RESOURCE_EXHAUSTED when no listener entry can be made, or the runtime's refusal. a failed bind is reported in the completion |

### bound_listener

```mach
pub fun bound_listener(driver: *Driver, completion: std.io.runtime.Completion) res[Listener, std.io.error.Error]
```

the listener a bind completion made

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `completion` | the bind's completion |
| **returns** | the listener's token, the completion's error, INVALID for a nil driver or another kind, or CLOSED when the listener is gone |

### submit_listen

```mach
pub fun submit_listen(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    listener: *Listener,
    backlog: i32,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

start listening on a bound listener. the listen runs now and its completion carries the result

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `listener` | the bound listener's token |
| `backlog` | the pending connection queue length, above 0 |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, or the refusal: INVALID for a bad argument, CLOSED when the listener is not bound here, or the runtime's refusal. a failed listen is reported in the completion |

### listening

```mach
pub fun listening(driver: *Driver, completion: std.io.runtime.Completion) err[std.io.error.Error]
```

whether a listen completion left its listener listening

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `completion` | the listen's completion |
| **returns** | ok, the completion's error, INVALID for a nil driver or another kind, or CLOSED when the listener is gone or not listening |

### listener_rename

```mach
pub fun listener_rename(
    driver: *Driver,
    listener: *Listener,
    replacement: std.net.local.endpoint.Endpoint,
) err[std.io.error.Error]
```

managed listeners must rename through their owning driver

### submit_accept

```mach
pub fun submit_accept(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    listener: *Listener,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

queue an accept on a listening listener

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `listener` | the listening listener's token |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, whose completion goes to accepted, or the refusal: INVALID for a nil argument, CLOSED when the listener is not listening here, RESOURCE_EXHAUSTED when no stream entry can be made, or the runtime's refusal |

### submit_connect

```mach
pub fun submit_connect(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    remote: std.net.local.endpoint.Endpoint,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

create a stream socket and queue its connect to a local endpoint

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `remote` | the endpoint to connect to |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, whose completion goes to connected, or the refusal: INVALID for a bad argument, the socket creation failure, RESOURCE_EXHAUSTED when no stream entry can be made, or the runtime's refusal |

### submit_read

```mach
pub fun submit_read(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *Stream, buffer: *u8, length: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

a read cancelled through its scope completes with has_error set and the
cancel or timeout reason, and still reports in bytes and end_of_stream what it
took before the cancellation took effect. those bytes are in buffer and
belong to the stream: the peer considers them delivered and no later read
returns them, so a caller that cancels a read consumes bytes from the
cancelled completion like any other read's

### submit_readable

```mach
pub fun submit_readable(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *Stream, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

wait until the local stream is readable, at orderly end of stream, or failed,
without holding a buffer. the completion is the same as net.async's
submit_readable: kind READABLE, zero bytes, end_of_stream at orderly EOF

### submit_write

```mach
pub fun submit_write(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *Stream, buffer: *u8, length: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

cancelling a write does not unsend it. a cancelled write completes with
has_error set and reports in bytes what it sent before the cancellation took
effect, so the stream continues after exactly those bytes

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *Stream, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

queue a shutdown of the stream's write side, behind the writes already queued

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `stream` | the open stream's token |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, or the refusal: INVALID for a nil argument, CLOSED when the stream is not open here, or the runtime's refusal |

### submit_stream_close

```mach
pub fun submit_stream_close(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    stream: *Stream,
    mode: std.io.lifecycle.Mode,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

close a stream the driver holds. a graceful close shuts the write side down,
and an abortive close cancels pending reads and closes the socket

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `stream` | the open stream's token, zeroed once an abortive close is taken |
| `mode` | GRACEFUL or ABORTIVE |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, or the refusal: INVALID for a bad argument, CLOSED when the stream is not open here, or the runtime's refusal |

### submit_listener_close

```mach
pub fun submit_listener_close(driver: *Driver, scope: *std.sync.cancel.Scope, listener: *Listener, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

close a listener, removing its socket file when the listener owns it

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `scope` | the cancel scope the operation joins |
| `listener` | the listener's token, zeroed once the backend takes the close |
| `context` | the caller's context, carried to the completion |
| **returns** | the operation's token, or the refusal: INVALID for a nil argument, CLOSED when the listener is not bound or listening here, or the runtime's refusal |

### awaiting_cancellations

```mach
pub fun awaiting_cancellations(driver: *Driver) usize
```

operations cancelled on this driver whose native request has not yet
reported back. each one keeps the driver busy, so a destroy that keeps
refusing with a nonzero count is waiting for the kernel, which a caller
settles by continuing to wait. always 0 on linux and darwin, which cancel
synchronously

### wait

```mach
pub fun wait(
    driver: *Driver,
    output: *std.io.runtime.Completion,
    output_capacity: usize,
    timeout_ms: i32,
) res[usize, std.io.error.Error]
```

returns 0 only on timeout, a caller's io.runtime.wake, or a closed runtime

### accepted

```mach
pub fun accepted(driver: *Driver, completion: std.io.runtime.Completion) res[Stream, std.io.error.Error]
```

the stream an accept completion hands over, whether it succeeded or was
cancelled after its stream was already accepted. a caller that cancels
accepts takes the stream from every accept completion and serves or closes it

| Parameter | |
| :--- | :--- |
| **returns** | the stream, which the caller now owns, or the completion's error when it hands nothing over |

### connected

```mach
pub fun connected(driver: *Driver, completion: std.io.runtime.Completion) res[Stream, std.io.error.Error]
```

the stream a connect completion opened

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `completion` | the connect's completion |
| **returns** | the stream's token, the completion's error, INVALID for a nil driver or another kind, or CLOSED when the stream is gone |

### detach

```mach
pub fun detach(driver: *Driver, stream: *Stream) res[Detached, std.io.error.Error]
```

take an open stream out of this driver, so another driver, on this thread or
another, can adopt it

the stream must be idle: every operation submitted on it has had its
completion returned by wait. a stream with an operation in flight is refused
BUSY and nothing changes. on success the driver keeps nothing of the stream:
its entry is freed under the table's generation floor and stream's token is
zeroed, so this token and every copy of it are refused by this driver and by
any other

| Parameter | |
| :--- | :--- |
| `driver` | the driver the stream belongs to |
| `stream` | the stream's token |
| **returns** | the detached stream, which owns the socket, or the refusal: CLOSED for a token this driver does not hold open, BUSY while an operation is in flight, or the platform's refusal to give the socket up |

### adopt

```mach
pub fun adopt(driver: *Driver, detached: *Detached) res[Stream, std.io.error.Error]
```

register a detached stream with this driver

the stream is open here as though this driver had accepted or connected it.
on success detached gives up the socket, so a second adopt of it is refused

| Parameter | |
| :--- | :--- |
| `driver` | the driver that takes the stream |
| `detached` | the stream detach returned |
| **returns** | the stream's token in this driver, or the refusal, which leaves detached owning the socket |

### peer_identity

```mach
pub fun peer_identity(driver: *Driver, stream: *Stream) res[std.net.local.types.PeerIdentity, std.io.error.Error]
```

the credentials of the process at the other end of a stream

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| `stream` | the open stream's token |
| **returns** | the identity, INVALID for a nil argument, CLOSED when the stream is not open here, or the platform's refusal |

### dnit

```mach
pub fun dnit(driver: *Driver) err[std.io.error.Error]
```

release the driver once no operation is in flight, closing every listener and stream it holds

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| **returns** | ok, INVALID for a nil or released driver, BUSY while an operation's completion has not been released, or the first failure to close or release |

