[std](../../README.md) / [net](../README.md) / [local](README.md) / **windows**

# std.net.local.windows

windows af_unix local byte streams

Source: [`src/net/local/windows.mach`](../../../../src/net/local/windows.mach)

Uses types from [`std.net.local.endpoint`](endpoint.md), [`std.net.local.types`](types.md).

| Functions | |
| :--- | :--- |
| [`cleanup_listener`](#cleanup_listener) | remove a listener's socket file when the path still names it, whatever its ownership |
| [`create_stream`](#create_stream) | create an unbound local stream socket |
| [`connect_start`](#connect_start) | connect a socket to an endpoint |
| [`bind`](#bind) | create a nonblocking socket and bind a listener to an endpoint |
| [`start_listener`](#start_listener) | start listening on a bound listener |
| [`listen`](#listen) | bind a listener and start listening, closing it when listening fails |
| [`connect`](#connect) | create a socket and connect it to an endpoint as a client stream |
| [`accept`](#accept) | accept one connection as a server-side stream |
| [`read`](#read) | receive bytes on a stream |
| [`write`](#write) | send bytes on a stream |
| [`shutdown_write`](#shutdown_write) | shut down a stream's sending side |
| [`peer_identity`](#peer_identity) | peer credentials, which windows local sockets do not report |
| [`rename`](#rename) | move a listener's socket file to another path, with no occupancy or identity check |
| [`close_stream`](#close_stream) | close a stream's socket |
| [`close_listener`](#close_listener) | close a listener's socket, then remove its socket file when it is owned |

---

## Functions

### cleanup_listener

```mach
pub fun cleanup_listener(listener: *std.net.local.types.Listener) i64
```

remove a listener's socket file when the path still names it, whatever its ownership

| Parameter | |
| :--- | :--- |
| `listener` | the listener whose file to remove |
| **returns** | 0 when removed or already gone, a negative native code otherwise, EBUSY when the path names another file or its identity cannot be read |

### create_stream

```mach
pub fun create_stream(value: std.net.local.endpoint.Endpoint, asynchronous: bool, handle: *usize) i64
```

create an unbound local stream socket

| Parameter | |
| :--- | :--- |
| `value` | the endpoint the socket is for, unused |
| `asynchronous` | make it nonblocking |
| `handle` | receives the native socket, which the caller closes |
| **returns** | 0, or a negative native code |

### connect_start

```mach
pub fun connect_start(handle: usize, value: std.net.local.endpoint.Endpoint) i64
```

connect a socket to an endpoint

| Parameter | |
| :--- | :--- |
| `handle` | the native socket |
| `value` | the endpoint to connect to |
| **returns** | 0, or a negative native code, ENOTSUP for a kind with no sockaddr form and EINVAL for an endpoint that does not encode |

### bind

```mach
pub fun bind(listener: *std.net.local.types.Listener, value: std.net.local.endpoint.Endpoint, options: std.net.local.types.BindOptions) i64
```

create a nonblocking socket and bind a listener to an endpoint

a failure after the socket is created closes it, removes a socket file the
bind made and sets listener.handle to all ones. an earlier failure leaves
listener.handle untouched

| Parameter | |
| :--- | :--- |
| `listener` | the listener to bind, its endpoint and ownership already set |
| `value` | the endpoint to bind |
| `options` | stale policy and permissions |
| **returns** | 0, or a negative native code, ENOTSUP for a stale policy or permissions other than REJECT_STALE and INHERIT_PERMISSIONS |

### start_listener

```mach
pub fun start_listener(listener: *std.net.local.types.Listener, backlog: i32) i64
```

start listening on a bound listener

| Parameter | |
| :--- | :--- |
| `listener` | the bound listener |
| `backlog` | pending connections the system may queue |
| **returns** | 0, or a negative native code |

### listen

```mach
pub fun listen(listener: *std.net.local.types.Listener, value: std.net.local.endpoint.Endpoint, options: std.net.local.types.ListenOptions) i64
```

bind a listener and start listening, closing it when listening fails

| Parameter | |
| :--- | :--- |
| `listener` | the listener to bind, its endpoint and ownership already set |
| `value` | the endpoint to bind |
| `options` | backlog, stale policy and permissions |
| **returns** | 0, or a negative native code |

### connect

```mach
pub fun connect(stream: *std.net.local.types.Stream, value: std.net.local.endpoint.Endpoint, asynchronous: bool) i64
```

create a socket and connect it to an endpoint as a client stream

| Parameter | |
| :--- | :--- |
| `stream` | receives the connected stream, which the caller closes |
| `value` | the endpoint to connect to |
| `asynchronous` | make the socket nonblocking |
| **returns** | 0, or a negative native code |

### accept

```mach
pub fun accept(listener: *std.net.local.types.Listener, stream: *std.net.local.types.Stream, asynchronous: bool) i64
```

accept one connection as a server-side stream

| Parameter | |
| :--- | :--- |
| `listener` | the listening listener |
| `stream` | receives the accepted stream, which the caller closes |
| `asynchronous` | make the accepted socket nonblocking |
| **returns** | 0, or a negative native code |

### read

```mach
pub fun read(handle: usize, buffer: *u8, length: usize) i64
```

receive bytes on a stream

| Parameter | |
| :--- | :--- |
| `handle` | the native socket |
| `buffer` | storage for the bytes |
| `length` | bytes of storage |
| **returns** | bytes received, 0 at the end of the stream, or a negative native code |

### write

```mach
pub fun write(handle: usize, buffer: *u8, length: usize) i64
```

send bytes on a stream

| Parameter | |
| :--- | :--- |
| `handle` | the native socket |
| `buffer` | the bytes to send |
| `length` | bytes to send |
| **returns** | bytes sent, or a negative native code |

### shutdown_write

```mach
pub fun shutdown_write(handle: usize) i64
```

shut down a stream's sending side

| Parameter | |
| :--- | :--- |
| `handle` | the native socket |
| **returns** | 0, or a negative native code |

### peer_identity

```mach
pub fun peer_identity(handle: usize, server_side: bool, identity: *std.net.local.types.PeerIdentity) i64
```

peer credentials, which windows local sockets do not report

| Parameter | |
| :--- | :--- |
| `handle` | the native socket, unused |
| `server_side` | unused |
| `identity` | left untouched |
| **returns** | ENOTSUP |

### rename

```mach
pub fun rename(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) i64
```

move a listener's socket file to another path, with no occupancy or identity check

| Parameter | |
| :--- | :--- |
| `listener` | the listener whose file to move |
| `replacement` | the new filesystem endpoint |
| **returns** | 0, or a negative native code |

### close_stream

```mach
pub fun close_stream(handle: usize, server_side: bool) i64
```

close a stream's socket

| Parameter | |
| :--- | :--- |
| `handle` | the native socket |
| `server_side` | whether the stream was accepted, unused |
| **returns** | 0, or a negative native code |

### close_listener

```mach
pub fun close_listener(listener: *std.net.local.types.Listener) i64
```

close a listener's socket, then remove its socket file when it is owned

| Parameter | |
| :--- | :--- |
| `listener` | the listener to close |
| **returns** | 0, the close's negative native code, or else the removal's |

