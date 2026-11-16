[std](../README.md) / [types](README.md) / **path**

# std.types.path

path manipulation helpers

Path is a type alias for str. functions that return new paths allocate
through the caller-provided Allocator. functions that return views into
existing paths (filename, extension) return pointers into the input and
do not allocate.

separator contract: parsing accepts any platform separator. on windows
both '/' and '\\' separate components (matching the Win32 file APIs); on
posix only '/' separates ('\\' is a legal filename byte). construction
(join, separator) emits the platform-preferred separator, and stored
paths are never normalized.

windows absolute roots: drive-letter roots ('C:\\', 'C:/') and UNC roots
('\\\\server\\share') are recognized as absolute, and filename/parent/is_root
never split inside them. a bare drive reference 'C:' (or 'C:foo') is
drive-relative: it is a root unit (its own parent, empty filename) but is
NOT absolute, matching Win32 where 'C:foo' resolves against the current
directory on drive C. a UNC '\\\\server\\share' is one indivisible root unit
(a bare '\\\\server' is not a usable path and is likewise treated as a whole
root). join does no drive-relative special-casing: join("C:", "foo")
inserts a separator yielding "C:\\foo".

nil contract: a nil Path means "no path". predicates answer false for nil,
views return nil, and clone/stem propagate nil as ok(nil) rather than
allocating an empty path.

