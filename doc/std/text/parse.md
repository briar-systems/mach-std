[std](../README.md) / [text](README.md) / **parse**

# std.text.parse

number parsing utilities

Source: [`src/text/parse.mach`](../../../src/text/parse.mach)

Uses types from [`std.math.ieee`](../math/ieee.md).

| Type | | |
| :--- | :--- | :--- |
| [`ParseError`](#parseerror) | `tag` | every way a number parse can fail |
| [`Radix`](#radix) | `tag` | which literal form a float parse reads |
| [`F16ParseWork`](#f16parsework) | `def` | parse_float work storage for each row, a u32 array a caller declares and passes as ?work[0]: PARSE_BIGNUMS bignums of the row's limbs, the length parse_float_work gives |
| [`F32ParseWork`](#f32parsework) | `def` |  |
| [`F64ParseWork`](#f64parsework) | `def` |  |

| On `ParseError` | |
| :--- | :--- |
| [`parse_u64`](#parse_u64) | parse an unsigned 64-bit integer prefix from a string |
| [`parse_u64_exact`](#parse_u64_exact) | parse an unsigned 64-bit integer from a string, requiring full consumption |
| [`parse_i64`](#parse_i64) | parse a signed 64-bit integer prefix from a string |
| [`parse_i64_exact`](#parse_i64_exact) | parse a signed 64-bit integer from a string, requiring full consumption |
| [`parse_u128`](#parse_u128) | parse an unsigned 128-bit integer prefix from a string, as parse_u64 does |
| [`parse_u128_exact`](#parse_u128_exact) | parse an unsigned 128-bit integer from a string, requiring full consumption, as parse_u64_exact does |
| [`parse_u256`](#parse_u256) | parse an unsigned 256-bit integer prefix from a string, as parse_u64 does |
| [`parse_u256_exact`](#parse_u256_exact) | parse an unsigned 256-bit integer from a string, requiring full consumption, as parse_u64_exact does |
| [`parse_u512`](#parse_u512) | parse an unsigned 512-bit integer prefix from a string, as parse_u64 does |
| [`parse_u512_exact`](#parse_u512_exact) | parse an unsigned 512-bit integer from a string, requiring full consumption, as parse_u64_exact does |
| [`parse_i128`](#parse_i128) | parse an signed 128-bit integer prefix from a string, as parse_i64 does |
| [`parse_i128_exact`](#parse_i128_exact) | parse an signed 128-bit integer from a string, requiring full consumption, as parse_i64_exact does |
| [`parse_i256`](#parse_i256) | parse an signed 256-bit integer prefix from a string, as parse_i64 does |
| [`parse_i256_exact`](#parse_i256_exact) | parse an signed 256-bit integer from a string, requiring full consumption, as parse_i64_exact does |
| [`parse_i512`](#parse_i512) | parse an signed 512-bit integer prefix from a string, as parse_i64 does |
| [`parse_i512_exact`](#parse_i512_exact) | parse an signed 512-bit integer from a string, requiring full consumption, as parse_i64_exact does |
| [`parse_f64`](#parse_f64) | parse a 64-bit floating point number prefix from a string |
| [`parse_f64_len`](#parse_f64_len) | parse a 64-bit floating point number prefix from the first `len` bytes of `s` |
| [`parse_f64_exact`](#parse_f64_exact) | parse a 64-bit floating point number from a string, requiring full consumption |
| [`parse_f32`](#parse_f32) | parse a 32-bit floating point number prefix from a string |
| [`parse_f32_len`](#parse_f32_len) | parse a 32-bit floating point number prefix from the first `len` bytes of `s` |
| [`parse_f32_exact`](#parse_f32_exact) | parse a 32-bit floating point number from a string, requiring full consumption |
| [`parse_f16`](#parse_f16) | parse a 16-bit floating point number prefix from a string |
| [`parse_f16_len`](#parse_f16_len) | parse a 16-bit floating point number prefix from the first `len` bytes of `s` |
| [`parse_f16_exact`](#parse_f16_exact) | parse a 16-bit floating point number from a string, requiring full consumption |
| [`parse_f64_hex`](#parse_f64_hex) | parse a 64-bit C99 hex float prefix from a string |
| [`parse_f64_hex_len`](#parse_f64_hex_len) | parse a 64-bit C99 hex float prefix from the first `len` bytes of `s` |
| [`parse_f64_hex_exact`](#parse_f64_hex_exact) | parse a 64-bit C99 hex float from a string, requiring full consumption |
| [`parse_f32_hex`](#parse_f32_hex) | parse a 32-bit C99 hex float prefix from a string |
| [`parse_f32_hex_len`](#parse_f32_hex_len) | parse a 32-bit C99 hex float prefix from the first `len` bytes of `s` |
| [`parse_f32_hex_exact`](#parse_f32_hex_exact) | parse a 32-bit C99 hex float from a string, requiring full consumption |
| [`parse_f16_hex`](#parse_f16_hex) | parse a 16-bit C99 hex float prefix from a string |
| [`parse_f16_hex_len`](#parse_f16_hex_len) | parse a 16-bit C99 hex float prefix from the first `len` bytes of `s` |
| [`parse_f16_hex_exact`](#parse_f16_hex_exact) | parse a 16-bit C99 hex float from a string, requiring full consumption |

| On `Radix` | |
| :--- | :--- |
| [`parse_float`](#parse_float) | parse a float of any ieee.Format row from the first `len` bytes of `s` |

| Functions | |
| :--- | :--- |
| [`parse_float_work`](#parse_float_work) | the u32 words of work storage parse_float needs for format f |

---

## ParseError

```mach
pub tag ParseError: u8 {
    empty;
    syntax:   usize;
    overflow: usize;
    base:     u8;
}
```

every way a number parse can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `empty` |  | nothing to parse (an empty string, or only whitespace) |
| `syntax` | `usize` | the byte at the payload offset is not part of a valid number |
| `overflow` | `usize` | the value does not fit; payload is the offset at which the overflow was detected |
| `base` | `u8` | the requested base is outside 2..36; payload is that base |

### parse_u64

```mach
pub fun parse_u64(s: str, base: u8) res[u64, ParseError]
```

parse an unsigned 64-bit integer prefix from a string

stops at the first character that is not a valid digit for the given base,
returning the value parsed so far. use parse_u64_exact to require full
input consumption.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or an error message |

### parse_u64_exact

```mach
pub fun parse_u64_exact(s: str, base: u8) res[u64, ParseError]
```

parse an unsigned 64-bit integer from a string, requiring full consumption

returns an error if there are any characters remaining after the number.
leading whitespace is also rejected.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or an error message |

### parse_i64

```mach
pub fun parse_i64(s: str, base: u8) res[i64, ParseError]
```

parse a signed 64-bit integer prefix from a string

delegates to parse_u64 for the unsigned portion, so it inherits the same
prefix-parsing behavior. use parse_i64_exact to require full input
consumption.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or an error message |

### parse_i64_exact

```mach
pub fun parse_i64_exact(s: str, base: u8) res[i64, ParseError]
```

parse a signed 64-bit integer from a string, requiring full consumption

returns an error if there are any characters remaining after the number.
leading whitespace is also rejected.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or an error message |

### parse_u128

```mach
pub fun parse_u128(s: str, base: u8) res[u128, ParseError]
```

parse an unsigned 128-bit integer prefix from a string, as parse_u64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_u128_exact

```mach
pub fun parse_u128_exact(s: str, base: u8) res[u128, ParseError]
```

parse an unsigned 128-bit integer from a string, requiring full consumption, as parse_u64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_u256

```mach
pub fun parse_u256(s: str, base: u8) res[u256, ParseError]
```

parse an unsigned 256-bit integer prefix from a string, as parse_u64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_u256_exact

```mach
pub fun parse_u256_exact(s: str, base: u8) res[u256, ParseError]
```

parse an unsigned 256-bit integer from a string, requiring full consumption, as parse_u64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_u512

```mach
pub fun parse_u512(s: str, base: u8) res[u512, ParseError]
```

parse an unsigned 512-bit integer prefix from a string, as parse_u64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_u512_exact

```mach
pub fun parse_u512_exact(s: str, base: u8) res[u512, ParseError]
```

parse an unsigned 512-bit integer from a string, requiring full consumption, as parse_u64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i128

```mach
pub fun parse_i128(s: str, base: u8) res[i128, ParseError]
```

parse an signed 128-bit integer prefix from a string, as parse_i64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i128_exact

```mach
pub fun parse_i128_exact(s: str, base: u8) res[i128, ParseError]
```

parse an signed 128-bit integer from a string, requiring full consumption, as parse_i64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i256

```mach
pub fun parse_i256(s: str, base: u8) res[i256, ParseError]
```

parse an signed 256-bit integer prefix from a string, as parse_i64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i256_exact

```mach
pub fun parse_i256_exact(s: str, base: u8) res[i256, ParseError]
```

parse an signed 256-bit integer from a string, requiring full consumption, as parse_i64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i512

```mach
pub fun parse_i512(s: str, base: u8) res[i512, ParseError]
```

parse an signed 512-bit integer prefix from a string, as parse_i64 does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_i512_exact

```mach
pub fun parse_i512_exact(s: str, base: u8) res[i512, ParseError]
```

parse an signed 512-bit integer from a string, requiring full consumption, as parse_i64_exact does

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| `base` | numeric base (2-36), or 0 for auto-detect (0x, 0b, 0o prefixes) |
| **returns** | the parsed value, or the error |

### parse_f64

```mach
pub fun parse_f64(s: str) res[f64, ParseError]
```

parse a 64-bit floating point number prefix from a string

decimal, correctly rounded, as parse_float describes. skips leading whitespace
and stops at the first character that is not part of a valid float.
use parse_f64_exact to require full input consumption, or parse_f64_len for a
span that is not null-terminated.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f64_len

```mach
pub fun parse_f64_len(s: str, len: usize) res[f64, ParseError]
```

parse a 64-bit floating point number prefix from the first `len` bytes of `s`

like parse_f64 but bounded by an explicit length instead of a null terminator,
so it is safe on a byte span embedded in a larger buffer (e.g. a zero-copy
slice into a parse input). stops at the first byte that is not part of a valid
float, or at `len`.

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f64_exact

```mach
pub fun parse_f64_exact(s: str) res[f64, ParseError]
```

parse a 64-bit floating point number from a string, requiring full consumption

handles optional sign, integer part, fractional part, and exponent.
also handles special values inf, -inf, nan, +inf, +nan. returns an error if there are any
characters remaining after the number. leading whitespace is also rejected.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f32

```mach
pub fun parse_f32(s: str) res[f32, ParseError]
```

parse a 32-bit floating point number prefix from a string

correctly rounded at f32's own precision, never through f64. otherwise as
parse_f64.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f32_len

```mach
pub fun parse_f32_len(s: str, len: usize) res[f32, ParseError]
```

parse a 32-bit floating point number prefix from the first `len` bytes of `s`

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f32_exact

```mach
pub fun parse_f32_exact(s: str) res[f32, ParseError]
```

parse a 32-bit floating point number from a string, requiring full consumption

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f16

```mach
pub fun parse_f16(s: str) res[f16, ParseError]
```

parse a 16-bit floating point number prefix from a string

correctly rounded at f16's own precision, never through a wider format.
otherwise as parse_f64.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f16_len

```mach
pub fun parse_f16_len(s: str, len: usize) res[f16, ParseError]
```

parse a 16-bit floating point number prefix from the first `len` bytes of `s`

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f16_exact

```mach
pub fun parse_f16_exact(s: str) res[f16, ParseError]
```

parse a 16-bit floating point number from a string, requiring full consumption

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f64_hex

```mach
pub fun parse_f64_hex(s: str) res[f64, ParseError]
```

parse a 64-bit C99 hex float prefix from a string

`0x` then hex digits with an optional point and an optional `p` exponent, as
parse_float describes, rounded half to even at f64's own precision. skips
leading whitespace and stops at the first character past the float.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f64_hex_len

```mach
pub fun parse_f64_hex_len(s: str, len: usize) res[f64, ParseError]
```

parse a 64-bit C99 hex float prefix from the first `len` bytes of `s`

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f64_hex_exact

```mach
pub fun parse_f64_hex_exact(s: str) res[f64, ParseError]
```

parse a 64-bit C99 hex float from a string, requiring full consumption

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f32_hex

```mach
pub fun parse_f32_hex(s: str) res[f32, ParseError]
```

parse a 32-bit C99 hex float prefix from a string

`0x` then hex digits with an optional point and an optional `p` exponent, as
parse_float describes, rounded half to even at f32's own precision. skips
leading whitespace and stops at the first character past the float.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f32_hex_len

```mach
pub fun parse_f32_hex_len(s: str, len: usize) res[f32, ParseError]
```

parse a 32-bit C99 hex float prefix from the first `len` bytes of `s`

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f32_hex_exact

```mach
pub fun parse_f32_hex_exact(s: str) res[f32, ParseError]
```

parse a 32-bit C99 hex float from a string, requiring full consumption

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f16_hex

```mach
pub fun parse_f16_hex(s: str) res[f16, ParseError]
```

parse a 16-bit C99 hex float prefix from a string

`0x` then hex digits with an optional point and an optional `p` exponent, as
parse_float describes, rounded half to even at f16's own precision. skips
leading whitespace and stops at the first character past the float.

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

### parse_f16_hex_len

```mach
pub fun parse_f16_hex_len(s: str, len: usize) res[f16, ParseError]
```

parse a 16-bit C99 hex float prefix from the first `len` bytes of `s`

| Parameter | |
| :--- | :--- |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| **returns** | the parsed value, or an error message |

### parse_f16_hex_exact

```mach
pub fun parse_f16_hex_exact(s: str) res[f16, ParseError]
```

parse a 16-bit C99 hex float from a string, requiring full consumption

| Parameter | |
| :--- | :--- |
| `s` | string to parse |
| **returns** | the parsed value, or an error message |

## Radix

```mach
pub tag Radix: u8 {
    decimal;
    hex;
}
```

which literal form a float parse reads

| Case | Payload | |
| :--- | :--- | :--- |
| `decimal` |  | digits with an optional point and an optional `e` exponent |
| `hex` |  | a C99 hex float, `0x` or `0X` then hex digits with an optional point and an optional `p` exponent |

### parse_float

```mach
pub fun parse_float(f: std.math.ieee.Format, radix: Radix, s: str, len: usize, whole: bool, work: *u32) res[u128, ParseError]
```

parse a float of any ieee.Format row from the first `len` bytes of `s`

the one parse every width and radix runs. accepts an optional sign, then `inf`,
`nan`, or a literal of the given radix, with `_` separators between digits.
both radices round to nearest, ties to even, at the format's own precision,
into the subnormal range and to inf. a sign before `nan` is ignored. a decimal
parse never reads hex: `0x1p3` is the decimal 0 followed by a stray `x`.

| Parameter | |
| :--- | :--- |
| `f` | the format to round into |
| `radix` | the literal form to read |
| `s` | the bytes to parse |
| `len` | the number of bytes available in s |
| `whole` | require the span be the number exactly, with no leading whitespace or trailing byte; otherwise skip leading whitespace and stop at the first byte that is not part of a float |
| `work` | storage a decimal parse works in, a row's ParseWork type (F64ParseWork for ieee.F64) or parse_float_work(f) u32 words; a hex parse never touches it |
| **returns** | the pattern in the low end, or the failure |

## F16ParseWork

```mach
pub def F16ParseWork:  [PARSE_BIGNUMS * ieee.F16_LIMBS]u32
```

parse_float work storage for each row, a u32 array a caller declares and
passes as ?work[0]: PARSE_BIGNUMS bignums of the row's limbs, the length
parse_float_work gives

## F32ParseWork

```mach
pub def F32ParseWork:  [PARSE_BIGNUMS * ieee.F32_LIMBS]u32
```

## F64ParseWork

```mach
pub def F64ParseWork:  [PARSE_BIGNUMS * ieee.F64_LIMBS]u32
```

## Functions

### parse_float_work

```mach
pub fun parse_float_work(f: std.math.ieee.Format) usize
```

the u32 words of work storage parse_float needs for format f

| Parameter | |
| :--- | :--- |
| `f` | the format a parse rounds into |
| **returns** | the words, PARSE_BIGNUMS bignums of ieee.bignum_limbs(f) limbs |

