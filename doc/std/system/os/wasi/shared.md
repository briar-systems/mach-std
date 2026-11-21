[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [wasi](README.md) / **shared**

# std.system.os.wasi.shared

what every wasi row shares: the contract's constants, the native codes and
the pages of linear memory, which std.memory.linear keeps

a wasi errno crosses the contract negated, as an errno does on linux and
darwin. the numbers are the ones the interface states, so a native code is the
host's own value. two of them have no contract meaning of their own and read
as the code that does: nosys as ENOTSUP, and notcapable, a path the host holds
outside what the program was given, as EACCES.

Source: [`src/system/os/wasi/shared.mach`](../../../../../src/system/os/wasi/shared.mach)

| Functions | |
| :--- | :--- |
| [`code`](#code) | the contract's code for what the host returned |
| [`error_message`](#error_message) | the native text for a negative code |
| [`deallocate`](#deallocate) | keep pages for the next allocate, merged with their neighbours |
| [`map_alignment`](#map_alignment) | the alignment map_file requires of an offset, the wasm page size |
| [`map_secret`](#map_secret) | storage for span bytes between two pages, which cannot be guarded or locked here |
| [`protect`](#protect) | linear memory has one protection, every page readable and writable |
| [`lock`](#lock) | linear memory cannot be locked, so locking a region always fails |
| [`unlock`](#unlock) | linear memory cannot be locked, so unlocking a region always fails |
| [`advise`](#advise) | linear memory takes no access advice, so advising always fails |

| Constants | |
| :--- | :--- |
| [`separator`](#constants), [`STDIN_FD`](#constants), [`STDOUT_FD`](#constants), [`STDERR_FD`](#constants), [`O_RDONLY`](#constants), [`O_WRONLY`](#constants), [`O_RDWR`](#constants), [`O_CREAT`](#constants), [`O_EXCL`](#constants), [`O_TRUNC`](#constants), [`O_APPEND`](#constants), [`O_NONBLOCK`](#constants), [`O_DIRECTORY`](#constants), [`O_NOFOLLOW`](#constants) | |
| [`AT_FDCWD`](#constants) | the preview has no working directory, so this names the root the preopens hang off |
| [`AT_SYMLINK_NOFOLLOW`](#constants), [`AT_REMOVEDIR`](#constants), [`LOCK_SH`](#constants), [`LOCK_EX`](#constants), [`LOCK_NB`](#constants), [`LOCK_UN`](#constants), [`S_IFMT`](#constants), [`S_IFDIR`](#constants), [`S_IFREG`](#constants), [`S_IFLNK`](#constants), [`WNOHANG`](#constants), [`WUNTRACED`](#constants), [`WCONTINUED`](#constants), [`CLOCK_REALTIME`](#constants), [`CLOCK_MONOTONIC`](#constants), [`E2BIG`](#constants), [`EACCES`](#constants), [`EADDRINUSE`](#constants), [`EAGAIN`](#constants), [`EBADF`](#constants), [`EBUSY`](#constants), [`ECANCELED`](#constants), [`ECHILD`](#constants), [`ECONNABORTED`](#constants), [`ECONNREFUSED`](#constants), [`ECONNRESET`](#constants), [`EEXIST`](#constants), [`EFAULT`](#constants), [`EHOSTUNREACH`](#constants), [`EINTR`](#constants), [`EINVAL`](#constants), [`EIO`](#constants), [`EISDIR`](#constants), [`ELOOP`](#constants), [`EMFILE`](#constants), [`ENAMETOOLONG`](#constants), [`ENETUNREACH`](#constants), [`ENFILE`](#constants), [`ENODEV`](#constants), [`ENOENT`](#constants), [`ENOMEM`](#constants), [`ENOSPC`](#constants), [`ENOSYS`](#constants), [`ENOTCONN`](#constants), [`ENOTDIR`](#constants), [`ENOTEMPTY`](#constants), [`ENOTSUP`](#constants), [`ENXIO`](#constants), [`EPERM`](#constants), [`EPIPE`](#constants), [`ERANGE`](#constants), [`EROFS`](#constants), [`ESRCH`](#constants), [`ETIMEDOUT`](#constants), [`ETXTBSY`](#constants), [`ENOTCAPABLE`](#constants) | |

| Forwards | |
| :--- | :--- |
| [`allocate`](#allocate), [`reallocate`](#reallocate), [`page_size`](#page_size), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend) | |

---

## Functions

### code

```mach
pub fun code(errno: i32) i64
```

the contract's code for what the host returned

| Parameter | |
| :--- | :--- |
| `errno` | the host's errno, zero for success |
| **returns** | zero, or the negative native code |

### error_message

```mach
pub fun error_message(code: i64) str
```

the native text for a negative code

### deallocate

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

keep pages for the next allocate, merged with their neighbours

| Parameter | |
| :--- | :--- |
| `p` | the pages, on a page boundary |
| `size` | their size in bytes |
| **returns** | 0, or EINVAL for an address off a page |

### map_alignment

```mach
pub fun map_alignment() usize
```

the alignment map_file requires of an offset, the wasm page size

### map_secret

```mach
pub fun map_secret(span: usize, page: usize, data: *ptr, locking: *bool) i64
```

storage for span bytes between two pages, which cannot be guarded or locked
here. the storage comes from allocate, so it is zero filled and has no typed
alias: std.system.os.secret welds it to its type as every host's mapping is

| Parameter | |
| :--- | :--- |
| `span` | usable bytes, whole pages of the caller's |
| `page` | the caller's page, which divides the wasm page |
| `data` | receives the usable bytes, one page past the start |
| `locking` | left false, since no step here locks |
| **returns** | 0, or ENOMEM |

### protect

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

linear memory has one protection, every page readable and writable

### lock

```mach
pub fun lock(p: ptr, size: usize) i64
```

linear memory cannot be locked, so locking a region always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### unlock

```mach
pub fun unlock(p: ptr, size: usize) i64
```

linear memory cannot be locked, so unlocking a region always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### advise

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

linear memory takes no access advice, so advising always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `separator` | `u8` | `'/'` |  |
| `STDIN_FD` | `i32` | `0` |  |
| `STDOUT_FD` | `i32` | `1` |  |
| `STDERR_FD` | `i32` | `2` |  |
| `O_RDONLY` | `i32` | `0` |  |
| `O_WRONLY` | `i32` | `1` |  |
| `O_RDWR` | `i32` | `2` |  |
| `O_CREAT` | `i32` | `64` |  |
| `O_EXCL` | `i32` | `128` |  |
| `O_TRUNC` | `i32` | `512` |  |
| `O_APPEND` | `i32` | `1024` |  |
| `O_NONBLOCK` | `i32` | `0o4000` |  |
| `O_DIRECTORY` | `i32` | `0o200000` |  |
| `O_NOFOLLOW` | `i32` | `0o400000` |  |
| `AT_FDCWD` | `i32` | `-100` | the preview has no working directory, so this names the root the preopens hang off |
| `AT_SYMLINK_NOFOLLOW` | `i32` | `0x100` |  |
| `AT_REMOVEDIR` | `i32` | `0x200` |  |
| `LOCK_SH` | `i32` | `1` |  |
| `LOCK_EX` | `i32` | `2` |  |
| `LOCK_NB` | `i32` | `4` |  |
| `LOCK_UN` | `i32` | `8` |  |
| `S_IFMT` | `u32` | `0o170000` |  |
| `S_IFDIR` | `u32` | `0o040000` |  |
| `S_IFREG` | `u32` | `0o100000` |  |
| `S_IFLNK` | `u32` | `0o120000` |  |
| `WNOHANG` | `i32` | `1` |  |
| `WUNTRACED` | `i32` | `2` |  |
| `WCONTINUED` | `i32` | `8` |  |
| `CLOCK_REALTIME` | `i32` | `0` |  |
| `CLOCK_MONOTONIC` | `i32` | `1` |  |
| `E2BIG` | `i64` | `-1` |  |
| `EACCES` | `i64` | `-2` |  |
| `EADDRINUSE` | `i64` | `-3` |  |
| `EAGAIN` | `i64` | `-6` |  |
| `EBADF` | `i64` | `-8` |  |
| `EBUSY` | `i64` | `-10` |  |
| `ECANCELED` | `i64` | `-11` |  |
| `ECHILD` | `i64` | `-12` |  |
| `ECONNABORTED` | `i64` | `-13` |  |
| `ECONNREFUSED` | `i64` | `-14` |  |
| `ECONNRESET` | `i64` | `-15` |  |
| `EEXIST` | `i64` | `-20` |  |
| `EFAULT` | `i64` | `-21` |  |
| `EHOSTUNREACH` | `i64` | `-23` |  |
| `EINTR` | `i64` | `-27` |  |
| `EINVAL` | `i64` | `-28` |  |
| `EIO` | `i64` | `-29` |  |
| `EISDIR` | `i64` | `-31` |  |
| `ELOOP` | `i64` | `-32` |  |
| `EMFILE` | `i64` | `-33` |  |
| `ENAMETOOLONG` | `i64` | `-37` |  |
| `ENETUNREACH` | `i64` | `-40` |  |
| `ENFILE` | `i64` | `-41` |  |
| `ENODEV` | `i64` | `-43` |  |
| `ENOENT` | `i64` | `-44` |  |
| `ENOMEM` | `i64` | `-48` |  |
| `ENOSPC` | `i64` | `-51` |  |
| `ENOSYS` | `i64` | `-52` |  |
| `ENOTCONN` | `i64` | `-53` |  |
| `ENOTDIR` | `i64` | `-54` |  |
| `ENOTEMPTY` | `i64` | `-55` |  |
| `ENOTSUP` | `i64` | `-58` |  |
| `ENXIO` | `i64` | `-60` |  |
| `EPERM` | `i64` | `-63` |  |
| `EPIPE` | `i64` | `-64` |  |
| `ERANGE` | `i64` | `-68` |  |
| `EROFS` | `i64` | `-69` |  |
| `ESRCH` | `i64` | `-71` |  |
| `ETIMEDOUT` | `i64` | `-73` |  |
| `ETXTBSY` | `i64` | `-74` |  |
| `ENOTCAPABLE` | `i64` | `-76` |  |

## Forwards

### allocate

Forwards [`std.memory.linear.allocate`](../../../memory/linear.md#allocate).

```mach
pub fun allocate(size: usize) ptr
```

whole zero-filled pages, kept ones first

### reallocate

Forwards [`std.memory.linear.reallocate`](../../../memory/linear.md#reallocate).

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a page allocation, in place when its pages still hold it

### page_size

Forwards [`std.memory.linear.page_size`](../../../memory/linear.md#page_size).

```mach
pub fun page_size() usize
```

the wasm page size, 64 KiB, which every allocation here is counted in

### heap_region_base

Forwards [`std.memory.linear.heap_region_base`](../../../memory/linear.md#heap_region_base).

```mach
pub fun heap_region_base() usize
```

the first address past what has been handed out

### heap_region_extend

Forwards [`std.memory.linear.heap_region_extend`](../../../memory/linear.md#heap_region_extend).

```mach
pub fun heap_region_extend(addr: usize) usize
```

move the region's end up to addr

the region is contiguous: it takes kept pages that start where it ends, then
new memory once it reaches the end of linear memory, so it stops growing
while pages `allocate` handed out lie past it

