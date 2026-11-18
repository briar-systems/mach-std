[std](../README.md) / [types](README.md) / **string**

# std.types.string

null-terminated string queries and allocating constructors

nil contract: nil is the empty string throughout. queries and predicates
treat it as "", and constructors produce a fresh empty allocation for it.
constructors fail only on allocation failure or a nil allocator, never on
their string inputs.

Source: [`src/types/string.mach`](../../../src/types/string.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`str`](#str) | `def` | a pointer to a null-terminated sequence of char |
| [`StrError`](#strerror) | `tag` | why an allocating string constructor did not produce a string |
| [`OwnedString`](#ownedstring) | `rec` | a string that owns its storage, with the extent needed to release it |

| On `str` | |
| :--- | :--- |
| [`owned_adopt`](#owned_adopt) | take ownership of a buffer an allocator already served |
| [`owned_dup`](#owned_dup) | an owned copy of a string whose extent is exactly its length plus one |
| [`str_len`](#str_len) | calculate the length of a null-terminated string |
| [`str_is_empty`](#str_is_empty) | check if the string is empty or nil |
| [`str_equals`](#str_equals) | compare two null-terminated strings for equality |
| [`str_region_equals`](#str_region_equals) | compare a region of a string against a pattern |
| [`str_compare`](#str_compare) | compare two null-terminated strings lexically |
| [`str_starts_with`](#str_starts_with) | check if the string starts with the given prefix |
| [`str_ends_with`](#str_ends_with) | check if the string ends with the given suffix |
| [`str_index_of`](#str_index_of) | find the first index of a substring |
| [`str_index_of_from`](#str_index_of_from) | find the first index of a substring at or after a starting offset |
| [`str_last_index_of`](#str_last_index_of) | find the last index of a substring |
| [`str_contains`](#str_contains) | check if the string contains the given substring |
| [`str_find`](#str_find) | find the first occurrence of a substring and return a pointer to it |
| [`str_find_last`](#str_find_last) | find the last occurrence of a substring and return a pointer to it |
| [`str_index_char`](#str_index_char) | find the first occurrence of a character in a string |
| [`str_last_index_char`](#str_last_index_char) | find the last occurrence of a character in a string |
| [`str_contains_char`](#str_contains_char) | check if a string contains a character |
| [`str_find_char`](#str_find_char) | find the first occurrence of a character and return a pointer to it |
| [`str_find_last_char`](#str_find_last_char) | find the last occurrence of a character and return a pointer to it |
| [`str_copy`](#str_copy) | create a copy of a string using the given allocator |
| [`str_copy_slice`](#str_copy_slice) | create a copy of a slice of a string using the given allocator |
| [`str_join`](#str_join) | join any number of strings into one newly allocated string |
| [`str_trim`](#str_trim) | trim leading and trailing whitespace from a string, returning a new allocated string |
| [`str_trim_right`](#str_trim_right) | trim trailing whitespace from a string, returning a new allocated string |
| [`str_trim_left`](#str_trim_left) | trim leading whitespace from a string, returning a new allocated string |
| [`str_to_lower`](#str_to_lower) | lowercase a string (ASCII), returning a new allocated string |
| [`str_to_upper`](#str_to_upper) | uppercase a string (ASCII), returning a new allocated string |
| [`str_repeat`](#str_repeat) | repeat a string n times, returning a new allocated string |
| [`str_replace`](#str_replace) | replace every occurrence of a substring, returning a new allocated string |

| On `OwnedString` | |
| :--- | :--- |
| [`owned_dnit`](#owned_dnit) | release an owned string's extent and leave the record owning nothing |

---

## str

```mach
pub def str: *char
```

a pointer to a null-terminated sequence of char

### owned_adopt

```mach
pub fun owned_adopt(a: *std.allocator.Allocator, data: str, len: usize, extent: usize) OwnedString
```

take ownership of a buffer an allocator already served

`data` must be `extent` bytes served by `a`, null-terminated within its
first `len + 1` bytes. nothing is allocated.

| Parameter | |
| :--- | :--- |
| `a` | the allocator that served data |
| `data` | the buffer to own |
| `len` | the logical length of the text in data |
| `extent` | the byte count a served |
| **returns** | the owning record |

### owned_dup

```mach
pub fun owned_dup(a: *std.allocator.Allocator, s: str) res[OwnedString, std.allocator.Error]
```

an owned copy of a string whose extent is exactly its length plus one

| Parameter | |
| :--- | :--- |
| `a` | allocator for the copy |
| `s` | string to copy (nil copies as empty) |
| **returns** | the owning record, or the allocator's refusal |

### str_len

```mach
pub fun str_len(s: str) usize
```

calculate the length of a null-terminated string

| Parameter | |
| :--- | :--- |
| **returns** | length of the string (not including null terminator) |

### str_is_empty

```mach
pub fun str_is_empty(s: str) bool
```

check if the string is empty or nil

| Parameter | |
| :--- | :--- |
| **returns** | true if the string has zero length or is nil |

### str_equals

```mach
pub fun str_equals(s: str, other: str) bool
```

compare two null-terminated strings for equality

| Parameter | |
| :--- | :--- |
| `other` | the other string to compare against |
| **returns** | true if the strings are equal |

### str_region_equals

```mach
pub fun str_region_equals(s: str, start: usize, len: usize, other: str) bool
```

compare a region of a string against a pattern

| Parameter | |
| :--- | :--- |
| `start` | byte offset into s |
| `len` | number of bytes to compare |
| `other` | null-terminated string to compare against |
| **returns** | true if s[start..start+len] equals other exactly |

### str_compare

```mach
pub fun str_compare(s: str, other: str) i64
```

compare two null-terminated strings lexically

| Parameter | |
| :--- | :--- |
| `other` | the other string to compare against |
| **returns** | \<0 if s \< other, 0 if equal, >0 if s > other |

### str_starts_with

```mach
pub fun str_starts_with(s: str, prefix: str) bool
```

check if the string starts with the given prefix

| Parameter | |
| :--- | :--- |
| `prefix` | the prefix to check |
| **returns** | true if the string starts with prefix |

### str_ends_with

```mach
pub fun str_ends_with(s: str, suffix: str) bool
```

check if the string ends with the given suffix

| Parameter | |
| :--- | :--- |
| `suffix` | the suffix to check |
| **returns** | true if the string ends with suffix |

### str_index_of

```mach
pub fun str_index_of(s: str, sub: str) opt[usize]
```

find the first index of a substring

| Parameter | |
| :--- | :--- |
| `sub` | the substring to find |
| **returns** | the index of the first occurrence, or none. an empty or nil sub matches at 0 |

### str_index_of_from

```mach
pub fun str_index_of_from(s: str, sub: str, from: usize) opt[usize]
```

find the first index of a substring at or after a starting offset

| Parameter | |
| :--- | :--- |
| `sub` | the substring to find |
| `from` | byte offset to begin scanning at |
| **returns** | the index of the first occurrence at or after from, or none. an empty or nil sub matches at from when from is within s |

### str_last_index_of

```mach
pub fun str_last_index_of(s: str, sub: str) opt[usize]
```

find the last index of a substring

| Parameter | |
| :--- | :--- |
| `sub` | the substring to find |
| **returns** | the index of the last occurrence, or none. an empty or nil sub matches at the length of s |

### str_contains

```mach
pub fun str_contains(s: str, sub: str) bool
```

check if the string contains the given substring

| Parameter | |
| :--- | :--- |
| `sub` | the substring to check |
| **returns** | true if the string contains sub. an empty or nil sub is contained in every string, including an empty or nil one |

### str_find

```mach
pub fun str_find(s: str, sub: str) opt[str]
```

find the first occurrence of a substring and return a pointer to it

| Parameter | |
| :--- | :--- |
| `sub` | the substring to find |
| **returns** | pointer into s at the first occurrence, or none. an empty or nil sub yields s itself |

### str_find_last

```mach
pub fun str_find_last(s: str, sub: str) opt[str]
```

find the last occurrence of a substring and return a pointer to it

| Parameter | |
| :--- | :--- |
| `sub` | the substring to find |
| **returns** | pointer into s at the last occurrence, or none. an empty or nil sub yields the empty tail of s |

### str_index_char

```mach
pub fun str_index_char(s: str, c: char) opt[usize]
```

find the first occurrence of a character in a string

| Parameter | |
| :--- | :--- |
| `c` | character to find |
| **returns** | the index of the first occurrence, or none |

### str_last_index_char

```mach
pub fun str_last_index_char(s: str, c: char) opt[usize]
```

find the last occurrence of a character in a string

| Parameter | |
| :--- | :--- |
| `c` | character to find |
| **returns** | the index of the last occurrence, or none |

### str_contains_char

```mach
pub fun str_contains_char(s: str, c: char) bool
```

check if a string contains a character

| Parameter | |
| :--- | :--- |
| `c` | character to find |
| **returns** | true if c appears in s |

### str_find_char

```mach
pub fun str_find_char(s: str, c: char) opt[str]
```

find the first occurrence of a character and return a pointer to it

| Parameter | |
| :--- | :--- |
| `c` | character to find |
| **returns** | pointer into s at the first occurrence, or none |

### str_find_last_char

```mach
pub fun str_find_last_char(s: str, c: char) opt[str]
```

find the last occurrence of a character and return a pointer to it

| Parameter | |
| :--- | :--- |
| `c` | character to find |
| **returns** | pointer into s at the last occurrence, or none |

### str_copy

```mach
pub fun str_copy(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

create a copy of a string using the given allocator

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for the copy |
| `s` | string to copy |
| **returns** | the copied string, or the allocator's refusal |

### str_copy_slice

```mach
pub fun str_copy_slice(a: *std.allocator.Allocator, s: str, start: usize, len: usize) res[str, StrError]
```

create a copy of a slice of a string using the given allocator

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for the copy |
| `s` | string to copy from |
| `start` | starting index of the slice |
| `len` | length of the slice |
| **returns** | the copied slice, `bounds` when the slice does not lie within s, or the allocator's refusal |

### str_join

```mach
pub fun str_join(a: *std.allocator.Allocator, va: ...) res[str, StrError]
```

join any number of strings into one newly allocated string

nil arguments contribute nothing, matching str_len/str_is_empty. a
zero-argument call returns an allocated empty string. every argument
must be a str, enforced at compile time.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `va` | strings to concatenate, in order |
| **returns** | the joined string, the allocator's refusal, or overflow when the total length does not fit usize |

### str_trim

```mach
pub fun str_trim(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

trim leading and trailing whitespace from a string, returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for the new string |
| `s` | string to trim |
| **returns** | the trimmed string, or the allocator's refusal |

### str_trim_right

```mach
pub fun str_trim_right(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

trim trailing whitespace from a string, returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for the new string |
| `s` | string to trim |
| **returns** | the trimmed string, or the allocator's refusal |

### str_trim_left

```mach
pub fun str_trim_left(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

trim leading whitespace from a string, returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator to use for the new string |
| `s` | string to trim |
| **returns** | the trimmed string, or the allocator's refusal |

### str_to_lower

```mach
pub fun str_to_lower(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

lowercase a string (ASCII), returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `s` | string to lowercase |
| **returns** | the lowercased string, or the allocator's refusal |

### str_to_upper

```mach
pub fun str_to_upper(a: *std.allocator.Allocator, s: str) res[str, StrError]
```

uppercase a string (ASCII), returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `s` | string to uppercase |
| **returns** | the uppercased string, or the allocator's refusal |

### str_repeat

```mach
pub fun str_repeat(a: *std.allocator.Allocator, s: str, n: usize) res[str, StrError]
```

repeat a string n times, returning a new allocated string

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `s` | string to repeat |
| `n` | number of repetitions (0 yields an empty string) |
| **returns** | the repeated string, or the allocator's refusal (`overflow` when len * n does not fit) |

### str_replace

```mach
pub fun str_replace(a: *std.allocator.Allocator, s: str, old: str, new: str) res[str, StrError]
```

replace every occurrence of a substring, returning a new allocated string

occurrences are found left to right and do not overlap. a nil or empty
`old` yields a plain copy of `s`.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `s` | string to replace within |
| `old` | substring to replace |
| `new` | replacement substring |
| **returns** | the replaced string, or the allocator's refusal |

## StrError

```mach
pub tag StrError: u8 {
    alloc: std.allocator.Error;
    bounds;
}
```

why an allocating string constructor did not produce a string

the first case is the zero default, so a zero-initialized `res[str, StrError]`
reads as an allocation refusal.

| Case | Payload | |
| :--- | :--- | :--- |
| `alloc` | `std.allocator.Error` | the allocator refused, with its reason |
| `bounds` |  | a slice does not lie within its string |

## OwnedString

```mach
pub rec OwnedString {
    data:   str;
    len:    usize;
    extent: usize;
    a:      *std.allocator.Allocator;
}
```

a string that owns its storage, with the extent needed to release it

a plain owned `str` from this module is released with `str_len + 1` bytes,
because that is what its constructor reserved. a producer whose buffer may
be larger than its final text (an environment value read into a probe, a
path normalized in place) cannot be released by length, so it hands the
caller this record instead. the record holds no pointer to itself and may
be copied into its final storage; exactly one copy is released.

| Field | Type | |
| :--- | :--- | :--- |
| `data` | `str` | the null-terminated text, or nil when nothing is owned |
| `len` | `usize` | the logical length, excluding the terminator |
| `extent` | `usize` | the allocated byte count, at least len + 1 when data is not nil |
| `a` | `*std.allocator.Allocator` | the allocator that owns the extent |

### owned_dnit

```mach
pub fun owned_dnit(o: *OwnedString) err[std.allocator.Error]
```

release an owned string's extent and leave the record owning nothing

releasing a record that owns nothing succeeds. on a refused release the
record is left as it was, still owning the extent.

| Parameter | |
| :--- | :--- |
| `o` | the record to release |
| **returns** | ok, or the allocator's refusal |

