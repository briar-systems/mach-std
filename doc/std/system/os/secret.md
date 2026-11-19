[std](../../README.md) / [system](../README.md) / [os](README.md) / **secret**

# std.system.os.secret

native primitives for secret-welded storage

each primitive keeps the welded pointer shape across the native boundary.
wiping, retrying, chunking and typed geometry are built on top of these in
std.memory.secret. a negative return is a native code.

every allocation is span usable bytes, the request rounded up to whole pages,
between two inaccessible guard pages, so a run off either end faults. the
span is locked against paging and, where the host can say so, kept out of
core dumps:

  linux    memfd_secret, which also removes the pages from the kernel's
           direct map, or on a kernel without it an anonymous mapping with
           mlock and MADV_DONTDUMP
  darwin   mmap and mlock. xnu has no per-mapping dump exclusion
  windows  VirtualAlloc and VirtualLock, the guards reserved and never
           committed. windows has no per-allocation dump exclusion
  wasi     fresh zeroed pages from the linear-memory heap, which can be
           neither guarded nor locked (LOCKS is false)

a host that refuses the lock (RLIMIT_MEMLOCK, the windows minimum working
set) fails the allocation with Status.lock set. nothing is ever handed out
unlocked on a host whose LOCKS is true.

Source: [`src/system/os/secret.mach`](../../../../src/system/os/secret.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Status`](#status) | `rec` | how an allocation ended |

| On `Status` | |
| :--- | :--- |
| [`allocate`](#allocate) | allocate one zero-initialized secret-welded byte region |
| [`allocate_typed`](#allocate_typed) | allocate a zero-initialized region of total bytes typed as T, without changing T's secrecy shape |

| Functions | |
| :--- | :--- |
| [`free`](#free) | release a region allocate returned, without wiping it |
| [`free_typed`](#free_typed) | release a region allocate_typed returned, without wiping it |
| [`random_fill`](#random_fill) | fill part of a region from the operating-system csprng in one native call |
| [`read_at`](#read_at) | one positioned read into welded storage: the kernel writes it through this call and nothing else |
| [`write_at`](#write_at) | one positioned write from welded storage: the kernel reads it through this call and nothing else |

| Constants | |
| :--- | :--- |
| [`ALIGN`](#constants) | the alignment every allocation starts on: the smallest page size any host has |
| [`LOCKS`](#constants) | every host std reaches locks secret pages |
| [`RANDOM_FILL_MAX`](#constants) | the most bytes one random_fill call accepts |

---

## Status

```mach
pub rec Status {
    code: i64;
    lock: bool;
}
```

how an allocation ended

| Field | Type | |
| :--- | :--- | :--- |
| `code` | `i64` | zero, or the negative native code of the step that failed |
| `lock` | `bool` | whether that step was the host refusing to lock the pages |

### allocate

```mach
pub fun allocate(size: usize, out: **^u8) Status
```

allocate one zero-initialized secret-welded byte region

| Parameter | |
| :--- | :--- |
| `size` | number of addressable bytes, nonzero |
| `out` | receives the region, aligned to at least ALIGN, untouched on failure |
| **returns** | the outcome. EINVAL for zero size, ENOMEM for one too large to map |

### allocate_typed

```mach
pub fun allocate_typed[T](total: usize, out: **T) Status
```

allocate a zero-initialized region of total bytes typed as T, without
changing T's secrecy shape

| Parameter | |
| :--- | :--- |
| `total` | region size in bytes, nonzero |
| `out` | receives the region, aligned to at least ALIGN, untouched on failure |
| **returns** | the outcome. EINVAL for zero total, ENOMEM for one too large to map |

## Functions

### free

```mach
pub fun free(data: *^u8, size: usize) i64
```

release a region allocate returned, without wiping it

| Parameter | |
| :--- | :--- |
| `data` | the region |
| `size` | the size it was allocated with |
| **returns** | zero, or a negative native code with the region still owned |

### free_typed

```mach
pub fun free_typed[T](base: *T, total: usize) i64
```

release a region allocate_typed returned, without wiping it

| Parameter | |
| :--- | :--- |
| `base` | the region |
| `total` | the size in bytes it was allocated with |
| **returns** | zero, or a negative native code with the region still owned |

### random_fill

```mach
pub fun random_fill(data: *^u8, len: usize) i64
```

fill part of a region from the operating-system csprng in one native call

| Parameter | |
| :--- | :--- |
| `data` | destination, at least len bytes |
| `len` | at most RANDOM_FILL_MAX |
| **returns** | bytes filled, which may be fewer than len, or a negative native code |

### read_at

```mach
pub fun read_at(descriptor: i32, data: *^u8, len: usize, offset: u64) i64
```

one positioned read into welded storage: the kernel writes it through this
call and nothing else

| Parameter | |
| :--- | :--- |
| **returns** | bytes delivered (zero at end of file), or a negative native code |

### write_at

```mach
pub fun write_at(descriptor: i32, data: *^u8, len: usize, offset: u64) i64
```

one positioned write from welded storage: the kernel reads it through this
call and nothing else

| Parameter | |
| :--- | :--- |
| **returns** | bytes persisted, or a negative native code |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `ALIGN` | `usize` | `4096` | the alignment every allocation starts on: the smallest page size any host has |
| `LOCKS` | `bool` | `true` where `$mach.build.sys == $mach.sys.linux`; `true` where `$mach.build.sys == $mach.sys.darwin`; `false` where `$mach.build.sys == $mach.sys.wasi`; `true` where `$mach.build.sys == $mach.sys.windows` | every host std reaches locks secret pages |
| `RANDOM_FILL_MAX` | `usize` | `256` where `$mach.build.sys == $mach.sys.darwin`; `0xFFFFFFFF` where `$mach.build.sys == $mach.sys.windows`; `~(0::usize)` otherwise | the most bytes one random_fill call accepts |

