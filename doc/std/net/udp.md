[std](../README.md) / [net](README.md) / **udp**

# std.net.udp

UDP socket operations

Source: [`src/net/udp.mach`](../../../src/net/udp.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.io.handle`](../io/handle.md), [`std.net.ip`](ip.md), [`std.net.socket`](socket.md).

| Type | | |
| :--- | :--- | :--- |
| [`Socket`](#socket) | `rec` | a bound or unbound UDP socket |

| On `Socket` | |
| :--- | :--- |
| [`create`](#create) | create an unbound blocking IPv4 UDP socket |
| [`create_v6`](#create_v6) | create an unbound blocking IPv6 UDP socket |
| [`create_with_flags`](#create_with_flags) | create an unbound UDP socket with explicit creation flags |
| [`bind`](#bind) | create a UDP socket bound to an endpoint |
| [`bind_with_flags`](#bind_with_flags) | create a UDP socket bound to an endpoint with explicit creation flags |
| [`bind_with`](#bind_with) | create a blocking UDP socket bound with explicit options |
| [`bind_with_options`](#bind_with_options) | create a UDP socket bound with explicit options and creation flags |
| [`local_endpoint`](#local_endpoint) | the local endpoint the socket is bound to |
| [`remote_endpoint`](#remote_endpoint) | the remote endpoint the socket is connected to |
| [`send_to`](#send_to) | send a datagram to a remote endpoint |
| [`recv_from`](#recv_from) | receive a datagram and populate the source endpoint |
| [`socket_set_recv_timeout`](#socket_set_recv_timeout) | bound blocking receives on a UDP socket to a timeout |
| [`socket_close`](#socket_close) | close a UDP socket |

---

## Socket

```mach
pub rec Socket {
    handle: std.io.handle.SocketHandle;
    family: i32;
}
```

a bound or unbound UDP socket

| Field | Type | |
| :--- | :--- | :--- |
| `handle` | `std.io.handle.SocketHandle` | the native-width socket handle |
| `family` | `i32` | the address family it was created for, AF_INET or AF_INET6 |

### create

```mach
pub fun create() res[Socket, std.io.error.Error]
```

create an unbound blocking IPv4 UDP socket

| Parameter | |
| :--- | :--- |
| **returns** | the Socket, which the caller closes with socket_close, or the failure |

### create_v6

```mach
pub fun create_v6() res[Socket, std.io.error.Error]
```

create an unbound blocking IPv6 UDP socket

| Parameter | |
| :--- | :--- |
| **returns** | the Socket, which the caller closes with socket_close, or the failure |

### create_with_flags

```mach
pub fun create_with_flags(family: i32, flags: std.net.socket.Flags) res[Socket, std.io.error.Error]
```

create an unbound UDP socket with explicit creation flags

| Parameter | |
| :--- | :--- |
| `family` | the address family, AF_INET or AF_INET6 |
| `flags` | socket creation flags |
| **returns** | the Socket, which the caller closes with socket_close, or the failure |

### bind

```mach
pub fun bind(ep: std.net.ip.Endpoint) res[Socket, std.io.error.Error]
```

create a UDP socket bound to an endpoint

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| **returns** | the bound Socket, or the failure |

### bind_with_flags

```mach
pub fun bind_with_flags(ep: std.net.ip.Endpoint, flags: std.net.socket.Flags) res[Socket, std.io.error.Error]
```

create a UDP socket bound to an endpoint with explicit creation flags

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `flags` | socket creation flags |
| **returns** | the bound Socket, or the failure |

### bind_with

```mach
pub fun bind_with(ep: std.net.ip.Endpoint, options: std.net.socket.BindOptions) res[Socket, std.io.error.Error]
```

create a blocking UDP socket bound with explicit options

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `options` | options applied between creation and bind |
| **returns** | the bound Socket, or the refusal. reuse_port where the target has no SO_REUSEPORT is UNSUPPORTED, and no socket is created |

### bind_with_options

```mach
pub fun bind_with_options(ep: std.net.ip.Endpoint, options: std.net.socket.BindOptions, flags: std.net.socket.Flags) res[Socket, std.io.error.Error]
```

create a UDP socket bound with explicit options and creation flags

| Parameter | |
| :--- | :--- |
| `ep` | endpoint to bind to |
| `options` | options applied between creation and bind |
| `flags` | socket creation flags |
| **returns** | the bound Socket, or the refusal |

### local_endpoint

```mach
pub fun local_endpoint(s: *Socket) res[std.net.ip.Endpoint, std.io.error.Error]
```

the local endpoint the socket is bound to

| Parameter | |
| :--- | :--- |
| `s` | the socket |
| **returns** | the endpoint, or the failure. UNSUPPORTED when the address family is not IP |

### remote_endpoint

```mach
pub fun remote_endpoint(s: *Socket) res[std.net.ip.Endpoint, std.io.error.Error]
```

the remote endpoint the socket is connected to

| Parameter | |
| :--- | :--- |
| `s` | the socket |
| **returns** | the endpoint, or the failure. UNSUPPORTED when the address family is not IP |

### send_to

```mach
pub fun send_to(s: *Socket, buf: *u8, len: usize, ep: std.net.ip.Endpoint) res[usize, std.io.error.Error]
```

send a datagram to a remote endpoint

| Parameter | |
| :--- | :--- |
| `s` | the socket to send from |
| `buf` | source buffer |
| `len` | number of bytes to send |
| `ep` | destination endpoint |
| **returns** | number of bytes sent, or the failure. INVALID when ep's family is not the socket's |

### recv_from

```mach
pub fun recv_from(s: *Socket, buf: *u8, len: usize, ep: *std.net.ip.Endpoint) res[usize, std.io.error.Error]
```

receive a datagram and populate the source endpoint

| Parameter | |
| :--- | :--- |
| `s` | the socket to receive on |
| `buf` | destination buffer |
| `len` | maximum bytes to receive |
| `ep` | pointer to an Endpoint to fill with the source address, or nil |
| **returns** | number of bytes received, or the failure. UNSUPPORTED when the source address cannot be read as an IP endpoint |

### socket_set_recv_timeout

```mach
pub fun socket_set_recv_timeout(s: *Socket, ms: u64) err[std.io.error.Error]
```

bound blocking receives on a UDP socket to a timeout

sets SO_RCVTIMEO on the socket. after ms elapses with no datagram pending, a
recv_from returns a normalized timeout or would-block error. ms == 0
restores indefinite blocking.

| Parameter | |
| :--- | :--- |
| `s` | the socket to bound receives on |
| `ms` | timeout in milliseconds, or 0 for no timeout |
| **returns** | ok on success, or the failure |

### socket_close

```mach
pub fun socket_close(s: *Socket) err[std.io.error.Error]
```

close a UDP socket

| Parameter | |
| :--- | :--- |
| `s` | the socket to close, whose handle is invalid afterwards |
| **returns** | ok, or the failure. CLOSED when the socket was already closed |

