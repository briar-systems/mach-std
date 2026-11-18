[std](../../README.md) / [net](../README.md) / [async](README.md) / **iocp**

# std.net.async.iocp

per-socket bookkeeping shared by the windows completion port backends
backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface)

the core decides what each state change on a socket makes due and makes no
native call itself, so a backend performs whatever a decision asks for and
every decision costs the same whatever else the backend holds. a backend
embeds one Link in each operation and hands the core the operation table and
the link's offset, so the core never owns or moves an operation

Source: [`src/net/async/iocp.mach`](../../../../src/net/async/iocp.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.io.runtime`](../../io/runtime.md), [`std.memory.table`](../../memory/table.md).

| Type | | |
| :--- | :--- | :--- |
| [`Link`](#link) | `rec` | the core's part of an operation, embedded in the backend's operation record |
| [`Socket`](#socket) | `rec` | one native socket under one opening |
| [`Core`](#core) | `rec` |  |

| On `Core` | |
| :--- | :--- |
| [`link`](#link-1), [`socket_at`](#socket_at) | |
| [`init`](#init) | the socket table starts at initial records and grows on demand |
| [`dnit`](#dnit), [`aliases`](#aliases) | |
| [`lookup`](#lookup) | the mapped record for a socket value, or NONE |
| [`trim`](#trim) | give back the socket records a peak grew: a chunk goes once it and the chunk below it hold no record in use, and the map is rehashed to the smaller table |
| [`acquire`](#acquire) | the record a submit for socket under opening joins |
| [`abort`](#abort) | an operation on a socket that is going away settles with status: an active request once its aborted packet arrives, a held request at once, and a pending control too when controls is set |
| [`unmap`](#unmap) | a submit no longer finds the record, so a reused socket value attaches fresh |
| [`transition`](#transition) | every state change goes through here, so the lane lists and the socket's in flight counts always agree with the states |
| [`must_defer`](#must_defer) | whether a read-lane request submitted now must wait behind the socket's earlier ones: a readiness wait and the reads around it settle in submission order, since a zero-byte receive posted beside a read could find the read's bytes already taken and report a false end of stream |
| [`join`](#join) | a free operation joins the socket record in state |
| [`release`](#release) | the operation leaves its socket and becomes free |
| [`take_deferred`](#take_deferred) | the oldest held read-lane request, now active, once nothing in flight holds it back |
| [`progress`](#progress) | settle what the socket's control is now waiting on |

| Constants | |
| :--- | :--- |
| [`NONE`](#constants), [`FREE`](#constants), [`ACTIVE`](#constants) | |
| [`CANCELLED`](#constants) | a driver cancel that waits for the operation's packet itself |
| [`CANCEL_READY`](#constants) | settled with its result once its aborted packet arrives |
| [`CONTROL_PENDING`](#constants) | a control waiting for its socket to allow it |
| [`CONTROL_READY`](#constants) | settled with its result without a packet |
| [`DEFERRED`](#constants) | a read-lane request held back so it posts in submission order |
| [`ACQUIRED`](#constants), [`CREATED`](#constants) | |
| [`STALE`](#constants) | the handle's socket was closed and its value reused by a newer opening |
| [`EXHAUSTED`](#constants) | |

---

## Link

```mach
pub rec Link {
    state:     u8;
    kind:      std.io.runtime.Kind;
    socket:    u32;
    sock_prev: u32;
    sock_next: u32;
    lane_prev: u32;
    lane_next: u32;
    result:    i64;
}
```

the core's part of an operation, embedded in the backend's operation record

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `u8` | one of the slot states above, changed only through the core |
| `kind` | `std.io.runtime.Kind` | the runtime kind the operation was joined with |
| `socket` | `u32` | index of the socket record the operation belongs to |
| `sock_prev` | `u32` | previous operation on the same socket |
| `sock_next` | `u32` | next operation on the same socket |
| `lane_prev` | `u32` | previous operation on the one lane list the state implies |
| `lane_next` | `u32` | next operation on that lane list |
| `result` | `i64` | the status a ready or cancel-ready operation settles with |

## Socket

```mach
pub rec Socket {
    socket:            usize;
    opening:           u64;
    ops_head:          u32;
    ops_tail:          u32;
    op_count:          usize;
    inflight_reads:    usize;
    inflight_readable: usize;
    inflight_writes:   usize;
    deferred_head:     u32;
    deferred_tail:     u32;
    control:           u32;
    mapped:            bool;
    associated:        bool;
    retired:           bool;
    live:              bool;
    index:             u32;
    next_free:         usize;
}
```

one native socket under one opening

| Field | Type | |
| :--- | :--- | :--- |
| `socket` | `usize` | the native socket value |
| `opening` | `u64` | the opening of the handle the record was acquired for |
| `ops_head` | `u32` | first operation on the socket |
| `ops_tail` | `u32` | last operation on the socket |
| `op_count` | `usize` | operations on the socket, the control included |
| `inflight_reads` | `usize` | read-lane operations whose native request is outstanding |
| `inflight_readable` | `usize` | the readiness waits among them |
| `inflight_writes` | `usize` | write-lane operations on the socket, in any state |
| `deferred_head` | `u32` | oldest held read-lane operation |
| `deferred_tail` | `u32` | newest held read-lane operation |
| `control` | `u32` | the socket's one shutdown or close, or NONE |
| `mapped` | `bool` | whether a submit for the socket value finds this record |
| `associated` | `bool` | whether the socket is associated with the completion port |
| `retired` | `bool` | whether the socket was detached under its opening, so a handle still carrying that opening is stale |
| `live` | `bool` | whether the record is in use |

## Core

```mach
pub rec Core {
    allocator:    std.allocator.Allocator;
    link_offset:  usize;
    sockets:      std.memory.table.Table;
    socket_pool:  std.memory.table.Pool;
    socket_map:   *u32;
    map_capacity: usize;
    mapped_count: usize;
    live_count:   usize;
    ready_head:   u32;
    ready_tail:   u32;
    pending_head: u32;
    pending_tail: u32;
}
```

| Field | Type | |
| :--- | :--- | :--- |
| `allocator` | `std.allocator.Allocator` | where the socket table and map come from |
| `link_offset` | `usize` | offset of the Link inside the backend's operation record |
| `socket_pool` | `std.memory.table.Pool` | free records, lowest chunk first. a record is referenced only by the operations on it and by the map while mapped, never by a token, so it carries no generation |
| `socket_map` | `*u32` | open-addressed map from socket value to record index plus one |
| `mapped_count` | `usize` | records a submit can find |
| `live_count` | `usize` | records in use, mapped or still draining |
| `ready_head` | `u32` | oldest operation in the control-ready state |
| `pending_head` | `u32` | an operation in the control-pending state |

### link

```mach
pub fun link(core: *Core, ops: *std.memory.table.Table, index: u32) *Link
```

### socket_at

```mach
pub fun socket_at(core: *Core, index: u32) *Socket
```

### init

```mach
pub fun init(core: *Core, a: *std.allocator.Allocator, link_offset: usize, initial: usize) bool
```

the socket table starts at initial records and grows on demand

### dnit

```mach
pub fun dnit(core: *Core)
```

### aliases

```mach
pub fun aliases(core: *Core, data: *u8, len: usize) bool
```

### lookup

```mach
pub fun lookup(core: *Core, socket: usize) u32
```

the mapped record for a socket value, or NONE

### trim

```mach
pub fun trim(core: *Core)
```

give back the socket records a peak grew: a chunk goes once it and the chunk
below it hold no record in use, and the map is rehashed to the smaller table.
only free records are released, so no operation's socket moves

### acquire

```mach
pub fun acquire(core: *Core, ops: *std.memory.table.Table, socket: usize, opening: u64, index: *u32) u8
```

the record a submit for socket under opening joins. an older opening is a
handle whose socket was closed outside the driver and reused, and a retired
record's own opening is a handle whose socket was detached, here or on any
other driver; a newer one drops the stale record, whose operations settle in
the background

| Parameter | |
| :--- | :--- |
| `index` | receives the record on ACQUIRED or CREATED |
| **returns** | ACQUIRED, CREATED, STALE or EXHAUSTED |

### abort

```mach
pub fun abort(core: *Core, ops: *std.memory.table.Table, index: u32, controls: bool, status: i64) bool
```

an operation on a socket that is going away settles with status: an active
request once its aborted packet arrives, a held request at once, and a
pending control too when controls is set

| Parameter | |
| :--- | :--- |
| **returns** | whether the request was active, so the caller must abort it natively |

### unmap

```mach
pub fun unmap(core: *Core, index: u32)
```

a submit no longer finds the record, so a reused socket value attaches fresh.
the record is recycled once its last operation leaves

### transition

```mach
pub fun transition(core: *Core, ops: *std.memory.table.Table, index: u32, state: u8, result: i64)
```

every state change goes through here, so the lane lists and the socket's in
flight counts always agree with the states

### must_defer

```mach
pub fun must_defer(core: *Core, sock: u32, kind: std.io.runtime.Kind) bool
```

whether a read-lane request submitted now must wait behind the socket's
earlier ones: a readiness wait and the reads around it settle in submission
order, since a zero-byte receive posted beside a read could find the read's
bytes already taken and report a false end of stream. other reads post at once

### join

```mach
pub fun join(core: *Core, ops: *std.memory.table.Table, sock: u32, index: u32, kind: std.io.runtime.Kind, state: u8)
```

a free operation joins the socket record in state

### release

```mach
pub fun release(core: *Core, ops: *std.memory.table.Table, index: u32) u32
```

the operation leaves its socket and becomes free

| Parameter | |
| :--- | :--- |
| **returns** | the socket record, or NONE once the record was recycled |

### take_deferred

```mach
pub fun take_deferred(core: *Core, ops: *std.memory.table.Table, sock: u32) u32
```

the oldest held read-lane request, now active, once nothing in flight holds
it back. the caller posts it

| Parameter | |
| :--- | :--- |
| **returns** | the operation to post, or NONE |

### progress

```mach
pub fun progress(core: *Core, ops: *std.memory.table.Table, sock: u32) u32
```

settle what the socket's control is now waiting on. a close becomes ready
once it is the socket's last operation. a shutdown is due once no write is
left, and the caller shuts the socket down and moves it to ready

| Parameter | |
| :--- | :--- |
| **returns** | a shutdown that is due, or NONE |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `NONE` | `u32` | `0xffffffff` |  |
| `FREE` | `u8` | `0` |  |
| `ACTIVE` | `u8` | `1` |  |
| `CANCELLED` | `u8` | `2` | a driver cancel that waits for the operation's packet itself |
| `CANCEL_READY` | `u8` | `3` | settled with its result once its aborted packet arrives |
| `CONTROL_PENDING` | `u8` | `4` | a control waiting for its socket to allow it |
| `CONTROL_READY` | `u8` | `5` | settled with its result without a packet |
| `DEFERRED` | `u8` | `6` | a read-lane request held back so it posts in submission order |
| `ACQUIRED` | `u8` | `0` |  |
| `CREATED` | `u8` | `1` |  |
| `STALE` | `u8` | `2` | the handle's socket was closed and its value reused by a newer opening |
| `EXHAUSTED` | `u8` | `3` |  |

