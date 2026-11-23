[std](../README.md) / [collections](README.md) / **natural**

# std.collections.natural

the natural order, equality and hash of a type, resolved at compile time

every collection that orders or hashes its elements reads this module rather
than carrying its own notion, so `sort`, `Heap`, `Map` and `Set` agree on what
"less than" and "equal" mean for a `T`. each operation is a generic whose body
is decided per instantiation: an integer or float compares with the operator,
a `str` compares by content, and a record compares lexicographically over its
fields in declaration order, descending into nested records. nothing here is a
function value, so the compare a collection emits is the operator itself, not
a call through a pointer.

WHAT HAS A NATURAL ORDER. integers and floats (by `<`, so a NaN is unordered
and a sort over NaNs has an unspecified but bounded result), `str` (by
`str_compare`, and equality by `str_equals`), and records whose fields all
classify under `std.derive`'s contract: scalars and nested records. a record
is ordered by its first differing field, so a caller that wants "by priority,
then by id" declares the fields in that order. a union, a tag, an array, a
vector or a `^` secret field is refused at compile time with `derive.check`'s
message. any other pointer type is refused here: address order is a choice,
and a caller who wants it says so through a comparator.

`str` IS `*char`. the type comparison cannot tell them apart, so a `*char`
element is compared and hashed by the string it points at. a record field of
type `str` is a pointer field and falls to `derive.check`'s refusal, which is
the same rule `derive.eq` and `derive.hash` apply.

THE HASH. a scalar is finalized with the murmur3 `fmix64` mixer; a string is
folded eight bytes at a time and finalized the same way; a record folds each
scalar field as one word in declaration order, so a nested record contributes
exactly what a flattened one would. two values that are `eq` hash alike. the
hash is not stable across std versions and is not a cryptographic one.

THE KEYED HASH. `hash_keyed` runs the same encoding, one little-endian word
per scalar and a string's bytes, through SipHash-2-4 under a caller's key
(`std.crypto.hash.siphash`). it is for keys an untrusted peer can choose,
where the unkeyed mixer lets the peer precompute collisions.

Source: [`src/collections/natural.mach`](../../../src/collections/natural.mach)

Uses types from [`std.crypto.hash.siphash`](../crypto/hash/siphash.md).

| Functions | |
| :--- | :--- |
| [`less`](#less) | the natural strict order of `T` |
| [`eq`](#eq) | the natural equality of `T` |
| [`hash`](#hash) | the natural hash of `T` |
| [`hash_keyed`](#hash_keyed) | the natural hash of `T` under a SipHash key |
| [`hash_str`](#hash_str) | hash a NUL-terminated string eight bytes at a time |

---

## Functions

### less

```mach
#[inline("always")]
pub fun less[T](a: *T, b: *T) bool
```

the natural strict order of `T`

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `a` | left operand |
| `b` | right operand |
| **returns** | true when `a` sorts before `b` |

### eq

```mach
#[inline("always")]
pub fun eq[T](a: *T, b: *T) bool
```

the natural equality of `T`

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `a` | left operand |
| `b` | right operand |
| **returns** | true when `a` and `b` are equal |

### hash

```mach
#[inline("always")]
pub fun hash[T](v: *T) u64
```

the natural hash of `T`

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `v` | the value to hash |
| **returns** | a 64-bit hash, equal for values that are `eq` |

### hash_keyed

```mach
pub fun hash_keyed[T](key: std.crypto.hash.siphash.Key, v: *T) u64
```

the natural hash of `T` under a SipHash key

equal for values that are `eq` under one key, and unpredictable without it.

| Parameter | |
| :--- | :--- |
| `[T]` | the element type |
| `key` | the SipHash key |
| `v` | the value to hash |
| **returns** | a 64-bit hash |

### hash_str

```mach
pub fun hash_str(s: str) u64
```

hash a NUL-terminated string eight bytes at a time

the length is measured first so the fold never reads past the terminator,
and the tail is folded as a partial word. the length itself seeds the fold,
so `"a"` and `"a\0..."` are distinct from a padded word. a nil string hashes
as the empty one, matching `str_equals`.

| Parameter | |
| :--- | :--- |
| `s` | the string |
| **returns** | the hash |

