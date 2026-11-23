[std](../README.md) / [allocator](README.md) / **arena**

# std.allocator.arena

arena allocator implementation

bump allocator with chunked growth. allocation is O(1) amortized.
deallocate is a no-op except for the most recent allocation which
can be rolled back. reallocate is in-place for the most recent
allocation when space permits, otherwise alloc+copy. grows
automatically by allocating new chunks from the backing allocator.
the Allocator it makes sets retains, since only a rollback is reused.

Source: [`src/allocator/arena.mach`](../../../src/allocator/arena.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Chunk`](#chunk) | `rec` | header for each backing allocation |
| [`Arena`](#arena) | `rec` | bump allocator state with chunked growth |

| On `Arena` | |
| :--- | :--- |
| [`init`](#init) | initialize an Arena with a backing allocator and optional initial capacity |
| [`dnit`](#dnit) | free all chunks and zero the Arena state |
| [`allocator`](#allocator) | wire up an Allocator backed by this Arena |
| [`reset`](#reset) | reset the Arena to empty, freeing all chunks except the first |

---

## Chunk

```mach
pub rec Chunk {
    prev: *Chunk;
    cap:  usize;
}
```

header for each backing allocation

| Field | Type | |
| :--- | :--- | :--- |
| `prev` | `*Chunk` | previous chunk in the linked list |
| `cap` | `usize` | data capacity in bytes (data follows the header) |

## Arena

```mach
pub rec Arena {
    backing: std.allocator.Allocator;

    buf: ptr;
    cap: usize;
    off: usize;

    last_off:  usize;
    last_size: usize;

    chunk:       *Chunk;
    first_chunk: *Chunk;
    default_cap: usize;
}
```

bump allocator state with chunked growth

| Field | Type | |
| :--- | :--- | :--- |
| `backing` | `std.allocator.Allocator` | allocator used for chunk allocations |
| `buf` | `ptr` | current chunk data pointer (cached for fast-path) |
| `cap` | `usize` | current chunk data capacity (cached) |
| `off` | `usize` | current allocation offset within current chunk |
| `last_off` | `usize` | offset of most recent allocation (for rollback/resize) |
| `last_size` | `usize` | size of most recent allocation (for rollback/resize) |
| `chunk` | `*Chunk` | current chunk header |
| `first_chunk` | `*Chunk` | first chunk (for reset/dnit) |
| `default_cap` | `usize` | minimum chunk capacity for growth |

### init

```mach
pub fun init(ar: *Arena, backing: *std.allocator.Allocator, cap: usize) err[std.allocator.Error]
```

initialize an Arena with a backing allocator and optional initial capacity

| Parameter | |
| :--- | :--- |
| `ar` | Arena to initialize |
| `backing` | allocator used to provide backing storage |
| `cap` | initial chunk capacity in bytes (0 = lazy allocation on first use) |
| **returns** | ok, `invalid` for a nil arena or backing allocator, or the refusal of the first chunk |

### dnit

```mach
pub fun dnit(ar: *Arena) err[std.allocator.Error]
```

free all chunks and zero the Arena state

every chunk is released even when one release fails; the first failure is
what is reported, so a combined failure stays observable.

| Parameter | |
| :--- | :--- |
| `ar` | Arena to destroy |
| **returns** | ok if all backing frees succeeded, or the first negative backend native code as `release` |

### allocator

```mach
pub fun allocator(a: *std.allocator.Allocator, ar: *Arena) err[std.allocator.Error]
```

wire up an Allocator backed by this Arena

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| `ar` | initialized Arena (must outlive the Allocator) |
| **returns** | ok, or `invalid` when either pointer is nil |

### reset

```mach
pub fun reset(ar: *Arena)
```

reset the Arena to empty, freeing all chunks except the first

existing allocations become invalid after reset.

| Parameter | |
| :--- | :--- |
| `ar` | Arena to reset |

