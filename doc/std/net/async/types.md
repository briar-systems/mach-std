[std](../../README.md) / [net](../README.md) / [async](README.md) / **types**

# std.net.async.types

portable asynchronous network descriptors

Source: [`src/net/async/types.mach`](../../../../src/net/async/types.mach)

Uses types from [`std.io.runtime`](../../io/runtime.md), [`std.net.ip`](../ip.md).

| Type | | |
| :--- | :--- | :--- |
| [`Token`](#token) | `rec` |  |
| [`Vector`](#vector) | `rec` |  |
| [`Packet`](#packet) | `rec` | packet storage is borrowed until its operation completes |
| [`NativeCompletion`](#nativecompletion) | `rec` |  |

| Constants | |
| :--- | :--- |
| [`STATUS_STALE`](#constants) | the status a backend reports for an operation left pending on a socket that was closed outside its driver |
| [`STATUS_CANCELLED`](#constants) | the status a backend reports for an operation whose cancellation it finished asynchronously: the driver publishes the cancellation, never a result |

---

## Token

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

## Vector

```mach
pub rec Vector {
    data:   *u8;
    length: usize;
}
```

## Packet

```mach
pub rec Packet {
    buffer:                *u8;
    capacity:              usize;
    length:                usize;
    peer:                  std.net.ip.Endpoint;
    local_destination:     std.net.ip.Addr;
    interface_index:       u32;
    has_local_destination: bool;
    truncated:             bool;
    zero_length:           bool;
}
```

packet storage is borrowed until its operation completes

| Field | Type | |
| :--- | :--- | :--- |
| `buffer` | `*u8` | the packet's storage |
| `capacity` | `usize` | the storage size in bytes. a send refuses a length above it |
| `length` | `usize` | bytes to send, or bytes received |

## NativeCompletion

```mach
pub rec NativeCompletion {
    context:       usize;
    kind:          std.io.runtime.Kind;
    bytes:         usize;
    items:         usize;
    resource:      usize;
    status:        i64;
    end_of_stream: bool;
}
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `STATUS_STALE` | `i64` | `-0x4000000000000000` | the status a backend reports for an operation left pending on a socket that was closed outside its driver |
| `STATUS_CANCELLED` | `i64` | `-0x4000000000000001` | the status a backend reports for an operation whose cancellation it finished asynchronously: the driver publishes the cancellation, never a result |

