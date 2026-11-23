[std](../README.md) / [net](README.md) / **async**

# std.net.async

portable bounded asynchronous TCP and UDP

ownership: a socket this driver has seen in a submission is closed through
the driver (submit_stream_close, submit_datagram_close), never directly. a
socket closed outside the driver is detected on its next submission through
either handle: the old socket's pending work completes CLOSED with code 0,
a submission through the old handle is refused the same way, and the socket
that now holds the native value keeps its own state. the driver tells the
two apart by the handle's opening (std.io.handle.socket), so wrap a native
socket once and pass that handle around

cancellation: an operation cancelled through its scope completes CANCELLED
once the platform gives up its buffers. on windows that happens when the
aborted request reports back, so the completion can arrive after the cancel
returns and destroy stays busy until it does (awaiting_cancellations). a
cancelled completion still reports the transfer that finished before the
cancellation: a read's bytes, which the caller must consume, a write's sent
bytes and a batch's datagrams (submit_read, submit_write), and the socket an
accept took, which the caller owns (accepted)

Source: [`src/net/async.mach`](../../../src/net/async.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.io.error`](../io/error.md), [`std.io.lifecycle`](../io/lifecycle.md), [`std.io.runtime`](../io/runtime.md), [`std.memory.table`](../memory/table.md), [`std.net.async.types`](async/types.md), [`std.net.ip`](ip.md), [`std.net.socket`](socket.md), [`std.net.tcp`](tcp.md), [`std.net.udp`](udp.md), [`std.sync.cancel`](../sync/cancel.md), [`std.sync.mutex`](../sync/mutex.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Driver`](#driver) | `rec` | the driver borrows one io runtime and never creates a second native queue |
| [`Detached`](#detached) | `rec` | an accepted or connected stream taken out of its driver by detach, owning the socket and nothing of any driver |

| On `Driver` | |
| :--- | :--- |
| [`aliases`](#aliases) | whether a byte range overlaps the driver, its platform backend or its borrowed runtime |
| [`init`](#init) | the driver starts at the runtime's initial size and grows with it |
| [`submit_accept`](#submit_accept) | the socket is closed through this driver once submitted (module header) |
| [`submit_connect`](#submit_connect) | the socket is closed through this driver once submitted (module header) |
| [`submit_read`](#submit_read) | the socket is closed through this driver once submitted (module header) |
| [`submit_readable`](#submit_readable) | wait until the stream is readable, at orderly end of stream, or failed, without holding a buffer |
| [`submit_write`](#submit_write) | cancelling a write does not unsend it |
| [`submit_write_vector`](#submit_write_vector) | the socket is closed through this driver once submitted (module header) |
| [`submit_receive_batch`](#submit_receive_batch) | receive up to count datagrams into packets |
| [`submit_send_batch`](#submit_send_batch) | the socket is closed through this driver once submitted (module header) |
| [`submit_shutdown_write`](#submit_shutdown_write) | the socket is closed through this driver once submitted (module header) |
| [`submit_stream_close`](#submit_stream_close) | close a stream the driver knows about |
| [`submit_datagram_close`](#submit_datagram_close) | close a datagram socket the driver knows about |
| [`submit_listener_close`](#submit_listener_close) | close a listener the driver knows about |
| [`detach`](#detach) | take a stream this driver accepted or connected out of it, so another driver, on this thread or another, can adopt it |
| [`adopt`](#adopt) | register a detached stream with this driver |
| [`awaiting_cancellations`](#awaiting_cancellations) | operations cancelled on this driver whose native request has not yet reported back |
| [`wait`](#wait) | one thread owns wait; submission may run concurrently returns 0 only on timeout, a caller's io.runtime.wake, or a closed runtime |
| [`dnit`](#dnit) | tear down an idle driver: retire its runtime source, destroy its backend and free its slot table |

| Functions | |
| :--- | :--- |
| [`listen`](#listen) | a nonblocking listener for this driver's runtime |
| [`bind_datagram`](#bind_datagram) | a nonblocking datagram socket bound to an endpoint |
| [`listen_with`](#listen_with) | a nonblocking listener with explicit options, for this driver's runtime |
| [`bind_datagram_with`](#bind_datagram_with) | a nonblocking datagram socket bound with explicit options |
| [`create_datagram`](#create_datagram) | an unbound nonblocking datagram socket |
| [`stream`](#stream) | the stream an accept or connect completion hands over |
| [`accepted`](#accepted) | the stream an accept completion hands over, whether it succeeded or was cancelled after its socket was already accepted |

| Forwards | |
| :--- | :--- |
| [`IoVector`](#iovector), [`Packet`](#packet) | |

---

## Driver

```mach
pub rec Driver {
    runtime: *std.io.runtime.Runtime;
    source:  std.io.runtime.SourceToken;
    backend: impl.Backend;
    # where every table's chunks come from
    allocator: std.allocator.Allocator;
    # indexed by runtime token index, and the runtime's generations tell
    # every token apart, so a slot needs no generation floor of its own
    slots: std.memory.table.Table;
    # active slots per chunk of the slot table
    slot_live:         [table.DIRECTORY]usize;
    backend_destroyed: bool;
    lock:              std.sync.mutex.Mutex;
}
```

the driver borrows one io runtime and never creates a second native queue

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

### submit_accept

```mach
pub fun submit_accept(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    listener: *std.net.tcp.Listener,
    peer: *std.net.ip.Endpoint,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

### submit_connect

```mach
pub fun submit_connect(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    endpoint: std.net.ip.Endpoint,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

### submit_read

```mach
pub fun submit_read(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *std.net.tcp.Stream, buffer: *u8, length: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

a read cancelled through its scope completes with has_error set and the
cancel or timeout reason, and still reports in bytes and end_of_stream what it
took before the cancellation took effect. those bytes are in buffer and
belong to the stream: the peer considers them delivered and no later read
returns them, so a caller that cancels a read consumes bytes from the
cancelled completion like any other read's

### submit_readable

```mach
pub fun submit_readable(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *std.net.tcp.Stream, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

wait until the stream is readable, at orderly end of stream, or failed, without
holding a buffer

the completion has kind READABLE and zero bytes: ok with end_of_stream false
means at least one byte can be read now, ok with end_of_stream true means the
peer closed and nothing is left, and an error is the socket's failure. nothing
is read. the wait queues in order with reads on the same stream, so a read
submitted after it completes after it. a TLS layer may already hold decrypted
bytes the socket no longer shows, so check that buffer before waiting here.
the socket is closed through this driver once submitted (module header)

| Parameter | |
| :--- | :--- |
| `driver` | the driver the stream belongs to |
| `scope` | the cancellation scope the wait is registered on |
| `stream` | the stream to wait on |
| `context` | returned with the completion |
| **returns** | the wait's token, or the refusal |

### submit_write

```mach
pub fun submit_write(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *std.net.tcp.Stream, buffer: *u8, length: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

cancelling a write does not unsend it. a cancelled write completes with
has_error set and reports in bytes what it sent before the cancellation took
effect, so the stream continues after exactly those bytes
the socket is closed through this driver once submitted (module header)

### submit_write_vector

```mach
pub fun submit_write_vector(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    stream: *std.net.tcp.Stream,
    vectors: *std.system.os.IoVector,
    count: usize,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

### submit_receive_batch

```mach
pub fun submit_receive_batch(driver: *Driver, scope: *std.sync.cancel.Scope, socket: *std.net.udp.Socket, packets: *std.net.async.types.Packet, count: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

receive up to count datagrams into packets

the completion arrives as soon as at least one datagram is available and
carries every datagram already queued, up to count. it never waits for the
batch to fill, so its items are between 1 and count

| Parameter | |
| :--- | :--- |
| `driver` | the driver the socket belongs to |
| `scope` | the cancellation scope the operation is registered on |
| `socket` | the datagram socket |
| `packets` | count packets whose buffer and capacity describe the storage. the storage is borrowed until the operation completes |
| `count` | the most datagrams one completion carries |
| `context` | returned with the completion |
| **returns** | the operation's token, or the refusal  the socket is closed through this driver once submitted (module header) |

### submit_send_batch

```mach
pub fun submit_send_batch(driver: *Driver, scope: *std.sync.cancel.Scope, socket: *std.net.udp.Socket, packets: *std.net.async.types.Packet, count: usize, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

### submit_shutdown_write

```mach
pub fun submit_shutdown_write(driver: *Driver, scope: *std.sync.cancel.Scope, stream: *std.net.tcp.Stream, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the socket is closed through this driver once submitted (module header)

### submit_stream_close

```mach
pub fun submit_stream_close(
    driver: *Driver,
    scope: *std.sync.cancel.Scope,
    stream: *std.net.tcp.Stream,
    mode: std.io.lifecycle.Mode,
    context: usize,
) res[std.io.runtime.Token, std.io.error.Error]
```

close a stream the driver knows about

a tracked stream is closed here or with submit_shutdown_write, not with
tcp.stream_close, so the backend unregisters it. a graceful close shuts the
write side down, and an abortive close cancels pending reads and closes it
a direct close is detected on next use and never hands the stream's state to
the socket that reuses its value (module header)

### submit_datagram_close

```mach
pub fun submit_datagram_close(driver: *Driver, scope: *std.sync.cancel.Scope, socket: *std.net.udp.Socket, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

close a datagram socket the driver knows about

a tracked socket is closed here, not with udp.socket_close, so the backend
unregisters it. every receive still pending on it completes cancelled
a direct close is detected on next use and never hands the socket's state to
the socket that reuses its value (module header)

### submit_listener_close

```mach
pub fun submit_listener_close(driver: *Driver, scope: *std.sync.cancel.Scope, listener: *std.net.tcp.Listener, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

close a listener the driver knows about

a listener that has had an accept submitted is tracked by the driver and is
closed here, not with tcp.listener_close, so the backend unregisters it.
every accept still pending on it completes cancelled. on success the
listener's handle is invalidated, and the close completes as its own
operation

| Parameter | |
| :--- | :--- |
| `driver` | the driver the listener belongs to |
| `scope` | the cancellation scope the close is registered on |
| `listener` | the listener to close |
| `context` | returned with the close's completion |
| **returns** | the close's token, or the refusal |

### detach

```mach
pub fun detach(driver: *Driver, stream: *std.net.tcp.Stream) res[Detached, std.io.error.Error]
```

take a stream this driver accepted or connected out of it, so another driver,
on this thread or another, can adopt it

the stream must be idle: every operation submitted on it has had its
completion returned by wait. a stream with an operation in flight is refused
BUSY and nothing changes. on success the socket leaves this driver's native
queue and the detached stream carries a new opening. stream's handle is
invalidated, and the old opening is retired process-wide, so a copy of the old
handle is refused CLOSED on every driver, the adopting one and any that never
saw the socket included

| Parameter | |
| :--- | :--- |
| `driver` | the driver the stream belongs to |
| `stream` | the stream |
| **returns** | the detached stream, which owns the socket, or the refusal: CLOSED for a handle already known to be stale, BUSY while an operation is in flight, RESOURCE_EXHAUSTED when the retirement cannot be recorded, or the platform's refusal to give the socket up |

### adopt

```mach
pub fun adopt(driver: *Driver, detached: *Detached) res[std.net.tcp.Stream, std.io.error.Error]
```

register a detached stream with this driver

the stream is this driver's as though it had accepted or connected it, and is
closed through it. on success detached gives up the socket, so a second
adopt of it is refused

| Parameter | |
| :--- | :--- |
| `driver` | the driver that takes the stream |
| `detached` | the stream detach returned |
| **returns** | the stream, or the refusal, which leaves detached owning the socket |

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

one thread owns wait; submission may run concurrently
returns 0 only on timeout, a caller's io.runtime.wake, or a closed runtime

### dnit

```mach
pub fun dnit(driver: *Driver) err[std.io.error.Error]
```

tear down an idle driver: retire its runtime source, destroy its backend
and free its slot table

the runtime stays the caller's to close

| Parameter | |
| :--- | :--- |
| `driver` | the driver |
| **returns** | ok, INVALID for a nil or torn down driver, BUSY while any operation's completion has not been released, or the runtime's, backend's or allocator's refusal |

## Detached

```mach
pub rec Detached {
    stream: std.net.tcp.Stream;
}
```

an accepted or connected stream taken out of its driver by detach, owning the
socket and nothing of any driver. adopt hands it to a driver, and one never
adopted is closed with tcp.stream_close

## Functions

### listen

```mach
pub fun listen(endpoint: std.net.ip.Endpoint, backlog: i32) res[std.net.tcp.Listener, std.io.error.Error]
```

a nonblocking listener for this driver's runtime

| Parameter | |
| :--- | :--- |
| `endpoint` | endpoint to bind to |
| `backlog` | pending connections the system may queue |
| **returns** | the listener, or the refusal |

### bind_datagram

```mach
pub fun bind_datagram(endpoint: std.net.ip.Endpoint) res[std.net.udp.Socket, std.io.error.Error]
```

a nonblocking datagram socket bound to an endpoint

| Parameter | |
| :--- | :--- |
| `endpoint` | endpoint to bind to |
| **returns** | the socket, or the refusal |

### listen_with

```mach
pub fun listen_with(endpoint: std.net.ip.Endpoint, options: std.net.tcp.ListenOptions) res[std.net.tcp.Listener, std.io.error.Error]
```

a nonblocking listener with explicit options, for this driver's runtime

| Parameter | |
| :--- | :--- |
| `endpoint` | endpoint to bind to |
| `options` | bind options (reuse_port for one listener per thread where std.system.capability.REUSE_PORT_BALANCES holds) and backlog |
| **returns** | the listener, or the refusal |

### bind_datagram_with

```mach
pub fun bind_datagram_with(endpoint: std.net.ip.Endpoint, options: std.net.socket.BindOptions) res[std.net.udp.Socket, std.io.error.Error]
```

a nonblocking datagram socket bound with explicit options

| Parameter | |
| :--- | :--- |
| `endpoint` | endpoint to bind to |
| `options` | options applied between creation and bind |
| **returns** | the socket, or the refusal |

### create_datagram

```mach
pub fun create_datagram(family: i32) res[std.net.udp.Socket, std.io.error.Error]
```

an unbound nonblocking datagram socket

| Parameter | |
| :--- | :--- |
| `family` | os.AF_INET or os.AF_INET6 |
| **returns** | the socket, or the refusal |

### stream

```mach
pub fun stream(completion: *std.io.runtime.Completion) std.net.tcp.Stream
```

the stream an accept or connect completion hands over

the handle keeps the opening the driver recorded for the socket, so the
driver knows the stream as the socket it accepted or connected

| Parameter | |
| :--- | :--- |
| `completion` | a successful ACCEPT or CONNECT completion from this driver |
| **returns** | the stream, which the caller now owns and closes through the driver |

### accepted

```mach
pub fun accepted(completion: *std.io.runtime.Completion) opt[std.net.tcp.Stream]
```

the stream an accept completion hands over, whether it succeeded or was
cancelled after its socket was already accepted

a cancelled accept can have taken a connection first, and its completion is
then the only thing that holds it, so a caller that cancels accepts takes the
stream from every accept completion it receives and serves or closes it

| Parameter | |
| :--- | :--- |
| `completion` | an ACCEPT completion from this driver |
| **returns** | the stream, which the caller now owns and closes through the driver, or none when the completion hands nothing over |

## Forwards

### IoVector

Forwards [`std.system.os.IoVector`](../system/os.md#iovector), only where `capability.HAS_CLOCK && capability.HAS_SOCKETS`.

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

one buffer of a gather write, laid out as struct iovec on linux and darwin
and as wasi's ciovec

### Packet

Forwards [`std.net.async.types.Packet`](async/types.md#packet), only where `capability.HAS_CLOCK && capability.HAS_SOCKETS`.

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

