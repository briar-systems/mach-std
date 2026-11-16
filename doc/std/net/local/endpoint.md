[std](../../README.md) / [net](../README.md) / [local](README.md) / **endpoint**

# std.net.local.endpoint

tagged local transport endpoints and target capabilities

Source: [`src/net/local/endpoint.mach`](../../../../src/net/local/endpoint.mach)

Uses types from [`std.io.error`](../../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Kind`](#kind) | `def` |  |
| [`Endpoint`](#endpoint) | `rec` | names are byte sequences and are never truncated or implicitly normalized |
| [`Capabilities`](#capabilities) | `rec` |  |

| On `Kind` | |
| :--- | :--- |
| [`FILESYSTEM`](#kind), [`ABSTRACT`](#kind), [`TARGET`](#kind), [`maximum_name_length`](#maximum_name_length) | |

| On `Endpoint` | |
| :--- | :--- |
| [`supported`](#supported), [`filesystem_bytes`](#filesystem_bytes), [`filesystem`](#filesystem) | |
| [`filesystem_native`](#filesystem_native) | a filesystem endpoint from a nul-terminated path in std.runtime.native units |
| [`abstract`](#abstract), [`target_bytes`](#target_bytes), [`target`](#target), [`equal`](#equal) | |
| [`to_sockaddr`](#to_sockaddr) | serialize only sockaddr-based endpoints |
| [`from_sockaddr`](#from_sockaddr) | |

| On `Capabilities` | |
| :--- | :--- |
| [`capabilities`](#capabilities-1) | |

| Constants | |
| :--- | :--- |
| [`NAME_CAPACITY`](#constants) | |

---

## Kind

```mach
pub def Kind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `FILESYSTEM` | `1` |  |
| `ABSTRACT` | `2` |  |
| `TARGET` | `3` |  |

### maximum_name_length

```mach
pub fun maximum_name_length(kind: Kind) usize
```

## Endpoint

```mach
pub rec Endpoint {
    kind:   Kind;
    name:   [108]u8;
    length: usize;
}
```

names are byte sequences and are never truncated or implicitly normalized

### supported

```mach
pub fun supported(endpoint: Endpoint) bool
```

### filesystem_bytes

```mach
pub fun filesystem_bytes(data: *u8, length: usize) res[Endpoint, std.io.error.Error]
```

### filesystem

```mach
pub fun filesystem(path: str) res[Endpoint, std.io.error.Error]
```

### filesystem_native

```mach
pub fun filesystem_native(name: *Unit) res[Endpoint, std.io.error.Error]
```

a filesystem endpoint from a nul-terminated path in std.runtime.native units

linux and darwin take the path as bytes, so they are the endpoint's name
unchanged, valid UTF-8 or not. windows sun_path is a byte string too, spelled
in UTF-8, so the UTF-16 path is converted once, and a path holding an
unpaired surrogate, which has no UTF-8 spelling, cannot name a local socket
there. it is refused with INVALID here, before any socket call

| Parameter | |
| :--- | :--- |
| `name` | the nul-terminated path |
| **returns** | the endpoint, or INVALID for a nil, empty, overlong or unspellable path |

### abstract

```mach
pub fun abstract(data: *u8, length: usize) res[Endpoint, std.io.error.Error]
```

### target_bytes

```mach
pub fun target_bytes(data: *u8, length: usize) res[Endpoint, std.io.error.Error]
```

### target

```mach
pub fun target(name: str) res[Endpoint, std.io.error.Error]
```

### equal

```mach
pub fun equal(a: Endpoint, b: Endpoint) bool
```

### to_sockaddr

```mach
pub fun to_sockaddr(endpoint: Endpoint, address: *u8, capacity: usize, length: *usize) err[std.io.error.Kind]
```

serialize only sockaddr-based endpoints

### from_sockaddr

```mach
pub fun from_sockaddr(address: *u8, length: usize, endpoint: *Endpoint) err[std.io.error.Kind]
```

## Capabilities

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

### capabilities

```mach
pub fun capabilities() Capabilities
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `NAME_CAPACITY` | `usize` | `108` |  |

