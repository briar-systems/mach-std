[std](../README.md) / [memory](README.md) / **secret**

# std.memory.secret

secret-welded storage: allocation and borrows

every pointer here keeps its welded shape. the native work is the os
contract's secret primitives: this module adds the wipe before release,
typed geometry, the borrow table, and the policy for a host that cannot lock
pages. it needs the pages capability alone. filling welded storage from the
system's entropy is std.crypto.rand.fill_secret, and positioned file
transfers into and out of it are std.io.file.secret.

storage stays typed *^u8 (or the exact *T for typed regions) across the whole
native boundary, with no public pointer or integer alias to the bytes. linux
uses direct syscalls, darwin libSystem, windows the virtual-memory apis, and
wasi fresh pages of linear memory.

every allocation is locked against paging, sits between two inaccessible
guard pages, and is kept out of core dumps where the host can say so (linux
does, through memfd_secret or MADV_DONTDUMP. darwin and windows have no
per-allocation exclusion). a host that refuses the lock fails the allocation
with io_error.OP_LOCK as its operation, never a silent unlocked fallback. a
host whose contract cannot lock at all (std.system.os.SECRET_LOCKS false)
serves secret storage only after the program calls accept_unlocked.

allocation returns zero-filled storage aligned to at least ALIGN. release
wipes the whole logical span before the native release and reports success
only once the original allocation is gone. (nil, 0) is a successful no-op,
and a failed release leaves zeroed storage owned by the caller. a refused
release writes nothing, since the span it was given is exactly what failed
validation, and the caller keeps live, unwiped storage.

typed allocation checks the complete count * $size_of(T) geometry and honours
$align_of(T), over-aligned records included. typed release needs the original
count, validates the stored geometry, and wipes every byte of every element,
padding included. the header is found through the caller's pointer, so a
refusal cannot prove any span is std's and wipes none of it.

the ^ qualifier enforces secret data flow. none of this isolates storage
across process creation or resists a debugger with process access.

Source: [`src/memory/secret.mach`](../../../src/memory/secret.mach)

