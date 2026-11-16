[std](../README.md) / [collections](README.md) / **sort**

# std.collections.sort

in-place sorting, searching, and array utilities

THE ORDERING CONTRACT. every entry point comes in two spellings. the bare one
(`sort`, `is_sorted`, `binary_search`, `sort_stable`) orders by the element's
natural order, `std.collections.natural.less[T]`, which is resolved at compile
time: the compare in the emitted loop is the operator on `T` itself, and no
call is made per comparison. the `_by` one takes a comparator returning
negative, zero or positive, the C `qsort` shape, and calls it through its
pointer per comparison; that is the path for an order the type does not
carry, and it costs an indirect call each time. a comparator that is not a
strict weak order (one that contradicts itself) leaves the elements in an
unspecified permutation, never out of bounds: every scan is bounded by the
range and not by a sentinel.

THE ALGORITHM is pattern-defeating quicksort (Peters, 2015): insertion sort
below `INSERTION_LIMIT`, a median-of-three pivot (ninther above
`NINTHER_LIMIT`), a partition that detects an already-partitioned range and
then confirms a nearly sorted one with a bounded insertion pass, an
equal-elements partition when the pivot repeats its predecessor so many
equal keys cost O(n), a pattern breaker on a badly unbalanced partition, and a
heapsort fallback after log2(n) of those, which is what bounds the worst case
at O(n log n). `sort` is not stable; `sort_stable` is a merge sort over a
caller-supplied scratch buffer, so nothing here allocates.

Source: [`src/collections/sort.mach`](../../../src/collections/sort.mach)

| Type | | |
| :--- | :--- | :--- |
| [`SearchPosition`](#searchposition) | `tag` | where a binary search landed |

| On `SearchPosition` | |
| :--- | :--- |
| [`binary_search`](#binary_search) | search a sorted array for a target by the element's natural order |
| [`binary_search_by`](#binary_search_by) | search a sorted array for a target by a comparator |

| Functions | |
| :--- | :--- |
| [`swap`](#swap) | exchange the values at two pointers |
| [`reverse`](#reverse) | reverse an array in place |
| [`sort`](#sort) | sort in place by the element's natural order |
| [`sort_by`](#sort_by) | sort in place by a comparator |
| [`sort_stable`](#sort_stable) | stable sort in place by the element's natural order |
| [`sort_stable_by`](#sort_stable_by) | stable sort in place by a comparator |
| [`is_sorted`](#is_sorted) | check if an array is sorted by the element's natural order |
| [`is_sorted_by`](#is_sorted_by) | check if an array is sorted according to the comparator |

---

## SearchPosition

```mach
pub tag SearchPosition: u8 {
    insertion: usize;
    found:     usize;
}
```

where a binary search landed

both outcomes carry a position, so this is a closed alternative and not a
failure: `insertion` is where the target would be inserted to keep the array
sorted, `found` is where an equal element is. `insertion` is declared first
so that a zero-initialized position reads as absent at index zero rather
than as a match.

| Case | Payload | |
| :--- | :--- | :--- |
| `insertion` | `usize` | the insertion position for an absent target |
| `found` | `usize` | the index of a matching element |

### binary_search

```mach
pub fun binary_search[T](data: *T, len: usize, target: *T) SearchPosition
```

search a sorted array for a target by the element's natural order

with equal elements present, `found` names the first of them.

| Parameter | |
| :--- | :--- |
| `data` | pointer to the sorted array |
| `len` | number of elements |
| `target` | pointer to the value to find |
| **returns** | found{index} for a match, insertion{position} otherwise |

### binary_search_by

```mach
pub fun binary_search_by[T](data: *T, len: usize, target: *T, cmp: fun(*T, *T) i64) SearchPosition
```

search a sorted array for a target by a comparator

with equal elements present, `found` names the first of them.

| Parameter | |
| :--- | :--- |
| `data` | pointer to the sorted array |
| `len` | number of elements |
| `target` | pointer to the value to find |
| `cmp` | comparator |
| **returns** | found{index} for a match, insertion{position} otherwise |

## Functions

### swap

```mach
#[inline("always")]
pub fun swap[T](a: *T, b: *T)
```

exchange the values at two pointers

| Parameter | |
| :--- | :--- |
| `a` | pointer to the first element |
| `b` | pointer to the second element |

### reverse

```mach
pub fun reverse[T](data: *T, len: usize)
```

reverse an array in place

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |

### sort

```mach
pub fun sort[T](data: *T, len: usize)
```

sort in place by the element's natural order

pattern-defeating quicksort, O(n log n) worst case, not stable. the compare
is `natural.less[T]`, resolved at compile time; a `T` without a natural order
is refused with its message.

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |

### sort_by

```mach
pub fun sort_by[T](data: *T, len: usize, cmp: fun(*T, *T) i64)
```

sort in place by a comparator

the same algorithm as `sort`, with the order supplied as a function called
through its pointer per comparison.

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |
| `cmp` | comparator returning negative if a \< b, zero if equal, positive if a > b |

### sort_stable

```mach
pub fun sort_stable[T](data: *T, len: usize, scratch: *T)
```

stable sort in place by the element's natural order

merge sort over a caller-supplied scratch buffer, O(n log n), and equal
elements keep their input order. nothing is allocated.

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |
| `scratch` | a buffer of at least `len / 2` elements the sort may overwrite |

### sort_stable_by

```mach
pub fun sort_stable_by[T](data: *T, len: usize, scratch: *T, cmp: fun(*T, *T) i64)
```

stable sort in place by a comparator

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |
| `scratch` | a buffer of at least `len / 2` elements the sort may overwrite |
| `cmp` | comparator returning negative if a \< b, zero if equal, positive if a > b |

### is_sorted

```mach
pub fun is_sorted[T](data: *T, len: usize) bool
```

check if an array is sorted by the element's natural order

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |
| **returns** | true if sorted in non-descending order |

### is_sorted_by

```mach
pub fun is_sorted_by[T](data: *T, len: usize, cmp: fun(*T, *T) i64) bool
```

check if an array is sorted according to the comparator

| Parameter | |
| :--- | :--- |
| `data` | pointer to the array |
| `len` | number of elements |
| `cmp` | comparator |
| **returns** | true if sorted in non-descending order |

