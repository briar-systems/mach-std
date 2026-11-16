[std](../README.md) / [collections](README.md) / **heap**

# std.collections.heap

binary heap (priority queue)

THE ORDERING CONTRACT. `Heap[T, D]` orders by the element's natural order,
`std.collections.natural.less[T]`, and `D` says which end is on top:
`Min` pops the least element first, `Max` the greatest. the compare in the
emitted sift is the operator on `T` itself, resolved at compile time, with no
call per comparison and nothing stored in the record. `HeapBy[T]` is the
spelling for an order the type does not carry: it stores a comparator and
calls it through its pointer per comparison, so a reader can tell from the
type name whether a sift is direct or indirect.

one core serves the three records. the policy is a zero-size value: each
record carries it as its `order` field, the public entry point hands that
value to the core, and every routine in the core is generic over the record
and the policy and dispatches on `$type_of(d)`. the value costs nothing to
pass, the gate folds per instantiation, and the sift bodies exist once. this
is the same shape `sort` uses for its `Natural` / `ByCmp` markers.

Source: [`src/collections/heap.mach`](../../../src/collections/heap.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Min`](#min) | `rec` | the least element is on top |
| [`Max`](#max) | `rec` | the greatest element is on top |
| [`Heap`](#heap) | `rec` | a heap ordered by the element's natural order |
| [`HeapBy`](#heapby) | `rec` | a heap ordered by a comparator |

| On `Heap` | |
| :--- | :--- |
| [`init`](#init) | create an empty heap by the natural order |
| [`dnit`](#dnit) | free the backing buffer |
| [`is_empty`](#is_empty) | check if the heap is empty |
| [`length`](#length) | return the number of elements in the heap |
| [`push`](#push) | add an element to the heap |
| [`pop`](#pop) | remove and return the top element |
| [`peek`](#peek) | return a pointer to the top element without removing it |

| On `HeapBy` | |
| :--- | :--- |
| [`init_by`](#init_by) | create an empty heap by a comparator |
| [`dnit_by`](#dnit_by) | free the backing buffer of a comparator heap; see `dnit` |
| [`is_empty_by`](#is_empty_by) | check if a comparator heap is empty |
| [`length_by`](#length_by) | return the number of elements in a comparator heap |
| [`push_by`](#push_by) | add an element to a comparator heap; see `push` |
| [`pop_by`](#pop_by) | remove and return the top element of a comparator heap; see `pop` |
| [`peek_by`](#peek_by) | return a pointer to the top element of a comparator heap; see `peek` |

---

## Min

```mach
pub rec Min {}
```

the least element is on top

## Max

```mach
pub rec Max {}
```

the greatest element is on top

## Heap

```mach
pub rec Heap[T, D] {
    alloc: *std.allocator.Allocator;
    data:  *T;
    len:   usize;
    cap:   usize;
    order: D;
}
```

a heap ordered by the element's natural order

| Field | Type | |
| :--- | :--- | :--- |
| `[T]` |  | the element type |
| `[D]` |  | `Min` or `Max` |
| `alloc` | `*std.allocator.Allocator` | allocator for the backing buffer |
| `data` | `*T` | the backing buffer |
| `len` | `usize` | number of elements |
| `cap` | `usize` | capacity in elements |
| `order` | `D` | the policy, a zero-size marker |

### init

```mach
pub fun init[T, D](alloc: *std.allocator.Allocator) Heap[T, D]
```

create an empty heap by the natural order

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `[D]` | `Min` or `Max` |
| `alloc` | allocator to use for allocations |
| **returns** | a new empty Heap[T, D] |

### dnit

```mach
pub fun dnit[T, D](h: *Heap[T, D]) err[std.allocator.Error]
```

free the backing buffer

elements are not visited: an element that owns storage is the caller's to
release before this runs.

| Parameter | |
| :--- | :--- |
| **returns** | ok when the buffer was released (or there was none), or the refusal, in which case the heap is left as it was |

### is_empty

```mach
pub fun is_empty[T, D](h: Heap[T, D]) bool
```

check if the heap is empty

| Parameter | |
| :--- | :--- |
| **returns** | true if the heap has no elements |

### length

```mach
pub fun length[T, D](h: Heap[T, D]) usize
```

return the number of elements in the heap

| Parameter | |
| :--- | :--- |
| **returns** | number of elements |

### push

```mach
pub fun push[T, D](h: *Heap[T, D], value: T) res[usize, std.allocator.Error]
```

add an element to the heap

the value is copied in; a refused growth leaves the heap unchanged and the
value the caller's.

| Parameter | |
| :--- | :--- |
| `value` | value to insert |
| **returns** | the new length, or the allocator's refusal |

### pop

```mach
pub fun pop[T, D](h: *Heap[T, D]) opt[T]
```

remove and return the top element

the element is copied out; one that owns storage is now the caller's.

| Parameter | |
| :--- | :--- |
| **returns** | the top value, or none when the heap is empty |

### peek

```mach
pub fun peek[T, D](h: *Heap[T, D]) opt[*T]
```

return a pointer to the top element without removing it

the pointer is into the heap's storage and is invalidated by any growth.

| Parameter | |
| :--- | :--- |
| **returns** | pointer to the top element, or none when the heap is empty |

## HeapBy

```mach
pub rec HeapBy[T] {
    alloc: *std.allocator.Allocator;
    data:  *T;
    len:   usize;
    cap:   usize;
    order: By;
    cmp:   fun(*T, *T) i64;
}
```

a heap ordered by a comparator

the least element under the comparator is on top; a max-heap is a
comparator with its arguments swapped.

| Field | Type | |
| :--- | :--- | :--- |
| `[T]` |  | the element type |
| `alloc` | `*std.allocator.Allocator` | allocator for the backing buffer |
| `data` | `*T` | the backing buffer |
| `len` | `usize` | number of elements |
| `cap` | `usize` | capacity in elements |
| `order` | `By` | the policy, a zero-size marker |
| `cmp` | `fun(*T, *T) i64` | the comparator, negative if a \< b, zero if equal, positive if a > b |

### init_by

```mach
pub fun init_by[T](alloc: *std.allocator.Allocator, cmp: fun(*T, *T) i64) HeapBy[T]
```

create an empty heap by a comparator

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `alloc` | allocator to use for allocations |
| `cmp` | comparison function (negative if a \< b, 0 if equal, positive if a > b) |
| **returns** | a new empty HeapBy[T] |

### dnit_by

```mach
pub fun dnit_by[T](h: *HeapBy[T]) err[std.allocator.Error]
```

free the backing buffer of a comparator heap; see `dnit`

### is_empty_by

```mach
pub fun is_empty_by[T](h: HeapBy[T]) bool
```

check if a comparator heap is empty

| Parameter | |
| :--- | :--- |
| **returns** | true if the heap has no elements |

### length_by

```mach
pub fun length_by[T](h: HeapBy[T]) usize
```

return the number of elements in a comparator heap

| Parameter | |
| :--- | :--- |
| **returns** | number of elements |

### push_by

```mach
pub fun push_by[T](h: *HeapBy[T], value: T) res[usize, std.allocator.Error]
```

add an element to a comparator heap; see `push`

### pop_by

```mach
pub fun pop_by[T](h: *HeapBy[T]) opt[T]
```

remove and return the top element of a comparator heap; see `pop`

### peek_by

```mach
pub fun peek_by[T](h: *HeapBy[T]) opt[*T]
```

return a pointer to the top element of a comparator heap; see `peek`

