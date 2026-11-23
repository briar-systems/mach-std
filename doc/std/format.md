[std](README.md) / **format**

# std.format

formatting primitives

writes formatted data to any io.Writer without allocation.

format strings fill `{}` holes from the arguments in order, each rendered by
its type: signed/unsigned integers (8 to 512 bits) in decimal, str as text, ptr as
0x-hex, and f64, f32 and f16 each as the shortest decimal that round-trips at
its own width, what write_f64, write_f32 and write_f16 write, so the f32
nearest 0.1 prints as `0.1`. bool is u1 and char is u8, so they render as their
numeric value, a bool prints 1 or 0. reach for the `{:c}` spec
to render an integer's low byte as a character.

a hole may carry a spec after `:`, a leading `<` to left-align (pad on the
right), `x`/`X` for lower/upper hex, `b` for binary, `c` for a low-byte char, a
decimal minimum width, and a leading `0` to zero-pad rather than space-pad (e.g.
`{:x}`, `{:b}`, `{:c}`, `{:5}`, `{:<5}`, `{:08x}`). hex and binary render a
signed integer's two's-complement pattern, at 64 bits for widths up to 64 and
at its own width for i128, i256 and i512. width pads on the left (right-align)
by default. `{{` and `}}`
emit literal braces. a hole/argument count mismatch is an error in either
direction, and an argument of a type with no rendering is a compile error.

every float width writes three ways, each one algorithm over the
std.math.ieee rows: shortest round-trip decimal (write_f64, write_f32,
write_f16), canonical C99 hex (write_*_hex) and C's `%.Ng` to a fixed number of
significant digits (write_*_g), with write_float, write_float_hex and
write_float_g taking any row's bit pattern.

the write_* primitives report the writer's own outcome, a WriteError whose
payload is the prefix this call persisted before the failure. vformat, format
and sprint add the format string's failures on top as a FormatError, whose
`write` case carries the same prefix, so a caller always knows how many bytes
reached the sink.

Source: [`src/format.mach`](../../src/format.mach)

Uses types from [`std.allocator`](allocator.md), [`std.io.writer`](io/writer.md), [`std.math.ieee`](math/ieee.md).

