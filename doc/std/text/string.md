[std](../README.md) / [text](README.md) / **string**

# std.text.string

owned null-terminated string helpers over the allocator

these helpers allocate, copy, and free null-terminated `str` buffers using a
caller-supplied allocator. they live above `std.types.string` (which operates
on borrowed views and does not own storage) because they depend on
`std.allocator`, which itself builds on `std.types.string`.

Source: [`src/text/string.mach`](../../../src/text/string.mach)

| Functions | |
| :--- | :--- |
| [`str_dup`](#str_dup) | allocate an owned, null-terminated copy of `s` |
| [`str_dup_range`](#str_dup_range) | allocate an owned, null-terminated copy of `len` bytes of `source` starting at `offset` |
| [`str_free`](#str_free) | release a string previously returned by str_dup / str_dup_range |

---

## Functions

### str_dup

```mach
pub fun str_dup(a: *Allocator, s: str) res[str, Error]
```

allocate an owned, null-terminated copy of `s`

| Parameter | |
| :--- | :--- |
| `a` | allocator backing the copy |
| `s` | borrowed null-terminated string to copy |
| **returns** | an owned copy (freed via str_free), or the allocator's refusal |

### str_dup_range

```mach
pub fun str_dup_range(a: *Allocator, source: str, offset: usize, len: usize) res[str, Error]
```

allocate an owned, null-terminated copy of `len` bytes of
`source` starting at `offset`.

| Parameter | |
| :--- | :--- |
| `a` | allocator backing the copy |
| `source` | borrowed string to slice from |
| `offset` | starting byte offset into source |
| `len` | number of bytes to copy |
| **returns** | an owned copy (freed via str_free), or the allocator's refusal |

### str_free

```mach
pub fun str_free(a: *Allocator, s: str) err[Error]
```

release a string previously returned by str_dup / str_dup_range

the allocation extent is `str_len + 1`, which is the extent every producer
of a plain owned `str` in std reserves; a string whose extent differs is an
`OwnedString` (std.types.string) and is released through its own record.

| Parameter | |
| :--- | :--- |
| `a` | allocator the string was allocated from |
| `s` | owned string to free (nil is a no-op) |
| **returns** | ok, or the allocator's refusal of the release |

