[std](../README.md) / [process](README.md) / **events**

# std.process.events

portable process lifecycle events

Source: [`src/process/events.mach`](../../../src/process/events.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.io.lifecycle`](../io/lifecycle.md), [`std.io.runtime`](../io/runtime.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Kind`](#kind) | `def` |  |
| [`Event`](#event) | `rec` | one lifecycle event, as next drains it |
| [`Capabilities`](#capabilities) | `rec` | which kinds of event the target can deliver |
| [`Source`](#source) | `rec` | the process's one event source, filled by make or make_runtime |

| On `Kind` | |
| :--- | :--- |
| [`SERVICE_STOP`](#kind), [`CONSOLE_CLOSE`](#kind), [`TERMINATE`](#kind), [`INTERRUPT`](#kind), [`RELOAD`](#kind) | |

| On `Capabilities` | |
| :--- | :--- |
| [`capabilities`](#capabilities-1) | which kinds of event this target delivers |

| On `Source` | |
| :--- | :--- |
| [`make`](#make) | claim the process's event source with its own wait queue |
| [`make_runtime`](#make_runtime) | the source must close before the runtime whose queue it borrows |
| [`notify_service_stop`](#notify_service_stop) | windows service handlers call this for stop, shutdown, or preshutdown control |
| [`next`](#next) | events are coalesced by kind and drained in service-to-reload priority order |
| [`begin_runtime_drain`](#begin_runtime_drain) | begin the graceful close of a runtime in answer to a termination event |
| [`wait`](#wait) | standalone sources may wait directly, runtime-attached sources use runtime wait |
| [`queue`](#queue) | the wait queue a standalone source waits on and every event wakes, so a caller can watch more on it (a child's end, std.process.exec.watch_exit) and have `wait` return for either |
| [`close`](#close) | release the process's event source: the native handlers are restored, the owned queue closed and the runtime registration released; the first refusal is reported after every step has run |

---

## Kind

```mach
pub def Kind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `SERVICE_STOP` | `0` |  |
| `CONSOLE_CLOSE` | `1` |  |
| `TERMINATE` | `2` |  |
| `INTERRUPT` | `3` |  |
| `RELOAD` | `4` |  |

## Event

```mach
pub rec Event {
    kind: Kind;
}
```

one lifecycle event, as next drains it

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `Kind` | which event |

## Capabilities

```mach
pub rec Capabilities {
    terminate:     bool;
    interrupt:     bool;
    reload:        bool;
    console_close: bool;
    service_stop:  bool;
}
```

which kinds of event the target can deliver

| Field | Type | |
| :--- | :--- | :--- |
| `terminate` | `bool` | TERMINATE is delivered |
| `interrupt` | `bool` | INTERRUPT is delivered |
| `reload` | `bool` | RELOAD is delivered |
| `console_close` | `bool` | CONSOLE_CLOSE is delivered |
| `service_stop` | `bool` | SERVICE_STOP is delivered |

### capabilities

```mach
pub fun capabilities() Capabilities
```

which kinds of event this target delivers

| Parameter | |
| :--- | :--- |
| **returns** | reload on posix, console_close and service_stop on windows, terminate and interrupt on both |

## Source

```mach
pub rec Source {
    generation:   usize;
    owns_queue:   bool;
    runtime:      *std.io.runtime.Runtime;
    registration: std.io.runtime.SourceToken;
    registered:   bool;
}
```

the process's one event source, filled by make or make_runtime

| Field | Type | |
| :--- | :--- | :--- |
| `generation` | `usize` | which claim of the process this source holds |
| `owns_queue` | `bool` | the source made its own wait queue, so wait and queue work |
| `runtime` | `*std.io.runtime.Runtime` | the runtime the source is attached to, or nil |
| `registration` | `std.io.runtime.SourceToken` | the source's registration with that runtime |
| `registered` | `bool` | registration is live |

### make

```mach
pub fun make(source: *Source) err[std.io.error.Error]
```

claim the process's event source with its own wait queue

| Parameter | |
| :--- | :--- |
| `source` | the source to fill, which close releases |
| **returns** | BUSY when another source owns the process, or the native failure |

### make_runtime

```mach
pub fun make_runtime(source: *Source, runtime: *std.io.runtime.Runtime) err[std.io.error.Error]
```

the source must close before the runtime whose queue it borrows

an event that becomes pending ends the runtime's wait with zero completions,
as a caller wake does: the caller drains with next after every wait return,
the same as after the standalone wait

### notify_service_stop

```mach
pub fun notify_service_stop(source: *Source) err[std.io.error.Error]
```

windows service handlers call this for stop, shutdown, or preshutdown control

### next

```mach
pub fun next(source: *Source) res[opt[Event], std.io.error.Error]
```

events are coalesced by kind and drained in service-to-reload priority order

| Parameter | |
| :--- | :--- |
| **returns** | the next pending event, absent when none is pending, or CLOSED for a source that is not the open owner |

### begin_runtime_drain

```mach
pub fun begin_runtime_drain(
    source: *Source,
    runtime: *std.io.runtime.Runtime,
    event: Event,
) res[std.io.lifecycle.CloseResult, std.io.error.Error]
```

begin the graceful close of a runtime in answer to a termination event

| Parameter | |
| :--- | :--- |
| `source` | the open source the event came from |
| `runtime` | the runtime to close |
| `event` | the event, any kind but RELOAD |
| **returns** | the runtime's close result, or INVALID for a source that is not the open owner, a nil runtime or a RELOAD event |

### wait

```mach
pub fun wait(source: *Source, timeout_ms: i32) res[bool, std.io.error.Error]
```

standalone sources may wait directly, runtime-attached sources use runtime wait.
the wait also returns when anything else watched on the source's queue is ready

| Parameter | |
| :--- | :--- |
| **returns** | whether an event is pending after the wait, or the failure |

### queue

```mach
pub fun queue(source: *Source) *std.system.os.IoQueue
```

the wait queue a standalone source waits on and every event wakes, so a caller
can watch more on it (a child's end, std.process.exec.watch_exit) and have
`wait` return for either

| Parameter | |
| :--- | :--- |
| **returns** | the queue, borrowed until close, or nil for a source that is not the open owner or is attached to a runtime |

### close

```mach
pub fun close(source: *Source) err[std.io.error.Error]
```

release the process's event source: the native handlers are restored, the
owned queue closed and the runtime registration released; the first
refusal is reported after every step has run

