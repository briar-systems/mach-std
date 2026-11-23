[std](../README.md) / [types](README.md) / **view**

# std.types.view

a length-counted view over a sub-range of a larger buffer

a View borrows the bytes it points into and owns nothing: constructing and
comparing never allocate or mutate. it names text that ends mid-buffer,
where a null-terminated str cannot exist without copying (a span of source
text, the head of a dotted path, a literal with its quotes stripped).

Source: [`src/types/view.mach`](../../../src/types/view.mach)

| Type | | |
| :--- | :--- | :--- |
| [`View`](#view) | `rec` | a borrowed view over len chars starting at data |

| On `View` | |
| :--- | :--- |
| [`view`](#view-1) | construct a View over `len` chars starting at `data` |
| [`view_eq_str`](#view_eq_str) | compare a view against a null-terminated string for byte equality |
| [`view_index_char`](#view_index_char) | find the first occurrence of a character within the view |
| [`view_contains_char`](#view_contains_char) | check whether the view contains a character |

---

## View

```mach
pub rec View {
    data: *char;
    len:  usize;
}
```

a borrowed view over len chars starting at data

| Field | Type | |
| :--- | :--- | :--- |
| `data` | `*char` | pointer to the first character (not owned) |
| `len` | `usize` | number of characters in the view |

### view

```mach
pub fun view(data: *char, len: usize) View
```

construct a View over `len` chars starting at `data`

| Parameter | |
| :--- | :--- |
| `data` | pointer to the first character |
| `len` | number of characters |
| **returns** | the view |

### view_eq_str

```mach
pub fun view_eq_str(v: View, s: str) bool
```

compare a view against a null-terminated string for byte equality

| Parameter | |
| :--- | :--- |
| `v` | the view |
| `s` | null-terminated string to compare against |
| **returns** | true iff `s` has exactly `v.len` bytes and every byte matches |

### view_index_char

```mach
pub fun view_index_char(v: View, c: char) opt[usize]
```

find the first occurrence of a character within the view

| Parameter | |
| :--- | :--- |
| `v` | the view to search |
| `c` | character to find |
| **returns** | the index of the first occurrence, or none |

### view_contains_char

```mach
pub fun view_contains_char(v: View, c: char) bool
```

check whether the view contains a character

| Parameter | |
| :--- | :--- |
| `v` | the view to search |
| `c` | character to find |
| **returns** | true if c appears within v |

