[std](../README.md) / [simd](README.md) / **reduce**

# std.simd.reduce

horizontal reductions over the seeded 128-bit vector types

a horizontal reduction collapses a vector's lanes to a single scalar. the
lane-to-lane combine is inherently scalar (comptime-constant lane reads), so
these read each lane and fold. the batch win lives in the caller: accumulate
many vectors with the lane-wise vector operators (one SSE2/NEON instruction
per step on a capable target) and call a horizontal reduction once at the end.
`dot_f32x4` shows the shape: a vector multiply then a single horizontal sum.

Source: [`src/simd/reduce.mach`](../../../src/simd/reduce.mach)

| Functions | |
| :--- | :--- |
| [`hsum_f32x4`](#hsum_f32x4) | horizontal sum of f32x4 lanes |
| [`hsum_f64x2`](#hsum_f64x2) | horizontal sum of f64x2 lanes |
| [`hsum_i32x4`](#hsum_i32x4) | horizontal sum of i32x4 lanes (wrapping) |
| [`hsum_u32x4`](#hsum_u32x4) | horizontal sum of u32x4 lanes (wrapping) |
| [`hmin_f32x4`](#hmin_f32x4) | horizontal minimum of f32x4 lanes |
| [`hmax_f32x4`](#hmax_f32x4) | horizontal maximum of f32x4 lanes |
| [`hmin_i32x4`](#hmin_i32x4) | horizontal minimum of i32x4 lanes |
| [`hmax_i32x4`](#hmax_i32x4) | horizontal maximum of i32x4 lanes |
| [`dot_f32x4`](#dot_f32x4) | dot product of two f32x4 vectors |
| [`hsum_i64x2`](#hsum_i64x2) | horizontal sum of i64x2 lanes (wrapping) |
| [`hsum_u64x2`](#hsum_u64x2) | horizontal sum of u64x2 lanes (wrapping) |
| [`dot_i32x4`](#dot_i32x4) | dot product of two i32x4 vectors (wrapping) |
| [`dot_u32x4`](#dot_u32x4) | dot product of two u32x4 vectors (wrapping) |

---

## Functions

### hsum_f32x4

```mach
pub fun hsum_f32x4(v: f32x4) f32
```

horizontal sum of f32x4 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] + v[2] + v[3] |

### hsum_f64x2

```mach
pub fun hsum_f64x2(v: f64x2) f64
```

horizontal sum of f64x2 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] |

### hsum_i32x4

```mach
pub fun hsum_i32x4(v: i32x4) i32
```

horizontal sum of i32x4 lanes (wrapping)

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] + v[2] + v[3] |

### hsum_u32x4

```mach
pub fun hsum_u32x4(v: u32x4) u32
```

horizontal sum of u32x4 lanes (wrapping)

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] + v[2] + v[3] |

### hmin_f32x4

```mach
pub fun hmin_f32x4(v: f32x4) f32
```

horizontal minimum of f32x4 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | the smallest lane |

### hmax_f32x4

```mach
pub fun hmax_f32x4(v: f32x4) f32
```

horizontal maximum of f32x4 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | the largest lane |

### hmin_i32x4

```mach
pub fun hmin_i32x4(v: i32x4) i32
```

horizontal minimum of i32x4 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | the smallest lane |

### hmax_i32x4

```mach
pub fun hmax_i32x4(v: i32x4) i32
```

horizontal maximum of i32x4 lanes

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | the largest lane |

### dot_f32x4

```mach
pub fun dot_f32x4(a: f32x4, b: f32x4) f32
```

dot product of two f32x4 vectors

the multiply is a single lane-wise vector op (vectorized on a capable target);
the horizontal sum folds the four products.

| Parameter | |
| :--- | :--- |
| `a` | first vector |
| `b` | second vector |
| **returns** | a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3] |

### hsum_i64x2

```mach
pub fun hsum_i64x2(v: i64x2) i64
```

horizontal sum of i64x2 lanes (wrapping)

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] |

### hsum_u64x2

```mach
pub fun hsum_u64x2(v: u64x2) u64
```

horizontal sum of u64x2 lanes (wrapping)

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | v[0] + v[1] |

### dot_i32x4

```mach
pub fun dot_i32x4(a: i32x4, b: i32x4) i32
```

dot product of two i32x4 vectors (wrapping)

products and sum wrap at i32. for an exact dot product of narrower elements
see `std.simd.matmul`, which widens before it multiplies.

| Parameter | |
| :--- | :--- |
| `a` | first vector |
| `b` | second vector |
| **returns** | a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3], modulo 2^32 |

### dot_u32x4

```mach
pub fun dot_u32x4(a: u32x4, b: u32x4) u32
```

dot product of two u32x4 vectors (wrapping)

| Parameter | |
| :--- | :--- |
| `a` | first vector |
| `b` | second vector |
| **returns** | a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3], modulo 2^32 |

