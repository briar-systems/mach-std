[std](../../README.md) / [system](../README.md) / **capability**

# std.system.capability

which operating system capabilities the build target provides

std.system.os is a contract of primitives in independent groups, and a
target may provide only some of them. each HAS_* constant says whether one
group is available, as a comptime value, so a module gates on it with `$if`
and the unselected branch, OS-bound imports included, is discarded before
resolution:

  $if (capability.HAS_FILES) { use std.system.os; ... }

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

The directory's root module is [`std.system.capability`](../capability.md).

| Module | |
| :--- | :--- |
| [`tests`](tests.md) | a gate in another module selects on the capability constants at comptime |

