[std](../README.md) / [simd](README.md) / **matmul**

# std.simd.matmul

widening integer dot products and matrix multiplication

a narrow element never multiplies into a wider lane on its own. each
routine here widens both operands first, then multiplies and adds. the
accumulator width is also the result width.

element widths and signedness, one row per element type:

  element  result  largest |product|   TERMS_* (exactness bound)
  i8       i32     (-128)^2   = 2^14   131071
  u8       u32     255^2      = 65025  66051
  i16      i64     (-32768)^2 = 2^30   8589934591
  u16      u64     65535^2             4295098371

signed elements accumulate in signed sums and unsigned in unsigned. there is
no mixed-signedness form. i32 and u32 elements are not offered: their largest
product needs 62 or 64 bits, so an i64 or u64 accumulator is exact for a
single term only, and there is no wider type to accumulate into. i16 into
i32 is not offered for the same reason ((-32768)^2 = 2^30, so two such
terms already overflow i32).

overflow policy: a result is exact, never wrapped, when every sum it is built
from has at most TERMS_* terms. TERMS_* is the largest count for which that
many worst-case products still fit the result type. the bound is checked
before any work: a dot product over more than TERMS_* elements, or a matmul
whose inner dimension exceeds it, returns `Error.terms` and reads and writes
nothing. a caller with a longer sum splits it into chunks of at most TERMS_*
and adds the chunk results in a type it has proven wide enough. nothing here
accumulates without bound.

the kernels run in lane form: whole-vector loads and stores are ranges
(`p[k, 4]::i32x4`), widening is the lane-wise `::` between vectors, and a
product that fits a narrower lane is taken there (i8 and u8 in 16-bit lanes,
i16 and u16 in 32-bit lanes) and widened into the accumulator. the tail of
each kernel is the plain scalar loop.

layouts: matrices are dense, row-major and contiguous, so element (r, c) of a
matrix with n columns is at `r * n + c`. `a` is rows x inner, `b` is inner x
cols and `out` is rows x cols. `out` must not overlap `a` or `b`. every
element of `out` is written.

