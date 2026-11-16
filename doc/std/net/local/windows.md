[std](../../README.md) / [net](../README.md) / [local](README.md) / **windows**

# std.net.local.windows

windows af_unix local byte streams

Source: [`src/net/local/windows.mach`](../../../../src/net/local/windows.mach)

Uses types from [`std.net.local.endpoint`](endpoint.md), [`std.net.local.types`](types.md).

| Functions | |
| :--- | :--- |
| [`cleanup_listener`](#cleanup_listener), [`create_stream`](#create_stream), [`connect_start`](#connect_start), [`bind`](#bind), [`start_listener`](#start_listener), [`listen`](#listen), [`connect`](#connect), [`accept`](#accept), [`read`](#read), [`write`](#write), [`shutdown_write`](#shutdown_write), [`peer_identity`](#peer_identity), [`rename`](#rename), [`close_stream`](#close_stream), [`close_listener`](#close_listener) | |

---

## Functions

### cleanup_listener

```mach
pub fun cleanup_listener(listener: *std.net.local.types.Listener) i64
```

### create_stream

```mach
pub fun create_stream(value: std.net.local.endpoint.Endpoint, asynchronous: bool, handle: *usize) i64
```

### connect_start

```mach
pub fun connect_start(handle: usize, value: std.net.local.endpoint.Endpoint) i64
```

### bind

```mach
pub fun bind(listener: *std.net.local.types.Listener, value: std.net.local.endpoint.Endpoint, options: std.net.local.types.BindOptions) i64
```

### start_listener

```mach
pub fun start_listener(listener: *std.net.local.types.Listener, backlog: i32) i64
```

### listen

```mach
pub fun listen(listener: *std.net.local.types.Listener, value: std.net.local.endpoint.Endpoint, options: std.net.local.types.ListenOptions) i64
```

### connect

```mach
pub fun connect(stream: *std.net.local.types.Stream, value: std.net.local.endpoint.Endpoint, asynchronous: bool) i64
```

### accept

```mach
pub fun accept(listener: *std.net.local.types.Listener, stream: *std.net.local.types.Stream, asynchronous: bool) i64
```

### read

```mach
pub fun read(handle: usize, buffer: *u8, length: usize) i64
```

### write

```mach
pub fun write(handle: usize, buffer: *u8, length: usize) i64
```

### shutdown_write

```mach
pub fun shutdown_write(handle: usize) i64
```

### peer_identity

```mach
pub fun peer_identity(handle: usize, server_side: bool, identity: *std.net.local.types.PeerIdentity) i64
```

### rename

```mach
pub fun rename(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) i64
```

### close_stream

```mach
pub fun close_stream(handle: usize, server_side: bool) i64
```

### close_listener

```mach
pub fun close_listener(listener: *std.net.local.types.Listener) i64
```

