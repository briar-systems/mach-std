[std](../README.md) / [net](README.md) / **dns**

# std.net.dns

DNS hostname resolution

a convenience IPv4 surface over the native resolver modules. richer needs
(dual stack, canonical names, services, asynchrony) belong to
std.net.resolve. a lookup runs under the caller's cancellation scope and keeps
std.net.resolve's contract: when the scope ends, it returns within 10 ms with
the scope's reason and holds nothing of the caller's afterwards.

Source: [`src/net/dns.mach`](../../../src/net/dns.mach)

Uses types from [`std.net.ip`](ip.md), [`std.net.resolve.types`](resolve/types.md), [`std.sync.cancel`](../sync/cancel.md).

| Functions | |
| :--- | :--- |
| [`lookup_hosts`](#lookup_hosts) | resolve a hostname via the system hosts file |
| [`query`](#query) | resolve a hostname via a DNS A record query |
| [`resolve`](#resolve) | resolve a hostname to an IPv4 address |

---

## Functions

### lookup_hosts

```mach
pub fun lookup_hosts(hostname: str, addr: *std.net.ip.IPv4) res[bool, std.net.resolve.types.Error]
```

resolve a hostname via the system hosts file

searches the platform hosts file for a matching hostname and writes
the first IPv4 address found into addr.

| Parameter | |
| :--- | :--- |
| `hostname` | null-terminated hostname to look up |
| `addr` | pointer to an IPv4 to fill on a match |
| **returns** | whether a match was found, or the hosts file failure |

### query

```mach
pub fun query(scope: *std.sync.cancel.Scope, hostname: str, addr: *std.net.ip.IPv4) res[bool, std.net.resolve.types.Error]
```

resolve a hostname via a DNS A record query

queries the target's configured nameservers for the literal name, without
search-domain expansion. writes the first address from the response into
addr. windows configures its resolver through the winsock surface instead
of resolv.conf, so this is not found there; use std.net.resolve.

| Parameter | |
| :--- | :--- |
| `scope` | bounds and cancels the lookup |
| `hostname` | null-terminated hostname to resolve |
| `addr` | pointer to an IPv4 to fill on success |
| **returns** | whether the name resolved, or the configuration or lookup failure |

### resolve

```mach
pub fun resolve(scope: *std.sync.cancel.Scope, hostname: str, addr: *std.net.ip.IPv4) res[bool, std.net.resolve.types.Error]
```

resolve a hostname to an IPv4 address

per RFC 6761 the name `localhost` and any name ending in `.localhost`
resolve to the loopback address (127.0.0.1) without consulting the hosts
file or a nameserver, this is resolver behavior, not hosts-file content,
and so is portable across platforms whose hosts file omits localhost.
other names fall back to the hosts file, then DNS with the target's
search-domain policy applied.

| Parameter | |
| :--- | :--- |
| `scope` | bounds and cancels the DNS lookup |
| `hostname` | null-terminated hostname to resolve |
| `addr` | pointer to an IPv4 to fill on success |
| **returns** | whether the name resolved, or the hosts, configuration or lookup failure |

