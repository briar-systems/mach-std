[std](../README.md) / [simd](README.md) / **saturate**

# std.simd.saturate

saturating (clamping) arithmetic over the seeded vector types

there is no lane-wise saturating operator, so each is built from the wrapping
lane-wise op plus an overflow mask — the `paddus`/`psubs`-class behavior
expressed in portable Mach.

unsigned add saturates to all-ones on carry-out; unsigned subtract saturates
to zero on borrow. these need no bit reinterpret: the overflow mask is an
unsigned comparison in the operand's own type.

signed add/sub saturate to the type's [MIN, MAX]. overflow is detected in the
mask domain from the operand and result sign bits — a signed compare against
zero yields the sign mask — and the saturated lanes are chosen with the
`select` blend (whose `:~` reinterpret is the only bitwise touch a signed
vector allows). overflow on add needs equal operand signs; on subtract,
opposite signs; either way the result sign must differ from the minuend's.

Source: [`src/simd/saturate.mach`](../../../src/simd/saturate.mach)

| Functions | |
| :--- | :--- |
| [`adds_u8x16`](#adds_u8x16) | saturating unsigned add of u8x16 lanes (clamps to 0xFF) |
| [`subs_u8x16`](#subs_u8x16) | saturating unsigned subtract of u8x16 lanes (clamps to 0) |
| [`adds_u16x8`](#adds_u16x8) | saturating unsigned add of u16x8 lanes (clamps to 0xFFFF) |
| [`subs_u16x8`](#subs_u16x8) | saturating unsigned subtract of u16x8 lanes (clamps to 0) |
| [`adds_i8x16`](#adds_i8x16) | saturating signed add of i8x16 lanes (clamps to [-128, 127]) |
| [`subs_i8x16`](#subs_i8x16) | saturating signed subtract of i8x16 lanes (clamps to [-128, 127]) |
| [`adds_i16x8`](#adds_i16x8) | saturating signed add of i16x8 lanes (clamps to [-32768, 32767]) |
| [`subs_i16x8`](#subs_i16x8) | saturating signed subtract of i16x8 lanes (clamps to [-32768, 32767]) |

---

## Functions

### adds_u8x16

```mach
pub fun adds_u8x16(a: u8x16, b: u8x16) u8x16
```

saturating unsigned add of u8x16 lanes (clamps to 0xFF)

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | lane-wise min(a + b, 0xFF) |

### subs_u8x16

```mach
pub fun subs_u8x16(a: u8x16, b: u8x16) u8x16
```

saturating unsigned subtract of u8x16 lanes (clamps to 0)

| Parameter | |
| :--- | :--- |
| `a` | minuend |
| `b` | subtrahend |
| **returns** | lane-wise max(a - b, 0) |

### adds_u16x8

```mach
pub fun adds_u16x8(a: u16x8, b: u16x8) u16x8
```

saturating unsigned add of u16x8 lanes (clamps to 0xFFFF)

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | lane-wise min(a + b, 0xFFFF) |

### subs_u16x8

```mach
pub fun subs_u16x8(a: u16x8, b: u16x8) u16x8
```

saturating unsigned subtract of u16x8 lanes (clamps to 0)

| Parameter | |
| :--- | :--- |
| `a` | minuend |
| `b` | subtrahend |
| **returns** | lane-wise max(a - b, 0) |

### adds_i8x16

```mach
pub fun adds_i8x16(a: i8x16, b: i8x16) i8x16
```

saturating signed add of i8x16 lanes (clamps to [-128, 127])

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | lane-wise clamp(a + b, -128, 127) |

### subs_i8x16

```mach
pub fun subs_i8x16(a: i8x16, b: i8x16) i8x16
```

saturating signed subtract of i8x16 lanes (clamps to [-128, 127])

| Parameter | |
| :--- | :--- |
| `a` | minuend |
| `b` | subtrahend |
| **returns** | lane-wise clamp(a - b, -128, 127) |

### adds_i16x8

```mach
pub fun adds_i16x8(a: i16x8, b: i16x8) i16x8
```

saturating signed add of i16x8 lanes (clamps to [-32768, 32767])

| Parameter | |
| :--- | :--- |
| `a` | first operand |
| `b` | second operand |
| **returns** | lane-wise clamp(a + b, -32768, 32767) |

### subs_i16x8

```mach
pub fun subs_i16x8(a: i16x8, b: i16x8) i16x8
```

saturating signed subtract of i16x8 lanes (clamps to [-32768, 32767])

| Parameter | |
| :--- | :--- |
| `a` | minuend |
| `b` | subtrahend |
| **returns** | lane-wise clamp(a - b, -32768, 32767) |

