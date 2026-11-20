[std](../README.md) / [sync](README.md) / **worker_pool**

# std.sync.worker_pool

bounded caller-owned worker pool

Source: [`src/sync/worker_pool.mach`](../../../src/sync/worker_pool.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.sync.cancel`](cancel.md), [`std.sync.channel`](channel.md), [`std.sync.condition`](condition.md), [`std.sync.mutex`](mutex.md), [`std.sync.thread`](thread.md).

| Type | | |
| :--- | :--- | :--- |
| [`TaskFun`](#taskfun) | `def` |  |
| [`Task`](#task) | `rec` | context is borrowed after acceptance and returned by completion or abort |
| [`Status`](#status) | `tag` | the outcome of a pool operation, and the pool's lifecycle state |
| [`StateError`](#stateerror) | `tag` | a refused pool destruction |
| [`Operation`](#operation) | `def` |  |
| [`Worker`](#worker) | `rec` | the argument one worker thread starts with |
| [`Pool`](#pool) | `rec` | all backing arrays and task contexts are caller-owned |
| [`Stats`](#stats-1) | `rec` | a snapshot of pool counters |

| On `Pool` | |
| :--- | :--- |
| [`make_with_config`](#make_with_config) | workers are unfair, task failure is counted, and the worker continues callbacks must not unwind or reclaim their context before pool ownership ends |
| [`make`](#make) | make a pool whose workers use the default thread configuration |
| [`try_submit`](#try_submit) | rejected tasks and their contexts remain submitter-owned |
| [`submit`](#submit) | queue a task, sleeping until a slot is free or the pool closes |
| [`submit_until`](#submit_until) | queue a task, sleeping no later than an absolute monotonic deadline |
| [`submit_scoped`](#submit_scoped) | queue a task, sleeping until a slot is free or the scope is cancelled or times out |
| [`close_drain`](#close_drain) | drain rejects new work while workers finish every accepted task |
| [`close_abort`](#close_abort) | abort returns every task still owned by the queue in fifo order a task already owned by a worker runs to completion before join returns |
| [`join`](#join) | join is valid after drain or abort and releases every worker resource callbacks must not join their own pool |
| [`shutdown_drain`](#shutdown_drain) | close_drain then join |
| [`shutdown_abort`](#shutdown_abort) | close_abort then join |
| [`state`](#state) | read the pool's lifecycle state |
| [`last_thread_error`](#last_thread_error) | the portable code of the first retained worker refusal, 0 when none |
| [`stats`](#stats) | read the pool's counters |
| [`dnit`](#dnit) | destruction is valid only after join and does not own caller storage |

---

## TaskFun

```mach
pub def TaskFun: fun(ptr) bool
```

## Task

```mach
pub rec Task {
    context: ptr;
    run:     TaskFun;
}
```

context is borrowed after acceptance and returned by completion or abort

| Field | Type | |
| :--- | :--- | :--- |
| `context` | `ptr` | caller pointer passed to run |
| `run` | `TaskFun` | task body, never nil for a submitted task |

## Status

```mach
pub tag Status: u8 {
    invalid;
    accepted;
    queue_full;
    pool_closed;
    timed_out;
    cancelled;
    spawn_failed: std.sync.thread.ThreadError;
    draining;
    aborting;
    joined;
    join_failed: std.sync.thread.ThreadError;
    joining;
}
```

the outcome of a pool operation, and the pool's lifecycle state

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | nil operands, an unmade pool, a task without a run function, an abort output too small, or an operation the state refuses |
| `accepted` |  | the task is queued (submit) or the pool is open (make, state) |
| `queue_full` |  | no slot was free (try_submit) |
| `pool_closed` |  | the queue no longer accepts work |
| `timed_out` |  | the absolute deadline passed first |
| `cancelled` |  | the scope was cancelled first |
| `spawn_failed` | `std.sync.thread.ThreadError` | a worker could not be spawned, the started workers were joined and the pool holds the refusal, ready for dnit unless one of those joins was refused |
| `draining` |  | new work is refused while workers finish accepted tasks |
| `aborting` |  | queued tasks were returned; in-flight tasks finish |
| `joined` |  | every worker resource is released |
| `join_failed` | `std.sync.thread.ThreadError` | a worker join was refused; the first refusal is carried |
| `joining` |  | another caller is joining |

## StateError

```mach
pub tag StateError: u8 { invalid; unjoined; busy; queue: std.sync.channel.StateError; }
```

a refused pool destruction

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil or unmade pool |
| `unjoined` |  | the pool has not reached joined |
| `busy` |  | callers are still waiting on join |
| `queue` | `std.sync.channel.StateError` | the queue refused destruction |

## Operation

```mach
pub def Operation: err[StateError]
```

## Worker

```mach
pub rec Worker {
    pool:  *Pool;
    index: usize;
}
```

the argument one worker thread starts with

| Field | Type | |
| :--- | :--- | :--- |
| `pool` | `*Pool` | pool the worker serves |
| `index` | `usize` | position of the worker in the pool's arrays |

## Pool

```mach
pub rec Pool {
    queue:        std.sync.channel.Channel[Task];
    threads:      *std.sync.thread.Thread;
    workers:      *Worker;
    worker_count: usize;
    started:      usize;
    state:        u8;
    completed:    i64;
    failed:       i64;
    thread_error: std.sync.thread.ThreadError;
    has_error:    bool;
    initialized:  bool;
    lock:         std.sync.mutex.Mutex;
    joined:       std.sync.condition.Condition;
}
```

all backing arrays and task contexts are caller-owned

prepare it with make or make_with_config and release it with dnit. the
fields are internal.

| Field | Type | |
| :--- | :--- | :--- |
| `queue` | `std.sync.channel.Channel[Task]` | bounded task channel over the caller's queue storage |
| `threads` | `*std.sync.thread.Thread` | caller array of worker_count thread handles |
| `workers` | `*Worker` | caller array of worker_count worker arguments |
| `worker_count` | `usize` | number of workers asked for |
| `started` | `usize` | number of workers actually spawned |
| `state` | `u8` | lifecycle state, guarded by lock |
| `completed` | `i64` | tasks run, counted atomically |
| `failed` | `i64` | tasks whose run returned false, counted atomically |
| `thread_error` | `std.sync.thread.ThreadError` | first retained spawn or join refusal, valid when has_error |
| `has_error` | `bool` | whether thread_error holds a refusal |
| `initialized` | `bool` | true between make and dnit |
| `lock` | `std.sync.mutex.Mutex` | guards state and the error fields |
| `joined` | `std.sync.condition.Condition` | signalled when a join finishes |

### make_with_config

```mach
pub fun make_with_config(pool: *Pool, queue_storage: *Task, queue_capacity: usize, threads: *std.sync.thread.Thread, workers: *Worker, worker_count: usize, config: *std.sync.thread.Config) Status
```

workers are unfair, task failure is counted, and the worker continues
callbacks must not unwind or reclaim their context before pool ownership ends

| Parameter | |
| :--- | :--- |
| `pool` | storage to make into an open pool |
| `queue_storage` | caller array of queue_capacity task slots |
| `queue_capacity` | number of queue slots, at least 1 |
| `threads` | caller array of worker_count thread handles |
| `workers` | caller array of worker_count worker arguments |
| `worker_count` | number of workers to spawn, at least 1 |
| `config` | creation policy for every worker thread |
| **returns** | accepted once every worker runs, invalid for nil or zero operands, or spawn_failed with the refusal |

### make

```mach
pub fun make(pool: *Pool, queue_storage: *Task, queue_capacity: usize, threads: *std.sync.thread.Thread, workers: *Worker, worker_count: usize) Status
```

make a pool whose workers use the default thread configuration

| Parameter | |
| :--- | :--- |
| `pool` | storage to make into an open pool |
| `queue_storage` | caller array of queue_capacity task slots |
| `queue_capacity` | number of queue slots, at least 1 |
| `threads` | caller array of worker_count thread handles |
| `workers` | caller array of worker_count worker arguments |
| `worker_count` | number of workers to spawn, at least 1 |
| **returns** | as make_with_config |

### try_submit

```mach
pub fun try_submit(pool: *Pool, task: Task) Status
```

rejected tasks and their contexts remain submitter-owned

| Parameter | |
| :--- | :--- |
| `pool` | open pool |
| `task` | task to queue |
| **returns** | accepted, queue_full, pool_closed, or invalid for a nil or unmade pool or a task without a run function |

### submit

```mach
pub fun submit(pool: *Pool, task: Task) Status
```

queue a task, sleeping until a slot is free or the pool closes

| Parameter | |
| :--- | :--- |
| `pool` | open pool |
| `task` | task to queue |
| **returns** | accepted, pool_closed, or invalid |

### submit_until

```mach
pub fun submit_until(pool: *Pool, task: Task, deadline: std.chrono.time.Instant) Status
```

queue a task, sleeping no later than an absolute monotonic deadline

| Parameter | |
| :--- | :--- |
| `pool` | open pool |
| `task` | task to queue |
| `deadline` | absolute monotonic instant to give up at |
| **returns** | accepted, pool_closed, timed_out, or invalid |

### submit_scoped

```mach
pub fun submit_scoped(pool: *Pool, scope: *std.sync.cancel.Scope, task: Task) Status
```

queue a task, sleeping until a slot is free or the scope is cancelled or times out

| Parameter | |
| :--- | :--- |
| `pool` | open pool |
| `scope` | cancellation scope that ends the wait |
| `task` | task to queue |
| **returns** | accepted, pool_closed, cancelled, timed_out, or invalid |

### close_drain

```mach
pub fun close_drain(pool: *Pool) Status
```

drain rejects new work while workers finish every accepted task

| Parameter | |
| :--- | :--- |
| `pool` | pool to close |
| **returns** | draining, the current state when the pool was not open, or invalid |

### close_abort

```mach
pub fun close_abort(pool: *Pool, rejected: *Task, rejected_capacity: usize, rejected_len: *usize) Status
```

abort returns every task still owned by the queue in fifo order
a task already owned by a worker runs to completion before join returns

| Parameter | |
| :--- | :--- |
| `pool` | pool to abort, open or draining |
| `rejected` | caller array that receives the queued tasks |
| `rejected_capacity` | number of slots in rejected |
| `rejected_len` | receives the number of tasks returned |
| **returns** | aborting, the current state when already aborting or joined, or invalid, including a rejected array too small |

### join

```mach
pub fun join(pool: *Pool) Status
```

join is valid after drain or abort and releases every worker resource
callbacks must not join their own pool

| Parameter | |
| :--- | :--- |
| `pool` | drained or aborted pool |
| **returns** | joined, join_failed with the first refusal, or invalid for a nil, unmade or still open pool |

### shutdown_drain

```mach
pub fun shutdown_drain(pool: *Pool) Status
```

close_drain then join

| Parameter | |
| :--- | :--- |
| `pool` | pool to shut down |
| **returns** | the join's status, or close_drain's when it refused |

### shutdown_abort

```mach
pub fun shutdown_abort(pool: *Pool, rejected: *Task, rejected_capacity: usize, rejected_len: *usize) Status
```

close_abort then join

| Parameter | |
| :--- | :--- |
| `pool` | pool to shut down |
| `rejected` | caller array that receives the queued tasks |
| `rejected_capacity` | number of slots in rejected |
| `rejected_len` | receives the number of tasks returned |
| **returns** | the join's status, or close_abort's when it refused |

### state

```mach
pub fun state(pool: *Pool) Status
```

read the pool's lifecycle state

| Parameter | |
| :--- | :--- |
| `pool` | pool to read |
| **returns** | accepted while open, draining, aborting, joining, joined, join_failed, or invalid for a nil or unmade pool |

### last_thread_error

```mach
pub fun last_thread_error(pool: *Pool) i64
```

the portable code of the first retained worker refusal, 0 when none

| Parameter | |
| :--- | :--- |
| `pool` | pool to read |
| **returns** | the code, or thread.ERROR_INVALID for a nil or unmade pool |

### stats

```mach
pub fun stats(pool: *Pool) Stats
```

read the pool's counters

| Parameter | |
| :--- | :--- |
| `pool` | pool to read |
| **returns** | the counters, all zero for a nil or unmade pool |

### dnit

```mach
pub fun dnit(pool: *Pool) Operation
```

destruction is valid only after join and does not own caller storage

| Parameter | |
| :--- | :--- |
| **returns** | ok once destroyed, invalid for a nil or unmade pool, unjoined before join completed, busy while joiners wait, or the queue's own refusal |

## Stats

```mach
pub rec Stats {
    completed: usize;
    failed:    usize;
    queued:    usize;
}
```

a snapshot of pool counters

| Field | Type | |
| :--- | :--- | :--- |
| `completed` | `usize` | tasks run so far, failed ones included |
| `failed` | `usize` | tasks whose run returned false |
| `queued` | `usize` | tasks accepted and not yet taken by a worker |

