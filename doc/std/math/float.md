[std](../README.md) / [math](README.md) / **float**

# std.math.float

scalar floating-point math: roots and transcendentals in plain Mach

every routine is a portable algorithm over the scalar float operators: no
hardware sqrt or transcendental instruction, since the compiler has no
SIMD-capable inline-asm encoders yet (a flagged gap, briar-systems/mach#2021).

the public surface is single-precision (f32); each wrapper widens to f64,
evaluates in double precision, and narrows the result, so the f32 answer is
accurate to well under one f32 ulp. f64-precision entry points are a follow-up.

Source: [`src/math/float.mach`](../../../src/math/float.mach)

| Functions | |
| :--- | :--- |
| [`sqrt_f32`](#sqrt_f32) | square root of a non-negative scalar |
| [`rsqrt_f32`](#rsqrt_f32) | reciprocal square root of a positive scalar |
| [`sin_f32`](#sin_f32) | sine of an angle in radians |
| [`cos_f32`](#cos_f32) | cosine of an angle in radians |
| [`asin_f32`](#asin_f32) | arcsine of a value in [-1, 1] |
| [`acos_f32`](#acos_f32) | arccosine of a value in [-1, 1] |

---

## Functions

### sqrt_f32

```mach
pub fun sqrt_f32(x: f32) f32
```

square root of a non-negative scalar

a Newton refinement in double precision, accurate to under one f32 ulp; a
hardware sqrt awaits SIMD-capable inline-asm encoders in the compiler.

| Parameter | |
| :--- | :--- |
| `x` | non-negative value |
| **returns** | sqrt(x), or 0 for x == 0 |

### rsqrt_f32

```mach
pub fun rsqrt_f32(x: f32) f32
```

reciprocal square root of a positive scalar

| Parameter | |
| :--- | :--- |
| `x` | positive value |
| **returns** | 1 / sqrt(x) |

### sin_f32

```mach
pub fun sin_f32(x: f32) f32
```

sine of an angle in radians

| Parameter | |
| :--- | :--- |
| `x` | angle in radians |
| **returns** | sin(x), or nan for an infinite or nan x |

### cos_f32

```mach
pub fun cos_f32(x: f32) f32
```

cosine of an angle in radians

| Parameter | |
| :--- | :--- |
| `x` | angle in radians |
| **returns** | cos(x), or nan for an infinite or nan x |

### asin_f32

```mach
pub fun asin_f32(x: f32) f32
```

arcsine of a value in [-1, 1]

| Parameter | |
| :--- | :--- |
| `x` | value in [-1, 1] |
| **returns** | asin(x) in [-pi/2, pi/2] |

### acos_f32

```mach
pub fun acos_f32(x: f32) f32
```

arccosine of a value in [-1, 1]

| Parameter | |
| :--- | :--- |
| `x` | value in [-1, 1] |
| **returns** | acos(x) in [0, pi] |