| Type | | |
| :--- | :--- | :--- |
| [`FormatError`](#formaterror) | `tag` | every way a format can fail beyond the writer's own outcome |
| [`F16WriteWork`](#f16writework) | `def` | write_float work storage for each row, a u32 array a caller declares and passes as ?work[0]: WRITE_BIGNUMS bignums of the row's limbs, the length write_float_work gives |
| [`F32WriteWork`](#f32writework) | `def` |  |
| [`F64WriteWork`](#f64writework) | `def` |  |
| [`F16WriteGWork`](#f16writegwork) | `def` | write_float_g work storage for each row, a u32 array a caller declares and passes as ?work[0]: the row's WriteWork and the words of its digits and line (two of the row's significant digits and LINE_SLACK bytes), the length write_float_g_work gives |
| [`F32WriteGWork`](#f32writegwork) | `def` |  |
| [`F64WriteGWork`](#f64writegwork) | `def` |  |

| On `FormatError` | |
| :--- | :--- |
| [`vformat`](#vformat) | format a comptime-variadic pack into a writer (v1.7 packs) |
| [`format`](#format) | format a comptime-variadic pack into a writer |
| [`sprint`](#sprint) | format a comptime-variadic pack into a freshly allocated string |

| Functions | |
| :--- | :--- |
| [`write_bytes`](#write_bytes) | write raw bytes to a writer |
| [`write_str`](#write_str) | write a null-terminated string to a writer |
| [`write_byte`](#write_byte) | write a single byte to a writer |
| [`write_newline`](#write_newline) | write a linefeed to a writer |
| [`write_u64`](#write_u64) | write an unsigned integer in decimal |
| [`write_i64`](#write_i64) | write a signed integer in decimal |
| [`put_u64`](#put_u64) | write an unsigned integer in decimal into storage |
| [`put_i64`](#put_i64) | write a signed integer in decimal into storage |
| [`write_hex_u64`](#write_hex_u64) | write a 64-bit value in hexadecimal |
| [`write_ptr`](#write_ptr) | write a pointer as 0x followed by hex digits |
| [`write_float_work`](#write_float_work) | the u32 words of work storage write_float needs for format fmt |
| [`write_float_g_work`](#write_float_g_work) | the u32 words of work storage write_float_g needs for format fmt |
| [`write_float`](#write_float) | write a float of any ieee.Format row in shortest round-trippable decimal |
| [`write_f64`](#write_f64) | write a 64-bit float in shortest round-trippable decimal |
| [`write_f32`](#write_f32) | write a 32-bit float in shortest round-trippable decimal |
| [`write_f16`](#write_f16) | write a 16-bit float in shortest round-trippable decimal |
| [`write_float_hex`](#write_float_hex) | write a float of any ieee.Format row as a canonical C99 hex float |
| [`write_f64_hex`](#write_f64_hex) | write a 64-bit float as a canonical C99 hex float, as write_float_hex |
| [`write_f32_hex`](#write_f32_hex) | write a 32-bit float as a canonical C99 hex float, as write_float_hex |
| [`write_f16_hex`](#write_f16_hex) | write a 16-bit float as a canonical C99 hex float, as write_float_hex |
| [`write_float_g`](#write_float_g) | write a float of any ieee.Format row to a fixed number of significant digits |
| [`write_f64_g`](#write_f64_g) | write a 64-bit float to `precision` significant digits, as write_float_g |
| [`write_f32_g`](#write_f32_g) | write a 32-bit float to `precision` significant digits, as write_float_g |
| [`write_f16_g`](#write_f16_g) | write a 16-bit float to `precision` significant digits, as write_float_g |
| [`write_value`](#write_value) | write values in their default rendering, the `{}` of vformat without a format string |

| Constants | |
| :--- | :--- |
| [`DECIMAL_MAX`](#constants) | the most bytes put_u64 or put_i64 writes |

---

## FormatError

```mach
pub tag FormatError: u8 {
    syntax:     usize;
    few_holes:  usize;
    many_holes: usize;
    write:      WriteError;
    alloc:      std.allocator.Error;
}
```

every way a format can fail beyond the writer's own outcome

| Case | Payload | |
| :--- | :--- | :--- |
| `syntax` | `usize` | the format string is malformed; payload is the byte offset of the offending brace or spec |
| `few_holes` | `usize` | more arguments than holes; payload is the offset where the scan ended with an argument still unrendered |
| `many_holes` | `usize` | more holes than arguments; payload is the offset of the hole no argument fills |
| `write` | `WriteError` | the sink failed; payload carries the persisted prefix and cause |
| `alloc` | `std.allocator.Error` | sprint's result buffer was refused; nothing was written |

### vformat

```mach
pub fun vformat(w: *std.io.writer.Writer, fmt: str, va: ...) res[usize, FormatError]
```

format a comptime-variadic pack into a writer (v1.7 packs)

holes are type-directed `{}` matched to args in order: signed/unsigned int ->
decimal, str -> text, ptr -> 0xHEX, f64/f32/f16 -> shortest round-trip decimal
at its own width. specs:
`{:x}`/`{:X}` hex, `{:b}` binary, `{:c}` low-byte char, `{:N}`/`{:0N}` minimum
width (right-align), `{:<N}` left-align. `{{` and `}}` are literal-brace
escapes. the arg sequence is comptime-unrolled and monomorphized per call, so
an argument of a type with no rendering is a compile error; the format scan
stays at runtime.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `fmt` | format string |
| `va` | comptime variadic argument pack |
| **returns** | total bytes written, or the failure; a write failure carries the bytes persisted before it |

### format

```mach
pub fun format(w: *std.io.writer.Writer, fmt: str, va: ...) res[usize, FormatError]
```

format a comptime-variadic pack into a writer

thin wrapper that forwards the whole pack to vformat.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `fmt` | format string |
| `va` | comptime variadic argument pack |
| **returns** | total bytes written, or the failure |

### sprint

```mach
pub fun sprint(a: *std.allocator.Allocator, fmt: str, va: ...) res[str, FormatError]
```

format a comptime-variadic pack into a freshly allocated string

the allocating counterpart to `format`/`vformat`: renders the same `{}` holes
with identical type-directed dispatch and spec vocabulary, but returns a new
str owned by `a` rather than writing to a Writer. the result is an exact-size,
null-terminated allocation (str_len + 1 bytes), matching the std.types.string
allocating constructors and released with text.string.str_free. formats
twice: a measuring pass over vformat sizes the buffer, then a filling pass
renders into it, so no growth or trimming is needed. a format error is
reported before any allocation.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `fmt` | format string |
| `va` | comptime variadic argument pack |
| **returns** | the formatted string, or the format's failure, or alloc when the allocator refuses the buffer |

## F16WriteWork

```mach
pub def F16WriteWork:  [WRITE_BIGNUMS * ieee.F16_LIMBS]u32
```

write_float work storage for each row, a u32 array a caller declares and
passes as ?work[0]: WRITE_BIGNUMS bignums of the row's limbs, the length
write_float_work gives

## F32WriteWork

```mach
pub def F32WriteWork:  [WRITE_BIGNUMS * ieee.F32_LIMBS]u32
```

## F64WriteWork

```mach
pub def F64WriteWork:  [WRITE_BIGNUMS * ieee.F64_LIMBS]u32
```

## F16WriteGWork

```mach
pub def F16WriteGWork:  [WRITE_BIGNUMS * ieee.F16_LIMBS + (2 * ieee.F16_SIG_DIGITS + LINE_SLACK + 3) / 4]u32
```

write_float_g work storage for each row, a u32 array a caller declares and
passes as ?work[0]: the row's WriteWork and the words of its digits and line
(two of the row's significant digits and LINE_SLACK bytes), the length
write_float_g_work gives. it also serves write_float

## F32WriteGWork

```mach
pub def F32WriteGWork:  [WRITE_BIGNUMS * ieee.F32_LIMBS + (2 * ieee.F32_SIG_DIGITS + LINE_SLACK + 3) / 4]u32
```

## F64WriteGWork

```mach
pub def F64WriteGWork:  [WRITE_BIGNUMS * ieee.F64_LIMBS + (2 * ieee.F64_SIG_DIGITS + LINE_SLACK + 3) / 4]u32
```

## Functions

### write_bytes

```mach
pub fun write_bytes(w: *std.io.writer.Writer, buf: *u8, len: usize) res[usize, WriteError]
```

write raw bytes to a writer

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `buf` | source buffer |
| `len` | number of bytes to write |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_str

```mach
pub fun write_str(w: *std.io.writer.Writer, s: str) res[usize, WriteError]
```

write a null-terminated string to a writer

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `s` | string to write (nil treated as empty) |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_byte

```mach
pub fun write_byte(w: *std.io.writer.Writer, b: u8) res[usize, WriteError]
```

write a single byte to a writer

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `b` | byte to write |
| **returns** | 1 on success, or the writer's failure |

### write_newline

```mach
pub fun write_newline(w: *std.io.writer.Writer) res[usize, WriteError]
```

write a linefeed to a writer

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| **returns** | 1 on success, or the writer's failure |

### write_u64

```mach
pub fun write_u64(w: *std.io.writer.Writer, n: u64) res[usize, WriteError]
```

write an unsigned integer in decimal

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_i64

```mach
pub fun write_i64(w: *std.io.writer.Writer, n: i64) res[usize, WriteError]
```

write a signed integer in decimal

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### put_u64

```mach
pub fun put_u64(dst: *u8, n: u64) usize
```

write an unsigned integer in decimal into storage

writes exactly the bytes it returns, so storage sized for this value's
digits suffices; DECIMAL_MAX bytes hold any value

| Parameter | |
| :--- | :--- |
| `dst` | storage for the digits |
| `n` | value to format |
| **returns** | bytes written, the digits starting at dst |

### put_i64

```mach
pub fun put_i64(dst: *u8, n: i64) usize
```

write a signed integer in decimal into storage

writes exactly the bytes it returns, so storage sized for this value's sign
and digits suffices; DECIMAL_MAX bytes hold any value

| Parameter | |
| :--- | :--- |
| `dst` | storage for the sign and digits |
| `n` | value to format |
| **returns** | bytes written, a leading `-` then the digits starting at dst |

### write_hex_u64

```mach
pub fun write_hex_u64(w: *std.io.writer.Writer, n: u64, upper: bool) res[usize, WriteError]
```

write a 64-bit value in hexadecimal

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| `upper` | true for uppercase (A-F), false for lowercase (a-f) |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_ptr

```mach
pub fun write_ptr(w: *std.io.writer.Writer, p: ptr) res[usize, WriteError]
```

write a pointer as 0x followed by hex digits

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `p` | pointer to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_float_work

```mach
pub fun write_float_work(fmt: std.math.ieee.Format) usize
```

the u32 words of work storage write_float needs for format fmt

| Parameter | |
| :--- | :--- |
| `fmt` | the format written |
| **returns** | the words, WRITE_BIGNUMS bignums of ieee.bignum_limbs(fmt) limbs |

### write_float_g_work

```mach
pub fun write_float_g_work(fmt: std.math.ieee.Format) usize
```

the u32 words of work storage write_float_g needs for format fmt

| Parameter | |
| :--- | :--- |
| `fmt` | the format written |
| **returns** | the words, write_float_work(fmt) and room for ieee.max_sig_digits(fmt) digits and a line of them |

### write_float

```mach
pub fun write_float(w: *std.io.writer.Writer, fmt: std.math.ieee.Format, bits: u128, work: *u32) res[usize, WriteError]
```

write a float of any ieee.Format row in shortest round-trippable decimal

the fewest significant digits that parse back to the same value at the
format's own precision. plain notation for a decimal exponent from -3 to 17,
exponent notation (`1e-7`, `1.5e20`) past it, and `inf`, `-inf`, `nan`, `-0`.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `fmt` | the pattern's format |
| `bits` | the pattern in the low end |
| `work` | storage the digits are found in, a row's WriteWork type (F64WriteWork for ieee.F64) or write_float_work(fmt) u32 words |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f64

```mach
pub fun write_f64(w: *std.io.writer.Writer, n: f64) res[usize, WriteError]
```

write a 64-bit float in shortest round-trippable decimal

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f32

```mach
pub fun write_f32(w: *std.io.writer.Writer, n: f32) res[usize, WriteError]
```

write a 32-bit float in shortest round-trippable decimal

shortest at f32's own precision: the f32 nearest 0.1 writes as `0.1`.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f16

```mach
pub fun write_f16(w: *std.io.writer.Writer, n: f16) res[usize, WriteError]
```

write a 16-bit float in shortest round-trippable decimal

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_float_hex

```mach
pub fun write_float_hex(w: *std.io.writer.Writer, fmt: std.math.ieee.Format, bits: u128) res[usize, WriteError]
```

write a float of any ieee.Format row as a canonical C99 hex float

`%a` style: a normal value is `0x1.<hex>p<exp>`, a subnormal `0x0.<hex>p<emin>`,
zero `0x0p+0`, the fraction left-aligned in hex digits with trailing zero
digits trimmed (and the point with them), the binary exponent always signed.
`inf`, `nan` and their negatives as printf writes them. every finite value
parses back bit for bit through the std.text.parse hex parsers.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `fmt` | the pattern's format |
| `bits` | the pattern in the low end |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f64_hex

```mach
pub fun write_f64_hex(w: *std.io.writer.Writer, n: f64) res[usize, WriteError]
```

write a 64-bit float as a canonical C99 hex float, as write_float_hex

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f32_hex

```mach
pub fun write_f32_hex(w: *std.io.writer.Writer, n: f32) res[usize, WriteError]
```

write a 32-bit float as a canonical C99 hex float, as write_float_hex

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f16_hex

```mach
pub fun write_f16_hex(w: *std.io.writer.Writer, n: f16) res[usize, WriteError]
```

write a 16-bit float as a canonical C99 hex float, as write_float_hex

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_float_g

```mach
pub fun write_float_g(w: *std.io.writer.Writer, fmt: std.math.ieee.Format, bits: u128, precision: usize, work: *u32) res[usize, WriteError]
```

write a float of any ieee.Format row to a fixed number of significant digits

C's `%.Ng`: the exact value rounded half to even to `precision` significant
digits (0 counts as 1), in plain notation when its decimal exponent X after
rounding satisfies -4 \<= X \< precision and in exponent notation (`1.5e+20`, at
least two exponent digits) otherwise, trailing fractional zeros and a bare
point removed. `inf`, `nan`, their negatives and `-0` as printf writes them.
`%.9g` of an f32 and `%.17g` of an f64 round-trip.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `fmt` | the pattern's format |
| `bits` | the pattern in the low end |
| `precision` | significant digits |
| `work` | storage the digits and the line are built in, a row's WriteGWork type (F64WriteGWork for ieee.F64) or write_float_g_work(fmt) u32 words |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f64_g

```mach
pub fun write_f64_g(w: *std.io.writer.Writer, n: f64, precision: usize) res[usize, WriteError]
```

write a 64-bit float to `precision` significant digits, as write_float_g

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| `precision` | significant digits |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f32_g

```mach
pub fun write_f32_g(w: *std.io.writer.Writer, n: f32, precision: usize) res[usize, WriteError]
```

write a 32-bit float to `precision` significant digits, as write_float_g

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| `precision` | significant digits |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_f16_g

```mach
pub fun write_f16_g(w: *std.io.writer.Writer, n: f16, precision: usize) res[usize, WriteError]
```

write a 16-bit float to `precision` significant digits, as write_float_g

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `n` | value to format |
| `precision` | significant digits |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

### write_value

```mach
pub fun write_value(w: *std.io.writer.Writer, va: ...) res[usize, WriteError]
```

write values in their default rendering, the `{}` of vformat without a
format string

the same type-directed dispatch as vformat's holes: signed/unsigned integers
in decimal, str as text, ptr as 0x-hex, each float width as its own shortest
round-trippable decimal. each value of the pack is rendered in order with
nothing between them; the common call passes one. a type vformat would
refuse at runtime is refused here at instantiation, since the pack's types
are known.

| Parameter | |
| :--- | :--- |
| `w` | target writer |
| `va` | the values to render |
| **returns** | bytes written, or the writer's failure with the persisted prefix |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `DECIMAL_MAX` | `usize` | `20` | the most bytes put_u64 or put_i64 writes |

