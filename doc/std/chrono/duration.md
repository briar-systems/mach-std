[std](../README.md) / [chrono](README.md) / **duration**

# std.chrono.duration

elapsed time representation and conversion

Duration represents elapsed time as nanoseconds (i64).

Source: [`src/chrono/duration.mach`](../../../src/chrono/duration.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Duration`](#duration) | `def` | elapsed time in nanoseconds |

| On `Duration` | |
| :--- | :--- |
| [`NANOSECOND`](#duration), [`MICROSECOND`](#duration), [`MILLISECOND`](#duration), [`SECOND`](#duration), [`MINUTE`](#duration), [`HOUR`](#duration) | |
| [`duration_nsec`](#duration_nsec) | return the duration as nanoseconds |
| [`duration_usec`](#duration_usec) | return the duration as microseconds |
| [`duration_msec`](#duration_msec) | return the duration as milliseconds |
| [`duration_sec`](#duration_sec) | return the duration as whole seconds |
| [`duration_min`](#duration_min) | return the duration as whole minutes |
| [`duration_hour`](#duration_hour) | return the duration as whole hours |
| [`duration_abs`](#duration_abs) | return the absolute value of d |
| [`format_duration`](#format_duration) | render d as a compact ASCII human-readable string into buf |

---

## Duration

```mach
pub def Duration: i64
```

elapsed time in nanoseconds

| Name | Value | |
| :--- | :--- | :--- |
| `NANOSECOND` | `1` |  |
| `MICROSECOND` | `1000` |  |
| `MILLISECOND` | `1000000` |  |
| `SECOND` | `1000000000` |  |
| `MINUTE` | `60 * SECOND` |  |
| `HOUR` | `60 * MINUTE` |  |

### duration_nsec

```mach
pub fun duration_nsec(d: Duration) i64
```

return the duration as nanoseconds

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in nanoseconds |

### duration_usec

```mach
pub fun duration_usec(d: Duration) i64
```

return the duration as microseconds

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in microseconds |

### duration_msec

```mach
pub fun duration_msec(d: Duration) i64
```

return the duration as milliseconds

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in milliseconds |

### duration_sec

```mach
pub fun duration_sec(d: Duration) i64
```

return the duration as whole seconds

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in seconds |

### duration_min

```mach
pub fun duration_min(d: Duration) i64
```

return the duration as whole minutes

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in minutes |

### duration_hour

```mach
pub fun duration_hour(d: Duration) i64
```

return the duration as whole hours

| Parameter | |
| :--- | :--- |
| `d` | duration to convert |
| **returns** | duration in hours |

### duration_abs

```mach
pub fun duration_abs(d: Duration) Duration
```

return the absolute value of d

| Parameter | |
| :--- | :--- |
| `d` | duration to take absolute value of |
| **returns** | \|d\|, or the largest Duration when d is the most negative one |

### format_duration

```mach
pub fun format_duration(d: Duration, buf: *u8, cap: usize) str
```

render d as a compact ASCII human-readable string into buf

| Parameter | |
| :--- | :--- |
| `d` | duration to render |
| `buf` | caller-provided byte buffer |
| `cap` | capacity of buf in bytes |
| **returns** | buf as a null-terminated str, or nil if cap is insufficient |

