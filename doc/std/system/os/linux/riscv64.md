[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [linux](README.md) / **riscv64**

# std.system.os.linux.riscv64

riscv64-specific linux OS primitives

provides page_size and thread_spawn which require arch-specific assembly.
everything else is in shared.mach.

Source: [`src/system/os/linux/riscv64.mach`](../../../../../src/system/os/linux/riscv64.mach)

Uses types from [`std.system.os.shared`](../shared.md).

| Functions | |
| :--- | :--- |
| [`page_size`](#page_size) | return the system page size |
| [`thread_spawn`](#thread_spawn) | create a new thread sharing the current address space |
| [`thread_join`](#thread_join), [`thread_detach`](#thread_detach) | |
| [`thread_block_enter`](#thread_block_enter) | install block as the calling thread's, as the tp just above it |
| [`thread_block`](#thread_block) | the calling thread's block, just below tp, without a system call |
| [`main_thread_block`](#main_thread_block) | the main thread's block, in an area with its thread-local block when the executable has thread-locals, else the static fallback |
| [`thread_exit_wipe`](#thread_exit_wipe) | wipe the calling thread's thread-local block as the thread ends |
| [`stack_bounds`](#stack_bounds) | the calling thread's stack bounds, read without a system call |

| Forwards | |
| :--- | :--- |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`timespec`](#timespec), [`DirectoryCursor`](#directorycursor), [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`separator`](#separator) | path |
| [`STDIN_FD`](#stdin_fd) | constants |
| [`STDOUT_FD`](#stdout_fd), [`STDERR_FD`](#stderr_fd), [`O_RDONLY`](#o_rdonly), [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_NONBLOCK`](#o_nonblock), [`O_DIRECTORY`](#o_directory), [`O_NOFOLLOW`](#o_nofollow), [`AT_FDCWD`](#at_fdcwd), [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow), [`AT_REMOVEDIR`](#at_removedir) | |
| [`LOCK_SH`](#lock_sh) | advisory file-lock operations |
| [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un), [`S_IFMT`](#s_ifmt), [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk), [`WNOHANG`](#wnohang), [`WUNTRACED`](#wuntraced), [`WCONTINUED`](#wcontinued), [`CLOCK_REALTIME`](#clock_realtime), [`CLOCK_MONOTONIC`](#clock_monotonic), [`EPERM`](#eperm), [`ENOENT`](#enoent), [`ESRCH`](#esrch), [`EINTR`](#eintr), [`EIO`](#eio), [`ENXIO`](#enxio), [`E2BIG`](#e2big), [`EBADF`](#ebadf), [`ECHILD`](#echild), [`EAGAIN`](#eagain), [`ENOMEM`](#enomem), [`EACCES`](#eacces), [`EFAULT`](#efault), [`EBUSY`](#ebusy), [`EEXIST`](#eexist), [`ENODEV`](#enodev), [`ENOTDIR`](#enotdir), [`EISDIR`](#eisdir), [`EINVAL`](#einval), [`ENFILE`](#enfile), [`EMFILE`](#emfile), [`ETXTBSY`](#etxtbsy), [`ENOSPC`](#enospc), [`EROFS`](#erofs), [`EPIPE`](#epipe), [`ENAMETOOLONG`](#enametoolong), [`ERANGE`](#erange), [`ENOTEMPTY`](#enotempty), [`ELOOP`](#eloop), [`ENOTSUP`](#enotsup), [`EINTR_MAX_RETRIES`](#eintr_max_retries) | |
| [`has_numa`](#has_numa) | feature detection |
| [`has_huge_pages`](#has_huge_pages) | |
| [`syscall0`](#syscall0) | syscall wrappers |
| [`syscall1`](#syscall1), [`syscall2`](#syscall2), [`syscall3`](#syscall3), [`syscall4`](#syscall4), [`syscall5`](#syscall5), [`syscall6`](#syscall6) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`allocate_huge`](#allocate_huge), [`numa_node_count`](#numa_node_count), [`numa_current_node`](#numa_current_node), [`numa_allocate`](#numa_allocate), [`numa_move`](#numa_move), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`_envp`](#_envp) | environment |
| [`environ`](#environ), [`capture_pagesz`](#capture_pagesz), [`loader_present`](#loader_present), [`capture_main_stack`](#capture_main_stack), [`capture_tls`](#capture_tls) | |
| [`read`](#read) | filesystem |
| [`write`](#write), [`read_at`](#read_at), [`write_at`](#write_at), [`open`](#open), [`close`](#close), [`sync_fd`](#sync_fd), [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at), [`file_identity`](#file_identity), [`identity_at`](#identity_at), [`retain_identity_at`](#retain_identity_at), [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path), [`stat_mode`](#stat_mode), [`unlink`](#unlink), [`rename`](#rename), [`symlink`](#symlink), [`make_dir`](#make_dir), [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_dnit`](#directory_dnit), [`access`](#access), [`seek`](#seek), [`lock_fd`](#lock_fd) | |
| [`terminate`](#terminate) | process |
| [`abort`](#abort), [`terminate_child`](#terminate_child), [`setpgid`](#setpgid), [`getpgid`](#getpgid), [`terminate_group`](#terminate_group), [`kill_group`](#kill_group), [`probe_group`](#probe_group), [`process_watch`](#process_watch), [`process_unwatch`](#process_unwatch), [`spawn`](#spawn), [`spawn_grouped`](#spawn_grouped), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_grouped`](#spawn_redirected_grouped), [`spawn_redirected_in`](#spawn_redirected_in), [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped), [`getpid`](#getpid), [`pipe`](#pipe), [`ignore_sigpipe`](#ignore_sigpipe), [`sleep`](#sleep), [`cpu_count`](#cpu_count), [`cpu_features`](#cpu_features), [`cpu_dit`](#cpu_dit), [`thread_affinity`](#thread_affinity), [`set_thread_affinity`](#set_thread_affinity), [`getcwd`](#getcwd), [`getenv`](#getenv), [`fork`](#fork), [`vfork`](#vfork), [`exec`](#exec), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`AF_INET`](#af_inet) | sockets |
| [`SOCK_STREAM`](#sock_stream), [`SOCK_DGRAM`](#sock_dgram), [`SOCK_NONBLOCK`](#sock_nonblock), [`SOCK_CLOEXEC`](#sock_cloexec), [`SOL_SOCKET`](#sol_socket), [`SO_UNSUPPORTED`](#so_unsupported), [`SO_REUSEADDR`](#so_reuseaddr), [`SO_REUSEPORT`](#so_reuseport), [`SO_EXCLUSIVEADDRUSE`](#so_exclusiveaddruse), [`SO_KEEPALIVE`](#so_keepalive), [`SO_SNDBUF`](#so_sndbuf), [`SO_RCVBUF`](#so_rcvbuf), [`SO_LINGER`](#so_linger), [`SO_RCVTIMEO`](#so_rcvtimeo), [`IPPROTO_IP`](#ipproto_ip), [`IPPROTO_TCP`](#ipproto_tcp), [`IPPROTO_IPV6`](#ipproto_ipv6), [`IP_TOS`](#ip_tos), [`IPV6_V6ONLY`](#ipv6_v6only), [`IPV6_TCLASS`](#ipv6_tclass), [`TCP_NODELAY`](#tcp_nodelay), [`TCP_KEEPIDLE`](#tcp_keepidle), [`TCP_KEEPINTVL`](#tcp_keepintvl), [`TCP_KEEPCNT`](#tcp_keepcnt), [`TCP_FASTOPEN`](#tcp_fastopen), [`SHUT_RD`](#shut_rd), [`SHUT_WR`](#shut_wr), [`SHUT_RDWR`](#shut_rdwr), [`SOCKADDR_IN_SIZE`](#sockaddr_in_size), [`sock_send`](#sock_send), [`sock_recv`](#sock_recv), [`IoVector`](#iovector), [`sock_write_vector`](#sock_write_vector), [`sock_send_message`](#sock_send_message), [`sock_receive_message`](#sock_receive_message), [`sock_set_nonblocking`](#sock_set_nonblocking), [`sock_connect_begin`](#sock_connect_begin), [`sock_connect_poll`](#sock_connect_poll), [`CONNECT_PENDING`](#connect_pending), [`sock_close`](#sock_close), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto), [`sock_recvfrom`](#sock_recvfrom), [`sock_peek_readable`](#sock_peek_readable), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable), [`io_queue_create`](#io_queue_create), [`io_queue_wait`](#io_queue_wait), [`IoCompletion`](#iocompletion), [`IO_EVENT_READ`](#io_event_read), [`IO_EVENT_WRITE`](#io_event_write), [`IO_EVENT_ERROR`](#io_event_error), [`IO_EVENT_HANGUP`](#io_event_hangup), [`IO_EVENT_WAKE`](#io_event_wake), [`io_queue_watch`](#io_queue_watch), [`io_queue_rearm`](#io_queue_rearm), [`duplicate_to`](#duplicate_to), [`io_queue_unwatch`](#io_queue_unwatch), [`io_queue_poll`](#io_queue_poll), [`io_queue_wake`](#io_queue_wake), [`io_queue_close`](#io_queue_close), [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | |
| [`DNS_HOSTS_PATH`](#dns_hosts_path) | dns |
| [`random_fill`](#random_fill) | random |
| [`thread_current_id`](#thread_current_id) | threads |
| [`thread_current_name`](#thread_current_name), [`thread_wait`](#thread_wait), [`thread_wait_until`](#thread_wait_until), [`thread_wake`](#thread_wake) | |
| [`clock_gettime`](#clock_gettime) | time |
| [`error_message`](#error_message) | errno |

---

## Functions

### page_size

```mach
pub fun page_size() usize
```

return the system page size

riscv64 linux uses 4 KiB base pages (Sv39/Sv48/Sv57 all share the 4 KiB leaf),
but it reads the runtime AT_PAGESZ the entrypoint captured
(shared.capture_pagesz) for one page-size source of truth. AT_PAGESZ is
mandatory on linux, so a 0 here means the auxv lacked it or a caller ran before
runtime init; page_size() panics rather than fabricating a default.

| Parameter | |
| :--- | :--- |
| **returns** | page size in bytes |

### thread_spawn

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

create a new thread sharing the current address space

uses clone with shared VM, FS, files, and signals. target-owned stack metadata
and portable owner pointers ride on the child stack without global handoff.
the child's area, its block and its copy of the executable's thread-local
template, sits at the top of its stack mapping, above the handoff words, and
clone installs its thread pointer before the child's first instruction. the
trampoline wipes the thread-local block and unmaps the area with the stack at
exit.

| Parameter | |
| :--- | :--- |
| **returns** | thread ID on success, or negative errno on failure |

### thread_join

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

### thread_detach

```mach
pub fun thread_detach(native: usize) i64
```

### thread_block_enter

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's, as the tp just above it

a block thread_spawn or main_thread_block laid out carries the thread-local
block above it. one laid out anywhere else reaches no thread-locals.
the compiler reserves tp, so mach code never writes it otherwise. a loader
sets it before the entry point, and the runtime then leaves the main thread's
alone

| Parameter | |
| :--- | :--- |
| **returns** | 0, since setting tp cannot fail |

### thread_block

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, just below tp, without a system call

this is found from the thread pointer whoever owns it: std's block where std
owns it, and memory of a C runtime's thread on the main thread under a loader
or a thread C code created. std reads nothing through that one, and its
address still names the thread

| Parameter | |
| :--- | :--- |
| **returns** | the block below the thread pointer |

### main_thread_block

```mach
pub fun main_thread_block(fallback: *std.system.os.shared.ThreadBlock) *std.system.os.shared.ThreadBlock
```

the main thread's block, in an area with its thread-local block when the
executable has thread-locals, else the static fallback

| Parameter | |
| :--- | :--- |
| **returns** | the block to install, or nil when the area could not be mapped |

### thread_exit_wipe

```mach
pub fun thread_exit_wipe()
```

wipe the calling thread's thread-local block as the thread ends

### stack_bounds

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, read without a system call

| Parameter | |
| :--- | :--- |
| **returns** | whether the bounds are known (see shared.stack_bounds_of) |

## Forwards

### stat_t

Forwards [`std.system.os.linux.shared.stat_t`](shared.md#stat_t).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

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

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub rec stat_t {
    st_dev:        u64;
    st_ino:        u64;
    st_mode:       u32;
    st_nlink:      u32;
    st_uid:        u32;
    st_gid:        u32;
    st_rdev:       u64;
    _pad1:         u64;
    st_size:       i64;
    st_blksize:    i32;
    _pad2:         i32;
    st_blocks:     i64;
    st_atime:      i64;
    st_atime_nsec: i64;
    st_mtime:      i64;
    st_mtime_nsec: i64;
    st_ctime:      i64;
    st_ctime_nsec: i64;
    _unused4:      u32;
    _unused5:      u32;
}
```

Where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32`:

```mach
pub rec stat_t {
    st_dev:        u64;
    st_ino:        u64;
    st_mode:       u32;
    st_nlink:      u32;
    st_uid:        u32;
    st_gid:        u32;
    st_rdev:       u64;
    _pad1:         u64;
    st_size:       i64;
    st_blksize:    i32;
    _pad2:         i32;
    st_blocks:     i64;
    st_atime:      i64;
    st_atime_nsec: i64;
    st_mtime:      i64;
    st_mtime_nsec: i64;
    st_ctime:      i64;
    st_ctime_nsec: i64;
    _unused4:      u32;
    _unused5:      u32;
}
```

kernel ABI types

### timespec

Forwards [`std.system.os.linux.shared.timespec`](shared.md#timespec).

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

### DirectoryCursor

Forwards [`std.system.os.linux.shared.DirectoryCursor`](shared.md#directorycursor).

```mach
pub rec DirectoryCursor {
    address: usize;
    fd:      i32;
    active:  bool;
    ended:   bool;
    error:   i64;
    buffer:  ptr;
    offset:  usize;
    count:   usize;
}
```

### DirectoryEntry

Forwards [`std.system.os.linux.shared.DirectoryEntry`](shared.md#directoryentry).

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### DirectoryInitResult

Forwards [`std.system.os.linux.shared.DirectoryInitResult`](shared.md#directoryinitresult).

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### separator

Forwards [`std.system.os.linux.shared.separator`](shared.md#constants).

```mach
pub val separator: u8 = '/'
```

path

### STDIN_FD

Forwards [`std.system.os.linux.shared.STDIN_FD`](shared.md#constants).

```mach
pub val STDIN_FD:  i32 = 0
```

constants

### STDOUT_FD

Forwards [`std.system.os.linux.shared.STDOUT_FD`](shared.md#constants).

```mach
pub val STDOUT_FD: i32 = 1
```

### STDERR_FD

Forwards [`std.system.os.linux.shared.STDERR_FD`](shared.md#constants).

```mach
pub val STDERR_FD: i32 = 2
```

### O_RDONLY

Forwards [`std.system.os.linux.shared.O_RDONLY`](shared.md#constants).

```mach
pub val O_RDONLY:   i32 = 0
```

### O_WRONLY

Forwards [`std.system.os.linux.shared.O_WRONLY`](shared.md#constants).

```mach
pub val O_WRONLY:   i32 = 1
```

### O_RDWR

Forwards [`std.system.os.linux.shared.O_RDWR`](shared.md#constants).

```mach
pub val O_RDWR:     i32 = 2
```

### O_CREAT

Forwards [`std.system.os.linux.shared.O_CREAT`](shared.md#constants).

```mach
pub val O_CREAT:    i32 = 64
```

### O_EXCL

Forwards [`std.system.os.linux.shared.O_EXCL`](shared.md#constants).

```mach
pub val O_EXCL:     i32 = 128
```

### O_TRUNC

Forwards [`std.system.os.linux.shared.O_TRUNC`](shared.md#constants).

```mach
pub val O_TRUNC:    i32 = 512
```

### O_APPEND

Forwards [`std.system.os.linux.shared.O_APPEND`](shared.md#constants).

```mach
pub val O_APPEND:   i32 = 1024
```

### O_NONBLOCK

Forwards [`std.system.os.linux.shared.O_NONBLOCK`](shared.md#constants).

```mach
pub val O_NONBLOCK: i32 = 0o4000
```

### O_DIRECTORY

Forwards [`std.system.os.linux.shared.O_DIRECTORY`](shared.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub val O_DIRECTORY: i32 = 0o40000
```

Otherwise:

```mach
pub val O_DIRECTORY: i32 = 0o200000
```

O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to
asm-generic. asm-generic/fcntl.h defines each under `#ifndef` precisely so an arch
can override, and arm does. aarch64 inherits arm's set. x86_64 and riscv64 take
asm-generic's values.

Getting this backwards is not a compile error and not a wrong result - the open is
simply refused EINVAL, so directory listing stops working on the arch you guessed
wrong. Both directions of that have now been observed on real hardware, so do not
"simplify" this to one value: verify on the arch before changing it, and note that
qemu-user is not evidence here (its aarch64 and riscv64 targets disagree with each
other about exactly this).

### O_NOFOLLOW

Forwards [`std.system.os.linux.shared.O_NOFOLLOW`](shared.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub val O_NOFOLLOW:  i32 = 0o100000
```

Otherwise:

```mach
pub val O_NOFOLLOW:  i32 = 0o400000
```

O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to
asm-generic. asm-generic/fcntl.h defines each under `#ifndef` precisely so an arch
can override, and arm does. aarch64 inherits arm's set. x86_64 and riscv64 take
asm-generic's values.

Getting this backwards is not a compile error and not a wrong result - the open is
simply refused EINVAL, so directory listing stops working on the arch you guessed
wrong. Both directions of that have now been observed on real hardware, so do not
"simplify" this to one value: verify on the arch before changing it, and note that
qemu-user is not evidence here (its aarch64 and riscv64 targets disagree with each
other about exactly this).

### AT_FDCWD

Forwards [`std.system.os.linux.shared.AT_FDCWD`](shared.md#constants).

```mach
pub val AT_FDCWD:            i32 = -100
```

### AT_SYMLINK_NOFOLLOW

Forwards [`std.system.os.linux.shared.AT_SYMLINK_NOFOLLOW`](shared.md#constants).

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0100
```

### AT_REMOVEDIR

Forwards [`std.system.os.linux.shared.AT_REMOVEDIR`](shared.md#constants).

```mach
pub val AT_REMOVEDIR:        i32 = 0x0200
```

### LOCK_SH

Forwards [`std.system.os.linux.shared.LOCK_SH`](shared.md#constants).

```mach
pub val LOCK_SH: i32 = 1
```

advisory file-lock operations

### LOCK_EX

Forwards [`std.system.os.linux.shared.LOCK_EX`](shared.md#constants).

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards [`std.system.os.linux.shared.LOCK_NB`](shared.md#constants).

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards [`std.system.os.linux.shared.LOCK_UN`](shared.md#constants).

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards [`std.system.os.linux.shared.S_IFMT`](shared.md#constants).

```mach
pub val S_IFMT:  u32 = 0o170000
```

### S_IFDIR

Forwards [`std.system.os.linux.shared.S_IFDIR`](shared.md#constants).

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards [`std.system.os.linux.shared.S_IFREG`](shared.md#constants).

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards [`std.system.os.linux.shared.S_IFLNK`](shared.md#constants).

```mach
pub val S_IFLNK: u32 = 0o120000
```

### WNOHANG

Forwards [`std.system.os.linux.shared.WNOHANG`](shared.md#constants).

```mach
pub val WNOHANG:    i32 = 1
```

### WUNTRACED

Forwards [`std.system.os.linux.shared.WUNTRACED`](shared.md#constants).

```mach
pub val WUNTRACED:  i32 = 2
```

### WCONTINUED

Forwards [`std.system.os.linux.shared.WCONTINUED`](shared.md#constants).

```mach
pub val WCONTINUED: i32 = 8
```

### CLOCK_REALTIME

Forwards [`std.system.os.linux.shared.CLOCK_REALTIME`](shared.md#constants).

```mach
pub val CLOCK_REALTIME:  i32 = 0
```

### CLOCK_MONOTONIC

Forwards [`std.system.os.linux.shared.CLOCK_MONOTONIC`](shared.md#constants).

```mach
pub val CLOCK_MONOTONIC: i32 = 1
```

### EPERM

Forwards [`std.system.os.linux.shared.EPERM`](shared.md#constants).

```mach
pub val EPERM:        i64 = -1
```

### ENOENT

Forwards [`std.system.os.linux.shared.ENOENT`](shared.md#constants).

```mach
pub val ENOENT:       i64 = -2
```

### ESRCH

Forwards [`std.system.os.linux.shared.ESRCH`](shared.md#constants).

```mach
pub val ESRCH:        i64 = -3
```

### EINTR

Forwards [`std.system.os.linux.shared.EINTR`](shared.md#constants).

```mach
pub val EINTR:        i64 = -4
```

### EIO

Forwards [`std.system.os.linux.shared.EIO`](shared.md#constants).

```mach
pub val EIO:          i64 = -5
```

### ENXIO

Forwards [`std.system.os.linux.shared.ENXIO`](shared.md#constants).

```mach
pub val ENXIO:        i64 = -6
```

### E2BIG

Forwards [`std.system.os.linux.shared.E2BIG`](shared.md#constants).

```mach
pub val E2BIG:        i64 = -7
```

### EBADF

Forwards [`std.system.os.linux.shared.EBADF`](shared.md#constants).

```mach
pub val EBADF:        i64 = -9
```

### ECHILD

Forwards [`std.system.os.linux.shared.ECHILD`](shared.md#constants).

```mach
pub val ECHILD:       i64 = -10
```

### EAGAIN

Forwards [`std.system.os.linux.shared.EAGAIN`](shared.md#constants).

```mach
pub val EAGAIN:       i64 = -11
```

### ENOMEM

Forwards [`std.system.os.linux.shared.ENOMEM`](shared.md#constants).

```mach
pub val ENOMEM:       i64 = -12
```

### EACCES

Forwards [`std.system.os.linux.shared.EACCES`](shared.md#constants).

```mach
pub val EACCES:       i64 = -13
```

### EFAULT

Forwards [`std.system.os.linux.shared.EFAULT`](shared.md#constants).

```mach
pub val EFAULT:       i64 = -14
```

### EBUSY

Forwards [`std.system.os.linux.shared.EBUSY`](shared.md#constants).

```mach
pub val EBUSY:        i64 = -16
```

### EEXIST

Forwards [`std.system.os.linux.shared.EEXIST`](shared.md#constants).

```mach
pub val EEXIST:       i64 = -17
```

### ENODEV

Forwards [`std.system.os.linux.shared.ENODEV`](shared.md#constants).

```mach
pub val ENODEV:       i64 = -19
```

### ENOTDIR

Forwards [`std.system.os.linux.shared.ENOTDIR`](shared.md#constants).

```mach
pub val ENOTDIR:      i64 = -20
```

### EISDIR

Forwards [`std.system.os.linux.shared.EISDIR`](shared.md#constants).

```mach
pub val EISDIR:       i64 = -21
```

### EINVAL

Forwards [`std.system.os.linux.shared.EINVAL`](shared.md#constants).

```mach
pub val EINVAL:       i64 = -22
```

### ENFILE

Forwards [`std.system.os.linux.shared.ENFILE`](shared.md#constants).

```mach
pub val ENFILE:       i64 = -23
```

### EMFILE

Forwards [`std.system.os.linux.shared.EMFILE`](shared.md#constants).

```mach
pub val EMFILE:       i64 = -24
```

### ETXTBSY

Forwards [`std.system.os.linux.shared.ETXTBSY`](shared.md#constants).

```mach
pub val ETXTBSY:      i64 = -26
```

### ENOSPC

Forwards [`std.system.os.linux.shared.ENOSPC`](shared.md#constants).

```mach
pub val ENOSPC:       i64 = -28
```

### EROFS

Forwards [`std.system.os.linux.shared.EROFS`](shared.md#constants).

```mach
pub val EROFS:        i64 = -30
```

### EPIPE

Forwards [`std.system.os.linux.shared.EPIPE`](shared.md#constants).

```mach
pub val EPIPE:        i64 = -32
```

### ENAMETOOLONG

Forwards [`std.system.os.linux.shared.ENAMETOOLONG`](shared.md#constants).

```mach
pub val ENAMETOOLONG: i64 = -36
```

### ERANGE

Forwards [`std.system.os.linux.shared.ERANGE`](shared.md#constants).

```mach
pub val ERANGE:       i64 = -34
```

### ENOTEMPTY

Forwards [`std.system.os.linux.shared.ENOTEMPTY`](shared.md#constants).

```mach
pub val ENOTEMPTY:    i64 = -39
```

### ELOOP

Forwards [`std.system.os.linux.shared.ELOOP`](shared.md#constants).

```mach
pub val ELOOP:        i64 = -40
```

### ENOTSUP

Forwards [`std.system.os.linux.shared.ENOTSUP`](shared.md#constants).

```mach
pub val ENOTSUP:      i64 = -95
```

### EINTR_MAX_RETRIES

Forwards [`std.system.os.linux.shared.EINTR_MAX_RETRIES`](shared.md#constants).

```mach
pub val EINTR_MAX_RETRIES: usize = 8
```

### has_numa

Forwards [`std.system.os.linux.shared.has_numa`](shared.md#has_numa).

```mach
pub fun has_numa() bool
```

feature detection

### has_huge_pages

Forwards [`std.system.os.linux.shared.has_huge_pages`](shared.md#has_huge_pages).

```mach
pub fun has_huge_pages() bool
```

check if the kernel supports huge page allocation

### syscall0

Forwards [`std.system.os.linux.shared.syscall0`](shared.md#syscall0).

```mach
pub fun syscall0(n: usize) i64
```

syscall wrappers

### syscall1

Forwards [`std.system.os.linux.shared.syscall1`](shared.md#syscall1).

```mach
pub fun syscall1(n: usize, a0: usize) i64
```

execute a syscall with 1 argument

### syscall2

Forwards [`std.system.os.linux.shared.syscall2`](shared.md#syscall2).

```mach
pub fun syscall2(n: usize, a0: usize, a1: usize) i64
```

execute a syscall with 2 arguments

### syscall3

Forwards [`std.system.os.linux.shared.syscall3`](shared.md#syscall3).

```mach
pub fun syscall3(n: usize, a0: usize, a1: usize, a2: usize) i64
```

execute a syscall with 3 arguments

### syscall4

Forwards [`std.system.os.linux.shared.syscall4`](shared.md#syscall4).

```mach
pub fun syscall4(n: usize, a0: usize, a1: usize, a2: usize, a3: usize) i64
```

execute a syscall with 4 arguments

### syscall5

Forwards [`std.system.os.linux.shared.syscall5`](shared.md#syscall5).

```mach
pub fun syscall5(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize) i64
```

execute a syscall with 5 arguments

### syscall6

Forwards [`std.system.os.linux.shared.syscall6`](shared.md#syscall6).

```mach
pub fun syscall6(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize, a5: usize) i64
```

execute a syscall with 6 arguments

### allocate

Forwards [`std.system.os.linux.shared.allocate`](shared.md#allocate).

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards [`std.system.os.linux.shared.deallocate`](shared.md#deallocate).

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

free memory via munmap

### reallocate

Forwards [`std.system.os.linux.shared.reallocate`](shared.md#reallocate).

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a memory region via mremap

### heap_region_base

Forwards [`std.system.os.linux.shared.heap_region_base`](shared.md#heap_region_base).

```mach
pub fun heap_region_base() usize
```

query the current program break via brk(0)

### heap_region_extend

Forwards [`std.system.os.linux.shared.heap_region_extend`](shared.md#heap_region_extend).

```mach
pub fun heap_region_extend(addr: usize) usize
```

set the program break to addr via brk

### protect

Forwards [`std.system.os.linux.shared.protect`](shared.md#protect).

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

change protection on a memory region via mprotect

### lock

Forwards [`std.system.os.linux.shared.lock`](shared.md#lock).

```mach
pub fun lock(p: ptr, size: usize) i64
```

lock a memory region into physical RAM via mlock

### unlock

Forwards [`std.system.os.linux.shared.unlock`](shared.md#unlock).

```mach
pub fun unlock(p: ptr, size: usize) i64
```

unlock a previously locked memory region via munlock

### advise

Forwards [`std.system.os.linux.shared.advise`](shared.md#advise).

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

advise the kernel on expected access patterns via madvise

### allocate_huge

Forwards [`std.system.os.linux.shared.allocate_huge`](shared.md#allocate_huge).

```mach
pub fun allocate_huge(size: usize, page_size: usize) ptr
```

allocate memory backed by huge pages via mmap

### numa_node_count

Forwards [`std.system.os.linux.shared.numa_node_count`](shared.md#numa_node_count).

```mach
pub fun numa_node_count() usize
```

return the number of NUMA nodes via get_mempolicy

### numa_current_node

Forwards [`std.system.os.linux.shared.numa_current_node`](shared.md#numa_current_node).

```mach
pub fun numa_current_node() usize
```

return the NUMA node of the current CPU via getcpu

### numa_allocate

Forwards [`std.system.os.linux.shared.numa_allocate`](shared.md#numa_allocate).

```mach
pub fun numa_allocate(size: usize, node: usize) ptr
```

allocate memory pinned to a specific NUMA node

### numa_move

Forwards [`std.system.os.linux.shared.numa_move`](shared.md#numa_move).

```mach
pub fun numa_move(p: ptr, size: usize, node: usize) i64
```

move a memory region to a different NUMA node via mbind

### map_file

Forwards [`std.system.os.linux.shared.map_file`](shared.md#map_file).

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map a file descriptor into memory via mmap

### sync_file

Forwards [`std.system.os.linux.shared.sync_file`](shared.md#sync_file).

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via msync

### _envp

Forwards [`std.system.os.linux.shared._envp`](shared.md#variables).

```mach
pub var _envp: usize = 0
```

environment

### environ

Forwards [`std.system.os.linux.shared.environ`](shared.md#environ).

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### capture_pagesz

Forwards [`std.system.os.linux.shared.capture_pagesz`](shared.md#capture_pagesz).

```mach
pub fun capture_pagesz()
```

publish the auxv page size into `_pagesz`

called once by the entrypoint at startup, after `_envp` is set and (in a PIE)
after `_rt_relocate` has applied any relocations, so it runs as ordinary
post-relocation code that may touch globals. `_pagesz` stays 0 only if the auxv
lacks the mandatory AT_PAGESZ, which page_size() treats as a fatal invariant
breach rather than fabricating a default. a shared artifact has no entrypoint
and no envp, so its first page_size() calls this and reads the kernel's copy.

### loader_present

Forwards [`std.system.os.linux.shared.loader_present`](shared.md#loader_present).

```mach
pub fun loader_present() bool
```

whether a program interpreter started this process

whoever starts the process owns the main thread's thread pointer, so the
runtime installs std's block there only when this is false

### capture_main_stack

Forwards [`std.system.os.linux.shared.capture_main_stack`](shared.md#capture_main_stack).

```mach
pub fun capture_main_stack()
```

capture the main thread's stack bounds, once, at entry

the kernel grows the main stack down from the end of its mapping by at most
RLIMIT_STACK. the first thing the kernel writes below that end is the
executable's path (AT_EXECFN) and one null word, so the page boundary above
the path's terminator ends the mapping. the soft limit is read once, and an
unlimited one, or an auxv without AT_EXECFN, leaves the bounds unknown. runs
after capture_pagesz, and records whether a loader owns the thread pointer

### capture_tls

Forwards [`std.system.os.linux.shared.capture_tls`](shared.md#capture_tls).

```mach
pub fun capture_tls()
```

read the executable's thread-local template from its program headers

AT_PHDR and AT_PHNUM locate the headers, and PT_PHDR gives the load bias of a
position-independent image, which a fixed image without one does not need.
runs once at entry, after relocation and before the main thread's block is
installed

### read

Forwards [`std.system.os.linux.shared.read`](shared.md#read).

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

filesystem

### write

Forwards [`std.system.os.linux.shared.write`](shared.md#write).

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a file descriptor

retries automatically on EINTR.

### read_at

Forwards [`std.system.os.linux.shared.read_at`](shared.md#read_at).

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

positioned file access does not mutate the descriptor offset

### write_at

Forwards [`std.system.os.linux.shared.write_at`](shared.md#write_at).

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

### open

Forwards [`std.system.os.linux.shared.open`](shared.md#open).

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

openat: open a file relative to a directory file descriptor

retries automatically on EINTR.

### close

Forwards [`std.system.os.linux.shared.close`](shared.md#close).

```mach
pub fun close(fd: i32) i64
```

close a file descriptor

### sync_fd

Forwards [`std.system.os.linux.shared.sync_fd`](shared.md#sync_fd).

```mach
pub fun sync_fd(fd: i32) i64
```

flush an open file's data and metadata to its backing storage

### stat

Forwards [`std.system.os.linux.shared.stat`](shared.md#stat).

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

fstat: get file status by file descriptor

### set_mode

Forwards [`std.system.os.linux.shared.set_mode`](shared.md#set_mode).

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

set permission bits through a held descriptor

### set_mode_at

Forwards [`std.system.os.linux.shared.set_mode_at`](shared.md#set_mode_at).

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

no following fallback is permitted when the flags-aware syscall is unavailable

### file_identity

Forwards [`std.system.os.linux.shared.file_identity`](shared.md#file_identity).

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

observational ids do not retain an object after this call

### identity_at

Forwards [`std.system.os.linux.shared.identity_at`](shared.md#identity_at).

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### retain_identity_at

Forwards [`std.system.os.linux.shared.retain_identity_at`](shared.md#retain_identity_at).

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_path pins the entry without acquiring content-read permission

### publication_capabilities

Forwards [`std.system.os.linux.shared.publication_capabilities`](shared.md#publication_capabilities).

```mach
pub fun publication_capabilities(fd: i32) i64
```

### stat_path

Forwards [`std.system.os.linux.shared.stat_path`](shared.md#stat_path).

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

newfstatat: get file status relative to a directory fd

### stat_mode

Forwards [`std.system.os.linux.shared.stat_mode`](shared.md#stat_mode).

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 32-bit in the linux stat ABI; the accessor exists so portable
callers read the mode uniformly across platforms (darwin's mode is 16-bit).

### unlink

Forwards [`std.system.os.linux.shared.unlink`](shared.md#unlink).

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

unlinkat: remove a file or directory relative to a directory fd

### rename

Forwards [`std.system.os.linux.shared.rename`](shared.md#rename).

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

renameat: rename a file relative to directory fds

### symlink

Forwards [`std.system.os.linux.shared.symlink`](shared.md#symlink).

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### make_dir

Forwards [`std.system.os.linux.shared.make_dir`](shared.md#make_dir).

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

mkdirat: create a directory relative to a directory fd

### directory_init

Forwards [`std.system.os.linux.shared.directory_init`](shared.md#directory_init).

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next

Forwards [`std.system.os.linux.shared.directory_next`](shared.md#directory_next).

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

### directory_dnit

Forwards [`std.system.os.linux.shared.directory_dnit`](shared.md#directory_dnit).

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

consumes the owner, including when native release reports failure

### access

Forwards [`std.system.os.linux.shared.access`](shared.md#access).

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

faccessat: check file accessibility relative to a directory fd

### seek

Forwards [`std.system.os.linux.shared.seek`](shared.md#seek).

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

lseek: reposition read/write offset of a file descriptor

### lock_fd

Forwards [`std.system.os.linux.shared.lock_fd`](shared.md#lock_fd).

```mach
pub fun lock_fd(fd: i32, op: i32) i64
```

flock: take or release an advisory whole-file lock on an open descriptor

the lock lives on the open file DESCRIPTION, not on the directory entry, so
the kernel drops it when the last descriptor referring to that description is
closed -- including the implicit close every exiting process performs, however
it exits. a holder that crashes therefore leaves no lock behind, which is what
makes a live holder distinguishable from a dead one's residue.

a directory descriptor is lockable on linux, but windows cannot lock one, so
portable callers that want to exclude writers from a directory lock a regular
file inside it rather than the directory itself.

### terminate

Forwards [`std.system.os.linux.shared.terminate`](shared.md#terminate).

```mach
pub fun terminate(code: i64)
```

process

### abort

Forwards [`std.system.os.linux.shared.abort`](shared.md#abort).

```mach
pub fun abort()
```

abort the process immediately with exit code 255

### terminate_child

Forwards [`std.system.os.linux.shared.terminate_child`](shared.md#terminate_child).

```mach
pub fun terminate_child(pid: i64) i64
```

forcefully stop a spawned child without reaping it

waitid with WNOWAIT first asks the kernel to verify that `pid` is still a
child of this process. this rejects unknown and already-reaped PIDs before
kill can affect them, while preserving an exited child's wait status.
callers must not concurrently reap this child through wait or wait_pid: a
reaper could release the numeric PID between the ownership check and kill.

### setpgid

Forwards [`std.system.os.linux.shared.setpgid`](shared.md#setpgid).

```mach
pub fun setpgid(pid: i64, pgid: i64) i64
```

setpgid: set (or join) the process group ID of a process

### getpgid

Forwards [`std.system.os.linux.shared.getpgid`](shared.md#getpgid).

```mach
pub fun getpgid(pid: i64) i64
```

getpgid: read the process group ID of a process

### terminate_group

Forwards [`std.system.os.linux.shared.terminate_group`](shared.md#terminate_group).

```mach
pub fun terminate_group(pgid: i64) i64
```

signal every process in a group without reaping any of them

unlike terminate_child, there is no waitid ownership probe first: a process
group is not tracked as a child of this process, so kill(-pgid, SIGTERM) is
the only available primitive. surviving members stay individually waitable
through wait/wait_any exactly as before.

### kill_group

Forwards [`std.system.os.linux.shared.kill_group`](shared.md#kill_group).

```mach
pub fun kill_group(pgid: i64) i64
```

forcefully stop every process in a group without reaping any of them

the group's members get SIGKILL, which none of them can catch or ignore.
as with terminate_group there is no ownership probe, and members stay
individually waitable.

### probe_group

Forwards [`std.system.os.linux.shared.probe_group`](shared.md#probe_group).

```mach
pub fun probe_group(pgid: i64) i64
```

whether any process is left in a group, without signalling it

kill(-pgid, 0) checks for members and delivers nothing. a member this
process may not signal still counts, so EPERM reads as present.

### process_watch

Forwards [`std.system.os.linux.shared.process_watch`](shared.md#process_watch).

```mach
pub fun process_watch(queue: *std.system.os.shared.IoQueue, pid: i64, context: usize) i64
```

make the end of the child `pid` a readiness event on `queue`, so the queue's
wait returns once the child ends. a pidfd names the child: it reads ready
from the moment the child ends, reaped or not, and is not inherited across exec

### process_unwatch

Forwards [`std.system.os.linux.shared.process_unwatch`](shared.md#process_unwatch).

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired

### spawn

Forwards [`std.system.os.linux.shared.spawn`](shared.md#spawn).

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

### spawn_grouped

Forwards [`std.system.os.linux.shared.spawn_grouped`](shared.md#spawn_grouped).

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program, placed as the leader of
its own new process group (see spawn_redirected_in_grouped)

### spawn_in

Forwards [`std.system.os.linux.shared.spawn_in`](shared.md#spawn_in).

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected

Forwards [`std.system.os.linux.shared.spawn_redirected`](shared.md#spawn_redirected).

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

### spawn_redirected_grouped

Forwards [`std.system.os.linux.shared.spawn_redirected_grouped`](shared.md#spawn_redirected_grouped).

```mach
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed as the leader of its own new process group (see
spawn_redirected_in_grouped)

### spawn_redirected_in

Forwards [`std.system.os.linux.shared.spawn_redirected_in`](shared.md#spawn_redirected_in).

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

### spawn_redirected_in_grouped

Forwards [`std.system.os.linux.shared.spawn_redirected_in_grouped`](shared.md#spawn_redirected_in_grouped).

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

identical to spawn_redirected_in except the child calls setpgid(0, 0)
between the clone and the exec (see spawn_trampoline), and the parent ALSO
calls setpgid(pid, pid) once clone returns, ignoring its result (mach#535).
on a real kernel CLONE_VFORK suspends the parent until the child execs or
exits, so the parent-side call is redundant there (it either finds the
child already exec'd, where POSIX's own rule against changing pgid post-exec
makes it a harmless no-op, or - vanishingly rarely - still pre-exec, where it
just repeats what the child was about to do anyway). it is NOT redundant
everywhere this runs: qemu-user (the riscv64 CI lane) silently downgrades
CLONE_VFORK to a plain fork, so the parent truly can run concurrently with
the child there, and a caller's getpgid(pid) right after this call returning
could otherwise observe the parent's own group for a still-ungrouped child.
the same double-setpgid mitigation the darwin backend already needs for its
real fork() closes that window here too.

### getpid

Forwards [`std.system.os.linux.shared.getpid`](shared.md#getpid).

```mach
pub fun getpid() i64
```

return the current process ID

### pipe

Forwards [`std.system.os.linux.shared.pipe`](shared.md#pipe).

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

### ignore_sigpipe

Forwards [`std.system.os.linux.shared.ignore_sigpipe`](shared.md#ignore_sigpipe).

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

rt_sigaction's first two words are the handler and flags on every supported
ISA. x86_64 and aarch64 then carry a restorer word before the signal mask;
riscv64 puts the mask in the third word. a zeroed four-word buffer satisfies
both layouts because this disposition has no flags, restorer, or masked
signals. the kernel reads only its own layout and the trailing word is inert.

the disposition is process-wide: after success, writes from every thread
return EPIPE when their pipe has no reader instead of terminating the process.

### sleep

Forwards [`std.system.os.linux.shared.sleep`](shared.md#sleep).

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

### cpu_count

Forwards [`std.system.os.linux.shared.cpu_count`](shared.md#cpu_count).

```mach
pub fun cpu_count() i64
```

the number of CPUs available to this process

popcounts the sched_getaffinity mask, so taskset/cgroup cpuset restrictions
are honoured; the kernel reports the mask size it wrote in the return value.
never returns less than 1.

### cpu_features

Forwards [`std.system.os.linux.shared.cpu_features`](shared.md#cpu_features).

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

the running processor's instruction-set extensions

x86_64 reads cpuid, which needs no OS. aarch64 reads AT_HWCAP from the
auxiliary vector past envp, which the kernel filled before the process
started, so the answer is ready before main. HWCAP_AES is bit 3,
HWCAP_PMULL bit 4 and HWCAP_SHA2 bit 6, and a bit the kernel leaves clear
reads false. riscv asks riscv_hwprobe for the base behaviour and IMA_EXT_0
keys, and on a kernel without the call reads the single-letter extensions
from AT_HWCAP. a caller that runs before the runtime captured envp sees ENOSYS

### cpu_dit

Forwards [`std.system.os.linux.shared.cpu_dit`](shared.md#cpu_dit).

```mach
pub fun cpu_dit() i64
```

whether the processor and kernel provide the data-independent-timing mode

aarch64 reads HWCAP_DIT (bit 24) from AT_HWCAP through the same auxv reader
`cpu_features` uses; the kernel sets it when ID_AA64PFR0_EL1.DIT is 1. a
caller that runs before the runtime captured envp sees ENOSYS. no other
architecture has the mode

### thread_affinity

Forwards [`std.system.os.linux.shared.thread_affinity`](shared.md#thread_affinity).

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

read the calling thread's CPU affinity

CPU i is bit i % 64 of words[i / 64]. the kernel reports the bytes it wrote,
which is its own cpumask size, so out_count is that size in words and every
word the kernel wrote is copied, including trailing zero words.

### set_thread_affinity

Forwards [`std.system.os.linux.shared.set_thread_affinity`](shared.md#set_thread_affinity).

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

pin the calling thread to the CPUs set in words

### getcwd

Forwards [`std.system.os.linux.shared.getcwd`](shared.md#getcwd).

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

the raw syscall returns the length INCLUDING the terminator; this layer
reports the path length the way darwin and windows do, so "length of path"
means one thing across the three backends (#432).

### getenv

Forwards [`std.system.os.linux.shared.getenv`](shared.md#getenv).

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

### fork

Forwards [`std.system.os.linux.shared.fork`](shared.md#fork).

```mach
pub fun fork() i64
```

create a new child process

### vfork

Forwards [`std.system.os.linux.shared.vfork`](shared.md#vfork).

```mach
pub fun vfork() i64
```

create child process sharing memory with parent

### exec

Forwards [`std.system.os.linux.shared.exec`](shared.md#exec).

```mach
pub fun exec(pathname: *u8, argv: **u8, envp: Environment) i64
```

execve: replace the current process image with a new program

### wait

Forwards [`std.system.os.linux.shared.wait`](shared.md#wait).

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

failures and no-event results leave the caller's status unchanged

### wait_pid

Forwards [`std.system.os.linux.shared.wait_pid`](shared.md#wait_pid).

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

### ProcessStatus

Forwards [`std.system.os.linux.shared.ProcessStatus`](shared.md#processstatus).

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

### FileLimit

Forwards [`std.system.os.linux.shared.FileLimit`](shared.md#filelimit).

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

Forwards [`std.system.os.linux.shared.LIMIT_UNLIMITED`](shared.md#limit_unlimited).

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards [`std.system.os.linux.shared.open_file_limit`](shared.md#open_file_limit).

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

read this process's open-file limit. linux's RLIM_INFINITY is all ones, the
same value as LIMIT_UNLIMITED, and an unprivileged process may raise its soft
limit up to the hard one

### set_open_file_limit

Forwards [`std.system.os.linux.shared.set_open_file_limit`](shared.md#set_open_file_limit).

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

set this process's open-file limit. ceiling is ignored

### ProcessWaitError

Forwards [`std.system.os.linux.shared.ProcessWaitError`](shared.md#processwaiterror).

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

### WaitResult

Forwards [`std.system.os.linux.shared.WaitResult`](shared.md#waitresult).

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards [`std.system.os.linux.shared.PROCESS_OP_WAIT`](shared.md#process_op_wait).

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards [`std.system.os.linux.shared.PROCESS_OP_STATUS`](shared.md#process_op_status).

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards [`std.system.os.linux.shared.PROCESS_OP_CLOSE`](shared.md#process_op_close).

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards [`std.system.os.linux.shared.PROCESS_OP_SPAWN`](shared.md#process_op_spawn).

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards [`std.system.os.linux.shared.PROCESS_OP_READ`](shared.md#process_op_read).

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards [`std.system.os.linux.shared.PROCESS_OP_PIPE`](shared.md#process_op_pipe).

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards [`std.system.os.linux.shared.PROCESS_OP_TERMINATE`](shared.md#process_op_terminate).

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards [`std.system.os.linux.shared.PROCESS_EXITED`](shared.md#process_exited).

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards [`std.system.os.linux.shared.PROCESS_SIGNALED`](shared.md#process_signaled).

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards [`std.system.os.linux.shared.PROCESS_STOPPED`](shared.md#process_stopped).

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards [`std.system.os.linux.shared.PROCESS_CONTINUED`](shared.md#process_continued).

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### AF_INET

Forwards [`std.system.os.linux.shared.AF_INET`](shared.md#constants).

```mach
pub val AF_INET:             i32 = 2
```

sockets

### SOCK_STREAM

Forwards [`std.system.os.linux.shared.SOCK_STREAM`](shared.md#constants).

```mach
pub val SOCK_STREAM:         i32 = 1
```

### SOCK_DGRAM

Forwards [`std.system.os.linux.shared.SOCK_DGRAM`](shared.md#constants).

```mach
pub val SOCK_DGRAM:          i32 = 2
```

### SOCK_NONBLOCK

Forwards [`std.system.os.linux.shared.SOCK_NONBLOCK`](shared.md#constants).

```mach
pub val SOCK_NONBLOCK:       i32 = O_NONBLOCK
```

### SOCK_CLOEXEC

Forwards [`std.system.os.linux.shared.SOCK_CLOEXEC`](shared.md#constants).

```mach
pub val SOCK_CLOEXEC:        i32 = 0x80000
```

### SOL_SOCKET

Forwards [`std.system.os.linux.shared.SOL_SOCKET`](shared.md#constants).

```mach
pub val SOL_SOCKET:          i32 = 1
```

### SO_UNSUPPORTED

Forwards [`std.system.os.linux.shared.SO_UNSUPPORTED`](shared.md#constants).

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

### SO_REUSEADDR

Forwards [`std.system.os.linux.shared.SO_REUSEADDR`](shared.md#constants).

```mach
pub val SO_REUSEADDR:        i32 = 2
```

### SO_REUSEPORT

Forwards [`std.system.os.linux.shared.SO_REUSEPORT`](shared.md#constants).

```mach
pub val SO_REUSEPORT:        i32 = 15
```

### SO_EXCLUSIVEADDRUSE

Forwards [`std.system.os.linux.shared.SO_EXCLUSIVEADDRUSE`](shared.md#constants).

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = SO_UNSUPPORTED
```

### SO_KEEPALIVE

Forwards [`std.system.os.linux.shared.SO_KEEPALIVE`](shared.md#constants).

```mach
pub val SO_KEEPALIVE:        i32 = 9
```

### SO_SNDBUF

Forwards [`std.system.os.linux.shared.SO_SNDBUF`](shared.md#constants).

```mach
pub val SO_SNDBUF:           i32 = 7
```

### SO_RCVBUF

Forwards [`std.system.os.linux.shared.SO_RCVBUF`](shared.md#constants).

```mach
pub val SO_RCVBUF:           i32 = 8
```

### SO_LINGER

Forwards [`std.system.os.linux.shared.SO_LINGER`](shared.md#constants).

```mach
pub val SO_LINGER:           i32 = 13
```

### SO_RCVTIMEO

Forwards [`std.system.os.linux.shared.SO_RCVTIMEO`](shared.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.riscv32`:

```mach
pub val SO_RCVTIMEO: i32 = 66
```

Otherwise:

```mach
pub val SO_RCVTIMEO: i32 = 20
```

riscv32 takes the 64-bit timeval sock_set_rcvtimeo writes only as SO_RCVTIMEO_NEW

### IPPROTO_IP

Forwards [`std.system.os.linux.shared.IPPROTO_IP`](shared.md#constants).

```mach
pub val IPPROTO_IP:    i32 = 0
```

### IPPROTO_TCP

Forwards [`std.system.os.linux.shared.IPPROTO_TCP`](shared.md#constants).

```mach
pub val IPPROTO_TCP:   i32 = 6
```

### IPPROTO_IPV6

Forwards [`std.system.os.linux.shared.IPPROTO_IPV6`](shared.md#constants).

```mach
pub val IPPROTO_IPV6:  i32 = 41
```

### IP_TOS

Forwards [`std.system.os.linux.shared.IP_TOS`](shared.md#constants).

```mach
pub val IP_TOS:        i32 = 1
```

### IPV6_V6ONLY

Forwards [`std.system.os.linux.shared.IPV6_V6ONLY`](shared.md#constants).

```mach
pub val IPV6_V6ONLY:   i32 = 26
```

### IPV6_TCLASS

Forwards [`std.system.os.linux.shared.IPV6_TCLASS`](shared.md#constants).

```mach
pub val IPV6_TCLASS:   i32 = 67
```

### TCP_NODELAY

Forwards [`std.system.os.linux.shared.TCP_NODELAY`](shared.md#constants).

```mach
pub val TCP_NODELAY:   i32 = 1
```

### TCP_KEEPIDLE

Forwards [`std.system.os.linux.shared.TCP_KEEPIDLE`](shared.md#constants).

```mach
pub val TCP_KEEPIDLE:  i32 = 4
```

### TCP_KEEPINTVL

Forwards [`std.system.os.linux.shared.TCP_KEEPINTVL`](shared.md#constants).

```mach
pub val TCP_KEEPINTVL: i32 = 5
```

### TCP_KEEPCNT

Forwards [`std.system.os.linux.shared.TCP_KEEPCNT`](shared.md#constants).

```mach
pub val TCP_KEEPCNT:   i32 = 6
```

### TCP_FASTOPEN

Forwards [`std.system.os.linux.shared.TCP_FASTOPEN`](shared.md#constants).

```mach
pub val TCP_FASTOPEN:  i32 = 23
```

### SHUT_RD

Forwards [`std.system.os.linux.shared.SHUT_RD`](shared.md#constants).

```mach
pub val SHUT_RD:       i32 = 0
```

### SHUT_WR

Forwards [`std.system.os.linux.shared.SHUT_WR`](shared.md#constants).

```mach
pub val SHUT_WR:       i32 = 1
```

### SHUT_RDWR

Forwards [`std.system.os.linux.shared.SHUT_RDWR`](shared.md#constants).

```mach
pub val SHUT_RDWR:     i32 = 2
```

### SOCKADDR_IN_SIZE

Forwards [`std.system.os.linux.shared.SOCKADDR_IN_SIZE`](shared.md#constants).

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

### sock_send

Forwards [`std.system.os.linux.shared.sock_send`](shared.md#sock_send).

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

send data on a connected socket

### sock_recv

Forwards [`std.system.os.linux.shared.sock_recv`](shared.md#sock_recv).

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

receive data from a connected socket

### IoVector

Forwards [`std.system.os.linux.shared.IoVector`](shared.md#iovector).

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

### sock_write_vector

Forwards [`std.system.os.linux.shared.sock_write_vector`](shared.md#sock_write_vector).

```mach
pub fun sock_write_vector(fd: usize, vectors: *IoVector, count: usize) i64
```

### sock_send_message

Forwards [`std.system.os.linux.shared.sock_send_message`](shared.md#sock_send_message).

```mach
pub fun sock_send_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: u32, control: *u8, control_length: usize) i64
```

### sock_receive_message

Forwards [`std.system.os.linux.shared.sock_receive_message`](shared.md#sock_receive_message).

```mach
pub fun sock_receive_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: *u32, control: *u8, control_length: *usize, flags: *i32) i64
```

### sock_set_nonblocking

Forwards [`std.system.os.linux.shared.sock_set_nonblocking`](shared.md#sock_set_nonblocking).

```mach
pub fun sock_set_nonblocking(fd: usize, enabled: bool) i64
```

switch a socket between blocking and nonblocking

### sock_connect_begin

Forwards [`std.system.os.linux.shared.sock_connect_begin`](shared.md#sock_connect_begin).

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

start a connect on a nonblocking socket

### sock_connect_poll

Forwards [`std.system.os.linux.shared.sock_connect_poll`](shared.md#sock_connect_poll).

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

### CONNECT_PENDING

Forwards [`std.system.os.linux.shared.CONNECT_PENDING`](shared.md#constants).

```mach
pub val CONNECT_PENDING: i64 = 1
```

what sock_connect_begin and sock_connect_poll return while the connect is in flight

### sock_close

Forwards [`std.system.os.linux.shared.sock_close`](shared.md#sock_close).

```mach
pub fun sock_close(fd: usize) i64
```

close a socket file descriptor

### sock_create

Forwards [`std.system.os.linux.shared.sock_create`](shared.md#sock_create).

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

create a socket file descriptor

### sock_create_flags

Forwards [`std.system.os.linux.shared.sock_create_flags`](shared.md#sock_create_flags).

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_bind

Forwards [`std.system.os.linux.shared.sock_bind`](shared.md#sock_bind).

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

bind a socket to an address

### sock_listen

Forwards [`std.system.os.linux.shared.sock_listen`](shared.md#sock_listen).

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

mark a socket as a passive listener

### sock_accept

Forwards [`std.system.os.linux.shared.sock_accept`](shared.md#sock_accept).

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

accept a connection on a listening socket

### sock_accept_flags

Forwards [`std.system.os.linux.shared.sock_accept_flags`](shared.md#sock_accept_flags).

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_connect

Forwards [`std.system.os.linux.shared.sock_connect`](shared.md#sock_connect).

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

connect a socket to a remote address

### sock_sendto

Forwards [`std.system.os.linux.shared.sock_sendto`](shared.md#sock_sendto).

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

send data to a specific address

### sock_recvfrom

Forwards [`std.system.os.linux.shared.sock_recvfrom`](shared.md#sock_recvfrom).

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

receive data and source address

### sock_peek_readable

Forwards [`std.system.os.linux.shared.sock_peek_readable`](shared.md#sock_peek_readable).

```mach
pub fun sock_peek_readable(fd: usize) i64
```

peek at a stream socket without consuming or blocking

### sock_shutdown

Forwards [`std.system.os.linux.shared.sock_shutdown`](shared.md#sock_shutdown).

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

shut down part or all of a socket connection

### sock_setopt

Forwards [`std.system.os.linux.shared.sock_setopt`](shared.md#sock_setopt).

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

set a socket option

### sock_getopt

Forwards [`std.system.os.linux.shared.sock_getopt`](shared.md#sock_getopt).

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

### sock_local_addr

Forwards [`std.system.os.linux.shared.sock_local_addr`](shared.md#sock_local_addr).

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_remote_addr

Forwards [`std.system.os.linux.shared.sock_remote_addr`](shared.md#sock_remote_addr).

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_inheritable

Forwards [`std.system.os.linux.shared.sock_inheritable`](shared.md#sock_inheritable).

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

### io_queue_create

Forwards [`std.system.os.linux.shared.io_queue_create`](shared.md#io_queue_create).

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_wait

Forwards [`std.system.os.linux.shared.io_queue_wait`](shared.md#io_queue_wait).

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

### IoCompletion

Forwards [`std.system.os.linux.shared.IoCompletion`](shared.md#iocompletion).

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

### IO_EVENT_READ

Forwards [`std.system.os.linux.shared.IO_EVENT_READ`](shared.md#constants).

```mach
pub val IO_EVENT_READ:   u32 = 0x01
```

### IO_EVENT_WRITE

Forwards [`std.system.os.linux.shared.IO_EVENT_WRITE`](shared.md#constants).

```mach
pub val IO_EVENT_WRITE:  u32 = 0x02
```

### IO_EVENT_ERROR

Forwards [`std.system.os.linux.shared.IO_EVENT_ERROR`](shared.md#constants).

```mach
pub val IO_EVENT_ERROR:  u32 = 0x04
```

### IO_EVENT_HANGUP

Forwards [`std.system.os.linux.shared.IO_EVENT_HANGUP`](shared.md#constants).

```mach
pub val IO_EVENT_HANGUP: u32 = 0x08
```

### IO_EVENT_WAKE

Forwards [`std.system.os.linux.shared.IO_EVENT_WAKE`](shared.md#constants).

```mach
pub val IO_EVENT_WAKE:   u32 = 0x10
```

### io_queue_watch

Forwards [`std.system.os.linux.shared.io_queue_watch`](shared.md#io_queue_watch).

```mach
pub fun io_queue_watch(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

registers a resource that has no registration on the queue yet. a resource
that is already registered is refused with EEXIST, never taken over

### io_queue_rearm

Forwards [`std.system.os.linux.shared.io_queue_rearm`](shared.md#io_queue_rearm).

```mach
pub fun io_queue_rearm(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

arms again a registration the caller made with io_queue_watch

### duplicate_to

Forwards [`std.system.os.linux.shared.duplicate_to`](shared.md#duplicate_to).

```mach
pub fun duplicate_to(from: usize, to: usize) i64
```

makes the descriptor to name what from names, closing whatever to named
before, in one step. the copy is not inherited across exec

### io_queue_unwatch

Forwards [`std.system.os.linux.shared.io_queue_unwatch`](shared.md#io_queue_unwatch).

```mach
pub fun io_queue_unwatch(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

### io_queue_poll

Forwards [`std.system.os.linux.shared.io_queue_poll`](shared.md#io_queue_poll).

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

completions is also the kernel scratch buffer. normalization runs backwards
so expanding packed x86-64 epoll records cannot overwrite unread records.

### io_queue_wake

Forwards [`std.system.os.linux.shared.io_queue_wake`](shared.md#io_queue_wake).

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

nil is invalid use and a closed queue is EBADF on every platform

### io_queue_close

Forwards [`std.system.os.linux.shared.io_queue_close`](shared.md#io_queue_close).

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

### sock_set_rcvtimeo

Forwards [`std.system.os.linux.shared.sock_set_rcvtimeo`](shared.md#sock_set_rcvtimeo).

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

set the receive timeout on a socket

writes a struct timeval (tv_sec, tv_usec) derived from ms as the SO_RCVTIMEO
option value. ms == 0 clears the timeout, restoring indefinite blocking. once
set, a recv with no data pending fails with EAGAIN after the interval elapses.

### DNS_HOSTS_PATH

Forwards [`std.system.os.linux.shared.DNS_HOSTS_PATH`](shared.md#constants).

```mach
pub val DNS_HOSTS_PATH: str = "/etc/hosts"
```

dns

### random_fill

Forwards [`std.system.os.linux.shared.random_fill`](shared.md#random_fill).

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

random

### thread_current_id

Forwards [`std.system.os.linux.shared.thread_current_id`](shared.md#thread_current_id).

```mach
pub fun thread_current_id() i64
```

threads

### thread_current_name

Forwards [`std.system.os.linux.shared.thread_current_name`](shared.md#thread_current_name).

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

### thread_wait

Forwards [`std.system.os.linux.shared.thread_wait`](shared.md#thread_wait).

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

wraps the futex FUTEX_WAIT operation. returns immediately if *addr
does not equal expected. spurious wakeups are possible.

### thread_wait_until

Forwards [`std.system.os.linux.shared.thread_wait_until`](shared.md#thread_wait_until).

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

block until the word changes or an absolute monotonic deadline is reached

### thread_wake

Forwards [`std.system.os.linux.shared.thread_wake`](shared.md#thread_wake).

```mach
pub fun thread_wake(addr: *i64) i64
```

wake one thread blocked on a futex wait at addr

### clock_gettime

Forwards [`std.system.os.linux.shared.clock_gettime`](shared.md#clock_gettime).

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

time

### error_message

Forwards [`std.system.os.linux.shared.error_message`](shared.md#error_message).

```mach
pub fun error_message(code: i64) str
```

errno

