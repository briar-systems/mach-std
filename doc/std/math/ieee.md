[std](../README.md) / [math](README.md) / **ieee**

# std.math.ieee

ieee 754 binary interchange formats as data

every float conversion in std (std.text.parse and std.format) reads its width
from a Format row rather than from code: one exact decimal parse, one hex
parse, one shortest writer and one fixed-precision writer serve every row, so a
further binary format (bfloat16, binary128) is one more row. a value travels as
its bit pattern in the low end of a u128, wide enough for any row up to
binary128. everything rounding and the subnormal range need is derived from
the three fields here.

the exact conversions hold their intermediates in std.math.bignum.nat numbers
over storage the caller sizes from the row: bignum_limbs gives the limbs one
number of a row needs and max_sig_digits the digits a row can decide, so each
width pays only for its own need. an array length cannot call them, so a
row's sizes (F64_LIMBS and the like) spell the same arithmetic over the row's
fields, for storage declared on the stack.

Source: [`src/math/ieee.mach`](../../../src/math/ieee.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Format`](#format) | `rec` | one ieee 754 binary interchange format |
| [`Fields`](#fields-1) | `rec` | a pattern taken apart into sign, biased exponent field and stored fraction |

| On `Format` | |
| :--- | :--- |
| [`F16`](#format) | binary16, the f16 type |
| [`F32`](#format) | binary32, the f32 type |
| [`F64`](#format) | binary64, the f64 type |
| [`precision`](#precision) | significand precision in bits, the hidden bit included |
| [`exp_field_max`](#exp_field_max) | the all-ones biased exponent field that marks inf and nan |
| [`min_lsb`](#min_lsb) | exponent of the smallest subnormal's single bit, the floor every lsb rounds at |
| [`hidden`](#hidden) | the hidden bit of a normal significand |
| [`sign_bit`](#sign_bit) | the sign bit of a pattern |
| [`inf_bits`](#inf_bits) | the positive infinity pattern |
| [`nan_bits`](#nan_bits) | the positive quiet nan pattern |
| [`max_sig_digits`](#max_sig_digits) | significant decimal digits that can decide a rounding |
| [`max_decimal_exp`](#max_decimal_exp) | decimal magnitude past which a value is certainly inf |
| [`min_decimal_exp`](#min_decimal_exp) | decimal magnitude below which a value certainly rounds to zero |
| [`bignum_bits`](#bignum_bits) | a bound on the bits any exact conversion of f holds in one bignum |
| [`bignum_limbs`](#bignum_limbs) | the 32-bit limbs one bignum of an exact conversion of f needs |
| [`fields`](#fields) | take a pattern apart |
| [`value`](#value) | the finite value of a pattern's fields as sig * 2^exp |
| [`pack`](#pack) | the nearest pattern to (sig + d) * 2^exp, 0 \<= d \< 1, ties to even |

| Constants | |
| :--- | :--- |
| [`F16_SIG_DIGITS`](#constants) | max_sig_digits of each row, over its fields so storage can be declared from it |
| [`F32_SIG_DIGITS`](#constants), [`F64_SIG_DIGITS`](#constants) | |
| [`F16_LIMBS`](#constants) | bignum_limbs of each row, over its fields so storage can be declared from it |
| [`F32_LIMBS`](#constants), [`F64_LIMBS`](#constants) | |

---

## Format

```mach
pub rec Format {
    mant_bits: u32;
    exp_bits:  u32;
    bias:      i64;
}
```

one ieee 754 binary interchange format

every conversion accepts any row, with storage sized from it.

| Field | Type | |
| :--- | :--- | :--- |
| `mant_bits` | `u32` | stored fraction bits, the hidden leading bit excluded (52 for f64) |
| `exp_bits` | `u32` | width of the biased exponent field (11 for f64) |
| `bias` | `i64` | exponent bias (1023 for f64) |

| Name | Value | |
| :--- | :--- | :--- |
| `F16` | `Format{mant_bits: 10, exp_bits: 5, bias: 15}` | binary16, the f16 type |
| `F32` | `Format{mant_bits: 23, exp_bits: 8, bias: 127}` | binary32, the f32 type |
| `F64` | `Format{mant_bits: 52, exp_bits: 11, bias: 1023}` | binary64, the f64 type |

### precision

```mach
pub fun precision(f: Format) i64
```

significand precision in bits, the hidden bit included

### exp_field_max

```mach
pub fun exp_field_max(f: Format) i64
```

the all-ones biased exponent field that marks inf and nan

### min_lsb

```mach
pub fun min_lsb(f: Format) i64
```

exponent of the smallest subnormal's single bit, the floor every lsb rounds at

### hidden

```mach
pub fun hidden(f: Format) u128
```

the hidden bit of a normal significand

### sign_bit

```mach
pub fun sign_bit(f: Format) u128
```

the sign bit of a pattern

### inf_bits

```mach
pub fun inf_bits(f: Format) u128
```

the positive infinity pattern

### nan_bits

```mach
pub fun nan_bits(f: Format) u128
```

the positive quiet nan pattern

### max_sig_digits

```mach
pub fun max_sig_digits(f: Format) i64
```

significant decimal digits that can decide a rounding

a midpoint between adjacent values is an odd multiple of 2^(min_lsb-1), so its
decimal expansion ends bias + mant_bits places after the point, and the longest
sits just under 2^(2-bias); 1233/4096 under-estimates log10(2), so this bound is
never short. digits past it only ever matter as nonzero or not.

### max_decimal_exp

```mach
pub fun max_decimal_exp(f: Format) i64
```

decimal magnitude past which a value is certainly inf

a value M * 10^D with D + floor(bitlen(M) * log10(2)) above this exceeds
2^(bias+1), since that estimate exceeds log10 of the value by less than 1/3.

### min_decimal_exp

```mach
pub fun min_decimal_exp(f: Format) i64
```

decimal magnitude below which a value certainly rounds to zero

the same estimate below this puts the value under half the smallest subnormal,
2^(min_lsb-1), since it falls short of log10 of the value by less than 1.02.

### bignum_bits

```mach
pub fun bignum_bits(f: Format) i64
```

a bound on the bits any exact conversion of f holds in one bignum

the power of ten scaling the smallest full significand of max_sig_digits digits
(each under 3.33 bits) with a quotient's worth of bits on top.

### bignum_limbs

```mach
pub fun bignum_limbs(f: Format) usize
```

the 32-bit limbs one bignum of an exact conversion of f needs

### fields

```mach
pub fun fields(f: Format, bits: u128) Fields
```

take a pattern apart

| Parameter | |
| :--- | :--- |
| `f` | the pattern's format |
| `bits` | the pattern in the low end |
| **returns** | its sign, exponent field and fraction |

### value

```mach
pub fun value(f: Format, p: Fields, out_sig: *u128, out_exp: *i64)
```

the finite value of a pattern's fields as sig * 2^exp

| Parameter | |
| :--- | :--- |
| `f` | the pattern's format |
| `p` | fields of a finite pattern |
| `out_sig` | the significand, hidden bit included for a normal |
| `out_exp` | the exponent of the significand's lowest bit |

### pack

```mach
pub fun pack(f: Format, neg: bool, sig: u128, exp: i64, sticky: bool) u128
```

the nearest pattern to (sig + d) * 2^exp, 0 \<= d \< 1, ties to even

the one rounding every parse ends in. sticky says d > 0, and is only set when
sig carries at least one bit below the result's lsb, so the bits dropped there
and sticky decide the rounding exactly. a zero sig packs to zero, so a caller
passes it only for a value under half the smallest subnormal. a value past the
largest finite by half an ulp or more is inf.

| Parameter | |
| :--- | :--- |
| `f` | the target format |
| `neg` | the sign of the result |
| `sig` | the significand |
| `exp` | the exponent of sig's lowest bit |
| `sticky` | whether nonzero bits lie below sig |
| **returns** | the correctly rounded pattern |

## Fields

```mach
pub rec Fields {
    neg:   bool;
    field: i64;
    frac:  u128;
}
```

a pattern taken apart into sign, biased exponent field and stored fraction

| Field | Type | |
| :--- | :--- | :--- |
| `neg` | `bool` | the sign bit |
| `field` | `i64` | the biased exponent field |
| `frac` | `u128` | the stored fraction bits |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `F16_SIG_DIGITS` | `usize` | `(F16.bias + F16.mant_bits::i64 + 1 - ((F16.bias - 2) * 1233) / 4096)::usize` | max_sig_digits of each row, over its fields so storage can be declared from it |
| `F32_SIG_DIGITS` | `usize` | `(F32.bias + F32.mant_bits::i64 + 1 - ((F32.bias - 2) * 1233) / 4096)::usize` |  |
| `F64_SIG_DIGITS` | `usize` | `(F64.bias + F64.mant_bits::i64 + 1 - ((F64.bias - 2) * 1233) / 4096)::usize` |  |
| `F16_LIMBS` | `usize` | `((((F16_SIG_DIGITS::i64 + ((F16.bias + F16.mant_bits::i64 + 1) * 1233) / 4096 + 3) * 3402) / 1024 + F16.mant_bits::i64 + 1 + 3 + 32 + 31) / 32)::usize` | bignum_limbs of each row, over its fields so storage can be declared from it |
| `F32_LIMBS` | `usize` | `((((F32_SIG_DIGITS::i64 + ((F32.bias + F32.mant_bits::i64 + 1) * 1233) / 4096 + 3) * 3402) / 1024 + F32.mant_bits::i64 + 1 + 3 + 32 + 31) / 32)::usize` |  |
| `F64_LIMBS` | `usize` | `((((F64_SIG_DIGITS::i64 + ((F64.bias + F64.mant_bits::i64 + 1) * 1233) / 4096 + 3) * 3402) / 1024 + F64.mant_bits::i64 + 1 + 3 + 32 + 31) / 32)::usize` |  |

