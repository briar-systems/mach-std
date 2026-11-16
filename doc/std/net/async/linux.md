[std](../../README.md) / [net](../README.md) / [async](README.md) / **linux**

# std.net.async.linux

the linux part of the linux and darwin readiness backend for internet sockets
backend for std.net.async, signatures may change in a minor release (README, API surface)
std.net.async.unix holds the backend. what differs on linux is the packet
metadata a datagram carries in its control messages.

Source: [`src/net/async/linux.mach`](../../../../src/net/async/linux.mach)

Uses types from [`std.net.async.types`](types.md).

| Functions | |
| :--- | :--- |
| [`configure_datagram`](#configure_datagram), [`packet_metadata`](#packet_metadata), [`packet_send_metadata`](#packet_send_metadata) | |

| Constants | |
| :--- | :--- |
| [`MSG_TRUNC`](#constants) | |

---

## Functions

### configure_datagram

```mach
pub fun configure_datagram(resource: usize, family: i32) i64
```

### packet_metadata

```mach
pub fun packet_metadata(packet: *std.net.async.types.Packet, control: *u8, length: usize)
```

### packet_send_metadata

```mach
pub fun packet_send_metadata(packet: *std.net.async.types.Packet, control: *u8, length: *usize) i64
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MSG_TRUNC` | `i32` | `0x20` |  |