Source: [`src/simd/matmul.mach`](../../../src/simd/matmul.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Error`](#error) | `tag` | terms: a sum would have more terms than the element type's TERMS_* bound size:  rows * inner, inner * cols or rows * cols does not fit usize |

| On `Error` | |
| :--- | :--- |
| [`dot_i8`](#dot_i8) | exact dot product of two i8 sequences, accumulated in i32 |
| [`dot_u8`](#dot_u8) | exact dot product of two u8 sequences, accumulated in u32 |
| [`dot_i16`](#dot_i16) | exact dot product of two i16 sequences, accumulated in i64 |
| [`dot_u16`](#dot_u16) | exact dot product of two u16 sequences, accumulated in u64 |
| [`matmul_i8`](#matmul_i8) | exact product of two i8 matrices into i32, accumulated in i32 |
| [`matmul_u8`](#matmul_u8) | exact product of two u8 matrices into u32, accumulated in u32 |
| [`matmul_i16`](#matmul_i16) | exact product of two i16 matrices into i64, accumulated in i64 |
| [`matmul_u16`](#matmul_u16) | exact product of two u16 matrices into u64, accumulated in u64 |

| Constants | |
| :--- | :--- |
| [`TERMS_I8`](#constants) | the most i8 products an i32 sum holds exactly |
| [`TERMS_U8`](#constants) | the most u8 products a u32 sum holds exactly |
| [`TERMS_I16`](#constants) | the most i16 products an i64 sum holds exactly |
| [`TERMS_U16`](#constants) | the most u16 products a u64 sum holds exactly |

---

## Error

```mach
pub tag Error: u8 {
    terms;
    size;
}
```

terms: a sum would have more terms than the element type's TERMS_* bound
size:  rows * inner, inner * cols or rows * cols does not fit usize

### dot_i8

```mach
pub fun dot_i8(a: *i8, b: *i8, n: usize) res[i32, Error]
```

exact dot product of two i8 sequences, accumulated in i32

| Parameter | |
| :--- | :--- |
| `a` | first sequence, n elements |
| `b` | second sequence, n elements |
| `n` | element count, at most TERMS_I8 |
| **returns** | the sum of a[k] * b[k], or `Error.terms` when n exceeds TERMS_I8 |

### dot_u8

```mach
pub fun dot_u8(a: *u8, b: *u8, n: usize) res[u32, Error]
```

exact dot product of two u8 sequences, accumulated in u32

| Parameter | |
| :--- | :--- |
| `a` | first sequence, n elements |
| `b` | second sequence, n elements |
| `n` | element count, at most TERMS_U8 |
| **returns** | the sum of a[k] * b[k], or `Error.terms` when n exceeds TERMS_U8 |

### dot_i16

```mach
pub fun dot_i16(a: *i16, b: *i16, n: usize) res[i64, Error]
```

exact dot product of two i16 sequences, accumulated in i64

| Parameter | |
| :--- | :--- |
| `a` | first sequence, n elements |
| `b` | second sequence, n elements |
| `n` | element count, at most TERMS_I16 |
| **returns** | the sum of a[k] * b[k], or `Error.terms` when n exceeds TERMS_I16 |

### dot_u16

```mach
pub fun dot_u16(a: *u16, b: *u16, n: usize) res[u64, Error]
```

exact dot product of two u16 sequences, accumulated in u64

| Parameter | |
| :--- | :--- |
| `a` | first sequence, n elements |
| `b` | second sequence, n elements |
| `n` | element count, at most TERMS_U16 |
| **returns** | the sum of a[k] * b[k], or `Error.terms` when n exceeds TERMS_U16 |

### matmul_i8

```mach
pub fun matmul_i8(out: *i32, a: *i8, b: *i8, rows: usize, inner: usize, cols: usize) err[Error]
```

exact product of two i8 matrices into i32, accumulated in i32

the kernel runs in i-k-j order: for each (row, k) it widens a[row, k] once
and adds its product with row k of b to the output row.

| Parameter | |
| :--- | :--- |
| `out` | rows x cols output, written in full |
| `a` | rows x inner left operand |
| `b` | inner x cols right operand |
| `rows` | rows of a and out |
| `inner` | columns of a and rows of b, at most TERMS_I8 |
| `cols` | columns of b and out |
| **returns** | ok, or `Error.terms` or `Error.size` with out untouched |

### matmul_u8

```mach
pub fun matmul_u8(out: *u32, a: *u8, b: *u8, rows: usize, inner: usize, cols: usize) err[Error]
```

exact product of two u8 matrices into u32, accumulated in u32

| Parameter | |
| :--- | :--- |
| `out` | rows x cols output, written in full |
| `a` | rows x inner left operand |
| `b` | inner x cols right operand |
| `rows` | rows of a and out |
| `inner` | columns of a and rows of b, at most TERMS_U8 |
| `cols` | columns of b and out |
| **returns** | ok, or `Error.terms` or `Error.size` with out untouched |

### matmul_i16

```mach
pub fun matmul_i16(out: *i64, a: *i16, b: *i16, rows: usize, inner: usize, cols: usize) err[Error]
```

exact product of two i16 matrices into i64, accumulated in i64

| Parameter | |
| :--- | :--- |
| `out` | rows x cols output, written in full |
| `a` | rows x inner left operand |
| `b` | inner x cols right operand |
| `rows` | rows of a and out |
| `inner` | columns of a and rows of b, at most TERMS_I16 |
| `cols` | columns of b and out |
| **returns** | ok, or `Error.terms` or `Error.size` with out untouched |

### matmul_u16

```mach
pub fun matmul_u16(out: *u64, a: *u16, b: *u16, rows: usize, inner: usize, cols: usize) err[Error]
```

exact product of two u16 matrices into u64, accumulated in u64

| Parameter | |
| :--- | :--- |
| `out` | rows x cols output, written in full |
| `a` | rows x inner left operand |
| `b` | inner x cols right operand |
| `rows` | rows of a and out |
| `inner` | columns of a and rows of b, at most TERMS_U16 |
| `cols` | columns of b and out |
| **returns** | ok, or `Error.terms` or `Error.size` with out untouched |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `TERMS_I8` | `u64` | `131071` | the most i8 products an i32 sum holds exactly |
| `TERMS_U8` | `u64` | `66051` | the most u8 products a u32 sum holds exactly |
| `TERMS_I16` | `u64` | `8589934591` | the most i16 products an i64 sum holds exactly |
| `TERMS_U16` | `u64` | `4295098371` | the most u16 products a u64 sum holds exactly |

