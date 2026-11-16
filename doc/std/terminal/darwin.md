[std](../README.md) / [terminal](README.md) / **darwin**

# std.terminal.darwin

darwin terminal keyboard input through public libsystem termios functions

raw-mode state is process-global and is not thread-safe.

Source: [`src/terminal/darwin.mach`](../../../src/terminal/darwin.mach)

Uses types from [`std.terminal.error`](error.md).

| Functions | |
| :--- | :--- |
| [`is_terminal`](#is_terminal) | |
| [`flush_input`](#flush_input) | drop whatever's sitting unread in the input queue |
| [`is_raw`](#is_raw) | whether raw mode is currently active |
| [`enable_raw`](#enable_raw) | switch stdin into raw mode -- same semantics as terminal.linux.enable_raw: no line buffering, no local echo, non-blocking reads (VMIN=0, VTIME=0) |
| [`disable_raw`](#disable_raw) | restore whatever tcgetattr saw before enable_raw ran |
| [`poll_key`](#poll_key) | read one raw byte without blocking |

---

## Functions

### is_terminal

```mach
pub fun is_terminal(fd: usize) bool
```

### flush_input

```mach
pub fun flush_input() std.terminal.error.Operation
```

drop whatever's sitting unread in the input queue

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal |

### is_raw

```mach
pub fun is_raw() bool
```

whether raw mode is currently active

### enable_raw

```mach
pub fun enable_raw() std.terminal.error.Operation
```

switch stdin into raw mode -- same semantics as terminal.linux.enable_raw:
no line buffering, no local echo, non-blocking reads (VMIN=0, VTIME=0).

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal (ENOTTY when stdin is not a terminal) |

### disable_raw

```mach
pub fun disable_raw() std.terminal.error.Operation
```

restore whatever tcgetattr saw before enable_raw ran

safe to call even if raw mode isn't active (no-op). pair with
`fin { terminal.disable_raw(); }` after a successful enable_raw.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal; raw mode stays active after a refusal |

### poll_key

```mach
pub fun poll_key() std.terminal.error.Poll
```

read one raw byte without blocking

requires raw mode; a genuine read failure is the error, distinct from an
empty queue (absence).

| Parameter | |
| :--- | :--- |
| **returns** | some{byte} if one was waiting, none when the queue was empty, or the native read failure |

