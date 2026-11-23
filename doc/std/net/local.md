[std](../README.md) / [net](README.md) / **local**

# std.net.local

portable local byte-stream descriptors and endpoint ownership

a stream has one closing owner. its receive queue is borrowed exclusively for
each read, across every raw or duplicated alias: a concurrent receive, receive
shutdown or close through another alias is invalid. peer writes and
operations on unrelated descriptors may run concurrently.

reads deliver bytes only. a peer may attach descriptor rights to those bytes,
and the stream never hands them to the caller or lets them occupy its
descriptor table:

- linux receives with MSG_CMSG_CLOEXEC into control storage sized for the
  kernel's bound (SCM_MAX_FD plus the SO_PASSCRED and SO_PASSPIDFD records)
  and closes every SCM_RIGHTS and SCM_PIDFD descriptor it reports. the storage
  is zero-filled first, so a native failure after rights were installed is
  still walked. MSG_CTRUNC means the kernel dropped records it could not
  report, and it installs none it does not report, so the walk is complete.
  std.system.os.linux.sock_recv_close_rights is that primitive with caller
  storage, and local_stream_recv supplies the bound.
- darwin inspects without consuming (MSG_PEEK with one control header),
  refuses any ancillary data or truncation as UNSUPPORTED, and otherwise
  consumes at most the inspected byte count. a zero-length read does not
  inspect. a refusal leaves the socket open with its queued rights still owned
  by it, and closing the stream releases them. native failures keep their
  cause, and buffer contents on failure are unspecified.
- windows local sockets carry no rights, so reads are plain.

raw os sock_recv and sock_receive_message keep native ancillary behaviour and
do not give this byte-only contract.

a filesystem endpoint is named by the bytes of its path. filesystem takes the
path as UTF-8 and filesystem_native in std.runtime.native units: bytes on
linux and darwin, passed through unchanged, and UTF-16 on windows, converted
once to UTF-8. windows sun_path is a byte string too, so the kernel cannot
name a socket at a path holding an unpaired surrogate, which has no UTF-8
spelling. filesystem_native refuses such a path with INVALID before any
socket call.

