[std](../README.md) / [chrono](README.md) / **time**

# std.chrono.time

wall-clock time and monotonic instants with nanosecond precision

Time is wall-clock time: seconds and nanoseconds since the Unix epoch
(1970-01-01 00:00:00 UTC), which can jump when the system clock is set.
Instant is monotonic: it counts from an unspecified start, never jumps, and
has no calendar meaning. the two are distinct types with no conversion, so a
deadline (always an Instant) cannot be built from the wall clock.

Source: [`src/chrono/time.mach`](../../../src/chrono/time.mach)

Uses types from [`std.io.error`](../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Clock`](#clock) | `def` | the outcome of reading the wall clock |
| [`InstantClock`](#instantclock) | `def` | the outcome of reading the monotonic clock |
| [`Elapsed`](#elapsed) | `def` | the outcome of measuring against a clock |
| [`Time`](#time) | `rec` | a wall-clock time with nanosecond precision |
| [`Instant`](#instant-1) | `rec` | a monotonic instant with nanosecond precision |

| On `Clock` | |
| :--- | :--- |
| [`now`](#now) | return the current wall-clock time |

| On `InstantClock` | |
| :--- | :--- |
| [`instant`](#instant) | return the current monotonic instant |

| On `Time` | |
| :--- | :--- |
| [`since`](#since) | return the wall-clock time elapsed since t |
| [`until`](#until) | return the wall-clock duration until t |
| [`unix`](#unix) | create a Time from a Unix timestamp |
| [`time_unix_sec`](#time_unix_sec) | return seconds since Unix epoch |
| [`time_unix_nsec`](#time_unix_nsec) | return nanoseconds since Unix epoch |
| [`time_unix_usec`](#time_unix_usec) | return microseconds since Unix epoch |
| [`time_unix_msec`](#time_unix_msec) | return milliseconds since Unix epoch |
| [`time_add`](#time_add) | return t + d |
| [`time_sub`](#time_sub) | return the duration t - u |
| [`time_before`](#time_before) | report whether t is before u |
| [`time_after`](#time_after) | report whether t is after u |
| [`time_equal`](#time_equal) | report whether t and u represent the same instant |
| [`time_is_zero`](#time_is_zero) | report whether t represents the zero time instant |

| On `Instant` | |
| :--- | :--- |
| [`elapsed`](#elapsed-1) | return the monotonic time elapsed since start |
| [`remaining`](#remaining) | return how long remains until deadline, negative once it has passed |
| [`instant_add`](#instant_add) | return i + d |
| [`instant_sub`](#instant_sub) | return the duration i - j |
| [`instant_before`](#instant_before) | report whether i is before j |
| [`instant_after`](#instant_after) | report whether i is after j |
| [`instant_equal`](#instant_equal) | report whether i and j are the same instant |

---

## Clock

```mach
pub def Clock: res[Time, std.io.error.Error]
```

the outcome of reading the wall clock

### now

Only where `capability.HAS_CLOCK`.

```mach
pub fun now() Clock
```

return the current wall-clock time

a failed clock is reported, never replaced by the zero time. never use
this for a deadline or a timeout: see `instant`

| Parameter | |
| :--- | :--- |
| **returns** | current Time from the system clock, or the native refusal |

## InstantClock

```mach
pub def InstantClock: res[Instant, std.io.error.Error]
```

the outcome of reading the monotonic clock

### instant

Only where `capability.HAS_CLOCK`.

```mach
pub fun instant() InstantClock
```

return the current monotonic instant

the clock for deadlines, timeouts and elapsed time. a deadline is
`instant_add(instant(), timeout)`

| Parameter | |
| :--- | :--- |
| **returns** | the current Instant, or the native refusal |

## Elapsed

```mach
pub def Elapsed: res[Duration, std.io.error.Error]
```

the outcome of measuring against a clock

## Time

```mach
pub rec Time {
    sec:  i64;
    nsec: i64;
}
```

a wall-clock time with nanosecond precision

for dates, timestamps and logs. never a deadline or a timeout: those are
Instants

| Field | Type | |
| :--- | :--- | :--- |
| `sec` | `i64` | seconds since Unix epoch (1970-01-01 00:00:00 UTC) |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |

### since

Only where `capability.HAS_CLOCK`.

```mach
pub fun since(t: Time) Elapsed
```

return the wall-clock time elapsed since t

this is calendar time, which can jump. for elapsed time use `elapsed`

| Parameter | |
| :--- | :--- |
| `t` | start time |
| **returns** | duration since t, or the wall clock's refusal |

### until

Only where `capability.HAS_CLOCK`.

```mach
pub fun until(t: Time) Elapsed
```

return the wall-clock duration until t

this is calendar time, which can jump. for a deadline use `remaining`

| Parameter | |
| :--- | :--- |
| `t` | target time |
| **returns** | duration until t, or the wall clock's refusal |

### unix

```mach
pub fun unix(sec: i64, nsec: i64) Time
```

create a Time from a Unix timestamp

| Parameter | |
| :--- | :--- |
| `sec` | seconds since Unix epoch |
| `nsec` | nanoseconds within second |
| **returns** | Time with nsec normalized to [0, 999999999] |

### time_unix_sec

```mach
pub fun time_unix_sec(t: Time) i64
```

return seconds since Unix epoch

| Parameter | |
| :--- | :--- |
| `t` | time to query |
| **returns** | seconds component |

### time_unix_nsec

```mach
pub fun time_unix_nsec(t: Time) i64
```

return nanoseconds since Unix epoch

| Parameter | |
| :--- | :--- |
| `t` | time to query |
| **returns** | total nanoseconds since epoch |

### time_unix_usec

```mach
pub fun time_unix_usec(t: Time) i64
```

return microseconds since Unix epoch

| Parameter | |
| :--- | :--- |
| `t` | time to query |
| **returns** | total microseconds since epoch |

### time_unix_msec

```mach
pub fun time_unix_msec(t: Time) i64
```

return milliseconds since Unix epoch

| Parameter | |
| :--- | :--- |
| `t` | time to query |
| **returns** | total milliseconds since epoch |

### time_add

```mach
pub fun time_add(t: Time, d: Duration) Time
```

return t + d

| Parameter | |
| :--- | :--- |
| `t` | base time |
| `d` | duration to add |
| **returns** | new Time offset by d |

### time_sub

```mach
pub fun time_sub(t: Time, u: Time) Duration
```

return the duration t - u

| Parameter | |
| :--- | :--- |
| `t` | minuend time |
| `u` | subtrahend time |
| **returns** | duration between t and u |

### time_before

```mach
pub fun time_before(t: Time, u: Time) bool
```

report whether t is before u

| Parameter | |
| :--- | :--- |
| `t` | time to test |
| `u` | time to compare against |
| **returns** | true if t \< u |

### time_after

```mach
pub fun time_after(t: Time, u: Time) bool
```

report whether t is after u

| Parameter | |
| :--- | :--- |
| `t` | time to test |
| `u` | time to compare against |
| **returns** | true if t > u |

### time_equal

```mach
pub fun time_equal(t: Time, u: Time) bool
```

report whether t and u represent the same instant

| Parameter | |
| :--- | :--- |
| `t` | first time |
| `u` | second time |
| **returns** | true if t == u |

### time_is_zero

```mach
pub fun time_is_zero(t: Time) bool
```

report whether t represents the zero time instant

| Parameter | |
| :--- | :--- |
| `t` | time to test |
| **returns** | true if t is the zero time (Unix epoch) |

## Instant

```mach
pub rec Instant {
    sec:  i64;
    nsec: i64;
}
```

a monotonic instant with nanosecond precision

read only from `instant`. it has no epoch meaning and is only compared with,
or measured against, other Instants. every deadline in std is an Instant

| Field | Type | |
| :--- | :--- | :--- |
| `sec` | `i64` | seconds since the monotonic clock's unspecified start |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |

### elapsed

Only where `capability.HAS_CLOCK`.

```mach
pub fun elapsed(start: Instant) Elapsed
```

return the monotonic time elapsed since start

| Parameter | |
| :--- | :--- |
| `start` | an earlier Instant |
| **returns** | the duration since start, or the monotonic clock's refusal |

### remaining

Only where `capability.HAS_CLOCK`.

```mach
pub fun remaining(deadline: Instant) Elapsed
```

return how long remains until deadline, negative once it has passed

| Parameter | |
| :--- | :--- |
| `deadline` | the Instant to measure to |
| **returns** | the duration until deadline, or the monotonic clock's refusal |

### instant_add

```mach
pub fun instant_add(i: Instant, d: Duration) Instant
```

return i + d

| Parameter | |
| :--- | :--- |
| `i` | base instant |
| `d` | duration to add |
| **returns** | the instant offset by d |

### instant_sub

```mach
pub fun instant_sub(i: Instant, j: Instant) Duration
```

return the duration i - j

| Parameter | |
| :--- | :--- |
| `i` | minuend instant |
| `j` | subtrahend instant |
| **returns** | duration between i and j |

### instant_before

```mach
pub fun instant_before(i: Instant, j: Instant) bool
```

report whether i is before j

| Parameter | |
| :--- | :--- |
| `i` | instant to test |
| `j` | instant to compare against |
| **returns** | true if i \< j |

### instant_after

```mach
pub fun instant_after(i: Instant, j: Instant) bool
```

report whether i is after j

| Parameter | |
| :--- | :--- |
| `i` | instant to test |
| `j` | instant to compare against |
| **returns** | true if i > j |

### instant_equal

```mach
pub fun instant_equal(i: Instant, j: Instant) bool
```

report whether i and j are the same instant

| Parameter | |
| :--- | :--- |
| `i` | first instant |
| `j` | second instant |
| **returns** | true if i == j |

