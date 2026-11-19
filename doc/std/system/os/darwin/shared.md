[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [darwin](README.md) / **shared**

# std.system.os.darwin.shared

code shared across all darwin ISA implementations

contains types, constants and every OS primitive, each a call into
libSystem (std.system.os.darwin.libsystem): no darwin primitive issues a
trap, because apple promises none. arch-specific modules provide only
page_size and pipe.

Source: [`src/system/os/darwin/shared.mach`](../../../../../src/system/os/darwin/shared.mach)

Uses types from [`std.system.cpu.features`](../../cpu/features.md), [`std.system.file_identity`](../../file_identity.md), [`std.system.os.darwin.libsystem`](libsystem.md), [`std.system.os.shared`](../shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`stat_t`](#stat_t) | `rec` | darwin stat64 structure for file metadata |
| [`timespec`](#timespec) | `rec` | time specification with seconds and nanoseconds |
| [`DirectoryCursor`](#directorycursor) | `rec` |  |
| [`IoCompletion`](#iocompletion) | `rec` | context is opaque to the OS and zero is reserved for the runtime wake source source: the id of the source that registered the context, 0 for a wake |

| On `stat_t` | |
| :--- | :--- |
| [`stat`](#stat), [`stat_path`](#stat_path) | |
| [`stat_mode`](#stat_mode) | read the type/permission bits from a filled stat buffer as a 32-bit word |

| On `timespec` | |
| :--- | :--- |
| [`clock_gettime`](#clock_gettime) | read a clock into a timespec |

| On `DirectoryCursor` | |
| :--- | :--- |
| [`directory_init`](#directory_init) | fd and its aliases lend exclusive enumeration and seek access until close |
| [`directory_next`](#directory_next) | |
| [`directory_dnit`](#directory_dnit) | closedir consumes its stream even when the underlying close fails |

| On `IoCompletion` | |
| :--- | :--- |
| [`io_queue_poll`](#io_queue_poll) | |

| Functions | |
| :--- | :--- |
| [`terminate`](#terminate) | exit the process with the given code |
| [`abort`](#abort) | abort the process immediately with exit code 255 |
| [`allocate`](#allocate), [`deallocate`](#deallocate) | |
| [`map_secret`](#map_secret) | map storage for secret-welded data: span locked bytes between two inaccessible guard pages, page aligned and zero-filled |
| [`reallocate`](#reallocate) | darwin has no mremap, allocate new, copy, free old |
| [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`environ`](#environ) | pointer to the environment captured by the runtime at program start (null-terminated array of "NAME=value" strings) |
| [`read`](#read), [`write`](#write) | |
| [`read_at`](#read_at) | positioned file access does not mutate the descriptor offset |
| [`write_at`](#write_at) | |
| [`open`](#open) | open a path relative to a directory descriptor |
| [`close`](#close) | close a descriptor |
| [`sync_fd`](#sync_fd) | flush an open file's data and metadata to its backing storage |
| [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at), [`publication_capabilities`](#publication_capabilities) | |
| [`file_identity`](#file_identity) | observational ids do not retain an object after this call |
| [`retain_identity_at`](#retain_identity_at) | o_evtonly retains identity without data i/o after explicit read authorization |
| [`identity_at`](#identity_at), [`unlink`](#unlink) | |
| [`lock_fd`](#lock_fd) | flock: take or release an advisory whole-file lock on an open descriptor |
| [`rename`](#rename) | |
| [`symlink`](#symlink) | create a symbolic link at linkpath pointing to target |
| [`make_dir`](#make_dir), [`access`](#access) | |
| [`seek`](#seek) | reposition a descriptor's offset |
| [`fd_flags`](#fd_flags) | read a descriptor's descriptor-level flags (FD_CLOEXEC) |
| [`set_fd_flags`](#set_fd_flags) | set a descriptor's descriptor-level flags |
| [`file_flags`](#file_flags) | read a descriptor's file-status flags (access mode, O_APPEND, O_NONBLOCK) |
| [`set_file_flags`](#set_file_flags) | set a descriptor's file-status flags |
| [`fork`](#fork) | create a child process by duplicating the caller |
| [`vfork`](#vfork) | create a child process through vfork(2) |
| [`exec`](#exec) | replace the calling process image; returns only on failure |
| [`wait`](#wait) | failures and no-event results leave the caller's status unchanged |
| [`wait_pid`](#wait_pid) | |
| [`terminate_child`](#terminate_child) | forcefully stop a spawned child without reaping it |
| [`setpgid`](#setpgid) | setpgid: set (or join) the process group ID of a process |
| [`getpgid`](#getpgid) | getpgid: read the process group ID of a process |
| [`terminate_group`](#terminate_group) | signal every process in a group without reaping any of them |
| [`kill_group`](#kill_group) | forcefully stop every process in a group without reaping any of them |
| [`probe_group`](#probe_group) | whether any process is left in a group, without signalling it |
| [`process_watch`](#process_watch) | make the end of the child `pid` a readiness event on `queue`, so the queue's wait returns once the child ends: a one-shot EVFILT_PROC NOTE_EXIT filter |
| [`process_unwatch`](#process_unwatch) | release a watch process_watch made, whether or not it fired |
| [`spawn`](#spawn) | create a child process running the given program |
| [`spawn_grouped`](#spawn_grouped) | create a child process running the given program, placed as the leader of its own new process group (see spawn_redirected_in_grouped) |
| [`spawn_in`](#spawn_in) | create a child process running the given program from `cwd` |
| [`spawn_redirected`](#spawn_redirected) | spawn a child with its standard streams bound to caller-supplied descriptors |
| [`spawn_redirected_grouped`](#spawn_redirected_grouped) | spawn a child with its standard streams bound to caller-supplied descriptors, placed as the leader of its own new process group (see spawn_redirected_in_grouped) |
| [`spawn_redirected_in`](#spawn_redirected_in) | spawn a child with redirected streams and an explicit working directory |
| [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | spawn a child with redirected streams and an explicit working directory, placed as the leader of its own new process group |
| [`getpid`](#getpid) | return the current process ID |
| [`open_file_limit`](#open_file_limit) | read this process's open-file limit |
| [`set_open_file_limit`](#set_open_file_limit) | set this process's open-file limit |
| [`ignore_sigpipe`](#ignore_sigpipe) | ignore SIGPIPE for this process |
| [`sleep`](#sleep) | suspend execution for the given number of nanoseconds |
| [`cpu_count`](#cpu_count) | the currently active processor count reads hw.activecpu, with a minimum of one if the query fails |
| [`cpu_features`](#cpu_features) | the running processor's instruction-set extensions |
| [`cpu_dit`](#cpu_dit) | whether the processor provides the data-independent-timing mode |
| [`thread_affinity`](#thread_affinity) | darwin has no hard CPU affinity: THREAD_AFFINITY_POLICY is a scheduling hint over tags, not a CPU set, so neither affinity primitive is offered |
| [`set_thread_affinity`](#set_thread_affinity) | darwin has no hard CPU affinity, so a thread cannot be pinned |
| [`getcwd`](#getcwd) | get the current working directory |
| [`getenv`](#getenv) | look up an environment variable by name |
| [`temp_dir`](#temp_dir) | the directory designated for temporary files: $TMPDIR, else "/tmp" |
| [`thread_block_enter`](#thread_block_enter) | install block as the calling thread's |
| [`thread_block`](#thread_block) | the calling thread's block, read from its pthread TSD without a system call |
| [`stack_bounds`](#stack_bounds) | the calling thread's stack bounds, recorded in its block when it was installed, or asked of libpthread on a thread std did not create |
| [`thread_exit_wipe`](#thread_exit_wipe) | wipe the calling thread's thread-local block as the thread ends |
| [`thread_spawn`](#thread_spawn) | create a joinable pthread and release it only through join or detach |
| [`thread_join`](#thread_join), [`thread_detach`](#thread_detach), [`thread_current_id`](#thread_current_id), [`thread_current_name`](#thread_current_name) | |
| [`thread_wait`](#thread_wait) | block until the value at addr changes from expected |
| [`thread_wait_until`](#thread_wait_until) | block until the word changes or an absolute monotonic deadline is reached |
| [`thread_wake`](#thread_wake) | wake threads blocked in thread_wait on addr |
| [`io_queue_create`](#io_queue_create), [`io_queue_watch`](#io_queue_watch) | |
| [`duplicate_to`](#duplicate_to) | makes the descriptor to name what from names, closing whatever to named before, in one step |
| [`io_queue_rearm`](#io_queue_rearm) | arms again a registration the caller made with io_queue_watch |
| [`io_queue_unwatch`](#io_queue_unwatch), [`io_queue_wait`](#io_queue_wait), [`io_queue_wake`](#io_queue_wake), [`io_queue_close`](#io_queue_close), [`sock_send`](#sock_send) | |
| [`sock_recv`](#sock_recv) | raw native read semantics do not safely discard ancillary descriptor rights |
| [`local_stream_recv`](#local_stream_recv) | exclusively borrow the receive queue through peek and consume, including all aliases |
| [`sock_write_vector`](#sock_write_vector), [`sock_send_message`](#sock_send_message) | |
| [`sock_receive_message`](#sock_receive_message) | raw recvmsg preserves native ancillary ownership and truncation behavior |
| [`sock_set_nonblocking`](#sock_set_nonblocking) | switch a socket between blocking and nonblocking |
| [`sock_connect_begin`](#sock_connect_begin) | start a connect on a nonblocking socket |
| [`sock_connect_poll`](#sock_connect_poll) | ask whether a connect sock_connect_begin started has settled, without waiting |
| [`sock_close`](#sock_close), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto) | |
| [`sock_peek_readable`](#sock_peek_readable) | peek at a stream socket without consuming or blocking |
| [`sock_recvfrom`](#sock_recvfrom), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable) | |
| [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | set the receive timeout on a socket |
| [`random_fill`](#random_fill) | fill a buffer with cryptographic random bytes via getentropy |
| [`error_message`](#error_message) | |

| Constants | |
| :--- | :--- |
| [`F_GETFD`](#constants) | fcntl commands |
| [`F_SETFD`](#constants), [`F_GETFL`](#constants), [`F_SETFL`](#constants), [`FD_CLOEXEC`](#constants), [`O_NONBLOCK`](#constants), [`O_EVTONLY`](#constants), [`O_CLOEXEC`](#constants) | |
| [`separator`](#constants) | path |
| [`STDIN_FD`](#constants) | portable constants |
| [`STDOUT_FD`](#constants), [`STDERR_FD`](#constants), [`O_RDONLY`](#constants), [`O_WRONLY`](#constants), [`O_RDWR`](#constants), [`O_CREAT`](#constants), [`O_EXCL`](#constants), [`O_TRUNC`](#constants), [`O_APPEND`](#constants), [`O_DIRECTORY`](#constants), [`O_NOFOLLOW`](#constants), [`AT_FDCWD`](#constants), [`AT_SYMLINK_NOFOLLOW`](#constants), [`AT_REMOVEDIR`](#constants) | |
| [`LOCK_SH`](#constants) | advisory whole-file lock operations, passed to lock_fd |
| [`LOCK_EX`](#constants), [`LOCK_NB`](#constants), [`LOCK_UN`](#constants), [`S_IFMT`](#constants), [`S_IFDIR`](#constants), [`S_IFREG`](#constants), [`S_IFLNK`](#constants), [`WNOHANG`](#constants), [`WUNTRACED`](#constants), [`WCONTINUED`](#constants), [`CLOCK_REALTIME`](#constants), [`CLOCK_MONOTONIC`](#constants), [`EPERM`](#constants), [`ENOENT`](#constants), [`ESRCH`](#constants), [`EINTR`](#constants), [`EIO`](#constants), [`ENXIO`](#constants), [`E2BIG`](#constants), [`EBADF`](#constants), [`ECHILD`](#constants), [`EAGAIN`](#constants), [`ENOMEM`](#constants), [`EACCES`](#constants), [`EFAULT`](#constants), [`EBUSY`](#constants), [`EEXIST`](#constants), [`ENODEV`](#constants), [`ENOTDIR`](#constants), [`EISDIR`](#constants), [`EINVAL`](#constants), [`ENFILE`](#constants), [`EMFILE`](#constants), [`ETXTBSY`](#constants), [`ENOSPC`](#constants), [`EROFS`](#constants), [`EPIPE`](#constants), [`ELOOP`](#constants), [`ENAMETOOLONG`](#constants), [`ENOTEMPTY`](#constants), [`ENOTSUP`](#constants), [`ENOSYS`](#constants), [`ERANGE`](#constants), [`EADDRINUSE`](#constants), [`ENETUNREACH`](#constants), [`ECONNABORTED`](#constants), [`ECONNRESET`](#constants), [`ENOTCONN`](#constants), [`ETIMEDOUT`](#constants), [`ECONNREFUSED`](#constants), [`EHOSTUNREACH`](#constants), [`ECANCELED`](#constants), [`EINTR_MAX_RETRIES`](#constants), [`IO_EVENT_READ`](#constants), [`IO_EVENT_WRITE`](#constants), [`IO_EVENT_ERROR`](#constants), [`IO_EVENT_HANGUP`](#constants), [`IO_EVENT_WAKE`](#constants), [`AF_INET`](#constants), [`AF_INET6`](#constants), [`SOCK_STREAM`](#constants), [`SOCK_DGRAM`](#constants), [`SOL_SOCKET`](#constants), [`SO_UNSUPPORTED`](#constants), [`SO_REUSEADDR`](#constants), [`SO_REUSEPORT`](#constants), [`SO_EXCLUSIVEADDRUSE`](#constants), [`SO_KEEPALIVE`](#constants), [`SO_SNDBUF`](#constants), [`SO_RCVBUF`](#constants), [`SO_LINGER`](#constants), [`SO_RCVTIMEO`](#constants), [`IPPROTO_IP`](#constants), [`IPPROTO_TCP`](#constants), [`IPPROTO_IPV6`](#constants), [`IP_TOS`](#constants), [`IPV6_V6ONLY`](#constants), [`IPV6_TCLASS`](#constants), [`TCP_NODELAY`](#constants), [`TCP_KEEPIDLE`](#constants), [`TCP_KEEPINTVL`](#constants), [`TCP_KEEPCNT`](#constants), [`TCP_FASTOPEN`](#constants), [`SHUT_RD`](#constants), [`SHUT_WR`](#constants), [`SHUT_RDWR`](#constants), [`SOCKADDR_IN_SIZE`](#constants), [`SOCKADDR_IN6_SIZE`](#constants), [`SOCKADDR_STORAGE_SIZE`](#constants) | |
| [`CONNECT_PENDING`](#constants) | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| [`DNS_HOSTS_PATH`](#constants) | |

| Variables | |
| :--- | :--- |
| [`_envp`](#variables) | environment (set by runtime at program start) |

| Forwards | |
| :--- | :--- |
| [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult), [`IoVector`](#iovector) | |
| [`ProcessStatus`](#processstatus) | canonical process observations |
| [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |

---

## stat_t

```mach
pub rec stat_t {
    st_dev:            i32;
    st_mode:           u16;
    st_nlink:          u16;
    st_ino:            u64;
    st_uid:            u32;
    st_gid:            u32;
    st_rdev:           i32;
    st_atime:          i64;
    st_atime_nsec:     i64;
    st_mtime:          i64;
    st_mtime_nsec:     i64;
    st_ctime:          i64;
    st_ctime_nsec:     i64;
    st_birthtime:      i64;
    st_birthtime_nsec: i64;
    st_size:           i64;
    st_blocks:         i64;
    st_blksize:        i32;
    st_flags:          u32;
    st_gen:            u32;
    _reserved0:        i32;
    _reserved1:        i64;
    _reserved2:        i64;
}
```

darwin stat64 structure for file metadata

### stat

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

### stat_path

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

### stat_mode

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 16-bit in the darwin stat64 ABI (mode_t is __uint16_t); widen it
so portable callers read the mode uniformly with the 32-bit platforms.

| Parameter | |
| :--- | :--- |
| `st` | pointer to a filled stat_t |
| **returns** | the raw mode bits, widened to 32 bits |

## timespec

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

### clock_gettime

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

read a clock into a timespec

CLOCK_REALTIME (0) and CLOCK_MONOTONIC (6) are darwin's own `clockid_t`
values from \<time.h>, not linux's - they happen to have been correct already,
because the constants were always written against darwin's header even while
the call underneath was a trap that does not exist.

| Parameter | |
| :--- | :--- |
| `clock_id` | CLOCK_REALTIME or CLOCK_MONOTONIC |
| `ts` | output timespec |
| **returns** | 0 on success, or negative errno |

## DirectoryCursor

```mach
pub rec DirectoryCursor {
    address: usize;
    active:  bool;
    ended:   bool;
    error:   i64;
    stream:  std.system.os.darwin.libsystem.DirectoryStream;
}
```

### directory_init

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

### directory_dnit

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

closedir consumes its stream even when the underlying close fails

## IoCompletion

```mach
pub rec IoCompletion {
    context: usize;
    events:  u32;
    source:  u16;
    status:  i64;
    flags:   u64;
}
```

context is opaque to the OS and zero is reserved for the runtime wake source
source: the id of the source that registered the context, 0 for a wake. it
        sits in the padding after events, so the record stays 32 bytes

### io_queue_poll

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

## Functions

### terminate

```mach
pub fun terminate(code: i64)
```

exit the process with the given code

`_exit(2)`, not `exit(3)`: std registers no atexit handlers and the raw
trap this replaces ran none. the trap after it is unreachable and kept only
as a guard; it is not the terminator.

| Parameter | |
| :--- | :--- |
| `code` | exit code |

### abort

```mach
pub fun abort()
```

abort the process immediately with exit code 255

the process-wide SIGABRT is what a debugger or crash reporter sees; if it
is ignored or handled, the exit below still ends the process.

### allocate

```mach
pub fun allocate(size: usize) ptr
```

### deallocate

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

### map_secret

```mach
pub fun map_secret(span: usize, page: usize, out: *ptr, locking: *bool) i64
```

map storage for secret-welded data: span locked bytes between two
inaccessible guard pages, page aligned and zero-filled

xnu has no per-mapping dump exclusion, so locking keeps the span out of swap
and nothing more. a refused lock is reported as one, never served unlocked

| Parameter | |
| :--- | :--- |
| `span` | usable bytes, a nonzero multiple of page |
| `page` | the page size |
| `out` | receives the first usable byte, one page past the mapping's start |
| `locking` | set when the failure was the kernel refusing to lock the span |
| **returns** | 0, or the negative errno of the step that failed, with nothing mapped |

### reallocate

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

darwin has no mremap, allocate new, copy, free old

### heap_region_base

```mach
pub fun heap_region_base() usize
```

### heap_region_extend

```mach
pub fun heap_region_extend(addr: usize) usize
```

### protect

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

### lock

```mach
pub fun lock(p: ptr, size: usize) i64
```

### unlock

```mach
pub fun unlock(p: ptr, size: usize) i64
```

### advise

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

### map_file

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

### sync_file

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

### environ

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### read

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

### write

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

### read_at

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

positioned file access does not mutate the descriptor offset

### write_at

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

### open

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path relative to a directory descriptor

`mode` is only consulted by the kernel when `flags` carries O_CREAT, so it is
passed in the variadic tail only in that case. the two forms are not
interchangeable spellings of one call: apple arm64 passes the whole variadic
tail on the stack, so the no-O_CREAT form genuinely passes nothing rather
than passing an ignored register.

| Parameter | |
| :--- | :--- |
| `dirfd` | directory descriptor the path resolves against, or AT_FDCWD |
| `path` | null-terminated path |
| `flags` | O_* flags |
| `mode` | permission bits for a created file; ignored without O_CREAT |
| **returns** | the new descriptor, or negative errno |

### close

```mach
pub fun close(fd: i32) i64
```

close a descriptor

a failed close does NOT mean the descriptor is still open: darwin has already
released it by the time an error is reported. callers must not retry, and
none do - the return exists to surface a deferred write error.

### sync_fd

```mach
pub fun sync_fd(fd: i32) i64
```

flush an open file's data and metadata to its backing storage

### set_mode

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

### set_mode_at

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

### publication_capabilities

```mach
pub fun publication_capabilities(fd: i32) i64
```

### file_identity

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

observational ids do not retain an object after this call

### retain_identity_at

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_evtonly retains identity without data i/o after explicit read authorization

### identity_at

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### unlink

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

### lock_fd

```mach
pub fun lock_fd(fd: i32, op: i32) i64
```

flock: take or release an advisory whole-file lock on an open descriptor

the lock lives on the open file description, not on the directory entry, so
darwin drops it when the last descriptor referring to that description is
closed -- including the implicit close every exiting process performs, however
it exits. a holder that crashes therefore leaves no lock behind, which is what
makes a live holder distinguishable from a dead one's residue.

a directory descriptor is lockable on darwin, but windows cannot lock one, so
portable callers that want to exclude writers from a directory lock a regular
file inside it rather than the directory itself.

| Parameter | |
| :--- | :--- |
| `fd` | open descriptor to lock, which may refer to a directory |
| `op` | LOCK_SH, LOCK_EX or LOCK_UN, optionally combined with LOCK_NB |
| **returns** | 0 on success, or negative errno; EAGAIN when LOCK_NB was set and another holder has the lock |

### rename

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

### symlink

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

| Parameter | |
| :--- | :--- |
| `target` | path the link points to (stored as given, not resolved) |
| `linkpath` | path of the link to create |
| **returns** | 0 on success, or negative errno |

### make_dir

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

### access

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

### seek

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

reposition a descriptor's offset

lseek's failure sentinel is exactly -1, not "negative": the success value is
a file offset, which is never negative but IS returned as a signed 64-bit
number that a caller may legitimately compare against. testing for the
documented sentinel rather than for a sign keeps that distinction.

| Parameter | |
| :--- | :--- |
| **returns** | the resulting absolute offset, or negative errno |

### fd_flags

```mach
pub fun fd_flags(fd: i32) i64
```

read a descriptor's descriptor-level flags (FD_CLOEXEC)

F_GETFD is a TWO-argument fcntl: it reads no third argument, so none is
passed. that is not a micro-optimisation - on apple arm64 the variadic tail
is stack-passed, so "pass a dummy zero" and "pass nothing" put genuinely
different bytes at the callee's stack slot. the two forms are kept distinct
everywhere fcntl is called.

| Parameter | |
| :--- | :--- |
| **returns** | the flag word, or negative errno |

### set_fd_flags

```mach
pub fun set_fd_flags(fd: i32, flags: i32) i64
```

set a descriptor's descriptor-level flags

F_SETFD is a three-argument fcntl: exactly one int rides the variadic tail.

| Parameter | |
| :--- | :--- |
| **returns** | 0 on success, or negative errno |

### file_flags

```mach
pub fun file_flags(fd: i32) i64
```

read a descriptor's file-status flags (access mode, O_APPEND, O_NONBLOCK)

F_GETFL, like F_GETFD, takes no third argument.

| Parameter | |
| :--- | :--- |
| **returns** | the status flag word, or negative errno |

### set_file_flags

```mach
pub fun set_file_flags(fd: i32, flags: i32) i64
```

set a descriptor's file-status flags

| Parameter | |
| :--- | :--- |
| **returns** | 0 on success, or negative errno |

### fork

```mach
pub fun fork() i64
```

create a child process by duplicating the caller

| Parameter | |
| :--- | :--- |
| **returns** | child PID in the parent, 0 in the child, or negative errno |

### vfork

```mach
pub fun vfork() i64
```

create a child process through vfork(2)

the wrapper promises the fork contract only; see the libsystem module.

| Parameter | |
| :--- | :--- |
| **returns** | child PID in the parent, 0 in the child, or negative errno |

### exec

```mach
pub fun exec(pathname: *u8, argv: **u8, envp: Environment) i64
```

replace the calling process image; returns only on failure

| Parameter | |
| :--- | :--- |
| **returns** | negative errno |

### wait

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

failures and no-event results leave the caller's status unchanged

### wait_pid

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

### terminate_child

```mach
pub fun terminate_child(pid: i64) i64
```

forcefully stop a spawned child without reaping it

waitid with WNOWAIT first asks the kernel to verify that `pid` is still a
child of this process. this rejects unknown and already-reaped PIDs before
kill can affect them, while preserving an exited child's wait status.
callers must not concurrently reap this child through wait or wait_pid: a
reaper could release the numeric PID between the ownership check and kill.

| Parameter | |
| :--- | :--- |
| `pid` | child process ID returned by spawn |
| **returns** | 0 on success, or negative errno |

### setpgid

```mach
pub fun setpgid(pid: i64, pgid: i64) i64
```

setpgid: set (or join) the process group ID of a process

| Parameter | |
| :--- | :--- |
| `pid` | target process ID (0 = caller) |
| `pgid` | desired process group ID (0 = pid becomes the leader of a new group) |
| **returns** | 0 on success, or negative errno |

### getpgid

```mach
pub fun getpgid(pid: i64) i64
```

getpgid: read the process group ID of a process

| Parameter | |
| :--- | :--- |
| `pid` | target process ID (0 = caller) |
| **returns** | process group ID, or negative errno |

### terminate_group

```mach
pub fun terminate_group(pgid: i64) i64
```

signal every process in a group without reaping any of them

unlike terminate_child, there is no waitid ownership probe first: a process
group is not tracked as a child of this process, so kill(-pgid, SIGTERM) is
the only available primitive. surviving members stay individually waitable
through wait/wait_any exactly as before.

| Parameter | |
| :--- | :--- |
| `pgid` | process group ID (must be > 0; a negated pgid targets the whole group) |
| **returns** | 0 on success, or negative errno |

### kill_group

```mach
pub fun kill_group(pgid: i64) i64
```

forcefully stop every process in a group without reaping any of them

the group's members get SIGKILL, which none of them can catch or ignore.
as with terminate_group there is no ownership probe, and members stay
individually waitable.

| Parameter | |
| :--- | :--- |
| `pgid` | process group ID (must be > 0) |
| **returns** | 0 on success, or negative errno |

### probe_group

```mach
pub fun probe_group(pgid: i64) i64
```

whether any process is left in a group, without signalling it

kill(-pgid, 0) checks for members and delivers nothing. a member this
process may not signal still counts, so EPERM reads as present.

| Parameter | |
| :--- | :--- |
| `pgid` | process group ID (must be > 0) |
| **returns** | 0 while a member is left, ESRCH once none is, or another negative errno |

### process_watch

```mach
pub fun process_watch(queue: *std.system.os.shared.IoQueue, pid: i64, context: usize) i64
```

make the end of the child `pid` a readiness event on `queue`, so the queue's
wait returns once the child ends: a one-shot EVFILT_PROC NOTE_EXIT filter

| Parameter | |
| :--- | :--- |
| `context` | the nonzero context the event carries |
| **returns** | the watch, which process_unwatch releases, or negative errno (ESRCH when the child has already ended) |

### process_unwatch

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired

| Parameter | |
| :--- | :--- |
| **returns** | 0, or the negative errno |

### spawn

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | child PID on success, or negative errno |

### spawn_grouped

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program, placed as the leader of
its own new process group (see spawn_redirected_in_grouped)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | child PID on success, or negative errno; the child's pgid equals its pid |

### spawn_in

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| **returns** | child PID on success, or negative errno |

### spawn_redirected

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with its standard streams bound to
caller-supplied descriptors.

forks, duplicates each non-negative descriptor onto the matching
standard stream (-1 inherits the parent's stream), closes inherited
descriptors >= 3 (including both ends of a capture pipe), and execs.
the parent keeps ownership of the passed descriptors; pairing one with
a pipe end lets the parent stream the child's stdio. the child exits
126 when a redirect fails and 127 when exec fails.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| **returns** | child PID on success, or negative errno |

### spawn_redirected_grouped

```mach
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed as the leader of its own new process group (see
spawn_redirected_in_grouped)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| **returns** | child PID on success, or negative errno; the child's pgid equals its pid |

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory

`cwd` is the directory the child starts in, or nil to inherit the parent's.
the chdir happens in the child, after the fork/clone, so the parent's own
working directory is untouched. passing it here rather than prefixing a `cd`
onto a shell command keeps the path out of the command line, where it would
have to survive a quoting convention the target program may not share
(mach#2587).

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| **returns** | child PID on success, or negative errno |

### spawn_redirected_in_grouped

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

the child alone creates the group and acknowledges it through a private pipe.
the parent returns only after receiving readiness, so immediate group signals
cannot race establishment. failed handshakes close their pipes and reap the
unexposed child before returning the native error.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| **returns** | child PID on success, or negative errno; the child's pgid equals its pid |

### getpid

```mach
pub fun getpid() i64
```

return the current process ID

| Parameter | |
| :--- | :--- |
| **returns** | process ID |

### open_file_limit

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

read this process's open-file limit.

darwin refuses a soft limit above kern.maxfilesperproc even when the hard
limit is RLIM_INFINITY (setrlimit(2) COMPATIBILITY), so the ceiling is the
smaller of the two. this is the rule Go's runtime applies before raising the
limit (os/rlimit_darwin.go)

| Parameter | |
| :--- | :--- |
| `out` | filled with the limit in force |
| **returns** | 0, or a negative native code |

### set_open_file_limit

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

set this process's open-file limit. ceiling is ignored, and darwin's own
refusal of a soft limit above its per-process maximum passes through

| Parameter | |
| :--- | :--- |
| `limit` | the soft and hard limits to set |
| **returns** | 0, or a negative native code |

### ignore_sigpipe

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

signal(3) installs the disposition through public libSystem. it is
process-wide, so subsequent writes from every thread return EPIPE when their
pipe has no reader instead of terminating the process.

| Parameter | |
| :--- | :--- |
| **returns** | 0 on success, or negative errno |

### sleep

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

uses nanosleep(3). the previous note here - "darwin has no nanosleep
syscall" - was true of the trap table and false of libSystem, so this went
through `select` with a timeout and lost the sub-microsecond resolution to
`timeval` on the way.

a signal that cuts the sleep short leaves the unslept remainder in `rem`, and
the retry resumes with THAT rather than restarting the full interval, so an
interrupted sleep still ends at about the requested time instead of
stretching towards double it.

| Parameter | |
| :--- | :--- |
| `nsec` | nanoseconds to sleep |

### cpu_count

```mach
pub fun cpu_count() i64
```

the currently active processor count
reads hw.activecpu, with a minimum of one if the query fails

### cpu_features

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

the running processor's instruction-set extensions

x86_64 reads cpuid, which needs no OS. aarch64 asks sysctl for
hw.optional.arm.FEAT_SHA256, FEAT_AES and FEAT_PMULL, each an int that is 0
or absent when the processor lacks it, as hw.activecpu is read above

| Parameter | |
| :--- | :--- |
| `out` | filled with the extensions the processor has |
| **returns** | 0, or a negative native code |

### cpu_dit

```mach
pub fun cpu_dit() i64
```

whether the processor provides the data-independent-timing mode

aarch64 asks sysctl for hw.optional.arm.FEAT_DIT, as `cpu_features` asks for
FEAT_SHA256. a failed read counts as absent, since the caller fails closed

| Parameter | |
| :--- | :--- |
| **returns** | 1 when present, 0 when absent or unreadable, ENOTSUP on x86_64 |

### thread_affinity

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

darwin has no hard CPU affinity: THREAD_AFFINITY_POLICY is a scheduling hint
over tags, not a CPU set, so neither affinity primitive is offered

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### set_thread_affinity

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

darwin has no hard CPU affinity, so a thread cannot be pinned

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### getcwd

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

this used to be an open(".") + fcntl(F_GETPATH) dance with a MAXPATHLEN
bounce buffer, because F_GETPATH carries no capacity: XNU writes up to
MAXPATHLEN bytes into the destination whatever the caller sized it, so the
result had to be caught in a large scratch and copied out only when it fit.

getcwd(3) TAKES the capacity, so the callee honours `size` itself and a path
that does not fit comes back as ERANGE from libSystem rather than as an
overrun this function has to defend against afterwards. the scratch buffer,
the copy loop, and the F_GETPATH constant all go away with it (#409, #413).

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `size` | buffer capacity in bytes, including room for the terminator |
| **returns** | length of path on success, or negative errno |

### getenv

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

| Parameter | |
| :--- | :--- |
| `name` | null-terminated variable name |
| `buf` | destination buffer for the value |
| `cap` | buffer capacity in bytes |
| **returns** | full length of the value, or ENOENT when the variable is unset |

### temp_dir

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

the directory designated for temporary files: $TMPDIR, else "/tmp"

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer for the path |
| `cap` | buffer capacity in bytes |
| **returns** | full length of the path, so ret >= cap signals truncation |

### thread_block_enter

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's

| Parameter | |
| :--- | :--- |
| **returns** | 0, or the negated refusal of pthread_key_create or pthread_setspecific |

### thread_block

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, read from its pthread TSD without a system call

| Parameter | |
| :--- | :--- |
| **returns** | the block, or nil on a thread nothing installed one on |

### stack_bounds

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, recorded in its block when it was
installed, or asked of libpthread on a thread std did not create

| Parameter | |
| :--- | :--- |
| **returns** | true, libpthread knows every thread's stack |

### thread_exit_wipe

```mach
pub fun thread_exit_wipe()
```

wipe the calling thread's thread-local block as the thread ends

thread-locals may hold secrets, so the whole block is zeroed with stores no
pass removes. nothing may read a thread-local after this

### thread_spawn

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

create a joinable pthread and release it only through join or detach

### thread_join

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

### thread_detach

```mach
pub fun thread_detach(native: usize) i64
```

### thread_current_id

```mach
pub fun thread_current_id() i64
```

### thread_current_name

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

### thread_wait

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

returns immediately if *addr does not equal expected. spurious wakeups are
possible and are expected: bucket sharing means a wake for a different
address can land here (see the bucket-table note above), so every caller must
re-test its own condition in a loop.

| Parameter | |
| :--- | :--- |
| `addr` | pointer to the futex word |
| `expected` | value to compare against |
| **returns** | 0 on wake, or negative errno |

### thread_wait_until

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

block until the word changes or an absolute monotonic deadline is reached

### thread_wake

```mach
pub fun thread_wake(addr: *i64) i64
```

wake threads blocked in thread_wait on addr

broadcasts rather than signals: buckets are shared by address hash, so a
signal could be delivered to a waiter on an unrelated address and the wake
this call was meant to deliver would be lost.

| Parameter | |
| :--- | :--- |
| `addr` | pointer to the futex word |
| **returns** | 0 on success, or negative errno |

### io_queue_create

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_watch

```mach
pub fun io_queue_watch(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

### duplicate_to

```mach
pub fun duplicate_to(from: usize, to: usize) i64
```

makes the descriptor to name what from names, closing whatever to named
before, in one step

| Parameter | |
| :--- | :--- |
| `from` | an open descriptor |
| `to` | the descriptor number to take over |
| **returns** | 0, or the native failure |

### io_queue_rearm

```mach
pub fun io_queue_rearm(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

arms again a registration the caller made with io_queue_watch. kqueue's
EV_ADD updates an existing filter, and the kernel drops every filter when the
descriptor closes, so re-arming and registering are the same change

### io_queue_unwatch

```mach
pub fun io_queue_unwatch(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

### io_queue_wait

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

### io_queue_wake

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_close

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

### sock_send

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

### sock_recv

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

raw native read semantics do not safely discard ancillary descriptor rights.
a darwin peer can send scm_rights that install descriptors without returning them.

### local_stream_recv

```mach
pub fun local_stream_recv(fd: usize, buffer: *u8, length: usize) i64
```

exclusively borrow the receive queue through peek and consume, including all aliases.
ancillary refusal leaves the socket and its queued rights owned by the caller.

### sock_write_vector

```mach
pub fun sock_write_vector(fd: usize, vectors: *IoVector, count: usize) i64
```

### sock_send_message

```mach
pub fun sock_send_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: u32, control: *u8, control_length: usize) i64
```

### sock_receive_message

```mach
pub fun sock_receive_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: *u32, control: *u8, control_length: *usize, flags: *i32) i64
```

raw recvmsg preserves native ancillary ownership and truncation behavior.
darwin can install unreported scm_rights descriptors with nil or undersized control.
callers receiving rights must provide adequate control storage and close each result.

### sock_set_nonblocking

```mach
pub fun sock_set_nonblocking(fd: usize, enabled: bool) i64
```

switch a socket between blocking and nonblocking

| Parameter | |
| :--- | :--- |
| `fd` | socket handle |
| `enabled` | true for nonblocking |
| **returns** | 0, or the native failure |

### sock_connect_begin

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

start a connect on a nonblocking socket

| Parameter | |
| :--- | :--- |
| `fd` | a nonblocking stream socket |
| `addr` | pointer to the peer's sockaddr |
| `addrlen` | size of the sockaddr |
| **returns** | 0 once connected, CONNECT_PENDING while in flight, or negative errno |

### sock_connect_poll

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

| Parameter | |
| :--- | :--- |
| `fd` | the socket sock_connect_begin returned CONNECT_PENDING for |
| **returns** | 0 once connected, CONNECT_PENDING while in flight, or the connect's negative errno |

### sock_close

```mach
pub fun sock_close(fd: usize) i64
```

### sock_create

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

### sock_create_flags

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_bind

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

### sock_listen

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

### sock_accept

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

### sock_accept_flags

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_connect

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

### sock_sendto

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

### sock_peek_readable

```mach
pub fun sock_peek_readable(fd: usize) i64
```

peek at a stream socket without consuming or blocking

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| **returns** | 1 when a byte is readable, 0 at orderly end of stream, EAGAIN when nothing is ready yet, or the socket's negative errno |

### sock_recvfrom

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

### sock_shutdown

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

### sock_setopt

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

### sock_getopt

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

### sock_local_addr

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_remote_addr

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_inheritable

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

### sock_set_rcvtimeo

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

set the receive timeout on a socket

writes a struct timeval (tv_sec, tv_usec) derived from ms as the SO_RCVTIMEO
option value. ms == 0 clears the timeout, restoring indefinite blocking. once
set, a recv with no data pending fails with EAGAIN after the interval elapses.
darwin's tv_usec is 32-bit with 4 trailing pad bytes; a sub-second usec fits
the low word and the padding stays zero, so the byte image matches the linux
64-bit-tv_usec layout.

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `ms` | timeout in milliseconds, or 0 for no timeout |
| **returns** | 0 on success, or negative errno |

### random_fill

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

fill a buffer with cryptographic random bytes via getentropy

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `len` | number of bytes to fill |
| **returns** | 0 on success, or negative errno |

### error_message

```mach
pub fun error_message(code: i64) str
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `F_GETFD` | `i32` | `1` | fcntl commands |
| `F_SETFD` | `i32` | `2` |  |
| `F_GETFL` | `i32` | `3` |  |
| `F_SETFL` | `i32` | `4` |  |
| `FD_CLOEXEC` | `i32` | `1` |  |
| `O_NONBLOCK` | `i32` | `4` |  |
| `O_EVTONLY` | `i32` | `0x00008000` |  |
| `O_CLOEXEC` | `i32` | `0x01000000` |  |
| `separator` | `u8` | `'/'` | path |
| `STDIN_FD` | `i32` | `0` | portable constants |
| `STDOUT_FD` | `i32` | `1` |  |
| `STDERR_FD` | `i32` | `2` |  |
| `O_RDONLY` | `i32` | `0` |  |
| `O_WRONLY` | `i32` | `1` |  |
| `O_RDWR` | `i32` | `2` |  |
| `O_CREAT` | `i32` | `0x200` |  |
| `O_EXCL` | `i32` | `0x800` |  |
| `O_TRUNC` | `i32` | `0x400` |  |
| `O_APPEND` | `i32` | `8` |  |
| `O_DIRECTORY` | `i32` | `0x100000` |  |
| `O_NOFOLLOW` | `i32` | `0x00000100` |  |
| `AT_FDCWD` | `i32` | `-2` |  |
| `AT_SYMLINK_NOFOLLOW` | `i32` | `0x0020` |  |
| `AT_REMOVEDIR` | `i32` | `0x0080` |  |
| `LOCK_SH` | `i32` | `1` | advisory whole-file lock operations, passed to lock_fd |
| `LOCK_EX` | `i32` | `2` |  |
| `LOCK_NB` | `i32` | `4` |  |
| `LOCK_UN` | `i32` | `8` |  |
| `S_IFMT` | `u32` | `0o170000` |  |
| `S_IFDIR` | `u32` | `0o040000` |  |
| `S_IFREG` | `u32` | `0o100000` |  |
| `S_IFLNK` | `u32` | `0o120000` |  |
| `WNOHANG` | `i32` | `1` |  |
| `WUNTRACED` | `i32` | `2` |  |
| `WCONTINUED` | `i32` | `0x10` |  |
| `CLOCK_REALTIME` | `i32` | `0` |  |
| `CLOCK_MONOTONIC` | `i32` | `6` |  |
| `EPERM` | `i64` | `-1` |  |
| `ENOENT` | `i64` | `-2` |  |
| `ESRCH` | `i64` | `-3` |  |
| `EINTR` | `i64` | `-4` |  |
| `EIO` | `i64` | `-5` |  |
| `ENXIO` | `i64` | `-6` |  |
| `E2BIG` | `i64` | `-7` |  |
| `EBADF` | `i64` | `-9` |  |
| `ECHILD` | `i64` | `-10` |  |
| `EAGAIN` | `i64` | `-35` |  |
| `ENOMEM` | `i64` | `-12` |  |
| `EACCES` | `i64` | `-13` |  |
| `EFAULT` | `i64` | `-14` |  |
| `EBUSY` | `i64` | `-16` |  |
| `EEXIST` | `i64` | `-17` |  |
| `ENODEV` | `i64` | `-19` |  |
| `ENOTDIR` | `i64` | `-20` |  |
| `EISDIR` | `i64` | `-21` |  |
| `EINVAL` | `i64` | `-22` |  |
| `ENFILE` | `i64` | `-23` |  |
| `EMFILE` | `i64` | `-24` |  |
| `ETXTBSY` | `i64` | `-26` |  |
| `ENOSPC` | `i64` | `-28` |  |
| `EROFS` | `i64` | `-30` |  |
| `EPIPE` | `i64` | `-32` |  |
| `ELOOP` | `i64` | `-62` |  |
| `ENAMETOOLONG` | `i64` | `-63` |  |
| `ENOTEMPTY` | `i64` | `-66` |  |
| `ENOTSUP` | `i64` | `-45` |  |
| `ENOSYS` | `i64` | `-78` |  |
| `ERANGE` | `i64` | `-34` |  |
| `EADDRINUSE` | `i64` | `-48` |  |
| `ENETUNREACH` | `i64` | `-51` |  |
| `ECONNABORTED` | `i64` | `-53` |  |
| `ECONNRESET` | `i64` | `-54` |  |
| `ENOTCONN` | `i64` | `-57` |  |
| `ETIMEDOUT` | `i64` | `-60` |  |
| `ECONNREFUSED` | `i64` | `-61` |  |
| `EHOSTUNREACH` | `i64` | `-65` |  |
| `ECANCELED` | `i64` | `-89` |  |
| `EINTR_MAX_RETRIES` | `usize` | `8` |  |
| `IO_EVENT_READ` | `u32` | `0x01` |  |
| `IO_EVENT_WRITE` | `u32` | `0x02` |  |
| `IO_EVENT_ERROR` | `u32` | `0x04` |  |
| `IO_EVENT_HANGUP` | `u32` | `0x08` |  |
| `IO_EVENT_WAKE` | `u32` | `0x10` |  |
| `AF_INET` | `i32` | `2` |  |
| `AF_INET6` | `i32` | `30` |  |
| `SOCK_STREAM` | `i32` | `1` |  |
| `SOCK_DGRAM` | `i32` | `2` |  |
| `SOL_SOCKET` | `i32` | `0xFFFF` |  |
| `SO_UNSUPPORTED` | `i32` | `-2147483648` |  |
| `SO_REUSEADDR` | `i32` | `4` |  |
| `SO_REUSEPORT` | `i32` | `0x0200` |  |
| `SO_EXCLUSIVEADDRUSE` | `i32` | `SO_UNSUPPORTED` |  |
| `SO_KEEPALIVE` | `i32` | `0x0008` |  |
| `SO_SNDBUF` | `i32` | `0x1001` |  |
| `SO_RCVBUF` | `i32` | `0x1002` |  |
| `SO_LINGER` | `i32` | `0x0080` |  |
| `SO_RCVTIMEO` | `i32` | `0x1006` |  |
| `IPPROTO_IP` | `i32` | `0` |  |
| `IPPROTO_TCP` | `i32` | `6` |  |
| `IPPROTO_IPV6` | `i32` | `41` |  |
| `IP_TOS` | `i32` | `1` |  |
| `IPV6_V6ONLY` | `i32` | `27` |  |
| `IPV6_TCLASS` | `i32` | `36` |  |
| `TCP_NODELAY` | `i32` | `1` |  |
| `TCP_KEEPIDLE` | `i32` | `0x10` |  |
| `TCP_KEEPINTVL` | `i32` | `0x101` |  |
| `TCP_KEEPCNT` | `i32` | `0x102` |  |
| `TCP_FASTOPEN` | `i32` | `0x105` |  |
| `SHUT_RD` | `i32` | `0` |  |
| `SHUT_WR` | `i32` | `1` |  |
| `SHUT_RDWR` | `i32` | `2` |  |
| `SOCKADDR_IN_SIZE` | `usize` | `16` |  |
| `SOCKADDR_IN6_SIZE` | `usize` | `28` |  |
| `SOCKADDR_STORAGE_SIZE` | `usize` | `128` |  |
| `CONNECT_PENDING` | `i64` | `1` | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| `DNS_HOSTS_PATH` | `str` | `"/etc/hosts"` |  |

## Variables

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `_envp` (var) | `usize` | `0` | environment (set by runtime at program start) |

## Forwards

### DirectoryEntry

Forwards [`std.system.os.shared.DirectoryEntry`](../shared.md#directoryentry).

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### DirectoryInitResult

Forwards [`std.system.os.shared.DirectoryInitResult`](../shared.md#directoryinitresult).

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### IoVector

Forwards [`std.system.os.darwin.libsystem.IoVector`](libsystem.md#iovector).

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

### ProcessStatus

Forwards [`std.system.os.shared.ProcessStatus`](../shared.md#processstatus).

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

canonical process observations

### FileLimit

Forwards [`std.system.os.shared.FileLimit`](../shared.md#filelimit).

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

### LIMIT_UNLIMITED

Forwards [`std.system.os.shared.LIMIT_UNLIMITED`](../shared.md#constants).

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### ProcessWaitError

Forwards [`std.system.os.shared.ProcessWaitError`](../shared.md#processwaiterror).

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

### WaitResult

Forwards [`std.system.os.shared.WaitResult`](../shared.md#waitresult).

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards [`std.system.os.shared.PROCESS_OP_WAIT`](../shared.md#constants).

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards [`std.system.os.shared.PROCESS_OP_STATUS`](../shared.md#constants).

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards [`std.system.os.shared.PROCESS_OP_CLOSE`](../shared.md#constants).

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards [`std.system.os.shared.PROCESS_OP_SPAWN`](../shared.md#constants).

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards [`std.system.os.shared.PROCESS_OP_READ`](../shared.md#constants).

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards [`std.system.os.shared.PROCESS_OP_PIPE`](../shared.md#constants).

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards [`std.system.os.shared.PROCESS_OP_TERMINATE`](../shared.md#constants).

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards [`std.system.os.shared.PROCESS_EXITED`](../shared.md#constants).

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards [`std.system.os.shared.PROCESS_SIGNALED`](../shared.md#constants).

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards [`std.system.os.shared.PROCESS_STOPPED`](../shared.md#constants).

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards [`std.system.os.shared.PROCESS_CONTINUED`](../shared.md#constants).

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

