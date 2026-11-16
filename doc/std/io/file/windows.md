[std](../../README.md) / [io](../README.md) / [file](README.md) / **windows**

# std.io.file.windows

handle-relative file primitives for windows

Source: [`src/io/file/windows.mach`](../../../../src/io/file/windows.mach)

Uses types from [`std.system.os`](../../system/os.md).

| Functions | |
| :--- | :--- |
| [`confined_name`](#confined_name) | a confined UTF-8 path converted once, released with os.native_path_dnit |
| [`open_root`](#open_root) | a UTF-8 path is converted once and then takes the native path |
| [`open_root_native`](#open_root_native), [`open_confined`](#open_confined) | |
| [`open_confined_native`](#open_confined_native) | every component is resolved from a pinned directory handle |
| [`rename_confined`](#rename_confined), [`rename_confined_native`](#rename_confined_native), [`read_at`](#read_at), [`write_at`](#write_at), [`unmap_file`](#unmap_file) | |

---

## Functions

### confined_name

```mach
pub fun confined_name(path: *u8, out: *std.system.os.NativePath) i64
```

a confined UTF-8 path converted once, released with os.native_path_dnit

### open_root

```mach
pub fun open_root(path: *u8) i64
```

a UTF-8 path is converted once and then takes the native path

### open_root_native

```mach
pub fun open_root_native(path: *u16) i64
```

### open_confined

```mach
pub fun open_confined(root: i32, path: *u8, flags: i32, mode: i32) i64
```

### open_confined_native

```mach
pub fun open_confined_native(root: i32, path: *u16, flags: i32, mode: i32) i64
```

every component is resolved from a pinned directory handle

### rename_confined

```mach
pub fun rename_confined(root: i32, source: *u8, destination: *u8) i64
```

### rename_confined_native

```mach
pub fun rename_confined_native(root: i32, source: *u16, destination: *u16) i64
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

