[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **linux**

# std.net.resolve.linux

linux native resolver adapter

resolution policy, in order: numeric addresses, RFC 6761 localhost names,
the hosts file, then DNS over the resolv.conf nameservers with search-domain
and ndots handling. results are ordered per RFC 6724. this speaks to the
kernel directly; no libc is involved, so nsswitch plugin modules do not
apply. systems routing resolution policy through a local stub resolver
(systemd-resolved and peers) keep that policy, since the stub sits behind
the nameserver interface.

Source: [`src/net/resolve/linux.mach`](../../../../src/net/resolve/linux.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.resolve.conf`](conf.md), [`std.net.resolve.types`](types.md), [`std.sync.cancel`](../../sync/cancel.md).

| Functions | |
| :--- | :--- |
| [`resolve_with_config`](#resolve_with_config) | the adapter body with an injected resolver policy, split out so tests can aim the lookup at a deterministic local nameserver |
| [`resolve`](#resolve) | |

---

## Functions

### resolve_with_config

```mach
pub fun resolve_with_config(scope: *std.sync.cancel.Scope, query: *std.net.resolve.types.Query, owner: *std.allocator.Allocator,
    limits: std.net.resolve.types.ResultLimits, output: *std.net.resolve.types.Resolution, config: *std.net.resolve.conf.Config) std.net.resolve.types.Error
```

the adapter body with an injected resolver policy, split out so tests can
aim the lookup at a deterministic local nameserver

### resolve

```mach
pub fun resolve(scope: *std.sync.cancel.Scope, query: *std.net.resolve.types.Query, owner: *std.allocator.Allocator, limits: std.net.resolve.types.ResultLimits,
    output: *std.net.resolve.types.Resolution) std.net.resolve.types.Error
```

