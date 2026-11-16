[std](../README.md) / [io](README.md) / **runtime**

# std.io.runtime

bounded portable operation-completion ownership

Source: [`src/io/runtime.mach`](../../../src/io/runtime.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.chrono.time`](../chrono/time.md), [`std.io.error`](error.md), [`std.io.lifecycle`](lifecycle.md), [`std.memory.table`](../memory/table.md), [`std.sync.cancel`](../sync/cancel.md), [`std.sync.mutex`](../sync/mutex.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Kind`](#kind) | `def` |  |
| [`Token`](#token) | `rec` |  |
| [`Operation`](#operation) | `rec` | buffer is borrowed from successful submission until its completion is dequeued |
| [`Completion`](#completion) | `rec` | a terminal result |
| [`NativeEvent`](#nativeevent) | `rec` | one native completion, laid out as the platform's IoCompletion |
| [`SourceToken`](#sourcetoken) | `rec` |  |
| [`DispatchFun`](#dispatchfun) | `def` | offered each native event carrying the source's id, and every wake (context 0) |
| [`CancelFun`](#cancelfun) | `def` |  |
| [`ReleaseFun`](#releasefun) | `def` |  |
| [`WaitPlan`](#waitplan) | `rec` | wait is false when the driver must not poll: the runtime is closed or a caller woke it, and woken says which |
| [`Runtime`](#runtime) | `rec` | one thread owns wait and dequeue, while submission and resolution may be concurrent |

| On `Kind` | |
| :--- | :--- |
| [`ACCEPT`](#kind), [`CONNECT`](#kind), [`READ`](#kind), [`WRITE`](#kind), [`RECEIVE_FROM`](#kind), [`SEND_TO`](#kind), [`FILE_READ`](#kind), [`FILE_WRITE`](#kind), [`TIMER`](#kind), [`PROCESS_WAIT`](#kind), [`USER_WAKE`](#kind), [`SHUTDOWN`](#kind), [`CLOSE`](#kind), [`BIND`](#kind), [`LISTEN`](#kind), [`RESOLVE`](#kind) | |
| [`READABLE`](#kind) | a stream is readable, at EOF, or failed; nothing is read and no buffer is held |

| On `SourceToken` | |
| :--- | :--- |
| [`source_id`](#source_id) | |

| On `Runtime` | |
| :--- | :--- |
| [`aliases`](#aliases) | whether a byte range overlaps the runtime or any storage reachable through it |
| [`capacity`](#capacity) | the slot table is the runtime's current size, not a limit it was given the slots the runtime holds now, which grow with load and fall back after it |
| [`pins_capacity`](#pins_capacity) | whether the live operation token names keeps capacity the runtime would otherwise give back |
| [`init`](#init) | every byte the runtime owns comes from a: its tables, its native event batch, and the tables of every driver registered on it |
| [`register_source`](#register_source), [`retire_source`](#retire_source), [`release_source`](#release_source), [`unregister_source`](#unregister_source) | |
| [`unrouted_events`](#unrouted_events) | native events whose source id matched no registered source since make |
| [`submit`](#submit), [`submit_owned`](#submit_owned) | |
| [`submit_scoped`](#submit_scoped) | prior cancellation is observed or the returned token is atomically scope-owned |
| [`submit_scoped_owned`](#submit_scoped_owned) | |
| [`complete`](#complete) | a byte completion |
| [`complete_copy`](#complete_copy) | copy is atomic with terminal publication |
| [`complete_opened`](#complete_opened) | a completion that hands the caller a socket it did not open itself, such as an accepted or a connected one, also carries that socket's opening, which is never zero |
| [`complete_batch`](#complete_batch) | batch completions report byte progress and completed item count separately, and after a cancellation claimed the operation both ride on its completion |
| [`fail`](#fail) | a failure after a cancellation claimed the operation is refused with CLOSED: the cancellation is reported in its place, with whatever transfer settled |
| [`complete_cancellation`](#complete_cancellation) | asynchronous sources publish only after target ownership has quiesced |
| [`complete_cancellation_transfer`](#complete_cancellation_transfer) | publish an asynchronous cancellation together with the transfer its native request finished before the cancellation took effect |
| [`submit_timer`](#submit_timer) | deadlines are absolute monotonic instants and never expire early late delivery is limited only by native scheduling and runtime dequeue latency |
| [`submit_timer_scoped`](#submit_timer_scoped) | |
| [`cancel_timer`](#cancel_timer) | expiry and cancellation race under one lock and publish one terminal result |
| [`poll`](#poll) | drains completions and expires due deadlines without entering the native wait a pending caller wake stays pending for the next wait or wait plan |
| [`prepare_wait`](#prepare_wait) | prepares another subsystem to wait on the runtime's native queue |
| [`begin_native_control`](#begin_native_control), [`end_native_control`](#end_native_control) | |
| [`wait`](#wait) | waits for completions |
| [`wake`](#wake) | ends a blocked wait early, or the next wait if none is blocked wakes coalesce: one wait answers every wake that came before its return |
| [`notify`](#notify) | makes a blocked wait collect every source again without ending it a source that queues completions off the native queue calls this, not wake |
| [`begin_close`](#begin_close) | close rejects new work and queues one terminal completion for every active operation |
| [`close`](#close) | |
| [`dnit`](#dnit) | destroy is valid only after close completions have been dequeued: a runtime that is not closed or already destroyed is INVALID, one with live operations, queued completions, a native controller or a registered source is EBUSY; a refused destroy keeps every allocation |
| [`pending`](#pending), [`snapshot`](#snapshot) | |

| Constants | |
| :--- | :--- |
| [`CANCELLATION_PENDING`](#constants), [`OPEN`](#constants), [`CLOSING`](#constants), [`CLOSED`](#constants), [`DESTROYED`](#constants) | |

---

## Kind

```mach
pub def Kind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `ACCEPT` | `0` |  |
| `CONNECT` | `1` |  |
| `READ` | `2` |  |
| `WRITE` | `3` |  |
| `RECEIVE_FROM` | `4` |  |
| `SEND_TO` | `5` |  |
| `FILE_READ` | `6` |  |
| `FILE_WRITE` | `7` |  |
| `TIMER` | `8` |  |
| `PROCESS_WAIT` | `9` |  |
| `USER_WAKE` | `10` |  |
| `SHUTDOWN` | `11` |  |
| `CLOSE` | `12` |  |
| `BIND` | `13` |  |
| `LISTEN` | `14` |  |
| `RESOLVE` | `15` |  |
| `READABLE` | `16` | a stream is readable, at EOF, or failed; nothing is read and no buffer is held |

## Token

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

## Operation

```mach
pub rec Operation {
    kind:     Kind;
    resource: usize;
    buffer:   *u8;
    length:   usize;
    offset:   u64;
    context:  usize;
}
```

buffer is borrowed from successful submission until its completion is dequeued

## Completion

```mach
pub rec Completion {
    token:         Token;
    kind:          Kind;
    context:       usize;
    bytes:         usize;
    items:         usize;
    resource:      usize;
    opening:       u64;
    has_error:     bool;
    error:         std.io.error.Error;
    end_of_stream: bool;
}
```

a terminal result. an error completion reports has_error and error, and a
cancelled, timed-out or closed one still reports in bytes, items and
end_of_stream the transfer that finished before the cancellation took
effect: bytes a read placed in its buffer, bytes a write sent, datagrams a
batch filled. those bytes belong to the stream, so a caller that cancels a
read consumes them like any other read's. opening is nonzero exactly when the
completion hands the caller a socket in resource: a successful accept or
connect, or a cancelled accept that had already accepted, whose socket the
caller owns and closes like any other

## NativeEvent

```mach
pub rec NativeEvent {
    context: usize;
    events:  u32;
    source:  u16;
    status:  i64;
    flags:   u64;
}
```

one native completion, laid out as the platform's IoCompletion

| Field | Type | |
| :--- | :--- | :--- |
| `source` | `u16` | the id of the source the event belongs to, 0 for a wake |

## SourceToken

```mach
pub rec SourceToken {
    index:      u32;
    generation: u32;
    tag:        u16;
}
```

### source_id

```mach
pub fun source_id(token: SourceToken) u16
```

## DispatchFun

```mach
pub def DispatchFun: fun(ptr, usize, u32, i64, u64) bool
```

offered each native event carrying the source's id, and every wake (context
0). returns true when the source consumed the event

## CancelFun

```mach
pub def CancelFun:   fun(ptr, Token, std.io.error.Error) i64
```

## ReleaseFun

```mach
pub def ReleaseFun:  fun(ptr, *Completion)
```

## WaitPlan

```mach
pub rec WaitPlan {
    wait:       bool;
    timeout_ms: i32;
    woken:      bool;
}
```

wait is false when the driver must not poll: the runtime is closed or a
caller woke it, and woken says which

## Runtime

```mach
pub rec Runtime {
    queue: std.system.os.IoQueue;
    # where every table's chunks come from
    allocator: std.allocator.Allocator;
    slots:     std.memory.table.Table;
    timers:    std.memory.table.Table;
    sources:   std.memory.table.Table;
    # a Route per source id ever issued, indexed by id
    source_routes: std.memory.table.Table;
    deadlines:     std.memory.table.Table;
    # open addressed on (owner, at), a power of two at least twice the slots
    deadline_index: std.memory.table.Table;
    deadline_pool:  std.memory.table.Pool;
    deadline_live:  usize;
    native_events:  *NativeEvent;
    initial:        usize;
    # its floor is the generation a slot of a regrown chunk starts from
    slot_pool:    std.memory.table.Pool;
    head:         usize;
    tail:         usize;
    count:        usize;
    live:         usize;
    timer_count:  usize;
    source_count: usize;
    # sources below this index have been initialised
    source_slots: usize;
    # registered sources per chunk of the source table
    source_live: [table.DIRECTORY]usize;
    # the source counterpart of the slot pool's floor
    source_floor: u32;
    # free source ids, each reused once no collection can still hold an event
    # harvested for it. id 0 is never issued
    route_pool: std.memory.table.Pool;
    # native collections begun and ended, each a harvest and its dispatch
    collections_begun: u64;
    collections_ended: u64;
    # native events whose source id matched no registered source
    unrouted:        u64;
    native_controls: usize;
    lifecycle:       std.io.lifecycle.Lifecycle;
    destroyed:       bool;
    # a caller's wake, pending until a wait or a wait plan answers it
    woken:       bool;
    lock:        std.sync.mutex.Mutex;
    native_lock: std.sync.mutex.Mutex;
    # held for a whole native control, so a waiter can yield to one
    control_lock: std.sync.mutex.Mutex;
}
```

one thread owns wait and dequeue, while submission and resolution may be concurrent

### aliases

```mach
pub fun aliases(runtime: *Runtime, data: *u8, len: usize) bool
```

whether a byte range overlaps the runtime or any storage reachable through it

read-only and allocation-free, and it takes the runtime's lock, so it waits
for an operation in progress and costs a lock per call. the queried range must
not change during the query. a caller may query while ordinary operations run,
but must synchronize with initialization and destruction. the answer is exact
for the tables as they stand under the lock: an operation that adds or
releases a chunk lands wholly before or wholly after the query. the drivers
take this and their own locks one at a time, so an answer from one of them is
exact per owner, and a range in a chunk being added or released can answer
either way there. any other range answers the same either way.

a non-empty malformed range, or an uninitialized, partially initialized,
partially torn-down or destroyed owner, reports overlap. an empty range owns
no bytes and reports none. endpoints are inclusive: a one-byte range at
usize::MAX is valid, and anything extending past it is malformed.

### capacity

```mach
pub fun capacity(runtime: *Runtime) usize
```

the slot table is the runtime's current size, not a limit it was given
the slots the runtime holds now, which grow with load and fall back after it

### pins_capacity

```mach
pub fun pins_capacity(runtime: *Runtime, token: Token) bool
```

whether the live operation token names keeps capacity the runtime would
otherwise give back

the runtime gives back a chunk of its slot table only once that chunk and the
one below it hold nothing live, and its timer, deadline and driver tables
follow the slot table down. an operation submitted at a peak takes the lowest
free slot, which is as high as the peak, so one that stays pending after the
load leaves holds every chunk up to its own. this is true when the
operation's slot lies above the slack chunk past where the live count would
end if every live slot were packed from index 0, and the table holds a chunk
past that slack: moving every such operation to the lowest free slots lets
the runtime release it. an operation submitted now takes the lowest free
slot, which never pins, so a caller that cancels and resubmits an operation
that pins never has to do it twice for the same peak

| Parameter | |
| :--- | :--- |
| `runtime` | the runtime the operation was submitted to |
| `token` | the operation |
| **returns** | false for a stale token, an operation whose completion was taken, or a runtime over an allocator that never reclaims, whose tables keep their peak anyway |

### init

```mach
pub fun init(runtime: *Runtime, a: *std.allocator.Allocator, initial: usize) err[std.io.error.Error]
```

every byte the runtime owns comes from a: its tables, its native event
batch, and the tables of every driver registered on it. the runtime keeps a
copy of a, so a's context must outlive the runtime. a refusal from a is the
only ceiling: initial is the size the runtime starts at, and the slot, timer
and source tables grow on demand until a refuses. what a peak grew goes back
to a once the load drains, keeping one chunk of slack above what is live, and
nothing live moves when it does.

| Parameter | |
| :--- | :--- |
| `runtime` | the runtime to initialize |
| `a` | where every allocation is taken from and returned to |
| `initial` | slots, timers and deadline records to start with, at least one |
| **returns** | ok, INVALID for a nil runtime or allocator or an initial size of zero, RESOURCE_EXHAUSTED when a refuses |

### register_source

```mach
pub fun register_source(
    runtime: *Runtime,
    context: ptr,
    dispatch: DispatchFun,
    cancel_operation: CancelFun,
    release: ReleaseFun,
) res[SourceToken, std.io.error.Error]
```

### retire_source

```mach
pub fun retire_source(runtime: *Runtime, token: SourceToken) res[bool, std.io.error.Error]
```

### release_source

```mach
pub fun release_source(runtime: *Runtime, token: SourceToken) err[std.io.error.Error]
```

### unregister_source

```mach
pub fun unregister_source(runtime: *Runtime, token: SourceToken) err[std.io.error.Error]
```

### unrouted_events

```mach
pub fun unrouted_events(runtime: *Runtime) u64
```

native events whose source id matched no registered source since make

a nonzero count is not by itself an error. a correct program raises it when a
source is released between the harvest of a native batch and the dispatch of
that source's event. a count that keeps rising with no releases points at a
backend reporting a wrong id

### submit

```mach
pub fun submit(runtime: *Runtime, operation: Operation) res[Token, std.io.error.Error]
```

### submit_owned

```mach
pub fun submit_owned(runtime: *Runtime, source_token: SourceToken, operation: Operation) res[Token, std.io.error.Error]
```

### submit_scoped

```mach
pub fun submit_scoped(runtime: *Runtime, scope: *std.sync.cancel.Scope, operation: Operation) res[Token, std.io.error.Error]
```

prior cancellation is observed or the returned token is atomically scope-owned

### submit_scoped_owned

```mach
pub fun submit_scoped_owned(
    runtime: *Runtime,
    source_token: SourceToken,
    scope: *std.sync.cancel.Scope,
    operation: Operation,
) res[Token, std.io.error.Error]
```

### complete

```mach
pub fun complete(runtime: *Runtime, token: Token, bytes: usize, resource: usize, end_of_stream: bool) err[std.io.error.Error]
```

a byte completion. one that finishes after a cancellation claimed the
operation is carried by the cancelled completion instead, and still succeeds

### complete_copy

```mach
pub fun complete_copy(runtime: *Runtime, token: Token, source: *u8, bytes: usize, resource: usize, end_of_stream: bool) err[std.io.error.Error]
```

copy is atomic with terminal publication. after a cancellation claimed the
operation the copy still lands and the cancelled completion reports it

### complete_opened

```mach
pub fun complete_opened(runtime: *Runtime, token: Token, resource: usize, opening: u64) err[std.io.error.Error]
```

a completion that hands the caller a socket it did not open itself, such as
an accepted or a connected one, also carries that socket's opening, which is
never zero. after a cancellation claimed an accept, the accepted socket rides
on the cancelled completion and this succeeds: the caller of the accept owns
it. after a cancellation claimed any other operation this is refused with
CLOSED, and the caller of this keeps, and closes, the socket

| Parameter | |
| :--- | :--- |
| `resource` | the native socket |
| `opening` | the opening its handle was stamped with (std.io.handle) |

### complete_batch

```mach
pub fun complete_batch(runtime: *Runtime, token: Token, bytes: usize, items: usize, resource: usize) err[std.io.error.Error]
```

batch completions report byte progress and completed item count separately,
and after a cancellation claimed the operation both ride on its completion

### fail

```mach
pub fun fail(runtime: *Runtime, token: Token, failure: std.io.error.Error) err[std.io.error.Error]
```

a failure after a cancellation claimed the operation is refused with CLOSED:
the cancellation is reported in its place, with whatever transfer settled

### complete_cancellation

```mach
pub fun complete_cancellation(runtime: *Runtime, token: Token) err[std.io.error.Error]
```

asynchronous sources publish only after target ownership has quiesced

### complete_cancellation_transfer

```mach
pub fun complete_cancellation_transfer(runtime: *Runtime, token: Token, bytes: usize, items: usize, end_of_stream: bool) err[std.io.error.Error]
```

publish an asynchronous cancellation together with the transfer its native
request finished before the cancellation took effect. a transfer a
completion already recorded for the operation describes the same request,
so the larger of the two is published, never their sum

| Parameter | |
| :--- | :--- |
| `bytes` | bytes the request moved |
| `items` | datagrams a batch filled |
| `end_of_stream` | whether a read reached the end of its stream |

### submit_timer

```mach
pub fun submit_timer(runtime: *Runtime, deadline: std.chrono.time.Instant, context: usize) res[Token, std.io.error.Error]
```

deadlines are absolute monotonic instants and never expire early
late delivery is limited only by native scheduling and runtime dequeue latency

### submit_timer_scoped

```mach
pub fun submit_timer_scoped(runtime: *Runtime, scope: *std.sync.cancel.Scope, deadline: std.chrono.time.Instant, context: usize) res[Token, std.io.error.Error]
```

### cancel_timer

```mach
pub fun cancel_timer(runtime: *Runtime, token: Token) err[std.io.error.Error]
```

expiry and cancellation race under one lock and publish one terminal result

### poll

```mach
pub fun poll(runtime: *Runtime, output: *Completion, output_capacity: usize) res[usize, std.io.error.Error]
```

drains completions and expires due deadlines without entering the native wait
a pending caller wake stays pending for the next wait or wait plan

### prepare_wait

```mach
pub fun prepare_wait(runtime: *Runtime, timeout_ms: i32) res[WaitPlan, std.io.error.Error]
```

prepares another subsystem to wait on the runtime's native queue

the driver polls the queue for at most timeout_ms and then drains with poll.
the queue also carries the runtime's own wakes, so a poll that returns with
nothing drained is not a reason to stop: the driver prepares again with the
time it has left, and ends early only on a plan with woken set, which answers
a caller's wake. a plan with wait unset must not be polled.

| Parameter | |
| :--- | :--- |
| `timeout_ms` | relative bound on the driver's poll, -1 for unbounded |
| **returns** | the plan, or the runtime's refusal |

### begin_native_control

```mach
pub fun begin_native_control(runtime: *Runtime) err[std.io.error.Error]
```

### end_native_control

```mach
pub fun end_native_control(runtime: *Runtime)
```

### wait

```mach
pub fun wait(runtime: *Runtime, output: *Completion, output_capacity: usize, timeout_ms: i32) res[usize, std.io.error.Error]
```

waits for completions

returns 0 only when timeout_ms has passed, a caller called wake, or the
runtime is closed with nothing left to return. the runtime's own wakes, such
as the one a submission posts, never end a wait early: the wait keeps waiting
for the time that remains. a return that carries completions also answers a
pending wake.

| Parameter | |
| :--- | :--- |
| `output` | completions are written here; the caller owns it and may reuse it after this call returns |
| `output_capacity` | the most completions one call writes |
| `timeout_ms` | relative bound, 0 to collect without blocking, -1 for unbounded |
| **returns** | the number of completions written, or the refusal |

### wake

```mach
pub fun wake(runtime: *Runtime) err[std.io.error.Error]
```

ends a blocked wait early, or the next wait if none is blocked
wakes coalesce: one wait answers every wake that came before its return

### notify

```mach
pub fun notify(runtime: *Runtime) err[std.io.error.Error]
```

makes a blocked wait collect every source again without ending it
a source that queues completions off the native queue calls this, not wake

### begin_close

```mach
pub fun begin_close(runtime: *Runtime, mode: std.io.lifecycle.Mode, cause: std.io.lifecycle.Cause) res[std.io.lifecycle.CloseResult, std.io.error.Error]
```

close rejects new work and queues one terminal completion for every active operation

### close

```mach
pub fun close(runtime: *Runtime) res[bool, std.io.error.Error]
```

### dnit

```mach
pub fun dnit(runtime: *Runtime) err[std.io.error.Error]
```

destroy is valid only after close completions have been dequeued: a runtime
that is not closed or already destroyed is INVALID, one with live operations,
queued completions, a native controller or a registered source is EBUSY;
a refused destroy keeps every allocation

### pending

```mach
pub fun pending(runtime: *Runtime) usize
```

### snapshot

```mach
pub fun snapshot(runtime: *Runtime) std.io.lifecycle.Snapshot
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CANCELLATION_PENDING` | `i64` | `1` |  |
| `OPEN` | `u8` | `lifecycle.OPEN` |  |
| `CLOSING` | `u8` | `lifecycle.CLOSING` |  |
| `CLOSED` | `u8` | `lifecycle.CLOSED` |  |
| `DESTROYED` | `u8` | `3` |  |

