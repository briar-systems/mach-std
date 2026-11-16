[std](../../README.md) / [io](../README.md) / [file](README.md) / **posix**

# std.io.file.posix

handle-relative file primitives shared by linux, darwin and wasi

Source: [`src/io/file/posix.mach`](../../../../src/io/file/posix.mach)

Uses types from [`std.system.os`](../../system/os.md).

| Functions | |
| :--- | :--- |
| [`confined_name`](#confined_name) | every component is resolved from a pinned directory handle without following links a UTF-8 path already is the native name, so each UTF-8 form is its native form a confined UTF-8 path, which is already its bytes: borrowed by os.native_path |
| [`open_root`](#open_root), [`open_root_native`](#open_root_native), [`open_confined`](#open_confined), [`open_confined_native`](#open_confined_native) | |
| [`rename_confined`](#rename_confined) | rename operates on pinned parents and never follows either leaf |
| [`rename_confined_native`](#rename_confined_native), [`read_at`](#read_at), [`write_at`](#write_at), [`unmap_file`](#unmap_file), [`no_follow_flag`](#no_follow_flag) | |

| Constants | |
| :--- | :--- |
| [`MAX_COMPONENT_BYTES`](#constants) | |

---

## Functions

### confined_name

```mach
pub fun confined_name(path: *u8, out: *std.system.os.NativePath) i64
```

every component is resolved from a pinned directory handle without following links
a UTF-8 path already is the native name, so each UTF-8 form is its native form
a confined UTF-8 path, which is already its bytes: borrowed by os.native_path

### open_root

```mach
pub fun open_root(path: *u8) i64
```

### open_root_native

```mach
pub fun open_root_native(path: *Unit) i64
```

### open_confined

```mach
pub fun open_confined(root: i32, path: *u8, flags: i32, mode: i32) i64
```

### open_confined_native

```mach
pub fun open_confined_native(root: i32, path: *Unit, flags: i32, mode: i32) i64
```

### rename_confined

```mach
pub fun rename_confined(root: i32, source: *u8, destination: *u8) i64
```

rename operates on pinned parents and never follows either leaf

### rename_confined_native

```mach
pub fun rename_confined_native(root: i32, source: *Unit, destination: *Unit) i64
```

### read_at

```mach
pub fun read_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

### write_at

```mach
pub fun write_at(handle: i32, buffer: *u8, length: usize, offset: u64) i64
```

### unmap_file

```mach
pub fun unmap_file(data: ptr, length: usize) i64
```

### no_follow_flag

```mach
pub fun no_follow_flag() i32
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_COMPONENT_BYTES` | `usize` | `255` |  |

