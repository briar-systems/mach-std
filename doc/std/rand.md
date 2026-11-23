[std](README.md) / **rand**

# std.rand

pseudorandom number generation (xoshiro256**)

fast, high-quality PRNG suitable for simulations, games, and general
non-cryptographic use. seed from std.crypto.rand for unpredictable output.

Source: [`src/rand.mach`](../../src/rand.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Rng`](#rng) | `rec` | the state of one xoshiro256** generator, which make and seed keep from being all zero |

| On `Rng` | |
| :--- | :--- |
| [`make`](#make) | create an Rng seeded from the kernel entropy pool |
| [`seed`](#seed) | create an Rng with explicit seed values |
| [`next`](#next) | generate the next random u64 and advance state |
| [`next_u32`](#next_u32) | generate the next random u32 and advance state |
| [`range`](#range) | generate a random value in the range [lo, hi) |
| [`range_u64`](#range_u64) | generate a random value in the unsigned range [lo, hi) |
| [`shuffle`](#shuffle) | shuffle an array in place using Fisher-Yates |

---

## Rng

```mach
pub rec Rng {
    s0: u64;
    s1: u64;
    s2: u64;
    s3: u64;
}
```

the state of one xoshiro256** generator, which make and seed keep from being all zero

| Field | Type | |
| :--- | :--- | :--- |
| `s0` | `u64` | first state word |
| `s1` | `u64` | second state word |
| `s2` | `u64` | third state word |
| `s3` | `u64` | fourth state word |

### make

```mach
pub fun make() Rng
```

create an Rng seeded from the kernel entropy pool

| Parameter | |
| :--- | :--- |
| **returns** | initialized Rng with cryptographic seed |

### seed

```mach
pub fun seed(s0: u64, s1: u64, s2: u64, s3: u64) Rng
```

create an Rng with explicit seed values

at least one value must be non-zero.

| Parameter | |
| :--- | :--- |
| `s0` | first state word |
| `s1` | second state word |
| `s2` | third state word |
| `s3` | fourth state word |
| **returns** | initialized Rng |

### next

```mach
pub fun next(r: *Rng) u64
```

generate the next random u64 and advance state

| Parameter | |
| :--- | :--- |
| `r` | pointer to the Rng state |
| **returns** | pseudorandom 64-bit value |

### next_u32

```mach
pub fun next_u32(r: *Rng) u32
```

generate the next random u32 and advance state

| Parameter | |
| :--- | :--- |
| `r` | pointer to the Rng state |
| **returns** | pseudorandom 32-bit value |

### range

```mach
pub fun range(r: *Rng, lo: i64, hi: i64) i64
```

generate a random value in the range [lo, hi)

hi must be greater than lo; otherwise returns lo.

| Parameter | |
| :--- | :--- |
| `r` | pointer to the Rng state |
| `lo` | inclusive lower bound |
| `hi` | exclusive upper bound |
| **returns** | pseudorandom value in [lo, hi) |

### range_u64

```mach
pub fun range_u64(r: *Rng, lo: u64, hi: u64) u64
```

generate a random value in the unsigned range [lo, hi)

hi must be greater than lo; otherwise returns lo.

| Parameter | |
| :--- | :--- |
| `r` | pointer to the Rng state |
| `lo` | inclusive lower bound |
| `hi` | exclusive upper bound |
| **returns** | pseudorandom value in [lo, hi) |

### shuffle

```mach
pub fun shuffle[T](r: *Rng, data: *T, len: usize)
```

shuffle an array in place using Fisher-Yates

| Parameter | |
| :--- | :--- |
| `r` | pointer to the Rng state |
| `data` | pointer to the array |
| `len` | number of elements |

