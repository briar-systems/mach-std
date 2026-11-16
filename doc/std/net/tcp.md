[std](../README.md) / [net](README.md) / **tcp**

# std.net.tcp

TCP socket operations

Source: [`src/net/tcp.mach`](../../../src/net/tcp.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.io.handle`](../io/handle.md), [`std.net.ip`](ip.md), [`std.net.socket`](socket.md).

| Type | | |
| :--- | :--- | :--- |
| [`Listener`](#listener) | `rec` | a bound TCP socket listening for connections |
| [`Stream`](#stream) | `rec` | a connected TCP socket for reading and writing |
| [`ListenOptions`](#listenoptions) | `rec` | how a listener is set up before it listens |

| On `Listener` | |
| :--- | :--- |
| [`listen`](#listen) | create a TCP listener bound to an endpoint |
| [`listen_with_flags`](#listen_with_flags) | |
| [`accept`](#accept) | accept a new connection on a listener |
| [`accept_with_flags`](#accept_with_flags) | |
| [`accept_ep`](#accept_ep) | accept a new connection and populate the remote endpoint |
| [`accept_ep_with_flags`](#accept_ep_with_flags), [`listener_local_endpoint`](#listener_local_endpoint) | |
| [`listener_close`](#listener_close) | close a TCP listener |

| On `Stream` | |
| :--- | :--- |
| [`connect`](#connect) | establish a TCP connection to a remote endpoint |
| [`connect_with_flags`](#connect_with_flags), [`stream_local_endpoint`](#stream_local_endpoint), [`stream_remote_endpoint`](#stream_remote_endpoint) | |
| [`stream_read`](#stream_read) | read bytes from a TCP stream |
| [`stream_set_read_timeout`](#stream_set_read_timeout) | bound blocking reads on a TCP stream to a timeout |
| [`stream_write`](#stream_write) | write bytes to a TCP stream |
| [`stream_shutdown`](#stream_shutdown) | shut down part or all of a TCP stream |
| [`stream_close`](#stream_close) | close a TCP stream |

| On `ListenOptions` | |
| :--- | :--- |
| [`listen_options`](#listen_options) | the options listen uses: SO_REUSEADDR, no SO_REUSEPORT |
| [`listen_with`](#listen_with) | create a blocking TCP listener with explicit options |
| [`listen_with_options`](#listen_with_options) | create a TCP listener with explicit options and creation flags |

---

## Listener

```mach
pub rec Listener {
    handle: std.io.handle.SocketHandle;
}
```

a bound TCP socket listening for connections

| Field | Type | |
| :--- | :--- | :--- |
| `handle` | `std.io.handle.SocketHandle` | the native-width socket handle |

### listen

```mach
pub fun listen(ep: std.net.ip.Endpoint, backlog: i32) res[Listener, std.io.error.Error]
```

create a TCP listener bound to an endpoint

creates a socket, sets SO_REUSEADDR, binds to the address and port,
and begins listening with the given backlog.

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `backlog` | maximum pending connection queue length |
| **returns** | the Listener, or an error message |

### listen_with_flags

```mach
pub fun listen_with_flags(ep: std.net.ip.Endpoint, backlog: i32, flags: std.net.socket.Flags) res[Listener, std.io.error.Error]
```

### accept

```mach
pub fun accept(ln: *Listener) res[Stream, std.io.error.Error]
```

accept a new connection on a listener

| Parameter | |
| :--- | :--- |
| `ln` | the listener to accept on |
| **returns** | a connected Stream, or an error message |

### accept_with_flags

```mach
pub fun accept_with_flags(ln: *Listener, flags: std.net.socket.Flags) res[Stream, std.io.error.Error]
```

### accept_ep

```mach
pub fun accept_ep(ln: *Listener, ep: *std.net.ip.Endpoint) res[Stream, std.io.error.Error]
```

accept a new connection and populate the remote endpoint

| Parameter | |
| :--- | :--- |
| `ln` | the listener to accept on |
| `ep` | pointer to an Endpoint to fill with the remote address |
| **returns** | a connected Stream, or an error message |

### accept_ep_with_flags

```mach
pub fun accept_ep_with_flags(ln: *Listener, ep: *std.net.ip.Endpoint, flags: std.net.socket.Flags) res[Stream, std.io.error.Error]
```

### listener_local_endpoint

```mach
pub fun listener_local_endpoint(ln: *Listener) res[std.net.ip.Endpoint, std.io.error.Error]
```

### listener_close

```mach
pub fun listener_close(ln: *Listener) err[std.io.error.Error]
```

close a TCP listener

| Parameter | |
| :--- | :--- |
| `ln` | the listener to close |

## Stream

```mach
pub rec Stream {
    handle: std.io.handle.SocketHandle;
}
```

a connected TCP socket for reading and writing

| Field | Type | |
| :--- | :--- | :--- |
| `handle` | `std.io.handle.SocketHandle` | the native-width socket handle |

### connect

```mach
pub fun connect(ep: std.net.ip.Endpoint) res[Stream, std.io.error.Error]
```

establish a TCP connection to a remote endpoint

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to connect to |
| **returns** | a connected Stream, or an error message |

### connect_with_flags

```mach
pub fun connect_with_flags(ep: std.net.ip.Endpoint, flags: std.net.socket.Flags) res[Stream, std.io.error.Error]
```

### stream_local_endpoint

```mach
pub fun stream_local_endpoint(stream: *Stream) res[std.net.ip.Endpoint, std.io.error.Error]
```

### stream_remote_endpoint

```mach
pub fun stream_remote_endpoint(stream: *Stream) res[std.net.ip.Endpoint, std.io.error.Error]
```

### stream_read

```mach
pub fun stream_read(s: *Stream, buf: *u8, len: usize) res[usize, std.io.error.Error]
```

read bytes from a TCP stream

| Parameter | |
| :--- | :--- |
| `s` | the stream to read from |
| `buf` | destination buffer |
| `len` | maximum bytes to read |
| **returns** | bytes read, 0 on peer close, or a normalized I/O error |

### stream_set_read_timeout

```mach
pub fun stream_set_read_timeout(s: *Stream, ms: u64) err[std.io.error.Error]
```

bound blocking reads on a TCP stream to a timeout

sets SO_RCVTIMEO on the stream. after ms elapses with no data pending, a
stream_read returns a normalized timeout or would-block error after the
interval, distinct from a peer close. ms == 0 restores indefinite blocking.

| Parameter | |
| :--- | :--- |
| `s` | the stream to bound reads on |
| `ms` | timeout in milliseconds, or 0 for no timeout |
| **returns** | ok on success, or an error message |

### stream_write

```mach
pub fun stream_write(s: *Stream, buf: *u8, len: usize) res[usize, std.io.error.Error]
```

write bytes to a TCP stream

| Parameter | |
| :--- | :--- |
| `s` | the stream to write to |
| `buf` | source buffer |
| `len` | number of bytes to write |
| **returns** | number of bytes written, or negative on error |

### stream_shutdown

```mach
pub fun stream_shutdown(s: *Stream, how: i32) err[std.io.error.Error]
```

shut down part or all of a TCP stream

| Parameter | |
| :--- | :--- |
| `s` | the stream to shut down |
| `how` | SHUT_RD (0), SHUT_WR (1), or SHUT_RDWR (2) |

### stream_close

```mach
pub fun stream_close(s: *Stream) err[std.io.error.Error]
```

close a TCP stream

| Parameter | |
| :--- | :--- |
| `s` | the stream to close |

## ListenOptions

```mach
pub rec ListenOptions {
    bind:    std.net.socket.BindOptions;
    backlog: i32;
}
```

how a listener is set up before it listens

| Field | Type | |
| :--- | :--- | :--- |
| `bind` | `std.net.socket.BindOptions` | options applied between creation and bind |
| `backlog` | `i32` | maximum pending connection queue length |

### listen_options

```mach
pub fun listen_options(backlog: i32) ListenOptions
```

the options listen uses: SO_REUSEADDR, no SO_REUSEPORT

| Parameter | |
| :--- | :--- |
| `backlog` | maximum pending connection queue length |
| **returns** | the options |

### listen_with

```mach
pub fun listen_with(ep: std.net.ip.Endpoint, options: ListenOptions) res[Listener, std.io.error.Error]
```

create a blocking TCP listener with explicit options

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `options` | bind options and backlog |
| **returns** | the Listener, or the refusal. reuse_port where the target has no SO_REUSEPORT is UNSUPPORTED, and no socket is created |

### listen_with_options

```mach
pub fun listen_with_options(ep: std.net.ip.Endpoint, options: ListenOptions, flags: std.net.socket.Flags) res[Listener, std.io.error.Error]
```

create a TCP listener with explicit options and creation flags

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `options` | bind options and backlog |
| `flags` | socket creation flags |
| **returns** | the Listener, or the refusal |

