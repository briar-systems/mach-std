[std](../README.md) / [crypto](README.md) / **rand**

# std.crypto.rand

cryptographic random number generation

fills buffers with random bytes from the OS entropy source: public storage
through fill, and secret-welded storage through fill_secret, whose bytes
never pass through public memory.

Source: [`src/crypto/rand.mach`](../../../src/crypto/rand.mach)

Uses types from [`std.io.error`](../io/error.md).

| Functions | |
| :--- | :--- |
| [`fill`](#fill) | fill a buffer with cryptographic random bytes |
| [`fill_secret`](#fill_secret) | initialize every requested byte of secret-welded storage from the entropy source |
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

### fill_secret

```mach
pub fun fill_secret(data: *^u8, len: usize) err[std.io.error.Error]
```

initialize every requested byte of secret-welded storage from the entropy
source

the source is read in the chunks one native call accepts, a short read is
continued, and an interrupted call is retried within a budget that progress
resets. the bytes are never seen outside the welded storage

| Parameter | |
| :--- | :--- |
| `data` | destination secret storage |
| `len` | number of bytes to initialize |
| **returns** | ok after complete initialization, or the error after a complete wipe: INVALID for a nil data, IO for a source that delivers nothing or more than it was asked, otherwise the native refusal |

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

