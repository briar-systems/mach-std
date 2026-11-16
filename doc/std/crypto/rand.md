[std](../README.md) / [crypto](README.md) / **rand**

# std.crypto.rand

cryptographic random number generation

fills buffers with random bytes from the OS entropy source.

Source: [`src/crypto/rand.mach`](../../../src/crypto/rand.mach)

Uses types from [`std.io.error`](../io/error.md).

| Functions | |
| :--- | :--- |
| [`fill`](#fill) | fill a buffer with cryptographic random bytes |
| [`u64`](#u64) | return a random 64-bit unsigned integer |
| [`u32`](#u32) | return a random 32-bit unsigned integer |

---

## Functions

### fill

```mach
pub fun fill(buf: *u8, len: usize) err[std.io.error.Error]
```

fill a buffer with cryptographic random bytes

the entropy source is read until len bytes are written. on failure the
bytes written before the refusal stay in buf (the completed prefix is
observable) and the error carries the native code under OP_READ.

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `len` | number of bytes to fill |
| **returns** | ok, or the entropy source's refusal |

### u64

```mach
pub fun u64() u64
```

return a random 64-bit unsigned integer

aborts if the OS entropy source fails.

| Parameter | |
| :--- | :--- |
| **returns** | random value |

### u32

```mach
pub fun u32() u32
```

return a random 32-bit unsigned integer

aborts if the OS entropy source fails.

| Parameter | |
| :--- | :--- |
| **returns** | random value |

