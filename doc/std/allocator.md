[std](README.md) / **allocator**

# std.allocator

generic allocator interface and utilities

this is intended to be the glue between platform memory primitives and higher
level containers/types

Source: [`src/allocator.mach`](../../src/allocator.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Error`](#error) | `tag` | why an allocation request or a release did not complete |
| [`Allocator`](#allocator) | `rec` | backend-agnostic allocator interface |

| On `Allocator` | |
| :--- | :--- |
| [`reclaims`](#reclaims) | whether memory given back to a is available to a later allocation from it |
| [`allocate_raw`](#allocate_raw) | allocate raw bytes using this allocator |
| [`reallocate_raw`](#reallocate_raw) | reallocate an allocation in-place if possible, otherwise may return a new pointer |
| [`deallocate_raw`](#deallocate_raw) | deallocate an allocation previously returned by allocate_raw or reallocate_raw |
| [`allocate`](#allocate) | allocate count elements of type T |
| [`zallocate`](#zallocate) | allocate and zero-initialize count elements of T |
| [`reallocate`](#reallocate) | reallocate an allocation of T elements |
| [`deallocate`](#deallocate) | deallocate memory previously returned by allocate/zallocate for count elements |

---

## Error

```mach
pub tag Error: u8 {
    exhausted;
    overflow;
    invalid;
    release: i64;
}
```

why an allocation request or a release did not complete

the first case is the zero default, so a zero-initialized `res[_, Error]`
reads as a refused request.

| Case | Payload | |
| :--- | :--- | :--- |
| `exhausted` |  | the backend refused the request, out of memory or over its bound |
| `overflow` |  | the byte count of the request does not fit usize |
| `invalid` |  | a nil allocator, an alignment that is zero or not a power of two, or another call that violates the interface contract |
| `release` | `i64` | the backend reported a negative native code while releasing storage |

## Allocator

```mach
pub rec Allocator {
    ctx:           ptr;
    fn_allocate:   fun(ptr, usize, usize) opt[ptr];
    fn_reallocate: fun(ptr, ptr, usize, usize, usize) opt[ptr];
    fn_deallocate: fun(ptr, ptr, usize, usize) i64;
    retains:       bool;
}
```

backend-agnostic allocator interface

an allocator reclaims by default: bytes given back through fn_deallocate are
available to a later allocation. a backend that never makes them available
again, such as a bump or fixed-buffer allocator, sets retains, and a wrapper
forwards its backing's retains. a container that would give capacity back
early to shed a peak asks reclaims first and keeps the capacity over a
retaining backing, since giving it back there would only cost fresh bytes
when the peak returns

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to callbacks. |
| `fn_allocate` | `fun(ptr, usize, usize) opt[ptr]` | allocate (ctx, size, align) -> some(ptr), or none when refused. |
| `fn_reallocate` | `fun(ptr, ptr, usize, usize, usize) opt[ptr]` | reallocate (ctx, p, old_size, new_size, align) -> some(ptr), or none when refused. new_size is never 0, since reallocate_raw frees that case through fn_deallocate. |
| `fn_deallocate` | `fun(ptr, ptr, usize, usize) i64` | deallocate (ctx, p, size, align) -> i64 (0 on success, negative backend native code on failure). |
| `retains` | `bool` | memory given back is never reused, zero for an allocator that reclaims |

### reclaims

```mach
pub fun reclaims(a: *Allocator) bool
```

whether memory given back to a is available to a later allocation from it

| Parameter | |
| :--- | :--- |
| `a` | the allocator to ask |
| **returns** | true unless a is nil or sets retains |

### allocate_raw

```mach
pub fun allocate_raw(a: *Allocator, size: usize, align: usize) res[ptr, Error]
```

allocate raw bytes using this allocator

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for this allocation. |
| `size` | number of bytes (0 returns nil). |
| `align` | requested alignment in bytes, a power of two. |
| **returns** | ptr to allocated memory, or the refusal |

### reallocate_raw

```mach
pub fun reallocate_raw(a: *Allocator, p: ptr, old_size: usize, new_size: usize, align: usize) res[ptr, Error]
```

reallocate an allocation in-place if possible, otherwise may return a new pointer

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for this operation |
| `p` | existing pointer (or nil to allocate new) |
| `old_size` | previous size in bytes |
| `new_size` | desired size in bytes (0 frees the allocation) |
| `align` | alignment in bytes, a power of two |
| **returns** | ptr to reallocated memory (same as p if in-place), or the refusal |

### deallocate_raw

```mach
pub fun deallocate_raw(a: *Allocator, p: ptr, size: usize, align: usize) err[Error]
```

deallocate an allocation previously returned by allocate_raw or reallocate_raw

a nil pointer is a no-op that succeeds. the backend's negative status is
carried as `release`, so a refused release keeps its native cause.

| Parameter | |
| :--- | :--- |
| `a` | Allocator to use for this operation |
| `p` | pointer previously returned by allocate_raw or reallocate_raw |
| `size` | size in bytes that was allocated |
| `align` | alignment in bytes |
| **returns** | ok, `invalid` for a nil allocator, or the backend's status as `release` |

### allocate

```mach
pub fun allocate[T](a: *Allocator, count: usize) res[*T, Error]
```

allocate count elements of type T

| Parameter | |
| :--- | :--- |
| `a` | Allocator to use for this allocation |
| `count` | number of elements to allocate |
| **returns** | pointer to allocated memory (nil for count == 0), or the refusal |

### zallocate

```mach
pub fun zallocate[T](a: *Allocator, count: usize) res[*T, Error]
```

allocate and zero-initialize count elements of T

| Parameter | |
| :--- | :--- |
| `a` | Allocator to use for this allocation |
| `count` | number of elements to allocate |
| **returns** | pointer to allocated and zero-initialized memory (nil for count == 0), or the refusal |

### reallocate

```mach
pub fun reallocate[T](a: *Allocator, p: *T, old_count: usize, new_count: usize) res[*T, Error]
```

reallocate an allocation of T elements

| Parameter | |
| :--- | :--- |
| `a` | Allocator to use for this operation |
| `p` | existing pointer |
| `old_count` | previous number of elements |
| `new_count` | desired number of elements (0 frees) |
| **returns** | pointer to reallocated memory (same as p if in-place, nil for new_count == 0), or the refusal |

### deallocate

```mach
pub fun deallocate[T](a: *Allocator, p: *T, count: usize) err[Error]
```

deallocate memory previously returned by allocate/zallocate for count
elements.

| Parameter | |
| :--- | :--- |
| `a` | Allocator to use for this operation |
| `p` | pointer returned by allocate/zallocate (may be nil) |
| `count` | number of elements to deallocate |
| **returns** | ok on success (including the nil-pointer / count == 0 no-op), or the deallocator's negative status as `release` |

