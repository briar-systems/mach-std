[std](../README.md) / [collections](README.md) / **set**

# std.collections.set

hash set backed by Map

`Set[K]` keys by the natural hash and equality of `K` and `SetBy[K]` by
stored functions, exactly as `Map` and `MapBy` do; see `map` for the
contract.

Source: [`src/collections/set.mach`](../../../src/collections/set.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.collections.map`](map.md).

| Type | | |
| :--- | :--- | :--- |
| [`Set`](#set) | `rec` | hash set of unique keys by the natural hash and equality of `K` |
| [`SetBy`](#setby) | `rec` | hash set of unique keys by caller-supplied hash and equality functions |

| On `Set` | |
| :--- | :--- |
| [`init`](#init) | create an empty set |
| [`dnit`](#dnit) | free all backing storage and reset the set |
| [`is_empty`](#is_empty) | check if the set has no entries |
| [`length`](#length) | return the number of entries in the set |
| [`insert`](#insert) | add a key to the set |
| [`contains`](#contains) | check if the set contains a key |
| [`remove`](#remove) | remove a key from the set |
| [`clone`](#clone) | a copy of the set on another allocator, without rehashing; see `map.clone` |
| [`iter`](#iter) | begin a walk over the set's keys; see `map.iter` for the walk's rules |
| [`next`](#next) | advance to the next live key |
| [`clear`](#clear) | remove all entries but keep allocated capacity |

| On `SetBy` | |
| :--- | :--- |
| [`init_by`](#init_by) | create an empty set keyed by the given functions |
| [`dnit_by`](#dnit_by) | free all backing storage of a `SetBy`; see `dnit` |
| [`is_empty_by`](#is_empty_by) | check if a `SetBy` has no entries; see `is_empty` |
| [`length_by`](#length_by) | return the number of entries in a `SetBy`; see `length` |
| [`insert_by`](#insert_by) | add a key to a `SetBy`; see `insert` |
| [`contains_by`](#contains_by) | check if a `SetBy` contains a key; see `contains` |
| [`remove_by`](#remove_by) | remove a key from a `SetBy`; see `remove` |
| [`clone_by`](#clone_by) | a copy of a `SetBy` on another allocator, carrying its functions; see `clone` |
| [`iter_by`](#iter_by) | begin a walk over a `SetBy`'s keys; see `iter` |
| [`next_by`](#next_by) | advance to the next live key of a `SetBy`; see `next` |
| [`clear_by`](#clear_by) | remove all entries of a `SetBy` but keep allocated capacity; see `clear` |

---

## Set

```mach
pub rec Set[K] {
    inner: std.collections.map.Map[K, u8];
}
```

hash set of unique keys by the natural hash and equality of `K`

| Field | Type | |
| :--- | :--- | :--- |
| `inner` | `std.collections.map.Map[K, u8]` | backing hash map with u8 dummy values |

### init

```mach
pub fun init[K](alloc: *std.allocator.Allocator) Set[K]
```

create an empty set

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for backing storage |
| **returns** | a new empty Set[K] |

### dnit

```mach
pub fun dnit[K](s: *Set[K]) err[std.allocator.Error]
```

free all backing storage and reset the set

| Parameter | |
| :--- | :--- |
| **returns** | ok when the backing storage was released, or the first refusal |

### is_empty

```mach
pub fun is_empty[K](s: Set[K]) bool
```

check if the set has no entries

| Parameter | |
| :--- | :--- |
| **returns** | true if the set is empty |

### length

```mach
pub fun length[K](s: Set[K]) usize
```

return the number of entries in the set

| Parameter | |
| :--- | :--- |
| **returns** | number of entries |

### insert

```mach
pub fun insert[K](s: *Set[K], key: K) res[bool, std.allocator.Error]
```

add a key to the set

| Parameter | |
| :--- | :--- |
| `key` | key to insert |
| **returns** | true if the key was new, false if it already existed, or the allocator's refusal |

### contains

```mach
pub fun contains[K](s: *Set[K], key: *K) bool
```

check if the set contains a key

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to check |
| **returns** | true if the key exists |

### remove

```mach
pub fun remove[K](s: *Set[K], key: *K) bool
```

remove a key from the set

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to remove |
| **returns** | true if removed, false if the key was not found |

### clone

```mach
pub fun clone[K](s: *Set[K], alloc: *std.allocator.Allocator) res[Set[K], std.allocator.Error]
```

a copy of the set on another allocator, without rehashing; see `map.clone`

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for the copy's backing storage |
| **returns** | the copy, or the allocator's refusal |

### iter

```mach
pub fun iter[K](s: *Set[K]) std.collections.map.Iter
```

begin a walk over the set's keys; see `map.iter` for the walk's rules

| Parameter | |
| :--- | :--- |
| **returns** | a cursor at the first slot |

### next

```mach
pub fun next[K](s: *Set[K], it: *std.collections.map.Iter, out: **K) bool
```

advance to the next live key

| Parameter | |
| :--- | :--- |
| `it` | the cursor, advanced past the key yielded |
| `out` | filled with a pointer to the key, into the set's storage |
| **returns** | true with `out` filled, or false when the walk is over |

### clear

```mach
pub fun clear[K](s: *Set[K])
```

remove all entries but keep allocated capacity

## SetBy

```mach
pub rec SetBy[K] {
    inner: std.collections.map.MapBy[K, u8];
}
```

hash set of unique keys by caller-supplied hash and equality functions

| Field | Type | |
| :--- | :--- | :--- |
| `inner` | `std.collections.map.MapBy[K, u8]` | backing hash map with u8 dummy values |

### init_by

```mach
pub fun init_by[K](alloc: *std.allocator.Allocator, hash_fn: fun(*K) u64, eq_fn: fun(*K, *K) bool) SetBy[K]
```

create an empty set keyed by the given functions

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for backing storage |
| `hash_fn` | hash function over a key |
| `eq_fn` | equality function over two keys |
| **returns** | a new empty SetBy[K] |

### dnit_by

```mach
pub fun dnit_by[K](s: *SetBy[K]) err[std.allocator.Error]
```

free all backing storage of a `SetBy`; see `dnit`

### is_empty_by

```mach
pub fun is_empty_by[K](s: SetBy[K]) bool
```

check if a `SetBy` has no entries; see `is_empty`

### length_by

```mach
pub fun length_by[K](s: SetBy[K]) usize
```

return the number of entries in a `SetBy`; see `length`

### insert_by

```mach
pub fun insert_by[K](s: *SetBy[K], key: K) res[bool, std.allocator.Error]
```

add a key to a `SetBy`; see `insert`

### contains_by

```mach
pub fun contains_by[K](s: *SetBy[K], key: *K) bool
```

check if a `SetBy` contains a key; see `contains`

### remove_by

```mach
pub fun remove_by[K](s: *SetBy[K], key: *K) bool
```

remove a key from a `SetBy`; see `remove`

### clone_by

```mach
pub fun clone_by[K](s: *SetBy[K], alloc: *std.allocator.Allocator) res[SetBy[K], std.allocator.Error]
```

a copy of a `SetBy` on another allocator, carrying its functions; see `clone`

### iter_by

```mach
pub fun iter_by[K](s: *SetBy[K]) std.collections.map.Iter
```

begin a walk over a `SetBy`'s keys; see `iter`

### next_by

```mach
pub fun next_by[K](s: *SetBy[K], it: *std.collections.map.Iter, out: **K) bool
```

advance to the next live key of a `SetBy`; see `next`

### clear_by

```mach
pub fun clear_by[K](s: *SetBy[K])
```

remove all entries of a `SetBy` but keep allocated capacity; see `clear`

