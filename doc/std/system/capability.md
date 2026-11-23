[std](../README.md) / [system](README.md) / **capability**

# std.system.capability

which operating system capabilities the build target provides

std.system.os is a contract of primitives in independent groups, and a
target may provide only some of them. each HAS_* constant says whether one
group is available, as a comptime value, so a module gates on it with `$if`
and the unselected branch, OS-bound imports included, is discarded before
resolution:

  $if (capability.HAS_FILES) { use std.system.os; ... }

a module that cannot exist without a group refuses itself at module scope,
naming itself and the flag, so a program that imports it on a target without
the group is told what the target lacks:

  $or { $error("std.sync.cancel needs the threads capability (std.system.capability.HAS_THREADS)"); }

a single declaration cannot refuse that way: a function whose body reaches a
`$error` fires wherever its module is checked, used or not. so a public name
gated on a group inside a module that exists everywhere is absent where the
group is, and naming it there reports it as not exported.

this module imports nothing OS-bound and builds on every target, freestanding
included. the members and assumptions behind each group are the contract
itself: std.system.os, described in OS-CONTRACT.md.

groups:

  core      error translation, panic sink, exit. present whenever HOSTED is
  pages     page allocation, protection, locking and advice
  clock     realtime and monotonic clocks, sleep
  entropy   cryptographic random fill
  threads   thread spawn and join, futex-shaped wait and wake, cpu count
  files     open, read, write, positioned io, stat, directories, pipes
  io_queue  the native completion or readiness queue
  sockets   stream, datagram and local sockets
  process   spawn, wait, process id, environment
  cpu       the processor's instruction-set extensions, for run-time dispatch

each target selects one row of group bits below, so a new target, a new wasi
preview or a new group is one row or one bit. a target that is not listed provides nothing,
so a module gated on a group refuses it rather than resolving against an OS
layer it does not have.

Source: [`src/system/capability.mach`](../../../src/system/capability.mach)

| Constants | |
| :--- | :--- |
| [`HOSTED`](#constants) | std.system.os resolves on this target: its core group is present |
| [`HAS_PAGES`](#constants), [`HAS_CLOCK`](#constants), [`HAS_ENTROPY`](#constants), [`HAS_THREADS`](#constants), [`HAS_FILES`](#constants), [`HAS_IO_QUEUE`](#constants), [`HAS_SOCKETS`](#constants), [`HAS_PROCESS`](#constants) | |
| [`REUSE_PORT_BALANCES`](#constants) | SO_REUSEPORT spreads a port's connections and datagrams across the sockets bound to it |
| [`HAS_FILE_MODES`](#constants) | the files group's stat reports permission bits and set_mode changes them |
| [`HAS_CPU_FEATURES`](#constants) | std.system.os fills std.system.cpu.features.Features on this target |

---

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `HOSTED` | `bool` | `(GROUPS & CORE) != 0` | std.system.os resolves on this target: its core group is present |
| `HAS_PAGES` | `bool` | `(GROUPS & PAGES) != 0` |  |
| `HAS_CLOCK` | `bool` | `(GROUPS & CLOCK) != 0` |  |
| `HAS_ENTROPY` | `bool` | `(GROUPS & ENTROPY) != 0` |  |
| `HAS_THREADS` | `bool` | `(GROUPS & THREADS) != 0` |  |
| `HAS_FILES` | `bool` | `(GROUPS & FILES) != 0` |  |
| `HAS_IO_QUEUE` | `bool` | `(GROUPS & IO_QUEUE) != 0` |  |
| `HAS_SOCKETS` | `bool` | `(GROUPS & SOCKETS) != 0` |  |
| `HAS_PROCESS` | `bool` | `(GROUPS & PROCESS) != 0` |  |
| `REUSE_PORT_BALANCES` | `bool` | `$mach.build.sys == $mach.sys.linux` | SO_REUSEPORT spreads a port's connections and datagrams across the sockets bound to it |
| `HAS_FILE_MODES` | `bool` | `HAS_FILES && $mach.build.sys != $mach.sys.wasi` | the files group's stat reports permission bits and set_mode changes them |
| `HAS_CPU_FEATURES` | `bool` | `(GROUPS & CPU) != 0` | std.system.os fills std.system.cpu.features.Features on this target |

