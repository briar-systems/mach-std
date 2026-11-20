[std](../README.md) / [system](README.md) / **dit**

# std.system.dit

the processor's data-independent-timing mode (PSTATE.DIT) on aarch64

a soft constant-time function switches the mode itself: its entry reads
PSTATE.DIT and, where it is off, sets it, and its return clears it again
where the entry set it. where the build does not select FEAT_DIT, the entry
first reads `__mach_timing_available` and runs without the mode where it is
0. the byte is one per image, hidden:

- every object that reads it defines it, weak and zero, so an image with a
  soft function holds it whether or not it reaches this module. the strong
  definition here stands for those where it does. it is never exported.
- std's program start sets it once before main and before any thread
  starts: 1 when the processor provides DIT and the process may switch it,
  0 otherwise. linux reads HWCAP_DIT in AT_HWCAP and darwin
  hw.optional.arm.FEAT_DIT, both through `os.cpu_dit`, and freestanding reads
  ID_AA64PFR0_EL1 at EL1. windows leaves the mode off, so the byte stays 0.
- a linux shared library runs no program start: mirl gives it a probe,
  `__mach_timing_probe`, which the loader runs before any other function it
  runs in the image and which reads ID_AA64PFR0_EL1 through the kernel's
  emulation of that read.

nothing turns the mode on at start or per thread. `enable`, `disable` and
`read` are for code that manages the mode itself. the enable sequence is
`msr dit, 1` then `dsb nsh; isb sy`.

the module imports no other std module but bool, so the runtimes and
crypto.ct can call it without a cycle. the test of `enable`, which needs the
OS's answer through `os.cpu_dit`, lives in std.system.cpu. the module builds
on every target, so the entry points can reference it unconditionally.

Source: [`src/system/dit.mach`](../../../src/system/dit.mach)

| Functions | |
| :--- | :--- |
| [`publish`](#publish) | publish whether the process may switch the mode, before main and before any thread starts |
| [`available`](#available) | whether the processor provides the mode and the process may switch it |
| [`enable`](#enable) | set PSTATE.DIT for the calling thread |
| [`disable`](#disable) | clear PSTATE.DIT for the calling thread, synchronized as enable is |
| [`read`](#read) | the calling thread's PSTATE.DIT, `DIT_BIT` when the mode is on |
| [`engage`](#engage) | set the mode for the calling thread where the processor provides it |

| Constants | |
| :--- | :--- |
| [`PROVIDED`](#constants) | whether this target has the mode for a process to set |
| [`DIT_BIT`](#constants) | the bit the mode occupies in PSTATE, as `mrs x0, dit` reads it |

---

## Functions

### publish

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`:

```mach
pub fun publish(available: i64)
```

Otherwise:

```mach
pub fun publish(available: i64)
```

publish whether the process may switch the mode, before main and before
any thread starts

| Parameter | |
| :--- | :--- |
| `available` | 1 when the processor and kernel provide DIT, 0 when not, negative when the answer could not be read. `os.cpu_dit()` on linux and darwin, the entry's own read on freestanding |

### available

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`:

```mach
pub fun available() bool
```

Otherwise:

```mach
pub fun available() bool
```

whether the processor provides the mode and the process may switch it

| Parameter | |
| :--- | :--- |
| **returns** | true once publish recorded 1 |

### enable

Only where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`.

```mach
#[extension("dit")]
pub fun enable()
```

set PSTATE.DIT for the calling thread

`msr dit, 1`, then `dsb nsh` and `isb sy` so nothing after this point
was fetched or issued under the old state

### disable

Only where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`.

```mach
#[extension("dit")]
pub fun disable()
```

clear PSTATE.DIT for the calling thread, synchronized as enable is

### read

Only where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`.

```mach
#[extension("dit")]
pub fun read() u64
```

the calling thread's PSTATE.DIT, `DIT_BIT` when the mode is on

### engage

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`:

```mach
pub fun engage() bool
```

Otherwise:

```mach
pub fun engage() bool
```

set the mode for the calling thread where the processor provides it

| Parameter | |
| :--- | :--- |
| **returns** | whether the mode is now on for the calling thread |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `PROVIDED` | `bool` | `true` where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows`; `false` otherwise | whether this target has the mode for a process to set |
| `DIT_BIT` | `u64` | `1 << 24` where `$mach.build.arch == $mach.arch.aarch64 && $mach.build.sys != $mach.sys.windows` | the bit the mode occupies in PSTATE, as `mrs x0, dit` reads it |

