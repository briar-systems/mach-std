[std](../README.md) / [compat](README.md) / **sha1**

# std.compat.sha1

SHA-1, for interop with formats that name it

this module exists only to read and write formats that fix SHA-1 in their
layout: Mach-O code directories, git object ids and the like. it is not a
security primitive and lives outside `std.crypto` on purpose. SHA-1
collisions are practical, so it must never be used for new integrity,
signature, authentication or key derivation purposes. use the mach-crypto
package's `crypto.hash.sha256` or `crypto.hash.sha512` instead.
there is no secret-typed form and nothing here is constant time.

Source: [`src/compat/sha1.mach`](../../../src/compat/sha1.mach)

| Type | | |
| :--- | :--- | :--- |
| [`State`](#state) | `rec` |  |

| On `State` | |
| :--- | :--- |
| [`make`](#make) | initialize a new SHA-1 state with the standard IV |
| [`update`](#update) | feed data into the hash state |
| [`final`](#final) | finalize the hash and write the 20-byte digest |

| Functions | |
| :--- | :--- |
| [`hash`](#hash) | compute the SHA-1 digest of a byte buffer in one call |

| Constants | |
| :--- | :--- |
| [`DIGEST_SIZE`](#constants), [`BLOCK_SIZE`](#constants) | |

---

## State

```mach
pub rec State {
    h0:      u32;
    h1:      u32;
    h2:      u32;
    h3:      u32;
    h4:      u32;
    buf:     [64]u8;
    buf_len: usize;
    total:   u64;
}
```

### make

```mach
pub fun make() State
```

initialize a new SHA-1 state with the standard IV

| Parameter | |
| :--- | :--- |
| **returns** | initialized state |

### update

```mach
pub fun update(s: *State, data: *u8, len: usize)
```

feed data into the hash state

| Parameter | |
| :--- | :--- |
| `s` | pointer to hash state |
| `data` | pointer to input bytes |
| `len` | number of bytes to process |

### final

```mach
pub fun final(s: *State, digest: *u8)
```

finalize the hash and write the 20-byte digest

| Parameter | |
| :--- | :--- |
| `s` | pointer to hash state |
| `digest` | pointer to 20-byte output buffer |

## Functions

### hash

```mach
pub fun hash(data: *u8, len: usize, digest: *u8)
```

compute the SHA-1 digest of a byte buffer in one call

| Parameter | |
| :--- | :--- |
| `data` | pointer to input bytes |
| `len` | number of bytes to hash |
| `digest` | pointer to 20-byte output buffer |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `DIGEST_SIZE` | `usize` | `20` |  |
| `BLOCK_SIZE` | `usize` | `64` |  |

