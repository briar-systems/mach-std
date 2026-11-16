[std](../README.md) / [simd](README.md) / **shuffle**

# std.simd.shuffle

lane shuffles and broadcast over the seeded 128-bit vector types

a shuffle rearranges or replicates lanes. lane indices are comptime constants,
so a shuffle is a fixed pattern of lane reads assembled into a new vector —
`splat` replicates one lane, `reverse` mirrors lane order. to broadcast a
specific lane of `v`, splat its comptime-indexed read, e.g. `splat_f32x4(v[2])`.

Source: [`src/simd/shuffle.mach`](../../../src/simd/shuffle.mach)

| Functions | |
| :--- | :--- |
| [`splat_f32x4`](#splat_f32x4) | broadcast a scalar into every f32x4 lane |
| [`splat_f64x2`](#splat_f64x2) | broadcast a scalar into every f64x2 lane |
| [`splat_i32x4`](#splat_i32x4) | broadcast a scalar into every i32x4 lane |
| [`splat_u32x4`](#splat_u32x4) | broadcast a scalar into every u32x4 lane |
| [`splat_u8x16`](#splat_u8x16) | broadcast a scalar into every u8x16 lane |
| [`splat_i8x16`](#splat_i8x16) | broadcast a scalar into every i8x16 lane |
| [`splat_i16x8`](#splat_i16x8) | broadcast a scalar into every i16x8 lane |
| [`reverse_f32x4`](#reverse_f32x4) | reverse the lane order of an f32x4 |
| [`reverse_i32x4`](#reverse_i32x4) | reverse the lane order of an i32x4 |
| [`reverse_u32x4`](#reverse_u32x4) | reverse the lane order of a u32x4 |

---

## Functions

### splat_f32x4

```mach
pub fun splat_f32x4(x: f32) f32x4
```

broadcast a scalar into every f32x4 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | f32x4 with every lane equal to x |

### splat_f64x2

```mach
pub fun splat_f64x2(x: f64) f64x2
```

broadcast a scalar into every f64x2 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | f64x2 with every lane equal to x |

### splat_i32x4

```mach
pub fun splat_i32x4(x: i32) i32x4
```

broadcast a scalar into every i32x4 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | i32x4 with every lane equal to x |

### splat_u32x4

```mach
pub fun splat_u32x4(x: u32) u32x4
```

broadcast a scalar into every u32x4 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | u32x4 with every lane equal to x |

### splat_u8x16

```mach
pub fun splat_u8x16(x: u8) u8x16
```

broadcast a scalar into every u8x16 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | u8x16 with every lane equal to x |

### splat_i8x16

```mach
pub fun splat_i8x16(x: i8) i8x16
```

broadcast a scalar into every i8x16 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | i8x16 with every lane equal to x |

### splat_i16x8

```mach
pub fun splat_i16x8(x: i16) i16x8
```

broadcast a scalar into every i16x8 lane

| Parameter | |
| :--- | :--- |
| `x` | value to replicate |
| **returns** | i16x8 with every lane equal to x |

### reverse_f32x4

```mach
pub fun reverse_f32x4(v: f32x4) f32x4
```

reverse the lane order of an f32x4

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | {v[3], v[2], v[1], v[0]} |

### reverse_i32x4

```mach
pub fun reverse_i32x4(v: i32x4) i32x4
```

reverse the lane order of an i32x4

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | {v[3], v[2], v[1], v[0]} |

### reverse_u32x4

```mach
pub fun reverse_u32x4(v: u32x4) u32x4
```

reverse the lane order of a u32x4

| Parameter | |
| :--- | :--- |
| `v` | input vector |
| **returns** | {v[3], v[2], v[1], v[0]} |

