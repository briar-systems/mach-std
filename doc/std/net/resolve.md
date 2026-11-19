[std](../README.md) / [net](README.md) / **resolve**

# std.net.resolve

bounded asynchronous system name resolution

every lookup runs under a cancellation scope and keeps one contract on every
platform: when the scope ends, the lookup returns within shared.POLL_MSEC
(10 ms) with the scope's reason, and holds nothing of the caller's
afterwards. what the system is still doing for it is the backend's business
and never reaches the caller. linux asks its nameservers itself and bounds
every wait by the poll, the TCP retry's connect included. windows runs
GetAddrInfoExW asynchronously into a request the library owns and asks
GetAddrInfoExCancel to end it. darwin runs getaddrinfo, which nothing can
interrupt, on a helper thread that owns the request and frees it when the
system lets it finish. an operation here hands its backend a scope of its
own, which the caller's scope, a token cancellation, the runtime and the
deadline all end

Source: [`src/net/resolve.mach`](../../../src/net/resolve.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.chrono.time`](../chrono/time.md), [`std.io.runtime`](../io/runtime.md), [`std.net.resolve.types`](resolve/types.md), [`std.sync.cancel`](../sync/cancel.md), [`std.sync.condition`](../sync/condition.md), [`std.sync.mutex`](../sync/mutex.md), [`std.sync.worker_pool`](../sync/worker_pool.md).

| Type | | |
| :--- | :--- | :--- |
| [`Resolver`](#resolver) | `rec` | operation and completion storage is fixed after construction the worker pool and allocator must remain live and drain accepted tasks allocator callbacks must support concurrent calls from the pool's workers |

| On `Resolver` | |
| :--- | :--- |
| [`init_with_adapter`](#init_with_adapter) | initialize a resolver in place over caller-owned storage; a refused acquisition releases what was acquired and leaves the storage unowned |
| [`init`](#init), [`init_runtime_with_adapter`](#init_runtime_with_adapter), [`init_runtime`](#init_runtime), [`submit`](#submit), [`submit_runtime`](#submit_runtime) | |
| [`cancel`](#cancel) | cancel a live operation |
| [`poll`](#poll), [`wait`](#wait), [`wait_until`](#wait_until) | |
| [`close`](#close) | stop admitting submissions; CLOSED when the resolver is not open |
| [`dnit`](#dnit) | release the resolver's storage: INVALID with EINVAL before close, INVALID with EBUSY while operations, completions or waiters remain; a refused release reports the runtime's or the allocator's failure after every release has been attempted |

| Functions | |
| :--- | :--- |
| [`resolution_dnit`](#resolution_dnit) | release a dequeued completion's storage; a refused release keeps the storage owned so the caller can retry |

| Constants | |
| :--- | :--- |
| [`MAX_HOST_LENGTH`](#constants), [`MAX_SERVICE_LENGTH`](#constants), [`OPEN`](#constants), [`CLOSING`](#constants), [`DESTROYED`](#constants) | |

| Forwards | |
| :--- | :--- |
| [`Family`](#family), [`ANY_FAMILY`](#any_family), [`IPV4_ONLY`](#ipv4_only), [`IPV6_ONLY`](#ipv6_only), [`SocketKind`](#socketkind), [`ANY_SOCKET`](#any_socket), [`STREAM_SOCKET`](#stream_socket), [`DATAGRAM_SOCKET`](#datagram_socket), [`CANONICAL_NAME`](#canonical_name), [`NUMERIC_HOST`](#numeric_host), [`NUMERIC_SERVICE`](#numeric_service), [`PASSIVE`](#passive), [`ErrorKind`](#errorkind), [`NO_ERROR`](#no_error), [`INVALID`](#invalid), [`OVERLOADED`](#overloaded), [`CLOSED`](#closed), [`OUT_OF_MEMORY`](#out_of_memory), [`NO_NAME`](#no_name), [`TEMPORARY`](#temporary), [`MALFORMED`](#malformed), [`SYSTEM_FAILURE`](#system_failure), [`CANCELLED`](#cancelled), [`TIMED_OUT`](#timed_out), [`Error`](#error), [`Token`](#token), [`Query`](#query), [`ResultLimits`](#resultlimits), [`Resolution`](#resolution), [`Completion`](#completion), [`AdapterFun`](#adapterfun) | |

---

## Resolver

```mach
pub rec Resolver {
    pool:               *std.sync.worker_pool.Pool;
    allocator:          *std.allocator.Allocator;
    adapter:            std.net.resolve.types.AdapterFun;
    adapter_context:    ptr;
    result_limits:      std.net.resolve.types.ResultLimits;
    runtime:            *std.io.runtime.Runtime;
    runtime_source:     std.io.runtime.SourceToken;
    runtime_registered: bool;
    operations:         *Operation;
    completions:        *std.net.resolve.types.Completion;
    capacity:           usize;
    free_head:          u32;
    free_tail:          u32;
    # runtime-owned operations queued and not yet published, oldest first
    queued_head: u32;
    queued_tail: u32;
    # open addressed on the runtime token index, holding operation index + 1
    routes:         *u32;
    route_capacity: usize;
    head:           usize;
    tail:           usize;
    count:          usize;
    live:           usize;
    state:          u8;
    lock:           std.sync.mutex.Mutex;
    ready:          std.sync.condition.Condition;
}
```

operation and completion storage is fixed after construction
the worker pool and allocator must remain live and drain accepted tasks
allocator callbacks must support concurrent calls from the pool's workers

### init_with_adapter

```mach
pub fun init_with_adapter(resolver: *Resolver, pool: *std.sync.worker_pool.Pool, owner: *std.allocator.Allocator,
    capacity: usize, result_limits: std.net.resolve.types.ResultLimits, adapter_context: ptr, adapter: std.net.resolve.types.AdapterFun) err[std.net.resolve.types.Error]
```

initialize a resolver in place over caller-owned storage; a refused
acquisition releases what was acquired and leaves the storage unowned

### init

```mach
pub fun init(resolver: *Resolver, pool: *std.sync.worker_pool.Pool, owner: *std.allocator.Allocator,
    capacity: usize, result_limits: std.net.resolve.types.ResultLimits) err[std.net.resolve.types.Error]
```

### init_runtime_with_adapter

```mach
pub fun init_runtime_with_adapter(resolver: *Resolver, runtime: *std.io.runtime.Runtime,
    pool: *std.sync.worker_pool.Pool, owner: *std.allocator.Allocator, capacity: usize,
    result_limits: std.net.resolve.types.ResultLimits, adapter_context: ptr, adapter: std.net.resolve.types.AdapterFun) err[std.net.resolve.types.Error]
```

### init_runtime

```mach
pub fun init_runtime(resolver: *Resolver, runtime: *std.io.runtime.Runtime,
    pool: *std.sync.worker_pool.Pool, owner: *std.allocator.Allocator, capacity: usize,
    result_limits: std.net.resolve.types.ResultLimits) err[std.net.resolve.types.Error]
```

### submit

```mach
pub fun submit(resolver: *Resolver, scope: *std.sync.cancel.Scope, query: *std.net.resolve.types.Query, context: usize) res[std.net.resolve.types.Token, std.net.resolve.types.Error]
```

### submit_runtime

```mach
pub fun submit_runtime(resolver: *Resolver, scope: *std.sync.cancel.Scope,
    query: *std.net.resolve.types.Query, context: usize) res[std.io.runtime.Token, std.net.resolve.types.Error]
```

### cancel

```mach
pub fun cancel(resolver: *Resolver, token: std.net.resolve.types.Token) res[bool, StateError]
```

cancel a live operation

| Parameter | |
| :--- | :--- |
| **returns** | whether this call changed the operation's reason (false when a deadline or an earlier cancellation already ended it); `invalid` for a nil resolver or an out-of-range token, `stale` for a token whose slot has been reused or released, `busy` for a runtime-owned operation, which the runtime's own cancellation reaches |

### poll

```mach
pub fun poll(resolver: *Resolver, output: *std.net.resolve.types.Completion, capacity: usize) usize
```

### wait

```mach
pub fun wait(resolver: *Resolver, output: *std.net.resolve.types.Completion, capacity: usize) usize
```

### wait_until

```mach
pub fun wait_until(resolver: *Resolver, output: *std.net.resolve.types.Completion, capacity: usize, deadline: std.chrono.time.Instant) usize
```

### close

```mach
pub fun close(resolver: *Resolver) err[std.net.resolve.types.Error]
```

stop admitting submissions; CLOSED when the resolver is not open

### dnit

```mach
pub fun dnit(resolver: *Resolver) err[std.net.resolve.types.Error]
```

release the resolver's storage: INVALID with EINVAL before close, INVALID
with EBUSY while operations, completions or waiters remain; a refused
release reports the runtime's or the allocator's failure after every
release has been attempted

## Functions

### resolution_dnit

```mach
pub fun resolution_dnit(resolution: *std.net.resolve.types.Resolution) err[std.net.resolve.types.Error]
```

release a dequeued completion's storage; a refused release keeps the
storage owned so the caller can retry

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_HOST_LENGTH` | `usize` | `253` |  |
| `MAX_SERVICE_LENGTH` | `usize` | `31` |  |
| `OPEN` | `u8` | `0` |  |
| `CLOSING` | `u8` | `1` |  |
| `DESTROYED` | `u8` | `2` |  |

## Forwards

### Family

Forwards [`std.net.resolve.types.Family`](resolve/types.md#family), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub def Family: u8
```

### ANY_FAMILY

Forwards [`std.net.resolve.types.ANY_FAMILY`](resolve/types.md#family), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val ANY_FAMILY: Family = 0
```

### IPV4_ONLY

Forwards [`std.net.resolve.types.IPV4_ONLY`](resolve/types.md#family), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val IPV4_ONLY:  Family = 1
```

### IPV6_ONLY

Forwards [`std.net.resolve.types.IPV6_ONLY`](resolve/types.md#family), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val IPV6_ONLY:  Family = 2
```

### SocketKind

Forwards [`std.net.resolve.types.SocketKind`](resolve/types.md#socketkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub def SocketKind: u8
```

### ANY_SOCKET

Forwards [`std.net.resolve.types.ANY_SOCKET`](resolve/types.md#socketkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val ANY_SOCKET:      SocketKind = 0
```

### STREAM_SOCKET

Forwards [`std.net.resolve.types.STREAM_SOCKET`](resolve/types.md#socketkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val STREAM_SOCKET:   SocketKind = 1
```

### DATAGRAM_SOCKET

Forwards [`std.net.resolve.types.DATAGRAM_SOCKET`](resolve/types.md#socketkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val DATAGRAM_SOCKET: SocketKind = 2
```

### CANONICAL_NAME

Forwards [`std.net.resolve.types.CANONICAL_NAME`](resolve/types.md#constants), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val CANONICAL_NAME:  u32 = 1
```

### NUMERIC_HOST

Forwards [`std.net.resolve.types.NUMERIC_HOST`](resolve/types.md#constants), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val NUMERIC_HOST:    u32 = 2
```

### NUMERIC_SERVICE

Forwards [`std.net.resolve.types.NUMERIC_SERVICE`](resolve/types.md#constants), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val NUMERIC_SERVICE: u32 = 4
```

### PASSIVE

Forwards [`std.net.resolve.types.PASSIVE`](resolve/types.md#constants), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val PASSIVE:         u32 = 8
```

### ErrorKind

Forwards [`std.net.resolve.types.ErrorKind`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub def ErrorKind: u8
```

### NO_ERROR

Forwards [`std.net.resolve.types.NO_ERROR`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val NO_ERROR:       ErrorKind = 0
```

### INVALID

Forwards [`std.net.resolve.types.INVALID`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val INVALID:        ErrorKind = 1
```

### OVERLOADED

Forwards [`std.net.resolve.types.OVERLOADED`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val OVERLOADED:     ErrorKind = 2
```

### CLOSED

Forwards [`std.net.resolve.types.CLOSED`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val CLOSED:         ErrorKind = 3
```

### OUT_OF_MEMORY

Forwards [`std.net.resolve.types.OUT_OF_MEMORY`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val OUT_OF_MEMORY:  ErrorKind = 4
```

### NO_NAME

Forwards [`std.net.resolve.types.NO_NAME`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val NO_NAME:        ErrorKind = 5
```

### TEMPORARY

Forwards [`std.net.resolve.types.TEMPORARY`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val TEMPORARY:      ErrorKind = 6
```

### MALFORMED

Forwards [`std.net.resolve.types.MALFORMED`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val MALFORMED:      ErrorKind = 7
```

### SYSTEM_FAILURE

Forwards [`std.net.resolve.types.SYSTEM_FAILURE`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val SYSTEM_FAILURE: ErrorKind = 8
```

### CANCELLED

Forwards [`std.net.resolve.types.CANCELLED`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val CANCELLED:      ErrorKind = 9
```

### TIMED_OUT

Forwards [`std.net.resolve.types.TIMED_OUT`](resolve/types.md#errorkind), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub val TIMED_OUT:      ErrorKind = 10
```

### Error

Forwards [`std.net.resolve.types.Error`](resolve/types.md#error), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec Error {
    kind:        ErrorKind;
    native_code: i64;
}
```

### Token

Forwards [`std.net.resolve.types.Token`](resolve/types.md#token), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec Token {
    index:      u32;
    generation: u32;
}
```

### Query

Forwards [`std.net.resolve.types.Query`](resolve/types.md#query), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec Query {
    host:        str;
    service:     str;
    family:      Family;
    socket_kind: SocketKind;
    protocol:    i32;
    flags:       u32;
}
```

### ResultLimits

Forwards [`std.net.resolve.types.ResultLimits`](resolve/types.md#resultlimits), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec ResultLimits {
    max_endpoints:            usize;
    max_canonical_name_bytes: usize;
}
```

### Resolution

Forwards [`std.net.resolve.types.Resolution`](resolve/types.md#resolution), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec Resolution {
    endpoints:          *std.net.ip.Endpoint;
    len:                usize;
    endpoint_capacity:  usize;
    canonical_name:     *u8;
    canonical_length:   usize;
    canonical_capacity: usize;
    allocator:          *std.allocator.Allocator;
}
```

result storage belongs to the caller after completion is dequeued

### Completion

Forwards [`std.net.resolve.types.Completion`](resolve/types.md#completion), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub rec Completion {
    token:      Token;
    context:    usize;
    resolution: Resolution;
    has_error:  bool;
    error:      Error;
}
```

### AdapterFun

Forwards [`std.net.resolve.types.AdapterFun`](resolve/types.md#adapterfun), only where `capability.HAS_CLOCK && capability.HAS_THREADS`.

```mach
pub def AdapterFun: fun(ptr, *std.sync.cancel.Scope, *Query, *std.allocator.Allocator, ResultLimits, *Resolution) Error
```

a resolver backend: context, the scope that bounds and cancels the lookup,
the query, the result's allocator, its limits and the result to fill. when
the scope ends, a backend returns within shared.POLL_MSEC with the scope's
reason (shared.ended) and holds nothing of the caller's afterwards: whatever
the system still does for the lookup is the backend's to own and free

