[std](../README.md) / [math](README.md) / **quat**

# std.math.quat

quaternions over f32x4

a quaternion is stored in an f32x4 as {x, y, z, w}: the vector part in lanes
0-2 and the real part in lane 3. operations are algorithms over the lane-wise
vector operators and scalar lane reads, with no bit reinterpret at vector width,
so correct on every target.

the reciprocal square root normalization needs, and the acos/sin true slerp
needs, come from the shared std.math.float module.

Source: [`src/math/quat.mach`](../../../src/math/quat.mach)

| Functions | |
| :--- | :--- |
| [`quat_identity`](#quat_identity) | the identity quaternion (no rotation) |
| [`quat_mul`](#quat_mul) | Hamilton product of two quaternions (composition of rotations) |
| [`quat_conjugate`](#quat_conjugate) | conjugate of a quaternion (negate the vector part) |
| [`quat_dot`](#quat_dot) | dot product of two quaternions |
| [`quat_length`](#quat_length) | length (magnitude) of a quaternion |
| [`quat_normalize`](#quat_normalize) | normalize a quaternion to unit length |
| [`quat_nlerp`](#quat_nlerp) | normalized linear interpolation between two quaternions |
| [`quat_slerp`](#quat_slerp) | spherical linear interpolation between two unit quaternions |

---

## Functions

### quat_identity

```mach
pub fun quat_identity() f32x4
```

the identity quaternion (no rotation)

| Parameter | |
| :--- | :--- |
| **returns** | {0, 0, 0, 1} |

### quat_mul

```mach
pub fun quat_mul(a: f32x4, b: f32x4) f32x4
```

Hamilton product of two quaternions (composition of rotations)

| Parameter | |
| :--- | :--- |
| `a` | left quaternion, applied second |
| `b` | right quaternion, applied first |
| **returns** | the composed quaternion a*b |

### quat_conjugate

```mach
pub fun quat_conjugate(q: f32x4) f32x4
```

conjugate of a quaternion (negate the vector part)

for a unit quaternion this is the inverse rotation.

| Parameter | |
| :--- | :--- |
| `q` | input quaternion |
| **returns** | {-x, -y, -z, w} |

### quat_dot

```mach
pub fun quat_dot(a: f32x4, b: f32x4) f32
```

dot product of two quaternions

| Parameter | |
| :--- | :--- |
| `a` | first quaternion |
| `b` | second quaternion |
| **returns** | a . b |

### quat_length

```mach
pub fun quat_length(q: f32x4) f32
```

length (magnitude) of a quaternion

| Parameter | |
| :--- | :--- |
| `q` | input quaternion |
| **returns** | sqrt(q . q) |

### quat_normalize

```mach
pub fun quat_normalize(q: f32x4) f32x4
```

normalize a quaternion to unit length

scaling by the reciprocal length is a single lane-wise vector multiply.

| Parameter | |
| :--- | :--- |
| `q` | input quaternion (must be non-zero) |
| **returns** | q / \|q\| |

### quat_nlerp

```mach
pub fun quat_nlerp(a: f32x4, b: f32x4, t: f32) f32x4
```

normalized linear interpolation between two quaternions

lerps the components then renormalizes, taking the shortest arc by flipping b
when the quaternions face opposite hemispheres. cheaper than true slerp and a
close approximation for nearby rotations; `quat_slerp` is the exact,
constant-angular-velocity interpolation.

| Parameter | |
| :--- | :--- |
| `a` | start quaternion (unit) |
| `b` | end quaternion (unit) |
| `t` | interpolation factor in [0, 1] |
| **returns** | the interpolated unit quaternion |

### quat_slerp

```mach
pub fun quat_slerp(a: f32x4, b: f32x4, t: f32) f32x4
```

spherical linear interpolation between two unit quaternions

traces the shortest great-circle arc at constant angular velocity: flips b to
the near hemisphere, then weights the endpoints by sin((1-t)*theta)/sin(theta)
and sin(t*theta)/sin(theta) where theta is the angle between them. as the two
quaternions approach coincidence sin(theta) -> 0 and the weights are
ill-conditioned, so a near-parallel arc falls back to the normalized lerp,
the exact limit there, not an approximation.

| Parameter | |
| :--- | :--- |
| `a` | start quaternion (unit) |
| `b` | end quaternion (unit) |
| `t` | interpolation factor in [0, 1] |
| **returns** | the interpolated unit quaternion |

