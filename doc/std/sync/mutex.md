[std](../README.md) / [sync](README.md) / **mutex**

# std.sync.mutex

sleeping mutual exclusion lock

a contended lock sleeps in the OS until the holder wakes it. a target with no
threads capability has no OS to sleep in, so a contended lock spins there, and
the holder is another core or an interrupt handler.

Source: [`src/sync/mutex.mach`](../../../src/sync/mutex.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Mutex`](#mutex) | `def` |  |

| On `Mutex` | |
| :--- | :--- |
| [`make`](#make) | mutexes are unfair and may admit a new caller before a woken waiter waits may wake spuriously, so acquisition always rechecks the state mutexes are not poisoned when a protected operation fails mutexes own no target handle and may be discarded only without waiters |
| [`lock`](#lock) | acquire the mutex, sleeping or spinning while another holder has it |
| [`unlock`](#unlock) | release the mutex and wake one sleeper if any |
| [`try_lock`](#try_lock) | acquire the mutex only if it is free right now |
| [`is_locked`](#is_locked) | this diagnostic result is stale as soon as it is returned |

---

## Mutex

```mach
pub def Mutex: i64
```

### make

```mach
pub fun make() Mutex
```

mutexes are unfair and may admit a new caller before a woken waiter
waits may wake spuriously, so acquisition always rechecks the state
mutexes are not poisoned when a protected operation fails
mutexes own no target handle and may be discarded only without waiters

| Parameter | |
| :--- | :--- |
| **returns** | an unlocked mutex |

### lock

```mach
pub fun lock(m: *Mutex)
```

acquire the mutex, sleeping or spinning while another holder has it

| Parameter | |
| :--- | :--- |
| `m` | mutex to acquire, not already held by the caller |

### unlock

```mach
pub fun unlock(m: *Mutex)
```

release the mutex and wake one sleeper if any

| Parameter | |
| :--- | :--- |
| `m` | mutex the caller holds |

### try_lock

```mach
pub fun try_lock(m: *Mutex) bool
```

acquire the mutex only if it is free right now

| Parameter | |
| :--- | :--- |
| `m` | mutex to acquire |
| **returns** | true when the caller now holds it |

### is_locked

```mach
pub fun is_locked(m: *Mutex) bool
```

this diagnostic result is stale as soon as it is returned

| Parameter | |
| :--- | :--- |
| `m` | mutex to read |
| **returns** | true when some caller holds it |

