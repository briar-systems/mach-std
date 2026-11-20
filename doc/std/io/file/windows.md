[std](../../README.md) / [io](../README.md) / [file](README.md) / **windows**

# std.io.file.windows

handle-relative file primitives for windows

Source: [`src/io/file/windows.mach`](../../../../src/io/file/windows.mach)

Uses types from [`std.system.os`](../../system/os.md).

| Functions | |
| :--- | :--- |
| [`confined_name`](#confined_name) | a confined UTF-8 path converted once, released with os.native_path_dnit |
| [`open_root`](#open_root) | a UTF-8 path is converted once and then takes the native path |
| [`open_root_native`](#open_root_native) | opens a directory named in native units as a confinement root |
| [`open_confined`](#open_confined) | open_confined_native for a UTF-8 path, converted once |
| [`open_confined_native`](#open_confined_native) | every component is resolved from a pinned directory handle |
| [`rename_confined_native`](#rename_confined_native) | |
| [`read_at`](#read_at) | reads at an offset |
| [`write_at`](#write_at) | writes at an offset |
| [`unmap_file`](#unmap_file) | releases a file mapping |

---

## Functions

### confined_name

```mach
pub fun confined_name(path: *u8, out: *std.system.os.NativePath) i64
```

a confined UTF-8 path converted once, released with os.native_path_dnit

| Parameter | |
| :--- | :--- |
| `path` | the confined UTF-8 path |
| `out` | receives the converted name, owned by the caller |
| **returns** | 0 on success, or a negative native error code |

### open_root

```mach
pub fun open_root(path: *u8) i64
```

a UTF-8 path is converted once and then takes the native path

| Parameter | |
| :--- | :--- |
| `path` | the directory, as a UTF-8 path |
| **returns** | the directory handle, or a negative native error code, EINVAL for a nil or empty path |

### open_root_native

```mach
pub fun open_root_native(path: *u16) i64
```

opens a directory named in native units as a confinement root

| Parameter | |
| :--- | :--- |
| `path` | the directory in UTF-16 units |
| **returns** | the directory handle, or a negative native error code, EINVAL for a nil or empty path |

### open_confined

```mach
pub fun open_confined(root: i32, path: *u8, flags: i32, mode: i32) i64
```

open_confined_native for a UTF-8 path, converted once

| Parameter | |
| :--- | :--- |
| `root` | the root directory handle |
| `path` | the relative UTF-8 path |
| `flags` | open flags for the final component |
| `mode` | permission bits when the final component is created |
| **returns** | the opened handle, or a negative native error code |

### open_confined_native

```mach
pub fun open_confined_native(root: i32, path: *u16, flags: i32, mode: i32) i64
```

every component is resolved from a pinned directory handle

| Parameter | |
| :--- | :--- |
| `root` | the root directory handle |
| `path` | the relative path in UTF-16 units, split at either slash |
| `flags` | open flags for the final component |
| `mode` | permission bits when the final component is created |
| **returns** | the opened handle, owned by the caller, or a negative native error code, EINVAL for a path that starts with a slash or an empty, "." or ".." component |

### rename_confined_native

```mach
pub fun rename_confined_native(root: i32, source: *u16, destination: *u16) i64
```

### read_at

```mach
pub fun read_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

reads at an offset

| Parameter | |
| :--- | :--- |
| `handle` | the file handle |
| `buffer` | receives the bytes |
| `length` | the most bytes to read |
| `offset` | the file offset to read from |
| **returns** | bytes read, 0 at end of file, or a negative native error code |

### write_at

```mach
pub fun write_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

writes at an offset

| Parameter | |
| :--- | :--- |
| `handle` | the file handle |
| `buffer` | the bytes to write |
| `length` | the number of bytes to write |
| `offset` | the file offset to write at |
| **returns** | bytes written, or a negative native error code |

### unmap_file

```mach
pub fun unmap_file(data: ptr, length: usize) i64
```

releases a file mapping

| Parameter | |
| :--- | :--- |
| `data` | the mapped view |
| `length` | its length in bytes |
| **returns** | 0 on success, or a negative native error code |

