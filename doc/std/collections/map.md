[std](../README.md) / [collections](README.md) / **map**

# std.collections.map

generic hash map, open addressing with linear probing over control bytes

THE KEY CONTRACT. `Map[K, V]` hashes and compares its keys by the key type's
natural equality and hash, `std.collections.natural.eq[K]` and `hash[K]`,
resolved at compile time: an integer key hashes with a multiply-xorshift
mixer and compares with `==`, a `str` key by content, a record key field by
field. nothing is stored in the record and no call is made per probe.
`MapBy[K, V]` is the spelling for a key the type does not carry a hash or
equality for: it stores the two functions and calls them through their
pointers, so a reader can tell from the type name whether a probe is direct
or indirect. they are runtime values because mach cannot yet take a
function as a comptime parameter of a generic (briar-systems/mach#3706,
#3707).

THE KEYED MAP. `Map`'s hash is public arithmetic, so a peer who chooses the
keys can choose keys that collide and make every probe walk the whole
cluster. `MapKeyed[K, V]` is the spelling for a map whose keys an untrusted
peer can influence: a connection id, a header name, an address. it compares
keys by `natural.eq[K]` as `Map` does and hashes them with
`natural.hash_keyed[K]`, SipHash-2-4 over the natural encoding under a key it
stores, which `std.crypto.hash.siphash.random_key` draws. a hash costs more
than `Map`'s mixer, so reach for it where the keys are not the program's own.
whether `Map` itself should be keyed is an open question, not settled here.

THE LAYOUT. three buffers of `cap` slots: keys, values, and one control
byte per slot. a control byte is `EMPTY`, `DELETED` (a tombstone), or the
low seven bits of the key's hash with the high bit clear, which marks the
slot full. a probe compares control bytes first, so a mismatch is rejected
without touching the key buffer, and a miss on a full table walks one byte
per slot. this is the groundwork for matching a group of control bytes at
once with a vector compare; the byte layout is what that needs and it costs
nothing to adopt now.

capacity is always a power of two, so the slot for a hash and every probe
step is a mask rather than a divide. the invariant is asserted where the
capacity is set.

one core serves the three records: each carries a zero-size `policy` field,
the public entry point hands its value to the core, and the core is
generic over the record and the policy and dispatches on `$type_of(p)`, the
same shape `sort` and `heap` use. every routine that reads the policy, the
two one-line policy readers included, is generic over exactly `[K, V, M, P]` in
that order, so a call from one to another forwards the whole list unchanged.

Source: [`src/collections/map.mach`](../../../src/collections/map.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.crypto.hash.siphash`](../crypto/hash/siphash.md).

| Type | | |
| :--- | :--- | :--- |
| [`Map`](#map) | `rec` | a map keyed by the natural hash and equality of `K` |
| [`MapBy`](#mapby) | `rec` | a map keyed by caller-supplied hash and equality functions |
| [`MapKeyed`](#mapkeyed) | `rec` | a map keyed by the natural equality of `K` and its natural encoding hashed with SipHash under a stored key |
| [`Iter`](#iter-1) | `rec` | a walk over a map's live entries |
| [`Entry`](#entry) | `rec` | one live entry, pointing into the map's storage |

| On `Map` | |
| :--- | :--- |
| [`init`](#init) | create an empty map keyed by the natural hash and equality of `K` |
| [`dnit`](#dnit) | free all backing storage and reset the map |
| [`is_empty`](#is_empty) | check if the map has no entries |
| [`length`](#length) | return the number of entries in the map |
| [`capacity`](#capacity) | return the current capacity in slots |
| [`clear`](#clear) | remove all entries but keep allocated capacity |
| [`insert`](#insert) | insert or update a key-value pair |
| [`get`](#get) | get a pointer to the value associated with a key |
| [`contains`](#contains) | check if the map contains a key |
| [`remove`](#remove) | remove a key-value pair from the map |
| [`clone`](#clone) | a copy of the map on another allocator, without rehashing |
| [`iter`](#iter) | begin a walk over the map's entries |
| [`next`](#next) | advance to the next live entry |

| On `MapBy` | |
| :--- | :--- |
| [`init_by`](#init_by) | create an empty map keyed by the given functions |
| [`dnit_by`](#dnit_by) | free all backing storage of a `MapBy`; see `dnit` |
| [`is_empty_by`](#is_empty_by) | check if a `MapBy` has no entries; see `is_empty` |
| [`length_by`](#length_by) | return the number of entries in a `MapBy`; see `length` |
| [`capacity_by`](#capacity_by) | return the current capacity of a `MapBy` in slots; see `capacity` |
| [`clear_by`](#clear_by) | remove all entries of a `MapBy` but keep allocated capacity; see `clear` |
| [`insert_by`](#insert_by) | insert or update a key-value pair in a `MapBy`; see `insert` |
| [`insert_by_hashed`](#insert_by_hashed) | insert or update a key-value pair in a `MapBy` whose hash the caller already holds; see `insert` and `get_by_hashed`, whose contract on `hash` it shares |
| [`get_by`](#get_by) | get a pointer to the value for a key in a `MapBy`; see `get` |
| [`get_by_hashed`](#get_by_hashed) | get the value for a key in a `MapBy` whose hash the caller already holds |
| [`contains_by`](#contains_by) | check if a `MapBy` contains a key; see `contains` |
| [`remove_by`](#remove_by) | remove a key-value pair from a `MapBy`; see `remove` |
| [`clone_by`](#clone_by) | a copy of a `MapBy` on another allocator, carrying its functions; see `clone` |
| [`iter_by`](#iter_by) | begin a walk over a `MapBy`'s entries; see `iter` |
| [`next_by`](#next_by) | advance to the next live entry of a `MapBy`; see `next` |

| On `MapKeyed` | |
| :--- | :--- |
| [`init_keyed`](#init_keyed) | create an empty map hashed under a SipHash key |
| [`dnit_keyed`](#dnit_keyed) | free all backing storage of a `MapKeyed`; see `dnit` |
| [`is_empty_keyed`](#is_empty_keyed) | check if a `MapKeyed` has no entries; see `is_empty` |
| [`length_keyed`](#length_keyed) | return the number of entries in a `MapKeyed`; see `length` |
| [`capacity_keyed`](#capacity_keyed) | return the current capacity of a `MapKeyed` in slots; see `capacity` |
| [`clear_keyed`](#clear_keyed) | remove all entries of a `MapKeyed` but keep allocated capacity; see `clear` |
| [`insert_keyed`](#insert_keyed) | insert or update a key-value pair in a `MapKeyed`; see `insert` |
| [`get_keyed`](#get_keyed) | get a pointer to the value for a key in a `MapKeyed`; see `get` |
| [`contains_keyed`](#contains_keyed) | check if a `MapKeyed` contains a key; see `contains` |
| [`remove_keyed`](#remove_keyed) | remove a key-value pair from a `MapKeyed`; see `remove` |
| [`clone_keyed`](#clone_keyed) | a copy of a `MapKeyed` on another allocator under the same key; see `clone` |
| [`iter_keyed`](#iter_keyed) | begin a walk over a `MapKeyed`'s entries; see `iter` |
| [`next_keyed`](#next_keyed) | advance to the next live entry of a `MapKeyed`; see `next` |

---

## Map

```mach
pub rec Map[K, V] {
    alloc:      *std.allocator.Allocator;
    keys:       *K;
    values:     *V;
    ctrl:       *u8;
    len:        usize;
    tombstones: usize;
    cap:        usize;
    policy:     Natural;
}
```

a map keyed by the natural hash and equality of `K`

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | allocator for backing storage |
| `keys` | `*K` | key buffer |
| `values` | `*V` | value buffer |
| `ctrl` | `*u8` | one control byte per slot |
| `len` | `usize` | number of entries |
| `tombstones` | `usize` | number of deleted slots |
| `cap` | `usize` | total slot count, a power of two or zero |
| `policy` | `Natural` | the policy, a zero-size marker |

### init

```mach
pub fun init[K, V](alloc: *std.allocator.Allocator) Map[K, V]
```

create an empty map keyed by the natural hash and equality of `K`

| Parameter | |
| :--- | :--- |
| `alloc` | allocator to use for backing storage |
| **returns** | a new empty Map[K, V] |

### dnit

```mach
pub fun dnit[K, V](m: *Map[K, V]) err[std.allocator.Error]
```

free all backing storage and reset the map

entries are not visited: a key or value that owns storage is the caller's
to release before this runs. all three buffers are released even when one
release fails, and the first failure is what is reported.

| Parameter | |
| :--- | :--- |
| **returns** | ok when every buffer was released (or there were none), or the first refusal |

### is_empty

```mach
pub fun is_empty[K, V](m: Map[K, V]) bool
```

check if the map has no entries

| Parameter | |
| :--- | :--- |
| **returns** | true if the map has no entries |

### length

```mach
pub fun length[K, V](m: Map[K, V]) usize
```

return the number of entries in the map

| Parameter | |
| :--- | :--- |
| **returns** | number of entries |

### capacity

```mach
pub fun capacity[K, V](m: Map[K, V]) usize
```

return the current capacity in slots

| Parameter | |
| :--- | :--- |
| **returns** | capacity in slots |

### clear

```mach
pub fun clear[K, V](m: *Map[K, V])
```

remove all entries but keep allocated capacity

### insert

```mach
pub fun insert[K, V](m: *Map[K, V], key: K, value: V) res[bool, std.allocator.Error]
```

insert or update a key-value pair

key and value are copied into the map. updating an existing key overwrites
the stored value in place and does not touch the stored key: a value that
owns storage must be read back with `get` and released by the caller before
it is replaced. a refused growth leaves the map unchanged.

| Parameter | |
| :--- | :--- |
| `key` | key to insert |
| `value` | value to associate |
| **returns** | true if a new entry was inserted, false if an existing entry was updated, or the allocator's refusal |

### get

```mach
pub fun get[K, V](m: *Map[K, V], key: *K) opt[*V]
```

get a pointer to the value associated with a key

the pointer is into the map's storage and is invalidated by any growth.

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to look up |
| **returns** | pointer to the value, or none when the key is absent |

### contains

```mach
pub fun contains[K, V](m: *Map[K, V], key: *K) bool
```

check if the map contains a key

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to check |
| **returns** | true if the key exists |

### remove

```mach
pub fun remove[K, V](m: *Map[K, V], key: *K) bool
```

remove a key-value pair from the map

the entry's slot is released; a key or value that owns storage must be read
back with `get` and released by the caller before it is removed. removal
never allocates, so it cannot be refused.

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to remove |
| **returns** | true if removed, false if the key was not found |

### clone

```mach
pub fun clone[K, V](m: *Map[K, V], alloc: *std.allocator.Allocator) res[Map[K, V], std.allocator.Error]
```

a copy of the map on another allocator, without rehashing

the control bytes, keys and values are copied as they are, so the copy costs
a copy and answers every lookup the original does. the two share nothing
afterwards: a mutation of either is invisible to the other. all three
buffers are acquired before anything is copied, so a refusal leaves nothing
allocated. an empty map copies to an empty map on `alloc`.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for the copy's backing storage |
| **returns** | the copy, or the allocator's refusal |

### iter

```mach
pub fun iter[K, V](m: *Map[K, V]) Iter
```

begin a walk over the map's entries

| Parameter | |
| :--- | :--- |
| **returns** | a cursor at the first slot |

### next

```mach
pub fun next[K, V](m: *Map[K, V], it: *Iter, out: *Entry[K, V]) bool
```

advance to the next live entry

| Parameter | |
| :--- | :--- |
| `it` | the cursor, advanced past the entry yielded |
| `out` | filled with the entry |
| **returns** | true with `out` filled, or false when the walk is over |

## MapBy

```mach
pub rec MapBy[K, V] {
    alloc:      *std.allocator.Allocator;
    keys:       *K;
    values:     *V;
    ctrl:       *u8;
    len:        usize;
    tombstones: usize;
    cap:        usize;
    policy:     Custom;
    hash_fn:    fun(*K) u64;
    eq_fn:      fun(*K, *K) bool;
}
```

a map keyed by caller-supplied hash and equality functions

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | allocator for backing storage |
| `keys` | `*K` | key buffer |
| `values` | `*V` | value buffer |
| `ctrl` | `*u8` | one control byte per slot |
| `len` | `usize` | number of entries |
| `tombstones` | `usize` | number of deleted slots |
| `cap` | `usize` | total slot count, a power of two or zero |
| `policy` | `Custom` | the policy, a zero-size marker |
| `hash_fn` | `fun(*K) u64` | hash function over a key |
| `eq_fn` | `fun(*K, *K) bool` | equality function over two keys |

### init_by

```mach
pub fun init_by[K, V](alloc: *std.allocator.Allocator, hash_fn: fun(*K) u64, eq_fn: fun(*K, *K) bool) MapBy[K, V]
```

create an empty map keyed by the given functions

| Parameter | |
| :--- | :--- |
| `alloc` | allocator to use for backing storage |
| `hash_fn` | hash function over a key |
| `eq_fn` | equality function over two keys |
| **returns** | a new empty MapBy[K, V] |

### dnit_by

```mach
pub fun dnit_by[K, V](m: *MapBy[K, V]) err[std.allocator.Error]
```

free all backing storage of a `MapBy`; see `dnit`

### is_empty_by

```mach
pub fun is_empty_by[K, V](m: MapBy[K, V]) bool
```

check if a `MapBy` has no entries; see `is_empty`

### length_by

```mach
pub fun length_by[K, V](m: MapBy[K, V]) usize
```

return the number of entries in a `MapBy`; see `length`

### capacity_by

```mach
pub fun capacity_by[K, V](m: MapBy[K, V]) usize
```

return the current capacity of a `MapBy` in slots; see `capacity`

### clear_by

```mach
pub fun clear_by[K, V](m: *MapBy[K, V])
```

remove all entries of a `MapBy` but keep allocated capacity; see `clear`

### insert_by

```mach
pub fun insert_by[K, V](m: *MapBy[K, V], key: K, value: V) res[bool, std.allocator.Error]
```

insert or update a key-value pair in a `MapBy`; see `insert`

### insert_by_hashed

```mach
pub fun insert_by_hashed[K, V](m: *MapBy[K, V], key: K, value: V, hash: u64) res[bool, std.allocator.Error]
```

insert or update a key-value pair in a `MapBy` whose hash the caller already
holds; see `insert` and `get_by_hashed`, whose contract on `hash` it shares

### get_by

```mach
pub fun get_by[K, V](m: *MapBy[K, V], key: *K) opt[*V]
```

get a pointer to the value for a key in a `MapBy`; see `get`

### get_by_hashed

```mach
pub fun get_by_hashed[K, V](m: *MapBy[K, V], key: *K, hash: u64) opt[*V]
```

get the value for a key in a `MapBy` whose hash the caller already holds

for a caller that looks one key up in several maps sharing a hash function.
`hash` must be what the map's hash function gives for `key`; any other value
finds nothing the key was stored under.

| Parameter | |
| :--- | :--- |
| `key` | pointer to the key to look up |
| `hash` | the map's hash of `key` |
| **returns** | pointer to the value, or none when the key is absent |

### contains_by

```mach
pub fun contains_by[K, V](m: *MapBy[K, V], key: *K) bool
```

check if a `MapBy` contains a key; see `contains`

### remove_by

```mach
pub fun remove_by[K, V](m: *MapBy[K, V], key: *K) bool
```

remove a key-value pair from a `MapBy`; see `remove`

### clone_by

```mach
pub fun clone_by[K, V](m: *MapBy[K, V], alloc: *std.allocator.Allocator) res[MapBy[K, V], std.allocator.Error]
```

a copy of a `MapBy` on another allocator, carrying its functions; see `clone`

### iter_by

```mach
pub fun iter_by[K, V](m: *MapBy[K, V]) Iter
```

begin a walk over a `MapBy`'s entries; see `iter`

### next_by

```mach
pub fun next_by[K, V](m: *MapBy[K, V], it: *Iter, out: *Entry[K, V]) bool
```

advance to the next live entry of a `MapBy`; see `next`

## MapKeyed

```mach
pub rec MapKeyed[K, V] {
    alloc:      *std.allocator.Allocator;
    keys:       *K;
    values:     *V;
    ctrl:       *u8;
    len:        usize;
    tombstones: usize;
    cap:        usize;
    policy:     Keyed;
    sip_key:    std.crypto.hash.siphash.Key;
}
```

a map keyed by the natural equality of `K` and its natural encoding hashed
with SipHash under a stored key

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | allocator for backing storage |
| `keys` | `*K` | key buffer |
| `values` | `*V` | value buffer |
| `ctrl` | `*u8` | one control byte per slot |
| `len` | `usize` | number of entries |
| `tombstones` | `usize` | number of deleted slots |
| `cap` | `usize` | total slot count, a power of two or zero |
| `policy` | `Keyed` | the policy, a zero-size marker |
| `sip_key` | `std.crypto.hash.siphash.Key` | the SipHash key every hash is taken under |

### init_keyed

```mach
pub fun init_keyed[K, V](alloc: *std.allocator.Allocator, sip_key: std.crypto.hash.siphash.Key) MapKeyed[K, V]
```

create an empty map hashed under a SipHash key

draw the key with `siphash.random_key` for a map whose keys a peer can
choose, and keep it private. a map made with a fixed or leaked key is only
as floodable as `Map`.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator to use for backing storage |
| `sip_key` | the key every hash is taken under |
| **returns** | a new empty MapKeyed[K, V] |

### dnit_keyed

```mach
pub fun dnit_keyed[K, V](m: *MapKeyed[K, V]) err[std.allocator.Error]
```

free all backing storage of a `MapKeyed`; see `dnit`

### is_empty_keyed

```mach
pub fun is_empty_keyed[K, V](m: MapKeyed[K, V]) bool
```

check if a `MapKeyed` has no entries; see `is_empty`

### length_keyed

```mach
pub fun length_keyed[K, V](m: MapKeyed[K, V]) usize
```

return the number of entries in a `MapKeyed`; see `length`

### capacity_keyed

```mach
pub fun capacity_keyed[K, V](m: MapKeyed[K, V]) usize
```

return the current capacity of a `MapKeyed` in slots; see `capacity`

### clear_keyed

```mach
pub fun clear_keyed[K, V](m: *MapKeyed[K, V])
```

remove all entries of a `MapKeyed` but keep allocated capacity; see `clear`

### insert_keyed

```mach
pub fun insert_keyed[K, V](m: *MapKeyed[K, V], key: K, value: V) res[bool, std.allocator.Error]
```

insert or update a key-value pair in a `MapKeyed`; see `insert`

### get_keyed

```mach
pub fun get_keyed[K, V](m: *MapKeyed[K, V], key: *K) opt[*V]
```

get a pointer to the value for a key in a `MapKeyed`; see `get`

### contains_keyed

```mach
pub fun contains_keyed[K, V](m: *MapKeyed[K, V], key: *K) bool
```

check if a `MapKeyed` contains a key; see `contains`

### remove_keyed

```mach
pub fun remove_keyed[K, V](m: *MapKeyed[K, V], key: *K) bool
```

remove a key-value pair from a `MapKeyed`; see `remove`

### clone_keyed

```mach
pub fun clone_keyed[K, V](m: *MapKeyed[K, V], alloc: *std.allocator.Allocator) res[MapKeyed[K, V], std.allocator.Error]
```

a copy of a `MapKeyed` on another allocator under the same key; see `clone`

### iter_keyed

```mach
pub fun iter_keyed[K, V](m: *MapKeyed[K, V]) Iter
```

begin a walk over a `MapKeyed`'s entries; see `iter`

### next_keyed

```mach
pub fun next_keyed[K, V](m: *MapKeyed[K, V], it: *Iter, out: *Entry[K, V]) bool
```

advance to the next live entry of a `MapKeyed`; see `next`

## Iter

```mach
pub rec Iter {
    idx: usize;
}
```

a walk over a map's live entries

the walk visits every live entry exactly once, in slot order, which is
unspecified and changes when the map grows. the entry just yielded may be
removed; an insert may grow the table, after which the walk is over. a step
skips empty and deleted slots, so a whole walk costs the capacity.

| Field | Type | |
| :--- | :--- | :--- |
| `idx` | `usize` | the next slot to look at |

## Entry

```mach
pub rec Entry[K, V] {
    key:   *K;
    value: *V;
}
```

one live entry, pointing into the map's storage

the pointers are invalidated by growth, as `get`'s are.

| Field | Type | |
| :--- | :--- | :--- |
| `key` | `*K` | the entry's key |
| `value` | `*V` | the entry's value |