Source: [`src/net/local.mach`](../../../src/net/local.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.io.lifecycle`](../io/lifecycle.md), [`std.net.local.endpoint`](local/endpoint.md), [`std.net.local.types`](local/types.md).

| Functions | |
| :--- | :--- |
| [`capabilities`](#capabilities) | the local transport capabilities of the build target |
| [`filesystem`](#filesystem) | a filesystem endpoint named by a nul-terminated UTF-8 path |
| [`filesystem_bytes`](#filesystem_bytes) | a filesystem endpoint named by length bytes of a path |
| [`filesystem_native`](#filesystem_native) | a filesystem endpoint from a path in native units (see endpoint.filesystem_native) |
| [`abstract`](#abstract) | a linux abstract endpoint named by length bytes |
| [`target`](#target) | a target-name endpoint named by a nul-terminated name |
| [`target_bytes`](#target_bytes) | a target-name endpoint named by length bytes |
| [`default_listen_options`](#default_listen_options) | listen options with a backlog of 128, an owned socket file, stale files rejected and inherited permissions |
| [`default_bind_options`](#default_bind_options) | bind options with an owned socket file, stale files rejected and inherited permissions |
| [`bind`](#bind) | filesystem ownership is race-free when the caller controls mutations in the parent directory |
| [`listener_start`](#listener_start) | start accepting connections on a bound listener |
| [`listen`](#listen) | bind an endpoint and start listening on it |
| [`connect`](#connect) | connect a blocking stream to a listening endpoint |
| [`accept`](#accept) | wait for and accept one connection as a blocking stream |
| [`stream_read`](#stream_read) | exclusively borrow the stream receive queue and close state, including raw aliases |
| [`stream_write`](#stream_write) | write bytes to a stream |
| [`stream_shutdown_write`](#stream_shutdown_write) | shut down the sending side, so the peer reads the end of the stream |
| [`peer_identity`](#peer_identity) | the credentials of a stream's peer, as far as the target reports them |
| [`listener_rename`](#listener_rename) | rename never knowingly replaces an occupied path callers must serialize parent directory mutation where atomic no-replace rename is unavailable |
| [`stream_close`](#stream_close) | close a stream, shutting down its sending side first when graceful |
| [`listener_close`](#listener_close) | close a listener, and when it is owned remove its socket file if the path still names it |

| Forwards | |
| :--- | :--- |
| [`Kind`](#kind), [`Endpoint`](#endpoint), [`Capabilities`](#capabilities-1), [`FILESYSTEM`](#filesystem-1), [`ABSTRACT`](#abstract-1), [`TARGET`](#target-1), [`Ownership`](#ownership), [`BORROWED`](#borrowed), [`OWNED`](#owned), [`StalePolicy`](#stalepolicy), [`REJECT_STALE`](#reject_stale), [`REMOVE_STALE_SOCKET`](#remove_stale_socket), [`INHERIT_PERMISSIONS`](#inherit_permissions), [`BindOptions`](#bindoptions), [`ListenOptions`](#listenoptions), [`Listener`](#listener), [`Stream`](#stream), [`PeerIdentity`](#peeridentity) | |

---

## Functions

### capabilities

```mach
pub fun capabilities() std.net.local.endpoint.Capabilities
```

the local transport capabilities of the build target

| Parameter | |
| :--- | :--- |
| **returns** | the capability set (see endpoint.capabilities) |

### filesystem

```mach
pub fun filesystem(path: str) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a filesystem endpoint named by a nul-terminated UTF-8 path

| Parameter | |
| :--- | :--- |
| `path` | the path, copied |
| **returns** | the endpoint, or the refusal (see endpoint.filesystem_bytes) |

### filesystem_bytes

```mach
pub fun filesystem_bytes(data: *u8, length: usize) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a filesystem endpoint named by length bytes of a path

| Parameter | |
| :--- | :--- |
| `data` | the path bytes, copied |
| `length` | path bytes |
| **returns** | the endpoint, or the refusal (see endpoint.filesystem_bytes) |

### filesystem_native

```mach
pub fun filesystem_native(name: *Unit) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a filesystem endpoint from a path in native units (see endpoint.filesystem_native)

### abstract

```mach
pub fun abstract(data: *u8, length: usize) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a linux abstract endpoint named by length bytes

| Parameter | |
| :--- | :--- |
| `data` | the name bytes, copied |
| `length` | name bytes |
| **returns** | the endpoint, or the refusal (see endpoint.abstract) |

### target

```mach
pub fun target(name: str) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a target-name endpoint named by a nul-terminated name

| Parameter | |
| :--- | :--- |
| `name` | the name, copied |
| **returns** | the endpoint, or the refusal (see endpoint.target_bytes) |

### target_bytes

```mach
pub fun target_bytes(data: *u8, length: usize) res[std.net.local.endpoint.Endpoint, std.io.error.Error]
```

a target-name endpoint named by length bytes

| Parameter | |
| :--- | :--- |
| `data` | the name bytes, copied |
| `length` | name bytes |
| **returns** | the endpoint, or the refusal (see endpoint.target_bytes) |

### default_listen_options

```mach
pub fun default_listen_options() std.net.local.types.ListenOptions
```

listen options with a backlog of 128, an owned socket file, stale files
rejected and inherited permissions

| Parameter | |
| :--- | :--- |
| **returns** | the options |

### default_bind_options

```mach
pub fun default_bind_options() std.net.local.types.BindOptions
```

bind options with an owned socket file, stale files rejected and inherited
permissions

| Parameter | |
| :--- | :--- |
| **returns** | the options |

### bind

```mach
pub fun bind(bound: std.net.local.endpoint.Endpoint, options: std.net.local.types.BindOptions) res[std.net.local.types.Listener, std.io.error.Error]
```

filesystem ownership is race-free when the caller controls mutations in the parent directory

| Parameter | |
| :--- | :--- |
| `bound` | the endpoint to bind |
| `options` | ownership, stale policy and permissions |
| **returns** | the bound listener, not yet listening, which the caller closes with listener_close, INVALID for an unsupported endpoint or bad options, or the bind failure |

### listener_start

```mach
pub fun listener_start(listener: *std.net.local.types.Listener, backlog: i32) err[std.io.error.Error]
```

start accepting connections on a bound listener

| Parameter | |
| :--- | :--- |
| `listener` | the bound listener |
| `backlog` | pending connections the system may queue, above zero |
| **returns** | ok, INVALID for a nil or closed listener or a backlog of zero or less, or the listen failure |

### listen

```mach
pub fun listen(bound: std.net.local.endpoint.Endpoint, options: std.net.local.types.ListenOptions) res[std.net.local.types.Listener, std.io.error.Error]
```

bind an endpoint and start listening on it

when listening fails the listener is closed as owned, removing a socket file
it created

| Parameter | |
| :--- | :--- |
| `bound` | the endpoint to bind |
| `options` | backlog, ownership, stale policy and permissions |
| **returns** | the listening listener, which the caller closes with listener_close, INVALID for a backlog of zero or less, or the bind or listen failure |

### connect

```mach
pub fun connect(remote: std.net.local.endpoint.Endpoint) res[std.net.local.types.Stream, std.io.error.Error]
```

connect a blocking stream to a listening endpoint

| Parameter | |
| :--- | :--- |
| `remote` | the endpoint to connect to |
| **returns** | the stream, which the caller closes with stream_close, INVALID for an unsupported endpoint, or the connect failure |

### accept

```mach
pub fun accept(listener: *std.net.local.types.Listener) res[std.net.local.types.Stream, std.io.error.Error]
```

wait for and accept one connection as a blocking stream

| Parameter | |
| :--- | :--- |
| `listener` | the listening listener |
| **returns** | the server-side stream, which the caller closes with stream_close, INVALID for a nil or closed listener, or the accept failure |

### stream_read

```mach
pub fun stream_read(stream: *std.net.local.types.Stream, buffer: *u8, length: usize) res[usize, std.io.error.Error]
```

exclusively borrow the stream receive queue and close state, including raw aliases.
darwin rejects ancillary input without consuming it and leaves the stream owned.

### stream_write

```mach
pub fun stream_write(stream: *std.net.local.types.Stream, buffer: *u8, length: usize) res[usize, std.io.error.Error]
```

write bytes to a stream

| Parameter | |
| :--- | :--- |
| `stream` | the open stream |
| `buffer` | the bytes to send, nil only for a zero length |
| `length` | bytes to send |
| **returns** | bytes written, which may be fewer than length, INVALID for a nil or closed stream or nil buffer, or the write failure |

### stream_shutdown_write

```mach
pub fun stream_shutdown_write(stream: *std.net.local.types.Stream) err[std.io.error.Error]
```

shut down the sending side, so the peer reads the end of the stream

| Parameter | |
| :--- | :--- |
| `stream` | the open stream |
| **returns** | ok, INVALID for a nil or closed stream, or the shutdown failure |

### peer_identity

```mach
pub fun peer_identity(stream: *std.net.local.types.Stream) res[std.net.local.types.PeerIdentity, std.io.error.Error]
```

the credentials of a stream's peer, as far as the target reports them

| Parameter | |
| :--- | :--- |
| `stream` | the open stream |
| **returns** | the identity with its has_ flags set for what was reported, INVALID for a nil or closed stream, or the failure, UNSUPPORTED where the target reports none |

### listener_rename

```mach
pub fun listener_rename(listener: *std.net.local.types.Listener, replacement: std.net.local.endpoint.Endpoint) err[std.io.error.Error]
```

rename never knowingly replaces an occupied path
callers must serialize parent directory mutation where atomic no-replace rename is unavailable

### stream_close

```mach
pub fun stream_close(stream: *std.net.local.types.Stream, mode: std.io.lifecycle.Mode) err[std.io.error.Error]
```

close a stream, shutting down its sending side first when graceful

the handle is closed and the stream marked closed even when shutdown fails

| Parameter | |
| :--- | :--- |
| `stream` | the open stream |
| `mode` | lifecycle.GRACEFUL or lifecycle.ABORTIVE |
| **returns** | ok, INVALID for a nil or closed stream or an unknown mode, the shutdown failure, or the close failure |

### listener_close

```mach
pub fun listener_close(listener: *std.net.local.types.Listener) err[std.io.error.Error]
```

close a listener, and when it is owned remove its socket file if the path
still names it

the listener is marked closed whatever the outcome

| Parameter | |
| :--- | :--- |
| `listener` | the open listener |
| **returns** | ok, INVALID for a nil or closed listener, the close failure, or the removal failure, BUSY when the path names another file |

## Forwards

### Kind

Forwards [`std.net.local.endpoint.Kind`](local/endpoint.md#kind).

```mach
pub def Kind: u8
```

### Endpoint

Forwards [`std.net.local.endpoint.Endpoint`](local/endpoint.md#endpoint).

```mach
pub rec Endpoint {
    kind:   Kind;
    name:   [108]u8;
    length: usize;
}
```

names are byte sequences and are never truncated or implicitly normalized

### Capabilities

Forwards [`std.net.local.endpoint.Capabilities`](local/endpoint.md#capabilities).

```mach
pub rec Capabilities {
    stream:                   bool;
    message:                  bool;
    datagram:                 bool;
    sequenced_packet:         bool;
    filesystem:               bool;
    abstract:                 bool;
    target_names:             bool;
    peer_process:             bool;
    peer_user:                bool;
    peer_group:               bool;
    owned_cleanup:            bool;
    conditional_cleanup:      bool;
    listener_rename:          bool;
    atomic_rename_no_replace: bool;
    stale_cleanup:            bool;
    custom_permissions:       bool;
}
```

what the target's local transport supports

### FILESYSTEM

Forwards [`std.net.local.endpoint.FILESYSTEM`](local/endpoint.md#kind).

```mach
pub val FILESYSTEM: Kind = 1
```

### ABSTRACT

Forwards [`std.net.local.endpoint.ABSTRACT`](local/endpoint.md#kind).

```mach
pub val ABSTRACT:   Kind = 2
```

### TARGET

Forwards [`std.net.local.endpoint.TARGET`](local/endpoint.md#kind).

```mach
pub val TARGET:     Kind = 3
```

### Ownership

Forwards [`std.net.local.types.Ownership`](local/types.md#ownership).

```mach
pub def Ownership: u8
```

### BORROWED

Forwards [`std.net.local.types.BORROWED`](local/types.md#ownership).

```mach
pub val BORROWED: Ownership = 0
```

### OWNED

Forwards [`std.net.local.types.OWNED`](local/types.md#ownership).

```mach
pub val OWNED:    Ownership = 1
```

### StalePolicy

Forwards [`std.net.local.types.StalePolicy`](local/types.md#stalepolicy).

```mach
pub def StalePolicy: u8
```

### REJECT_STALE

Forwards [`std.net.local.types.REJECT_STALE`](local/types.md#stalepolicy).

```mach
pub val REJECT_STALE:        StalePolicy = 0
```

### REMOVE_STALE_SOCKET

Forwards [`std.net.local.types.REMOVE_STALE_SOCKET`](local/types.md#stalepolicy).

```mach
pub val REMOVE_STALE_SOCKET: StalePolicy = 1
```

### INHERIT_PERMISSIONS

Forwards [`std.net.local.types.INHERIT_PERMISSIONS`](local/types.md#constants).

```mach
pub val INHERIT_PERMISSIONS: u32 = 0xffffffff
```

### BindOptions

Forwards [`std.net.local.types.BindOptions`](local/types.md#bindoptions).

```mach
pub rec BindOptions {
    ownership:   Ownership;
    stale:       StalePolicy;
    permissions: u32;
}
```

how a listener is bound

### ListenOptions

Forwards [`std.net.local.types.ListenOptions`](local/types.md#listenoptions).

```mach
pub rec ListenOptions {
    backlog:     i32;
    ownership:   Ownership;
    stale:       StalePolicy;
    permissions: u32;
}
```

how a listener is bound and started

### Listener

Forwards [`std.net.local.types.Listener`](local/types.md#listener).

```mach
pub rec Listener {
    handle:            usize;
    endpoint:          std.net.local.endpoint.Endpoint;
    ownership:         Ownership;
    node_device:       u64;
    node_file:         u64;
    has_node_identity: bool;
}
```

a bound local listener

### Stream

Forwards [`std.net.local.types.Stream`](local/types.md#stream).

```mach
pub rec Stream {
    handle:      usize;
    server_side: bool;
}
```

one owner closes the handle, and receive operations exclude aliased reads and close.

### PeerIdentity

Forwards [`std.net.local.types.PeerIdentity`](local/types.md#peeridentity).

```mach
pub rec PeerIdentity {
    process:     u64;
    user:        u64;
    group:       u64;
    has_process: bool;
    has_user:    bool;
    has_group:   bool;
}
```

the credentials of a connected peer, as far as the target reports them

