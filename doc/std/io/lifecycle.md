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
| [`Lifecycle`](#lifecycle) | `rec` |  |
| [`Attachment`](#attachment) | `rec` |  |
| [`Snapshot`](#snapshot-1) | `rec` |  |
| [`CloseResult`](#closeresult) | `rec` |  |

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
| [`begin_close`](#begin_close), [`begin_process_drain`](#begin_process_drain), [`fail`](#fail), [`snapshot`](#snapshot) | |

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

### begin_process_drain

```mach
pub fun begin_process_drain(lifecycle: *Lifecycle) CloseResult
```

### fail

```mach
pub fun fail(lifecycle: *Lifecycle) CloseResult
```

### snapshot

```mach
pub fun snapshot(lifecycle: *Lifecycle) Snapshot
```

## Attachment

```mach
pub rec Attachment {
    owner:      *Lifecycle;
    generation: u32;
    sequence:   u64;
    active:     bool;
}
```

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

## CloseResult

```mach
pub rec CloseResult {
    started:   bool;
    escalated: bool;
    complete:  bool;
    snapshot:  Snapshot;
}
```

