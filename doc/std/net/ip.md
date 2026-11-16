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
| [`endpoint_v4`](#endpoint_v4), [`ipv4_parse`](#ipv4_parse) | |

| On `IPv6` | |
| :--- | :--- |
| [`ipv6_any`](#ipv6_any) | return the unspecified IPv6 address (::) |
| [`ipv6_loopback`](#ipv6_loopback) | return the IPv6 loopback address (::1) |
| [`addr_v6`](#addr_v6) | wrap an IPv6 address in an Addr |
| [`endpoint_v6`](#endpoint_v6), [`ipv6_parse`](#ipv6_parse), [`ipv6_format`](#ipv6_format) | |

| On `Addr` | |
| :--- | :--- |
| [`addr_parse`](#addr_parse) | parse a borrowed address string without retaining or allocating it |
| [`addr_format`](#addr_format) | format an address into caller-owned storage without allocating |
| [`addr_is_unspecified`](#addr_is_unspecified), [`addr_is_loopback`](#addr_is_loopback), [`addr_is_multicast`](#addr_is_multicast), [`addr_is_v4_mapped`](#addr_is_v4_mapped) | |

| On `Endpoint` | |
| :--- | :--- |
| [`endpoint`](#endpoint-1) | create an Endpoint from octets and a port |
| [`endpoint_family`](#endpoint_family), [`sockaddr_size`](#sockaddr_size) | |
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

### ipv4_parse

```mach
pub fun ipv4_parse(text: str) res[IPv4, ParseError]
```

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

### ipv6_parse

```mach
pub fun ipv6_parse(text: str) res[IPv6, ParseError]
```

### ipv6_format

```mach
pub fun ipv6_format(addr: IPv6, buf: *u8, cap: usize) usize
```

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

### addr_is_loopback

```mach
pub fun addr_is_loopback(addr: Addr) bool
```

### addr_is_multicast

```mach
pub fun addr_is_multicast(addr: Addr) bool
```

### addr_is_v4_mapped

```mach
pub fun addr_is_v4_mapped(addr: Addr) bool
```

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

### sockaddr_size

```mach
pub fun sockaddr_size(ep: Endpoint) usize
```

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

