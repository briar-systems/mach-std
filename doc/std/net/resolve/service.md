[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **service**

# std.net.resolve.service

service name to port resolution

Source: [`src/net/resolve/service.mach`](../../../../src/net/resolve/service.mach)

Uses types from [`std.net.resolve.types`](types.md).

| Functions | |
| :--- | :--- |
| [`numeric`](#numeric) | parse a decimal port, rejecting overflow and empty or trailing garbage |
| [`scan_line`](#scan_line) | fold one services line into the search; true when the line resolves it |
| [`lookup`](#lookup) | resolve a service name to a port via /etc/services |

---

## Functions

### numeric

```mach
pub fun numeric(service: str, port: *u16) bool
```

parse a decimal port, rejecting overflow and empty or trailing garbage

### scan_line

```mach
pub fun scan_line(line: *u8, service: str, socket_kind: std.net.resolve.types.SocketKind, port: *u16) bool
```

fold one services line into the search; true when the line resolves it

### lookup

```mach
pub fun lookup(service: str, socket_kind: std.net.resolve.types.SocketKind) res[opt[u16], std.net.resolve.types.Error]
```

resolve a service name to a port via /etc/services

| Parameter | |
| :--- | :--- |
| **returns** | the port of the first matching entry, absent when no entry matches or the file is missing, or the read failure |

