[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **order**

# std.net.resolve.order

RFC 6724 destination address ordering

Source: [`src/net/resolve/order.mach`](../../../../src/net/resolve/order.mach)

Uses types from [`std.net.ip`](../ip.md).

| Functions | |
| :--- | :--- |
| [`sort`](#sort) | stable in-place ordering of resolved destinations per RFC 6724; a set larger than MAX_SORT keeps its resolver order |

---

## Functions

### sort

```mach
pub fun sort(addrs: *std.net.ip.Addr, count: usize)
```

stable in-place ordering of resolved destinations per RFC 6724; a set
larger than MAX_SORT keeps its resolver order

