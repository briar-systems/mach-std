[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **shared**

# std.net.resolve.shared

target resolver result ownership helpers

Source: [`src/net/resolve/shared.mach`](../../../../src/net/resolve/shared.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.ip`](../ip.md), [`std.net.resolve.types`](types.md).

| Functions | |
| :--- | :--- |
| [`error`](#error), [`clear`](#clear) | |
| [`dnit`](#dnit) | release the resolution's storage; both buffers are attempted, the first refusal is reported, and a buffer whose release was refused stays owned by the resolution so the caller can retry |
| [`allocate_endpoints`](#allocate_endpoints), [`valid`](#valid), [`within_limits`](#within_limits) | |
| [`deduplicate`](#deduplicate) | compaction preserves the target resolver's first occurrence order |
| [`append_unique`](#append_unique) | first occurrence wins, preserving the target resolver's policy order; a duplicate is a success that stores nothing, a full result is OVERLOADED |
| [`set_canonical`](#set_canonical), [`canonical_fits`](#canonical_fits) | |

---

## Functions

### error

```mach
pub fun error(kind: std.net.resolve.types.ErrorKind, native_code: i64) std.net.resolve.types.Error
```

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

### canonical_fits

```mach
pub fun canonical_fits(name: str, max_bytes: usize) bool
```

