[std](../README.md) / [math](README.md) / **mat4**

# std.math.mat4

4x4 single-precision matrices over f32x4 rows

a Mat4 is an algorithm over vectors, not a language type: it is a record of
four f32x4 rows (row-major), and every operation is expressed with the
compiler's lane-wise vector operators plus scalar lane reads. the convention
is row-vector: a vector transforms as `v * M` (see mat4_mul_vec), and the
product `mat4_mul(a, b)` is the matrix applying a then b.

Source: [`src/math/mat4.mach`](../../../src/math/mat4.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Mat4`](#mat4) | `rec` | a 4x4 single-precision matrix, four f32x4 rows in row-major order |

| On `Mat4` | |
| :--- | :--- |
| [`mat4_identity`](#mat4_identity) | the 4x4 identity matrix |
| [`mat4_zero`](#mat4_zero) | the 4x4 zero matrix |
| [`mat4_add`](#mat4_add) | element-wise sum of two matrices |
| [`mat4_sub`](#mat4_sub) | element-wise difference of two matrices |
| [`mat4_scale`](#mat4_scale) | scale every element of a matrix by a scalar |
| [`mat4_mul`](#mat4_mul) | matrix product a*b (row-vector convention: applies a then b) |
| [`mat4_mul_vec`](#mat4_mul_vec) | transform a row vector by a matrix (v * m) |
| [`mat4_transpose`](#mat4_transpose) | transpose a matrix (swap rows and columns) |
| [`mat4_determinant`](#mat4_determinant) | determinant of a matrix |
| [`mat4_inverse`](#mat4_inverse) | inverse of a matrix, or none when it is singular |

---

## Mat4

```mach
pub rec Mat4 {
    rows: [4]f32x4;
}
```

a 4x4 single-precision matrix, four f32x4 rows in row-major order

| Field | Type | |
| :--- | :--- | :--- |
| `rows` | `[4]f32x4` | the four row vectors, rows[i][j] is row i column j |

### mat4_identity

```mach
pub fun mat4_identity() Mat4
```

the 4x4 identity matrix

| Parameter | |
| :--- | :--- |
| **returns** | a matrix with ones on the diagonal, zero elsewhere |

### mat4_zero

```mach
pub fun mat4_zero() Mat4
```

the 4x4 zero matrix

| Parameter | |
| :--- | :--- |
| **returns** | a matrix with every element zero |

### mat4_add

```mach
pub fun mat4_add(a: Mat4, b: Mat4) Mat4
```

element-wise sum of two matrices

| Parameter | |
| :--- | :--- |
| `a` | first matrix |
| `b` | second matrix |
| **returns** | a + b, element-wise |

### mat4_sub

```mach
pub fun mat4_sub(a: Mat4, b: Mat4) Mat4
```

element-wise difference of two matrices

| Parameter | |
| :--- | :--- |
| `a` | first matrix |
| `b` | second matrix |
| **returns** | a - b, element-wise |

### mat4_scale

```mach
pub fun mat4_scale(m: Mat4, s: f32) Mat4
```

scale every element of a matrix by a scalar

| Parameter | |
| :--- | :--- |
| `m` | matrix |
| `s` | scalar factor |
| **returns** | m with every element multiplied by s |

### mat4_mul

```mach
pub fun mat4_mul(a: Mat4, b: Mat4) Mat4
```

matrix product a*b (row-vector convention: applies a then b)

each result row is a's row recombined over b's rows, so the multiplies and
adds are lane-wise vector ops on a capable target.

| Parameter | |
| :--- | :--- |
| `a` | left matrix |
| `b` | right matrix |
| **returns** | the product a*b |

### mat4_mul_vec

```mach
pub fun mat4_mul_vec(m: Mat4, v: f32x4) f32x4
```

transform a row vector by a matrix (v * m)

| Parameter | |
| :--- | :--- |
| `m` | matrix |
| `v` | row vector |
| **returns** | the transformed vector v * m |

### mat4_transpose

```mach
pub fun mat4_transpose(m: Mat4) Mat4
```

transpose a matrix (swap rows and columns)

| Parameter | |
| :--- | :--- |
| `m` | matrix |
| **returns** | the transpose of m |

### mat4_determinant

```mach
pub fun mat4_determinant(m: Mat4) f32
```

determinant of a matrix

expanded over the six 2x2 minors of the top two rows against the six of the
bottom two: the Laplace complementary-minor form, shared with the inverse.

| Parameter | |
| :--- | :--- |
| `m` | matrix |
| **returns** | det(m) |

### mat4_inverse

```mach
pub fun mat4_inverse(m: Mat4) opt[Mat4]
```

inverse of a matrix, or none when it is singular

builds the adjugate over the same complementary 2x2 minors as the determinant,
then scales by its reciprocal. a determinant of exactly zero is mathematical
absence: there is no inverse, so the answer is none.

| Parameter | |
| :--- | :--- |
| `m` | matrix |
| **returns** | some{inverse} if invertible, none if singular |

