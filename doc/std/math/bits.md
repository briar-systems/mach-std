[std](../README.md) / [math](README.md) / **bits**

# std.math.bits

bit manipulation utilities

Source: [`src/math/bits.mach`](../../../src/math/bits.mach)

| Functions | |
| :--- | :--- |
| [`popcount`](#popcount) | count the number of set bits (Hamming weight) |
| [`clz`](#clz) | count leading zeros |
| [`ctz`](#ctz) | count trailing zeros |
| [`rotate_left`](#rotate_left) | rotate bits left by n positions |
| [`rotate_right`](#rotate_right) | rotate bits right by n positions |
| [`byte_swap`](#byte_swap) | reverse byte order (big-endian to little-endian or vice versa) |
| [`bit_reverse`](#bit_reverse) | reverse all 64 bits |

---

## Functions

### popcount

```mach
pub fun popcount(v: u64) u64
```

count the number of set bits (Hamming weight)

| Parameter | |
| :--- | :--- |
| `v` | value to count |
| **returns** | number of 1-bits in v |

### clz

```mach
pub fun clz(v: u64) u64
```

count leading zeros

returns 64 if v is 0.

| Parameter | |
| :--- | :--- |
| `v` | value |
| **returns** | number of leading zero bits |

### ctz

```mach
pub fun ctz(v: u64) u64
```

count trailing zeros

returns 64 if v is 0.

| Parameter | |
| :--- | :--- |
| `v` | value |
| **returns** | number of trailing zero bits |

### rotate_left

```mach
pub fun rotate_left(v: u64, n: u64) u64
```

rotate bits left by n positions

| Parameter | |
| :--- | :--- |
| `v` | value to rotate |
| `n` | number of bit positions (masked to 0..63) |
| **returns** | v rotated left by n |

### rotate_right

```mach
pub fun rotate_right(v: u64, n: u64) u64
```

rotate bits right by n positions

| Parameter | |
| :--- | :--- |
| `v` | value to rotate |
| `n` | number of bit positions (masked to 0..63) |
| **returns** | v rotated right by n |

### byte_swap

```mach
pub fun byte_swap(v: u64) u64
```

reverse byte order (big-endian to little-endian or vice versa)

| Parameter | |
| :--- | :--- |
| `v` | value to byte-swap |
| **returns** | v with bytes in reversed order |

### bit_reverse

```mach
pub fun bit_reverse(v: u64) u64
```

reverse all 64 bits

| Parameter | |
| :--- | :--- |
| `v` | value to reverse |
| **returns** | v with all bits in reversed order |

