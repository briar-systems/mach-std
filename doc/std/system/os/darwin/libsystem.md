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
| [`IoVector`](#iovector) | `rec` |  |
| [`ControlHeader`](#controlheader) | `rec` |  |
| [`MessageHeader`](#messageheader) | `rec` |  |
| [`Termios`](#termios) | `rec` | public lp64 termios layout from darwin sys/termios.h |
| [`DlInfo`](#dlinfo) | `rec` | what dladdr reports of the image holding an address |
| [`ResourceLimit`](#resourcelimit) | `rec` |  |
| [`Kevent`](#kevent) | `rec` | pointer-only storage with the SDK field offsets and stronger alignment |

| On `DirectoryStream` | |
| :--- | :--- |
| [`fdopendir`](#fdopendir), [`readdir`](#readdir), [`closedir`](#closedir) | |

| On `IoVector` | |
| :--- | :--- |
| [`writev`](#writev) | |

| On `MessageHeader` | |
| :--- | :--- |
| [`sendmsg`](#sendmsg), [`recvmsg`](#recvmsg) | |

| On `Termios` | |
| :--- | :--- |
| [`tcgetattr`](#tcgetattr), [`tcsetattr`](#tcsetattr) | |

| On `DlInfo` | |
| :--- | :--- |
| [`dladdr`](#dladdr) | |

| On `ResourceLimit` | |
| :--- | :--- |
| [`getrlimit`](#getrlimit), [`setrlimit`](#setrlimit) | |

| On `Kevent` | |
| :--- | :--- |
| [`kevent`](#kevent-1) | |

| Functions | |
| :--- | :--- |
| [`errno`](#errno) | the calling thread's current errno, as a positive number |
| [`clear_errno`](#clear_errno) | |
| [`fail_errno`](#fail_errno) | the current errno negated, for a darwin OS primitive's return |
| [`sysctlbyname`](#sysctlbyname), [`getentropy`](#getentropy), [`mmap`](#mmap), [`munmap`](#munmap), [`mprotect`](#mprotect), [`mlock`](#mlock), [`munlock`](#munlock), [`madvise`](#madvise), [`msync`](#msync), [`read`](#read), [`write`](#write), [`pread`](#pread), [`pwrite`](#pwrite) | |
| [`openat`](#openat) | `openat` is C-variadic: the mode argument is only read when the flags carry O_CREAT |
| [`close`](#close), [`fsync`](#fsync), [`lseek`](#lseek) | |
| [`fstat`](#fstat) | the stat family carries the `$INODE64` suffix on x86_64 only; see the module header |
| [`fstatfs`](#fstatfs) | the stat family carries the `$INODE64` suffix on x86_64 only; see the module header |
| [`fstatat`](#fstatat) | the stat family carries the `$INODE64` suffix on x86_64 only; see the module header |
| [`flock`](#flock) | flock: advisory whole-file lock on an open descriptor |
| [`unlinkat`](#unlinkat), [`renameat`](#renameat), [`symlink`](#symlink), [`mkdirat`](#mkdirat), [`faccessat`](#faccessat) | |
| [`getcwd`](#getcwd) | `getcwd(3)` replaces the open(".") + fcntl(F_GETPATH) dance the raw-syscall backend needed |
| [`pipe`](#pipe), [`socket`](#socket), [`bind`](#bind), [`listen`](#listen), [`accept`](#accept), [`connect`](#connect), [`sendto`](#sendto), [`recvfrom`](#recvfrom), [`shutdown`](#shutdown), [`setsockopt`](#setsockopt), [`getsockopt`](#getsockopt), [`getsockname`](#getsockname), [`getpeername`](#getpeername), [`tcflush`](#tcflush) | |
| [`signal`](#signal) | install a process-wide signal disposition |
| [`sigaction`](#sigaction), [`raise`](#raise) | |
| [`clock_gettime`](#clock_gettime) | time |
| [`nanosleep`](#nanosleep) | suspend the calling thread for the requested interval |
| [`pthread_create`](#pthread_create) | `start` is a `void *(*)(void *)` passed as a bare address, matching how the windows backend hands CreateThread its trampoline |
| [`pthread_join`](#pthread_join), [`pthread_detach`](#pthread_detach), [`pthread_setname_np`](#pthread_setname_np), [`pthread_getname_np`](#pthread_getname_np), [`pthread_self`](#pthread_self), [`pthread_threadid_np`](#pthread_threadid_np) | |
| [`pthread_get_stackaddr_np`](#pthread_get_stackaddr_np) | the top of thread's stack, its highest address plus one |
| [`pthread_get_stacksize_np`](#pthread_get_stacksize_np) | |
| [`pthread_key_create`](#pthread_key_create) | a pthread_key_t is an unsigned long on darwin |
| [`pthread_setspecific`](#pthread_setspecific), [`pthread_getspecific`](#pthread_getspecific), [`pthread_attr_init`](#pthread_attr_init), [`pthread_attr_destroy`](#pthread_attr_destroy), [`pthread_attr_setstacksize`](#pthread_attr_setstacksize), [`pthread_attr_setdetachstate`](#pthread_attr_setdetachstate), [`pthread_mutex_init`](#pthread_mutex_init), [`pthread_mutex_lock`](#pthread_mutex_lock), [`pthread_mutex_unlock`](#pthread_mutex_unlock), [`pthread_cond_init`](#pthread_cond_init), [`pthread_cond_wait`](#pthread_cond_wait), [`pthread_cond_timedwait_relative_np`](#pthread_cond_timedwait_relative_np), [`pthread_cond_broadcast`](#pthread_cond_broadcast) | |
| [`pthread_once`](#pthread_once) | `init` is a `void (*)(void)` passed as a bare address |
| [`umask`](#umask) | set the file-mode creation mask, returning the previous one |
| [`fcntl`](#fcntl) | `fcntl` is C-variadic |
| [`fchmod`](#fchmod), [`fchmodat`](#fchmodat), [`fork`](#fork), [`vfork`](#vfork), [`execve`](#execve), [`wait4`](#wait4) | |
| [`waitid`](#waitid) | `info` is a `siginfo_t *` (104 bytes on darwin); the caller passes storage and never reads it, so it is taken as bytes |
| [`kill`](#kill), [`getpid`](#getpid), [`setpgid`](#setpgid), [`getpgid`](#getpgid), [`dup2`](#dup2), [`chdir`](#chdir), [`_exit`](#_exit), [`kqueue`](#kqueue) | |

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

### closedir

```mach
#[library("libsystem")]
pub ext fun closedir(stream: DirectoryStream) i32
```

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

## IoVector

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

### writev

```mach
#[library("libsystem")]
pub ext fun writev(fd: i32, vectors: *IoVector, count: i32) i64
```

## ControlHeader

```mach
pub rec ControlHeader {
    length: u32;
    level:  i32;
    kind:   i32;
}
```

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

### sendmsg

```mach
#[library("libsystem")]
pub ext fun sendmsg(fd: i32, message: *MessageHeader, flags: i32) i64
```

### recvmsg

```mach
#[library("libsystem")]
pub ext fun recvmsg(fd: i32, message: *MessageHeader, flags: i32) i64
```

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

### tcsetattr

```mach
#[library("libsystem")]
pub ext fun tcsetattr(fd: i32, action: i32, settings: *Termios) i32
```

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

## ResourceLimit

```mach
pub rec ResourceLimit {
    current: u64;
    maximum: u64;
}
```

### getrlimit

```mach
#[library("libsystem")]
pub ext fun getrlimit(resource: i32, limit: *ResourceLimit) i32
```

### setrlimit

```mach
#[library("libsystem")]
pub ext fun setrlimit(resource: i32, limit: *ResourceLimit) i32
```

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

### getentropy

```mach
#[library("libsystem")]
pub ext fun getentropy(data: ptr, length: usize) i32
```

### mmap

```mach
#[library("libsystem")]
pub ext fun mmap(address: ptr, length: usize, protection: i32, flags: i32, fd: i32, offset: i64) ptr
```

### munmap

```mach
#[library("libsystem")]
pub ext fun munmap(address: ptr, length: usize) i32
```

### mprotect

```mach
#[library("libsystem")]
pub ext fun mprotect(address: ptr, length: usize, protection: i32) i32
```

### mlock

```mach
#[library("libsystem")]
pub ext fun mlock(address: ptr, length: usize) i32
```

### munlock

```mach
#[library("libsystem")]
pub ext fun munlock(address: ptr, length: usize) i32
```

### madvise

```mach
#[library("libsystem")]
pub ext fun madvise(address: ptr, length: usize, advice: i32) i32
```

### msync

```mach
#[library("libsystem")]
pub ext fun msync(address: ptr, length: usize, flags: i32) i32
```

### read

```mach
#[library("libsystem")]
pub ext fun read(fd: i32, buf: *u8, count: usize) i64
```

### write

```mach
#[library("libsystem")]
pub ext fun write(fd: i32, buf: *u8, count: usize) i64
```

### pread

```mach
#[library("libsystem")]
pub ext fun pread(fd: i32, buf: *u8, count: usize, offset: i64) i64
```

### pwrite

```mach
#[library("libsystem")]
pub ext fun pwrite(fd: i32, buf: *u8, count: usize, offset: i64) i64
```

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

### fsync

```mach
#[library("libsystem")]
pub ext fun fsync(fd: i32) i32
```

### lseek

```mach
#[library("libsystem")]
pub ext fun lseek(fd: i32, offset: i64, whence: i32) i64
```

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

the stat family carries the `$INODE64` suffix on x86_64 only; see the module
header. the two arms are mutually exclusive, so the duplicate-attribution
check does not apply to them.

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

the stat family carries the `$INODE64` suffix on x86_64 only; see the module
header. the two arms are mutually exclusive, so the duplicate-attribution
check does not apply to them.

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

the stat family carries the `$INODE64` suffix on x86_64 only; see the module
header. the two arms are mutually exclusive, so the duplicate-attribution
check does not apply to them.

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

### renameat

```mach
#[library("libsystem")]
pub ext fun renameat(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i32
```

### symlink

```mach
#[library("libsystem")]
pub ext fun symlink(target: *u8, linkpath: *u8) i32
```

### mkdirat

```mach
#[library("libsystem")]
pub ext fun mkdirat(dirfd: i32, path: *u8, mode: u32) i32
```

### faccessat

```mach
#[library("libsystem")]
pub ext fun faccessat(dirfd: i32, path: *u8, mode: i32, flags: i32) i32
```

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

### socket

```mach
#[library("libsystem")]
pub ext fun socket(domain: i32, kind: i32, protocol: i32) i32
```

### bind

```mach
#[library("libsystem")]
pub ext fun bind(fd: i32, address: *u8, length: u32) i32
```

### listen

```mach
#[library("libsystem")]
pub ext fun listen(fd: i32, backlog: i32) i32
```

### accept

```mach
#[library("libsystem")]
pub ext fun accept(fd: i32, address: *u8, length: *u32) i32
```

### connect

```mach
#[library("libsystem")]
pub ext fun connect(fd: i32, address: *u8, length: u32) i32
```

### sendto

```mach
#[library("libsystem")]
pub ext fun sendto(fd: i32, buffer: *u8, length: usize, flags: i32, address: *u8, address_length: u32) i64
```

### recvfrom

```mach
#[library("libsystem")]
pub ext fun recvfrom(fd: i32, buffer: *u8, length: usize, flags: i32, address: *u8, address_length: *u32) i64
```

### shutdown

```mach
#[library("libsystem")]
pub ext fun shutdown(fd: i32, how: i32) i32
```

### setsockopt

```mach
#[library("libsystem")]
pub ext fun setsockopt(fd: i32, level: i32, option: i32, value: *u8, length: u32) i32
```

### getsockopt

```mach
#[library("libsystem")]
pub ext fun getsockopt(fd: i32, level: i32, option: i32, value: *u8, length: *u32) i32
```

### getsockname

```mach
#[library("libsystem")]
pub ext fun getsockname(fd: i32, address: *u8, length: *u32) i32
```

### getpeername

```mach
#[library("libsystem")]
pub ext fun getpeername(fd: i32, address: *u8, length: *u32) i32
```

### tcflush

```mach
#[library("libsystem")]
pub ext fun tcflush(fd: i32, queue: i32) i32
```

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

### raise

```mach
#[library("libsystem")]
pub ext fun raise(sig: i32) i32
```

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

### pthread_detach

```mach
#[library("libsystem")]
pub ext fun pthread_detach(thread: usize) i32
```

### pthread_setname_np

```mach
#[library("libsystem")]
pub ext fun pthread_setname_np(name: *u8) i32
```

### pthread_getname_np

```mach
#[library("libsystem")]
pub ext fun pthread_getname_np(thread: usize, name: *u8, len: usize) i32
```

### pthread_self

```mach
#[library("libsystem")]
pub ext fun pthread_self() usize
```

### pthread_threadid_np

```mach
#[library("libsystem")]
pub ext fun pthread_threadid_np(thread: usize, id: *u64) i32
```

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

### pthread_getspecific

```mach
#[library("libsystem")]
pub ext fun pthread_getspecific(key: usize) ptr
```

### pthread_attr_init

```mach
#[library("libsystem")]
pub ext fun pthread_attr_init(attr: *u8) i32
```

### pthread_attr_destroy

```mach
#[library("libsystem")]
pub ext fun pthread_attr_destroy(attr: *u8) i32
```

### pthread_attr_setstacksize

```mach
#[library("libsystem")]
pub ext fun pthread_attr_setstacksize(attr: *u8, size: usize) i32
```

### pthread_attr_setdetachstate

```mach
#[library("libsystem")]
pub ext fun pthread_attr_setdetachstate(attr: *u8, state: i32) i32
```

### pthread_mutex_init

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_init(m: *u8, attr: *u8) i32
```

### pthread_mutex_lock

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_lock(m: *u8) i32
```

### pthread_mutex_unlock

```mach
#[library("libsystem")]
pub ext fun pthread_mutex_unlock(m: *u8) i32
```

### pthread_cond_init

```mach
#[library("libsystem")]
pub ext fun pthread_cond_init(c: *u8, attr: *u8) i32
```

### pthread_cond_wait

```mach
#[library("libsystem")]
pub ext fun pthread_cond_wait(c: *u8, m: *u8) i32
```

### pthread_cond_timedwait_relative_np

```mach
#[library("libsystem")]
pub ext fun pthread_cond_timedwait_relative_np(c: *u8, m: *u8, relative: *u8) i32
```

### pthread_cond_broadcast

```mach
#[library("libsystem")]
pub ext fun pthread_cond_broadcast(c: *u8) i32
```

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

### fchmodat

```mach
#[library("libsystem")]
pub ext fun fchmodat(dirfd: i32, name: *u8, mode: u32, flags: i32) i32
```

### fork

```mach
#[library("libsystem")]
pub ext fun fork() i32
```

### vfork

```mach
#[library("libsystem")]
pub ext fun vfork() i32
```

### execve

```mach
#[library("libsystem")]
pub ext fun execve(path: *u8, argv: **u8, envp: **u8) i32
```

### wait4

```mach
#[library("libsystem")]
pub ext fun wait4(pid: i32, status: *i32, options: i32, rusage: *u8) i32
```

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

### getpid

```mach
#[library("libsystem")]
pub ext fun getpid() i32
```

### setpgid

```mach
#[library("libsystem")]
pub ext fun setpgid(pid: i32, pgid: i32) i32
```

### getpgid

```mach
#[library("libsystem")]
pub ext fun getpgid(pid: i32) i32
```

### dup2

```mach
#[library("libsystem")]
pub ext fun dup2(from: i32, to: i32) i32
```

### chdir

```mach
#[library("libsystem")]
pub ext fun chdir(path: *u8) i32
```

### _exit

```mach
#[library("libsystem")]
pub ext fun _exit(code: i32)
```

### kqueue

```mach
#[library("libsystem")]
pub ext fun kqueue() i32
```

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

