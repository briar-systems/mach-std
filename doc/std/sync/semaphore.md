[std](../README.md) / [sync](README.md) / **semaphore**

# std.sync.semaphore

bounded counting semaphore

Source: [`src/sync/semaphore.mach`](../../../src/sync/semaphore.mach)

| Type | | |
| :--- | :--- | :--- |
| [`StateError`](#stateerror) | `tag` | a refused semaphore operation |
| [`Operation`](#operation) | `def` |  |
| [`Semaphore`](#semaphore) | `rec` | a counting semaphore with an upper bound, made with make |

| On `Semaphore` | |
| :--- | :--- |
| [`make`](#make) | semaphores are unfair and a new caller may acquire before a woken waiter waits may wake spuriously and always retry permit acquisition failed work does not poison permits or change the configured bound initialization must complete before the semaphore is published semaphores own no target handle and may be discarded only without waiters |
| [`try_wait`](#try_wait) | take one permit only if one is available right now |
| [`wait`](#wait) | take one permit, sleeping until one is available |
| [`release`](#release) | release refuses with overflow at the bound and leaves the count unchanged |
| [`available`](#available) | this diagnostic result is stale as soon as it is returned |
| [`waiter_count`](#waiter_count) | this diagnostic result is stale as soon as it is returned |

---

## StateError

```mach
pub tag StateError: u8 { invalid; overflow; }
```

a refused semaphore operation

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil semaphore, a negative count or bound, or an initial count above the bound |
| `overflow` |  | a release that would exceed the bound; the count is unchanged |

## Operation

```mach
pub def Operation: err[StateError]
```

## Semaphore

```mach
pub rec Semaphore {
    permits:    i64;
    limit:      i64;
    generation: i64;
    waiters:    i64;
}
```

a counting semaphore with an upper bound, made with make

| Field | Type | |
| :--- | :--- | :--- |
| `permits` | `i64` | permits currently available |
| `limit` | `i64` | the most permits the semaphore may hold |
| `generation` | `i64` | bumped by every release, the word waiters sleep on |
| `waiters` | `i64` | threads sleeping in wait |

### make

```mach
pub fun make(s: *Semaphore, initial: i64, limit: i64) Operation
```

semaphores are unfair and a new caller may acquire before a woken waiter
waits may wake spuriously and always retry permit acquisition
failed work does not poison permits or change the configured bound
initialization must complete before the semaphore is published
semaphores own no target handle and may be discarded only without waiters

| Parameter | |
| :--- | :--- |
| `s` | storage to make into a semaphore |
| `initial` | permits available at start, between 0 and limit |
| `limit` | the most permits the semaphore may hold, at least 0 |
| **returns** | ok, or invalid for a nil s or out of range counts, with s left holding no permits |

### try_wait

```mach
pub fun try_wait(s: *Semaphore) bool
```

take one permit only if one is available right now

| Parameter | |
| :--- | :--- |
| `s` | semaphore |
| **returns** | true when a permit was taken |

### wait

```mach
pub fun wait(s: *Semaphore)
```

take one permit, sleeping until one is available

| Parameter | |
| :--- | :--- |
| `s` | semaphore |

### release

```mach
pub fun release(s: *Semaphore) Operation
```

release refuses with overflow at the bound and leaves the count unchanged

| Parameter | |
| :--- | :--- |
| `s` | semaphore |
| **returns** | ok, overflow at the bound, or invalid for nil |

### available

```mach
pub fun available(s: *Semaphore) i64
```

this diagnostic result is stale as soon as it is returned

| Parameter | |
| :--- | :--- |
| `s` | semaphore |
| **returns** | permits currently available |

### waiter_count

```mach
pub fun waiter_count(s: *Semaphore) i64
```

this diagnostic result is stale as soon as it is returned

| Parameter | |
| :--- | :--- |
| `s` | semaphore |
| **returns** | threads sleeping in wait |

