[std](../README.md) / [sync](README.md) / **condition**

# std.sync.condition

condition variable over a generation word

Source: [`src/sync/condition.mach`](../../../src/sync/condition.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.sync.mutex`](mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Condition`](#condition) | `rec` | a condition variable, paired by the caller with one mutex |
| [`WaitStatus`](#waitstatus) | `tag` | the outcome of a timed wait |

| On `Condition` | |
| :--- | :--- |
| [`make`](#make) | conditions are unfair and callers must always wait in a predicate loop target waits may wake spuriously and signal may be observed by any waiter predicate access and notification must use the same caller-owned mutex failure while holding the paired mutex does not poison the condition conditions own no target handle and may be discarded only without waiters |
| [`wait`](#wait) | generation closes the race between releasing the mutex and sleeping |
| [`wait_until`](#wait_until) | the deadline is an absolute monotonic instant and never expires early |
| [`signal`](#signal) | wake at least one waiter, if any |
| [`broadcast`](#broadcast) | wake every thread waiting when the call began |
| [`waiter_count`](#waiter_count) | this diagnostic result is stale as soon as it is returned |

---

## Condition

```mach
pub rec Condition {
    generation: i64;
    waiters:    i64;
}
```

a condition variable, paired by the caller with one mutex

| Field | Type | |
| :--- | :--- | :--- |
| `generation` | `i64` | bumped by every signal and broadcast, the word waiters sleep on |
| `waiters` | `i64` | number of threads currently inside wait or wait_until |

### make

```mach
pub fun make() Condition
```

conditions are unfair and callers must always wait in a predicate loop
target waits may wake spuriously and signal may be observed by any waiter
predicate access and notification must use the same caller-owned mutex
failure while holding the paired mutex does not poison the condition
conditions own no target handle and may be discarded only without waiters

| Parameter | |
| :--- | :--- |
| **returns** | a condition with no waiters |

### wait

```mach
pub fun wait(c: *Condition, m: *std.sync.mutex.Mutex)
```

generation closes the race between releasing the mutex and sleeping

releases m, sleeps until notified or a spurious wakeup, then reacquires m

| Parameter | |
| :--- | :--- |
| `c` | condition to wait on |
| `m` | mutex the caller holds, released while asleep and held again on return |

### wait_until

```mach
pub fun wait_until(c: *Condition, m: *std.sync.mutex.Mutex, deadline: std.chrono.time.Instant) WaitStatus
```

the deadline is an absolute monotonic instant and never expires early

releases m while asleep, and the caller holds m again on every return

| Parameter | |
| :--- | :--- |
| `c` | condition to wait on |
| `m` | mutex the caller holds |
| `deadline` | absolute monotonic instant to give up at |
| **returns** | notified, timed_out, failed with the native code, or invalid |

### signal

```mach
pub fun signal(c: *Condition)
```

wake at least one waiter, if any

| Parameter | |
| :--- | :--- |
| `c` | condition to notify |

### broadcast

```mach
pub fun broadcast(c: *Condition)
```

wake every thread waiting when the call began

| Parameter | |
| :--- | :--- |
| `c` | condition to notify |

### waiter_count

```mach
pub fun waiter_count(c: *Condition) i64
```

this diagnostic result is stale as soon as it is returned

| Parameter | |
| :--- | :--- |
| `c` | condition to read |
| **returns** | number of threads inside wait or wait_until |

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

