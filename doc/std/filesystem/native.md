[std](../README.md) / [filesystem](README.md) / **native**

# std.filesystem.native

filesystem helpers built on the os contract's stat, unlink and environment

each one reads a per-OS layout or policy the contract does not name, so it
selects the per-OS module the way a filesystem backend does

Source: [`src/filesystem/native.mach`](../../../src/filesystem/native.mach)

Uses types from [`std.system.os`](../system/os.md).

| Functions | |
| :--- | :--- |
| [`stat_mode`](#stat_mode) | the mode word of a stat record: file type and permission bits |
| [`unlink_force`](#unlink_force) | remove a rooted entry without changing read-only attributes on surviving aliases |
| [`unlink_force_native`](#unlink_force_native) | unlink_force for a name in native units, which reach the kernel unchanged |
| [`temp_dir`](#temp_dir) | resolve the directory designated for temporary files |
| [`temp_dir_native`](#temp_dir_native) | temp_dir in native units, under the same truncation contract with cap counted in units |

---

## Functions

### stat_mode

```mach
pub fun stat_mode(st: *std.system.os.stat_t) u32
```

the mode word of a stat record: file type and permission bits

### unlink_force

```mach
pub fun unlink_force(dir: usize, path: *u8, flags: i32) i64
```

remove a rooted entry without changing read-only attributes on surviving aliases

| Parameter | |
| :--- | :--- |
| `dir` | the root handle, never the working directory |
| `path` | the entry below it |
| `flags` | AT_REMOVEDIR for a directory |
| **returns** | zero, or a negative native code |

### unlink_force_native

```mach
pub fun unlink_force_native(dir: usize, name: *Unit, flags: i32) i64
```

unlink_force for a name in native units, which reach the kernel unchanged

| Parameter | |
| :--- | :--- |
| `dir` | the root handle, never the working directory |
| `name` | the nul-terminated entry below it |
| `flags` | AT_REMOVEDIR for a directory |
| **returns** | zero, or a negative native code |

### temp_dir

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

resolve the directory designated for temporary files

follows the env.get truncation contract: ret \< cap means the path was
copied and null-terminated, and ret >= cap signals truncation with ret the
full path length. lookup order is per-OS:
  windows: GetTempPathA, TMP, then TEMP, then USERPROFILE, then the
           windows directory. the result ends with a path separator
  posix:   the $TMPDIR environment variable, falling back to "/tmp"

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer for the path |
| `cap` | buffer capacity in bytes |
| **returns** | full length of the path, or a negative native code |

### temp_dir_native

```mach
pub fun temp_dir_native(buf: *Unit, cap: usize) i64
```

temp_dir in native units, under the same truncation contract with cap
counted in units. on windows the W API's path is reported as it is, so a
directory whose path holds an unpaired surrogate is still found. on linux
and darwin the bytes are the native units and this is temp_dir

