[std](README.md) / **math**

# std.math

integer math utilities

Source: [`src/math.mach`](../../src/math.mach)

| Functions | |
| :--- | :--- |
| [`min`](#min) | return the smaller of two signed integers |
| [`max`](#max) | return the larger of two signed integers |
| [`clamp`](#clamp) | clamp a signed integer to the range [lo, hi] |
| [`abs`](#abs) | return the absolute value of a signed integer |
| [`umin`](#umin) | return the smaller of two unsigned integers |
| [`umax`](#umax) | return the larger of two unsigned integers |
| [`uclamp`](#uclamp) | clamp an unsigned integer to the range [lo, hi] |
| [`is_pow2`](#is_pow2) | check whether a value is a power of two |
| [`next_pow2`](#next_pow2) | round up to the next power of two |
| [`log2`](#log2) | compute the floor of log base 2 |
| [`ceil_div`](#ceil_div) | ceiling division of two unsigned integers |
| [`sat_add`](#sat_add) | saturating signed addition |
| [`sat_sub`](#sat_sub) | saturating signed subtraction |
| [`sat_mul`](#sat_mul) | saturating signed multiplication |

---

## Functions

### min

```mach
pub fun min(a: i64, b: i64) i64
```

return the smaller of two signed integers

| Parameter | |
| :--- | :--- |
| `a` | first value |
| `b` | second value |
| **returns** | the smaller of a and b |

### max

```mach
pub fun max(a: i64, b: i64) i64
```

return the larger of two signed integers

| Parameter | |
| :--- | :--- |
| `a` | first value |
| `b` | second value |
| **returns** | the larger of a and b |

### clamp

```mach
pub fun clamp(v: i64, lo: i64, hi: i64) i64
```

clamp a signed integer to the range [lo, hi]

| Parameter | |
| :--- | :--- |
| `v` | value to clamp |
| `lo` | lower bound |
| `hi` | upper bound |
| **returns** | v clamped to [lo, hi] |

### abs

```mach
pub fun abs(v: i64) i64
```

return the absolute value of a signed integer

saturates at I64_MAX for I64_MIN input.

| Parameter | |
| :--- | :--- |
| `v` | value |
| **returns** | absolute value of v |

### umin

```mach
pub fun umin(a: u64, b: u64) u64
```

return the smaller of two unsigned integers

| Parameter | |
| :--- | :--- |
| `a` | first value |
| `b` | second value |
| **returns** | the smaller of a and b |

### umax

```mach
pub fun umax(a: u64, b: u64) u64
```

return the larger of two unsigned integers

| Parameter | |
| :--- | :--- |
| `a` | first value |
| `b` | second value |
| **returns** | the larger of a and b |

### uclamp

```mach
pub fun uclamp(v: u64, lo: u64, hi: u64) u64
```

clamp an unsigned integer to the range [lo, hi]

| Parameter | |
| :--- | :--- |
| `v` | value to clamp |
| `lo` | lower bound |
| `hi` | upper bound |
| **returns** | v clamped to [lo, hi] |

### is_pow2

```mach
pub fun is_pow2(v: u64) bool
```

check whether a value is a power of two

| Parameter | |
| :--- | :--- |
| `v` | value to check |
| **returns** | true if v is a non-zero power of two |

### next_pow2

```mach
pub fun next_pow2(v: u64) u64
```

round up to the next power of two

returns v if already a power of two, 1 if v is 0.

| Parameter | |
| :--- | :--- |
| `v` | value to round up |
| **returns** | next power of two >= v |

### log2

```mach
pub fun log2(v: u64) u64
```

compute the floor of log base 2

returns 0 for v == 0 (undefined).

| Parameter | |
| :--- | :--- |
| `v` | value |
| **returns** | floor(log2(v)) |

### ceil_div

```mach
pub fun ceil_div(a: u64, b: u64) u64
```

ceiling division of two unsigned integers

| Parameter | |
| :--- | :--- |
| `a` | dividend |
| `b` | divisor (must not be 0) |
| **returns** | ceil(a / b) |

### sat_add

```mach
pub fun sat_add(a: i64, b: i64) i64
```

saturating signed addition

clamps the result to [I64_MIN, I64_MAX] on overflow.

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | a + b, saturated |

### sat_sub

```mach
pub fun sat_sub(a: i64, b: i64) i64
```

saturating signed subtraction

clamps the result to [I64_MIN, I64_MAX] on overflow.

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | a - b, saturated |

### sat_mul

```mach
pub fun sat_mul(a: i64, b: i64) i64
```

saturating signed multiplication

clamps the result to [I64_MIN, I64_MAX] on overflow.

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | a * b, saturated |

