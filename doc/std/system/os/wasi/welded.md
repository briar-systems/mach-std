[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [wasi](README.md) / **welded**

# std.system.os.wasi.welded

secret-welded storage on a target with no page mappings

the secrecy rules let no plain pointer become a welded one and no welded one
become an integer, and a native target carries a page mapping across in asm.
wasm has no mapping to carry, so here the storage is welded from its
declaration: one region of ^u8 that every secret allocation is carved from,
and an address crosses as an offset into it, recovered from a pointer by
ordering it against the region, which the rules allow since an address is
public. nothing here reads or moves a secret.

a T with public bytes cannot be viewed through the region, and such an
instance is refused where it is written.

Source: [`src/system/os/wasi/welded.mach`](../../../../../src/system/os/wasi/welded.mach)

| Functions | |
| :--- | :--- |
| [`index`](#index) | the offset in the region a pointer into it holds |
| [`at`](#at) | a view of T at an offset in the region |
| [`map_secret`](#map_secret) | storage for span bytes between two pages, which cannot be guarded here |
| [`unmap_secret`](#unmap_secret) | give back what map_secret took, guards included |

| Constants | |
| :--- | :--- |
| [`PAGE`](#constants) | the unit storage is carved in, and the page of the secret contract here |

---

## Functions

### index

```mach
pub fun index[T](p: *T) usize
```

the offset in the region a pointer into it holds

### at

```mach
pub fun at[T](offset: usize) *T
```

a view of T at an offset in the region

### map_secret

```mach
pub fun map_secret(span: usize, page: usize, data: *ptr, locking: *bool) i64
```

storage for span bytes between two pages, which cannot be guarded here

| Parameter | |
| :--- | :--- |
| `span` | usable bytes, whole pages |
| `page` | PAGE |
| `data` | receives the usable bytes' offset, as a ptr |
| `locking` | left false, since no step here locks |
| **returns** | 0, or ENOMEM |

### unmap_secret

```mach
pub fun unmap_secret(offset: usize, total: usize) i64
```

give back what map_secret took, guards included

| Parameter | |
| :--- | :--- |
| `offset` | where the leading page starts |
| `total` | its bytes, the two pages included |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `PAGE` | `usize` | `4096` | the unit storage is carved in, and the page of the secret contract here |

