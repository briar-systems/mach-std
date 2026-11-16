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
| [`Channel`](#channel) | `rec` |  |

| On `Channel` | |
| :--- | :--- |
| [`make`](#make) | channels are unfair, unpoisoned, and own no storage or target handles storage and the channel address remain stable until close and waiter exit |
| [`try_send`](#try_send) | the caller retains value unless the send succeeds |
| [`send`](#send) | blocking send sleeps until one slot is owned or the channel closes |
| [`send_until`](#send_until) | deadlines are absolute monotonic instants and never fire early |
| [`send_scoped`](#send_scoped) | cancellation owns the registration until unregister or completion returns |
| [`try_receive`](#try_receive) | the value is carried on the received case only |
| [`receive`](#receive) | close drains accepted values before receivers observe closure |
| [`receive_until`](#receive_until), [`receive_scoped`](#receive_scoped) | |
| [`close`](#close) | close is idempotent and wakes every blocked sender and receiver |
| [`close_abort`](#close_abort) | abort transfers every queued value to output in fifo order |
| [`count`](#count), [`is_closed`](#is_closed) | |
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

### make

```mach
pub fun make[T](channel: *Channel[T], storage: *T, capacity: usize) Operation
```

channels are unfair, unpoisoned, and own no storage or target handles
storage and the channel address remain stable until close and waiter exit

### try_send

```mach
pub fun try_send[T](channel: *Channel[T], value: T) Status[T]
```

the caller retains value unless the send succeeds

### send

```mach
pub fun send[T](channel: *Channel[T], value: T) Status[T]
```

blocking send sleeps until one slot is owned or the channel closes

### send_until

```mach
pub fun send_until[T](channel: *Channel[T], value: T, deadline: std.chrono.time.Instant) Status[T]
```

deadlines are absolute monotonic instants and never fire early

### send_scoped

```mach
pub fun send_scoped[T](channel: *Channel[T], scope: *std.sync.cancel.Scope, value: T) Status[T]
```

cancellation owns the registration until unregister or completion returns

### try_receive

```mach
pub fun try_receive[T](channel: *Channel[T]) Status[T]
```

the value is carried on the received case only

### receive

```mach
pub fun receive[T](channel: *Channel[T]) Status[T]
```

close drains accepted values before receivers observe closure

### receive_until

```mach
pub fun receive_until[T](channel: *Channel[T], deadline: std.chrono.time.Instant) Status[T]
```

### receive_scoped

```mach
pub fun receive_scoped[T](channel: *Channel[T], scope: *std.sync.cancel.Scope) Status[T]
```

### close

```mach
pub fun close[T](channel: *Channel[T]) Transition
```

close is idempotent and wakes every blocked sender and receiver

| Parameter | |
| :--- | :--- |
| **returns** | true when this call closed the channel, false when it already was |

### close_abort

```mach
pub fun close_abort[T](channel: *Channel[T], output: *T, output_capacity: usize, output_len: *usize) Status[T]
```

abort transfers every queued value to output in fifo order

### count

```mach
pub fun count[T](channel: *Channel[T]) usize
```

### is_closed

```mach
pub fun is_closed[T](channel: *Channel[T]) bool
```

### dnit

```mach
pub fun dnit[T](channel: *Channel[T]) Operation
```

destruction succeeds only after close, drain, and all waiter exit

| Parameter | |
| :--- | :--- |
| **returns** | ok once destroyed, invalid for a nil or never-made channel, destroyed when it already was, open while the channel is open, busy while values, waiters or in-flight callers remain |

