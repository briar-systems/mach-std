[std](../README.md) / [terminal](README.md) / **windows**

# std.terminal.windows

windows terminal keyboard input backend (see ../terminal.mach)

windows has no termios/ioctl -- console mode is toggled via kernel32's
GetConsoleMode/SetConsoleMode, and single keys are polled via
GetNumberOfConsoleInputEvents + ReadConsoleInputA, since the console layer
delivers structured key-event records, not a raw byte stream. arrows already
arrive as a distinct virtual-key code, so this backend decodes them in
poll_key and the parent's poll_key_decoded is a passthrough here.

raw-mode state is a single process-global toggle and is not thread-safe. this
backend cannot be built or tested on a non-windows host.

Source: [`src/terminal/windows.mach`](../../../src/terminal/windows.mach)

Uses types from [`std.terminal.error`](error.md).

| Functions | |
| :--- | :--- |
| [`is_raw`](#is_raw) | whether raw mode is currently active |
| [`flush_input`](#flush_input) | no FlushConsoleInputBuffer binding yet -- poll_key already consumes only one event per call, so there is nothing separate to flush for this surface |
| [`is_terminal`](#is_terminal) | |
| [`enable_raw`](#enable_raw) | switch stdin into raw mode -- same semantics as terminal.linux.enable_raw: no line buffering, no local echo |
| [`disable_raw`](#disable_raw) | restore whatever GetConsoleMode saw before enable_raw ran |
| [`poll_key`](#poll_key) | read one key-event record without blocking |

---

## Functions

### is_raw

```mach
pub fun is_raw() bool
```

whether raw mode is currently active

### flush_input

```mach
pub fun flush_input() std.terminal.error.Operation
```

no FlushConsoleInputBuffer binding yet -- poll_key already consumes only one
event per call, so there is nothing separate to flush for this surface. a
real binding would go here if that changes.

| Parameter | |
| :--- | :--- |
| **returns** | ok (always succeeds) |

### is_terminal

```mach
pub fun is_terminal(fd: usize) bool
```

### enable_raw

```mach
pub fun enable_raw() std.terminal.error.Operation
```

switch stdin into raw mode -- same semantics as terminal.linux.enable_raw:
no line buffering, no local echo. windows has no VMIN/VTIME equivalent;
non-blocking polling comes from checking GetNumberOfConsoleInputEvents before
reading, in poll_key below, rather than from the mode itself.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal (EINVAL when stdin is not a console) |

### disable_raw

```mach
pub fun disable_raw() std.terminal.error.Operation
```

restore whatever GetConsoleMode saw before enable_raw ran

safe to call even if raw mode isn't active (no-op). pair with
`fin { terminal.disable_raw(); }` after a successful enable_raw.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal; raw mode stays active after a refusal |

### poll_key

```mach
pub fun poll_key() std.terminal.error.Poll
```

read one key-event record without blocking

unlike linux/darwin's raw byte, this checks GetNumberOfConsoleInputEvents
first and reports absence if nothing is queued -- there's no
read-returns-0-when-empty convention on the console API. a failed console
call is the error, distinct from an empty queue. non-key events (a key-up,
resize, or mouse event) are consumed and reported as absence so the next
poll sees fresh data rather than piling up.

| Parameter | |
| :--- | :--- |
| **returns** | some{byte} for an ascii key, some{special} for a decoded arrow, none when nothing usable was queued, or the native console failure |

