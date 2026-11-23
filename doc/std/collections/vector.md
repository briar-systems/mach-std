[std](../README.md) / [collections](README.md) / **vector**

# std.collections.vector

resizable dynamic array backed by an allocator

Source: [`src/collections/vector.mach`](../../../src/collections/vector.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`VectorError`](#vectorerror) | `tag` | a refused vector operation |
| [`Vector`](#vector) | `rec` | Resizable vector backed by an Allocator |

| On `Vector` | |
| :--- | :--- |
| [`init`](#init) | create an empty vector using the provided allocator |
| [`dnit`](#dnit) | free the backing buffer and reset the vector fields |
| [`is_empty`](#is_empty) | check if the vector is empty |
| [`clear`](#clear) | clear the vector contents but keep allocated capacity |
| [`reserve`](#reserve) | reserve space for additional elements, growing the backing array if necessary |
| [`ensure`](#ensure) | ensure the vector has at least the given capacity, growing if necessary |
| [`push`](#push) | append a value to the vector |
| [`pop`](#pop) | remove and return the last element |
| [`get`](#get) | get a pointer to the element at the given index |
| [`length`](#length) | return the number of elements in the vector |
| [`capacity`](#capacity) | return the number of elements the backing array holds without growing |
| [`truncate`](#truncate) | shorten the vector to its first len elements, keeping the capacity |
| [`set`](#set) | replace the element at the given index |
| [`insert`](#insert) | insert a value at the given index, shifting later elements up by one |
| [`remove`](#remove) | remove and return the element at the given index, shifting later elements down by one |
| [`swap_remove`](#swap_remove) | remove and return the element at the given index, moving the last element into its place |
| [`extend`](#extend) | append a copy of every element of a slice |
| [`items`](#items) | borrow the elements as a slice |
| [`spare`](#spare) | borrow the unused capacity past the last element as a slice |
| [`commit`](#commit) | take the first count slots of the spare capacity in as elements |
| [`shrink`](#shrink) | release the capacity past the last element |

---

## VectorError

```mach
pub tag VectorError: u8 {
    alloc: std.allocator.Error;
    bounds;
}
```

a refused vector operation

| Case | Payload | |
| :--- | :--- | :--- |
| `alloc` | `std.allocator.Error` | the allocator refused a growth, which left the vector as it was |
| `bounds` |  | an index or length lies past what the vector holds, nothing changed |

## Vector

```mach
pub rec Vector[T] {
    a:    *std.allocator.Allocator;
    data: *T;
    len:  usize;
    cap:  usize;
}
```

Resizable vector backed by an Allocator

| Field | Type | |
| :--- | :--- | :--- |
| `a` | `*std.allocator.Allocator` | allocator to use for allocations |
| `data` | `*T` | pointer to the backing array |
| `len` | `usize` | number of elements in the vector |
| `cap` | `usize` | allocated capacity of the backing array |

### init

```mach
pub fun init[T](a: *std.allocator.Allocator) Vector[T]
```

create an empty vector using the provided allocator

an empty vector owns nothing, so the value is relocatable until the first
growth and never fails to construct.

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for allocations |
| **returns** | a new empty Vector[T] |

### dnit

```mach
pub fun dnit[T](vec: *Vector[T]) err[std.allocator.Error]
```

free the backing buffer and reset the vector fields

the elements are not visited: an element that owns storage is the caller's
to release before this runs.

| Parameter | |
| :--- | :--- |
| `vec` | vector to deinitialize |
| **returns** | ok when the backing buffer was released (or there was none), or the allocator's refusal, in which case the vector is left as it was |

### is_empty

```mach
pub fun is_empty[T](vec: *Vector[T]) bool
```

check if the vector is empty

| Parameter | |
| :--- | :--- |
| **returns** | true if the vector has no elements |

### clear

```mach
pub fun clear[T](vec: *Vector[T])
```

clear the vector contents but keep allocated capacity

| Parameter | |
| :--- | :--- |
| `vec` | vector to clear |

### reserve

```mach
pub fun reserve[T](vec: *Vector[T], additional: usize) res[usize, std.allocator.Error]
```

reserve space for additional elements, growing the backing array if necessary

a refused growth leaves the vector exactly as it was: the old buffer, length
and capacity stay valid and nothing was moved.

| Parameter | |
| :--- | :--- |
| `vec` | vector to reserve space in |
| `additional` | number of extra elements to reserve space for |
| **returns** | the new capacity, or the allocator's refusal |

### ensure

```mach
pub fun ensure[T](vec: *Vector[T], cap: usize) res[usize, std.allocator.Error]
```

ensure the vector has at least the given capacity, growing if necessary

| Parameter | |
| :--- | :--- |
| `vec` | vector to ensure capacity for |
| `cap` | minimum capacity to ensure |
| **returns** | the new capacity, or the allocator's refusal |

### push

```mach
pub fun push[T](vec: *Vector[T], value: T) res[usize, std.allocator.Error]
```

append a value to the vector

the value is copied into the vector's storage. a refused push leaves the
vector unchanged and the value still the caller's.

| Parameter | |
| :--- | :--- |
| `value` | value to append |
| **returns** | the new length, or the allocator's refusal |

### pop

```mach
pub fun pop[T](vec: *Vector[T]) opt[T]
```

remove and return the last element

the element is copied out and the slot is released; an element that owns
storage is now the caller's to release.

| Parameter | |
| :--- | :--- |
| **returns** | the value, or none when the vector is empty |

### get

```mach
pub fun get[T](vec: *Vector[T], index: usize) opt[*T]
```

get a pointer to the element at the given index

the pointer is into the vector's storage and is invalidated by any growth.

| Parameter | |
| :--- | :--- |
| `index` | element index |
| **returns** | pointer to the element, or none when the index is out of range |

### length

```mach
pub fun length[T](vec: *Vector[T]) usize
```

return the number of elements in the vector

| Parameter | |
| :--- | :--- |
| **returns** | number of elements |

### capacity

```mach
pub fun capacity[T](vec: *Vector[T]) usize
```

return the number of elements the backing array holds without growing

| Parameter | |
| :--- | :--- |
| **returns** | allocated capacity in elements |

### truncate

```mach
pub fun truncate[T](vec: *Vector[T], len: usize) err[VectorError]
```

shorten the vector to its first len elements, keeping the capacity

truncate never grows the vector. the elements past len are not visited: one
that owns storage is the caller's to release, through get or items, before
this runs.

| Parameter | |
| :--- | :--- |
| `len` | the new length, at most the current length |
| **returns** | ok, or bounds when len is past the current length, which changes nothing |

### set

```mach
pub fun set[T](vec: *Vector[T], index: usize, value: T) opt[T]
```

replace the element at the given index

the replaced element is copied out; one that owns storage is now the
caller's to release.

| Parameter | |
| :--- | :--- |
| `index` | element index |
| `value` | value to store |
| **returns** | the replaced element, or none when the index is out of range, in which case nothing was stored and the value is still the caller's |

### insert

```mach
pub fun insert[T](vec: *Vector[T], index: usize, value: T) res[usize, VectorError]
```

insert a value at the given index, shifting later elements up by one

an index equal to the length appends. a refused insert leaves the vector
unchanged and the value still the caller's.

| Parameter | |
| :--- | :--- |
| `index` | position the value takes, at most the current length |
| `value` | value to insert |
| **returns** | the new length, bounds when the index is past the length, or alloc when the growth was refused |

### remove

```mach
pub fun remove[T](vec: *Vector[T], index: usize) opt[T]
```

remove and return the element at the given index, shifting later elements
down by one

the element is copied out; one that owns storage is now the caller's to
release.

| Parameter | |
| :--- | :--- |
| `index` | element index |
| **returns** | the removed element, or none when the index is out of range |

### swap_remove

```mach
pub fun swap_remove[T](vec: *Vector[T], index: usize) opt[T]
```

remove and return the element at the given index, moving the last element
into its place

constant time, but the order of the remaining elements is not kept. the
element is copied out; one that owns storage is now the caller's to release.

| Parameter | |
| :--- | :--- |
| `index` | element index |
| **returns** | the removed element, or none when the index is out of range |

### extend

```mach
pub fun extend[T](vec: *Vector[T], items: Slice[T]) res[usize, std.allocator.Error]
```

append a copy of every element of a slice

the elements are copied, so an element that owns storage is then held by
both the slice and the vector. the slice may borrow from this vector itself:
it is re-read from the grown buffer. a refused extend leaves the vector
unchanged.

| Parameter | |
| :--- | :--- |
| `items` | elements to append |
| **returns** | the new length, or the allocator's refusal |

### items

```mach
pub fun items[T](vec: *Vector[T]) Slice[T]
```

borrow the elements as a slice

the slice points into the vector's storage and is invalidated by any growth,
shrink, insert or removal.

| Parameter | |
| :--- | :--- |
| **returns** | a slice over the vector's elements |

### spare

```mach
pub fun spare[T](vec: *Vector[T]) Slice[T]
```

borrow the unused capacity past the last element as a slice

its contents are unspecified. writing into it does not change the length:
commit takes the written slots in. the slice is invalidated by any growth,
shrink or insert.

| Parameter | |
| :--- | :--- |
| **returns** | a slice over the slots between the length and the capacity |

### commit

```mach
pub fun commit[T](vec: *Vector[T], count: usize) res[usize, VectorError]
```

take the first count slots of the spare capacity in as elements

the caller has written those slots, through spare, before this runs.

| Parameter | |
| :--- | :--- |
| `count` | number of spare slots written, at most the spare capacity |
| **returns** | the new length, or bounds when count is past the spare capacity, which changes nothing |

### shrink

```mach
pub fun shrink[T](vec: *Vector[T]) res[usize, std.allocator.Error]
```

release the capacity past the last element

over an allocator that never reclaims what it is given back, the capacity is
kept, since releasing it there would only cost fresh bytes on the next
growth. a refused shrink leaves the vector exactly as it was.

| Parameter | |
| :--- | :--- |
| **returns** | the capacity now held, or the allocator's refusal |

