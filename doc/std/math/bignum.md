[std](../README.md) / [math](README.md) / **bignum**

# std.math.bignum

fixed-capacity big integer

a std.math.bignum.nat.Nat over LIMBS inline limbs (4096 bits), for a caller
whose values have a known small bound. the float conversions do not use it:
they size their own Nat storage from the format row (see std.math.ieee).

Source: [`src/math/bignum.mach`](../../../src/math/bignum.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Big`](#big) | `rec` | a fixed-capacity unsigned big integer |

| On `Big` | |
| :--- | :--- |
| [`zero`](#zero) | set b to zero |
| [`norm`](#norm) | drop leading-zero limbs so n is exact |
| [`from_u64`](#from_u64) | set b to v |
| [`from_u128`](#from_u128) | set b to v |
| [`is_zero`](#is_zero) | true iff b == 0 |
| [`to_u64`](#to_u64) | low 64 bits of b (exact when b \< 2^64) |
| [`copy`](#copy) | dst = src |
| [`cmp`](#cmp) | -1 if a \< b, 0 if equal, 1 if a > b |
| [`mul_small`](#mul_small) | b = b * m |
| [`shl`](#shl) | b = b \<\< bits (multiply by 2^bits) |
| [`add`](#add) | a = a + b |
| [`sub`](#sub) | a = a - b, requires a >= b |
| [`add_small`](#add_small) | b = b + x |
| [`mul_pow10`](#mul_pow10) | b = b * 10^k |
| [`bitlen`](#bitlen) | number of significant bits (0 when b == 0) |

| Constants | |
| :--- | :--- |
| [`LIMBS`](#constants) | the limb capacity of a Big |

---

## Big

```mach
pub rec Big {
    n: usize;
    d: [LIMBS]u32;
}
```

a fixed-capacity unsigned big integer

### zero

```mach
pub fun zero(b: *Big)
```

set b to zero

### norm

```mach
pub fun norm(b: *Big)
```

drop leading-zero limbs so n is exact

### from_u64

```mach
pub fun from_u64(b: *Big, v: u64)
```

set b to v

### from_u128

```mach
pub fun from_u128(b: *Big, v: u128)
```

set b to v

### is_zero

```mach
pub fun is_zero(b: *Big) bool
```

true iff b == 0

### to_u64

```mach
pub fun to_u64(b: *Big) u64
```

low 64 bits of b (exact when b \< 2^64)

### copy

```mach
pub fun copy(dst: *Big, src: *Big)
```

dst = src

### cmp

```mach
pub fun cmp(a: *Big, b: *Big) i64
```

-1 if a \< b, 0 if equal, 1 if a > b

### mul_small

```mach
pub fun mul_small(b: *Big, m: u32)
```

b = b * m

### shl

```mach
pub fun shl(b: *Big, bits: usize)
```

b = b \<\< bits (multiply by 2^bits)

### add

```mach
pub fun add(a: *Big, b: *Big)
```

a = a + b

### sub

```mach
pub fun sub(a: *Big, b: *Big)
```

a = a - b, requires a >= b

### add_small

```mach
pub fun add_small(b: *Big, x: u32)
```

b = b + x

### mul_pow10

```mach
pub fun mul_pow10(b: *Big, k: usize)
```

b = b * 10^k

### bitlen

```mach
pub fun bitlen(b: *Big) usize
```

number of significant bits (0 when b == 0)

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `LIMBS` | `usize` | `128` | the limb capacity of a Big |

