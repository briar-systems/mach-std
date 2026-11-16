[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **wire**

# std.net.resolve.wire

DNS message encoding and decoding (RFC 1035)

Source: [`src/net/resolve/wire.mach`](../../../../src/net/resolve/wire.mach)

Uses types from [`std.net.ip`](../ip.md).

| Type | | |
| :--- | :--- | :--- |
| [`Parsed`](#parsed) | `rec` | decoded response summary; addresses and the canonical name are written into caller storage during parse |

| On `Parsed` | |
| :--- | :--- |
| [`parse`](#parse) | decode a response, collecting addresses of the wanted record type and the final CNAME target when the answer section carries a chain |

| Functions | |
| :--- | :--- |
| [`build_query`](#build_query) | build a recursion-desired question for hostname, optionally suffixed with a search domain |

| Constants | |
| :--- | :--- |
| [`TYPE_A`](#constants), [`TYPE_CNAME`](#constants), [`TYPE_AAAA`](#constants), [`CLASS_IN`](#constants), [`RCODE_OK`](#constants), [`RCODE_FORMAT`](#constants), [`RCODE_SERVFAIL`](#constants), [`RCODE_NXDOMAIN`](#constants), [`HEADER_LENGTH`](#constants), [`MAX_MESSAGE`](#constants), [`MAX_NAME_TEXT`](#constants) | |

---

## Parsed

```mach
pub rec Parsed {
    rcode:            u8;
    truncated:        bool;
    addr_count:       usize;
    canonical_length: usize;
}
```

decoded response summary; addresses and the canonical name are written
into caller storage during parse

| Field | Type | |
| :--- | :--- | :--- |
| `rcode` | `u8` | server response code |
| `truncated` | `bool` | TC bit; the caller should retry the query over TCP |
| `addr_count` | `usize` | addresses of the wanted type written to the addrs array |
| `canonical_length` | `usize` | text length of the final CNAME target, 0 when none |

### parse

```mach
pub fun parse(buf: *u8, length: usize, id: u16, want_type: u16, addrs: *std.net.ip.Addr,
    addr_capacity: usize, canonical: *u8, canonical_capacity: usize, out: *Parsed) bool
```

decode a response, collecting addresses of the wanted record type and the
final CNAME target when the answer section carries a chain

| Parameter | |
| :--- | :--- |
| **returns** | true when the message parsed as a response to the given id; header status (rcode, truncation) is reported through out even when the answer section carries no usable records |

## Functions

### build_query

```mach
pub fun build_query(id: u16, hostname: str, domain: *u8, qtype: u16, buf: *u8, capacity: usize) usize
```

build a recursion-desired question for hostname, optionally suffixed with a
search domain. a single trailing dot marks the name fully qualified and is
stripped; when present the domain must be nil.

| Parameter | |
| :--- | :--- |
| **returns** | message length, or 0 when the name does not encode |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `TYPE_A` | `u16` | `1` |  |
| `TYPE_CNAME` | `u16` | `5` |  |
| `TYPE_AAAA` | `u16` | `28` |  |
| `CLASS_IN` | `u16` | `1` |  |
| `RCODE_OK` | `u8` | `0` |  |
| `RCODE_FORMAT` | `u8` | `1` |  |
| `RCODE_SERVFAIL` | `u8` | `2` |  |
| `RCODE_NXDOMAIN` | `u8` | `3` |  |
| `HEADER_LENGTH` | `usize` | `12` |  |
| `MAX_MESSAGE` | `usize` | `4096` |  |
| `MAX_NAME_TEXT` | `usize` | `254` |  |