Source: [`src/types/path.mach`](../../../src/types/path.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.types.view`](view.md).

| Type | | |
| :--- | :--- | :--- |
| [`Path`](#path) | `def` | a null-terminated filesystem path |

| On `Path` | |
| :--- | :--- |
| [`root`](#root) | borrow the indivisible root prefix without changing its spelling unanchored relative, empty and nil paths have zero length drive-relative paths expose their drive anchor and every view retains p separator-only paths expose one separator rather than an empty UNC share |
| [`has_separator`](#has_separator) | check whether p contains any path separator |
| [`is_empty`](#is_empty) | check whether a path is empty or nil |
| [`is_abs`](#is_abs) | check whether a path is absolute |
| [`is_root`](#is_root) | check whether a path is a root unit |
| [`seg_count`](#seg_count) | count the net directory depth of a path |
| [`filename`](#filename) | return the final component of a path |
| [`extension`](#extension) | return the file extension without the leading dot |
| [`stem`](#stem) | return the filename without its extension |
| [`clone`](#clone) | duplicate a path using the provided allocator |
| [`join`](#join) | join two path segments with the platform separator |
| [`parent`](#parent) | return the parent directory of a path |
| [`resolve`](#resolve) | resolve p against base: an absolute p is cloned verbatim, a relative p is joined onto base |
| [`clean`](#clean) | lexically normalize a path: collapse `.`, resolve safe `..`, and squash separator runs, without touching the filesystem (mach#2998, mach-lsp#141) |

| Functions | |
| :--- | :--- |
| [`separator`](#separator) | platform path separator character, emitted by construction |
| [`is_separator`](#is_separator) | check whether c separates path components on the target |
| [`native_len`](#native_len) | the same rules over a name in std.runtime.native units, for the native filesystem calls |
| [`native_is_empty`](#native_is_empty), [`native_is_root`](#native_is_root), [`native_is_separator`](#native_is_separator) | |
| [`native_root_len`](#native_root_len) | the length of root's prefix, in units |
| [`native_clone`](#native_clone) | |
| [`unit_is_separator`](#unit_is_separator) | the separator rules for a caller that is itself generic over the unit |
| [`unit_separator`](#unit_separator), [`native_filename`](#native_filename), [`native_parent`](#native_parent), [`native_join`](#native_join) | |

---

## Path

```mach
pub def Path: str
```

a null-terminated filesystem path

### root

```mach
pub fun root(p: Path) std.types.view.View
```

borrow the indivisible root prefix without changing its spelling
unanchored relative, empty and nil paths have zero length
drive-relative paths expose their drive anchor and every view retains p
separator-only paths expose one separator rather than an empty UNC share

### has_separator

```mach
pub fun has_separator(p: Path) bool
```

check whether p contains any path separator

| Parameter | |
| :--- | :--- |
| **returns** | true when at least one byte of p separates components |

### is_empty

```mach
pub fun is_empty(p: Path) bool
```

check whether a path is empty or nil

| Parameter | |
| :--- | :--- |
| **returns** | true if the path is nil or zero-length |

### is_abs

```mach
pub fun is_abs(p: Path) bool
```

check whether a path is absolute

a path is absolute when it begins with a separator (a posix or UNC root)
or, on windows, with a drive-letter root 'X:\\' / 'X:/'. a bare drive
reference 'C:' or 'C:foo' is drive-relative and is not absolute.

| Parameter | |
| :--- | :--- |
| **returns** | true when p is absolute |

### is_root

```mach
pub fun is_root(p: Path) bool
```

check whether a path is a root unit

true when p is only separators, or (on windows) exactly a drive or UNC
root followed by any trailing separators.

| Parameter | |
| :--- | :--- |
| **returns** | true when p is exactly a root unit |

### seg_count

```mach
pub fun seg_count(p: Path) usize
```

count the net directory depth of a path

walks p's is_separator-delimited segments: a real segment adds one level, a
'.' segment contributes nothing, and a '..' segment climbs one level, clamped
so the depth never falls below zero. empty runs (leading, trailing, or
repeated separators) contribute nothing. the result is how far p descends
below its anchor - the count of '..' needed to climb from p back to that
anchor - which is why '..' decrements and the floor holds a relative climb at
the root.

| Parameter | |
| :--- | :--- |
| `p` | path to measure |
| **returns** | the net segment depth, zero for a nil, empty, root, or fully-climbing path |

### filename

```mach
pub fun filename(p: Path) str
```

return the final component of a path

returns a pointer into p (no allocation). returns nil for empty paths
and empty string for paths ending in a separator.

| Parameter | |
| :--- | :--- |
| `p` | path to extract filename from |
| **returns** | pointer into p at the filename, or nil |

### extension

```mach
pub fun extension(p: Path) str
```

return the file extension without the leading dot

returns a pointer into p (no allocation). returns nil if there is no
extension (no dot, or dot is first char of filename).

| Parameter | |
| :--- | :--- |
| `p` | path to extract extension from |
| **returns** | pointer into p at the extension, or nil |

### stem

```mach
pub fun stem(a: *std.allocator.Allocator, p: Path) res[Path, std.allocator.Error]
```

return the filename without its extension

"foo/bar.txt" → "bar", "foo/.hidden" → ".hidden", "foo/bar" → "bar"

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `p` | path to extract stem from |
| **returns** | the stem, or the allocator's refusal |

### clone

```mach
pub fun clone(a: *std.allocator.Allocator, p: Path) res[Path, std.allocator.Error]
```

duplicate a path using the provided allocator

| Parameter | |
| :--- | :--- |
| `a` | allocator for the new path |
| `p` | path to clone (nil returns nil) |
| **returns** | the cloned path, or the allocator's refusal |

### join

```mach
pub fun join(a: *std.allocator.Allocator, left: Path, right: Path) res[Path, std.allocator.Error]
```

join two path segments with the platform separator

| Parameter | |
| :--- | :--- |
| `a` | allocator for the resulting path |
| `left` | left path segment |
| `right` | right path segment |
| **returns** | the joined path, or the allocator's refusal |

### parent

```mach
pub fun parent(a: *std.allocator.Allocator, p: Path) res[Path, std.allocator.Error]
```

return the parent directory of a path

| Parameter | |
| :--- | :--- |
| `a` | allocator for the resulting path |
| `p` | path to get parent of |
| **returns** | the parent path, or the allocator's refusal |

### resolve

```mach
pub fun resolve(a: *std.allocator.Allocator, base: Path, p: Path) res[Path, std.allocator.Error]
```

resolve p against base: an absolute p is cloned verbatim, a relative p is
joined onto base

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `base` | base directory for a relative p |
| `p` | path to resolve |
| **returns** | the resolved path, or the allocator's refusal |

### clean

```mach
pub fun clean(a: *std.allocator.Allocator, p: Path) res[Path, std.allocator.Error]
```

lexically normalize a path: collapse `.`, resolve safe `..`, and squash
separator runs, without touching the filesystem (mach#2998, mach-lsp#141)

PURELY LEXICAL, and that is the contract rather than a limitation. No `stat`, no
symlink resolution, no current-directory lookup - two spellings that clean to the
same bytes name the same path *as written*, which is exactly the identity an editor
overlay needs: the compiler composes `<root>/./src/f.mach` from a manifest's
`src = "./src"` while the editor supplies `<root>/src/f.mach`, and the buffer is
missed unless those two compare equal. Resolving symlinks would be a different
(and I/O-bearing) question.

THE ROOT IS PRESERVED, NEVER CLIMBED THROUGH. `root_len` already knows what a root
is on this target - a POSIX `/`, a drive `C:\`, a UNC `\\server\share` - so a `..`
that would escape one is dropped, the way every real path resolver behaves. A
RELATIVE path keeps its leading `..` segments, because there is nothing above it to
cancel them against yet; `../a/../b` cleans to `../b`, not `b`.

SEPARATORS COME OUT NATIVE, and go in either way on windows. `is_separator` accepts
both `/` and `\` there, which is what lets a compiler-produced forward-slash
spelling and an editor's backslash one meet; the output uses `separator()` so the
result is one canonical spelling rather than whichever the caller happened to pass.

EMBEDDED NUL IS NOT REPRESENTABLE. `Path` is a null-terminated `str`, so a path ends
at its first NUL by construction and there is nothing to reject - stated here
because the question is a real one for a byte-oriented normalizer and the answer is
a property of the type rather than of this function.

An empty result is spelled `.`, so the return is always a usable path.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the returned path |
| `p` | the path to normalize |
| **returns** | the cleaned path, or the allocator's refusal |

## Functions

### separator

```mach
pub fun separator() u8
```

platform path separator character, emitted by construction

| Parameter | |
| :--- | :--- |
| **returns** | the preferred separator byte for the target |

### is_separator

```mach
pub fun is_separator(c: u8) bool
```

check whether c separates path components on the target

windows accepts both '/' and '\\'; posix treats only '/' as a separator.

| Parameter | |
| :--- | :--- |
| `c` | byte to test |
| **returns** | true when c is a separator |

### native_len

```mach
pub fun native_len(p: *Unit) usize
```

the same rules over a name in std.runtime.native units, for the native
filesystem calls. each result is a nul-terminated native name, allocated
like its Path counterpart's

### native_is_empty

```mach
pub fun native_is_empty(p: *Unit) bool
```

### native_is_root

```mach
pub fun native_is_root(p: *Unit) bool
```

### native_is_separator

```mach
pub fun native_is_separator(c: Unit) bool
```

### native_root_len

```mach
pub fun native_root_len(p: *Unit) usize
```

the length of root's prefix, in units

### native_clone

```mach
pub fun native_clone(a: *std.allocator.Allocator, p: *Unit) res[*Unit, std.allocator.Error]
```

### unit_is_separator

```mach
pub fun unit_is_separator[T](c: T) bool
```

the separator rules for a caller that is itself generic over the unit

### unit_separator

```mach
pub fun unit_separator[T]() T
```

### native_filename

```mach
pub fun native_filename(p: *Unit) *Unit
```

### native_parent

```mach
pub fun native_parent(a: *std.allocator.Allocator, p: *Unit) res[*Unit, std.allocator.Error]
```

### native_join

```mach
pub fun native_join(a: *std.allocator.Allocator, left: *Unit, right: *Unit) res[*Unit, std.allocator.Error]
```

