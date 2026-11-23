[std](README.md) / **terminal**

# std.terminal

terminal keyboard input: raw single-key polling for game loops

raw mode turns off line buffering and local echo so keystrokes arrive one
byte at a time without waiting for enter; poll_key / poll_key_decoded then
read at most one key per call without blocking, suiting a per-frame loop.
plain press-enter line input is not a terminal concern and lives in
std.input (it needs no tty and works over pipes and redirects).

lifecycle: enable_raw once, poll each frame, disable_raw on exit. always pair
the two -- e.g. `fin { terminal.disable_raw(); }` -- so the terminal is
restored even on an early return. raw-mode state is a single process-global
toggle: not thread-safe, not reentrant. all i/o targets the stdin fd.

outcomes: the mode and queue controls return err[TermError] and a poll
returns res[opt[Key], TermError], where an empty queue is absence and a
native read failure is the error. TermError nests the native io failure with
its operation.

the Key type, its kinds, and the special-key constants come from
std.terminal.key and the outcome tags from std.terminal.error; both are
re-exported here.

Source: [`src/terminal.mach`](../../src/terminal.mach)

Uses types from [`std.terminal.error`](terminal/error.md).

| Functions | |
| :--- | :--- |
| [`control_failure`](#control_failure) | a native refusal on a mode or queue control call |
| [`read_failure`](#read_failure) | a native refusal on a poll |
| [`flush_input`](#flush_input) | drop whatever's sitting unread in the input queue, read-ahead bytes included |
| [`poll_key`](#poll_key) | read one key without blocking |
| [`poll_key_decoded`](#poll_key_decoded) | poll_key, which already decodes arrows on windows |

| Forwards | |
| :--- | :--- |
| [`KeyKind`](#keykind) | key representation (from std.terminal.key) |
| [`KIND_NONE`](#kind_none), [`KIND_BYTE`](#kind_byte), [`KIND_SPECIAL`](#kind_special), [`Special`](#special), [`KEY_UP`](#key_up), [`KEY_DOWN`](#key_down), [`KEY_LEFT`](#key_left), [`KEY_RIGHT`](#key_right), [`Key`](#key), [`key_none`](#key_none), [`key_byte`](#key_byte), [`key_special`](#key_special), [`is_none`](#is_none), [`is_byte`](#is_byte), [`is_special`](#is_special) | |
| [`TermError`](#termerror) | outcomes (from std.terminal.error) |
| [`Operation`](#operation), [`Poll`](#poll), [`code`](#code) | |
| [`is_terminal`](#is_terminal) | whether a descriptor is a terminal, as os.stdout() or any other handle |
| [`enable_raw`](#enable_raw) | mode control (per-os backend) |
| [`disable_raw`](#disable_raw), [`is_raw`](#is_raw) | |

---

## Functions

### control_failure

```mach
pub fun control_failure(code: i64) std.terminal.error.TermError
```

a native refusal on a mode or queue control call

### read_failure

```mach
pub fun read_failure(code: i64) std.terminal.error.TermError
```

a native refusal on a poll

### flush_input

```mach
pub fun flush_input() std.terminal.error.Operation
```

drop whatever's sitting unread in the input queue, read-ahead bytes included

worth calling right before enable_raw / disable_raw so a burst of stale
keystrokes from the old mode doesn't leak into the new one.

| Parameter | |
| :--- | :--- |
| **returns** | ok, or the native refusal |

### poll_key

```mach
pub fun poll_key() std.terminal.error.Poll
```

read one key without blocking

a byte poll_key_decoded read ahead and did not consume comes first, then the
backend's own poll. requires raw mode (enable_raw).

| Parameter | |
| :--- | :--- |
| **returns** | some{key} if one was waiting, none when the queue was empty, or the native read failure |

### poll_key_decoded

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub fun poll_key_decoded() std.terminal.error.Poll
```

Otherwise:

```mach
pub fun poll_key_decoded() std.terminal.error.Poll
```

poll_key, which already decodes arrows on windows

| Parameter | |
| :--- | :--- |
| **returns** | some{key} -- a special arrow or an ordinary byte -- none when nothing was waiting, or the native read failure |

## Forwards

### KeyKind

Forwards [`std.terminal.key.KeyKind`](terminal/key.md#keykind).

```mach
pub def KeyKind: u8
```

key representation (from std.terminal.key)

### KIND_NONE

Forwards [`std.terminal.key.KIND_NONE`](terminal/key.md#keykind).

```mach
pub val KIND_NONE:    KeyKind = 0
```

### KIND_BYTE

Forwards [`std.terminal.key.KIND_BYTE`](terminal/key.md#keykind).

```mach
pub val KIND_BYTE:    KeyKind = 1
```

### KIND_SPECIAL

Forwards [`std.terminal.key.KIND_SPECIAL`](terminal/key.md#keykind).

```mach
pub val KIND_SPECIAL: KeyKind = 2
```

### Special

Forwards [`std.terminal.key.Special`](terminal/key.md#special).

```mach
pub def Special: u8
```

a special (non-byte) key

### KEY_UP

Forwards [`std.terminal.key.KEY_UP`](terminal/key.md#special).

```mach
pub val KEY_UP:    Special = 0
```

### KEY_DOWN

Forwards [`std.terminal.key.KEY_DOWN`](terminal/key.md#special).

```mach
pub val KEY_DOWN:  Special = 1
```

### KEY_LEFT

Forwards [`std.terminal.key.KEY_LEFT`](terminal/key.md#special).

```mach
pub val KEY_LEFT:  Special = 2
```

### KEY_RIGHT

Forwards [`std.terminal.key.KEY_RIGHT`](terminal/key.md#special).

```mach
pub val KEY_RIGHT: Special = 3
```

### Key

Forwards [`std.terminal.key.Key`](terminal/key.md#key).

```mach
pub rec Key {
    kind:    KeyKind;
    byte:    u8;
    special: Special;
}
```

a single decoded key event

### key_none

Forwards [`std.terminal.key.key_none`](terminal/key.md#key_none).

```mach
pub fun key_none() Key
```

a Key meaning nothing was waiting

### key_byte

Forwards [`std.terminal.key.key_byte`](terminal/key.md#key_byte).

```mach
pub fun key_byte(b: u8) Key
```

a Key holding an ordinary byte

### key_special

Forwards [`std.terminal.key.key_special`](terminal/key.md#key_special).

```mach
pub fun key_special(s: Special) Key
```

a Key holding a special (non-byte) key

### is_none

Forwards [`std.terminal.key.is_none`](terminal/key.md#is_none).

```mach
pub fun is_none(k: Key) bool
```

whether no key was waiting

### is_byte

Forwards [`std.terminal.key.is_byte`](terminal/key.md#is_byte).

```mach
pub fun is_byte(k: Key) bool
```

whether the key is an ordinary byte

### is_special

Forwards [`std.terminal.key.is_special`](terminal/key.md#is_special).

```mach
pub fun is_special(k: Key) bool
```

whether the key is a special (non-byte) key

### TermError

Forwards [`std.terminal.error.TermError`](terminal/error.md#termerror).

```mach
pub tag TermError: u8 {
    native: std.io.error.Error;
}
```

outcomes (from std.terminal.error)

### Operation

Forwards [`std.terminal.error.Operation`](terminal/error.md#operation).

```mach
pub def Operation: err[TermError]
```

the outcome of a mode or queue control call

### Poll

Forwards [`std.terminal.error.Poll`](terminal/error.md#poll).

```mach
pub def Poll: res[opt[std.terminal.key.Key], TermError]
```

the outcome of one poll: a waiting key, absence when the queue is empty, or
the native read failure

### code

Forwards [`std.terminal.error.code`](terminal/error.md#code).

```mach
pub fun code(e: TermError) i64
```

the native code behind a terminal failure

### is_terminal

Forwards the first of these whose condition holds:

- [`std.terminal.linux.is_terminal`](terminal/linux.md#is_terminal), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.linux`
- [`std.terminal.darwin.is_terminal`](terminal/darwin.md#is_terminal), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.darwin`
- [`std.terminal.windows.is_terminal`](terminal/windows.md#is_terminal), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.windows`

```mach
pub fun is_terminal(fd: usize) bool
```

whether a descriptor is a terminal, as os.stdout() or any other handle

a pipe, a file or a closed descriptor reads false. on windows a terminal is a
console handle, so a pty that is not a console reads false

### enable_raw

Forwards the first of these whose condition holds:

- [`std.terminal.linux.enable_raw`](terminal/linux.md#enable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.linux`
- [`std.terminal.darwin.enable_raw`](terminal/darwin.md#enable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.darwin`
- [`std.terminal.windows.enable_raw`](terminal/windows.md#enable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.windows`

```mach
pub fun enable_raw() std.terminal.error.Operation
```

mode control (per-os backend)

### disable_raw

Forwards the first of these whose condition holds:

- [`std.terminal.linux.disable_raw`](terminal/linux.md#disable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.linux`
- [`std.terminal.darwin.disable_raw`](terminal/darwin.md#disable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.darwin`
- [`std.terminal.windows.disable_raw`](terminal/windows.md#disable_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.windows`

```mach
pub fun disable_raw() std.terminal.error.Operation
```

restore whatever tcgetattr saw before enable_raw ran

safe to call even if raw mode isn't active (no-op). pair with
`fin { terminal.disable_raw(); }` after a successful enable_raw so the
terminal comes back even if the caller returns early or panics.

### is_raw

Forwards the first of these whose condition holds:

- [`std.terminal.linux.is_raw`](terminal/linux.md#is_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.linux`
- [`std.terminal.darwin.is_raw`](terminal/darwin.md#is_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.darwin`
- [`std.terminal.windows.is_raw`](terminal/windows.md#is_raw), where `capability.HAS_FILES` and `$mach.build.sys == $mach.sys.windows`

```mach
pub fun is_raw() bool
```

whether raw mode is currently active

