[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [darwin](README.md) / **libsystem**

# std.system.os.darwin.libsystem

libSystem imports for the darwin backend

apple does not guarantee syscall-number stability, so `svc 0x80` / `syscall`
is not a supportable distribution surface: libSystem is. every darwin OS
primitive that used to issue a raw trap binds a libSystem symbol declared
here instead.

three things about this boundary are easy to get wrong, so they are settled
once, here, rather than at each call site.

## the errno contract

a raw BSD trap sets the carry flag and returns the POSITIVE errno in the
result register. libSystem uses each function's documented failure sentinel
(-1 for integer results, nil for some pointers, MAP_FAILED for mmap) and
leaves errno in thread-local storage. these are
different contracts, and the difference is not just where the number lives:

  - errno is NOT cleared on success. reading it after a call that succeeded
    returns whatever the last failing call left behind. it may only be read
    once the RETURN VALUE has already said the call failed.
  - a success can be a negative number. `lseek` past 2^63 cannot happen, but
    the rule holds generally: the failure indicator is the documented
    sentinel for that specific function, never "the result is negative".

`fail_errno` is the only way this module converts a failure, and it is only
ever reached from inside an `if` that already tested the sentinel. the darwin
OS layer keeps its existing outward contract - a negative errno - so nothing
above `std.system.os.darwin` changes shape.

## `__error`, and why it is not the thing we refuse to use

`<errno.h>` defines `errno` as `(*__error())`. the underscores make it look
like the private `__open` / `__fcntl` family, but it is the opposite: it is
the documented, stable, public way to reach errno on darwin, and there is no
other one. the symbols this migration refuses are the private SYSCALL shims
(`__open`, `__fcntl`, ...) whose only purpose is to skip the cancellation
wrapper - taking those would leave us on exactly the unsupported surface the
migration exists to leave.

## cancellation: the plain entry points, deliberately

libSystem exports a `$NOCANCEL` twin for every entry point that is a POSIX
cancellation point (`read$NOCANCEL`, `open$NOCANCEL`, ...). this module binds
the PLAIN names on purpose:

  - std has no cancellation model. it never calls `pthread_cancel` and
    exposes no way for a caller to. a cancellation point only acts when a
    cancel is already pending, so with none ever requested the plain entry
    point does exactly what its `$NOCANCEL` twin does.
  - the plain name is the public one. `$NOCANCEL` is a suffixed variant symbol
    that exists to serve libpthread's internals; binding it would put the same
    "Apple never promised you this" question back into the layer whose whole
    purpose is to answer it.

so the choice costs nothing today and keeps the supported surface. should std
ever grow real cancellation, the decision to revisit is here, in one place,
and not spread across sixty call sites.

## `$INODE64`, and why the stat family is arch-gated

macOS grew a 64-bit `st_ino` in 10.5 without breaking the binaries compiled
against the 32-bit one. on x86_64 both layouts still ship: the PLAIN `_fstat`
is the legacy 32-bit-inode struct, and the 64-bit layout - the one `stat_t`
in shared.mach describes - is reached through the `$INODE64` variant symbol.
arm64 has no legacy to carry, so only the plain name exists there.

binding the plain name on x86_64 would link and run and quietly fill the
caller's `stat_t` from a struct with a different field order. that is silent
corruption, not an error, which is why the suffix is applied by an explicit
arch gate rather than left to whatever the linker happens to resolve.

Source: [`src/system/os/darwin/libsystem.mach`](../../../../../src/system/os/darwin/libsystem.mach)

Uses types from [`std.system.os.shared`](../shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`DirectoryStream`](#directorystream) | `def` | opaque public dir stream, never dereferenced by mach |
| [`DirectoryRecord`](#directoryrecord) | `rec` | variable-length native record, only the header and actual name extent are read |
| [`ControlHeader`](#controlheader) | `rec` | the header of one ancillary data item, the layout of struct cmsghdr |
| [`MessageHeader`](#messageheader) | `rec` | the argument of sendmsg and recvmsg, the layout of struct msghdr |
| [`Termios`](#termios) | `rec` | public lp64 termios layout from darwin sys/termios.h |
| [`DlInfo`](#dlinfo) | `rec` | what dladdr reports of the image holding an address |
| [`ResourceLimit`](#resourcelimit) | `rec` | a resource limit, the layout of struct rlimit |
| [`Kevent`](#kevent) | `rec` | pointer-only storage with the SDK field offsets and stronger alignment |

| On `DirectoryStream` | |
| :--- | :--- |
| [`fdopendir`](#fdopendir) | open a directory stream over a directory descriptor, which the stream then owns |
| [`readdir`](#readdir) | the next record of a directory stream |
| [`closedir`](#closedir) | close a directory stream and the descriptor it owns |

| On `MessageHeader` | |
| :--- | :--- |
| [`sendmsg`](#sendmsg) | send a message with optional address and ancillary data |
| [`recvmsg`](#recvmsg) | receive a message with its address and ancillary data |

| On `Termios` | |
| :--- | :--- |
| [`tcgetattr`](#tcgetattr) | read a terminal's settings |
| [`tcsetattr`](#tcsetattr) | apply a terminal's settings |

| On `DlInfo` | |
| :--- | :--- |
| [`dladdr`](#dladdr) | describe the image and nearest symbol holding an address |

| On `ResourceLimit` | |
| :--- | :--- |
| [`getrlimit`](#getrlimit) | read a resource limit |
| [`setrlimit`](#setrlimit) | set a resource limit |

| On `Kevent` | |
| :--- | :--- |
| [`kevent`](#kevent-1) | apply changes to an event queue and collect pending events |

| Functions | |
| :--- | :--- |
| [`errno`](#errno) | the calling thread's current errno, as a positive number |
| [`clear_errno`](#clear_errno) | set the calling thread's errno to 0 |
| [`fail_errno`](#fail_errno) | the current errno negated, for a darwin OS primitive's return |
| [`sysctlbyname`](#sysctlbyname) | read or write a kernel state value by name |
| [`getentropy`](#getentropy) | fill a buffer with cryptographic random bytes |
| [`mmap`](#mmap) | map memory or a file into the address space |
| [`munmap`](#munmap) | unmap a region |
| [`mprotect`](#mprotect) | change the protection of a region |
| [`mlock`](#mlock) | lock a region into physical memory |
| [`munlock`](#munlock) | unlock a region mlock locked |
| [`madvise`](#madvise) | advise the kernel how a region will be accessed |
| [`msync`](#msync) | flush a shared file mapping to its file |
| [`read`](#read) | read bytes from a descriptor |
| [`write`](#write) | write bytes to a descriptor |
| [`pread`](#pread) | read bytes at a file offset without moving the descriptor offset |
| [`pwrite`](#pwrite) | write bytes at a file offset without moving the descriptor offset |
| [`openat`](#openat) | `openat` is C-variadic: the mode argument is only read when the flags carry O_CREAT |
| [`close`](#close) | close a descriptor, which is released even when the close reports failure |
| [`fsync`](#fsync) | flush an open file's data and metadata to storage |
| [`lseek`](#lseek) | reposition a descriptor's offset |
| [`fstat`](#fstat) | read an open file's metadata |
| [`fstatfs`](#fstatfs) | read the metadata of the filesystem holding an open file |
| [`fstatat`](#fstatat) | read a path's metadata relative to a directory |
| [`flock`](#flock) | flock: advisory whole-file lock on an open descriptor |
| [`unlinkat`](#unlinkat) | remove a name relative to a directory |
| [`renameat`](#renameat) | rename a path, each side relative to its own directory |
| [`symlink`](#symlink) | create a symbolic link |
| [`mkdirat`](#mkdirat) | create a directory relative to a directory |
| [`faccessat`](#faccessat) | check access to a path relative to a directory |
| [`getcwd`](#getcwd) | `getcwd(3)` replaces the open(".") + fcntl(F_GETPATH) dance the raw-syscall backend needed |
| [`pipe`](#pipe) | create a unidirectional pipe |
| [`socket`](#socket) | create a socket |
| [`bind`](#bind) | bind a socket to a local address |
| [`listen`](#listen) | mark a socket as accepting connections |
| [`accept`](#accept) | accept a pending connection |
| [`connect`](#connect) | connect a socket to a peer |
| [`sendto`](#sendto) | send bytes on a socket, to an address when it is unconnected |
| [`recvfrom`](#recvfrom) | receive bytes from a socket, with the sender's address |
| [`shutdown`](#shutdown) | shut down one or both directions of a socket |
| [`setsockopt`](#setsockopt) | set a socket option |
| [`getsockopt`](#getsockopt) | read a socket option |
| [`getsockname`](#getsockname) | read a socket's local address |
| [`getpeername`](#getpeername) | read a connected socket's peer address |
| [`writev`](#writev) | write a gather list to a descriptor |
| [`tcflush`](#tcflush) | discard a terminal's queued data |
| [`signal`](#signal) | install a process-wide signal disposition |
| [`sigaction`](#sigaction) | examine or change a signal's disposition |
| [`raise`](#raise) | send a signal to the calling thread |
| [`clock_gettime`](#clock_gettime) | time |
| [`nanosleep`](#nanosleep) | suspend the calling thread for the requested interval |
| [`pthread_create`](#pthread_create) | `start` is a `void *(*)(void *)` passed as a bare address, matching how the windows backend hands CreateThread its trampoline |
| [`pthread_join`](#pthread_join) | wait for a thread to end and release it |
| [`pthread_detach`](#pthread_detach) | let a thread release itself when it ends, so it is never joined |
| [`pthread_setname_np`](#pthread_setname_np) | name the calling thread |
| [`pthread_getname_np`](#pthread_getname_np) | read a thread's name |
| [`pthread_self`](#pthread_self) | the calling thread |
| [`pthread_threadid_np`](#pthread_threadid_np) | a thread's system-wide unique id |
| [`pthread_get_stackaddr_np`](#pthread_get_stackaddr_np) | the top of thread's stack, its highest address plus one |
| [`pthread_get_stacksize_np`](#pthread_get_stacksize_np) | the size of a thread's stack |
| [`pthread_key_create`](#pthread_key_create) | a pthread_key_t is an unsigned long on darwin |
| [`pthread_setspecific`](#pthread_setspecific) | set the calling thread's value for a key |
| [`pthread_getspecific`](#pthread_getspecific) | the calling thread's value for a key |
| [`pthread_attr_init`](#pthread_attr_init) | initialize thread attributes to the defaults |
| [`pthread_attr_destroy`](#pthread_attr_destroy) | release thread attributes |
| [`pthread_attr_setstacksize`](#pthread_attr_setstacksize) | set the stack size threads created with attr get |
| [`pthread_attr_setdetachstate`](#pthread_attr_setdetachstate) | set whether threads created with attr start joinable or detached |
| [`pthread_mutex_init`](#pthread_mutex_init) | initialize a mutex |
| [`pthread_mutex_lock`](#pthread_mutex_lock) | lock a mutex, blocking until it is free |
| [`pthread_mutex_unlock`](#pthread_mutex_unlock) | unlock a mutex the caller holds |
| [`pthread_cond_init`](#pthread_cond_init) | initialize a condition variable |
| [`pthread_cond_wait`](#pthread_cond_wait) | release m and wait on c, holding m again on return |
| [`pthread_cond_timedwait_relative_np`](#pthread_cond_timedwait_relative_np) | release m and wait on c for at most a relative interval, holding m again on return |
| [`pthread_cond_broadcast`](#pthread_cond_broadcast) | wake every thread waiting on a condition variable |
| [`pthread_once`](#pthread_once) | `init` is a `void (*)(void)` passed as a bare address |
| [`umask`](#umask) | set the file-mode creation mask, returning the previous one |
| [`fcntl`](#fcntl) | `fcntl` is C-variadic |
| [`fchmod`](#fchmod) | set a file's permission bits through an open descriptor |
| [`fchmodat`](#fchmodat) | set the permission bits of a path relative to a directory |
| [`fork`](#fork) | create a child process duplicating the caller |
| [`vfork`](#vfork) | create a child process through vfork |
| [`execve`](#execve) | replace the process image, returning only on failure |
| [`wait4`](#wait4) | wait for a child to change state |
| [`waitid`](#waitid) | `info` is a `siginfo_t *` (104 bytes on darwin); the caller passes storage and never reads it, so it is taken as bytes |
| [`kill`](#kill) | send a signal to a process, or to a process group for a negated pid |
| [`getpid`](#getpid) | the calling process's id |
| [`setpgid`](#setpgid) | set the process group of a process |
| [`getpgid`](#getpgid) | the process group of a process |
| [`dup2`](#dup2) | make to name what from names, closing what to named before |
| [`chdir`](#chdir) | change the working directory |
| [`_exit`](#_exit) | end the process at once without running atexit handlers |
| [`kqueue`](#kqueue) | create a kernel event queue |

| Constants | |
| :--- | :--- |
| [`F_DUPFD_CLOEXEC`](#constants), [`MSG_PEEK`](#constants), [`MSG_DONTWAIT`](#constants), [`MSG_TRUNC`](#constants), [`MSG_CTRUNC`](#constants), [`TCSAFLUSH`](#constants), [`TCIFLUSH`](#constants), [`ICANON`](#constants), [`ECHO`](#constants), [`VMIN`](#constants), [`VTIME`](#constants) | |
| [`PTHREAD_MUTEX_BYTES`](#constants) | opaque pthread object sizes, from \<sys/_pthread/_pthread_types.h> on LP64 |
| [`PTHREAD_COND_BYTES`](#constants), [`PTHREAD_ATTR_BYTES`](#constants), [`PTHREAD_ONCE_BYTES`](#constants) | |
| [`PTHREAD_CREATE_JOINABLE`](#constants) | pthread_attr_setdetachstate states (\<pthread.h>) |
| [`PTHREAD_CREATE_DETACHED`](#constants) | |
| [`P_PID`](#constants) | waitid selectors and options (\<sys/wait.h>) |
| [`WEXITED`](#constants), [`WNOWAIT`](#constants) | |
| [`RLIMIT_NOFILE`](#constants) | resource limits (\<sys/resource.h>); `rlim_t` is u64 on LP64 |

| Forwards | |
| :--- | :--- |
| [`IoVector`](#iovector) | |

---

## DirectoryStream

```mach
pub def DirectoryStream: ptr
```

opaque public dir stream, never dereferenced by mach

### fdopendir

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
#[library("libsystem")]
#[symbol("fdopendir$INODE64")]
pub ext fun fdopendir(fd: i32) DirectoryStream
```

Otherwise:

```mach
#[library("libsystem")]
pub ext fun fdopendir(fd: i32) DirectoryStream
```

open a directory stream over a directory descriptor, which the stream then owns

| Parameter | |
| :--- | :--- |
| `fd` | an open directory descriptor |
| **returns** | the stream, or nil with errno set |

### readdir

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
#[library("libsystem")]
#[symbol("readdir$INODE64")]
pub ext fun readdir(stream: DirectoryStream) *DirectoryRecord
```

Otherwise:

```mach
#[library("libsystem")]
pub ext fun readdir(stream: DirectoryStream) *DirectoryRecord
```

the next record of a directory stream

| Parameter | |
| :--- | :--- |
| `stream` | a stream fdopendir opened |
| **returns** | the record, valid until the next call on the stream, or nil at the end (errno untouched) or on failure (errno set) |

### closedir

```mach
#[library("libsystem")]
pub ext fun closedir(stream: DirectoryStream) i32
```

close a directory stream and the descriptor it owns

| Parameter | |
| :--- | :--- |
| `stream` | a stream fdopendir opened, consumed even when the close fails |
| **returns** | 0, or -1 with errno set |

## DirectoryRecord

```mach
pub rec DirectoryRecord {
    inode:         u64;
    seek_offset:   u64;
    record_length: u16;
    name_length:   u16;
    type_hint:     u8;
    name:          [1]u8;
}
```

variable-length native record, only the header and actual name extent are read

## ControlHeader

```mach
pub rec ControlHeader {
    length: u32;
    level:  i32;
    kind:   i32;
}
```

the header of one ancillary data item, the layout of struct cmsghdr

| Field | Type | |
| :--- | :--- | :--- |
| `length` | `u32` | bytes of the item, header included |
| `level` | `i32` | originating protocol |
| `kind` | `i32` | protocol-specific type |

## MessageHeader

```mach
pub rec MessageHeader {
    address:        *u8;
    address_length: u32;
    vectors:        *IoVector;
    vector_count:   i32;
    control:        *u8;
    control_length: u32;
    flags:          i32;
}
```

the argument of sendmsg and recvmsg, the layout of struct msghdr

| Field | Type | |
| :--- | :--- | :--- |
| `address` | `*u8` | peer address, or nil |
| `address_length` | `u32` | size of address |
| `vectors` | `*IoVector` | the gather or scatter list |
| `vector_count` | `i32` | entries in vectors |
| `control` | `*u8` | ancillary data buffer, or nil |
| `control_length` | `u32` | size of control |
| `flags` | `i32` | flags recvmsg reports |

### sendmsg

```mach
#[library("libsystem")]
pub ext fun sendmsg(fd: i32, message: *MessageHeader, flags: i32) i64
```

send a message with optional address and ancillary data

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `message` | what to send |
| `flags` | MSG_* bits |
| **returns** | bytes sent, or -1 with errno set |

### recvmsg

```mach
#[library("libsystem")]
pub ext fun recvmsg(fd: i32, message: *MessageHeader, flags: i32) i64
```

receive a message with its address and ancillary data

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `message` | the buffers to fill, whose lengths and flags are updated |
| `flags` | MSG_* bits |
| **returns** | bytes received, 0 at orderly end, or -1 with errno set |

## Termios

```mach
pub rec Termios {
    iflag:  u64;
    oflag:  u64;
    cflag:  u64;
    lflag:  u64;
    cc:     [20]u8;
    ispeed: u64;
    ospeed: u64;
}
```

public lp64 termios layout from darwin sys/termios.h

### tcgetattr

```mach
#[library("libsystem")]
pub ext fun tcgetattr(fd: i32, settings: *Termios) i32
```

read a terminal's settings

| Parameter | |
| :--- | :--- |
| `fd` | the terminal descriptor |
| `settings` | receives the settings |
| **returns** | 0, or -1 with errno set |

### tcsetattr

```mach
#[library("libsystem")]
pub ext fun tcsetattr(fd: i32, action: i32, settings: *Termios) i32
```

apply a terminal's settings

| Parameter | |
| :--- | :--- |
| `fd` | the terminal descriptor |
| `action` | when to apply them, such as TCSAFLUSH |
| `settings` | the settings |
| **returns** | 0, or -1 with errno set |

## DlInfo

```mach
pub rec DlInfo {
    fname: *u8;
    fbase: usize;
    sname: *u8;
    saddr: usize;
}
```

what dladdr reports of the image holding an address

| Field | Type | |
| :--- | :--- | :--- |
| `fname` | `*u8` | the image's path |
| `fbase` | `usize` | the image's mach header |
| `sname` | `*u8` | the nearest symbol's name, or nil |
| `saddr` | `usize` | the nearest symbol's address, or 0 |

### dladdr

```mach
#[library("libsystem")]
pub ext fun dladdr(addr: ptr, info: *DlInfo) i32
```

describe the image and nearest symbol holding an address

| Parameter | |
| :--- | :--- |
| `addr` | the address |
| `info` | receives the description |
| **returns** | nonzero on success, 0 when no image holds addr |

## ResourceLimit

```mach
pub rec ResourceLimit {
    current: u64;
    maximum: u64;
}
```

a resource limit, the layout of struct rlimit

| Field | Type | |
| :--- | :--- | :--- |
| `current` | `u64` | the soft limit in force |
| `maximum` | `u64` | the hard limit |

### getrlimit

```mach
#[library("libsystem")]
pub ext fun getrlimit(resource: i32, limit: *ResourceLimit) i32
```

read a resource limit

| Parameter | |
| :--- | :--- |
| `resource` | RLIMIT_* value |
| `limit` | receives the limit |
| **returns** | 0, or -1 with errno set |

### setrlimit

```mach
#[library("libsystem")]
pub ext fun setrlimit(resource: i32, limit: *ResourceLimit) i32
```

set a resource limit

| Parameter | |
| :--- | :--- |
| `resource` | RLIMIT_* value |
| `limit` | the limit |
| **returns** | 0, or -1 with errno set |

## Kevent

```mach
pub rec Kevent {
    ident:  usize;
    filter: i16;
    flags:  u16;
    fflags: u32;
    data:   isize;
    udata:  ptr;
}
```

pointer-only storage with the SDK field offsets and stronger alignment

### kevent

```mach
#[library("libsystem")]
pub ext fun kevent(queue: i32, changes: *Kevent, change_count: i32, events: *Kevent, capacity: i32, timeout: *std.system.os.shared.Timespec) i32
```

apply changes to an event queue and collect pending events

| Parameter | |
| :--- | :--- |
| `queue` | the kqueue descriptor |
| `changes` | filters to add, change or delete, or nil |
| `change_count` | entries in changes |
| `events` | receives pending events, or nil |
| `capacity` | entries events holds |
| `timeout` | how long to wait, or nil to wait indefinitely |
| **returns** | events stored, 0 on timeout, or -1 with errno set |

## Functions

### errno

```mach
pub fun errno() i32
```

the calling thread's current errno, as a positive number

only meaningful directly after a call whose return value already reported
failure - errno is not cleared by a successful call.

| Parameter | |
| :--- | :--- |
| **returns** | the current errno |

### clear_errno

```mach
pub fun clear_errno()
```

set the calling thread's errno to 0

a call that reports failure only through errno, such as readdir at its end,
needs errno cleared before it so a stale value is not read as its failure

### fail_errno

```mach
pub fun fail_errno() i64
```

the current errno negated, for a darwin OS primitive's return

the darwin backend's outward contract is "a negative errno on failure", which
is what it returned when it read the number straight out of a trap's result
register. this is the single place that contract is reconstructed from the
libSystem one.

a libSystem entry point that fails without setting errno is not supposed to
exist, but a zero here would be indistinguishable from success to every
caller, so it is reported as EINVAL rather than silently swallowed.

| Parameter | |
| :--- | :--- |
| **returns** | the negated errno, always \< 0 |

### sysctlbyname

```mach
#[library("libsystem")]
pub ext fun sysctlbyname(name: *u8, old: ptr, old_len: *usize, new: ptr, new_len: usize) i32
```

read or write a kernel state value by name

| Parameter | |
| :--- | :--- |
| `name` | null-terminated sysctl name |
| `old` | receives the current value, or nil |
| `old_len` | in, the capacity of old, out, the bytes written |
| `new` | the value to set, or nil |
| `new_len` | the size of new |
| **returns** | 0, or -1 with errno set |

### getentropy

```mach
#[library("libsystem")]
pub ext fun getentropy(data: ptr, length: usize) i32
```

fill a buffer with cryptographic random bytes

| Parameter | |
| :--- | :--- |
| `data` | destination buffer |
| `length` | bytes to fill, at most 256 |
| **returns** | 0, or -1 with errno set |

### mmap

```mach
#[library("libsystem")]
pub ext fun mmap(address: ptr, length: usize, protection: i32, flags: i32, fd: i32, offset: i64) ptr
```

map memory or a file into the address space

| Parameter | |
| :--- | :--- |
| `address` | placement hint, or nil |
| `length` | bytes to map |
| `protection` | PROT_* bits |
| `flags` | MAP_* bits |
| `fd` | the file to map, or -1 for an anonymous mapping |
| `offset` | page-aligned offset into the file |
| **returns** | the mapping, or MAP_FAILED (all bits one) with errno set |

### munmap

```mach
#[library("libsystem")]
pub ext fun munmap(address: ptr, length: usize) i32
```

unmap a region

| Parameter | |
| :--- | :--- |
| `address` | page-aligned start of the region |
| `length` | bytes to unmap |
| **returns** | 0, or -1 with errno set |

### mprotect

```mach
#[library("libsystem")]
pub ext fun mprotect(address: ptr, length: usize, protection: i32) i32
```

change the protection of a region

| Parameter | |
| :--- | :--- |
| `address` | page-aligned start of the region |
| `length` | region size in bytes |
| `protection` | PROT_* bits |
| **returns** | 0, or -1 with errno set |

### mlock

```mach
#[library("libsystem")]
pub ext fun mlock(address: ptr, length: usize) i32
```

lock a region into physical memory

| Parameter | |
| :--- | :--- |
| `address` | start of the region |
| `length` | region size in bytes |
| **returns** | 0, or -1 with errno set |

### munlock

```mach
#[library("libsystem")]
pub ext fun munlock(address: ptr, length: usize) i32
```

unlock a region mlock locked

| Parameter | |
| :--- | :--- |
| `address` | start of the region |
| `length` | region size in bytes |
| **returns** | 0, or -1 with errno set |

### madvise

```mach
#[library("libsystem")]
pub ext fun madvise(address: ptr, length: usize, advice: i32) i32
```

advise the kernel how a region will be accessed

| Parameter | |
| :--- | :--- |
| `address` | start of the region |
| `length` | region size in bytes |
| `advice` | MADV_* value |
| **returns** | 0, or -1 with errno set |

### msync

```mach
#[library("libsystem")]
pub ext fun msync(address: ptr, length: usize, flags: i32) i32
```

flush a shared file mapping to its file

| Parameter | |
| :--- | :--- |
| `address` | page-aligned start of the region |
| `length` | region size in bytes |
| `flags` | MS_* bits |
| **returns** | 0, or -1 with errno set |

### read

```mach
#[library("libsystem")]
pub ext fun read(fd: i32, buf: *u8, count: usize) i64
```

read bytes from a descriptor

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `buf` | destination buffer |
| `count` | most bytes to read |
| **returns** | bytes read, 0 at end of file, or -1 with errno set |

### write

```mach
#[library("libsystem")]
pub ext fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a descriptor

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `buf` | source bytes |
| `count` | bytes to write |
| **returns** | bytes written, or -1 with errno set |

### pread

```mach
#[library("libsystem")]
pub ext fun pread(fd: i32, buf: *u8, count: usize, offset: i64) i64
```

read bytes at a file offset without moving the descriptor offset

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `buf` | destination buffer |
| `count` | most bytes to read |
| `offset` | file offset to read from |
| **returns** | bytes read, 0 at end of file, or -1 with errno set |

### pwrite

```mach
#[library("libsystem")]
pub ext fun pwrite(fd: i32, buf: *u8, count: usize, offset: i64) i64
```

write bytes at a file offset without moving the descriptor offset

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `buf` | source bytes |
| `count` | bytes to write |
| `offset` | file offset to write at |
| **returns** | bytes written, or -1 with errno set |

### openat

```mach
#[library("libsystem")]
pub ext fun openat(dirfd: i32, path: *u8, flags: i32, ...) i32
```

`openat` is C-variadic: the mode argument is only read when the flags carry
O_CREAT. declaring it at a fixed arity of three would be silently wrong on
apple arm64, which passes the whole variadic tail on the stack while a fixed
third parameter would be lowered into x2 (see mach's doc/language/ext-fun.md).

### close

```mach
#[library("libsystem")]
pub ext fun close(fd: i32) i32
```

close a descriptor, which is released even when the close reports failure

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| **returns** | 0, or -1 with errno set |

### fsync

```mach
#[library("libsystem")]
pub ext fun fsync(fd: i32) i32
```

flush an open file's data and metadata to storage

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| **returns** | 0, or -1 with errno set |

### lseek

```mach
#[library("libsystem")]
pub ext fun lseek(fd: i32, offset: i64, whence: i32) i64
```

reposition a descriptor's offset

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `offset` | offset relative to whence |
| `whence` | SEEK_SET, SEEK_CUR or SEEK_END |
| **returns** | the resulting offset, or exactly -1 with errno set |

### fstat

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
#[library("libsystem")]
#[symbol("fstat$INODE64")]
pub ext fun fstat(fd: i32, st: *u8) i32
```

Otherwise:

```mach
#[library("libsystem")]
pub ext fun fstat(fd: i32, st: *u8) i32
```

read an open file's metadata

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `st` | receives a stat_t |
| **returns** | 0, or -1 with errno set |

### fstatfs

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
#[library("libsystem")]
#[symbol("fstatfs$INODE64")]
pub ext fun fstatfs(fd: i32, st: *u8) i32
```

Otherwise:

```mach
#[library("libsystem")]
pub ext fun fstatfs(fd: i32, st: *u8) i32
```

read the metadata of the filesystem holding an open file

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `st` | receives a struct statfs |
| **returns** | 0, or -1 with errno set |

### fstatat

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
#[library("libsystem")]
#[symbol("fstatat$INODE64")]
pub ext fun fstatat(dirfd: i32, path: *u8, st: *u8, flags: i32) i32
```

Otherwise:

```mach
#[library("libsystem")]
pub ext fun fstatat(dirfd: i32, path: *u8, st: *u8, flags: i32) i32
```

read a path's metadata relative to a directory

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor, or AT_FDCWD |
| `path` | null-terminated path |
| `st` | receives a stat_t |
| `flags` | AT_SYMLINK_NOFOLLOW or 0 |
| **returns** | 0, or -1 with errno set |

### flock

```mach
#[library("libsystem")]
pub ext fun flock(fd: i32, op: i32) i32
```

flock: advisory whole-file lock on an open descriptor

the lock is held by the open file description and darwin releases it when the
last descriptor on that description closes, including at process exit.

### unlinkat

```mach
#[library("libsystem")]
pub ext fun unlinkat(dirfd: i32, path: *u8, flags: i32) i32
```

remove a name relative to a directory

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor, or AT_FDCWD |
| `path` | null-terminated path |
| `flags` | AT_REMOVEDIR to remove an empty directory, or 0 |
| **returns** | 0, or -1 with errno set |

### renameat

```mach
#[library("libsystem")]
pub ext fun renameat(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i32
```

rename a path, each side relative to its own directory

| Parameter | |
| :--- | :--- |
| `olddir` | source directory descriptor, or AT_FDCWD |
| `oldpath` | source path |
| `newdir` | destination directory descriptor, or AT_FDCWD |
| `newpath` | destination path |
| **returns** | 0, or -1 with errno set |

### symlink

```mach
#[library("libsystem")]
pub ext fun symlink(target: *u8, linkpath: *u8) i32
```

create a symbolic link

| Parameter | |
| :--- | :--- |
| `target` | the path the link holds, stored as given |
| `linkpath` | the path of the link to create |
| **returns** | 0, or -1 with errno set |

### mkdirat

```mach
#[library("libsystem")]
pub ext fun mkdirat(dirfd: i32, path: *u8, mode: u32) i32
```

create a directory relative to a directory

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor, or AT_FDCWD |
| `path` | null-terminated path |
| `mode` | permission bits, before the umask |
| **returns** | 0, or -1 with errno set |

### faccessat

```mach
#[library("libsystem")]
pub ext fun faccessat(dirfd: i32, path: *u8, mode: i32, flags: i32) i32
```

check access to a path relative to a directory

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor, or AT_FDCWD |
| `path` | null-terminated path |
| `mode` | R_OK, W_OK and X_OK bits, or F_OK |
| `flags` | AT_* flags |
| **returns** | 0 when accessible, or -1 with errno set |

### getcwd

```mach
#[library("libsystem")]
pub ext fun getcwd(buf: *u8, size: usize) *u8
```

`getcwd(3)` replaces the open(".") + fcntl(F_GETPATH) dance the raw-syscall
backend needed. it takes a capacity, so the caller's buffer size is honoured
by the callee instead of being defended against afterwards.

| Parameter | |
| :--- | :--- |
| **returns** | `buf` on success, or nil with errno set (ERANGE when size is too small) |

### pipe

```mach
#[library("libsystem")]
pub ext fun pipe(fds: *i32) i32
```

create a unidirectional pipe

| Parameter | |
| :--- | :--- |
| `fds` | receives two descriptors, fds[0] the read end and fds[1] the write end |
| **returns** | 0, or -1 with errno set |

### socket

```mach
#[library("libsystem")]
pub ext fun socket(domain: i32, kind: i32, protocol: i32) i32
```

create a socket

| Parameter | |
| :--- | :--- |
| `domain` | AF_* family |
| `kind` | SOCK_* type |
| `protocol` | protocol, or 0 for the default |
| **returns** | the descriptor, or -1 with errno set |

### bind

```mach
#[library("libsystem")]
pub ext fun bind(fd: i32, address: *u8, length: u32) i32
```

bind a socket to a local address

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `address` | the sockaddr |
| `length` | size of the sockaddr |
| **returns** | 0, or -1 with errno set |

### listen

```mach
#[library("libsystem")]
pub ext fun listen(fd: i32, backlog: i32) i32
```

mark a socket as accepting connections

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `backlog` | most pending connections to queue |
| **returns** | 0, or -1 with errno set |

### accept

```mach
#[library("libsystem")]
pub ext fun accept(fd: i32, address: *u8, length: *u32) i32
```

accept a pending connection

| Parameter | |
| :--- | :--- |
| `fd` | the listening socket |
| `address` | receives the peer address, or nil |
| `length` | in, the capacity of address, out, its size |
| **returns** | the connected descriptor, or -1 with errno set |

### connect

```mach
#[library("libsystem")]
pub ext fun connect(fd: i32, address: *u8, length: u32) i32
```

connect a socket to a peer

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `address` | the peer sockaddr |
| `length` | size of the sockaddr |
| **returns** | 0, or -1 with errno set (EINPROGRESS on a nonblocking socket) |

### sendto

```mach
#[library("libsystem")]
pub ext fun sendto(fd: i32, buffer: *u8, length: usize, flags: i32, address: *u8, address_length: u32) i64
```

send bytes on a socket, to an address when it is unconnected

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `buffer` | source bytes |
| `length` | bytes to send |
| `flags` | MSG_* bits |
| `address` | destination sockaddr, or nil |
| `address_length` | size of address |
| **returns** | bytes sent, or -1 with errno set |

### recvfrom

```mach
#[library("libsystem")]
pub ext fun recvfrom(fd: i32, buffer: *u8, length: usize, flags: i32, address: *u8, address_length: *u32) i64
```

receive bytes from a socket, with the sender's address

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `buffer` | destination buffer |
| `length` | most bytes to receive |
| `flags` | MSG_* bits |
| `address` | receives the sender address, or nil |
| `address_length` | in, the capacity of address, out, its size, or nil |
| **returns** | bytes received, 0 at orderly end, or -1 with errno set |

### shutdown

```mach
#[library("libsystem")]
pub ext fun shutdown(fd: i32, how: i32) i32
```

shut down one or both directions of a socket

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `how` | SHUT_RD, SHUT_WR or SHUT_RDWR |
| **returns** | 0, or -1 with errno set |

### setsockopt

```mach
#[library("libsystem")]
pub ext fun setsockopt(fd: i32, level: i32, option: i32, value: *u8, length: u32) i32
```

set a socket option

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `level` | option level |
| `option` | option name |
| `value` | the option value |
| `length` | size of value |
| **returns** | 0, or -1 with errno set |

### getsockopt

```mach
#[library("libsystem")]
pub ext fun getsockopt(fd: i32, level: i32, option: i32, value: *u8, length: *u32) i32
```

read a socket option

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `level` | option level |
| `option` | option name |
| `value` | receives the option value |
| `length` | in, the capacity of value, out, its size |
| **returns** | 0, or -1 with errno set |

### getsockname

```mach
#[library("libsystem")]
pub ext fun getsockname(fd: i32, address: *u8, length: *u32) i32
```

read a socket's local address

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `address` | receives the sockaddr |
| `length` | in, the capacity of address, out, its size |
| **returns** | 0, or -1 with errno set |

### getpeername

```mach
#[library("libsystem")]
pub ext fun getpeername(fd: i32, address: *u8, length: *u32) i32
```

read a connected socket's peer address

| Parameter | |
| :--- | :--- |
| `fd` | the socket |
| `address` | receives the sockaddr |
| `length` | in, the capacity of address, out, its size |
| **returns** | 0, or -1 with errno set (ENOTCONN while unconnected) |

### writev

```mach
#[library("libsystem")]
pub ext fun writev(fd: i32, vectors: *IoVector, count: i32) i64
```

write a gather list to a descriptor

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `vectors` | the buffers, written in order |
| `count` | entries in vectors |
| **returns** | bytes written, or -1 with errno set |

### tcflush

```mach
#[library("libsystem")]
pub ext fun tcflush(fd: i32, queue: i32) i32
```

discard a terminal's queued data

| Parameter | |
| :--- | :--- |
| `fd` | the terminal descriptor |
| `queue` | which queue, such as TCIFLUSH |
| **returns** | 0, or -1 with errno set |

### signal

```mach
#[library("libsystem")]
pub ext fun signal(sig: i32, handler: usize) usize
```

install a process-wide signal disposition

signal(3) is sufficient for SIG_IGN and keeps darwin on its supported
libSystem surface instead of reproducing the platform's sigaction layout.

| Parameter | |
| :--- | :--- |
| **returns** | previous handler, or all-bits-one with errno set on failure |

### sigaction

```mach
#[library("libsystem")]
pub ext fun sigaction(sig: i32, action: *usize, previous: *usize) i32
```

examine or change a signal's disposition

| Parameter | |
| :--- | :--- |
| `sig` | the signal |
| `action` | the new struct sigaction, or nil |
| `previous` | receives the old struct sigaction, or nil |
| **returns** | 0, or -1 with errno set |

### raise

```mach
#[library("libsystem")]
pub ext fun raise(sig: i32) i32
```

send a signal to the calling thread

| Parameter | |
| :--- | :--- |
| `sig` | the signal |
| **returns** | 0, or nonzero on failure |

### clock_gettime

```mach
#[library("libsystem")]
pub ext fun clock_gettime(clock_id: i32, ts: *u8) i32
```

time

darwin has no `clock_gettime` BSD trap at all. the backend used to call
syscall 427 and read the result as a time; whatever that number is on current
macOS, it is not one - `now()` came back BELOW the unix epoch, and the three
`std.chrono.time` tests had been failing on darwin for as long as nothing was
running them.

`clock_gettime(3)` is real, public, and has shipped since macOS 10.12; it is
implemented in userspace over `mach_absolute_time()` and the commpage rather
than as a trap, which is exactly why looking for a syscall number for it was
never going to work. 10.12 is older than any macOS that runs on hardware
these targets support, so binding it moves no floor - unlike
`os_sync_wait_on_address`, which is why the thread layer went a different way.

`timespec` here is the same layout `shared.mach` declares; it is taken as
`*u8` only to keep this module free of a dependency back on that one.

### nanosleep

```mach
#[library("libsystem")]
pub ext fun nanosleep(req: *u8, rem: *u8) i32
```

suspend the calling thread for the requested interval

the old backend said "darwin has no nanosleep syscall" and reached for
`select` with a timeout instead. that is true of the TRAP table and false of
libSystem, which exports nanosleep(3). taking it also gets the remaining-time
argument, so an interrupted sleep can resume for what is left rather than
returning early or restarting the full interval.

| Parameter | |
| :--- | :--- |
| `req` | requested interval |
| `rem` | filled with the unslept remainder when interrupted; may be nil |
| **returns** | 0, or -1 with errno set (EINTR when a signal cut the sleep short) |

### pthread_create

```mach
#[library("libsystem")]
pub ext fun pthread_create(thread: *usize, attr: *u8, start: usize, arg: ptr) i32
```

`start` is a `void *(*)(void *)` passed as a bare address, matching how the
windows backend hands CreateThread its trampoline.

### pthread_join

```mach
#[library("libsystem")]
pub ext fun pthread_join(thread: usize, value: *usize) i32
```

wait for a thread to end and release it

| Parameter | |
| :--- | :--- |
| `thread` | the thread |
| `value` | receives its exit value, or nil |
| **returns** | 0, or an errno value |

### pthread_detach

```mach
#[library("libsystem")]
pub ext fun pthread_detach(thread: usize) i32
```

let a thread release itself when it ends, so it is never joined

| Parameter | |
| :--- | :--- |
| `thread` | the thread |
| **returns** | 0, or an errno value |

### pthread_setname_np

```mach
#[library("libsystem")]
pub ext fun pthread_setname_np(name: *u8) i32
```

name the calling thread

| Parameter | |
| :--- | :--- |
| `name` | null-terminated name |
| **returns** | 0, or an errno value |

### pthread_getname_np

```mach
#[library("libsystem")]
pub ext fun pthread_getname_np(thread: usize, name: *u8, len: usize) i32
```

read a thread's name

| Parameter | |
| :--- | :--- |
| `thread` | the thread |
| `name` | receives the null-terminated name |
| `len` | capacity of name |
| **returns** | 0, or an errno value |

### pthread_self

```mach
#[library("libsystem")]
pub ext fun pthread_self() usize
```

the calling thread

| Parameter | |
| :--- | :--- |
| **returns** | its pthread handle |

### pthread_threadid_np

```mach
#[library("libsystem")]
pub ext fun pthread_threadid_np(thread: usize, id: *u64) i32
```

a thread's system-wide unique id

| Parameter | |
| :--- | :--- |
| `thread` | the thread, or 0 for the calling thread |
| `id` | receives the id |
| **returns** | 0, or an errno value |

### pthread_get_stackaddr_np

```mach
#[library("libsystem")]
pub ext fun pthread_get_stackaddr_np(thread: usize) ptr
```

the top of thread's stack, its highest address plus one

### pthread_get_stacksize_np

```mach
#[library("libsystem")]
pub ext fun pthread_get_stacksize_np(thread: usize) usize
```

the size of a thread's stack

| Parameter | |
| :--- | :--- |
| `thread` | the thread |
| **returns** | the stack size in bytes |

### pthread_key_create

```mach
#[library("libsystem")]
pub ext fun pthread_key_create(key: *usize, destructor: usize) i32
```

a pthread_key_t is an unsigned long on darwin. std's key has no destructor

### pthread_setspecific

```mach
#[library("libsystem")]
pub ext fun pthread_setspecific(key: usize, value: ptr) i32
```

set the calling thread's value for a key

| Parameter | |
| :--- | :--- |
| `key` | a key pthread_key_create made |
| `value` | the value |
| **returns** | 0, or an errno value |

### pthread_getspecific

```mach
#[library("libsystem")]
pub ext fun pthread_getspecific(key: usize) ptr
```

the calling thread's value for a key

| Parameter | |
| :--- | :--- |
| `key` | a key pthread_key_create made |
| **returns** | the value, or nil when none is set |

### pthread_attr_init

```mach
#[library("libsystem")]
pub ext fun pthread_attr_init(attr: *u8) i32
```

initialize thread attributes to the defaults

| Parameter | |
| :--- | :--- |
| `attr` | PTHREAD_ATTR_BYTES of storage |
| **returns** | 0, or an errno value |

### pthread_attr_destroy

```mach
#[library("libsystem")]
pub ext fun pthread_attr_destroy(attr: *u8) i32
```

release thread attributes

| Parameter | |
| :--- | :--- |
| `attr` | attributes pthread_attr_init initialized |
| **returns** | 0, or an errno value |

### pthread_attr_setstacksize

```mach
#[library("libsystem")]
pub ext fun pthread_attr_setstacksize(attr: *u8, size: usize) i32
```

set the stack size threads created with attr get

| Parameter | |
| :--- | :--- |
| `attr` | the attributes |
| `size` | stack size in bytes |
| **returns** | 0, or an errno value |

### pthread_attr_setdetachstate

```mach
#[library("libsystem")]
pub ext fun pthread_attr_setdetachstate(attr: *u8, state: i32) i32
```

set whether threads created with attr start joinable or detached

| Parameter | |
| :--- | :--- |
| `attr` | the attributes |
| `state` | PTHREAD_CREATE_JOINABLE or PTHREAD_CREATE_DETACHED |
| **returns** | 0, or an errno value |

### pthread_mutex_init

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_init(m: *u8, attr: *u8) i32
```

initialize a mutex

| Parameter | |
| :--- | :--- |
| `m` | PTHREAD_MUTEX_BYTES of storage |
| `attr` | mutex attributes, or nil for the defaults |
| **returns** | 0, or an errno value |

### pthread_mutex_lock

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_lock(m: *u8) i32
```

lock a mutex, blocking until it is free

| Parameter | |
| :--- | :--- |
| `m` | the mutex |
| **returns** | 0, or an errno value |

### pthread_mutex_unlock

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_unlock(m: *u8) i32
```

unlock a mutex the caller holds

| Parameter | |
| :--- | :--- |
| `m` | the mutex |
| **returns** | 0, or an errno value |

### pthread_cond_init

```mach
#[library("libsystem")]
pub ext fun pthread_cond_init(c: *u8, attr: *u8) i32
```

initialize a condition variable

| Parameter | |
| :--- | :--- |
| `c` | PTHREAD_COND_BYTES of storage |
| `attr` | condition attributes, or nil for the defaults |
| **returns** | 0, or an errno value |

### pthread_cond_wait

```mach
#[library("libsystem")]
pub ext fun pthread_cond_wait(c: *u8, m: *u8) i32
```

release m and wait on c, holding m again on return

| Parameter | |
| :--- | :--- |
| `c` | the condition variable |
| `m` | the mutex the caller holds |
| **returns** | 0, or an errno value |

### pthread_cond_timedwait_relative_np

```mach
#[library("libsystem")]
pub ext fun pthread_cond_timedwait_relative_np(c: *u8, m: *u8, relative: *u8) i32
```

release m and wait on c for at most a relative interval, holding m again on return

| Parameter | |
| :--- | :--- |
| `c` | the condition variable |
| `m` | the mutex the caller holds |
| `relative` | a timespec interval |
| **returns** | 0, ETIMEDOUT when the interval passed, or another errno value |

### pthread_cond_broadcast

```mach
#[library("libsystem")]
pub ext fun pthread_cond_broadcast(c: *u8) i32
```

wake every thread waiting on a condition variable

| Parameter | |
| :--- | :--- |
| `c` | the condition variable |
| **returns** | 0, or an errno value |

### pthread_once

```mach
#[library("libsystem")]
pub ext fun pthread_once(once: *u8, init: usize) i32
```

`init` is a `void (*)(void)` passed as a bare address.

### umask

```mach
#[library("libsystem")]
pub ext fun umask(mask: u32) u32
```

set the file-mode creation mask, returning the previous one

cannot fail and does not touch errno. imported so a test can pin the mask to
a known value and then assert a created file's mode EXACTLY, rather than
asserting some umask-dependent subset of it - which is what makes the mode
assertion able to catch a dropped variadic argument.

### fcntl

```mach
#[library("libsystem")]
pub ext fun fcntl(fd: i32, cmd: i32, ...) i32
```

`fcntl` is C-variadic. the two-argument commands (F_GETFL, F_GETFD) pass no
tail at all and are called with none; F_SETFD / F_SETFL / F_DUPFD pass a
single int. every tail this module ever passes is an int or a pointer, never
a float, which is what keeps `AL` at zero on the SysV x86_64 leg.

### fchmod

```mach
#[library("libsystem")]
pub ext fun fchmod(fd: i32, mode: u32) i32
```

set a file's permission bits through an open descriptor

| Parameter | |
| :--- | :--- |
| `fd` | the descriptor |
| `mode` | permission bits |
| **returns** | 0, or -1 with errno set |

### fchmodat

```mach
#[library("libsystem")]
pub ext fun fchmodat(dirfd: i32, name: *u8, mode: u32, flags: i32) i32
```

set the permission bits of a path relative to a directory

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor, or AT_FDCWD |
| `name` | null-terminated path |
| `mode` | permission bits |
| `flags` | AT_SYMLINK_NOFOLLOW or 0 |
| **returns** | 0, or -1 with errno set |

### fork

```mach
#[library("libsystem")]
pub ext fun fork() i32
```

create a child process duplicating the caller

| Parameter | |
| :--- | :--- |
| **returns** | the child pid in the parent, 0 in the child, or -1 with errno set |

### vfork

```mach
#[library("libsystem")]
pub ext fun vfork() i32
```

create a child process through vfork

| Parameter | |
| :--- | :--- |
| **returns** | the child pid in the parent, 0 in the child, or -1 with errno set |

### execve

```mach
#[library("libsystem")]
pub ext fun execve(path: *u8, argv: **u8, envp: **u8) i32
```

replace the process image, returning only on failure

| Parameter | |
| :--- | :--- |
| `path` | the program |
| `argv` | null-terminated argument array |
| `envp` | null-terminated environment array |
| **returns** | -1 with errno set |

### wait4

```mach
#[library("libsystem")]
pub ext fun wait4(pid: i32, status: *i32, options: i32, rusage: *u8) i32
```

wait for a child to change state

| Parameter | |
| :--- | :--- |
| `pid` | the child, or -1 for any child |
| `status` | receives the raw wait status |
| `options` | WNOHANG, WUNTRACED, WCONTINUED |
| `rusage` | receives a struct rusage, or nil |
| **returns** | the child's pid, 0 under WNOHANG when nothing changed, or -1 with errno set |

### waitid

```mach
#[library("libsystem")]
pub ext fun waitid(idtype: i32, id: u32, info: *u8, options: i32) i32
```

`info` is a `siginfo_t *` (104 bytes on darwin); the caller passes storage
and never reads it, so it is taken as bytes

### kill

```mach
#[library("libsystem")]
pub ext fun kill(pid: i32, sig: i32) i32
```

send a signal to a process, or to a process group for a negated pid

| Parameter | |
| :--- | :--- |
| `pid` | the target |
| `sig` | the signal, or 0 to check the target exists |
| **returns** | 0, or -1 with errno set |

### getpid

```mach
#[library("libsystem")]
pub ext fun getpid() i32
```

the calling process's id

| Parameter | |
| :--- | :--- |
| **returns** | the pid |

### setpgid

```mach
#[library("libsystem")]
pub ext fun setpgid(pid: i32, pgid: i32) i32
```

set the process group of a process

| Parameter | |
| :--- | :--- |
| `pid` | the process, or 0 for the caller |
| `pgid` | the group, or 0 to make pid its own group's leader |
| **returns** | 0, or -1 with errno set |

### getpgid

```mach
#[library("libsystem")]
pub ext fun getpgid(pid: i32) i32
```

the process group of a process

| Parameter | |
| :--- | :--- |
| `pid` | the process, or 0 for the caller |
| **returns** | the group id, or -1 with errno set |

### dup2

```mach
#[library("libsystem")]
pub ext fun dup2(from: i32, to: i32) i32
```

make to name what from names, closing what to named before

| Parameter | |
| :--- | :--- |
| `from` | an open descriptor |
| `to` | the descriptor number to take over |
| **returns** | to, or -1 with errno set |

### chdir

```mach
#[library("libsystem")]
pub ext fun chdir(path: *u8) i32
```

change the working directory

| Parameter | |
| :--- | :--- |
| `path` | null-terminated path |
| **returns** | 0, or -1 with errno set |

### _exit

```mach
#[library("libsystem")]
#[noreturn]
pub ext fun _exit(code: i32)
```

end the process at once without running atexit handlers

| Parameter | |
| :--- | :--- |
| `code` | the exit code |

### kqueue

```mach
#[library("libsystem")]
pub ext fun kqueue() i32
```

create a kernel event queue

| Parameter | |
| :--- | :--- |
| **returns** | its descriptor, or -1 with errno set |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `F_DUPFD_CLOEXEC` | `i32` | `67` |  |
| `MSG_PEEK` | `i32` | `0x2` |  |
| `MSG_DONTWAIT` | `i32` | `0x80` |  |
| `MSG_TRUNC` | `i32` | `0x10` |  |
| `MSG_CTRUNC` | `i32` | `0x20` |  |
| `TCSAFLUSH` | `i32` | `2` |  |
| `TCIFLUSH` | `i32` | `1` |  |
| `ICANON` | `u64` | `0x0100` |  |
| `ECHO` | `u64` | `0x0008` |  |
| `VMIN` | `usize` | `16` |  |
| `VTIME` | `usize` | `17` |  |
| `PTHREAD_MUTEX_BYTES` | `usize` | `64` | opaque pthread object sizes, from \<sys/_pthread/_pthread_types.h> on LP64 |
| `PTHREAD_COND_BYTES` | `usize` | `48` |  |
| `PTHREAD_ATTR_BYTES` | `usize` | `64` |  |
| `PTHREAD_ONCE_BYTES` | `usize` | `16` |  |
| `PTHREAD_CREATE_JOINABLE` | `i32` | `1` | pthread_attr_setdetachstate states (\<pthread.h>) |
| `PTHREAD_CREATE_DETACHED` | `i32` | `2` |  |
| `P_PID` | `i32` | `1` | waitid selectors and options (\<sys/wait.h>) |
| `WEXITED` | `i32` | `0x4` |  |
| `WNOWAIT` | `i32` | `0x20` |  |
| `RLIMIT_NOFILE` | `i32` | `8` | resource limits (\<sys/resource.h>); `rlim_t` is u64 on LP64 |

## Forwards

### IoVector

Forwards [`std.system.os.shared.IoVector`](../shared.md#iovector).

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

one buffer of a gather write, laid out as struct iovec on linux and darwin
and as wasi's ciovec

