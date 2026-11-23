[std](../../README.md) / [io](../README.md) / [file](README.md) / **adapter**

# std.io.file.adapter

bounded worker-backed file completion adapter

Source: [`src/io/file/adapter.mach`](../../../../src/io/file/adapter.mach)

Uses types from [`std.filesystem`](../../filesystem.md), [`std.io.error`](../error.md), [`std.io.runtime`](../runtime.md), [`std.memory.secret`](../../memory/secret.md), [`std.sync.cancel`](../../sync/cancel.md), [`std.sync.mutex`](../../sync/mutex.md), [`std.sync.thread`](../../sync/thread.md), [`std.sync.worker_pool`](../../sync/worker_pool.md).

| Type | | |
| :--- | :--- | :--- |
| [`Request`](#request) | `rec` | a secret request names its scratch span and read destination by borrow handle only: no welded pointer is stored here, so the request stays a `ptr` context the worker pool and the runtime can carry |
| [`Adapter`](#adapter) | `rec` | request, task, abort, worker, thread, and scratch storage are caller-owned the adapter is initialized in place by init: the runtime source and the worker pool hold its address until dnit |

| On `Adapter` | |
| :--- | :--- |
| [`init`](#init) | initializes an adapter in place, registers it with the runtime and starts its workers |
| [`submit_read`](#submit_read) | file handles and cancellation scopes remain borrowed until the request retires read buffers remain borrowed until their runtime completion is dequeued |
| [`submit_write`](#submit_write) | write bytes are copied into bounded adapter storage before this call succeeds |
| [`attach_secret_scratch`](#attach_secret_scratch) | lend welded scratch to the adapter for secret requests: one span of max_transfer bytes per request, the same geometry as the public scratch |
| [`submit_secret_read`](#submit_secret_read) | the welded destination is borrowed until the completion is dequeued, and is written exactly then with exactly the delivered prefix; on any error or cancellation it is unchanged |
| [`submit_secret_write`](#submit_secret_write) | welded bytes are copied into the attached secret scratch before this call succeeds; the caller's storage is not borrowed past the return |
| [`shutdown_drain`](#shutdown_drain) | stops new submissions, lets queued and running requests finish and joins the workers |
| [`shutdown_abort`](#shutdown_abort) | stops new submissions, fails queued requests as CANCELLED and joins the workers |
| [`active`](#active) | the number of requests claimed and not yet retired |
| [`dnit`](#dnit) | retires the runtime source, destroys the pool and ends the secret scratch borrow |

---

## Request

```mach
pub rec Request {
    adapter:        *Adapter;
    state:          i64;
    kind:           std.io.runtime.Kind;
    file:           std.filesystem.File;
    length:         usize;
    offset:         u64;
    scratch:        *u8;
    token:          std.io.runtime.Token;
    secret:         bool;
    scratch_offset: usize;
    arrivals:       usize;
    borrow:         std.memory.secret.Borrow;
}
```

a secret request names its scratch span and read destination by borrow
handle only: no welded pointer is stored here, so the request stays a `ptr`
context the worker pool and the runtime can carry. a secret request is
retired by the later of two arrivals, its resolution (PUBLISHED, not FREE)
and the runtime dequeuing its completion; the dequeue is when the delivered
prefix lands in the caller's welded storage, and the retire is when the
scratch span is wiped and the borrow ends

## Adapter

```mach
pub rec Adapter {
    runtime:          *std.io.runtime.Runtime;
    source:           std.io.runtime.SourceToken;
    requests:         *Request;
    request_capacity: usize;
    scratch:          *u8;
    scratch_length:   usize;
    max_transfer:     usize;
    secret_scratch:   std.memory.secret.Borrow;
    secret_attached:  bool;
    tasks:            *std.sync.worker_pool.Task;
    abort_tasks:      *std.sync.worker_pool.Task;
    threads:          *std.sync.thread.Thread;
    workers:          *std.sync.worker_pool.Worker;
    worker_count:     usize;
    pool:             std.sync.worker_pool.Pool;
    next_request:     usize;
    active:           usize;
    state:            u8;
    initialized:      bool;
    lock:             std.sync.mutex.Mutex;
}
```

request, task, abort, worker, thread, and scratch storage are caller-owned
the adapter is initialized in place by init: the runtime source and the
worker pool hold its address until dnit

### init

```mach
pub fun init(
    adapter: *Adapter,
    runtime: *std.io.runtime.Runtime,
    requests: *Request,
    request_capacity: usize,
    scratch: *u8,
    scratch_length: usize,
    max_transfer: usize,
    tasks: *std.sync.worker_pool.Task,
    abort_tasks: *std.sync.worker_pool.Task,
    threads: *std.sync.thread.Thread,
    workers: *std.sync.worker_pool.Worker,
    worker_count: usize,
) err[std.io.error.Error]
```

initializes an adapter in place, registers it with the runtime and starts its workers

| Parameter | |
| :--- | :--- |
| `adapter` | the adapter to initialize, address-bound until dnit |
| `runtime` | the runtime completions are published to |
| `requests` | request_capacity request slots |
| `request_capacity` | the most requests in flight at once |
| `scratch` | public staging storage, one max_transfer span per request |
| `scratch_length` | size of scratch in bytes, at least request_capacity * max_transfer |
| `max_transfer` | the largest single read or write in bytes |
| `tasks` | request_capacity task slots for the worker pool queue |
| `abort_tasks` | request_capacity task slots that receive queued work on abort |
| `threads` | worker_count thread slots |
| `workers` | worker_count worker slots |
| `worker_count` | the number of worker threads |
| **returns** | the failure. INVALID for a nil pointer, a zero count or a zero max_transfer, RESOURCE_EXHAUSTED when scratch is too small or its required size overflows, the runtime's registration failure, or WOULD_BLOCK when the pool refused to start |

### submit_read

```mach
pub fun submit_read(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

file handles and cancellation scopes remain borrowed until the request retires
read buffers remain borrowed until their runtime completion is dequeued

### submit_write

```mach
pub fun submit_write(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

write bytes are copied into bounded adapter storage before this call succeeds

### attach_secret_scratch

```mach
pub fun attach_secret_scratch(adapter: *Adapter, scratch: *^u8, scratch_length: usize) err[std.io.error.Error]
```

lend welded scratch to the adapter for secret requests: one span of
max_transfer bytes per request, the same geometry as the public scratch.
the storage stays the caller's; the adapter wipes each span after its
request's terminal completion is dequeued, wipes the whole of it and ends
the borrow in dnit, and the caller releases it after that

### submit_secret_read

```mach
pub fun submit_secret_read(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *^u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the welded destination is borrowed until the completion is dequeued, and is
written exactly then with exactly the delivered prefix; on any error or
cancellation it is unchanged

### submit_secret_write

```mach
pub fun submit_secret_write(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *^u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

welded bytes are copied into the attached secret scratch before this call
succeeds; the caller's storage is not borrowed past the return

### shutdown_drain

```mach
pub fun shutdown_drain(adapter: *Adapter) res[bool, std.io.error.Error]
```

stops new submissions, lets queued and running requests finish and joins the workers

| Parameter | |
| :--- | :--- |
| `adapter` | the adapter to drain |
| **returns** | true when this call drained it, false when it was already joined. INVALID for a nil or uninitialized adapter, BUSY while another shutdown is under way or after dnit began, IO when the pool fails to close or join |

### shutdown_abort

```mach
pub fun shutdown_abort(adapter: *Adapter) res[usize, std.io.error.Error]
```

stops new submissions, fails queued requests as CANCELLED and joins the workers

requests already running finish normally

| Parameter | |
| :--- | :--- |
| `adapter` | the adapter to abort |
| **returns** | the number of queued requests failed, or the failure. INVALID for a nil or uninitialized adapter, BUSY unless the adapter is open, IO when the pool fails to close or join |

### active

```mach
pub fun active(adapter: *Adapter) usize
```

the number of requests claimed and not yet retired

| Parameter | |
| :--- | :--- |
| `adapter` | the adapter to inspect |
| **returns** | the count, 0 for a nil or uninitialized adapter |

### dnit

```mach
pub fun dnit(adapter: *Adapter) err[std.io.error.Error]
```

retires the runtime source, destroys the pool and ends the secret scratch borrow

the adapter must be joined by a shutdown with no request outstanding. a call
that fails part-way may be repeated and resumes where it stopped

| Parameter | |
| :--- | :--- |
| `adapter` | the adapter to tear down |
| **returns** | the failure. INVALID for a nil or uninitialized adapter, BUSY before the join or while requests are outstanding, the runtime's retire or release failure, or IO when the pool cannot be destroyed |

