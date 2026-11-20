[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **lookup**

# std.net.resolve.lookup

DNS lookup over the target's configured nameservers

a lookup runs under the caller's cancellation scope: when the scope ends, it
returns within shared.POLL_MSEC with the scope's reason and holds no socket.
every wait blocks for at most that long before it asks the scope again, the
TCP retry's connect included. the configuration's timeout_ms is the
resolver's own policy, how long one request waits before the next server is
tried, and never outlasts the scope

Source: [`src/net/resolve/lookup.mach`](../../../../src/net/resolve/lookup.mach)

Uses types from [`std.net.ip`](../ip.md), [`std.net.resolve.conf`](conf.md), [`std.sync.cancel`](../../sync/cancel.md).

| Type | | |
| :--- | :--- | :--- |
| [`Outcome`](#outcome) | `tag` | how a lookup ended |
| [`Answer`](#answer) | `rec` | a completed lookup: addresses in the order their responses arrived, each response's records in answer order, and the canonical name |

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
pub tag Outcome: u8 { found; no_name; temporary; failed; ended: std.sync.cancel.Reason; }
```

how a lookup ended

| Case | Payload | |
| :--- | :--- | :--- |
| `found` |  | the answer holds at least one address |
| `no_name` |  | every nameserver answered and none knows the name, or the name does not encode as a query |
| `temporary` |  | a nameserver did not answer in time; retrying may succeed |
| `failed` |  | no nameserver is configured or no family was requested |
| `ended` | `std.sync.cancel.Reason` | the scope ended the lookup first, with its reason (invalid for a nil scope) |

## Answer

```mach
pub rec Answer {
    addrs:            [32]std.net.ip.Addr;
    count:            usize;
    canonical:        [254]u8;
    canonical_length: usize;
}
```

a completed lookup: addresses in the order their responses arrived, each
response's records in answer order, and the canonical name

| Field | Type | |
| :--- | :--- | :--- |
| `addrs` | `[32]std.net.ip.Addr` | the addresses found, at most MAX_ADDRS |
| `count` | `usize` | valid entries in addrs |
| `canonical` | `[254]u8` | nul-terminated final CNAME target when a chain was followed, otherwise after resolve_name the name that resolved |
| `canonical_length` | `usize` | text length of canonical, 0 when there is none |

### query_name

```mach
pub fun query_name(config: *std.net.resolve.conf.Config, scope: *std.sync.cancel.Scope, hostname: str, domain: *u8,
    want_v4: bool, want_v6: bool, answer: *Answer) Outcome
```

query one fully-composed name (hostname, optionally suffixed by a search
domain) for the requested families across the configured nameservers

| Parameter | |
| :--- | :--- |
| `config` | the resolver policy |
| `scope` | bounds and cancels the lookup |
| `hostname` | the name to ask for |
| `domain` | a search domain to append, or nil |
| `want_v4` | ask for A records |
| `want_v6` | ask for AAAA records |
| `answer` | filled with what was found, meaningful when the outcome is found |
| **returns** | how the lookup ended |

### resolve_name

```mach
pub fun resolve_name(config: *std.net.resolve.conf.Config, scope: *std.sync.cancel.Scope, hostname: str, want_v4: bool, want_v6: bool, answer: *Answer) Outcome
```

resolve a hostname applying the search-domain and ndots policy: a name at
or above the dot threshold (or fully qualified) tries the literal name
first, otherwise the search list is tried first. the first name that
resolves wins; a temporary or system failure, or the scope ending, aborts
the search.

| Parameter | |
| :--- | :--- |
| `config` | the resolver policy |
| `scope` | bounds and cancels the whole search |
| `hostname` | the name to resolve |
| `want_v4` | ask for A records |
| `want_v6` | ask for AAAA records |
| `answer` | filled with what was found, meaningful when the outcome is found |
| **returns** | how the lookup ended |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_ADDRS` | `usize` | `32` |  |

