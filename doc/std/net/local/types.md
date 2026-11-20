[std](../../README.md) / [net](../README.md) / [local](README.md) / **types**

# std.net.local.types

local transport descriptor and ownership types

Source: [`src/net/local/types.mach`](../../../../src/net/local/types.mach)

Uses types from [`std.net.local.endpoint`](endpoint.md).

| Type | | |
| :--- | :--- | :--- |
| [`Ownership`](#ownership) | `def` |  |
| [`StalePolicy`](#stalepolicy) | `def` |  |
| [`BindOptions`](#bindoptions) | `rec` | how a listener is bound |
| [`ListenOptions`](#listenoptions) | `rec` | how a listener is bound and started |
| [`Listener`](#listener) | `rec` | a bound local listener |
| [`Stream`](#stream) | `rec` | one owner closes the handle, and receive operations exclude aliased reads and close |
| [`PeerIdentity`](#peeridentity) | `rec` | the credentials of a connected peer, as far as the target reports them |

| On `Ownership` | |
| :--- | :--- |
| [`BORROWED`](#ownership), [`OWNED`](#ownership) | |

| On `StalePolicy` | |
| :--- | :--- |
| [`REJECT_STALE`](#stalepolicy), [`REMOVE_STALE_SOCKET`](#stalepolicy) | |

| Constants | |
| :--- | :--- |
| [`INHERIT_PERMISSIONS`](#constants) | |

---

## Ownership

```mach
pub def Ownership: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `BORROWED` | `0` |  |
| `OWNED` | `1` |  |

## StalePolicy

```mach
pub def StalePolicy: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `REJECT_STALE` | `0` |  |
| `REMOVE_STALE_SOCKET` | `1` |  |

## BindOptions

```mach
pub rec BindOptions {
    ownership:   Ownership;
    stale:       StalePolicy;
    permissions: u32;
}
```

how a listener is bound

| Field | Type | |
| :--- | :--- | :--- |
| `ownership` | `Ownership` | whether the listener removes its socket file on close |
| `stale` | `StalePolicy` | what to do with a socket file already at the path |
| `permissions` | `u32` | mode bits 0o777 to set on the socket file, or INHERIT_PERMISSIONS |

## ListenOptions

```mach
pub rec ListenOptions {
    backlog:     i32;
    ownership:   Ownership;
    stale:       StalePolicy;
    permissions: u32;
}
```

how a listener is bound and started

| Field | Type | |
| :--- | :--- | :--- |
| `backlog` | `i32` | pending connections the system may queue, above zero |
| `ownership` | `Ownership` | whether the listener removes its socket file on close |
| `stale` | `StalePolicy` | what to do with a socket file already at the path |
| `permissions` | `u32` | mode bits 0o777 to set on the socket file, or INHERIT_PERMISSIONS |

## Listener

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

| Field | Type | |
| :--- | :--- | :--- |
| `handle` | `usize` | the native socket, all ones when closed |
| `endpoint` | `std.net.local.endpoint.Endpoint` | the endpoint it is bound to |
| `ownership` | `Ownership` | whether close removes its socket file |
| `node_device` | `u64` | device of the socket file as bound |
| `node_file` | `u64` | file number of the socket file as bound |
| `has_node_identity` | `bool` | node_device and node_file were captured |

## Stream

```mach
pub rec Stream {
    handle:      usize;
    server_side: bool;
}
```

one owner closes the handle, and receive operations exclude aliased reads and close.

## PeerIdentity

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

| Field | Type | |
| :--- | :--- | :--- |
| `process` | `u64` | the peer's process id, valid when has_process |
| `user` | `u64` | the peer's user id, valid when has_user |
| `group` | `u64` | the peer's group id, valid when has_group |
| `has_process` | `bool` | process was reported |
| `has_user` | `bool` | user was reported |
| `has_group` | `bool` | group was reported |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `INHERIT_PERMISSIONS` | `u32` | `0xffffffff` |  |

