[std](../../README.md) / [net](../README.md) / [local](README.md) / **types**

# std.net.local.types

local transport descriptor and ownership types

Source: [`src/net/local/types.mach`](../../../../src/net/local/types.mach)

Uses types from [`std.net.local.endpoint`](endpoint.md).

| Type | | |
| :--- | :--- | :--- |
| [`Ownership`](#ownership) | `def` |  |
| [`StalePolicy`](#stalepolicy) | `def` |  |
| [`BindOptions`](#bindoptions) | `rec` |  |
| [`ListenOptions`](#listenoptions) | `rec` |  |
| [`Listener`](#listener) | `rec` |  |
| [`Stream`](#stream) | `rec` | one owner closes the handle, and receive operations exclude aliased reads and close |
| [`PeerIdentity`](#peeridentity) | `rec` |  |

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

## ListenOptions

```mach
pub rec ListenOptions {
    backlog:     i32;
    ownership:   Ownership;
    stale:       StalePolicy;
    permissions: u32;
}
```

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

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `INHERIT_PERMISSIONS` | `u32` | `0xffffffff` |  |

