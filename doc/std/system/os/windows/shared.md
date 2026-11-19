[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [windows](README.md) / **shared**

# std.system.os.windows.shared

code shared across all windows ISA implementations

windows has no stable syscall interface. all OS interaction goes through
kernel32.dll and ntdll.dll via ext fun declarations, plus ws2_32.dll for
sockets, bcrypt.dll for system entropy, advapi32.dll for access control, and
api-ms-win-core-synch-l1-2-0.dll for the wait-on-address family. every import
carries an explicit `#[library]` decorator naming its providing DLL, so the PE
import directory attributes each to the right DLL rather than the first
dependency. a HANDLE-to-fd mapping table bridges the POSIX-style fd interface
used by os.mach.

Source: [`src/system/os/windows/shared.mach`](../../../../../src/system/os/windows/shared.mach)

Uses types from [`std.system.cpu.features`](../../cpu/features.md), [`std.system.file_identity`](../../file_identity.md), [`std.system.os.shared`](../shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`stat_t`](#stat_t) | `rec` |  |
| [`timespec`](#timespec) | `rec` |  |
| [`DirectoryCursor`](#directorycursor) | `rec` | the current entry's units are kept, terminated, just past the native area, and its UTF-8 spelling past them |
| [`IoCompletion`](#iocompletion) | `rec` | source: the id of the source that registered the context, 0 for a wake |

| On `stat_t` | |
| :--- | :--- |
| [`stat`](#stat) | |
| [`stat_mode`](#stat_mode) | read the type/permission bits from a filled stat buffer as a 32-bit word |
| [`stat_path`](#stat_path) | |
| [`stat_path_native`](#stat_path_native) | stat_path for a nul-terminated UTF-16 name, the units unchanged |

| On `timespec` | |
| :--- | :--- |
| [`clock_gettime`](#clock_gettime) | |

| On `DirectoryCursor` | |
| :--- | :--- |
| [`directory_init`](#directory_init) | fd and its aliases lend exclusive enumeration and seek access until close |
| [`directory_next_native`](#directory_next_native) | the next entry in UTF-16 units as the kernel gives it, so a name holding an unpaired surrogate is yielded like any other |
| [`directory_next`](#directory_next) | the next entry spelled in UTF-8, converted once from the native entry |
| [`directory_refused_native`](#directory_refused_native) | the entry the last directory_next refused for having no UTF-8 spelling, in native units and borrowed like an entry: 1 with out filled, or 0 when the last call refused nothing |
| [`directory_dnit`](#directory_dnit) | consumes the owner, including when native release reports failure |

| On `IoCompletion` | |
| :--- | :--- |
| [`io_queue_poll`](#io_queue_poll) | context is the stable OVERLAPPED address, flags carries transferred bytes and source comes from the completion key |
| [`io_queue_restore`](#io_queue_restore) | move one dequeued packet to the tail without changing its portable status |

| Functions | |
| :--- | :--- |
| [`last_error`](#last_error) | the calling thread's last Win32 error as a negated POSIX errno, for a consumer that binds a kernel32 call of its own (std.terminal.windows) |
| [`allocate`](#allocate), [`deallocate`](#deallocate) | |
| [`map_secret`](#map_secret) | map storage for secret-welded data: span locked bytes between two reserved, uncommitted guard pages, page aligned and zero-filled |
| [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size) | |
| [`map_file`](#map_file) | map a file descriptor into memory via CreateFileMapping + MapViewOfFile |
| [`sync_file`](#sync_file) | flush a memory-mapped region to its backing file via FlushViewOfFile |
| [`unmap_file`](#unmap_file) | |
| [`native_spelling`](#native_spelling) | a name in UTF-16 units spelled in UTF-8 through the one converter, not terminated: the byte count written, or measured when out is nil, EINVAL for a name with no UTF-8 spelling, or ERANGE when out is too small |
| [`native_path`](#native_path) | convert a UTF-8 path once into an owned native path, as every UTF-8 primitive does, for a caller that walks the name itself |
| [`confined_path`](#confined_path) | release what native_path converted a confined path, walked a component at a time, converted once: a path over the converter's limit is ENAMETOOLONG, as each of its components would be |
| [`native_path_release`](#native_path_release), [`open_root_utf8`](#open_root_utf8) | |
| [`open_root_native`](#open_root_native) | open a directory by a wide path, resolved by the W API |
| [`make_dir_utf8`](#make_dir_utf8), [`remove_file_utf8`](#remove_file_utf8), [`remove_dir_utf8`](#remove_dir_utf8) | |
| [`open_relative_utf8`](#open_relative_utf8) | open one utf-8 component from a pinned directory descriptor |
| [`open_relative_native`](#open_relative_native) | open one wide component from a pinned directory descriptor |
| [`positioned_begin`](#positioned_begin) | pin a descriptor's handle and file pointer around one positioned transfer: the entry lock serializes position changes and `positioned_end` restores the pointer the transfer moved |
| [`positioned_end`](#positioned_end), [`read_at`](#read_at), [`write_at`](#write_at), [`publication_capabilities`](#publication_capabilities), [`rename_relative_utf8`](#rename_relative_utf8) | |
| [`rename_relative_native`](#rename_relative_native) | rename one wide component to another between pinned directory descriptors |
| [`read`](#read), [`write`](#write), [`open`](#open) | |
| [`open_native`](#open_native) | open a nul-terminated UTF-16 path as given: the units reach the W APIs unchanged, so a name holding an unpaired surrogate opens what it names |
| [`close`](#close) | |
| [`lock_fd`](#lock_fd) | lock_fd: take or release an advisory whole-file lock on an open descriptor |
| [`sync_fd`](#sync_fd) | flush file data or ntfs directory metadata through the pinned object other windows filesystems cannot certify directory persistence and return enotsup |
| [`set_mode`](#set_mode) | an owner-only mode is enforced with a protected dacl granting only the current user, who also becomes the owner |
| [`set_mode_at`](#set_mode_at) | the same mapping as set_mode, for the object named relative to dirfd |
| [`set_mode_at_native`](#set_mode_at_native) | set_mode_at for a nul-terminated UTF-16 name, the units unchanged |
| [`file_identity`](#file_identity), [`retain_identity_at`](#retain_identity_at) | |
| [`retain_identity_at_native`](#retain_identity_at_native) | retain_identity_at for a nul-terminated UTF-16 name, the units unchanged |
| [`identity_at`](#identity_at) | |
| [`identity_at_native`](#identity_at_native) | identity_at for a nul-terminated UTF-16 name, the units unchanged |
| [`local_endpoint_path`](#local_endpoint_path) | the sun_path bytes of a nul-terminated UTF-16 socket path, converted once |
| [`local_endpoint_identity`](#local_endpoint_identity), [`unlink_force`](#unlink_force) | |
| [`unlink_force_native`](#unlink_force_native) | unlink_force for a nul-terminated UTF-16 name, the units unchanged |
| [`unlink`](#unlink) | |
| [`unlink_native`](#unlink_native) | remove a nul-terminated UTF-16 path as given, the units unchanged |
| [`rename`](#rename) | |
| [`rename_native`](#rename_native) | rename for nul-terminated UTF-16 names, the units unchanged |
| [`symlink`](#symlink) | relative targets remain relative, with native separators in the reparse data |
| [`symlink_native`](#symlink_native) | symlink for nul-terminated UTF-16 names, the units unchanged |
| [`make_dir`](#make_dir) | |
| [`make_dir_native`](#make_dir_native) | make_dir for a nul-terminated UTF-16 name, the units unchanged |
| [`access`](#access) | |
| [`access_native`](#access_native) | access for a nul-terminated UTF-16 name, the units unchanged |
| [`seek`](#seek), [`terminate`](#terminate), [`abort`](#abort) | |
| [`environment_name_compare`](#environment_name_compare) | compare complete UTF-8 names, each converted once and compared as environment_name_compare_native compares their units |
| [`environment_name_compare_native`](#environment_name_compare_native) | compare complete names in UTF-16 units as given, with the operating system's ordinal case table and no conversion, so unpaired surrogates compare as units |
| [`spawn`](#spawn) | create a child process running the given program |
| [`spawn_grouped`](#spawn_grouped) | create a child process running the given program, placed in its own new job object (see spawn_redirected_in_grouped) |
| [`spawn_in`](#spawn_in) | create a child process running the given program from `cwd` |
| [`spawn_redirected`](#spawn_redirected) | spawn a child with its standard streams bound to caller-supplied descriptors (-1 inherits the parent's stream) |
| [`spawn_redirected_grouped`](#spawn_redirected_grouped) | spawn a child with its standard streams bound to caller-supplied descriptors, placed in its own new job object (see spawn_redirected_in_grouped) |
| [`spawn_redirected_in`](#spawn_redirected_in) | spawn a child with redirected streams and an explicit working directory |
| [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | spawn a child with redirected streams and an explicit working directory, placed in its own new job object (process group) |
| [`spawn_native`](#spawn_native) | spawn as spawn does, from an executable and arguments in UTF-16 |
| [`spawn_in_native`](#spawn_in_native) | spawn as spawn_in does, from an executable, arguments and directory in UTF-16 |
| [`spawn_redirected_native`](#spawn_redirected_native) | spawn as spawn_redirected does, from an executable and arguments in UTF-16 |
| [`spawn_redirected_in_native`](#spawn_redirected_in_native) | spawn as spawn_redirected_in does, from nul-terminated UTF-16 given as is |
| [`spawn_redirected_in_grouped_native`](#spawn_redirected_in_grouped_native) | spawn as spawn_redirected_in_grouped does, from nul-terminated UTF-16 given as is |
| [`spawn_command_line`](#spawn_command_line) | spawn a program from a verbatim native command line, inheriting the streams |
| [`terminate_child`](#terminate_child) | forcefully stop a spawned child without reaping it |
| [`terminate_group`](#terminate_group) | terminate every process in a group's job without reaping its child |
| [`probe_group`](#probe_group) | whether any process is left in a group's job |
| [`process_watch`](#process_watch) | make the end of the tracked child `pid` a completion on `queue`, so the queue's wait returns once the child ends: a wait completion packet associated with the child's handle (windows 8 and later) carries `context` as its overlapped pointer |
| [`process_unwatch`](#process_unwatch) | release a watch process_watch made, whether or not it fired, removing a completion it queued and nobody took |
| [`getpid`](#getpid) | return the current process ID |
| [`open_file_limit`](#open_file_limit) | windows has no settable per-process descriptor limit: handles are bounded by kernel memory, so neither query nor set has a faithful answer |
| [`set_open_file_limit`](#set_open_file_limit) | |
| [`ignore_sigpipe`](#ignore_sigpipe) | ignore SIGPIPE for this process |
| [`pipe`](#pipe) | create a unidirectional pipe |
| [`sleep`](#sleep) | suspend execution for the given number of nanoseconds |
| [`cpu_count`](#cpu_count) | the number of CPUs available to this process |
| [`cpu_features`](#cpu_features) | the running processor's instruction-set extensions |
| [`cpu_dit`](#cpu_dit) | windows offers no way to set the data-independent-timing mode |
| [`thread_affinity`](#thread_affinity) | read the calling thread's CPU affinity, as global CPU indices |
| [`set_thread_affinity`](#set_thread_affinity) | pin the calling thread to the CPUs set in words |
| [`getcwd`](#getcwd) | get the current working directory |
| [`getcwd_native`](#getcwd_native) | getcwd in UTF-16 units, as the W API gives the path: a directory whose path holds an unpaired surrogate is reported as it is |
| [`getenv`](#getenv) | look up an environment variable by name |
| [`getenv_native`](#getenv_native) | getenv in UTF-16 units: the value is read with GetEnvironmentVariableW and not converted, so one holding an unpaired surrogate reads as it is |
| [`temp_dir`](#temp_dir) | resolve the directory designated for temporary files |
| [`temp_dir_native`](#temp_dir_native) | temp_dir in UTF-16 units, under the same truncation contract with cap in units |
| [`environ_native`](#environ_native) | captures the block once as UTF-16 entries, unconverted, and skips hidden drive-current-directory names |
| [`wait`](#wait), [`wait_pid`](#wait_pid) | |
| [`thread_block_enter`](#thread_block_enter) | install block as the calling thread's |
| [`thread_block`](#thread_block) | the calling thread's block, read from its TEB without a system call |
| [`stack_bounds`](#stack_bounds) | the calling thread's stack bounds, read from its TEB without a system call |
| [`thread_exit_wipe`](#thread_exit_wipe) | wipe the calling thread's thread-local block as the thread ends |
| [`thread_spawn`](#thread_spawn) | create a thread with a retained native handle |
| [`thread_join`](#thread_join), [`thread_detach`](#thread_detach), [`thread_current_id`](#thread_current_id), [`thread_current_name`](#thread_current_name) | |
| [`thread_wait`](#thread_wait) | block until the value at addr changes from expected |
| [`thread_wait_until`](#thread_wait_until) | block until the word changes or an absolute monotonic deadline is reached |
| [`thread_wake`](#thread_wake) | wake one thread blocked on WaitOnAddress at addr |
| [`io_queue_create`](#io_queue_create) | |
| [`io_queue_attach`](#io_queue_attach) | every completion for resource reports source |
| [`io_queue_detach`](#io_queue_detach) | resource leaves the completion port it is attached to, so another queue can attach it |
| [`io_queue_wait`](#io_queue_wait) | |
| [`io_queue_wake`](#io_queue_wake) | nil is invalid use and a closed queue is EBADF on every platform |
| [`io_queue_close`](#io_queue_close), [`io_queue_cancel`](#io_queue_cancel) | |
| [`running_under_wine`](#running_under_wine) | detect whether the process is running under the wine windows compatibility layer rather than on genuine windows |
| [`sock_send`](#sock_send), [`sock_recv`](#sock_recv), [`sock_close`](#sock_close), [`sock_async_accept`](#sock_async_accept), [`sock_async_connect`](#sock_async_connect), [`sock_async_receive`](#sock_async_receive), [`sock_async_send`](#sock_async_send) | |
| [`sock_pending_bytes`](#sock_pending_bytes) | the bytes queued for reading on a socket |
| [`sock_async_receive_message`](#sock_async_receive_message) | |
| [`sock_receive_message_ready`](#sock_receive_message_ready) | receive one message now, without an overlapped operation |
| [`sock_async_send_message`](#sock_async_send_message), [`sock_async_result`](#sock_async_result), [`sock_accept_context`](#sock_accept_context), [`sock_connect_context`](#sock_connect_context), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto), [`sock_recvfrom`](#sock_recvfrom), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr) | |
| [`sock_set_nonblocking`](#sock_set_nonblocking) | switch a socket between blocking and nonblocking |
| [`sock_connect_begin`](#sock_connect_begin) | start a connect on a nonblocking socket |
| [`sock_connect_poll`](#sock_connect_poll) | ask whether a connect sock_connect_begin started has settled, without waiting |
| [`sock_inheritable`](#sock_inheritable) | |
| [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | set the receive timeout on a socket |
| [`random_fill`](#random_fill) | fill a buffer with cryptographic random bytes via BCryptGenRandom |
| [`error_message`](#error_message) | |

| Constants | |
| :--- | :--- |
| [`ECONNREFUSED`](#constants), [`ETIMEDOUT`](#constants), [`ECONNRESET`](#constants), [`ECONNABORTED`](#constants), [`ENETUNREACH`](#constants), [`EADDRINUSE`](#constants), [`EHOSTUNREACH`](#constants), [`ENOTCONN`](#constants), [`ENOTSOCK`](#constants), [`ECANCELED`](#constants) | |
| [`separator`](#constants) | path |
| [`STDIN_FD`](#constants) | portable constants |
| [`STDOUT_FD`](#constants), [`STDERR_FD`](#constants), [`O_RDONLY`](#constants), [`O_WRONLY`](#constants), [`O_RDWR`](#constants), [`O_CREAT`](#constants), [`O_EXCL`](#constants), [`O_TRUNC`](#constants), [`O_APPEND`](#constants), [`O_DIRECTORY`](#constants), [`AT_FDCWD`](#constants), [`AT_SYMLINK_NOFOLLOW`](#constants), [`AT_REMOVEDIR`](#constants) | |
| [`LOCK_SH`](#constants) | advisory whole-file lock operations, passed to lock_fd |
| [`LOCK_EX`](#constants), [`LOCK_NB`](#constants), [`LOCK_UN`](#constants), [`S_IFMT`](#constants), [`S_IFDIR`](#constants), [`S_IFREG`](#constants), [`S_IFLNK`](#constants), [`WNOHANG`](#constants), [`WUNTRACED`](#constants), [`WCONTINUED`](#constants), [`CLOCK_REALTIME`](#constants), [`CLOCK_MONOTONIC`](#constants), [`EPERM`](#constants), [`ENOENT`](#constants), [`ESRCH`](#constants), [`EINTR`](#constants), [`EIO`](#constants), [`ENXIO`](#constants), [`E2BIG`](#constants), [`EBADF`](#constants), [`ECHILD`](#constants), [`EAGAIN`](#constants), [`ENOMEM`](#constants), [`EACCES`](#constants), [`EFAULT`](#constants), [`EBUSY`](#constants), [`EEXIST`](#constants), [`ENODEV`](#constants), [`ENOTDIR`](#constants), [`EISDIR`](#constants), [`EINVAL`](#constants), [`ENFILE`](#constants), [`EMFILE`](#constants), [`ETXTBSY`](#constants), [`ENOSPC`](#constants), [`EROFS`](#constants), [`EPIPE`](#constants), [`ENAMETOOLONG`](#constants), [`ENOTEMPTY`](#constants), [`ELOOP`](#constants), [`ENOTSUP`](#constants), [`ENOSYS`](#constants), [`ERANGE`](#constants), [`EINTR_MAX_RETRIES`](#constants), [`IO_EVENT_READ`](#constants), [`IO_EVENT_WRITE`](#constants), [`IO_EVENT_ERROR`](#constants), [`IO_EVENT_HANGUP`](#constants), [`IO_EVENT_WAKE`](#constants), [`AF_INET`](#constants), [`AF_INET6`](#constants), [`SOCK_STREAM`](#constants), [`SOCK_DGRAM`](#constants), [`SOL_SOCKET`](#constants), [`SO_UNSUPPORTED`](#constants), [`SO_REUSEADDR`](#constants), [`SO_REUSEPORT`](#constants), [`SO_EXCLUSIVEADDRUSE`](#constants), [`SO_KEEPALIVE`](#constants), [`SO_SNDBUF`](#constants), [`SO_RCVBUF`](#constants), [`SO_LINGER`](#constants), [`SO_RCVTIMEO`](#constants), [`IPPROTO_IP`](#constants), [`IPPROTO_TCP`](#constants), [`IPPROTO_IPV6`](#constants), [`IP_TOS`](#constants), [`IPV6_V6ONLY`](#constants), [`IPV6_TCLASS`](#constants), [`TCP_NODELAY`](#constants), [`TCP_KEEPIDLE`](#constants), [`TCP_KEEPINTVL`](#constants), [`TCP_KEEPCNT`](#constants), [`TCP_FASTOPEN`](#constants), [`SHUT_RD`](#constants), [`SHUT_WR`](#constants), [`SHUT_RDWR`](#constants), [`SOCKADDR_IN_SIZE`](#constants), [`SOCKADDR_IN6_SIZE`](#constants), [`SOCKADDR_STORAGE_SIZE`](#constants), [`SOCKET_EXTENSION_ACCEPT`](#constants), [`SOCKET_EXTENSION_CONNECT`](#constants), [`SOCKET_EXTENSION_RECEIVE_MESSAGE`](#constants), [`SOCKET_EXTENSION_SEND_MESSAGE`](#constants) | |
| [`CONNECT_PENDING`](#constants) | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| [`DNS_HOSTS_PATH`](#constants) | |

| Forwards | |
| :--- | :--- |
| [`DirectoryEntry`](#directoryentry), [`NativeEntry`](#nativeentry), [`DirectoryInitResult`](#directoryinitresult), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate) | |

---

## stat_t

```mach
pub rec stat_t {
    st_dev:        u64;
    st_ino:        u64;
    st_nlink:      u64;
    st_mode:       u32;
    st_uid:        u32;
    st_gid:        u32;
    pad0:          i32;
    st_rdev:       u64;
    st_size:       i64;
    st_blksize:    i64;
    st_blocks:     i64;
    st_atime:      i64;
    st_atime_nsec: i64;
    st_mtime:      i64;
    st_mtime_nsec: i64;
    st_ctime:      i64;
    st_ctime_nsec: i64;
    _reserved0:    i64;
    _reserved1:    i64;
    _reserved2:    i64;
}
```

### stat

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

### stat_mode

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 32-bit in the synthesized windows stat_t; the accessor exists so
portable callers read the mode uniformly across platforms (darwin's is 16-bit).

| Parameter | |
| :--- | :--- |
| `st` | pointer to a filled stat_t |
| **returns** | the raw mode bits, widened to 32 bits |

### stat_path

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

### stat_path_native

```mach
pub fun stat_path_native(dirfd: i32, path: *u16, st: *stat_t, flags: i32) i64
```

stat_path for a nul-terminated UTF-16 name, the units unchanged

## timespec

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

### clock_gettime

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

## DirectoryCursor

```mach
pub rec DirectoryCursor {
    address:         usize;
    fd:              i32;
    active:          bool;
    ended:           bool;
    error:           i64;
    buffer:          ptr;
    capacity:        usize;
    native_capacity: usize;
    procedure:       ptr;
    entry_units:     usize;
    entry_type:      u8;
    refused:         bool;
}
```

the current entry's units are kept, terminated, just past the native area,
and its UTF-8 spelling past them

### directory_init

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next_native

```mach
pub fun directory_next_native(cursor: *DirectoryCursor, out: *NativeEntry) i64
```

the next entry in UTF-16 units as the kernel gives it, so a name holding an
unpaired surrogate is yielded like any other

### directory_next

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

the next entry spelled in UTF-8, converted once from the native entry. an
entry with no UTF-8 spelling is refused by itself: the converter's EINVAL,
out untouched, the native name kept for directory_refused_native, and the
next call goes on to the following entry

### directory_refused_native

```mach
pub fun directory_refused_native(cursor: *DirectoryCursor, out: *NativeEntry) i64
```

the entry the last directory_next refused for having no UTF-8 spelling, in
native units and borrowed like an entry: 1 with out filled, or 0 when the
last call refused nothing

### directory_dnit

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

consumes the owner, including when native release reports failure

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

source: the id of the source that registered the context, 0 for a wake. it
        sits in the padding after events, so the record stays 32 bytes

### io_queue_poll

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

context is the stable OVERLAPPED address, flags carries transferred bytes and
source comes from the completion key

### io_queue_restore

```mach
pub fun io_queue_restore(queue: *std.system.os.shared.IoQueue, completion: IoCompletion) i64
```

move one dequeued packet to the tail without changing its portable status

the net.async backends no longer call this: their cancel is asynchronous, and
restoring foreign packets reorders them behind later ones. its presence is
not a recommendation to drain and restore a shared queue

## Functions

### last_error

```mach
pub fun last_error() i64
```

the calling thread's last Win32 error as a negated POSIX errno, for a
consumer that binds a kernel32 call of its own (std.terminal.windows)

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

map storage for secret-welded data: span locked bytes between two reserved,
uncommitted guard pages, page aligned and zero-filled

VirtualLock keeps the span resident within the process's minimum working
set, the windows counterpart of RLIMIT_MEMLOCK. a refused lock is reported
as one, never served unlocked

| Parameter | |
| :--- | :--- |
| `span` | usable bytes, a nonzero multiple of page |
| `page` | the page size |
| `out` | receives the first usable byte, one page past the reservation's start |
| `locking` | set when the failure was the system refusing to lock the span |
| **returns** | 0, or the negated errno of the step that failed, with nothing mapped |

### reallocate

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

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

### page_size

```mach
pub fun page_size() usize
```

### map_file

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map a file descriptor into memory via CreateFileMapping + MapViewOfFile

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor to map |
| `offset` | offset into the file (must be page-aligned) |
| `size` | number of bytes to map; if 0, returns nil |
| `prot` | protection flags (PROT_READ, PROT_WRITE, PROT_EXEC) |
| **returns** | pointer to mapped region, or nil on failure |

### sync_file

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via FlushViewOfFile

| Parameter | |
| :--- | :--- |
| `p` | pointer to the mapped region |
| `size` | size of the region in bytes |
| **returns** | 0 on success, or negative errno |

### unmap_file

```mach
pub fun unmap_file(p: ptr, size: usize) i64
```

### native_spelling

```mach
pub fun native_spelling(name: *u16, length: usize, out: *u8, capacity: usize) i64
```

a name in UTF-16 units spelled in UTF-8 through the one converter, not
terminated: the byte count written, or measured when out is nil, EINVAL for
a name with no UTF-8 spelling, or ERANGE when out is too small

### native_path

```mach
pub fun native_path(path: *u8, out: *std.system.os.shared.NativePath) i64
```

convert a UTF-8 path once into an owned native path, as every UTF-8
primitive does, for a caller that walks the name itself

### confined_path

```mach
pub fun confined_path(path: *u8, out: *std.system.os.shared.NativePath) i64
```

release what native_path converted
a confined path, walked a component at a time, converted once: a path over
the converter's limit is ENAMETOOLONG, as each of its components would be

### native_path_release

```mach
pub fun native_path_release(path: *std.system.os.shared.NativePath)
```

### open_root_utf8

```mach
pub fun open_root_utf8(path: *u8) i64
```

### open_root_native

```mach
pub fun open_root_native(path: *u16) i64
```

open a directory by a wide path, resolved by the W API

### make_dir_utf8

```mach
pub fun make_dir_utf8(path: *u8) i64
```

### remove_file_utf8

```mach
pub fun remove_file_utf8(path: *u8) i64
```

### remove_dir_utf8

```mach
pub fun remove_dir_utf8(path: *u8) i64
```

### open_relative_utf8

```mach
pub fun open_relative_utf8(dirfd: i32, path: *u8, path_length: usize, flags: i32, mode: i32) i64
```

open one utf-8 component from a pinned directory descriptor

### open_relative_native

```mach
pub fun open_relative_native(dirfd: i32, name: *u16, name_length: usize, flags: i32, mode: i32) i64
```

open one wide component from a pinned directory descriptor

### positioned_begin

```mach
pub fun positioned_begin(fd: i32, handle: *isize, saved: *i64) i64
```

pin a descriptor's handle and file pointer around one positioned transfer:
the entry lock serializes position changes and `positioned_end` restores the
pointer the transfer moved. the secret OS boundary shares this discipline
for its welded transfers

### positioned_end

```mach
pub fun positioned_end(fd: i32, handle: isize, saved: i64) i64
```

### read_at

```mach
pub fun read_at(fd: i32, buffer: *u8, count: usize, offset: u64) i64
```

### write_at

```mach
pub fun write_at(fd: i32, buffer: *u8, count: usize, offset: u64) i64
```

### publication_capabilities

```mach
pub fun publication_capabilities(fd: i32) i64
```

### rename_relative_utf8

```mach
pub fun rename_relative_utf8(olddir: i32, oldpath: *u8, oldpath_length: usize, newdir: i32, newpath: *u8, newpath_length: usize) i64
```

### rename_relative_native

```mach
pub fun rename_relative_native(olddir: i32, old_name: *u16, old_length: usize, newdir: i32, new_name: *u16, new_length: usize) i64
```

rename one wide component to another between pinned directory descriptors

### read

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

### write

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

### open

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

### open_native

```mach
pub fun open_native(dirfd: i32, path: *u16, flags: i32, mode: i32) i64
```

open a nul-terminated UTF-16 path as given: the units reach the W APIs
unchanged, so a name holding an unpaired surrogate opens what it names

### close

```mach
pub fun close(fd: i32) i64
```

### lock_fd

```mach
pub fun lock_fd(fd: i32, op: i32) i64
```

lock_fd: take or release an advisory whole-file lock on an open descriptor

windows has no flock, so the lock is a LockFileEx byte-range lock over the
whole 64-bit range, which gives the same whole-file exclusion. the lock is
owned by the file HANDLE, and windows releases every lock a handle holds when
the handle closes, including the implicit close a terminating process performs.
a holder that crashes therefore leaves no lock behind, matching the unix
guarantee this call exists to provide.

unlike unix, a windows DIRECTORY handle cannot be locked. a caller that wants
to exclude writers from a directory must lock a regular file inside it.

| Parameter | |
| :--- | :--- |
| `fd` | open descriptor to lock, which must refer to a regular file |
| `op` | LOCK_SH, LOCK_EX or LOCK_UN, optionally combined with LOCK_NB |
| **returns** | 0 on success, or negative errno; EAGAIN when LOCK_NB was set and another holder has the lock |

### sync_fd

```mach
pub fun sync_fd(fd: i32) i64
```

flush file data or ntfs directory metadata through the pinned object
other windows filesystems cannot certify directory persistence and return enotsup

### set_mode

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

an owner-only mode is enforced with a protected dacl granting only the
current user, who also becomes the owner. any other mode has no faithful
windows form, since access control has no group or other split, so it
returns ENOTSUP and leaves the object unchanged

### set_mode_at

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

the same mapping as set_mode, for the object named relative to dirfd. a
reparse point is refused rather than followed

### set_mode_at_native

```mach
pub fun set_mode_at_native(dirfd: i32, name: *u16, mode: i32) i64
```

set_mode_at for a nul-terminated UTF-16 name, the units unchanged

### file_identity

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

### retain_identity_at

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

### retain_identity_at_native

```mach
pub fun retain_identity_at_native(dirfd: i32, path: *u16, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

retain_identity_at for a nul-terminated UTF-16 name, the units unchanged

### identity_at

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### identity_at_native

```mach
pub fun identity_at_native(dirfd: i32, path: *u16, out: *std.system.file_identity.Identity) i64
```

identity_at for a nul-terminated UTF-16 name, the units unchanged

### local_endpoint_path

```mach
pub fun local_endpoint_path(name: *u16, output: *u8, capacity: usize) i64
```

the sun_path bytes of a nul-terminated UTF-16 socket path, converted once.
sun_path is a byte string spelled in UTF-8, as local_endpoint_identity reads
it back, so an unpaired surrogate has no spelling there and is refused here

| Parameter | |
| :--- | :--- |
| `name` | the path in UTF-16 |
| `output` | destination for the bytes, not nul-terminated |
| `capacity` | size of output in bytes |
| **returns** | the byte count, or a negative native code |

### local_endpoint_identity

```mach
pub fun local_endpoint_identity(path: *u8, device: *u64, file: *u64) i64
```

### unlink_force

```mach
pub fun unlink_force(dirfd: i32, path: *u8, flags: i32) i64
```

### unlink_force_native

```mach
pub fun unlink_force_native(dirfd: i32, path: *u16, flags: i32) i64
```

unlink_force for a nul-terminated UTF-16 name, the units unchanged

### unlink

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

### unlink_native

```mach
pub fun unlink_native(dirfd: i32, path: *u16, flags: i32) i64
```

remove a nul-terminated UTF-16 path as given, the units unchanged

### rename

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

### rename_native

```mach
pub fun rename_native(olddir: i32, oldpath: *u16, newdir: i32, newpath: *u16) i64
```

rename for nul-terminated UTF-16 names, the units unchanged

### symlink

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

relative targets remain relative, with native separators in the reparse data

### symlink_native

```mach
pub fun symlink_native(target: *u16, linkpath: *u16) i64
```

symlink for nul-terminated UTF-16 names, the units unchanged. the target is
copied, since its separators are made native in the copy

### make_dir

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

### make_dir_native

```mach
pub fun make_dir_native(dirfd: i32, path: *u16, mode: i32) i64
```

make_dir for a nul-terminated UTF-16 name, the units unchanged

### access

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

### access_native

```mach
pub fun access_native(dirfd: i32, path: *u16, mode: i32, flags: i32) i64
```

access for a nul-terminated UTF-16 name, the units unchanged

### seek

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

### terminate

```mach
pub fun terminate(code: i64)
```

### abort

```mach
pub fun abort()
```

### environment_name_compare

```mach
pub fun environment_name_compare(left: *u8, right: *u8, output: *i32) i64
```

compare complete UTF-8 names, each converted once and compared as
environment_name_compare_native compares their units

### environment_name_compare_native

```mach
pub fun environment_name_compare_native(left: *u16, left_units: usize, right: *u16, right_units: usize, output: *i32) i64
```

compare complete names in UTF-16 units as given, with the operating system's
ordinal case table and no conversion, so unpaired surrogates compare as units

| Parameter | |
| :--- | :--- |
| `output` | -1, 0 or 1, written only on success |
| **returns** | 0, E2BIG for a length past the i32 CompareStringOrdinal takes, or EINVAL when it refuses |

### spawn

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

collapses onto spawn_redirected with all three streams inherited.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | child PID on success, or negative errno |

### spawn_grouped

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment, job_out: *isize) i64
```

create a child process running the given program, placed in its own new
job object (see spawn_redirected_in_grouped)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `job_out` | receives the tracked child group token on success |
| **returns** | child PID on success, or negative errno |

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
caller-supplied descriptors (-1 inherits the parent's stream).

with no redirection the child inherits the parent's streams natively;
otherwise inheritance is scoped to exactly the child's std handles via
PROC_THREAD_ATTRIBUTE_HANDLE_LIST (see create_redirected). the process
handle is tracked in the process table for wait/wait_pid. envp maps to
the CreateProcess environment block, and inherit to its NULL block, the
parent's own. a nil given environment is refused with EINVAL. an argv
whose joined command line exceeds the 32 KiB windows limit fails with E2BIG.

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
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32, job_out: *isize) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed in its own new job object (see
spawn_redirected_in_grouped)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| `job_out` | receives the tracked child group token on success |
| **returns** | child PID on success, or negative errno |

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory

`cwd` is the directory the child starts in, or nil to inherit the parent's.
passing it here rather than prefixing a `cd` onto a shell command keeps the
path out of the command line, where it would have to survive a quoting
convention the target program may not share (mach#2587).

the executable, each argument, the directory and each environment entry
are converted to UTF-16 once, refusing malformed UTF-8 with EINVAL, and
spawned by spawn_redirected_in_native

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
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32, job_out: *isize) i64
```

spawn a child with redirected streams and an explicit working directory,
placed in its own new job object (process group)

identical to spawn_redirected_in except the child is created CREATE_SUSPENDED
so it (and anything it might otherwise race to spawn before the group
exists) cannot run before AssignProcessToJobObject completes; see
register_child_grouped for the assign-then-resume sequence and its own
failure cleanup. the job carries JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| `stdin_fd` | descriptor to install as the child's stdin, or -1 to inherit |
| `stdout_fd` | descriptor to install as the child's stdout, or -1 to inherit |
| `stderr_fd` | descriptor to install as the child's stderr, or -1 to inherit |
| `job_out` | receives the tracked child group token on success |
| **returns** | child PID on success, or negative errno (job_out untouched) |

### spawn_native

```mach
pub fun spawn_native(pathname: *u16, argv: **u16, envp: NativeEnvironment) i64
```

spawn as spawn does, from an executable and arguments in UTF-16

### spawn_in_native

```mach
pub fun spawn_in_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16) i64
```

spawn as spawn_in does, from an executable, arguments and directory in UTF-16

### spawn_redirected_native

```mach
pub fun spawn_redirected_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn as spawn_redirected does, from an executable and arguments in UTF-16

### spawn_redirected_in_native

```mach
pub fun spawn_redirected_in_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn as spawn_redirected_in does, from nul-terminated UTF-16 given as is

the executable, the directory and each environment entry reach
CreateProcessW unchanged, and each argument enters the command line unit for
unit under the CRT quoting, so an unpaired surrogate launches, starts in or
reaches the child as it was given

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| **returns** | child PID on success, or negative errno |

### spawn_redirected_in_grouped_native

```mach
pub fun spawn_redirected_in_grouped_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32, job_out: *isize) i64
```

spawn as spawn_redirected_in_grouped does, from nul-terminated UTF-16 given as is

### spawn_command_line

```mach
pub fun spawn_command_line(application: *u8, command_line: *u8, envp: Environment, cwd: *u8) i64
```

spawn a program from a verbatim native command line, inheriting the streams

windows only, and outside the std.system.os contract: an escape hatch, not a
portable primitive. the contract's argv spawn cannot express it, because
cmd.exe does not read the CRT quoting that spawn produces. std.process.exec
uses it only to start the shell, and never for an ordinary argv spawn

the argv spawns encode their arguments with the CRT convention. a program
that parses its command line another way, such as cmd.exe, needs the line
exactly as it will read it, and this is the only spawn that passes one
through untouched. application is the resolved executable, so no PATH or
current-directory search happens. each string and environment entry is
converted to UTF-16 once, as the argv spawns convert theirs

| Parameter | |
| :--- | :--- |
| `application` | path to the executable |
| `command_line` | the complete native command line, program name included |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | working directory for the child, or nil to inherit |
| **returns** | child PID on success, or a negative native code |

### terminate_child

```mach
pub fun terminate_child(pid: i64) i64
```

forcefully stop a spawned child without reaping it

the retained process handle identifies the exact child even if Windows has
reused its numeric PID. the handle stays registered and open after
TerminateProcess, so wait_pid remains responsible for collecting the exit
status and closing it.
for parity with POSIX, callers must serialize termination and reaping of the
same child; concurrent waits on one child are not supported.

| Parameter | |
| :--- | :--- |
| `pid` | child process ID returned by spawn |
| **returns** | 0 on success, or negative errno |

### terminate_group

```mach
pub fun terminate_group(group: i64) i64
```

terminate every process in a group's job without reaping its child

the group token is the child pid, pinned until its retained process handle
closes. reaping the child closes its job and ends every process left in it,
so a group whose child is gone has no process left: ESRCH, as kill gives for
an empty group on posix.

| Parameter | |
| :--- | :--- |
| `group` | the group token from a grouped spawn |
| **returns** | 0 on success, ESRCH once no process is left, or another negative errno |

### probe_group

```mach
pub fun probe_group(group: i64) i64
```

whether any process is left in a group's job

reaping the group's child closes its job, and the job's kill-on-close limit
ends every process left in it, so a group whose child is gone has none left.

| Parameter | |
| :--- | :--- |
| `group` | the group token from a grouped spawn |
| **returns** | 0 while a process is left, ESRCH once none is, or another negative errno |

### process_watch

```mach
pub fun process_watch(queue: *std.system.os.shared.IoQueue, pid: i64, context: usize) i64
```

make the end of the tracked child `pid` a completion on `queue`, so the
queue's wait returns once the child ends: a wait completion packet
associated with the child's handle (windows 8 and later) carries `context`
as its overlapped pointer

| Parameter | |
| :--- | :--- |
| `context` | the nonzero context the completion carries |
| **returns** | the watch, the packet's handle, which process_unwatch releases, or negative errno (ECHILD for a pid this process does not track) |

### process_unwatch

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired, removing a
completion it queued and nobody took

| Parameter | |
| :--- | :--- |
| **returns** | 0, or the negative errno |

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

windows has no settable per-process descriptor limit: handles are bounded by
kernel memory, so neither query nor set has a faithful answer

### set_open_file_limit

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

### ignore_sigpipe

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

windows does not deliver SIGPIPE for a broken pipe, so this portable surface
is a no-op. writes already report EPIPE through their normal error return.

| Parameter | |
| :--- | :--- |
| **returns** | always 0 |

### pipe

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

| Parameter | |
| :--- | :--- |
| `fds` | pointer to two i32s; fds[0] = read end, fds[1] = write end |
| **returns** | 0 on success, or negative errno |

### sleep

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

| Parameter | |
| :--- | :--- |
| `nsec` | nanoseconds to sleep |

### cpu_count

```mach
pub fun cpu_count() i64
```

the number of CPUs available to this process

GetActiveProcessorCount over all processor groups, so machines with more
than 64 logical processors report fully. never returns less than 1.

| Parameter | |
| :--- | :--- |
| **returns** | usable CPU count (>= 1) |

### cpu_features

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

the running processor's instruction-set extensions

x86_64 reads cpuid, which needs no OS. aarch64 asks the kernel, which reports
the armv8 crypto extensions as one feature

| Parameter | |
| :--- | :--- |
| `out` | filled with the extensions the processor has |
| **returns** | 0 |

### cpu_dit

```mach
pub fun cpu_dit() i64
```

windows offers no way to set the data-independent-timing mode

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### thread_affinity

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

read the calling thread's CPU affinity, as global CPU indices

CPU i is bit i % 64 of words[i / 64]. out_count covers every active
processor across all groups, and only the thread's own group has bits set.

| Parameter | |
| :--- | :--- |
| `words` | destination for the mask words |
| `capacity` | number of words the destination holds |
| `out_count` | words written, or words needed when capacity is too small |
| **returns** | 0, ERANGE when capacity is too small, or the native refusal |

### set_thread_affinity

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

pin the calling thread to the CPUs set in words

every set CPU must lie in one processor group, since a thread's affinity is a
single group's mask. a set spanning groups is refused rather than truncated.

| Parameter | |
| :--- | :--- |
| `words` | mask words, CPU i is bit i % 64 of words[i / 64] |
| `count` | number of mask words |
| **returns** | 0, EINVAL for an empty set or an inactive CPU, ENOTSUP for a set spanning groups, or the native refusal |

### getcwd

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

GetCurrentDirectoryW overloads its return: on success it is the length
written, and when the destination is too small it is the size required
INCLUDING the terminator, with nothing written. Passing both through as a
success let a caller read an untouched buffer and believe it held a path, so
the too-small case is reported as ERANGE the way linux and darwin report it.

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `size` | buffer capacity in bytes, including room for the terminator |
| **returns** | length of the path, excluding the terminator, or negative errno |

### getcwd_native

```mach
pub fun getcwd_native(buf: *u16, size: usize) i64
```

getcwd in UTF-16 units, as the W API gives the path: a directory whose path
holds an unpaired surrogate is reported as it is. size counts units

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
| **returns** | full length of the value, ENOENT when the variable is unset, or a negative native code |

### getenv_native

```mach
pub fun getenv_native(name: *u16, buf: *u16, cap: usize) i64
```

getenv in UTF-16 units: the value is read with GetEnvironmentVariableW and
not converted, so one holding an unpaired surrogate reads as it is. below
cap it is copied with its terminator, and the full length is always returned

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated variable name |
| `buf` | destination for the value |
| `cap` | capacity in units |
| **returns** | full length of the value in units, ENOENT when the variable is unset, EINVAL for a nil name, or a negative native code |

### temp_dir

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

resolve the directory designated for temporary files

GetTempPathW consults TMP, then TEMP, then USERPROFILE, then the windows
directory, returning the first as a path that ends with a separator. it
follows the getenv truncation contract: ret \< cap means the path was
copied and null-terminated; ret >= cap means the buffer was too small and
ret is the full path length.

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer for the path |
| `cap` | buffer capacity in bytes |
| **returns** | full length of the path, or negative errno |

### temp_dir_native

```mach
pub fun temp_dir_native(buf: *u16, cap: usize) i64
```

temp_dir in UTF-16 units, under the same truncation contract with cap in units

### environ_native

```mach
pub fun environ_native() **u16
```

captures the block once as UTF-16 entries, unconverted, and skips hidden
drive-current-directory names

| Parameter | |
| :--- | :--- |
| **returns** | nil-terminated array of nul-terminated NAME=value entries, or nil when the block cannot be read or copied |

### wait

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

### wait_pid

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

### thread_block_enter

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's

| Parameter | |
| :--- | :--- |
| **returns** | 0, or the refusal of TlsAlloc or TlsSetValue |

### thread_block

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, read from its TEB without a system call

| Parameter | |
| :--- | :--- |
| **returns** | the block, or nil on a thread nothing installed one on |

### stack_bounds

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, read from its TEB without a system call

StackBase is the top of the stack and DeallocationStack the base of its
reserve, which the stack commits down toward as it grows, so the bounds hold
for every thread whoever created it. the block records none

| Parameter | |
| :--- | :--- |
| **returns** | true, every thread has a TEB |

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

create a thread with a retained native handle

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

wraps WaitOnAddress for 64-bit compare-and-wait. returns immediately
if *addr does not equal expected. spurious wakeups are possible.

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

wake one thread blocked on WaitOnAddress at addr

| Parameter | |
| :--- | :--- |
| `addr` | pointer to the futex word |
| **returns** | 0 (always succeeds) |

### io_queue_create

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_attach

```mach
pub fun io_queue_attach(queue: *std.system.os.shared.IoQueue, resource: usize, source: u16) i64
```

every completion for resource reports source

### io_queue_detach

```mach
pub fun io_queue_detach(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

resource leaves the completion port it is attached to, so another queue can
attach it. the resource must have no request outstanding. windows 8.1 and
later replace a handle's port this way

### io_queue_wait

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

### io_queue_wake

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

nil is invalid use and a closed queue is EBADF on every platform

### io_queue_close

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_cancel

```mach
pub fun io_queue_cancel(resource: usize, overlapped: ptr) i64
```

### running_under_wine

```mach
pub fun running_under_wine() bool
```

detect whether the process is running under the wine
windows compatibility layer rather than on genuine windows.

probes ntdll for the wine-only `wine_get_version` export, the canonical
wine marker; it is absent on real windows. ntdll is always mapped into a
win32 process, so GetModuleHandleA resolves it without a load.

| Parameter | |
| :--- | :--- |
| **returns** | true under wine, false on genuine windows |

### sock_send

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

### sock_recv

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

### sock_close

```mach
pub fun sock_close(fd: usize) i64
```

### sock_async_accept

```mach
pub fun sock_async_accept(listener: usize, accepted: usize, address: *u8, address_capacity: usize, bytes: *u32, overlapped: ptr) i64
```

### sock_async_connect

```mach
pub fun sock_async_connect(resource: usize, address: *u8, address_length: usize, bytes: *u32, overlapped: ptr) i64
```

### sock_async_receive

```mach
pub fun sock_async_receive(resource: usize, buffers: ptr, count: usize, flags: *u32, overlapped: ptr) i64
```

### sock_async_send

```mach
pub fun sock_async_send(resource: usize, buffers: ptr, count: usize, flags: u32, overlapped: ptr) i64
```

### sock_pending_bytes

```mach
pub fun sock_pending_bytes(resource: usize, out: *usize) i64
```

the bytes queued for reading on a socket. for a datagram socket a nonzero
count means a datagram is waiting, so a receive would not pend

| Parameter | |
| :--- | :--- |
| `resource` | the socket |
| `out` | receives the queued byte count |
| **returns** | 0, or a negative native code |

### sock_async_receive_message

```mach
pub fun sock_async_receive_message(resource: usize, message: ptr, overlapped: ptr) i64
```

### sock_receive_message_ready

```mach
pub fun sock_receive_message_ready(resource: usize, message: ptr, bytes: *u32) i64
```

receive one message now, without an overlapped operation. the caller has
checked that a datagram is queued (sock_pending_bytes), so the call does not
wait

| Parameter | |
| :--- | :--- |
| `resource` | the socket |
| `message` | the WSAMSG to fill |
| `bytes` | receives the byte count |
| **returns** | 0, or a negative native code (EMSGSIZE for a truncated datagram) |

### sock_async_send_message

```mach
pub fun sock_async_send_message(resource: usize, message: ptr, flags: u32, overlapped: ptr) i64
```

### sock_async_result

```mach
pub fun sock_async_result(resource: usize, overlapped: ptr, bytes: *u32, flags: *u32, wait: bool) i64
```

### sock_accept_context

```mach
pub fun sock_accept_context(accepted: usize, listener: usize) i64
```

### sock_connect_context

```mach
pub fun sock_connect_context(resource: usize) i64
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
| **returns** | 0 once connected, CONNECT_PENDING while in flight, or the negated errno winsock's failure maps to |

### sock_connect_poll

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

SO_CONNECT_TIME reads 0xffffffff until the socket is connected, which is
winsock's own answer: getpeername is not, since a socket can name its peer
before the connect completes

| Parameter | |
| :--- | :--- |
| `fd` | the socket sock_connect_begin returned CONNECT_PENDING for |
| **returns** | 0 once connected, CONNECT_PENDING while in flight, or the connect's failure |

### sock_inheritable

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

### sock_set_rcvtimeo

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

set the receive timeout on a socket

winsock takes SO_RCVTIMEO as a DWORD of milliseconds, not a timeval. ms == 0
clears the timeout, restoring indefinite blocking. once set, a recv with no
data pending fails with WSAETIMEDOUT (mapped to ETIMEDOUT) after the interval.

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `ms` | timeout in milliseconds, or 0 for no timeout |
| **returns** | 0 on success, or negative errno |

### random_fill

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

fill a buffer with cryptographic random bytes via BCryptGenRandom

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
| `ECONNREFUSED` | `i64` | `-111` |  |
| `ETIMEDOUT` | `i64` | `-110` |  |
| `ECONNRESET` | `i64` | `-104` |  |
| `ECONNABORTED` | `i64` | `-103` |  |
| `ENETUNREACH` | `i64` | `-101` |  |
| `EADDRINUSE` | `i64` | `-98` |  |
| `EHOSTUNREACH` | `i64` | `-113` |  |
| `ENOTCONN` | `i64` | `-107` |  |
| `ENOTSOCK` | `i64` | `-88` |  |
| `ECANCELED` | `i64` | `-125` |  |
| `separator` | `u8` | `'\\'` | path |
| `STDIN_FD` | `i32` | `0` | portable constants |
| `STDOUT_FD` | `i32` | `1` |  |
| `STDERR_FD` | `i32` | `2` |  |
| `O_RDONLY` | `i32` | `0` |  |
| `O_WRONLY` | `i32` | `1` |  |
| `O_RDWR` | `i32` | `2` |  |
| `O_CREAT` | `i32` | `0x100` |  |
| `O_EXCL` | `i32` | `0x200` |  |
| `O_TRUNC` | `i32` | `0x400` |  |
| `O_APPEND` | `i32` | `0x800` |  |
| `O_DIRECTORY` | `i32` | `0x10000` |  |
| `AT_FDCWD` | `i32` | `-100` |  |
| `AT_SYMLINK_NOFOLLOW` | `i32` | `0x0100` |  |
| `AT_REMOVEDIR` | `i32` | `0x0200` |  |
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
| `WCONTINUED` | `i32` | `8` |  |
| `CLOCK_REALTIME` | `i32` | `0` |  |
| `CLOCK_MONOTONIC` | `i32` | `1` |  |
| `EPERM` | `i64` | `-1` |  |
| `ENOENT` | `i64` | `-2` |  |
| `ESRCH` | `i64` | `-3` |  |
| `EINTR` | `i64` | `-4` |  |
| `EIO` | `i64` | `-5` |  |
| `ENXIO` | `i64` | `-6` |  |
| `E2BIG` | `i64` | `-7` |  |
| `EBADF` | `i64` | `-9` |  |
| `ECHILD` | `i64` | `-10` |  |
| `EAGAIN` | `i64` | `-11` |  |
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
| `ENAMETOOLONG` | `i64` | `-36` |  |
| `ENOTEMPTY` | `i64` | `-39` |  |
| `ELOOP` | `i64` | `-40` |  |
| `ENOTSUP` | `i64` | `-95` |  |
| `ENOSYS` | `i64` | `-38` |  |
| `ERANGE` | `i64` | `-34` |  |
| `EINTR_MAX_RETRIES` | `usize` | `8` |  |
| `IO_EVENT_READ` | `u32` | `0x01` |  |
| `IO_EVENT_WRITE` | `u32` | `0x02` |  |
| `IO_EVENT_ERROR` | `u32` | `0x04` |  |
| `IO_EVENT_HANGUP` | `u32` | `0x08` |  |
| `IO_EVENT_WAKE` | `u32` | `0x10` |  |
| `AF_INET` | `i32` | `2` |  |
| `AF_INET6` | `i32` | `23` |  |
| `SOCK_STREAM` | `i32` | `1` |  |
| `SOCK_DGRAM` | `i32` | `2` |  |
| `SOL_SOCKET` | `i32` | `0xFFFF` |  |
| `SO_UNSUPPORTED` | `i32` | `-2147483648` |  |
| `SO_REUSEADDR` | `i32` | `4` |  |
| `SO_REUSEPORT` | `i32` | `SO_UNSUPPORTED` |  |
| `SO_EXCLUSIVEADDRUSE` | `i32` | `-5` |  |
| `SO_KEEPALIVE` | `i32` | `8` |  |
| `SO_SNDBUF` | `i32` | `0x1001` |  |
| `SO_RCVBUF` | `i32` | `0x1002` |  |
| `SO_LINGER` | `i32` | `0x0080` |  |
| `SO_RCVTIMEO` | `i32` | `0x1006` |  |
| `IPPROTO_IP` | `i32` | `0` |  |
| `IPPROTO_TCP` | `i32` | `6` |  |
| `IPPROTO_IPV6` | `i32` | `41` |  |
| `IP_TOS` | `i32` | `3` |  |
| `IPV6_V6ONLY` | `i32` | `27` |  |
| `IPV6_TCLASS` | `i32` | `39` |  |
| `TCP_NODELAY` | `i32` | `1` |  |
| `TCP_KEEPIDLE` | `i32` | `3` |  |
| `TCP_KEEPINTVL` | `i32` | `17` |  |
| `TCP_KEEPCNT` | `i32` | `16` |  |
| `TCP_FASTOPEN` | `i32` | `15` |  |
| `SHUT_RD` | `i32` | `0` |  |
| `SHUT_WR` | `i32` | `1` |  |
| `SHUT_RDWR` | `i32` | `2` |  |
| `SOCKADDR_IN_SIZE` | `usize` | `16` |  |
| `SOCKADDR_IN6_SIZE` | `usize` | `28` |  |
| `SOCKADDR_STORAGE_SIZE` | `usize` | `128` |  |
| `SOCKET_EXTENSION_ACCEPT` | `u8` | `1` |  |
| `SOCKET_EXTENSION_CONNECT` | `u8` | `2` |  |
| `SOCKET_EXTENSION_RECEIVE_MESSAGE` | `u8` | `3` |  |
| `SOCKET_EXTENSION_SEND_MESSAGE` | `u8` | `4` |  |
| `CONNECT_PENDING` | `i64` | `1` | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| `DNS_HOSTS_PATH` | `str` | `"C:/Windows/System32/drivers/etc/hosts"` |  |

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

### NativeEntry

Forwards [`std.system.os.shared.NativeEntry`](../shared.md#nativeentry).

```mach
pub rec NativeEntry {
    name:      *Unit;
    length:    usize;
    type_hint: u8;
}
```

a directory entry in native units, borrowed until the next cursor
operation like a DirectoryEntry

### DirectoryInitResult

Forwards [`std.system.os.shared.DirectoryInitResult`](../shared.md#directoryinitresult).

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

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

