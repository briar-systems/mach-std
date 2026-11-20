[std](../../README.md) / [net](../README.md) / [local](README.md) / **endpoint**

# std.net.local.endpoint

tagged local transport endpoints and target capabilities

Source: [`src/net/local/endpoint.mach`](../../../../src/net/local/endpoint.mach)

Uses types from [`std.io.error`](../../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Kind`](#kind) | `def` |  |
| [`Endpoint`](#endpoint) | `rec` | names are byte sequences and are never truncated or implicitly normalized |
| [`Capabilities`](#capabilities) | `rec` | what the target's local transport supports |

| On `Kind` | |
| :--- | :--- |
| [`FILESYSTEM`](#kind), [`ABSTRACT`](#kind), [`TARGET`](#kind) | |
| [`maximum_name_length`](#maximum_name_length) | the longest name the target accepts for a kind |

| On `Endpoint` | |
| :--- | :--- |
| [`supported`](#supported) | check an endpoint's name is non-empty and within its kind's limit on this target |
| [`filesystem_bytes`](#filesystem_bytes) | a filesystem endpoint named by length bytes of a path |
| [`filesystem`](#filesystem) | a filesystem endpoint named by a nul-terminated path |
| [`filesystem_native`](#filesystem_native) | a filesystem endpoint from a nul-terminated path in std.runtime.native units |
| [`abstract`](#abstract) | an abstract endpoint named by length bytes, NUL bytes included |
| [`target_bytes`](#target_bytes) | a target-name endpoint named by length bytes |
| [`target`](#target) | a target-name endpoint named by a nul-terminated name |
| [`equal`](#equal) | compare two endpoints by kind and name bytes |
| [`to_sockaddr`](#to_sockaddr) | serialize only sockaddr-based endpoints |
| [`from_sockaddr`](#from_sockaddr) | decode a local sockaddr into an endpoint |

| On `Capabilities` | |
| :--- | :--- |
| [`capabilities`](#capabilities-1) | the local transport capabilities of the build target |

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

the longest name the target accepts for a kind

| Parameter | |
| :--- | :--- |
| `kind` | the endpoint kind |
| **returns** | the limit in bytes, 0 when the target does not support the kind |

## Endpoint

```mach
pub rec Endpoint {
    kind:   Kind;
    name:   [108]u8;
    length: usize;
}
```

names are byte sequences and are never truncated or implicitly normalized

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `Kind` | the namespace of the name |
| `name` | `[108]u8` | the name bytes, zero past length |
| `length` | `usize` | name bytes in use |

### supported

```mach
pub fun supported(endpoint: Endpoint) bool
```

check an endpoint's name is non-empty and within its kind's limit on this target

| Parameter | |
| :--- | :--- |
| `endpoint` | the endpoint to check |
| **returns** | true when the target can use it |

### filesystem_bytes

```mach
pub fun filesystem_bytes(data: *u8, length: usize) res[Endpoint, std.io.error.Error]
```

a filesystem endpoint named by length bytes of a path

| Parameter | |
| :--- | :--- |
| `data` | the path bytes, copied |
| `length` | path bytes, at most maximum_name_length(FILESYSTEM) |
| **returns** | the endpoint, INVALID for nil, empty, overlong or NUL-holding bytes, or UNSUPPORTED when the target has no filesystem endpoints |

### filesystem

```mach
pub fun filesystem(path: str) res[Endpoint, std.io.error.Error]
```

a filesystem endpoint named by a nul-terminated path

| Parameter | |
| :--- | :--- |
| `path` | the path, copied |
| **returns** | as filesystem_bytes |

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

an abstract endpoint named by length bytes, NUL bytes included

| Parameter | |
| :--- | :--- |
| `data` | the name bytes, copied |
| `length` | name bytes, at most maximum_name_length(ABSTRACT) |
| **returns** | the endpoint, INVALID for nil, empty or overlong bytes, or UNSUPPORTED off linux |

### target_bytes

```mach
pub fun target_bytes(data: *u8, length: usize) res[Endpoint, std.io.error.Error]
```

a target-name endpoint named by length bytes

| Parameter | |
| :--- | :--- |
| `data` | the name bytes, copied |
| `length` | name bytes |
| **returns** | the endpoint, or UNSUPPORTED since no current target has target names |

### target

```mach
pub fun target(name: str) res[Endpoint, std.io.error.Error]
```

a target-name endpoint named by a nul-terminated name

| Parameter | |
| :--- | :--- |
| `name` | the name, copied |
| **returns** | as target_bytes |

### equal

```mach
pub fun equal(a: Endpoint, b: Endpoint) bool
```

compare two endpoints by kind and name bytes

| Parameter | |
| :--- | :--- |
| `a` | first endpoint |
| `b` | second endpoint |
| **returns** | true when kinds, lengths and bytes match, false for a length past NAME_CAPACITY |

### to_sockaddr

```mach
pub fun to_sockaddr(endpoint: Endpoint, address: *u8, capacity: usize, length: *usize) err[std.io.error.Kind]
```

serialize only sockaddr-based endpoints

| Parameter | |
| :--- | :--- |
| `endpoint` | the endpoint to encode |
| `address` | storage for the sockaddr, zeroed first |
| `capacity` | bytes at address |
| `length` | receives the sockaddr length |
| **returns** | ok, INVALID for nil storage, an unsupported endpoint or too little room, or UNSUPPORTED for a kind with no sockaddr form |

### from_sockaddr

```mach
pub fun from_sockaddr(address: *u8, length: usize, endpoint: *Endpoint) err[std.io.error.Kind]
```

decode a local sockaddr into an endpoint

| Parameter | |
| :--- | :--- |
| `address` | the sockaddr bytes |
| `length` | the sockaddr length the system reported |
| `endpoint` | receives the endpoint |
| **returns** | ok, or INVALID for a nil pointer, a malformed address or a name the target does not accept |

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

what the target's local transport supports

| Field | Type | |
| :--- | :--- | :--- |
| `stream` | `bool` | byte streams |
| `message` | `bool` | message-preserving streams |
| `datagram` | `bool` | datagrams |
| `sequenced_packet` | `bool` | sequenced packets |
| `filesystem` | `bool` | FILESYSTEM endpoints |
| `abstract` | `bool` | ABSTRACT endpoints |
| `target_names` | `bool` | TARGET endpoints |
| `peer_process` | `bool` | peer identity reports the process |
| `peer_user` | `bool` | peer identity reports the user |
| `peer_group` | `bool` | peer identity reports the group |
| `owned_cleanup` | `bool` | an OWNED listener removes its socket file on close |
| `conditional_cleanup` | `bool` | that removal leaves a path that names another file |
| `listener_rename` | `bool` | listener_rename is available |
| `atomic_rename_no_replace` | `bool` | rename refuses an occupied path atomically |
| `stale_cleanup` | `bool` | REMOVE_STALE_SOCKET is honoured |
| `custom_permissions` | `bool` | bind options may set the socket file's permissions |

### capabilities

```mach
pub fun capabilities() Capabilities
```

the local transport capabilities of the build target

| Parameter | |
| :--- | :--- |
| **returns** | the capability set, all false on a target with no local transport |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `NAME_CAPACITY` | `usize` | `108` |  |

