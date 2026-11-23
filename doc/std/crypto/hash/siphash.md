[std](../../README.md) / [crypto](../README.md) / [hash](README.md) / **siphash**

# std.crypto.hash.siphash

keyed SipHash-2-4, a short-input pseudorandom function

WHEN TO USE IT. any hash table, shard choice or bucket index whose keys an
untrusted peer can influence: a connection id, a header name, a path, an
address. an unkeyed hash (`fnv1a`, `std.collections.natural.hash`) is public
arithmetic, so a peer can precompute keys that all land in one bucket and
turn every lookup into a linear walk. SipHash under a secret random key makes
the placement unpredictable to anyone who does not hold the key. draw the key
once per table or per process with `random_key` and never send it anywhere.
`std.collections.map.MapKeyed` is a map hashed this way.

WHAT IT IS NOT. a 64-bit output is a table hash, not a message
authenticator worth trusting at a protocol boundary and not a digest: use
sha256 or sha3 for those. the key is held in public words, so a record
holding it is not welded; it guards against flooding, not against a reader
of this process's memory.

the algorithm is Aumasson and Bernstein's, "SipHash: a fast short-input
PRF" (2012): two compression rounds per 8-byte word, four finalization
rounds, the message length folded into the last word. `bytes` hashes a whole
buffer at once. `make`, `update`, `update_u64` and `final` hash a message
delivered in pieces and agree with `bytes` over the concatenation.

Source: [`src/crypto/hash/siphash.mach`](../../../../src/crypto/hash/siphash.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Key`](#key) | `rec` | a 128-bit SipHash key as two little-endian words |
| [`State`](#state) | `rec` | an incremental SipHash state |

| On `Key` | |
| :--- | :--- |
| [`random_key`](#random_key) | draw a key from the operating system entropy source |
| [`make`](#make) | start a hash under a key |
| [`bytes`](#bytes) | hash a buffer in one call |

| On `State` | |
| :--- | :--- |
| [`update`](#update) | absorb bytes |
| [`update_u64`](#update_u64) | absorb a word as its eight little-endian bytes, on any host byte order |
| [`final`](#final) | the hash of everything absorbed |

---

## Key

```mach
pub rec Key {
    k0: u64;
    k1: u64;
}
```

a 128-bit SipHash key as two little-endian words

| Field | Type | |
| :--- | :--- | :--- |
| `k0` | `u64` | key bytes 0 to 7 |
| `k1` | `u64` | key bytes 8 to 15 |

### random_key

Only where `capability.HAS_ENTROPY`.

```mach
pub fun random_key() opt[Key]
```

draw a key from the operating system entropy source

there is no fallback: when the source refuses, no key is returned, and a
table built on a guessable key would defeat the point of keying it.

| Parameter | |
| :--- | :--- |
| **returns** | a fresh key, or none when the entropy source refused |

### make

```mach
pub fun make(key: Key) State
```

start a hash under a key

| Parameter | |
| :--- | :--- |
| `key` | the key |
| **returns** | a state that has absorbed nothing |

### bytes

```mach
pub fun bytes(key: Key, data: *u8, len: usize) u64
```

hash a buffer in one call

| Parameter | |
| :--- | :--- |
| `key` | the key |
| `data` | the bytes, which may be nil when len is 0 |
| `len` | number of bytes |
| **returns** | the 64-bit hash |

## State

```mach
pub rec State {
    v0:       u64;
    v1:       u64;
    v2:       u64;
    v3:       u64;
    tail:     u64;
    tail_len: usize;
    total:    u64;
}
```

an incremental SipHash state

| Field | Type | |
| :--- | :--- | :--- |
| `v0` | `u64` | internal word 0 |
| `v1` | `u64` | internal word 1 |
| `v2` | `u64` | internal word 2 |
| `v3` | `u64` | internal word 3 |
| `tail` | `u64` | the bytes of an incomplete word, little-endian |
| `tail_len` | `usize` | number of bytes held in `tail`, below 8 |
| `total` | `u64` | number of bytes absorbed so far |

### update

```mach
pub fun update(s: *State, data: *u8, len: usize)
```

absorb bytes

| Parameter | |
| :--- | :--- |
| `s` | the state |
| `data` | the bytes, which may be nil when len is 0 |
| `len` | number of bytes |

### update_u64

```mach
pub fun update_u64(s: *State, word: u64)
```

absorb a word as its eight little-endian bytes, on any host byte order

| Parameter | |
| :--- | :--- |
| `s` | the state |
| `word` | the word |

### final

```mach
pub fun final(s: *State) u64
```

the hash of everything absorbed

the state is left as it was, so more bytes may follow and a later `final`
covers them too.

| Parameter | |
| :--- | :--- |
| `s` | the state |
| **returns** | the 64-bit hash |

