[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **types**

# std.net.resolve.types

portable asynchronous resolver types

Source: [`src/net/resolve/types.mach`](../../../../src/net/resolve/types.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.ip`](../ip.md), [`std.sync.cancel`](../../sync/cancel.md).

| Type | | |
| :--- | :--- | :--- |
| [`Family`](#family) | `def` |  |
| [`SocketKind`](#socketkind) | `def` |  |
| [`ErrorKind`](#errorkind) | `def` |  |
| [`Error`](#error) | `rec` | a resolver failure |
| [`Token`](#token) | `rec` | names one submitted lookup |
| [`Query`](#query) | `rec` | what a lookup asks for |
| [`ResultLimits`](#resultlimits) | `rec` | caps on what one resolution may allocate |
| [`Resolution`](#resolution) | `rec` | result storage belongs to the caller after completion is dequeued |
| [`Completion`](#completion) | `rec` | one finished lookup as the resolver delivers it |
| [`AdapterFun`](#adapterfun) | `def` | a resolver backend: context, the scope that bounds and cancels the lookup, the query, the result's allocator, its limits and the result to fill |

| On `Family` | |
| :--- | :--- |
| [`ANY_FAMILY`](#family), [`IPV4_ONLY`](#family), [`IPV6_ONLY`](#family) | |

| On `SocketKind` | |
| :--- | :--- |
| [`ANY_SOCKET`](#socketkind), [`STREAM_SOCKET`](#socketkind), [`DATAGRAM_SOCKET`](#socketkind) | |

| On `ErrorKind` | |
| :--- | :--- |
| [`NO_ERROR`](#errorkind), [`INVALID`](#errorkind), [`OVERLOADED`](#errorkind), [`CLOSED`](#errorkind), [`OUT_OF_MEMORY`](#errorkind), [`NO_NAME`](#errorkind), [`TEMPORARY`](#errorkind), [`MALFORMED`](#errorkind), [`SYSTEM_FAILURE`](#errorkind), [`CANCELLED`](#errorkind), [`TIMED_OUT`](#errorkind) | |

| Constants | |
| :--- | :--- |
| [`CANONICAL_NAME`](#constants), [`NUMERIC_HOST`](#constants), [`NUMERIC_SERVICE`](#constants), [`PASSIVE`](#constants) | |

---

## Family

```mach
pub def Family: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `ANY_FAMILY` | `0` |  |
| `IPV4_ONLY` | `1` |  |
| `IPV6_ONLY` | `2` |  |

## SocketKind

```mach
pub def SocketKind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `ANY_SOCKET` | `0` |  |
| `STREAM_SOCKET` | `1` |  |
| `DATAGRAM_SOCKET` | `2` |  |

## ErrorKind

```mach
pub def ErrorKind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `NO_ERROR` | `0` |  |
| `INVALID` | `1` |  |
| `OVERLOADED` | `2` |  |
| `CLOSED` | `3` |  |
| `OUT_OF_MEMORY` | `4` |  |
| `NO_NAME` | `5` |  |
| `TEMPORARY` | `6` |  |
| `MALFORMED` | `7` |  |
| `SYSTEM_FAILURE` | `8` |  |
| `CANCELLED` | `9` |  |
| `TIMED_OUT` | `10` |  |

## Error

```mach
pub rec Error {
    kind:        ErrorKind;
    native_code: i64;
}
```

a resolver failure

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `ErrorKind` | what kind of failure it is |
| `native_code` | `i64` | the backend's own status, 0 when there is none |

## Token

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

names one submitted lookup

| Field | Type | |
| :--- | :--- | :--- |
| `index` | `u32` | the lookup slot |
| `generation` | `u32` | the slot's use count, so a stale token never names a later lookup |

## Query

```mach
pub rec Query {
    host:        str;
    service:     str;
    family:      Family;
    socket_kind: SocketKind;
    protocol:    i32;
    flags:       u32;
}
```

what a lookup asks for

| Field | Type | |
| :--- | :--- | :--- |
| `host` | `str` | nul-terminated host name or numeric address, nil only with PASSIVE |
| `service` | `str` | nul-terminated service name or port, nil for port zero |
| `family` | `Family` | the address families wanted |
| `socket_kind` | `SocketKind` | the socket kind the service is looked up for |
| `protocol` | `i32` | the protocol number handed to the system resolver, 0 for any |
| `flags` | `u32` | CANONICAL_NAME, NUMERIC_HOST, NUMERIC_SERVICE and PASSIVE bits |

## ResultLimits

```mach
pub rec ResultLimits {
    max_endpoints:            usize;
    max_canonical_name_bytes: usize;
}
```

caps on what one resolution may allocate

| Field | Type | |
| :--- | :--- | :--- |
| `max_endpoints` | `usize` | the most endpoints a resolution may hold |
| `max_canonical_name_bytes` | `usize` | the most bytes a canonical name may take, its terminator included |

## Resolution

```mach
pub rec Resolution {
    endpoints:          *std.net.ip.Endpoint;
    len:                usize;
    endpoint_capacity:  usize;
    canonical_name:     *u8;
    canonical_length:   usize;
    canonical_capacity: usize;
    allocator:          *std.allocator.Allocator;
}
```

result storage belongs to the caller after completion is dequeued

## Completion

```mach
pub rec Completion {
    token:      Token;
    context:    usize;
    resolution: Resolution;
    has_error:  bool;
    error:      Error;
}
```

one finished lookup as the resolver delivers it

| Field | Type | |
| :--- | :--- | :--- |
| `token` | `Token` | the lookup it finishes |
| `context` | `usize` | the caller's value given at submission |
| `resolution` | `Resolution` | the result, which the caller owns once the completion is dequeued |
| `has_error` | `bool` | the lookup failed and error says how |
| `error` | `Error` | the failure, kind NO_ERROR on success |

## AdapterFun

```mach
pub def AdapterFun: fun(ptr, *std.sync.cancel.Scope, *Query, *std.allocator.Allocator, ResultLimits, *Resolution) Error
```

a resolver backend: context, the scope that bounds and cancels the lookup,
the query, the result's allocator, its limits and the result to fill. when
the scope ends, a backend returns within shared.POLL_MSEC with the scope's
reason (shared.ended) and holds nothing of the caller's afterwards: whatever
the system still does for the lookup is the backend's to own and free

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANONICAL_NAME` | `u32` | `1` |  |
| `NUMERIC_HOST` | `u32` | `2` |  |
| `NUMERIC_SERVICE` | `u32` | `4` |  |
| `PASSIVE` | `u32` | `8` |  |

