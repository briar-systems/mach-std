[std](../README.md) / [sync](README.md) / **cancel**

# std.sync.cancel

caller-owned hierarchical cancellation

threading model
each scope's lock guards its state, its registrations and its children's
sibling links. attach and unregister take only their scope's lock, and
make_child and dnit take the parent's (dnit then the scope's own).
a cancel walks the subtree top-down, holding a parent's lock while it visits
that parent's children. locks are only ever taken parent before child.
finish and reason take no lock.

a shared scope serializes attach and unregister across every thread using
it, and a shared parent serializes make_child and dnit. servers should
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
| [`Registration`](#registration) | `rec` | a caller-owned slot that ties a cancellation callback to a scope |
| [`Scope`](#scope) | `rec` | a caller-owned node in a cancellation tree, fixed in memory once made |

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
| [`cancel`](#cancel) | cancel a scope and its whole subtree, running each claimed callback |
| [`timeout`](#timeout) | time a scope and its whole subtree out, running each claimed callback |
| [`expire`](#expire) | callers without a runtime may drive absolute deadlines explicitly |
| [`get_deadline`](#get_deadline) | returns the effective deadline and the ancestor that owns it |
| [`reason`](#reason-1) | read why a scope is no longer active, or that it still is |
| [`wait`](#wait) | block until a scope leaves active |
| [`waiter_count`](#waiter_count) | count the threads blocked in wait on a scope |
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

a caller-owned slot that ties a cancellation callback to a scope

prepare it with registration_make, then attach it. the fields are internal.

| Field | Type | |
| :--- | :--- | :--- |
| `root` | `*Scope` | root of the scope it is attached to, nil while unattached |
| `scope` | `*Scope` | scope it is listed on, nil while unattached or once claimed |
| `prev` | `*Registration` | previous registration on the scope's list |
| `next` | `*Registration` | next registration on the scope's list, or on a cancel's claim list |
| `callback` | `CancelFun` | hook run when the scope is cancelled or times out |
| `completion` | `CancelFun` | optional hook run after callback, nil when absent |
| `context` | `ptr` | caller pointer passed to both hooks |
| `reason` | `i64` | state the claiming cancel moved the scope to |
| `state` | `i64` | lifecycle state of the registration, changed atomically |

### registration_make

```mach
pub fun registration_make(registration: *Registration) Operation
```

initialization is valid before first attachment or after terminal completion

| Parameter | |
| :--- | :--- |
| `registration` | storage to reset to the unused state |
| **returns** | ok, or invalid for nil |

### finish

```mach
pub fun finish(registration: *Registration) Transition
```

this must be the completion hook's final registration operation

| Parameter | |
| :--- | :--- |
| `registration` | registration whose completion hook is running |
| **returns** | true when this call completed a cancelled registration, false when the registration was not awaiting completion, invalid for nil |

### unregister

```mach
pub fun unregister(registration: *Registration) Transition
```

completion wins only while the registration remains owned by its scope

| Parameter | |
| :--- | :--- |
| `registration` | registration to detach from its scope |
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

a caller-owned node in a cancellation tree, fixed in memory once made

prepare it with make_root or make_child and release it with dnit. the fields
are internal.

| Field | Type | |
| :--- | :--- | :--- |
| `root` | `*Scope` | root of the tree, the scope itself for a root |
| `parent` | `*Scope` | parent scope, nil for a root |
| `first_child` | `*Scope` | head of the list of child scopes |
| `prev_sibling` | `*Scope` | previous child of the same parent |
| `next_sibling` | `*Scope` | next child of the same parent |
| `first_registration` | `*Registration` | head of the list of attached registrations |
| `deadline` | `opt[std.chrono.time.Instant]` | effective absolute monotonic deadline, none when absent |
| `deadline_owner` | `*Scope` | scope that declared the effective deadline |
| `state` | `i64` | active, cancelled, timed out or destroyed, changed atomically |
| `waiters` | `i64` | threads blocked in wait on this scope |
| `gate` | `i64` | in-flight callers, or GATE_CLOSED once destroyed |
| `callback_count` | `i64` | claimed callbacks still running, kept on the root |
| `lock` | `std.sync.mutex.Mutex` | guards state, registrations and the children's sibling links |

### make_root

```mach
pub fun make_root(scope: *Scope, deadline: opt[std.chrono.time.Instant]) Operation
```

scopes are fixed in memory and own no target handle or allocation
callers stop starting new calls before reclaiming a destroyed scope

a deadline is an absolute monotonic Instant, for example
`time.instant_add(time.instant().ok, timeout)`

| Parameter | |
| :--- | :--- |
| `scope` | storage to make into a root scope |
| `deadline` | absolute monotonic deadline, or none |
| **returns** | ok, or invalid for a nil scope or a malformed deadline |

### make_child

```mach
pub fun make_child(scope: *Scope, parent: *Scope, deadline: opt[std.chrono.time.Instant]) Operation
```

child deadlines inherit the earliest absolute monotonic ancestor deadline

a deadline is an absolute monotonic Instant, for example
`time.instant_add(time.instant().ok, timeout)`
a child made under a parent that already left active starts in the same state

| Parameter | |
| :--- | :--- |
| `scope` | storage to make into a child scope |
| `parent` | live scope to attach the child under |
| `deadline` | absolute monotonic deadline of the child, or none |
| **returns** | ok, invalid for nil operands, scope equal to parent or a malformed deadline, destroyed when the parent has been destroyed |

### attach

```mach
pub fun attach(scope: *Scope, registration: *Registration, callback: CancelFun, context: ptr) Reason
```

successful registration is the ownership linearization point

| Parameter | |
| :--- | :--- |
| `scope` | scope to attach to |
| `registration` | unused or completed registration to attach |
| `callback` | hook run once if the scope is cancelled or times out |
| `context` | caller pointer passed to callback |
| **returns** | active once attached, the scope's reason when it already left active, destroyed for a destroyed scope, invalid for nil operands, a nil callback or a registration in use |

### attach_with_completion

```mach
pub fun attach_with_completion(scope: *Scope, registration: *Registration, callback: CancelFun, completion: CancelFun, context: ptr) Reason
```

completion publishes external work and must call finish under its lifetime lock

| Parameter | |
| :--- | :--- |
| `scope` | scope to attach to |
| `registration` | unused or completed registration to attach |
| `callback` | hook run once if the scope is cancelled or times out |
| `completion` | hook run right after callback, it must end with finish |
| `context` | caller pointer passed to both hooks |
| **returns** | as attach, and invalid for a nil completion |

### cancel

```mach
pub fun cancel(scope: *Scope) Transition
```

cancel a scope and its whole subtree, running each claimed callback

| Parameter | |
| :--- | :--- |
| `scope` | scope to cancel |
| **returns** | true when this call cancelled the scope, false when it was already cancelled or timed out |

### timeout

```mach
pub fun timeout(scope: *Scope) Transition
```

time a scope and its whole subtree out, running each claimed callback

| Parameter | |
| :--- | :--- |
| `scope` | scope to time out |
| **returns** | true when this call timed the scope out, false when it was already cancelled or timed out |

### expire

```mach
pub fun expire(scope: *Scope, now: std.chrono.time.Instant) Transition
```

callers without a runtime may drive absolute deadlines explicitly

| Parameter | |
| :--- | :--- |
| `scope` | scope whose effective deadline is checked |
| `now` | current absolute monotonic instant |
| **returns** | true when now reached the effective deadline and this call timed its owner out, false when there is no deadline, it has not passed, or the owner had already left active |

### get_deadline

```mach
pub fun get_deadline(scope: *Scope) DeadlineQuery
```

returns the effective deadline and the ancestor that owns it

| Parameter | |
| :--- | :--- |
| `scope` | scope to query |
| **returns** | some{deadline} when the scope or an ancestor declared one, none when the scope has no deadline, destroyed once the scope is gone |

### reason

```mach
pub fun reason(scope: *Scope) Reason
```

read why a scope is no longer active, or that it still is

| Parameter | |
| :--- | :--- |
| `scope` | scope to read |
| **returns** | the scope's reason, destroyed for nil or a destroyed scope |

### wait

```mach
pub fun wait(scope: *Scope) Reason
```

block until a scope leaves active

| Parameter | |
| :--- | :--- |
| `scope` | scope to wait on |
| **returns** | the reason it left active, destroyed for nil or a destroyed scope |

### waiter_count

```mach
pub fun waiter_count(scope: *Scope) i64
```

count the threads blocked in wait on a scope

| Parameter | |
| :--- | :--- |
| `scope` | scope to read |
| **returns** | waiter count, 0 for nil or a destroyed scope |

### dnit

```mach
pub fun dnit(scope: *Scope) Operation
```

destruction rejects children, live registrations, waiters, and callbacks

| Parameter | |
| :--- | :--- |
| **returns** | ok once the scope is destroyed, invalid for a nil or never-made scope, destroyed when it already was, busy while children, registrations, waiters, running callbacks or in-flight callers remain |

