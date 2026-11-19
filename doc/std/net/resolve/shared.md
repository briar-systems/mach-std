[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **shared**

# std.net.resolve.shared

target resolver result ownership helpers

Source: [`src/net/resolve/shared.mach`](../../../../src/net/resolve/shared.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.ip`](../ip.md), [`std.net.resolve.types`](types.md), [`std.sync.cancel`](../../sync/cancel.md).

| Type | | |
| :--- | :--- | :--- |
| [`Pending`](#pending) | `rec` | a system lookup its caller may stop waiting for |

| On `Pending` | |
| :--- | :--- |
| [`pending_make`](#pending_make) | |
| [`pending_wait`](#pending_wait) | wait for the completion under a scope, asking the scope at least every POLL_MSEC |
| [`pending_done`](#pending_done) | publish that the completion has stored its result, waking a waiting caller |
| [`pending_release`](#pending_release) | let go of one reference |

| Functions | |
| :--- | :--- |
| [`error`](#error) | |
| [`ended`](#ended) | the error for a scope that ended a lookup: a destroyed or refused scope is INVALID, its native code 3 or 4 after its place among cancel.Reason's cases |
| [`scope_reason`](#scope_reason) | a lookup's scope's reason with its deadline applied, invalid for a nil scope |
| [`clear`](#clear) | |
| [`dnit`](#dnit) | release the resolution's storage; both buffers are attempted, the first refusal is reported, and a buffer whose release was refused stays owned by the resolution so the caller can retry |
| [`allocate_endpoints`](#allocate_endpoints), [`valid`](#valid), [`within_limits`](#within_limits) | |
| [`deduplicate`](#deduplicate) | compaction preserves the target resolver's first occurrence order |
| [`append_unique`](#append_unique) | first occurrence wins, preserving the target resolver's policy order; a duplicate is a success that stores nothing, a full result is OVERLOADED |
| [`set_canonical`](#set_canonical) | |
| [`is_localhost`](#is_localhost) | an RFC 6761 localhost name: `localhost` or any name under `.localhost`, case-insensitively, with an optional trailing dot |
| [`canonical_fits`](#canonical_fits) | |

| Constants | |
| :--- | :--- |
| [`POLL_MSEC`](#constants) | the longest a lookup waits before it asks its scope again, and so the bound on how long a lookup outlives the end of its scope |

---

## Pending

```mach
pub rec Pending {
    state: i64;
    refs:  i64;
}
```

a system lookup its caller may stop waiting for

the caller and whatever completes the lookup (a helper thread, or the
system's completion callback) each hold one of two references to the request
that embeds this, and the last to let go frees the request with its result.
so a caller whose scope ends returns at once and holds nothing of the lookup,
and the completion touches nothing of the caller's

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `i64` | RUNNING until the completion has stored its result, then DONE. the word the caller waits on |
| `refs` | `i64` | the references still held, 2 when made |

### pending_make

```mach
pub fun pending_make(pending: *Pending)
```

### pending_wait

```mach
pub fun pending_wait(pending: *Pending, scope: *std.sync.cancel.Scope) std.sync.cancel.Reason
```

wait for the completion under a scope, asking the scope at least every POLL_MSEC

| Parameter | |
| :--- | :--- |
| **returns** | active once the completion has stored its result, or the reason the scope ended first, invalid for a nil scope |

### pending_done

```mach
pub fun pending_done(pending: *Pending)
```

publish that the completion has stored its result, waking a waiting caller

### pending_release

```mach
pub fun pending_release(pending: *Pending) bool
```

let go of one reference

| Parameter | |
| :--- | :--- |
| **returns** | true for the last, whose holder frees the request and any result in it |

## Functions

### error

```mach
pub fun error(kind: std.net.resolve.types.ErrorKind, native_code: i64) std.net.resolve.types.Error
```

### ended

```mach
pub fun ended(reason: std.sync.cancel.Reason) std.net.resolve.types.Error
```

the error for a scope that ended a lookup: a destroyed or refused scope is
INVALID, its native code 3 or 4 after its place among cancel.Reason's cases

### scope_reason

```mach
pub fun scope_reason(scope: *std.sync.cancel.Scope) std.sync.cancel.Reason
```

a lookup's scope's reason with its deadline applied, invalid for a nil scope

### clear

```mach
pub fun clear(output: *std.net.resolve.types.Resolution, owner: *std.allocator.Allocator)
```

### dnit

```mach
pub fun dnit(output: *std.net.resolve.types.Resolution) err[std.net.resolve.types.Error]
```

release the resolution's storage; both buffers are attempted, the first
refusal is reported, and a buffer whose release was refused stays owned by
the resolution so the caller can retry

### allocate_endpoints

```mach
pub fun allocate_endpoints(output: *std.net.resolve.types.Resolution, capacity: usize) err[std.net.resolve.types.Error]
```

### valid

```mach
pub fun valid(output: *std.net.resolve.types.Resolution) bool
```

### within_limits

```mach
pub fun within_limits(output: *std.net.resolve.types.Resolution, limits: std.net.resolve.types.ResultLimits) bool
```

### deduplicate

```mach
pub fun deduplicate(output: *std.net.resolve.types.Resolution) err[std.net.resolve.types.Error]
```

compaction preserves the target resolver's first occurrence order

### append_unique

```mach
pub fun append_unique(output: *std.net.resolve.types.Resolution, endpoint: std.net.ip.Endpoint) err[std.net.resolve.types.Error]
```

first occurrence wins, preserving the target resolver's policy order; a
duplicate is a success that stores nothing, a full result is OVERLOADED

### set_canonical

```mach
pub fun set_canonical(output: *std.net.resolve.types.Resolution, name: str) err[std.net.resolve.types.Error]
```

### is_localhost

```mach
pub fun is_localhost(hostname: str) bool
```

an RFC 6761 localhost name: `localhost` or any name under `.localhost`,
case-insensitively, with an optional trailing dot

### canonical_fits

```mach
pub fun canonical_fits(name: str, max_bytes: usize) bool
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `POLL_MSEC` | `i64` | `10` | the longest a lookup waits before it asks its scope again, and so the bound on how long a lookup outlives the end of its scope |

