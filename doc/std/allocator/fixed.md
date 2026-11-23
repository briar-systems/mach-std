[std](../README.md) / [allocator](README.md) / **fixed**

# std.allocator.fixed

fixed-buffer bump allocator

bump-allocates from a caller-provided byte buffer and never calls the OS.
individual allocations cannot be freed; the whole buffer is reclaimed at
once with reset, or discarded with its owner. suitable for bounded scratch,
no-syscall contexts, and as an allocator below the OS layer in the module
graph (where a page/brk-backed allocator would form an import cycle).
the Allocator it makes sets retains, since nothing freed is reused.

Source: [`src/allocator/fixed.mach`](../../../src/allocator/fixed.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`FixedState`](#fixedstate) | `rec` | fixed-buffer bump allocator state |

| On `FixedState` | |
| :--- | :--- |
| [`make`](#make) | initialize a fixed-buffer Allocator over a caller-provided buffer |
| [`reset`](#reset) | reclaim every allocation at once by rewinding to the start of the buffer |
| [`remaining`](#remaining) | unused capacity remaining in the buffer |

---

## FixedState

```mach
pub rec FixedState {
    buffer:   *u8;
    capacity: usize;
    offset:   usize;
}
```

fixed-buffer bump allocator state

| Field | Type | |
| :--- | :--- | :--- |
| `buffer` | `*u8` | caller-provided backing buffer |
| `capacity` | `usize` | capacity of buffer in bytes |
| `offset` | `usize` | bytes consumed so far (including alignment padding) |

### make

```mach
pub fun make(a: *std.allocator.Allocator, state: *FixedState, buf: *u8, cap: usize) err[std.allocator.Error]
```

initialize a fixed-buffer Allocator over a caller-provided buffer

the buffer and state must outlive the Allocator. allocations are drawn from
buf until it is exhausted, after which allocation fails rather than growing.

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| `state` | FixedState to initialize (must outlive the Allocator) |
| `buf` | backing buffer the allocator bumps within |
| `cap` | capacity of buf in bytes |
| **returns** | ok, or `invalid` when any pointer is nil |

### reset

```mach
pub fun reset(state: *FixedState)
```

reclaim every allocation at once by rewinding to the start of the buffer

| Parameter | |
| :--- | :--- |
| `state` | FixedState to reset |

### remaining

```mach
pub fun remaining(state: *FixedState) usize
```

unused capacity remaining in the buffer

| Parameter | |
| :--- | :--- |
| `state` | FixedState to query |
| **returns** | bytes left before allocation fails (before any alignment padding) |

