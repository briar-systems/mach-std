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
| [`Worker`](#worker) | `rec` |  |
| [`Pool`](#pool) | `rec` | all backing arrays and task contexts are caller-owned |
| [`Stats`](#stats-1) | `rec` |  |

| On `Pool` | |
| :--- | :--- |
| [`make_with_config`](#make_with_config) | workers are unfair, task failure is counted, and the worker continues callbacks must not unwind or reclaim their context before pool ownership ends |
| [`make`](#make) | |
| [`try_submit`](#try_submit) | rejected tasks and their contexts remain submitter-owned |
| [`submit`](#submit), [`submit_until`](#submit_until), [`submit_scoped`](#submit_scoped) | |
| [`close_drain`](#close_drain) | drain rejects new work while workers finish every accepted task |
| [`close_abort`](#close_abort) | abort returns every task still owned by the queue in fifo order a task already owned by a worker runs to completion before join returns |
| [`join`](#join) | join is valid after drain or abort and releases every worker resource callbacks must not join their own pool |
| [`shutdown_drain`](#shutdown_drain), [`shutdown_abort`](#shutdown_abort), [`state`](#state) | |
| [`last_thread_error`](#last_thread_error) | the portable code of the first retained worker refusal, 0 when none |
| [`stats`](#stats) | |
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
| `spawn_failed` | `std.sync.thread.ThreadError` | a worker could not be spawned; the pool is joined and holds the refusal, ready for destroy |
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

### make_with_config

```mach
pub fun make_with_config(pool: *Pool, queue_storage: *Task, queue_capacity: usize, threads: *std.sync.thread.Thread, workers: *Worker, worker_count: usize, config: *std.sync.thread.Config) Status
```

workers are unfair, task failure is counted, and the worker continues
callbacks must not unwind or reclaim their context before pool ownership ends

### make

```mach
pub fun make(pool: *Pool, queue_storage: *Task, queue_capacity: usize, threads: *std.sync.thread.Thread, workers: *Worker, worker_count: usize) Status
```

### try_submit

```mach
pub fun try_submit(pool: *Pool, task: Task) Status
```

rejected tasks and their contexts remain submitter-owned

### submit

```mach
pub fun submit(pool: *Pool, task: Task) Status
```

### submit_until

```mach
pub fun submit_until(pool: *Pool, task: Task, deadline: std.chrono.time.Instant) Status
```

### submit_scoped

```mach
pub fun submit_scoped(pool: *Pool, scope: *std.sync.cancel.Scope, task: Task) Status
```

### close_drain

```mach
pub fun close_drain(pool: *Pool) Status
```

drain rejects new work while workers finish every accepted task

### close_abort

```mach
pub fun close_abort(pool: *Pool, rejected: *Task, rejected_capacity: usize, rejected_len: *usize) Status
```

abort returns every task still owned by the queue in fifo order
a task already owned by a worker runs to completion before join returns

### join

```mach
pub fun join(pool: *Pool) Status
```

join is valid after drain or abort and releases every worker resource
callbacks must not join their own pool

### shutdown_drain

```mach
pub fun shutdown_drain(pool: *Pool) Status
```

### shutdown_abort

```mach
pub fun shutdown_abort(pool: *Pool, rejected: *Task, rejected_capacity: usize, rejected_len: *usize) Status
```

### state

```mach
pub fun state(pool: *Pool) Status
```

### last_thread_error

```mach
pub fun last_thread_error(pool: *Pool) i64
```

the portable code of the first retained worker refusal, 0 when none

### stats

```mach
pub fun stats(pool: *Pool) Stats
```

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

