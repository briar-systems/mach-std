[std](../README.md) / [collections](README.md) / **deque**

# std.collections.deque

double-ended queue (ring buffer)

Source: [`src/collections/deque.mach`](../../../src/collections/deque.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Deque`](#deque) | `rec` |  |

| On `Deque` | |
| :--- | :--- |
| [`init`](#init) | create an empty deque |
| [`dnit`](#dnit) | free the backing buffer |
| [`is_empty`](#is_empty) | check if the deque is empty |
| [`length`](#length) | return the number of elements in the deque |
| [`push_back`](#push_back) | append a value to the back of the deque |
| [`push_front`](#push_front) | prepend a value to the front of the deque |
| [`pop_back`](#pop_back) | remove and return the element at the back |
| [`pop_front`](#pop_front) | remove and return the element at the front |
| [`get`](#get) | get a pointer to the element at the given logical index |
| [`clear`](#clear) | reset the deque to empty without freeing memory |

---

## Deque

```mach
pub rec Deque[T] {
    alloc: *std.allocator.Allocator;
    data:  *T;
    head:  usize;
    len:   usize;
    cap:   usize;
}
```

### init

```mach
pub fun init[T](alloc: *std.allocator.Allocator) Deque[T]
```

create an empty deque

| Parameter | |
| :--- | :--- |
| `alloc` | allocator to use for allocations |
| **returns** | a new empty Deque[T] |

### dnit

```mach
pub fun dnit[T](dq: *Deque[T]) err[std.allocator.Error]
```

free the backing buffer

elements are not visited: an element that owns storage is the caller's to
release before this runs.

| Parameter | |
| :--- | :--- |
| **returns** | ok when the buffer was released (or there was none), or the refusal, in which case the deque is left as it was |

### is_empty

```mach
pub fun is_empty[T](dq: Deque[T]) bool
```

check if the deque is empty

| Parameter | |
| :--- | :--- |
| **returns** | true if the deque has no elements |

### length

```mach
pub fun length[T](dq: Deque[T]) usize
```

return the number of elements in the deque

| Parameter | |
| :--- | :--- |
| **returns** | number of elements |

### push_back

```mach
pub fun push_back[T](dq: *Deque[T], value: T) res[usize, std.allocator.Error]
```

append a value to the back of the deque

| Parameter | |
| :--- | :--- |
| `value` | value to append |
| **returns** | the new length, or the allocator's refusal, which leaves the deque unchanged and the value the caller's |

### push_front

```mach
pub fun push_front[T](dq: *Deque[T], value: T) res[usize, std.allocator.Error]
```

prepend a value to the front of the deque

| Parameter | |
| :--- | :--- |
| `value` | value to prepend |
| **returns** | the new length, or the allocator's refusal, which leaves the deque unchanged and the value the caller's |

### pop_back

```mach
pub fun pop_back[T](dq: *Deque[T]) opt[T]
```

remove and return the element at the back

the element is copied out; one that owns storage is now the caller's.

| Parameter | |
| :--- | :--- |
| **returns** | the value, or none when the deque is empty |

### pop_front

```mach
pub fun pop_front[T](dq: *Deque[T]) opt[T]
```

remove and return the element at the front

the element is copied out; one that owns storage is now the caller's.

| Parameter | |
| :--- | :--- |
| **returns** | the value, or none when the deque is empty |

### get

```mach
pub fun get[T](dq: *Deque[T], index: usize) opt[*T]
```

get a pointer to the element at the given logical index

the pointer is into the deque's storage and is invalidated by any growth.

| Parameter | |
| :--- | :--- |
| `index` | logical index (0 = front) |
| **returns** | pointer to element, or none when the index is out of range |

### clear

```mach
pub fun clear[T](dq: *Deque[T])
```

reset the deque to empty without freeing memory

