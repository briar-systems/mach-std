[std](../README.md) / [io](README.md) / **lifecycle**

# std.io.lifecycle

shared resource close and drain state

Source: [`src/io/lifecycle.mach`](../../../src/io/lifecycle.mach)

Uses types from [`std.sync.mutex`](../sync/mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`StateError`](#stateerror) | `tag` | every way a state transition can be refused |
| [`State`](#state) | `def` |  |
| [`Mode`](#mode) | `def` |  |
| [`Cause`](#cause) | `def` |  |
| [`Lifecycle`](#lifecycle) | `rec` | the close and drain state of one shared resource |
| [`Attachment`](#attachment) | `rec` | one unit of outstanding work held against a lifecycle |
| [`Snapshot`](#snapshot-1) | `rec` | a consistent copy of a lifecycle's state |
| [`CloseResult`](#closeresult) | `rec` | what a close request did |

| On `State` | |
| :--- | :--- |
| [`OPEN`](#state), [`CLOSING`](#state), [`CLOSED`](#state) | |

| On `Mode` | |
| :--- | :--- |
| [`GRACEFUL`](#mode), [`ABORTIVE`](#mode) | |

| On `Cause` | |
| :--- | :--- |
| [`EXPLICIT`](#cause), [`PROCESS_TERMINATION`](#cause), [`DEADLINE`](#cause), [`CANCELLATION`](#cause), [`FAILURE`](#cause) | |

| On `Lifecycle` | |
| :--- | :--- |
| [`make`](#make) | initializes a lifecycle in place; the storage is address-bound from here on |
| [`attach`](#attach) | initializes an attachment in place against an open lifecycle; the attachment is address-bound until it settles |
| [`begin_close`](#begin_close) | starts or escalates a close |
| [`begin_process_drain`](#begin_process_drain) | starts a graceful close because the process is terminating |
| [`fail`](#fail) | starts or escalates to an abortive close because the resource failed |
| [`snapshot`](#snapshot) | reads a lifecycle's state under its lock |

| On `Attachment` | |
| :--- | :--- |
| [`settle`](#settle) | settles an attachment; true when this settlement completed the owner's close |
| [`settle_closed_child`](#settle_closed_child) | settles the parent's attachment for a child that has fully closed; a child still open or draining is busy and the attachment stays active |

---

## StateError

```mach
pub tag StateError: u8 {
    invalid;
    closed;
    exhausted;
    active;
    inactive;
    stale;
    busy;
}
```

every way a state transition can be refused

the domain error tag for state machines: lifecycles and their attachments
here, and the queued sinks, channels, pools and resolvers that later lanes
migrate. a case names the fact that refused the transition; the receiver is
left exactly as it was.

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil receiver or an argument outside the closed set |
| `closed` |  | the owner has left the open state and admits no new work |
| `exhausted` |  | a bounded counter or table is full |
| `active` |  | the object is already attached, registered or open |
| `inactive` |  | the object is not attached, registered or open |
| `stale` |  | the object belongs to an earlier generation of its owner |
| `busy` |  | outstanding work forbids the transition |

## State

```mach
pub def State: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `OPEN` | `0` |  |
| `CLOSING` | `1` |  |
| `CLOSED` | `2` |  |

## Mode

```mach
pub def Mode: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `GRACEFUL` | `0` |  |
| `ABORTIVE` | `1` |  |

## Cause

```mach
pub def Cause: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `EXPLICIT` | `0` |  |
| `PROCESS_TERMINATION` | `1` |  |
| `DEADLINE` | `2` |  |
| `CANCELLATION` | `3` |  |
| `FAILURE` | `4` |  |

## Lifecycle

```mach
pub rec Lifecycle {
    state:          State;
    mode:           Mode;
    cause:          Cause;
    terminal_cause: Cause;
    generation:     u32;
    submitted:      u64;
    settled:        u64;
    lock:           std.sync.mutex.Mutex;
}
```

the close and drain state of one shared resource

the storage is address-bound once make has run, since attachments point at it

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `State` | where the close stands |
| `mode` | `Mode` | how the close treats outstanding work |
| `cause` | `Cause` | why the close started |
| `terminal_cause` | `Cause` | why the close took its final mode, the start or the last escalation |
| `generation` | `u32` | bumped by each make, so attachments from an earlier one read as stale |
| `submitted` | `u64` | attachments taken in this generation |
| `settled` | `u64` | attachments settled in this generation |
| `lock` | `std.sync.mutex.Mutex` | guards every field above |

### make

```mach
pub fun make(lifecycle: *Lifecycle) err[StateError]
```

initializes a lifecycle in place; the storage is address-bound from here on

### attach

```mach
pub fun attach(lifecycle: *Lifecycle, attachment: *Attachment) err[StateError]
```

initializes an attachment in place against an open lifecycle; the attachment
is address-bound until it settles

### begin_close

```mach
pub fun begin_close(lifecycle: *Lifecycle, mode: Mode, cause: Cause) CloseResult
```

starts or escalates a close

an open lifecycle moves to CLOSING with the given mode and cause. a graceful
close asked to go abortive escalates and records the cause as terminal. any
other request changes nothing. the close completes at once when nothing is
outstanding

| Parameter | |
| :--- | :--- |
| `lifecycle` | the lifecycle to close |
| `mode` | GRACEFUL or ABORTIVE |
| `cause` | why the close is asked for |
| **returns** | what the request did. a nil lifecycle or a mode or cause outside its set yields started false and a CLOSED, ABORTIVE, FAILURE snapshot |

### begin_process_drain

```mach
pub fun begin_process_drain(lifecycle: *Lifecycle) CloseResult
```

starts a graceful close because the process is terminating

| Parameter | |
| :--- | :--- |
| `lifecycle` | the lifecycle to drain |
| **returns** | what the request did, as for begin_close |

### fail

```mach
pub fun fail(lifecycle: *Lifecycle) CloseResult
```

starts or escalates to an abortive close because the resource failed

| Parameter | |
| :--- | :--- |
| `lifecycle` | the lifecycle that failed |
| **returns** | what the request did, as for begin_close |

### snapshot

```mach
pub fun snapshot(lifecycle: *Lifecycle) Snapshot
```

reads a lifecycle's state under its lock

| Parameter | |
| :--- | :--- |
| `lifecycle` | the lifecycle to read |
| **returns** | its state, or a CLOSED, ABORTIVE, FAILURE snapshot when lifecycle is nil |

## Attachment

```mach
pub rec Attachment {
    owner:      *Lifecycle;
    generation: u32;
    sequence:   u64;
    active:     bool;
}
```

one unit of outstanding work held against a lifecycle

| Field | Type | |
| :--- | :--- | :--- |
| `owner` | `*Lifecycle` | the lifecycle it is attached to, nil once settled |
| `generation` | `u32` | the owner's generation when it attached |
| `sequence` | `u64` | the owner's submitted count when it attached |
| `active` | `bool` | true from attach until settle |

### settle

```mach
pub fun settle(attachment: *Attachment) res[bool, StateError]
```

settles an attachment; true when this settlement completed the owner's close

### settle_closed_child

```mach
pub fun settle_closed_child(attachment: *Attachment, child: *Lifecycle) res[bool, StateError]
```

settles the parent's attachment for a child that has fully closed; a child
still open or draining is busy and the attachment stays active

## Snapshot

```mach
pub rec Snapshot {
    state:          State;
    mode:           Mode;
    cause:          Cause;
    terminal_cause: Cause;
    outstanding:    usize;
}
```

a consistent copy of a lifecycle's state

| Field | Type | |
| :--- | :--- | :--- |
| `state` | `State` | where the close stands |
| `mode` | `Mode` | how the close treats outstanding work |
| `cause` | `Cause` | why the close started |
| `terminal_cause` | `Cause` | why the close took its final mode |
| `outstanding` | `usize` | attachments not yet settled |

## CloseResult

```mach
pub rec CloseResult {
    started:   bool;
    escalated: bool;
    complete:  bool;
    snapshot:  Snapshot;
}
```

what a close request did

| Field | Type | |
| :--- | :--- | :--- |
| `started` | `bool` | true when this request moved the lifecycle out of OPEN |
| `escalated` | `bool` | true when this request turned a graceful close abortive |
| `complete` | `bool` | true when the lifecycle is CLOSED after the request |
| `snapshot` | `Snapshot` | the state after the request |

