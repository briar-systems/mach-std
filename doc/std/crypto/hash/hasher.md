[std](../../README.md) / [crypto](../README.md) / [hash](README.md) / **hasher**

# std.crypto.hash.hasher

caller-supplied running digest

a consumer that wants to digest bytes it handles takes a Hasher instead of
choosing a hash. the owner creates the state, passes a Hasher over it, and
reads or finishes the digest itself, so the consumer assumes no digest size,
block size or output length.

Source: [`src/crypto/hash/hasher.mach`](../../../../src/crypto/hash/hasher.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Hasher`](#hasher) | `rec` | a running digest fed by someone else's bytes |

| On `Hasher` | |
| :--- | :--- |
| [`update`](#update) | feed len bytes at data to the digest |

---

## Hasher

```mach
pub rec Hasher {
    ctx:       ptr;
    fn_update: fun(ptr, *u8, usize);
}
```

a running digest fed by someone else's bytes

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque hash state owned by the caller |
| `fn_update` | `fun(ptr, *u8, usize)` | folds len bytes at data into the state |

### update

```mach
pub fun update(h: *Hasher, data: *u8, len: usize)
```

feed len bytes at data to the digest

| Parameter | |
| :--- | :--- |
| `h` | hasher to feed |
| `data` | bytes to fold in |
| `len` | number of bytes |

