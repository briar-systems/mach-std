[std](../README.md) / [allocator](README.md) / **bump**

# std.allocator.bump

brk-based bump allocator

monotonically advances a brk pointer for small allocations (\< 128KB),
falls back to mmap for large allocations. deallocate is a no-op for
brk-backed memory, individual small allocations cannot be freed, only
reclaimed on program exit. use an arena allocator for bulk-freeable
allocation patterns, or a real heap allocator for general-purpose use.
the Allocator it makes sets retains, since freed brk memory is never reused.

Source: [`src/allocator/bump.mach`](../../../src/allocator/bump.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`BumpState`](#bumpstate) | `rec` | brk bump allocator tracking state |

| On `BumpState` | |
| :--- | :--- |
| [`make`](#make) | initialize a bump-backed Allocator and its BumpState |

---

## BumpState

```mach
pub rec BumpState {
    current: usize;
    end:     usize;
}
```

brk bump allocator tracking state

| Field | Type | |
| :--- | :--- | :--- |
| `current` | `usize` | current bump pointer position |
| `end` | `usize` | current end of the brk region |

### make

```mach
pub fun make(a: *std.allocator.Allocator, state: *BumpState) err[std.allocator.Error]
```

initialize a bump-backed Allocator and its BumpState

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| `state` | BumpState to initialize (must outlive the Allocator) |
| **returns** | ok, or `invalid` when either pointer is nil |

