[std](../README.md) / [terminal](README.md) / **linux**

# std.terminal.linux

linux terminal keyboard input backend (see ../terminal.mach)

raw ioctl(TCGETS/TCSETSF) over std.system.os.linux's syscall3 -- no libc,
matching the rest of std.system.os.linux. owns only the genuinely per-os
pieces (mode toggle and single-byte poll); the portable Key type and arrow
decoding live in the parent. raw-mode state is a single process-global toggle
(_raw_active) and is not thread-safe.

Source: [`src/terminal/linux.mach`](../../../src/terminal/linux.mach)

Uses types from [`std.terminal.error`](error.md).

| Functions | |
| :--- | :--- |
| [`is_terminal`](#is_terminal) | |
| [`flush_input`](#flush_input) | drop whatever's sitting unread in the input queue |
| [`is_raw`](#is_raw) | whether raw mode is currently active |
| [`enable_raw`](#enable_raw) | switch stdin into raw mode: no line buffering, no local echo, reads return immediately whether or not a byte is waiting (VMIN=0, VTIME=0 -- the tty's own non-blocking convention, distinct from O_NONBLOCK on the fd) |
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

worth calling right before enable_raw / disable_raw so a burst of stale
keystrokes from the old mode doesn't leak into the new one.

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

switch stdin into raw mode: no line buffering, no local echo, reads return
immediately whether or not a byte is waiting (VMIN=0, VTIME=0 -- the tty's
own non-blocking convention, distinct from O_NONBLOCK on the fd).

the previous settings are saved and restored by disable_raw. calling this
twice without a matching disable_raw is a no-op.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal (ENOTTY when stdin is not a terminal) |

### disable_raw

```mach
pub fun disable_raw() std.terminal.error.Operation
```

restore whatever tcgetattr saw before enable_raw ran

safe to call even if raw mode isn't active (no-op). pair with
`fin { terminal.disable_raw(); }` after a successful enable_raw so the
terminal comes back even if the caller returns early or panics.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal; raw mode stays active after a refusal |

### poll_key

```mach
pub fun poll_key() std.terminal.error.Poll
```

read one raw byte without blocking

requires raw mode (enable_raw); call once per game-loop tick. a genuine read
failure is the error, distinct from an empty queue (absence).

| Parameter | |
| :--- | :--- |
| **returns** | some{byte} if one was waiting, none when the queue was empty, or the native read failure |

