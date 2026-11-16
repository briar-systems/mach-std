[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **lookup**

# std.net.resolve.lookup

DNS lookup over the target's configured nameservers

Source: [`src/net/resolve/lookup.mach`](../../../../src/net/resolve/lookup.mach)

Uses types from [`std.net.ip`](../ip.md), [`std.net.resolve.conf`](conf.md).

| Type | | |
| :--- | :--- | :--- |
| [`Outcome`](#outcome) | `tag` | how a lookup ended |
| [`Answer`](#answer) | `rec` | a completed lookup: addresses in response order, A before AAAA merge order preserved per query, and the final CNAME target when a chain was followed |

| On `Answer` | |
| :--- | :--- |
| [`query_name`](#query_name) | query one fully-composed name (hostname, optionally suffixed by a search domain) for the requested families across the configured nameservers |
| [`resolve_name`](#resolve_name) | resolve a hostname applying the search-domain and ndots policy: a name at or above the dot threshold (or fully qualified) tries the literal name first, otherwise the search list is tried first |

| Constants | |
| :--- | :--- |
| [`MAX_ADDRS`](#constants) | |

---

## Outcome

```mach
pub tag Outcome: u8 { found; no_name; temporary; failed; }
```

how a lookup ended

| Case | Payload | |
| :--- | :--- | :--- |
| `found` |  | the answer holds at least one address |
| `no_name` |  | every nameserver answered and none knows the name |
| `temporary` |  | a nameserver did not answer in time; retrying may succeed |
| `failed` |  | no nameserver is configured or no family was requested |

## Answer

```mach
pub rec Answer {
    addrs:            [32]std.net.ip.Addr;
    count:            usize;
    canonical:        [254]u8;
    canonical_length: usize;
}
```

a completed lookup: addresses in response order, A before AAAA merge order
preserved per query, and the final CNAME target when a chain was followed

### query_name

```mach
pub fun query_name(config: *std.net.resolve.conf.Config, hostname: str, domain: *u8,
    want_v4: bool, want_v6: bool, answer: *Answer) Outcome
```

query one fully-composed name (hostname, optionally suffixed by a search
domain) for the requested families across the configured nameservers

### resolve_name

```mach
pub fun resolve_name(config: *std.net.resolve.conf.Config, hostname: str, want_v4: bool, want_v6: bool, answer: *Answer) Outcome
```

resolve a hostname applying the search-domain and ndots policy: a name at
or above the dot threshold (or fully qualified) tries the literal name
first, otherwise the search list is tried first. the first name that
resolves wins; a temporary or system failure aborts the search.

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_ADDRS` | `usize` | `32` |  |

