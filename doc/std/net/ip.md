[std](../README.md) / [net](README.md) / **ip**

# std.net.ip

IP address types and utilities

Source: [`src/net/ip.mach`](../../../src/net/ip.mach)

| Type | | |
| :--- | :--- | :--- |
| [`IPv4`](#ipv4) | `rec` | an IPv4 address stored as four octets |
| [`IPv6`](#ipv6) | `rec` | an IPv6 address stored as sixteen octets |
| [`Addr`](#addr) | `rec` | a tagged union of IPv4 and IPv6 addresses |
| [`Endpoint`](#endpoint) | `rec` | an IP address and port pair |
| [`ParseError`](#parseerror) | `tag` | why a borrowed text is not an address or endpoint |

| On `IPv4` | |
| :--- | :--- |
| [`ipv4`](#ipv4-1) | create an IPv4 address from four octets |
| [`ipv4_any`](#ipv4_any) | return the unspecified IPv4 address (0.0.0.0) |
| [`ipv4_loopback`](#ipv4_loopback) | return the IPv4 loopback address (127.0.0.1) |
| [`ipv4_to_u32`](#ipv4_to_u32) | convert an IPv4 address to a network byte order u32 |
| [`ipv4_from_u32`](#ipv4_from_u32) | convert a network byte order u32 to an IPv4 address |
| [`ipv4_format`](#ipv4_format) | format an IPv4 address as "a.b.c.d" into a buffer |
| [`addr_v4`](#addr_v4) | wrap an IPv4 address in an Addr |
| [`endpoint_v4`](#endpoint_v4) | create an Endpoint from an IPv4 address and a port |
| [`ipv4_parse`](#ipv4_parse) | parse a dotted-quad IPv4 address |

| On `IPv6` | |
| :--- | :--- |
| [`ipv6_any`](#ipv6_any) | return the unspecified IPv6 address (::) |
| [`ipv6_loopback`](#ipv6_loopback) | return the IPv6 loopback address (::1) |
| [`addr_v6`](#addr_v6) | wrap an IPv6 address in an Addr |
| [`endpoint_v6`](#endpoint_v6) | create an Endpoint from an IPv6 address, a port and a scope |
| [`ipv6_parse`](#ipv6_parse) | parse an IPv6 address in colon-hexadecimal form |
| [`ipv6_format`](#ipv6_format) | format an IPv6 address in its compressed lowercase form into a buffer |

| On `Addr` | |
| :--- | :--- |
| [`addr_parse`](#addr_parse) | parse a borrowed address string without retaining or allocating it |
| [`addr_format`](#addr_format) | format an address into caller-owned storage without allocating |
| [`addr_is_unspecified`](#addr_is_unspecified) | check for the unspecified address, 0.0.0.0 or :: |
| [`addr_is_loopback`](#addr_is_loopback) | check for a loopback address, 127.0.0.0/8 or ::1 |
| [`addr_is_multicast`](#addr_is_multicast) | check for a multicast address, 224.0.0.0/4 or ff00::/8 |
| [`addr_is_v4_mapped`](#addr_is_v4_mapped) | check for an IPv4-mapped IPv6 address, ::ffff:0:0/96 |

| On `Endpoint` | |
| :--- | :--- |
| [`endpoint`](#endpoint-1) | create an Endpoint from octets and a port |
| [`endpoint_family`](#endpoint_family) | the socket address family of an endpoint |
| [`sockaddr_size`](#sockaddr_size) | the size of the sockaddr to_sockaddr writes for an endpoint |
| [`to_sockaddr`](#to_sockaddr) | serialize an Endpoint into a sockaddr_in or sockaddr_in6 byte buffer |
| [`from_sockaddr`](#from_sockaddr) | deserialize a sockaddr_in or sockaddr_in6 byte buffer into an Endpoint |
| [`endpoint_parse`](#endpoint_parse) | parse a borrowed endpoint string into a self-contained value |
| [`endpoint_format`](#endpoint_format) | format an endpoint into caller-owned storage without allocating |

| Functions | |
| :--- | :--- |
| [`sockaddr_family`](#sockaddr_family) | the family a sockaddr buffer carries |

---

## IPv4

```mach
pub rec IPv4 {
    octets: [4]u8;
}
```

an IPv4 address stored as four octets

| Field | Type | |
| :--- | :--- | :--- |
| `octets` | `[4]u8` | the four octets in network order |

### ipv4

```mach
pub fun ipv4(a: u8, b: u8, c: u8, d: u8) IPv4
```

create an IPv4 address from four octets

| Parameter | |
| :--- | :--- |
| `a` | first octet |
| `b` | second octet |
| `c` | third octet |
| `d` | fourth octet |
| **returns** | the constructed IPv4 address |

### ipv4_any

```mach
pub fun ipv4_any() IPv4
```

return the unspecified IPv4 address (0.0.0.0)

### ipv4_loopback

```mach
pub fun ipv4_loopback() IPv4
```

return the IPv4 loopback address (127.0.0.1)

### ipv4_to_u32

```mach
pub fun ipv4_to_u32(ip: IPv4) u32
```

convert an IPv4 address to a network byte order u32

| Parameter | |
| :--- | :--- |
| `ip` | the IPv4 address |
| **returns** | 32-bit integer in network byte order |

### ipv4_from_u32

```mach
pub fun ipv4_from_u32(n: u32) IPv4
```

convert a network byte order u32 to an IPv4 address

| Parameter | |
| :--- | :--- |
| `n` | 32-bit integer in network byte order |
| **returns** | the constructed IPv4 address |

### ipv4_format

```mach
pub fun ipv4_format(ip: IPv4, buf: *u8, len: usize) usize
```

format an IPv4 address as "a.b.c.d" into a buffer

| Parameter | |
| :--- | :--- |
| `ip` | the IPv4 address |
| `buf` | destination buffer |
| `len` | buffer capacity in bytes |
| **returns** | number of bytes written (not including null terminator) |

### addr_v4

```mach
pub fun addr_v4(ip: IPv4) Addr
```

wrap an IPv4 address in an Addr

| Parameter | |
| :--- | :--- |
| `ip` | the IPv4 address |
| **returns** | an Addr containing the IPv4 address |

### endpoint_v4

```mach
pub fun endpoint_v4(addr: IPv4, port: u16) Endpoint
```

create an Endpoint from an IPv4 address and a port

| Parameter | |
| :--- | :--- |
| `addr` | the IPv4 address |
| `port` | port number in host byte order |
| **returns** | the endpoint, with scope zero |

### ipv4_parse

```mach
pub fun ipv4_parse(text: str) res[IPv4, ParseError]
```

parse a dotted-quad IPv4 address

each of the four parts is decimal, 0 to 255, leading zeros included

| Parameter | |
| :--- | :--- |
| `text` | the nul-terminated text, borrowed |
| **returns** | the address, or syntax |

## IPv6

```mach
pub rec IPv6 {
    octets: [16]u8;
}
```

an IPv6 address stored as sixteen octets

| Field | Type | |
| :--- | :--- | :--- |
| `octets` | `[16]u8` | the sixteen octets in network order |

### ipv6_any

```mach
pub fun ipv6_any() IPv6
```

return the unspecified IPv6 address (::)

### ipv6_loopback

```mach
pub fun ipv6_loopback() IPv6
```

return the IPv6 loopback address (::1)

### addr_v6

```mach
pub fun addr_v6(ip: IPv6) Addr
```

wrap an IPv6 address in an Addr

| Parameter | |
| :--- | :--- |
| `ip` | the IPv6 address |
| **returns** | an Addr containing the IPv6 address |

### endpoint_v6

```mach
pub fun endpoint_v6(addr: IPv6, port: u16, scope: u32) Endpoint
```

create an Endpoint from an IPv6 address, a port and a scope

| Parameter | |
| :--- | :--- |
| `addr` | the IPv6 address |
| `port` | port number in host byte order |
| `scope` | interface scope identifier, or zero |
| **returns** | the endpoint |

### ipv6_parse

```mach
pub fun ipv6_parse(text: str) res[IPv6, ParseError]
```

parse an IPv6 address in colon-hexadecimal form

accepts one `::` and a trailing embedded IPv4 address, and no zone

| Parameter | |
| :--- | :--- |
| `text` | the nul-terminated text, borrowed |
| **returns** | the address, or syntax |

### ipv6_format

```mach
pub fun ipv6_format(addr: IPv6, buf: *u8, cap: usize) usize
```

format an IPv6 address in its compressed lowercase form into a buffer

the first longest run of two or more zero groups becomes `::`. bytes past
cap are counted but not written, and a terminator is written when it fits

| Parameter | |
| :--- | :--- |
| `addr` | the IPv6 address |
| `buf` | destination buffer |
| `cap` | buffer capacity in bytes |
| **returns** | the length of the full text, not including the terminator |

## Addr

```mach
pub rec Addr {
    is_v6: u8;
    v4:    IPv4;
    v6:    IPv6;
}
```

a tagged union of IPv4 and IPv6 addresses

| Field | Type | |
| :--- | :--- | :--- |
| `is_v6` | `u8` | nonzero if the address is IPv6 |
| `v4` | `IPv4` | the IPv4 address (valid when is_v6 == 0) |
| `v6` | `IPv6` | the IPv6 address (valid when is_v6 != 0) |

### addr_parse

```mach
pub fun addr_parse(text: str) res[Addr, ParseError]
```

parse a borrowed address string without retaining or allocating it

### addr_format

```mach
pub fun addr_format(addr: Addr, buf: *u8, cap: usize) usize
```

format an address into caller-owned storage without allocating

### addr_is_unspecified

```mach
pub fun addr_is_unspecified(addr: Addr) bool
```

check for the unspecified address, 0.0.0.0 or ::

| Parameter | |
| :--- | :--- |
| `addr` | the address |
| **returns** | true when every octet of the address is zero |

### addr_is_loopback

```mach
pub fun addr_is_loopback(addr: Addr) bool
```

check for a loopback address, 127.0.0.0/8 or ::1

| Parameter | |
| :--- | :--- |
| `addr` | the address |
| **returns** | true when the address is loopback in its own family |

### addr_is_multicast

```mach
pub fun addr_is_multicast(addr: Addr) bool
```

check for a multicast address, 224.0.0.0/4 or ff00::/8

| Parameter | |
| :--- | :--- |
| `addr` | the address |
| **returns** | true when the address is multicast in its own family |

### addr_is_v4_mapped

```mach
pub fun addr_is_v4_mapped(addr: Addr) bool
```

check for an IPv4-mapped IPv6 address, ::ffff:0:0/96

| Parameter | |
| :--- | :--- |
| `addr` | the address |
| **returns** | true for an IPv6 address in that range, false for any IPv4 address |

## Endpoint

```mach
pub rec Endpoint {
    addr:  Addr;
    port:  u16;
    scope: u32;
}
```

an IP address and port pair

| Field | Type | |
| :--- | :--- | :--- |
| `addr` | `Addr` | IPv4 or IPv6 address |
| `port` | `u16` | port number in host byte order |
| `scope` | `u32` | IPv6 interface scope identifier, or zero |

### endpoint

```mach
pub fun endpoint(a: u8, b: u8, c: u8, d: u8, port: u16) Endpoint
```

create an Endpoint from octets and a port

| Parameter | |
| :--- | :--- |
| `a` | first octet |
| `b` | second octet |
| `c` | third octet |
| `d` | fourth octet |
| `port` | port number in host byte order |
| **returns** | the constructed Endpoint |

### endpoint_family

```mach
pub fun endpoint_family(ep: Endpoint) i32
```

the socket address family of an endpoint

| Parameter | |
| :--- | :--- |
| `ep` | the endpoint |
| **returns** | os.AF_INET6 for an IPv6 address, otherwise os.AF_INET |

### sockaddr_size

```mach
pub fun sockaddr_size(ep: Endpoint) usize
```

the size of the sockaddr to_sockaddr writes for an endpoint

| Parameter | |
| :--- | :--- |
| `ep` | the endpoint |
| **returns** | os.SOCKADDR_IN6_SIZE for an IPv6 address, otherwise os.SOCKADDR_IN_SIZE |

### to_sockaddr

```mach
pub fun to_sockaddr(ep: Endpoint, sa: *u8) usize
```

serialize an Endpoint into a sockaddr_in or sockaddr_in6 byte buffer

| Parameter | |
| :--- | :--- |
| `ep` | the endpoint to serialize |
| `sa` | a buffer of at least sockaddr_size(ep) bytes |
| **returns** | the bytes written |

### from_sockaddr

```mach
pub fun from_sockaddr(sa: *u8, ep: *Endpoint) bool
```

deserialize a sockaddr_in or sockaddr_in6 byte buffer into an Endpoint

| Parameter | |
| :--- | :--- |
| `sa` | the sockaddr buffer |
| `ep` | the Endpoint to fill |
| **returns** | false for any other family |

### endpoint_parse

```mach
pub fun endpoint_parse(text: str) res[Endpoint, ParseError]
```

parse a borrowed endpoint string into a self-contained value

IPv6 zones are numeric interface indices. named zones fail explicitly
because resolving an interface name belongs to a target network interface API.

### endpoint_format

```mach
pub fun endpoint_format(ep: Endpoint, buf: *u8, cap: usize) usize
```

format an endpoint into caller-owned storage without allocating

## ParseError

```mach
pub tag ParseError: u8 { syntax; empty; bracket; zone; port; }
```

why a borrowed text is not an address or endpoint

| Case | Payload | |
| :--- | :--- | :--- |
| `syntax` |  | the text does not spell an address of the requested family |
| `empty` |  | an empty endpoint text |
| `bracket` |  | an IPv6 endpoint whose `[addr]:port` framing is malformed |
| `zone` |  | an IPv6 zone that is not a numeric interface index |
| `port` |  | a missing or out-of-range port |

## Functions

### sockaddr_family

```mach
pub fun sockaddr_family(sa: *u8) i32
```

the family a sockaddr buffer carries

