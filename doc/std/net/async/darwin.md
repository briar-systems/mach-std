[std](../../README.md) / [net](../README.md) / [async](README.md) / **darwin**

# std.net.async.darwin

the darwin part of the linux and darwin readiness backend for internet sockets
backend for std.net.async, signatures may change in a minor release (README, API surface)
std.net.async.unix holds the backend. what differs on darwin is the packet
metadata a datagram carries in its control messages.

Source: [`src/net/async/darwin.mach`](../../../../src/net/async/darwin.mach)

Uses types from [`std.net.async.types`](types.md).

| Functions | |
| :--- | :--- |
| [`configure_datagram`](#configure_datagram) | ask the kernel to report each datagram's local destination and interface |
| [`packet_metadata`](#packet_metadata) | fill a received packet's local destination and interface from its control messages |
| [`packet_send_metadata`](#packet_send_metadata) | build the control messages that send a packet from its local destination and interface |

| Constants | |
| :--- | :--- |
| [`MSG_TRUNC`](#constants) | |

---

## Functions

### configure_datagram

```mach
pub fun configure_datagram(resource: usize, family: i32) i64
```

ask the kernel to report each datagram's local destination and interface

| Parameter | |
| :--- | :--- |
| `resource` | the native datagram socket |
| `family` | the socket's address family |
| **returns** | 0, a negative native error, or ENOTSUP for a family other than inet and inet6 |

### packet_metadata

```mach
pub fun packet_metadata(packet: *std.net.async.types.Packet, control: *u8, length: usize)
```

fill a received packet's local destination and interface from its control messages

| Parameter | |
| :--- | :--- |
| `packet` | the packet received |
| `control` | the control message bytes |
| `length` | bytes of control messages, parsing stops at the first malformed one |

### packet_send_metadata

```mach
pub fun packet_send_metadata(packet: *std.net.async.types.Packet, control: *u8, length: *usize) i64
```

build the control messages that send a packet from its local destination and interface

| Parameter | |
| :--- | :--- |
| `packet` | the packet to send |
| `control` | at least 48 bytes of control message storage |
| `length` | receives the control message length, 0 when the packet asks for neither |
| **returns** | 0, or a negative native error for metadata the family cannot carry |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MSG_TRUNC` | `i32` | `0x10` |  |

