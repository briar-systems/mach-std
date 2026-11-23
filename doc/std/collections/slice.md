[std](../README.md) / [collections](README.md) / **slice**

# std.collections.slice

slice over a contiguous sequence of elements

Source: [`src/collections/slice.mach`](../../../src/collections/slice.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Slice`](#slice) | `rec` | pointer + length view over a contiguous sequence of T |

| On `Slice` | |
| :--- | :--- |
| [`make`](#make) | create a Slice[T] from a pointer and element count |
| [`is_empty`](#is_empty) | check if the slice has no elements |
| [`get`](#get) | retrieve a reference to the element at the given index |
| [`set`](#set) | update the element at the given index |

---

## Slice

```mach
pub rec Slice[T] {
    data: *T;
    size: usize;
}
```

pointer + length view over a contiguous sequence of T

| Field | Type | |
| :--- | :--- | :--- |
| `data` | `*T` | pointer to the first element |
| `size` | `usize` | number of elements in the slice |

### make

```mach
pub fun make[T](data: *T, size: usize) Slice[T]
```

create a Slice[T] from a pointer and element count

| Parameter | |
| :--- | :--- |
| `data` | pointer to the data |
| `size` | number of elements |
| **returns** | a Slice[T] over the data |

### is_empty

```mach
pub fun is_empty[T](s: Slice[T]) bool
```

check if the slice has no elements

### get

```mach
pub fun get[T](s: Slice[T], index: usize) opt[*T]
```

retrieve a reference to the element at the given index

| Parameter | |
| :--- | :--- |
| `s` | slice to access |
| `index` | element index |
| **returns** | reference to the element, or none when the index is out of range |

### set

```mach
pub fun set[T](s: Slice[T], index: usize, value: T) bool
```

update the element at the given index

| Parameter | |
| :--- | :--- |
| `s` | slice to modify |
| `index` | element index |
| `value` | new value to store |
| **returns** | true when the element was stored, false when the index is out of range |

