[std](../../README.md) / [crypto](../README.md) / [hash](README.md) / **fnv1a**

# std.crypto.hash.fnv1a

incremental FNV-1a hashing

the type interners hash composite records field-by-field rather than over a
contiguous byte buffer, so they need an incremental folding API. this mirrors
the byte-wise FNV-1a used by `std.derive`'s record hash, exposed as the
`FNV_INIT` seed constant plus per-value `step_*` folds. `step_bytes` folds a
whole buffer, so hashing a string is `step_bytes(FNV_INIT, s, str_len(s))`.

Source: [`src/crypto/hash/fnv1a.mach`](../../../../src/crypto/hash/fnv1a.mach)

| Functions | |
| :--- | :--- |
| [`step_u8`](#step_u8) | fold one byte into the running hash |
| [`step_u32`](#step_u32) | fold a 32-bit value into the running hash, byte by byte (little-endian) |
| [`step_bytes`](#step_bytes) | fold a run of bytes into the running hash, in order |

| Constants | |
| :--- | :--- |
| [`FNV_PRIME`](#constants) | FNV-1a 64-bit prime |
| [`FNV_OFFSET`](#constants) | FNV-1a 64-bit offset basis |
| [`FNV_INIT`](#constants) | |

---

## Functions

### step_u8

```mach
pub fun step_u8(h: u64, v: u8) u64
```

fold one byte into the running hash

| Parameter | |
| :--- | :--- |
| `h` | running hash |
| `v` | byte to fold in |
| **returns** | updated hash |

### step_u32

```mach
pub fun step_u32(h: u64, v: u32) u64
```

fold a 32-bit value into the running hash, byte by byte (little-endian)

| Parameter | |
| :--- | :--- |
| `h` | running hash |
| `v` | value to fold in |
| **returns** | updated hash |

### step_bytes

```mach
pub fun step_bytes(h: u64, p: *u8, n: usize) u64
```

fold a run of bytes into the running hash, in order

| Parameter | |
| :--- | :--- |
| `h` | running hash |
| `p` | bytes to fold in; may be nil when n is 0 |
| `n` | number of bytes |
| **returns** | updated hash |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `FNV_PRIME` | `u64` | `1099511628211` | FNV-1a 64-bit prime |
| `FNV_OFFSET` | `u64` | `14695981039346656037` | FNV-1a 64-bit offset basis |
| `FNV_INIT` | `u64` | `FNV_OFFSET` |  |

