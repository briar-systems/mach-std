[std](../README.md) / [simd](README.md) / **gather**

# std.simd.gather

gather / scatter over the seeded 128-bit vector types

gather loads one lane per index from a base array; scatter stores each lane to
its index. lane indices into the result/source vector are comptime constants,
so each is a fixed sequence of indexed pointer accesses — the defined scalar
form of a masked gather, correct on every target. the memory indices
themselves are ordinary runtime values carried in a u32x4.

Source: [`src/simd/gather.mach`](../../../src/simd/gather.mach)

| Functions | |
| :--- | :--- |
| [`gather_f32x4`](#gather_f32x4) | gather four f32 lanes from base at the four u32 indices |
| [`gather_i32x4`](#gather_i32x4) | gather four i32 lanes from base at the four u32 indices |
| [`gather_u32x4`](#gather_u32x4) | gather four u32 lanes from base at the four u32 indices |
| [`scatter_f32x4`](#scatter_f32x4) | scatter four f32 lanes to base at the four u32 indices |
| [`scatter_i32x4`](#scatter_i32x4) | scatter four i32 lanes to base at the four u32 indices |

---

## Functions

### gather_f32x4

```mach
pub fun gather_f32x4(base: *f32, idx: u32x4) f32x4
```

gather four f32 lanes from base at the four u32 indices

| Parameter | |
| :--- | :--- |
| `base` | pointer to the source array |
| `idx` | per-lane element indices into base |
| **returns** | {base[idx[0]], base[idx[1]], base[idx[2]], base[idx[3]]} |

### gather_i32x4

```mach
pub fun gather_i32x4(base: *i32, idx: u32x4) i32x4
```

gather four i32 lanes from base at the four u32 indices

| Parameter | |
| :--- | :--- |
| `base` | pointer to the source array |
| `idx` | per-lane element indices into base |
| **returns** | {base[idx[0]], base[idx[1]], base[idx[2]], base[idx[3]]} |

### gather_u32x4

```mach
pub fun gather_u32x4(base: *u32, idx: u32x4) u32x4
```

gather four u32 lanes from base at the four u32 indices

| Parameter | |
| :--- | :--- |
| `base` | pointer to the source array |
| `idx` | per-lane element indices into base |
| **returns** | {base[idx[0]], base[idx[1]], base[idx[2]], base[idx[3]]} |

### scatter_f32x4

```mach
pub fun scatter_f32x4(base: *f32, idx: u32x4, v: f32x4)
```

scatter four f32 lanes to base at the four u32 indices

| Parameter | |
| :--- | :--- |
| `base` | pointer to the destination array |
| `idx` | per-lane element indices into base |
| `v` | lanes to store, v[i] written to base[idx[i]] |

### scatter_i32x4

```mach
pub fun scatter_i32x4(base: *i32, idx: u32x4, v: i32x4)
```

scatter four i32 lanes to base at the four u32 indices

| Parameter | |
| :--- | :--- |
| `base` | pointer to the destination array |
| `idx` | per-lane element indices into base |
| `v` | lanes to store, v[i] written to base[idx[i]] |

