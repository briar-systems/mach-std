[std](../../README.md) / [io](../README.md) / [file](README.md) / **adapter**

# std.io.file.adapter

bounded worker-backed file completion adapter

Source: [`src/io/file/adapter.mach`](../../../../src/io/file/adapter.mach)

Uses types from [`std.filesystem`](../../filesystem.md), [`std.io.error`](../error.md), [`std.io.runtime`](../runtime.md), [`std.memory.secret`](../../memory/secret.md), [`std.sync.cancel`](../../sync/cancel.md), [`std.sync.mutex`](../../sync/mutex.md), [`std.sync.thread`](../../sync/thread.md), [`std.sync.worker_pool`](../../sync/worker_pool.md).

| Type | | |
| :--- | :--- | :--- |
| [`Request`](#request) | `rec` | a secret request names its scratch span and read destination by borrow handle only: no welded pointer is stored here, so the request stays a `ptr` context the worker pool and the runtime can carry |
| [`Adapter`](#adapter) | `rec` | request, task, abort, worker, thread, and scratch storage are caller-owned the adapter is initialized in place by make: the runtime source and the worker pool hold its address until destroy |

| On `Adapter` | |
| :--- | :--- |
| [`init`](#init) | |
| [`submit_read`](#submit_read) | file handles and cancellation scopes remain borrowed until the request retires read buffers remain borrowed until their runtime completion is dequeued |
| [`submit_write`](#submit_write) | write bytes are copied into bounded adapter storage before this call succeeds |
| [`attach_secret_scratch`](#attach_secret_scratch) | lend welded scratch to the adapter for secret requests: one span of max_transfer bytes per request, the same geometry as the public scratch |
| [`submit_secret_read`](#submit_secret_read) | the welded destination is borrowed until the completion is dequeued, and is written exactly then with exactly the delivered prefix; on any error or cancellation it is unchanged |
| [`submit_secret_write`](#submit_secret_write) | welded bytes are copied into the attached secret scratch before this call succeeds; the caller's storage is not borrowed past the return |
| [`shutdown_drain`](#shutdown_drain), [`shutdown_abort`](#shutdown_abort), [`active`](#active), [`dnit`](#dnit) | |

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
the adapter is initialized in place by make: the runtime source and the
worker pool hold its address until destroy

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
the borrow in destroy, and the caller releases it after that

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

### shutdown_abort

```mach
pub fun shutdown_abort(adapter: *Adapter) res[usize, std.io.error.Error]
```

### active

```mach
pub fun active(adapter: *Adapter) usize
```

### dnit

```mach
pub fun dnit(adapter: *Adapter) err[std.io.error.Error]
```

