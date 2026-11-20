[std](../README.md) / [sync](README.md) / **once**

# std.sync.once

exactly-once initialization with sticky failure

Source: [`src/sync/once.mach`](../../../src/sync/once.mach)

| Type | | |
| :--- | :--- | :--- |
| [`InitFun`](#initfun) | `def` | an initializer reports its own failure as a code it chooses; the once value retains the code so every later caller observes the same refusal |
| [`InitError`](#initerror) | `tag` | why initialization did not complete |
| [`Outcome`](#outcome) | `def` |  |
| [`Once`](#once) | `rec` | an exactly-once gate, made with make |

| On `Once` | |
| :--- | :--- |
| [`make`](#make) | initializer selection is unfair and recursive use of one value deadlocks waits may wake spuriously and always recheck the published state a refused initializer is a sticky failure and initialization is never retried a panic terminates the process and does not create recoverable poisoning once owns no target handle and may be discarded only without callers |
| [`run`](#run) | run init exactly once across every caller, waiting while another caller runs it |
| [`is_complete`](#is_complete) | report whether initialization completed |
| [`is_failed`](#is_failed) | report whether initialization failed |

| Constants | |
| :--- | :--- |
| [`PENDING`](#constants), [`RUNNING`](#constants), [`COMPLETE`](#constants), [`FAILED`](#constants) | |

---

## InitFun

```mach
pub def InitFun: fun(ptr) err[i64]
```

an initializer reports its own failure as a code it chooses; the once
value retains the code so every later caller observes the same refusal

## InitError

```mach
pub tag InitError: u8 { invalid; failed: i64; }
```

why initialization did not complete

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil once value or initializer |
| `failed` | `i64` | the initializer refused, with the code it returned (sticky) |

## Outcome

```mach
pub def Outcome: res[bool, InitError]
```

## Once

```mach
pub rec Once {
    state:   i64;
    waiters: i64;
    error:   i64;
}
```

an exactly-once gate, made with make

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `i64` | PENDING, RUNNING, COMPLETE or FAILED, changed atomically |
| `waiters` | `i64` | callers sleeping while another runs the initializer |
| `error` | `i64` | the code the initializer refused with, valid once FAILED |

### make

```mach
pub fun make() Once
```

initializer selection is unfair and recursive use of one value deadlocks
waits may wake spuriously and always recheck the published state
a refused initializer is a sticky failure and initialization is never retried
a panic terminates the process and does not create recoverable poisoning
once owns no target handle and may be discarded only without callers

| Parameter | |
| :--- | :--- |
| **returns** | a pending once value |

### run

```mach
pub fun run(o: *Once, ctx: ptr, init: InitFun) Outcome
```

run init exactly once across every caller, waiting while another caller runs it

| Parameter | |
| :--- | :--- |
| `o` | once value |
| `ctx` | caller pointer passed to init |
| `init` | initializer to run |
| **returns** | true when this call ran the initializer to completion, false when initialization had already completed, or the retained failure |

### is_complete

```mach
pub fun is_complete(o: *Once) bool
```

report whether initialization completed

| Parameter | |
| :--- | :--- |
| `o` | once value |
| **returns** | true once the initializer succeeded |

### is_failed

```mach
pub fun is_failed(o: *Once) bool
```

report whether initialization failed

| Parameter | |
| :--- | :--- |
| `o` | once value |
| **returns** | true once the initializer refused |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `PENDING` | `i64` | `0` |  |
| `RUNNING` | `i64` | `1` |  |
| `COMPLETE` | `i64` | `2` |  |
| `FAILED` | `i64` | `3` |  |

