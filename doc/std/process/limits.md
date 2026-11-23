[std](../README.md) / [process](README.md) / **limits**

# std.process.limits

per-process resource limits

the open-file limit bounds how many descriptors a process may hold, so a
server that expects many connections raises it at startup. the limit itself
is read and set through the os contract; this module holds no OS knowledge

Source: [`src/process/limits.mach`](../../../src/process/limits.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.system.os`](../system/os.md).

| Functions | |
| :--- | :--- |
| [`open_files`](#open_files) | read the open-file limit |
| [`set_open_files`](#set_open_files) | set the open-file limit |
| [`raise_open_files`](#raise_open_files) | raise the soft open-file limit as far as this process may, leaving the hard limit unchanged |

| Forwards | |
| :--- | :--- |
| [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited) | |

---

## Functions

### open_files

```mach
pub fun open_files() res[std.system.os.FileLimit, std.io.error.Error]
```

read the open-file limit

| Parameter | |
| :--- | :--- |
| **returns** | the soft limit in force, the hard limit, and the highest soft limit this process may set, or the failure. UNSUPPORTED where the platform has no such limit |

### set_open_files

```mach
pub fun set_open_files(limit: std.system.os.FileLimit) err[std.io.error.Error]
```

set the open-file limit

a soft limit above the hard one is INVALID, and raising the hard limit
without privilege is PERMISSION. the record's ceiling is ignored

| Parameter | |
| :--- | :--- |
| `limit` | the soft and hard limits to set |
| **returns** | success, or the failure |

### raise_open_files

```mach
pub fun raise_open_files() res[std.system.os.FileLimit, std.io.error.Error]
```

raise the soft open-file limit as far as this process may, leaving the hard
limit unchanged

| Parameter | |
| :--- | :--- |
| **returns** | the limit now in force, or the failure |

## Forwards

### FileLimit

Forwards [`std.system.os.FileLimit`](../system/os.md#filelimit).

```mach
pub rec FileLimit {
    soft:    u64;
    hard:    u64;
    ceiling: u64;
}
```

the open-file limit. soft is the limit in force, hard its ceiling for an
unprivileged raise, and ceiling the highest soft value this process may set,
which the implementation fills and a set ignores

### LIMIT_UNLIMITED

Forwards [`std.system.os.LIMIT_UNLIMITED`](../system/os.md#limit_unlimited).

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

