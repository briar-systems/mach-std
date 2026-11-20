[std](../README.md) / [system](README.md) / **panic**

# std.system.panic

low-level panic: write message to stderr and terminate, or on bare metal hand it to
the program's sink and park the core

self-contained module with no dependency on std.system.os, so the
os layer and the runtime can panic without a circular import chain.

ONE ARM PER OPERATING SYSTEM, AND NO FALLTHROUGH (#397). This module previously
dispatched `$if linux { ... } $or { ...darwin... }`, so "not linux" MEANT "darwin" and a
windows build silently compiled darwin syscall numbers - a panic there wrote nothing a
reader could see. The terminator was worse: arch-gated with no OS gate at all, so every
OS got `hlt` / `brk` / `ebreak` regardless. Two independent instances of one failure
mode, and both produced a wrong BINARY rather than a build error.

Each OS now defines its own `panic_sink`, selected where the DECLARATIONS are gated rather
than inside one function body. That placement is load-bearing twice over: a helper's
`$error` fires even when its arm is not the selected one, and an `ext fun` is linked
unconditionally wherever it is declared - so a windows-only import declared at module
scope breaks every linux and darwin link. Gating the declarations solves both.

The property this buys is that an OS with no arm has no `panic_sink` and therefore CANNOT
BUILD, rather than inheriting another platform's syscalls. Deleting the windows arm and
building for windows demonstrates it. The trailing `$error` names that case explicitly
when comptime reaches it first; either way the failure is at compile time. linux,
darwin, wasi, windows, uefi and freestanding have arms. spirv reaches the `$error`, as a
shader has no write target and no process to end.

THE FREESTANDING ARM HAS NO WRITE TARGET of its own, so the program installs one with
`install` and the arm parks the core after it, or parks at once when none is installed.
The hook is set at run time rather than overridden at link time because a sink usually
drives a device the program brings up itself, so a panic before that point must park
rather than call into a device that is not ready yet.

THE WRITE AND THE TERMINATOR MOVE TOGETHER, in one `panic_sink` per platform. Splitting
them is what made the windows breakage look survivable: fixing only the terminator would
have produced a correct exit status for a message nobody ever saw.

Source: [`src/system/panic.mach`](../../../src/system/panic.mach)

| Functions | |
| :--- | :--- |
| [`panic_sink`](#panic_sink) | write(2, msg, len) then exit_group(255) |
| [`install`](#install) | install the program's panic sink |
| [`panic`](#panic) | write a null-terminated message to stderr and abort |

| Constants | |
| :--- | :--- |
| [`PANIC_EXIT`](#constants) | the process exit status a panic terminates with |

---

## Functions

### panic_sink

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.linux`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.darwin`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.wasi`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.uefi`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.freestanding`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

write(2, msg, len) then exit_group(255)

exit_group rather than exit so every thread of the process ends - a panic on a
worker must not leave the rest running. The trap after it is unreachable and kept
only as a guard, matching `std.system.os.exit`; it is NOT the terminator.

| Parameter | |
| :--- | :--- |
| `msg` | message bytes |
| `len` | message length |

### install

Only where `$mach.build.sys == $mach.sys.freestanding` and not `$mach.build.sys == $mach.sys.linux`, `$mach.build.sys == $mach.sys.darwin`, `$mach.build.sys == $mach.sys.wasi`, `$mach.build.sys == $mach.sys.windows` nor `$mach.build.sys == $mach.sys.uefi`.

```mach
pub fun install(sink: fun(*u8, usize))
```

install the program's panic sink

bare metal has no write target std could know, so the program says where a
message goes: a uart, a framebuffer, a debug port. the sink is called with
the message and the core is parked when it returns, so a panic never
returns either way. installing nil restores the default, which only parks.

| Parameter | |
| :--- | :--- |
| `sink` | called with the message bytes and their length |

### panic

```mach
pub fun panic(msg: *u8)
```

write a null-terminated message to stderr and abort

| Parameter | |
| :--- | :--- |
| `msg` | pointer to null-terminated error message |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `PANIC_EXIT` | `u32` | `255` | the process exit status a panic terminates with |

