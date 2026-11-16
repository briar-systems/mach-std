[std](../README.md) / [sync](README.md) / **condition**

# std.sync.condition

condition variable over a generation word

Source: [`src/sync/condition.mach`](../../../src/sync/condition.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.sync.mutex`](mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Condition`](#condition) | `rec` |  |
| [`WaitStatus`](#waitstatus) | `tag` | the outcome of a timed wait |

| On `Condition` | |
| :--- | :--- |
| [`make`](#make) | conditions are unfair and callers must always wait in a predicate loop target waits may wake spuriously and signal may be observed by any waiter predicate access and notification must use the same caller-owned mutex failure while holding the paired mutex does not poison the condition conditions own no target handle and may be discarded only without waiters |
| [`wait`](#wait) | generation closes the race between releasing the mutex and sleeping |
| [`wait_until`](#wait_until) | the deadline is an absolute monotonic instant and never expires early |
| [`signal`](#signal), [`broadcast`](#broadcast) | |
| [`waiter_count`](#waiter_count) | this diagnostic result is stale as soon as it is returned |

---

## Condition

```mach
pub rec Condition {
    generation: i64;
    waiters:    i64;
}
```

### make

```mach
pub fun make() Condition
```

conditions are unfair and callers must always wait in a predicate loop
target waits may wake spuriously and signal may be observed by any waiter
predicate access and notification must use the same caller-owned mutex
failure while holding the paired mutex does not poison the condition
conditions own no target handle and may be discarded only without waiters

### wait

```mach
pub fun wait(c: *Condition, m: *std.sync.mutex.Mutex)
```

generation closes the race between releasing the mutex and sleeping

### wait_until

```mach
pub fun wait_until(c: *Condition, m: *std.sync.mutex.Mutex, deadline: std.chrono.time.Instant) WaitStatus
```

the deadline is an absolute monotonic instant and never expires early

### signal

```mach
pub fun signal(c: *Condition)
```

### broadcast

```mach
pub fun broadcast(c: *Condition)
```

### waiter_count

```mach
pub fun waiter_count(c: *Condition) i64
```

this diagnostic result is stale as soon as it is returned

## WaitStatus

```mach
pub tag WaitStatus: u8 { invalid; failed: i64; timed_out; notified; }
```

the outcome of a timed wait

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil condition or mutex, or a deadline outside the target range |
| `failed` | `i64` | the native wait refused, with its negative code |
| `timed_out` |  | the absolute deadline passed before a notification |
| `notified` |  | woken by signal, broadcast or a spurious target wakeup |

