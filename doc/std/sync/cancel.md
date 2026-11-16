[std](../README.md) / [sync](README.md) / **cancel**

# std.sync.cancel

caller-owned hierarchical cancellation

threading model
each scope's lock guards its state, its registrations and its children's
sibling links. attach and unregister take only their scope's lock, and
make_child and destroy take the parent's (destroy then the scope's own).
a cancel walks the subtree top-down, holding a parent's lock while it visits
that parent's children. locks are only ever taken parent before child.
finish and reason take no lock.

a shared scope serializes attach and unregister across every thread using
it, and a shared parent serializes make_child and destroy. servers should
give each worker its own root and each connection its own child scope. on a
ryzen 7 5800x3d at -O2, attach plus unregister totals about 3.8M/s on one
scope shared by 8 threads, against about 78M/s on 8 per-thread children

Source: [`src/sync/cancel.mach`](../../../src/sync/cancel.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.sync.mutex`](mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Reason`](#reason) | `tag` | why a scope is no longer active, or that it still is |
| [`StateError`](#stateerror) | `tag` | a refused scope or registration operation |
| [`Deadline`](#deadline) | `rec` | the effective absolute monotonic deadline of a scope |
| [`CancelFun`](#cancelfun) | `def` |  |
| [`Transition`](#transition) | `def` |  |
| [`Operation`](#operation) | `def` |  |
| [`DeadlineQuery`](#deadlinequery) | `def` |  |
| [`Registration`](#registration) | `rec` |  |
| [`Scope`](#scope) | `rec` |  |

| On `Registration` | |
| :--- | :--- |
| [`registration_make`](#registration_make) | initialization is valid before first attachment or after terminal completion |
| [`finish`](#finish) | this must be the completion hook's final registration operation |
| [`unregister`](#unregister) | completion wins only while the registration remains owned by its scope |

| On `Scope` | |
| :--- | :--- |
| [`make_root`](#make_root) | scopes are fixed in memory and own no target handle or allocation callers stop starting new calls before reclaiming a destroyed scope |
| [`make_child`](#make_child) | child deadlines inherit the earliest absolute monotonic ancestor deadline |
| [`attach`](#attach) | successful registration is the ownership linearization point |
| [`attach_with_completion`](#attach_with_completion) | completion publishes external work and must call finish under its lifetime lock |
| [`cancel`](#cancel) | ret: true when this call cancelled the scope, false when it was already      cancelled or timed out |
| [`timeout`](#timeout) | ret: true when this call timed the scope out, false when it was already      cancelled or timed out |
| [`expire`](#expire) | callers without a runtime may drive absolute deadlines explicitly |
| [`get_deadline`](#get_deadline) | returns the effective deadline and the ancestor that owns it |
| [`reason`](#reason-1), [`wait`](#wait), [`waiter_count`](#waiter_count) | |
| [`dnit`](#dnit) | destruction rejects children, live registrations, waiters, and callbacks |

---

## Reason

```mach
pub tag Reason: u8 { active; cancelled; timed_out; destroyed; invalid; }
```

why a scope is no longer active, or that it still is

| Case | Payload | |
| :--- | :--- | :--- |
| `active` |  | no cancellation has been requested |
| `cancelled` |  | cancelled explicitly through this scope or an ancestor |
| `timed_out` |  | an absolute deadline owned by this scope or an ancestor passed |
| `destroyed` |  | the scope was destroyed, or the call reached a destroyed scope |
| `invalid` |  | the call was refused (nil operands, a registration in use) |

## StateError

```mach
pub tag StateError: u8 { invalid; destroyed; busy; }
```

a refused scope or registration operation

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | nil operands, a deadline outside the target range, a scope parented to itself, or a scope that was never made |
| `destroyed` |  | the scope (or the parent) has already been destroyed |
| `busy` |  | destruction refused while children, registrations, waiters, running callbacks or in-flight callers remain |

## Deadline

```mach
pub rec Deadline {
    at:    std.chrono.time.Instant;
    owner: *Scope;
}
```

the effective absolute monotonic deadline of a scope

| Field | Type | |
| :--- | :--- | :--- |
| `at` | `std.chrono.time.Instant` | the earliest deadline along the ancestor chain |
| `owner` | `*Scope` | the scope that declared it, borrowed from the tree |

## CancelFun

```mach
pub def CancelFun: fun(ptr, Reason)
```

## Transition

```mach
pub def Transition:    res[bool, StateError]
```

## Operation

```mach
pub def Operation:     err[StateError]
```

## DeadlineQuery

```mach
pub def DeadlineQuery: res[opt[Deadline], StateError]
```

## Registration

```mach
pub rec Registration {
    root:       *Scope;
    scope:      *Scope;
    prev:       *Registration;
    next:       *Registration;
    callback:   CancelFun;
    completion: CancelFun;
    context:    ptr;
    reason:     i64;
    state:      i64;
}
```

### registration_make

```mach
pub fun registration_make(registration: *Registration) Operation
```

initialization is valid before first attachment or after terminal completion

### finish

```mach
pub fun finish(registration: *Registration) Transition
```

this must be the completion hook's final registration operation

| Parameter | |
| :--- | :--- |
| **returns** | true when this call completed a cancelled registration, false when the registration was not awaiting completion, invalid for nil |

### unregister

```mach
pub fun unregister(registration: *Registration) Transition
```

completion wins only while the registration remains owned by its scope

| Parameter | |
| :--- | :--- |
| **returns** | true when this call detached the registration, false when cancellation already claimed it (the completion hook owns it), invalid for nil |

## Scope

```mach
pub rec Scope {
    root:               *Scope;
    parent:             *Scope;
    first_child:        *Scope;
    prev_sibling:       *Scope;
    next_sibling:       *Scope;
    first_registration: *Registration;
    deadline:           opt[std.chrono.time.Instant];
    deadline_owner:     *Scope;
    state:              i64;
    waiters:            i64;
    gate:               i64;
    callback_count:     i64;
    lock:               std.sync.mutex.Mutex;
}
```

### make_root

```mach
pub fun make_root(scope: *Scope, deadline: opt[std.chrono.time.Instant]) Operation
```

scopes are fixed in memory and own no target handle or allocation
callers stop starting new calls before reclaiming a destroyed scope

a deadline is an absolute monotonic Instant, for example
`time.instant_add(time.instant().ok, timeout)`

### make_child

```mach
pub fun make_child(scope: *Scope, parent: *Scope, deadline: opt[std.chrono.time.Instant]) Operation
```

child deadlines inherit the earliest absolute monotonic ancestor deadline

a deadline is an absolute monotonic Instant, for example
`time.instant_add(time.instant().ok, timeout)`

### attach

```mach
pub fun attach(scope: *Scope, registration: *Registration, callback: CancelFun, context: ptr) Reason
```

successful registration is the ownership linearization point

### attach_with_completion

```mach
pub fun attach_with_completion(scope: *Scope, registration: *Registration, callback: CancelFun, completion: CancelFun, context: ptr) Reason
```

completion publishes external work and must call finish under its lifetime lock

### cancel

```mach
pub fun cancel(scope: *Scope) Transition
```

ret: true when this call cancelled the scope, false when it was already
     cancelled or timed out

### timeout

```mach
pub fun timeout(scope: *Scope) Transition
```

ret: true when this call timed the scope out, false when it was already
     cancelled or timed out

### expire

```mach
pub fun expire(scope: *Scope, now: std.chrono.time.Instant) Transition
```

callers without a runtime may drive absolute deadlines explicitly

| Parameter | |
| :--- | :--- |
| **returns** | true when now reached the effective deadline and this call timed its owner out, false when there is no deadline, it has not passed, or the owner had already left active |

### get_deadline

```mach
pub fun get_deadline(scope: *Scope) DeadlineQuery
```

returns the effective deadline and the ancestor that owns it

| Parameter | |
| :--- | :--- |
| **returns** | some{deadline} when the scope or an ancestor declared one, none when the scope has no deadline, destroyed once the scope is gone |

### reason

```mach
pub fun reason(scope: *Scope) Reason
```

### wait

```mach
pub fun wait(scope: *Scope) Reason
```

### waiter_count

```mach
pub fun waiter_count(scope: *Scope) i64
```

### dnit

```mach
pub fun dnit(scope: *Scope) Operation
```

destruction rejects children, live registrations, waiters, and callbacks

| Parameter | |
| :--- | :--- |
| **returns** | ok once the scope is destroyed, invalid for a nil or never-made scope, destroyed when it already was, busy while children, registrations, waiters, running callbacks or in-flight callers remain |

