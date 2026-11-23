[std](../README.md) / [sync](README.md) / **channel**

# std.sync.channel

bounded caller-owned multi-producer multi-consumer channel

Source: [`src/sync/channel.mach`](../../../src/sync/channel.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.sync.cancel`](cancel.md), [`std.sync.condition`](condition.md), [`std.sync.mutex`](mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Status`](#status) | `tag` | the outcome of a transfer |
| [`StateError`](#stateerror) | `tag` | a refused channel state operation |
| [`Operation`](#operation) | `def` |  |
| [`Transition`](#transition) | `def` |  |
| [`Channel`](#channel) | `rec` | a bounded fifo ring of T over caller storage, guarded by one lock |

| On `Channel` | |
| :--- | :--- |
| [`make`](#make) | channels are unfair, unpoisoned, and own no storage or target handles storage and the channel address remain stable until close and waiter exit |
| [`try_send`](#try_send) | the caller retains value unless the send succeeds |
| [`send`](#send) | blocking send sleeps until one slot is owned or the channel closes |
| [`send_until`](#send_until) | deadlines are absolute monotonic instants and never fire early |
| [`send_scoped`](#send_scoped) | cancellation owns the registration until unregister or completion returns |
| [`try_receive`](#try_receive) | the value is carried on the received case only |
| [`receive`](#receive) | close drains accepted values before receivers observe closure |
| [`receive_until`](#receive_until) | receive, sleeping no later than an absolute monotonic deadline |
| [`receive_scoped`](#receive_scoped) | receive, sleeping until a value arrives or the scope is cancelled or times out |
| [`close`](#close) | close is idempotent and wakes every blocked sender and receiver |
| [`close_abort`](#close_abort) | abort transfers every queued value to output in fifo order |
| [`count`](#count) | count the queued values |
| [`is_closed`](#is_closed) | report whether the channel is closed |
| [`dnit`](#dnit) | destruction succeeds only after close, drain, and all waiter exit |

---

## Status

```mach
pub tag Status[T]: u8 { invalid; sent; received: T; full; empty; closed; timed_out; cancelled; aborted; }
```

the outcome of a transfer

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil or destroyed channel, a nil scope, a deadline outside the target range, or a refused native wait |
| `sent` |  | the value is owned by the channel |
| `received` | `T` | the value taken from the channel |
| `full` |  | no slot was available (try_send) |
| `empty` |  | no value was queued (try_receive) |
| `closed` |  | the channel is closed (and drained, for receivers) |
| `timed_out` |  | the absolute deadline passed first |
| `cancelled` |  | the scope was cancelled first |
| `aborted` |  | close_abort transferred every queued value |

## StateError

```mach
pub tag StateError: u8 { invalid; destroyed; open; busy; }
```

a refused channel state operation

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil channel, nil storage, zero capacity, or a channel that was never made |
| `destroyed` |  | the channel has already been destroyed |
| `open` |  | destruction refused while the channel is still open |
| `busy` |  | destruction refused while values, waiters or in-flight callers remain |

## Operation

```mach
pub def Operation:  err[StateError]
```

## Transition

```mach
pub def Transition: res[bool, StateError]
```

## Channel

```mach
pub rec Channel[T] {
    storage:     *T;
    capacity:    usize;
    head:        usize;
    len:         usize;
    open:        bool;
    initialized: bool;
    gate:        i64;
    lock:        std.sync.mutex.Mutex;
    readable:    std.sync.condition.Condition;
    writable:    std.sync.condition.Condition;
}
```

a bounded fifo ring of T over caller storage, guarded by one lock

prepare it with make and release it with dnit. the fields are internal.

| Field | Type | |
| :--- | :--- | :--- |
| `storage` | `*T` | caller-owned ring of capacity slots |
| `capacity` | `usize` | number of slots in storage |
| `head` | `usize` | index of the oldest queued value |
| `len` | `usize` | number of queued values |
| `open` | `bool` | false once close or close_abort ran |
| `initialized` | `bool` | true between make and dnit |
| `gate` | `i64` | in-flight callers, or GATE_CLOSED once destroyed |
| `lock` | `std.sync.mutex.Mutex` | guards every field above except gate |
| `readable` | `std.sync.condition.Condition` | signalled when a value is queued or the channel closes |
| `writable` | `std.sync.condition.Condition` | signalled when a slot frees or the channel closes |

### make

```mach
pub fun make[T](channel: *Channel[T], storage: *T, capacity: usize) Operation
```

channels are unfair, unpoisoned, and own no storage or target handles
storage and the channel address remain stable until close and waiter exit

| Parameter | |
| :--- | :--- |
| `channel` | storage to make into an open, empty channel |
| `storage` | caller-owned array of capacity slots, borrowed until dnit |
| `capacity` | number of slots, at least 1 |
| **returns** | ok, or invalid for a nil channel, nil storage or zero capacity |

### try_send

```mach
pub fun try_send[T](channel: *Channel[T], value: T) Status[T]
```

the caller retains value unless the send succeeds

| Parameter | |
| :--- | :--- |
| `channel` | channel to send on |
| `value` | value to queue |
| **returns** | sent, full when no slot is free, closed, or invalid for a nil or destroyed channel |

### send

```mach
pub fun send[T](channel: *Channel[T], value: T) Status[T]
```

blocking send sleeps until one slot is owned or the channel closes

| Parameter | |
| :--- | :--- |
| `channel` | channel to send on |
| `value` | value to queue |
| **returns** | sent, closed, or invalid for a nil or destroyed channel |

### send_until

```mach
pub fun send_until[T](channel: *Channel[T], value: T, deadline: std.chrono.time.Instant) Status[T]
```

deadlines are absolute monotonic instants and never fire early

| Parameter | |
| :--- | :--- |
| `channel` | channel to send on |
| `value` | value to queue |
| `deadline` | absolute monotonic instant to give up at |
| **returns** | sent, closed, timed_out, or invalid for a nil or destroyed channel, a malformed deadline or a refused native wait |

### send_scoped

```mach
pub fun send_scoped[T](channel: *Channel[T], scope: *std.sync.cancel.Scope, value: T) Status[T]
```

cancellation owns the registration until unregister or completion returns

| Parameter | |
| :--- | :--- |
| `channel` | channel to send on |
| `scope` | cancellation scope that ends the wait, its deadline included |
| `value` | value to queue |
| **returns** | sent, closed, cancelled, timed_out, or invalid for a nil or destroyed scope, a nil or destroyed channel or a refused native wait |

### try_receive

```mach
pub fun try_receive[T](channel: *Channel[T]) Status[T]
```

the value is carried on the received case only

| Parameter | |
| :--- | :--- |
| `channel` | channel to receive from |
| **returns** | received with the oldest value, empty, closed once closed and drained, or invalid for a nil or destroyed channel |

### receive

```mach
pub fun receive[T](channel: *Channel[T]) Status[T]
```

close drains accepted values before receivers observe closure

| Parameter | |
| :--- | :--- |
| `channel` | channel to receive from |
| **returns** | received with the oldest value, closed once closed and drained, or invalid for a nil or destroyed channel |

### receive_until

```mach
pub fun receive_until[T](channel: *Channel[T], deadline: std.chrono.time.Instant) Status[T]
```

receive, sleeping no later than an absolute monotonic deadline

a value already queued is taken even when the deadline has passed

| Parameter | |
| :--- | :--- |
| `channel` | channel to receive from |
| `deadline` | absolute monotonic instant to give up at |
| **returns** | received, closed once closed and drained, timed_out, or invalid for a nil or destroyed channel, a malformed deadline or a refused native wait |

### receive_scoped

```mach
pub fun receive_scoped[T](channel: *Channel[T], scope: *std.sync.cancel.Scope) Status[T]
```

receive, sleeping until a value arrives or the scope is cancelled or times out

| Parameter | |
| :--- | :--- |
| `channel` | channel to receive from |
| `scope` | cancellation scope that ends the wait, its deadline included |
| **returns** | received, closed once closed and drained, cancelled, timed_out, or invalid for a nil or destroyed scope, a nil or destroyed channel or a refused native wait |

### close

```mach
pub fun close[T](channel: *Channel[T]) Transition
```

close is idempotent and wakes every blocked sender and receiver

| Parameter | |
| :--- | :--- |
| `channel` | channel to close |
| **returns** | true when this call closed the channel, false when it already was |

### close_abort

```mach
pub fun close_abort[T](channel: *Channel[T], output: *T, output_capacity: usize, output_len: *usize) Status[T]
```

abort transfers every queued value to output in fifo order

the channel is closed and left empty, and every blocked caller is woken

| Parameter | |
| :--- | :--- |
| `channel` | channel to abort |
| `output` | caller array that receives the queued values, may be nil when none are queued |
| `output_capacity` | number of slots in output |
| `output_len` | receives the number of values written |
| **returns** | aborted, or invalid for a nil output_len, a nil or destroyed channel, or output too small for the queued values, with the channel untouched |

### count

```mach
pub fun count[T](channel: *Channel[T]) usize
```

count the queued values

| Parameter | |
| :--- | :--- |
| `channel` | channel to read |
| **returns** | queued value count, 0 for a nil or destroyed channel |

### is_closed

```mach
pub fun is_closed[T](channel: *Channel[T]) bool
```

report whether the channel is closed

| Parameter | |
| :--- | :--- |
| `channel` | channel to read |
| **returns** | true once closed, and for a nil or destroyed channel |

### dnit

```mach
pub fun dnit[T](channel: *Channel[T]) Operation
```

destruction succeeds only after close, drain, and all waiter exit

| Parameter | |
| :--- | :--- |
| **returns** | ok once destroyed, invalid for a nil, never-made or already destroyed channel, open while the channel is open, busy while values, waiters or in-flight callers remain |

