[std](../../README.md) / [system](../README.md) / [os](README.md) / **shared**

# std.system.os.shared

abstract types and constants for the OS interface

types here are target-independent. every OS implementation populates them.

Source: [`src/system/os/shared.mach`](../../../../src/system/os/shared.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Timespec`](#timespec) | `rec` | seconds and nanoseconds from a clock source |
| [`IoQueue`](#ioqueue) | `rec` | native wait queue state owned by the portable completion runtime |
| [`ThreadBlock`](#threadblock) | `rec` | the per-thread block std installs for each thread it runs |
| [`DirectoryEntry`](#directoryentry) | `rec` | the name is borrowed until the next cursor operation, including eof or failure |
| [`NativePath`](#nativepath) | `rec` | a whole path in native units, nul-terminated, as native_path gives it |
| [`NativeEntry`](#nativeentry) | `rec` | a directory entry in native units, borrowed until the next cursor operation like a DirectoryEntry |
| [`DirectoryInitResult`](#directoryinitresult) | `rec` | initialization failure and failed duplicate cleanup remain independent |
| [`ProcessStatus`](#processstatus) | `rec` |  |
| [`ProcessWaitError`](#processwaiterror) | `rec` |  |
| [`FileLimit`](#filelimit) | `rec` | the open-file limit |
| [`WaitResult`](#waitresult) | `rec` | pid is positive for an observation, zero for no event or an error |
| [`EnvironmentOf`](#environmentof) | `tag` | the environment a spawn or exec hands its child, its entries in units T |
| [`Environment`](#environment) | `def` | the environment of a UTF-8 spawn, its entries in UTF-8 |
| [`NativeEnvironment`](#nativeenvironment) | `def` | the environment of a native spawn, its entries in std.runtime.native units |

| On `IoQueue` | |
| :--- | :--- |
| [`io_wake_claim`](#io_wake_claim) | whether this request must post the native wake: only the first since the last harvest does |
| [`io_wake_posted`](#io_wake_posted) | the claimed wake was posted |
| [`io_wake_harvested`](#io_wake_harvested) | the posted wake was taken, or a claimed one could not be posted |

| On `ProcessStatus` | |
| :--- | :--- |
| [`posix_status`](#posix_status) | native producers identify their own continued encoding before decoding |

| Functions | |
| :--- | :--- |
| [`io_context_source`](#io_context_source) | the source id a registered readiness context carries |
| [`io_source_context`](#io_source_context) | a readiness context for source from the source's own 48 low bits |

| Constants | |
| :--- | :--- |
| [`IO_SOURCE_SHIFT`](#constants) | a registered readiness context carries its source id in the top 16 bits, the rest belongs to the source |
| [`PUBLICATION_CLAIMS`](#constants) | independently qualified cooperative publication capabilities |
| [`PUBLICATION_RETAIN_REPLACE`](#constants), [`PUBLICATION_READ_RETAIN_REPLACE`](#constants) | |
| [`SEEK_SET`](#constants) | seek whence |
| [`SEEK_CUR`](#constants), [`SEEK_END`](#constants) | |
| [`PROT_NONE`](#constants) | memory protection flags |
| [`PROT_READ`](#constants), [`PROT_WRITE`](#constants), [`PROT_EXEC`](#constants) | |
| [`ADVISE_NORMAL`](#constants) | memory advisory hints |
| [`ADVISE_RANDOM`](#constants), [`ADVISE_SEQUENTIAL`](#constants), [`ADVISE_WILL_NEED`](#constants), [`ADVISE_DONT_NEED`](#constants) | |
| [`HUGE_2MB`](#constants) | standard huge page sizes |
| [`HUGE_1GB`](#constants) | |
| [`HEAP_RESERVE`](#constants) | heap region reserve size (256MB) |
| [`PROCESS_EXITED`](#constants) | a process state observation, with a full native windows exit code |
| [`PROCESS_SIGNALED`](#constants), [`PROCESS_STOPPED`](#constants), [`PROCESS_CONTINUED`](#constants), [`PROCESS_OP_WAIT`](#constants), [`PROCESS_OP_STATUS`](#constants), [`PROCESS_OP_CLOSE`](#constants), [`PROCESS_OP_SPAWN`](#constants), [`PROCESS_OP_READ`](#constants), [`PROCESS_OP_PIPE`](#constants), [`PROCESS_OP_TERMINATE`](#constants) | |
| [`LIMIT_UNLIMITED`](#constants) | a limit with no bound |

---

## Timespec

```mach
pub rec Timespec {
    sec:  i64;
    nsec: i64;
}
```

seconds and nanoseconds from a clock source

| Field | Type | |
| :--- | :--- | :--- |
| `sec` | `i64` | whole seconds |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |

## IoQueue

```mach
pub rec IoQueue {
    handle:       usize;
    wake:         usize;
    wake_pending: usize;
    wakes_posted: usize;
}
```

native wait queue state owned by the portable completion runtime

| Field | Type | |
| :--- | :--- | :--- |
| `wake_pending` | `usize` | 1 from the first wake request until a poll harvests the posted wake, so later requests in that window post nothing |
| `wakes_posted` | `usize` | native wakes actually posted, for the scaling tests  the two counters are words because a signal handler can wake the queue, and word atomics take no lock on any target |

### io_wake_claim

```mach
pub fun io_wake_claim(queue: *IoQueue) bool
```

whether this request must post the native wake: only the first since the
last harvest does. a later request finds its work done by the collector that
harvests the posted wake, because the collector clears the flag after taking
the wake and before it looks for work

### io_wake_posted

```mach
pub fun io_wake_posted(queue: *IoQueue)
```

the claimed wake was posted

### io_wake_harvested

```mach
pub fun io_wake_harvested(queue: *IoQueue)
```

the posted wake was taken, or a claimed one could not be posted

## ThreadBlock

```mach
pub rec ThreadBlock {
    self_addr:  usize;
    stack_low:  usize;
    stack_high: usize;
}
```

the per-thread block std installs for each thread it runs

the implementation owns the block of every thread it spawns and installs it
before the thread runs any std code. the runtime installs a static one for the
main thread before main, unless a loader owns that thread's thread pointer
(see OS-CONTRACT.md). its address identifies the thread while it lives.
it is not general thread-local storage. on linux it shares an area with the
thread's copy of the executable's thread-local template, at the thread
pointer on x86_64 and just below it on aarch64, riscv64 and riscv32.

| Field | Type | |
| :--- | :--- | :--- |
| `self_addr` | `usize` | the block's own address, written when it is installed. x86_64 linux reads the thread pointer through it (fs:[0]), as the psABI has every thread control block do |
| `stack_low` | `usize` | the lowest address of the thread's stack, recorded once where the implementation keeps the bounds here |
| `stack_high` | `usize` | one past the highest usable address of the thread's stack, or 0 where the block records no bounds |

## DirectoryEntry

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

## NativePath

```mach
pub rec NativePath {
    units: *Unit;
    size:  usize;
}
```

a whole path in native units, nul-terminated, as native_path gives it

| Field | Type | |
| :--- | :--- | :--- |
| `units` | `*Unit` | the path, borrowed from the UTF-8 input where that already is the native name, owned otherwise |
| `size` | `usize` | bytes owned, 0 when borrowed |

## NativeEntry

```mach
pub rec NativeEntry {
    name:      *Unit;
    length:    usize;
    type_hint: u8;
}
```

a directory entry in native units, borrowed until the next cursor
operation like a DirectoryEntry

| Field | Type | |
| :--- | :--- | :--- |
| `name` | `*Unit` | the entry's nul-terminated name in std.runtime.native units |
| `length` | `usize` | its length in units |

## DirectoryInitResult

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

## ProcessStatus

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

### posix_status

```mach
pub fun posix_status(raw: i32, continued: bool) ProcessStatus
```

native producers identify their own continued encoding before decoding

## ProcessWaitError

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

## FileLimit

```mach
pub rec FileLimit {
    soft:    u64;
    hard:    u64;
    ceiling: u64;
}
```

the open-file limit. soft is the limit in force, hard its ceiling for an
unprivileged raise, and ceiling the highest soft value this process may set,
which the implementation fills and a set ignores

## WaitResult

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

## EnvironmentOf

```mach
pub tag EnvironmentOf[T]: u8 {
    given: **T;
    inherit;
}
```

the environment a spawn or exec hands its child, its entries in units T

| Case | Payload | |
| :--- | :--- | :--- |
| `given` | `**T` | a nil-terminated array of nul-terminated NAME=value entries in T, passed as given. a nil array is not an environment and is refused with EINVAL. it is the first case, so a zeroed environment is refused rather than inherited |
| `inherit` |  | this process's own environment in native units, with no conversion: CreateProcessW's NULL environment on windows, the envp the kernel gave the process on linux and darwin |

## Environment

```mach
pub def Environment: EnvironmentOf[u8]
```

the environment of a UTF-8 spawn, its entries in UTF-8

## NativeEnvironment

```mach
pub def NativeEnvironment: EnvironmentOf[Unit]
```

the environment of a native spawn, its entries in std.runtime.native units.
on linux and darwin the units are bytes, so it is Environment itself

## Functions

### io_context_source

```mach
pub fun io_context_source(context: usize) u16
```

the source id a registered readiness context carries

### io_source_context

```mach
pub fun io_source_context(source: u16, low: u64) usize
```

a readiness context for source from the source's own 48 low bits

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `IO_SOURCE_SHIFT` | `u64` | `48` | a registered readiness context carries its source id in the top 16 bits, the rest belongs to the source |
| `PUBLICATION_CLAIMS` | `i64` | `1` | independently qualified cooperative publication capabilities |
| `PUBLICATION_RETAIN_REPLACE` | `i64` | `2` |  |
| `PUBLICATION_READ_RETAIN_REPLACE` | `i64` | `4` |  |
| `SEEK_SET` | `i32` | `0` | seek whence |
| `SEEK_CUR` | `i32` | `1` |  |
| `SEEK_END` | `i32` | `2` |  |
| `PROT_NONE` | `u32` | `0b000` | memory protection flags |
| `PROT_READ` | `u32` | `0b001` |  |
| `PROT_WRITE` | `u32` | `0b010` |  |
| `PROT_EXEC` | `u32` | `0b100` |  |
| `ADVISE_NORMAL` | `u32` | `0` | memory advisory hints |
| `ADVISE_RANDOM` | `u32` | `1` |  |
| `ADVISE_SEQUENTIAL` | `u32` | `2` |  |
| `ADVISE_WILL_NEED` | `u32` | `3` |  |
| `ADVISE_DONT_NEED` | `u32` | `4` |  |
| `HUGE_2MB` | `usize` | `2097152` | standard huge page sizes |
| `HUGE_1GB` | `usize` | `1073741824` |  |
| `HEAP_RESERVE` | `usize` | `268435456` | heap region reserve size (256MB) |
| `PROCESS_EXITED` | `u8` | `1` | a process state observation, with a full native windows exit code |
| `PROCESS_SIGNALED` | `u8` | `2` |  |
| `PROCESS_STOPPED` | `u8` | `3` |  |
| `PROCESS_CONTINUED` | `u8` | `4` |  |
| `PROCESS_OP_WAIT` | `u8` | `1` |  |
| `PROCESS_OP_STATUS` | `u8` | `2` |  |
| `PROCESS_OP_CLOSE` | `u8` | `3` |  |
| `PROCESS_OP_SPAWN` | `u8` | `4` |  |
| `PROCESS_OP_READ` | `u8` | `5` |  |
| `PROCESS_OP_PIPE` | `u8` | `6` |  |
| `PROCESS_OP_TERMINATE` | `u8` | `7` |  |
| `LIMIT_UNLIMITED` | `u64` | `0xffffffffffffffff` | a limit with no bound |

