[std](../README.md) / **terminal**

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

The directory's root module is [`std.terminal`](../terminal.md).

| Module | |
| :--- | :--- |
| [`darwin`](darwin.md) | darwin terminal keyboard input through public libsystem termios functions |
| [`error`](error.md) | terminal outcomes shared by std.terminal and its per-os backends |
| [`key`](key.md) | decoded keyboard key shared by std.terminal and its per-os backends |
| [`linux`](linux.md) | linux terminal keyboard input backend (see ../terminal.mach) |
| [`windows`](windows.md) | windows terminal keyboard input backend (see ../terminal.mach) |