Uses types from [`std.io.error`](../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Borrow`](#borrow) | `rec` | a handle to welded storage lent to the borrow table, not an address |

| On `Borrow` | |
| :--- | :--- |
| [`borrow_span`](#borrow_span) | resolve a span inside a live borrow |
| [`borrow_acquire`](#borrow_acquire) | lend welded storage to a handle |
| [`borrow_release`](#borrow_release) | return a borrow; the storage is neither wiped nor released, it was never owned |
| [`borrow_size`](#borrow_size) | the span length of a live borrow, or zero |
| [`borrow_data`](#borrow_data) | the welded storage of a live borrow, or nil |
| [`borrow_wipe`](#borrow_wipe) | zero a span of a borrow |
| [`borrow_fill`](#borrow_fill) | copy welded bytes into a span of a borrow |
| [`borrow_drain`](#borrow_drain) | copy welded bytes out of a span of a borrow |
| [`borrow_copy`](#borrow_copy) | copy between two borrows without either pointer leaving the boundary |

| Functions | |
| :--- | :--- |
| [`typed_aligned`](#typed_aligned) | whether a typed pointer sits on an alignment boundary, read without turning the address into an integer the secrecy rules would refuse |
| [`accept_unlocked`](#accept_unlocked) | accept secret storage the host cannot lock, on a host whose contract says it cannot (std.system.os.SECRET_LOCKS false) |
| [`allocate`](#allocate) | allocate one zero-initialized secret-welded byte region |
| [`deallocate`](#deallocate) | wipe and release one secret-welded byte region |
| [`allocate_typed`](#allocate_typed) | allocate a zero-initialized typed region without changing T's secrecy shape |
| [`deallocate_typed`](#deallocate_typed) | wipe and release a typed region without changing T's secrecy shape |

| Constants | |
| :--- | :--- |
| [`ALIGN`](#constants) | the alignment every allocation starts on, whatever its size |

---

## Borrow

```mach
pub rec Borrow {
    index:      u32;
    generation: u32;
}
```

a handle to welded storage lent to the borrow table, not an address

| Field | Type | |
| :--- | :--- | :--- |
| `index` | `u32` | the entry's slot in the table |
| `generation` | `u32` | the slot's generation when the borrow was acquired, so a handle outlived by its release names no later borrow of the same slot |

### borrow_span

```mach
pub fun borrow_span(borrow: Borrow, offset: usize, len: usize, data: **^u8, operation: std.io.error.Operation) err[std.io.error.Error]
```

resolve a span inside a live borrow

the pointer stays valid until the owner closes the borrow, the same lifetime
borrow_data has

| Parameter | |
| :--- | :--- |
| `data` | receives the span's first byte, untouched on failure |
| `operation` | the operation an error names |
| **returns** | ok, CLOSED for a handle that is not live, INVALID for a span outside the borrow |

### borrow_acquire

```mach
pub fun borrow_acquire(data: *^u8, size: usize, out: *Borrow) err[std.io.error.Error]
```

lend welded storage to a handle

| Parameter | |
| :--- | :--- |
| `data` | the storage, which stays owned by and valid for the caller until close |
| `size` | nonzero span length |
| `out` | the handle |
| **returns** | ok, INVALID for nil or empty storage or a nil out, RESOURCE_EXHAUSTED when the table cannot grow, at the latest once every u32 index is live |

### borrow_release

```mach
pub fun borrow_release(borrow: Borrow) err[std.io.error.Error]
```

return a borrow; the storage is neither wiped nor released, it was never owned

| Parameter | |
| :--- | :--- |
| **returns** | ok, or CLOSED for a handle that is not live |

### borrow_size

```mach
pub fun borrow_size(borrow: Borrow) usize
```

the span length of a live borrow, or zero

### borrow_data

```mach
pub fun borrow_data(borrow: Borrow) *^u8
```

the welded storage of a live borrow, or nil

the pointer stays valid until the owner closes the borrow, the same lifetime
the positioned transfers rely on

### borrow_wipe

```mach
pub fun borrow_wipe(borrow: Borrow, offset: usize, len: usize) err[std.io.error.Error]
```

zero a span of a borrow

| Parameter | |
| :--- | :--- |
| **returns** | ok, CLOSED for a dead handle, INVALID for a span outside the borrow |

### borrow_fill

```mach
pub fun borrow_fill(borrow: Borrow, offset: usize, source: *^u8, len: usize) err[std.io.error.Error]
```

copy welded bytes into a span of a borrow

| Parameter | |
| :--- | :--- |
| `source` | welded storage the caller can read |
| **returns** | ok, CLOSED, or INVALID for a span outside the borrow or a nil source |

### borrow_drain

```mach
pub fun borrow_drain(borrow: Borrow, offset: usize, destination: *^u8, len: usize) err[std.io.error.Error]
```

copy welded bytes out of a span of a borrow

| Parameter | |
| :--- | :--- |
| `destination` | welded storage the caller owns |
| **returns** | ok, CLOSED, or INVALID for a span outside the borrow or a nil destination |

### borrow_copy

```mach
pub fun borrow_copy(destination: Borrow, destination_offset: usize, source: Borrow, source_offset: usize, len: usize) err[std.io.error.Error]
```

copy between two borrows without either pointer leaving the boundary

| Parameter | |
| :--- | :--- |
| **returns** | ok, CLOSED for a dead handle, INVALID for a span outside either borrow |

## Functions

### typed_aligned

```mach
pub fun typed_aligned[T](data: *T, alignment: usize) bool
```

whether a typed pointer sits on an alignment boundary, read without turning
the address into an integer the secrecy rules would refuse

| Parameter | |
| :--- | :--- |
| `alignment` | a power of two |

### accept_unlocked

```mach
pub fun accept_unlocked()
```

accept secret storage the host cannot lock, on a host whose contract says it
cannot (std.system.os.SECRET_LOCKS false). until a program calls this, such a
host refuses every allocation as UNSUPPORTED with operation OP_LOCK. on a host
that locks, a refused lock still fails the allocation: this never downgrades
it

### allocate

```mach
pub fun allocate(size: usize, out: **^u8) err[std.io.error.Error]
```

allocate one zero-initialized secret-welded byte region

| Parameter | |
| :--- | :--- |
| `size` | number of addressable bytes |
| `out` | receives the logical span owner, nil for zero size, untouched on failure |
| **returns** | ok, or the refusal: INVALID for a nil out, UNSUPPORTED with OP_LOCK on a host that cannot lock before accept_unlocked, the host's lock refusal with OP_LOCK, or the native mapping error |

### deallocate

```mach
pub fun deallocate(data: *^u8, size: usize) err[std.io.error.Error]
```

wipe and release one secret-welded byte region

| Parameter | |
| :--- | :--- |
| `data` | allocation returned by allocate |
| `size` | original nonzero allocation size |
| **returns** | ok after the wipe and release. INVALID for a nil data or zero size (not both), with nothing written and the caller still owning any storage unwiped. otherwise the native error, with the storage wiped and still owned by the caller |

### allocate_typed

```mach
pub fun allocate_typed[T](count: usize, out: **T) err[std.io.error.Error]
```

allocate a zero-initialized typed region without changing T's secrecy shape

| Parameter | |
| :--- | :--- |
| `count` | number of T values |
| `out` | receives the aligned typed owner, nil for zero count, untouched on failure |
| **returns** | ok, or the refusal: INVALID for a nil out or a zero-sized T, RANGE for a count whose geometry overflows, and otherwise as allocate |

### deallocate_typed

```mach
pub fun deallocate_typed[T](data: *T, count: usize) err[std.io.error.Error]
```

wipe and release a typed region without changing T's secrecy shape

| Parameter | |
| :--- | :--- |
| `data` | allocation returned by allocate_typed[T] |
| `count` | original element count |
| **returns** | ok after the wipe and release. INVALID for a nil data or zero count (not both), a zero-sized T, an overflowing count, a misaligned data, or a header that does not match count, with nothing written and the caller still owning live, unwiped storage to release with the correct count. otherwise the native error, with every element wiped and the storage still owned by the caller |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `ALIGN` | `usize` | `os.SECRET_ALIGN` | the alignment every allocation starts on, whatever its size |

