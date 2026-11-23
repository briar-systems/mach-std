[std](../README.md) / [simd](README.md) / **select**

# std.simd.select

lane-wise select / blend over the seeded 128-bit vector types

select is the load-bearing SIMD-library primitive: the compiler produces no
`select` operator, so a conditional lane pick is expressed as the pure
bitwise idiom `(mask & a) | (~mask & b)` over the unsigned mask a comparison
yields. `mask` is an unsigned vector whose lanes are all-ones (true) or
all-zeros (false), exactly the shape a vector comparison produces (see the
compiler's operators.md). Where a lane of `mask` is true the result takes the
corresponding lane of `a`; where false, of `b`.

the four unsigned types blend directly. the signed and float types have no
bitwise operators, so their operands are bit-reinterpreted (`:~`) through the
matching unsigned type, a pure reinterpret and not a numeric conversion, and
the result reinterpreted back. a mask with partial (non-uniform) lane bits
yields a per-bit mix; masks are expected to come from comparisons.

Source: [`src/simd/select.mach`](../../../src/simd/select.mach)

| Functions | |
| :--- | :--- |
| [`select_u8x16`](#select_u8x16) | select over u8x16 lanes |
| [`select_u16x8`](#select_u16x8) | select over u16x8 lanes |
| [`select_u32x4`](#select_u32x4) | select over u32x4 lanes |
| [`select_u64x2`](#select_u64x2) | select over u64x2 lanes |
| [`select_i8x16`](#select_i8x16) | select over i8x16 lanes, mask is the matching u8x16 |
| [`select_i16x8`](#select_i16x8) | select over i16x8 lanes, mask is the matching u16x8 |
| [`select_i32x4`](#select_i32x4) | select over i32x4 lanes, mask is the matching u32x4 |
| [`select_i64x2`](#select_i64x2) | select over i64x2 lanes, mask is the matching u64x2 |
| [`select_f32x4`](#select_f32x4) | select over f32x4 lanes, mask is the matching u32x4 |
| [`select_f64x2`](#select_f64x2) | select over f64x2 lanes, mask is the matching u64x2 |

---

## Functions

### select_u8x16

```mach
pub fun select_u8x16(mask: u8x16, a: u8x16, b: u8x16) u8x16
```

select over u8x16 lanes

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_u16x8

```mach
pub fun select_u16x8(mask: u16x8, a: u16x8, b: u16x8) u16x8
```

select over u16x8 lanes

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_u32x4

```mach
pub fun select_u32x4(mask: u32x4, a: u32x4, b: u32x4) u32x4
```

select over u32x4 lanes

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_u64x2

```mach
pub fun select_u64x2(mask: u64x2, a: u64x2, b: u64x2) u64x2
```

select over u64x2 lanes

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_i8x16

```mach
pub fun select_i8x16(mask: u8x16, a: i8x16, b: i8x16) i8x16
```

select over i8x16 lanes, mask is the matching u8x16

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_i16x8

```mach
pub fun select_i16x8(mask: u16x8, a: i16x8, b: i16x8) i16x8
```

select over i16x8 lanes, mask is the matching u16x8

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_i32x4

```mach
pub fun select_i32x4(mask: u32x4, a: i32x4, b: i32x4) i32x4
```

select over i32x4 lanes, mask is the matching u32x4

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_i64x2

```mach
pub fun select_i64x2(mask: u64x2, a: i64x2, b: i64x2) i64x2
```

select over i64x2 lanes, mask is the matching u64x2

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_f32x4

```mach
pub fun select_f32x4(mask: u32x4, a: f32x4, b: f32x4) f32x4
```

select over f32x4 lanes, mask is the matching u32x4

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

### select_f64x2

```mach
pub fun select_f64x2(mask: u64x2, a: f64x2, b: f64x2) f64x2
```

select over f64x2 lanes, mask is the matching u64x2

| Parameter | |
| :--- | :--- |
| `mask` | per-lane selector, all-ones picks a and all-zeros picks b |
| `a` | value chosen where the mask lane is true |
| `b` | value chosen where the mask lane is false |
| **returns** | lane-wise blend of a and b |

