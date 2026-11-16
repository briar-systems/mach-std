[std](../../README.md) / [math](../README.md) / [bignum](README.md) / **nat**

# std.math.bignum.nat

unsigned big integer over caller storage

limbs are little-endian 32-bit; n counts active limbs (n == 0 is zero, no
leading-zero limbs). a Nat owns nothing: its capacity is whatever storage the
caller hands it, which must hold every value the number takes, so each user
sizes it to its own need (std.math.ieee.bignum_limbs gives a float format's).
all multiplies are by small constants, so no 64x64->128 is needed. the core of
std.math.bignum.Big and of the exact float conversions in std.text.parse and
std.format.

Source: [`src/math/bignum/nat.mach`](../../../../src/math/bignum/nat.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Nat`](#nat) | `rec` | an unsigned big integer whose limbs live in caller storage |

| On `Nat` | |
| :--- | :--- |
| [`over`](#over) | zero over the limbs at d |
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

---

## Nat

```mach
pub rec Nat {
    n: usize;
    d: *u32;
}
```

an unsigned big integer whose limbs live in caller storage

| Field | Type | |
| :--- | :--- | :--- |
| `n` | `usize` | active limbs |
| `d` | `*u32` | the storage, borrowed for the number's lifetime |

### over

```mach
pub fun over(d: *u32) Nat
```

zero over the limbs at d

| Parameter | |
| :--- | :--- |
| `d` | storage for every value the number will take |
| **returns** | the number, zero |

### zero

```mach
pub fun zero(b: *Nat)
```

set b to zero

### norm

```mach
pub fun norm(b: *Nat)
```

drop leading-zero limbs so n is exact

### from_u64

```mach
pub fun from_u64(b: *Nat, v: u64)
```

set b to v

### from_u128

```mach
pub fun from_u128(b: *Nat, v: u128)
```

set b to v

### is_zero

```mach
pub fun is_zero(b: *Nat) bool
```

true iff b == 0

### to_u64

```mach
pub fun to_u64(b: *Nat) u64
```

low 64 bits of b (exact when b \< 2^64)

### copy

```mach
pub fun copy(dst: *Nat, src: *Nat)
```

dst = src

### cmp

```mach
pub fun cmp(a: *Nat, b: *Nat) i64
```

-1 if a \< b, 0 if equal, 1 if a > b

### mul_small

```mach
pub fun mul_small(b: *Nat, m: u32)
```

b = b * m

### shl

```mach
pub fun shl(b: *Nat, bits: usize)
```

b = b \<\< bits (multiply by 2^bits)

### add

```mach
pub fun add(a: *Nat, b: *Nat)
```

a = a + b

### sub

```mach
pub fun sub(a: *Nat, b: *Nat)
```

a = a - b, requires a >= b

### add_small

```mach
pub fun add_small(b: *Nat, x: u32)
```

b = b + x

### mul_pow10

```mach
pub fun mul_pow10(b: *Nat, k: usize)
```

b = b * 10^k

### bitlen

```mach
pub fun bitlen(b: *Nat) usize
```

number of significant bits (0 when b == 0)

