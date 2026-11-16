[std](../README.md) / [collections](README.md) / **bitset**

# std.collections.bitset

dynamic bitset backed by allocator

Source: [`src/collections/bitset.mach`](../../../src/collections/bitset.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Bitset`](#bitset) | `rec` | dynamic bitset storing nbits bits in an array of u64 words |

| On `Bitset` | |
| :--- | :--- |
| [`init`](#init) | create a bitset with all bits cleared |
| [`dnit`](#dnit) | free the backing word array |
| [`set`](#set) | set the bit at the given index |
| [`clear`](#clear) | clear the bit at the given index |
| [`get`](#get) | test the bit at the given index |
| [`toggle`](#toggle) | flip the bit at the given index |
| [`count`](#count) | count the number of set bits |
| [`clear_all`](#clear_all) | clear all bits to zero |
| [`set_all`](#set_all) | set all bits to one, masking the trailing word |

---

## Bitset

```mach
pub rec Bitset {
    alloc:  *std.allocator.Allocator;
    words:  *u64;
    nbits:  usize;
    nwords: usize;
}
```

dynamic bitset storing nbits bits in an array of u64 words

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | allocator for backing storage |
| `words` | `*u64` | pointer to the u64 word array |
| `nbits` | `usize` | number of bits |
| `nwords` | `usize` | number of u64 words |

### init

```mach
pub fun init(alloc: *std.allocator.Allocator, nbits: usize) res[Bitset, std.allocator.Error]
```

create a bitset with all bits cleared

the value owns its word array from here until `dnit`; it holds no pointer
to itself, so it may be copied into its final storage. a refused allocation
leaves nothing owned.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for backing storage |
| `nbits` | number of bits |
| **returns** | a new zeroed Bitset, or the allocator's refusal |

### dnit

```mach
pub fun dnit(bs: *Bitset) err[std.allocator.Error]
```

free the backing word array

| Parameter | |
| :--- | :--- |
| **returns** | ok when the words were released (or there were none), or the refusal |

### set

```mach
pub fun set(bs: *Bitset, idx: usize)
```

set the bit at the given index

| Parameter | |
| :--- | :--- |
| `idx` | bit index |

### clear

```mach
pub fun clear(bs: *Bitset, idx: usize)
```

clear the bit at the given index

| Parameter | |
| :--- | :--- |
| `idx` | bit index |

### get

```mach
pub fun get(bs: *Bitset, idx: usize) bool
```

test the bit at the given index

| Parameter | |
| :--- | :--- |
| `idx` | bit index |
| **returns** | true if the bit is set, false if cleared or out of range |

### toggle

```mach
pub fun toggle(bs: *Bitset, idx: usize)
```

flip the bit at the given index

| Parameter | |
| :--- | :--- |
| `idx` | bit index |

### count

```mach
pub fun count(bs: *Bitset) usize
```

count the number of set bits

| Parameter | |
| :--- | :--- |
| **returns** | population count |

### clear_all

```mach
pub fun clear_all(bs: *Bitset)
```

clear all bits to zero

### set_all

```mach
pub fun set_all(bs: *Bitset)
```

set all bits to one, masking the trailing word

