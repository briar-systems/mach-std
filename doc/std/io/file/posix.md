[std](../../README.md) / [io](../README.md) / [file](README.md) / **posix**

# std.io.file.posix

handle-relative file primitives shared by linux, darwin and wasi

Source: [`src/io/file/posix.mach`](../../../../src/io/file/posix.mach)

Uses types from [`std.system.os`](../../system/os.md).

| Functions | |
| :--- | :--- |
| [`confined_name`](#confined_name) | a UTF-8 path already is the native name, so each UTF-8 form is its native form a confined UTF-8 path, which is already its bytes: borrowed by os.native_path |
| [`open_root`](#open_root) | opens a directory as a confinement root, without following a final link |
| [`open_root_native`](#open_root_native) | open_root for a directory named in native units |
| [`open_confined`](#open_confined) | open_confined_native for a UTF-8 path |
| [`open_confined_native`](#open_confined_native) | opens a relative path beneath a root, one component at a time |
| [`rename_confined_native`](#rename_confined_native) | rename operates on pinned parents and never follows either leaf |
| [`read_at`](#read_at) | reads at an offset without moving the descriptor's position |
| [`write_at`](#write_at) | writes at an offset without moving the descriptor's position |
| [`unmap_file`](#unmap_file) | releases a file mapping |

| Constants | |
| :--- | :--- |
| [`MAX_COMPONENT_BYTES`](#constants) | |

---

## Functions

### confined_name

```mach
pub fun confined_name(path: *u8, out: *std.system.os.NativePath) i64
```

a UTF-8 path already is the native name, so each UTF-8 form is its native form
a confined UTF-8 path, which is already its bytes: borrowed by os.native_path

| Parameter | |
| :--- | :--- |
| `path` | the confined UTF-8 path |
| `out` | receives the native name, which borrows path |
| **returns** | what os.native_path returns, negative errno on failure |

### open_root

```mach
pub fun open_root(path: *u8) i64
```

opens a directory as a confinement root, without following a final link

| Parameter | |
| :--- | :--- |
| `path` | the directory, as a UTF-8 path |
| **returns** | the directory descriptor, or negative errno |

### open_root_native

```mach
pub fun open_root_native(path: *Unit) i64
```

open_root for a directory named in native units

| Parameter | |
| :--- | :--- |
| `path` | the directory in native units |
| **returns** | the directory descriptor, or negative errno, EINVAL for a nil or empty path |

### open_confined

```mach
pub fun open_confined(root: i32, path: *u8, flags: i32, mode: i32) i64
```

open_confined_native for a UTF-8 path

| Parameter | |
| :--- | :--- |
| `root` | the root directory descriptor |
| `path` | the relative UTF-8 path |
| `flags` | open flags for the final component |
| `mode` | permission bits when the final component is created |
| **returns** | the opened descriptor, or negative errno |

### open_confined_native

```mach
pub fun open_confined_native(root: i32, path: *Unit, flags: i32, mode: i32) i64
```

opens a relative path beneath a root, one component at a time

every component is resolved from a pinned directory handle without following links.
an empty, absolute, "." or ".." component, or one longer than
MAX_COMPONENT_BYTES, is refused

| Parameter | |
| :--- | :--- |
| `root` | the root directory descriptor |
| `path` | the relative path in native units |
| `flags` | open flags for the final component, O_NOFOLLOW is always added |
| `mode` | permission bits when the final component is created |
| **returns** | the opened descriptor, owned by the caller, or negative errno |

### rename_confined_native

```mach
pub fun rename_confined_native(root: i32, source: *Unit, destination: *Unit) i64
```

rename operates on pinned parents and never follows either leaf

### read_at

```mach
pub fun read_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

reads at an offset without moving the descriptor's position

| Parameter | |
| :--- | :--- |
| `handle` | the file descriptor |
| `buffer` | receives the bytes |
| `length` | the most bytes to read |
| `offset` | the file offset to read from |
| **returns** | bytes read, 0 at end of file, or negative errno |

### write_at

```mach
pub fun write_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

writes at an offset without moving the descriptor's position

| Parameter | |
| :--- | :--- |
| `handle` | the file descriptor |
| `buffer` | the bytes to write |
| `length` | the number of bytes to write |
| `offset` | the file offset to write at |
| **returns** | bytes written, or negative errno |

### unmap_file

```mach
pub fun unmap_file(data: ptr, length: usize) i64
```

releases a file mapping

| Parameter | |
| :--- | :--- |
| `data` | the mapped region |
| `length` | its length in bytes |
| **returns** | 0 on success, or negative errno |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_COMPONENT_BYTES` | `usize` | `255` |  |

