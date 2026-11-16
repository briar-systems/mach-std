[std](../README.md) / [sync](README.md) / **semaphore**

# std.sync.semaphore

bounded counting semaphore

Source: [`src/sync/semaphore.mach`](../../../src/sync/semaphore.mach)

| Type | | |
| :--- | :--- | :--- |
| [`StateError`](#stateerror) | `tag` | a refused semaphore operation |
| [`Operation`](#operation) | `def` |  |
| [`Semaphore`](#semaphore) | `rec` |  |

| On `Semaphore` | |
| :--- | :--- |
| [`make`](#make) | semaphores are unfair and a new caller may acquire before a woken waiter waits may wake spuriously and always retry permit acquisition failed work does not poison permits or change the configured bound initialization must complete before the semaphore is published semaphores own no target handle and may be discarded only without waiters |
| [`try_wait`](#try_wait), [`wait`](#wait) | |
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

### make

```mach
pub fun make(s: *Semaphore, initial: i64, limit: i64) Operation
```

semaphores are unfair and a new caller may acquire before a woken waiter
waits may wake spuriously and always retry permit acquisition
failed work does not poison permits or change the configured bound
initialization must complete before the semaphore is published
semaphores own no target handle and may be discarded only without waiters

### try_wait

```mach
pub fun try_wait(s: *Semaphore) bool
```

### wait

```mach
pub fun wait(s: *Semaphore)
```

### release

```mach
pub fun release(s: *Semaphore) Operation
```

release refuses with overflow at the bound and leaves the count unchanged

### available

```mach
pub fun available(s: *Semaphore) i64
```

this diagnostic result is stale as soon as it is returned

### waiter_count

```mach
pub fun waiter_count(s: *Semaphore) i64
```

this diagnostic result is stale as soon as it is returned

