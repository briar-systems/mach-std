[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [linux](README.md) / **shared**

# std.system.os.linux.shared

code shared across all linux ISA implementations

contains types, constants, syscall wrappers, and all OS primitives that
are identical across linux architectures. arch-specific modules provide
only page_size and thread_spawn.

Source: [`src/system/os/linux/shared.mach`](../../../../../src/system/os/linux/shared.mach)

Uses types from [`std.system.cpu.features`](../../cpu/features.md), [`std.system.file_identity`](../../file_identity.md), [`std.system.os.shared`](../shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`stat_t`](#stat_t) | `rec` | riscv32 has no stat call: stat and stat_path fill this layout from statx |
| [`timespec`](#timespec) | `rec` | time specification with seconds and nanoseconds |
| [`DirectoryCursor`](#directorycursor) | `rec` |  |
| [`TlsLayout`](#tlslayout) | `rec` | where an architecture's psABI puts the thread-local block against the thread pointer, as the linker lays out local-exec offsets |
| [`IoCompletion`](#iocompletion) | `rec` | context is opaque to the OS and zero is reserved for the runtime wake source source: the id of the source that registered the context, 0 for a wake |
| [`IoVector`](#iovector) | `rec` |  |

| On `stat_t` | |
| :--- | :--- |
| [`stat`](#stat) | fstat: get file status by file descriptor |
| [`stat_path`](#stat_path) | newfstatat: get file status relative to a directory fd |
| [`stat_mode`](#stat_mode) | read the type/permission bits from a filled stat buffer as a 32-bit word |

| On `timespec` | |
| :--- | :--- |
| [`clock_gettime`](#clock_gettime) | get time from a clock source |

| On `DirectoryCursor` | |
| :--- | :--- |
| [`directory_init`](#directory_init) | fd and its aliases lend exclusive enumeration and seek access until close |
| [`directory_next`](#directory_next) | |
| [`directory_dnit`](#directory_dnit) | consumes the owner, including when native release reports failure |

| On `TlsLayout` | |
| :--- | :--- |
| [`thread_area_size`](#thread_area_size) | the bytes a thread's area takes: its block, its thread-local block, the control block and the slack that aligns the thread pointer, a multiple of 16 |
| [`thread_area_build`](#thread_area_build) | lay out a thread's area in zeroed memory and fill its thread-local block |
| [`thread_pointer_of`](#thread_pointer_of) | the thread pointer that installs a block |
| [`thread_block_at`](#thread_block_at) | the block a thread pointer installs |
| [`thread_tls_of`](#thread_tls_of) | the start of the thread-local block a thread pointer reaches |
| [`main_thread_block`](#main_thread_block) | the main thread's block: one in an area of its own when the executable has thread-locals, else the static fallback |
| [`thread_tls_wipe`](#thread_tls_wipe) | wipe the calling thread's thread-local block before the thread ends |

| On `IoCompletion` | |
| :--- | :--- |
| [`io_queue_poll`](#io_queue_poll) | completions is also the kernel scratch buffer |

| On `IoVector` | |
| :--- | :--- |
| [`sock_write_vector`](#sock_write_vector), [`sock_send_message`](#sock_send_message), [`sock_receive_message`](#sock_receive_message) | |

| Functions | |
| :--- | :--- |
| [`syscall0`](#syscall0) | execute a syscall with no arguments |
| [`syscall1`](#syscall1) | execute a syscall with 1 argument |
| [`syscall2`](#syscall2) | execute a syscall with 2 arguments |
| [`syscall3`](#syscall3) | execute a syscall with 3 arguments |
| [`syscall4`](#syscall4) | execute a syscall with 4 arguments |
| [`syscall5`](#syscall5) | execute a syscall with 5 arguments |
| [`syscall6`](#syscall6) | execute a syscall with 6 arguments |
| [`allocate`](#allocate) | allocate anonymous read-write memory via mmap |
| [`deallocate`](#deallocate) | free memory via munmap |
| [`map_secret`](#map_secret) | map storage for secret-welded data: span locked, dump-excluded bytes between two inaccessible guard pages, page aligned and zero-filled |
| [`thread_stack_allocate`](#thread_stack_allocate) | allocate a thread stack mapping with a guard below it |
| [`thread_stack_size`](#thread_stack_size) | the whole mapping thread_stack_allocate makes for reserve, guard included |
| [`thread_block_reserve`](#thread_block_reserve) | the bytes a spawned thread's block takes from the top of its stack, a multiple of 16 so the handoff words below it keep their alignment |
| [`thread_block_prepare`](#thread_block_prepare) | fill a thread block before it is installed, with no stack bounds yet |
| [`thread_block_bound`](#thread_block_bound) | record the stack a spawned thread runs on in its block |
| [`capture_tls`](#capture_tls) | read the executable's thread-local template from its program headers |
| [`thread_set_name`](#thread_set_name) | set the current thread's native diagnostic name |
| [`thread_current_id`](#thread_current_id), [`thread_current_name`](#thread_current_name) | |
| [`reallocate`](#reallocate) | resize a memory region via mremap |
| [`heap_region_base`](#heap_region_base) | query the current program break via brk(0) |
| [`heap_region_extend`](#heap_region_extend) | set the program break to addr via brk |
| [`protect`](#protect) | change protection on a memory region via mprotect |
| [`lock`](#lock) | lock a memory region into physical RAM via mlock |
| [`unlock`](#unlock) | unlock a previously locked memory region via munlock |
| [`advise`](#advise) | advise the kernel on expected access patterns via madvise |
| [`allocate_huge`](#allocate_huge) | allocate memory backed by huge pages via mmap |
| [`numa_node_count`](#numa_node_count) | return the number of NUMA nodes via get_mempolicy |
| [`numa_current_node`](#numa_current_node) | return the NUMA node of the current CPU via getcpu |
| [`numa_allocate`](#numa_allocate) | allocate memory pinned to a specific NUMA node |
| [`numa_move`](#numa_move) | move a memory region to a different NUMA node via mbind |
| [`map_file`](#map_file) | map a file descriptor into memory via mmap |
| [`sync_file`](#sync_file) | flush a memory-mapped region to its backing file via msync |
| [`has_numa`](#has_numa) | check if the kernel supports NUMA memory policy |
| [`has_huge_pages`](#has_huge_pages) | check if the kernel supports huge page allocation |
| [`read`](#read) | read bytes from a file descriptor |
| [`write`](#write) | write bytes to a file descriptor |
| [`read_at`](#read_at) | positioned file access does not mutate the descriptor offset |
| [`write_at`](#write_at) | |
| [`open`](#open) | openat: open a file relative to a directory file descriptor |
| [`close`](#close) | close a file descriptor |
| [`sync_fd`](#sync_fd) | flush an open file's data and metadata to its backing storage |
| [`set_mode`](#set_mode) | set permission bits through a held descriptor |
| [`set_mode_at`](#set_mode_at) | no following fallback is permitted when the flags-aware syscall is unavailable |
| [`publication_capabilities`](#publication_capabilities) | |
| [`file_identity`](#file_identity) | observational ids do not retain an object after this call |
| [`retain_identity_at`](#retain_identity_at) | o_path pins the entry without acquiring content-read permission |
| [`identity_at`](#identity_at) | |
| [`unlink`](#unlink) | unlinkat: remove a file or directory relative to a directory fd |
| [`rename`](#rename) | renameat: rename a file relative to directory fds |
| [`lock_fd`](#lock_fd) | flock: take or release an advisory whole-file lock on an open descriptor |
| [`symlink`](#symlink) | create a symbolic link at linkpath pointing to target |
| [`make_dir`](#make_dir) | mkdirat: create a directory relative to a directory fd |
| [`access`](#access) | faccessat: check file accessibility relative to a directory fd |
| [`seek`](#seek) | lseek: reposition read/write offset of a file descriptor |
| [`environ`](#environ) | pointer to the environment captured by the runtime at program start (null-terminated array of "NAME=value" strings) |
| [`capture_pagesz`](#capture_pagesz) | publish the auxv page size into `_pagesz` |
| [`capture_main_stack`](#capture_main_stack) | capture the main thread's stack bounds, once, at entry |
| [`thread_pointer_owned`](#thread_pointer_owned) | whether the block a thread reads through its thread pointer is std's |
| [`stack_bounds_of`](#stack_bounds_of) | the calling thread's stack bounds, from its block or the main thread's record |
| [`loader_started`](#loader_started) | whether a program interpreter ran before the entry point |
| [`loader_present`](#loader_present) | whether a program interpreter started this process |
| [`terminate`](#terminate) | exit the process with the given code |
| [`abort`](#abort) | abort the process immediately with exit code 255 |
| [`fork`](#fork) | create a new child process |
| [`vfork`](#vfork) | create child process sharing memory with parent |
| [`exec`](#exec) | execve: replace the current process image with a new program |
| [`wait`](#wait) | failures and no-event results leave the caller's status unchanged |
| [`wait_pid`](#wait_pid) | |
| [`terminate_child`](#terminate_child) | forcefully stop a spawned child without reaping it |
| [`setpgid`](#setpgid) | setpgid: set (or join) the process group ID of a process |
| [`getpgid`](#getpgid) | getpgid: read the process group ID of a process |
| [`terminate_group`](#terminate_group) | signal every process in a group without reaping any of them |
| [`kill_group`](#kill_group) | forcefully stop every process in a group without reaping any of them |
| [`probe_group`](#probe_group) | whether any process is left in a group, without signalling it |
| [`process_watch`](#process_watch) | make the end of the child `pid` a readiness event on `queue`, so the queue's wait returns once the child ends |
| [`process_unwatch`](#process_unwatch) | release a watch process_watch made, whether or not it fired |
| [`spawn`](#spawn) | create a child process running the given program |
| [`spawn_grouped`](#spawn_grouped) | create a child process running the given program, placed as the leader of its own new process group (see spawn_redirected_in_grouped) |
| [`spawn_in`](#spawn_in) | create a child process running the given program from `cwd` |
| [`spawn_redirected`](#spawn_redirected) | spawn a child with its standard streams bound to caller-supplied descriptors |
| [`spawn_redirected_grouped`](#spawn_redirected_grouped) | spawn a child with its standard streams bound to caller-supplied descriptors, placed as the leader of its own new process group (see spawn_redirected_in_grouped) |
| [`spawn_redirected_in`](#spawn_redirected_in) | spawn a child with redirected streams and an explicit working directory |
| [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | spawn a child with redirected streams and an explicit working directory, placed as the leader of its own new process group |
| [`running_under_user_emulation`](#running_under_user_emulation) | detect a user-mode emulator such as qemu-user |
| [`getpid`](#getpid) | return the current process ID |
| [`open_file_limit`](#open_file_limit) | read this process's open-file limit |
| [`set_open_file_limit`](#set_open_file_limit) | set this process's open-file limit |
| [`pipe`](#pipe) | create a unidirectional pipe |
| [`ignore_sigpipe`](#ignore_sigpipe) | ignore SIGPIPE for this process |
| [`sleep`](#sleep) | suspend execution for the given number of nanoseconds |
| [`cpu_features`](#cpu_features) | the running processor's instruction-set extensions |
| [`cpu_dit`](#cpu_dit) | whether the processor and kernel provide the data-independent-timing mode |
| [`cpu_count`](#cpu_count) | the number of CPUs available to this process |
| [`thread_affinity`](#thread_affinity) | read the calling thread's CPU affinity |
| [`set_thread_affinity`](#set_thread_affinity) | pin the calling thread to the CPUs set in words |
| [`getcwd`](#getcwd) | get the current working directory |
| [`getenv`](#getenv) | look up an environment variable by name |
| [`temp_dir`](#temp_dir) | the directory designated for temporary files: $TMPDIR, else "/tmp" |
| [`thread_wait`](#thread_wait) | block until the value at addr changes from expected |
| [`thread_wait_until`](#thread_wait_until) | block until the word changes or an absolute monotonic deadline is reached |
| [`thread_wake`](#thread_wake) | wake one thread blocked on a futex wait at addr |
| [`io_queue_create`](#io_queue_create) | |
| [`io_queue_watch`](#io_queue_watch) | registers a resource that has no registration on the queue yet |
| [`io_queue_rearm`](#io_queue_rearm) | arms again a registration the caller made with io_queue_watch |
| [`duplicate_to`](#duplicate_to) | makes the descriptor to name what from names, closing whatever to named before, in one step |
| [`io_queue_unwatch`](#io_queue_unwatch), [`io_queue_wait`](#io_queue_wait) | |
| [`io_queue_wake`](#io_queue_wake) | nil is invalid use and a closed queue is EBADF on every platform |
| [`io_queue_close`](#io_queue_close) | |
| [`sock_send`](#sock_send) | send data on a connected socket |
| [`sock_recv`](#sock_recv) | receive data from a connected socket |
| [`sock_peek_readable`](#sock_peek_readable) | peek at a stream socket without consuming or blocking |
| [`sock_recv_close_rights`](#sock_recv_close_rights) | receives bytes and closes every descriptor the kernel installed for them |
| [`local_stream_recv`](#local_stream_recv) | byte reception for local streams: rights a peer attaches are observed and closed |
| [`sock_set_nonblocking`](#sock_set_nonblocking) | switch a socket between blocking and nonblocking |
| [`sock_connect_begin`](#sock_connect_begin) | start a connect on a nonblocking socket |
| [`sock_connect_poll`](#sock_connect_poll) | ask whether a connect sock_connect_begin started has settled, without waiting |
| [`sock_close`](#sock_close) | close a socket file descriptor |
| [`sock_create`](#sock_create) | create a socket file descriptor |
| [`sock_create_flags`](#sock_create_flags) | |
| [`sock_bind`](#sock_bind) | bind a socket to an address |
| [`sock_listen`](#sock_listen) | mark a socket as a passive listener |
| [`sock_accept`](#sock_accept) | accept a connection on a listening socket |
| [`sock_accept_flags`](#sock_accept_flags) | |
| [`sock_connect`](#sock_connect) | connect a socket to a remote address |
| [`sock_sendto`](#sock_sendto) | send data to a specific address |
| [`sock_recvfrom`](#sock_recvfrom) | receive data and source address |
| [`sock_shutdown`](#sock_shutdown) | shut down part or all of a socket connection |
| [`sock_setopt`](#sock_setopt) | set a socket option |
| [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable) | |
| [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | set the receive timeout on a socket |
| [`random_fill`](#random_fill) | fill a buffer with cryptographic random bytes via getrandom |
| [`error_message`](#error_message) | return a human-readable message for a negated errno code |

| Constants | |
| :--- | :--- |
| [`SYS_FUTEX`](#constants) | syscall numbers are architecture-specific: x86_64 has its own table, while aarch64 and riscv64 both use the generic asm-generic/unistd table |
| [`FUTEX_WAIT`](#constants) | constants identical across linux architectures (asm-generic matches x86_64 for these), declared once at module scope |
| [`FUTEX_WAKE`](#constants), [`FUTEX_WAIT_BITSET`](#constants), [`FUTEX_BITSET_MATCH_ANY`](#constants), [`CLONE_VM`](#constants), [`CLONE_FS`](#constants), [`CLONE_FILES`](#constants), [`CLONE_SIGHAND`](#constants), [`CLONE_THREAD`](#constants), [`CLONE_SYSVSEM`](#constants), [`CLONE_SETTLS`](#constants) | |
| [`PROT_READ`](#constants) | the read-only protection, exported for the static-PIE RELRO re-protection in std.runtime.linux.reloc |
| [`ENOSYS`](#constants) | |
| [`separator`](#constants) | path |
| [`STDIN_FD`](#constants) | portable constants |
| [`STDOUT_FD`](#constants), [`STDERR_FD`](#constants), [`O_RDONLY`](#constants), [`O_WRONLY`](#constants), [`O_RDWR`](#constants), [`O_CREAT`](#constants), [`O_EXCL`](#constants), [`O_TRUNC`](#constants), [`O_APPEND`](#constants), [`O_NONBLOCK`](#constants) | |
| [`O_DIRECTORY`](#constants) | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
| [`O_NOFOLLOW`](#constants) | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
| [`O_DIRECT`](#constants) | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
| [`AT_FDCWD`](#constants), [`AT_SYMLINK_NOFOLLOW`](#constants), [`AT_REMOVEDIR`](#constants) | |
| [`LOCK_SH`](#constants) | advisory whole-file lock operations, passed to lock_fd |
| [`LOCK_EX`](#constants), [`LOCK_NB`](#constants), [`LOCK_UN`](#constants), [`S_IFMT`](#constants), [`S_IFDIR`](#constants), [`S_IFREG`](#constants), [`S_IFLNK`](#constants), [`WNOHANG`](#constants), [`WUNTRACED`](#constants), [`WCONTINUED`](#constants), [`CLOCK_REALTIME`](#constants), [`CLOCK_MONOTONIC`](#constants), [`EPERM`](#constants), [`ENOENT`](#constants), [`ESRCH`](#constants), [`EINTR`](#constants), [`EIO`](#constants), [`ENXIO`](#constants), [`E2BIG`](#constants), [`EBADF`](#constants), [`ECHILD`](#constants), [`EAGAIN`](#constants), [`ENOMEM`](#constants), [`EACCES`](#constants), [`EFAULT`](#constants), [`EBUSY`](#constants), [`EEXIST`](#constants), [`ENODEV`](#constants), [`ENOTDIR`](#constants), [`EISDIR`](#constants), [`EINVAL`](#constants), [`ENFILE`](#constants), [`EMFILE`](#constants), [`ETXTBSY`](#constants), [`ENOSPC`](#constants), [`EROFS`](#constants), [`EPIPE`](#constants), [`ENAMETOOLONG`](#constants), [`ENOTEMPTY`](#constants), [`ELOOP`](#constants), [`ENOTSUP`](#constants), [`ERANGE`](#constants), [`EADDRINUSE`](#constants), [`ENETUNREACH`](#constants), [`ECONNABORTED`](#constants), [`ECONNRESET`](#constants), [`ENOTCONN`](#constants), [`ETIMEDOUT`](#constants), [`ECONNREFUSED`](#constants), [`EHOSTUNREACH`](#constants), [`ECANCELED`](#constants), [`EINTR_MAX_RETRIES`](#constants) | |
| [`THREAD_STACK_GUARD`](#constants) | the inaccessible bytes below every spawned thread's stack, so an overflow faults instead of writing into the mapping below |
| [`IO_EVENT_READ`](#constants), [`IO_EVENT_WRITE`](#constants), [`IO_EVENT_ERROR`](#constants), [`IO_EVENT_HANGUP`](#constants), [`IO_EVENT_WAKE`](#constants), [`AF_INET`](#constants), [`AF_INET6`](#constants), [`SOCK_STREAM`](#constants), [`SOCK_DGRAM`](#constants), [`SOCK_NONBLOCK`](#constants), [`SOCK_CLOEXEC`](#constants), [`SOL_SOCKET`](#constants), [`SO_UNSUPPORTED`](#constants), [`SO_REUSEADDR`](#constants), [`SO_REUSEPORT`](#constants), [`SO_EXCLUSIVEADDRUSE`](#constants), [`SO_KEEPALIVE`](#constants), [`SO_SNDBUF`](#constants), [`SO_RCVBUF`](#constants), [`SO_LINGER`](#constants) | |
| [`SO_RCVTIMEO`](#constants) | riscv32 takes the 64-bit timeval sock_set_rcvtimeo writes only as SO_RCVTIMEO_NEW |
| [`IPPROTO_IP`](#constants), [`IPPROTO_TCP`](#constants), [`IPPROTO_IPV6`](#constants), [`IP_TOS`](#constants), [`IPV6_V6ONLY`](#constants), [`IPV6_TCLASS`](#constants), [`TCP_NODELAY`](#constants), [`TCP_KEEPIDLE`](#constants), [`TCP_KEEPINTVL`](#constants), [`TCP_KEEPCNT`](#constants), [`TCP_FASTOPEN`](#constants), [`SHUT_RD`](#constants), [`SHUT_WR`](#constants), [`SHUT_RDWR`](#constants), [`SOCKADDR_IN_SIZE`](#constants), [`SOCKADDR_IN6_SIZE`](#constants), [`SOCKADDR_STORAGE_SIZE`](#constants), [`MSG_CTRUNC`](#constants), [`MSG_CMSG_CLOEXEC`](#constants), [`SCM_RIGHTS`](#constants), [`SCM_CREDENTIALS`](#constants), [`SCM_PIDFD`](#constants) | |
| [`SCM_MAX_FD`](#constants) | net/scm.h SCM_MAX_FD: sendmsg refuses a larger descriptor set, and a stream receive returns at most one set (unix_stream_read_generic stops after the record that carries it) |
| [`LOCAL_CONTROL_CAPACITY`](#constants) | CMSG_SPACE(253 descriptors) + CMSG_SPACE(ucred) + CMSG_SPACE(pidfd): the largest descriptor set together with the fixed-size records SO_PASSCRED and SO_PASSPIDFD prepend to it |
| [`CONNECT_PENDING`](#constants) | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| [`DNS_HOSTS_PATH`](#constants) | |

| Variables | |
| :--- | :--- |
| [`_envp`](#variables) | environment (set by runtime at program start) |
| [`_pagesz`](#variables) | the runtime page size in bytes, read from the auxiliary vector (AT_PAGESZ) at program start |

| Forwards | |
| :--- | :--- |
| [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`ProcessStatus`](#processstatus) | canonical process observations |
| [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |

---

## stat_t

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

riscv32 has no stat call: stat and stat_path fill this layout from statx

### stat

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

fstat: get file status by file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `st` | pointer to stat_t to fill |
| **returns** | 0 on success, or negative errno |

### stat_path

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

newfstatat: get file status relative to a directory fd

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `st` | pointer to stat_t to fill |
| `flags` | AT_* flags |
| **returns** | 0 on success, or negative errno |

### stat_mode

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 32-bit in the linux stat ABI; the accessor exists so portable
callers read the mode uniformly across platforms (darwin's mode is 16-bit).

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

get time from a clock source

| Parameter | |
| :--- | :--- |
| `clock_id` | clock to query (CLOCK_REALTIME, CLOCK_MONOTONIC) |
| `ts` | pointer to timespec to fill |
| **returns** | 0 on success, negative errno on failure |

## DirectoryCursor

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

consumes the owner, including when native release reports failure

## TlsLayout

```mach
pub rec TlsLayout {
    below: bool;
    tcb:   usize;
}
```

where an architecture's psABI puts the thread-local block against the thread
pointer, as the linker lays out local-exec offsets

| Field | Type | |
| :--- | :--- | :--- |
| `below` | `bool` | variant II, the block ends at the thread pointer (x86_64) |
| `tcb` | `usize` | variant I, the control block bytes between the thread pointer and the block, which starts at tcb aligned up to the block's alignment |

### thread_area_size

```mach
pub fun thread_area_size(l: TlsLayout) usize
```

the bytes a thread's area takes: its block, its thread-local block, the
control block and the slack that aligns the thread pointer, a multiple of 16

### thread_area_build

```mach
pub fun thread_area_build(base: usize, l: TlsLayout) *std.system.os.shared.ThreadBlock
```

lay out a thread's area in zeroed memory and fill its thread-local block

x86_64 puts the block at the thread pointer and the thread-local block below
it. variant I puts the block just below the thread pointer and the control
block and the thread-local block above it. the thread pointer is aligned to
the template's alignment, so the block's offsets land as the linker laid them
out

| Parameter | |
| :--- | :--- |
| `base` | the area's start, 16-aligned, thread_area_size(l) zeroed bytes |
| **returns** | the thread's block, prepared but not installed |

### thread_pointer_of

```mach
pub fun thread_pointer_of(block: *std.system.os.shared.ThreadBlock, l: TlsLayout) usize
```

the thread pointer that installs a block

### thread_block_at

```mach
pub fun thread_block_at(tp: usize, l: TlsLayout) *std.system.os.shared.ThreadBlock
```

the block a thread pointer installs

### thread_tls_of

```mach
pub fun thread_tls_of(tp: usize, l: TlsLayout) usize
```

the start of the thread-local block a thread pointer reaches

### main_thread_block

```mach
pub fun main_thread_block(fallback: *std.system.os.shared.ThreadBlock, l: TlsLayout) *std.system.os.shared.ThreadBlock
```

the main thread's block: one in an area of its own when the executable has
thread-locals, else the static fallback

| Parameter | |
| :--- | :--- |
| **returns** | the block to install, or nil when the area could not be mapped |

### thread_tls_wipe

```mach
pub fun thread_tls_wipe(tp: usize, l: TlsLayout)
```

wipe the calling thread's thread-local block before the thread ends

thread-locals may hold secrets, so the whole block is zeroed with stores no
pass removes. nothing may read a thread-local after this

| Parameter | |
| :--- | :--- |
| `tp` | the calling thread's thread pointer |

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

completions is also the kernel scratch buffer. normalization runs backwards
so expanding packed x86-64 epoll records cannot overwrite unread records.

## IoVector

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

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

## Functions

### syscall0

```mach
pub fun syscall0(n: usize) i64
```

execute a syscall with no arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| **returns** | syscall result (negative on error) |

### syscall1

```mach
pub fun syscall1(n: usize, a0: usize) i64
```

execute a syscall with 1 argument

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| **returns** | syscall result (negative on error) |

### syscall2

```mach
pub fun syscall2(n: usize, a0: usize, a1: usize) i64
```

execute a syscall with 2 arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| `a1` | second argument |
| **returns** | syscall result (negative on error) |

### syscall3

```mach
pub fun syscall3(n: usize, a0: usize, a1: usize, a2: usize) i64
```

execute a syscall with 3 arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| `a1` | second argument |
| `a2` | third argument |
| **returns** | syscall result (negative on error) |

### syscall4

```mach
pub fun syscall4(n: usize, a0: usize, a1: usize, a2: usize, a3: usize) i64
```

execute a syscall with 4 arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| `a1` | second argument |
| `a2` | third argument |
| `a3` | fourth argument |
| **returns** | syscall result (negative on error) |

### syscall5

```mach
pub fun syscall5(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize) i64
```

execute a syscall with 5 arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| `a1` | second argument |
| `a2` | third argument |
| `a3` | fourth argument |
| `a4` | fifth argument |
| **returns** | syscall result (negative on error) |

### syscall6

```mach
pub fun syscall6(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize, a5: usize) i64
```

execute a syscall with 6 arguments

| Parameter | |
| :--- | :--- |
| `n` | syscall number |
| `a0` | first argument |
| `a1` | second argument |
| `a2` | third argument |
| `a3` | fourth argument |
| `a4` | fifth argument |
| `a5` | sixth argument |
| **returns** | syscall result (negative on error) |

### allocate

```mach
pub fun allocate(size: usize) ptr
```

allocate anonymous read-write memory via mmap

| Parameter | |
| :--- | :--- |
| `size` | number of bytes to allocate; if 0, returns nil |
| **returns** | pointer to allocated memory, or nil on failure |

### deallocate

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

free memory via munmap

| Parameter | |
| :--- | :--- |
| `p` | pointer to memory; if nil, returns 0 |
| `size` | allocation size in bytes; if 0, returns 0 |
| **returns** | 0 on success, or negative errno |

### map_secret

```mach
pub fun map_secret(span: usize, page: usize, out: *ptr, locking: *bool) i64
```

map storage for secret-welded data: span locked, dump-excluded bytes between
two inaccessible guard pages, page aligned and zero-filled

memfd_secret backs the span where the kernel provides it, which locks it,
keeps it out of dumps and removes it from the kernel's direct map. a kernel
without it (ENOSYS) gets an anonymous span locked with mlock and marked
MADV_DONTDUMP. a refused lock is reported as one, never served unlocked

| Parameter | |
| :--- | :--- |
| `span` | usable bytes, a nonzero multiple of page |
| `page` | the page size |
| `out` | receives the first usable byte, one page past the mapping's start |
| `locking` | set when the failure was the kernel refusing to lock the span |
| **returns** | 0, or the negative errno of the step that failed, with nothing mapped |

### thread_stack_allocate

```mach
pub fun thread_stack_allocate(reserve: usize, commit: usize, base: *usize) i64
```

allocate a thread stack mapping with a guard below it

the mapping is the guard followed by reserve writable bytes, so the usable
stack runs from base + THREAD_STACK_GUARD to base + thread_stack_size(reserve)

| Parameter | |
| :--- | :--- |
| `reserve` | the usable stack extent, a multiple of the page size |
| `commit` | must be 0 until safe stack growth is implemented |
| `base` | receives the mapping base, the guard's low end, on success |
| **returns** | 0 on success, or normalized negative error |

### thread_stack_size

```mach
pub fun thread_stack_size(reserve: usize) usize
```

the whole mapping thread_stack_allocate makes for reserve, guard included

### thread_block_reserve

```mach
pub fun thread_block_reserve() usize
```

the bytes a spawned thread's block takes from the top of its stack, a
multiple of 16 so the handoff words below it keep their alignment

### thread_block_prepare

```mach
pub fun thread_block_prepare(block: *std.system.os.shared.ThreadBlock)
```

fill a thread block before it is installed, with no stack bounds yet

### thread_block_bound

```mach
pub fun thread_block_bound(block: *std.system.os.shared.ThreadBlock, low: usize, high: usize)
```

record the stack a spawned thread runs on in its block

### capture_tls

```mach
pub fun capture_tls()
```

read the executable's thread-local template from its program headers

AT_PHDR and AT_PHNUM locate the headers, and PT_PHDR gives the load bias of a
position-independent image, which a fixed image without one does not need.
runs once at entry, after relocation and before the main thread's block is
installed

### thread_set_name

```mach
pub fun thread_set_name(name: *u8) i64
```

set the current thread's native diagnostic name

### thread_current_id

```mach
pub fun thread_current_id() i64
```

### thread_current_name

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

### reallocate

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a memory region via mremap

| Parameter | |
| :--- | :--- |
| `p` | pointer to memory; if nil, behaves like allocate |
| `old_size` | current allocation size in bytes |
| `new_size` | desired size; if 0, deallocates and returns nil |
| **returns** | pointer to reallocated memory, or nil on failure |

### heap_region_base

```mach
pub fun heap_region_base() usize
```

query the current program break via brk(0)

| Parameter | |
| :--- | :--- |
| **returns** | current break address |

### heap_region_extend

```mach
pub fun heap_region_extend(addr: usize) usize
```

set the program break to addr via brk

| Parameter | |
| :--- | :--- |
| `addr` | desired new break address |
| **returns** | actual break address after the call |

### protect

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

change protection on a memory region via mprotect

| Parameter | |
| :--- | :--- |
| `p` | page-aligned pointer to the region |
| `size` | size of the region in bytes |
| `prot` | protection flags (PROT_READ, PROT_WRITE, PROT_EXEC, PROT_NONE) |
| **returns** | 0 on success, or negative errno |

### lock

```mach
pub fun lock(p: ptr, size: usize) i64
```

lock a memory region into physical RAM via mlock

| Parameter | |
| :--- | :--- |
| `p` | pointer to the region |
| `size` | size of the region in bytes |
| **returns** | 0 on success, or negative errno |

### unlock

```mach
pub fun unlock(p: ptr, size: usize) i64
```

unlock a previously locked memory region via munlock

| Parameter | |
| :--- | :--- |
| `p` | pointer to the region |
| `size` | size of the region in bytes |
| **returns** | 0 on success, or negative errno |

### advise

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

advise the kernel on expected access patterns via madvise

| Parameter | |
| :--- | :--- |
| `p` | pointer to the region |
| `size` | size of the region in bytes |
| `advice` | advisory hint (MADV_NORMAL, MADV_RANDOM, etc.) |
| **returns** | 0 on success, or negative errno |

### allocate_huge

```mach
pub fun allocate_huge(size: usize, page_size: usize) ptr
```

allocate memory backed by huge pages via mmap

| Parameter | |
| :--- | :--- |
| `size` | number of bytes; if 0, returns nil |
| `page_size` | huge page size in bytes (must be power of two) |
| **returns** | pointer to allocated memory, or nil on failure |

### numa_node_count

```mach
pub fun numa_node_count() usize
```

return the number of NUMA nodes via get_mempolicy

| Parameter | |
| :--- | :--- |
| **returns** | number of NUMA nodes (at least 1) |

### numa_current_node

```mach
pub fun numa_current_node() usize
```

return the NUMA node of the current CPU via getcpu

| Parameter | |
| :--- | :--- |
| **returns** | NUMA node id (0 on failure) |

### numa_allocate

```mach
pub fun numa_allocate(size: usize, node: usize) ptr
```

allocate memory pinned to a specific NUMA node

| Parameter | |
| :--- | :--- |
| `size` | number of bytes; if 0, returns nil |
| `node` | target NUMA node id |
| **returns** | pointer to allocated memory, or nil on failure |

### numa_move

```mach
pub fun numa_move(p: ptr, size: usize, node: usize) i64
```

move a memory region to a different NUMA node via mbind

| Parameter | |
| :--- | :--- |
| `p` | pointer to the region |
| `size` | size of the region in bytes |
| `node` | target NUMA node id |
| **returns** | 0 on success, or negative errno |

### map_file

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map a file descriptor into memory via mmap

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor to map |
| `offset` | offset into the file (must be page-aligned) |
| `size` | number of bytes to map; if 0, returns nil |
| `prot` | protection flags |
| **returns** | pointer to mapped region, or nil on failure |

### sync_file

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via msync

| Parameter | |
| :--- | :--- |
| `p` | pointer to the mapped region |
| `size` | size of the region in bytes |
| **returns** | 0 on success, or negative errno |

### has_numa

```mach
pub fun has_numa() bool
```

check if the kernel supports NUMA memory policy

| Parameter | |
| :--- | :--- |
| **returns** | true if get_mempolicy syscall is available |

### has_huge_pages

```mach
pub fun has_huge_pages() bool
```

check if the kernel supports huge page allocation

| Parameter | |
| :--- | :--- |
| **returns** | true if MAP_HUGETLB mmap succeeds |

### read

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

read bytes from a file descriptor

retries automatically on EINTR.

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | destination buffer |
| `count` | maximum bytes to read |
| **returns** | bytes read, or negative errno |

### write

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a file descriptor

retries automatically on EINTR.

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | source buffer |
| `count` | bytes to write |
| **returns** | bytes written, or negative errno |

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

openat: open a file relative to a directory file descriptor

retries automatically on EINTR.

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `flags` | open flags |
| `mode` | permission bits for creation |
| **returns** | new fd, or negative errno |

### close

```mach
pub fun close(fd: i32) i64
```

close a file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| **returns** | 0 on success, or negative errno |

### sync_fd

```mach
pub fun sync_fd(fd: i32) i64
```

flush an open file's data and metadata to its backing storage

### set_mode

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

set permission bits through a held descriptor

### set_mode_at

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

no following fallback is permitted when the flags-aware syscall is unavailable

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

o_path pins the entry without acquiring content-read permission

### identity_at

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### unlink

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

unlinkat: remove a file or directory relative to a directory fd

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `flags` | AT_REMOVEDIR to remove a directory |
| **returns** | 0 on success, or negative errno |

### rename

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

renameat: rename a file relative to directory fds

| Parameter | |
| :--- | :--- |
| `olddir` | source directory fd |
| `oldpath` | source path |
| `newdir` | destination directory fd |
| `newpath` | destination path |
| **returns** | 0 on success, or negative errno |

### lock_fd

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

| Parameter | |
| :--- | :--- |
| `fd` | open descriptor to lock, which may refer to a directory |
| `op` | LOCK_SH, LOCK_EX or LOCK_UN, optionally combined with LOCK_NB |
| **returns** | 0 on success, or negative errno; EAGAIN when LOCK_NB was set and another holder has the lock |

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

mkdirat: create a directory relative to a directory fd

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `mode` | permission bits |
| **returns** | 0 on success, or negative errno |

### access

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

faccessat: check file accessibility relative to a directory fd

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `mode` | access mode flags |
| `flags` | AT_* flags |
| **returns** | 0 if accessible, or negative errno |

### seek

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

lseek: reposition read/write offset of a file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `offset` | byte offset |
| `whence` | SEEK_SET, SEEK_CUR, or SEEK_END |
| **returns** | resulting offset, or negative errno |

### environ

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### capture_pagesz

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

### capture_main_stack

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

### thread_pointer_owned

```mach
pub fun thread_pointer_owned() bool
```

whether the block a thread reads through its thread pointer is std's

### stack_bounds_of

```mach
pub fun stack_bounds_of(block: *std.system.os.shared.ThreadBlock, low: *usize, high: *usize) bool
```

the calling thread's stack bounds, from its block or the main thread's record

a spawned thread's block carries its stack. the main thread's block carries
none, so a thread whose block has no bounds, or one that has no block std
owns, gets the main thread's when the caller's frame lies inside them

| Parameter | |
| :--- | :--- |
| `block` | the calling thread's block when std owns it, else nil |
| **returns** | whether the bounds are known |

### loader_started

```mach
pub fun loader_started(envp: *usize) bool
```

whether a program interpreter ran before the entry point

AT_BASE is the interpreter's load address, and the kernel writes 0 when the
image names none. an interpreter run as the command itself has AT_BASE 0 too,
and hands its program an auxv naming that program's headers, whose PT_INTERP
then tells. the auxv and the headers are kernel facts: std assumes nothing
about the interpreter.

the relocation pass asks this before any relocation, so it touches only envp,
the stack it points into and the headers, and its constants are literals

| Parameter | |
| :--- | :--- |
| `envp` | the runtime envp pointer (the value the entrypoint captured) |
| **returns** | true when AT_BASE is nonzero or the image names an interpreter |

### loader_present

```mach
pub fun loader_present() bool
```

whether a program interpreter started this process

whoever starts the process owns the main thread's thread pointer, so the
runtime installs std's block there only when this is false

| Parameter | |
| :--- | :--- |
| **returns** | `loader_started` of the published envp, false before the runtime publishes it |

### terminate

```mach
pub fun terminate(code: i64)
```

exit the process with the given code

uses exit_group so all threads in the process are terminated; plain
exit would only end the calling thread, leaving the process alive.

| Parameter | |
| :--- | :--- |
| `code` | exit code |

### abort

```mach
pub fun abort()
```

abort the process immediately with exit code 255

### fork

```mach
pub fun fork() i64
```

create a new child process

| Parameter | |
| :--- | :--- |
| **returns** | in parent: child PID (>0), in child: 0, on error: negative errno |

### vfork

```mach
pub fun vfork() i64
```

create child process sharing memory with parent

| Parameter | |
| :--- | :--- |
| **returns** | in parent: child PID (>0), in child: 0, on error: negative errno |

### exec

```mach
pub fun exec(pathname: *u8, argv: **u8, envp: Environment) i64
```

execve: replace the current process image with a new program

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | does not return on success; negative errno on error |

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
wait returns once the child ends. a pidfd names the child: it reads ready
from the moment the child ends, reaped or not, and is not inherited across exec

| Parameter | |
| :--- | :--- |
| `context` | the nonzero context the event carries |
| **returns** | the watch, which process_unwatch releases, or negative errno (ESRCH when no such process is left) |

### process_unwatch

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired

| Parameter | |
| :--- | :--- |
| **returns** | 0, or the first negative errno |

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

### running_under_user_emulation

```mach
pub fun running_under_user_emulation() bool
```

detect a user-mode emulator such as qemu-user

the kernel names a process after the image it executed (/proc/self/comm, at most
fifteen bytes), while an emulator presents the guest's own command line through
/proc/self/cmdline. natively the two name the same executable; under emulation the
comm names the emulator. tests use this to decline what an emulator's syscall
translation cannot reproduce, as running_under_wine does on windows.

| Parameter | |
| :--- | :--- |
| **returns** | true when the process image is not the executable the command line names |

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

read this process's open-file limit. linux's RLIM_INFINITY is all ones, the
same value as LIMIT_UNLIMITED, and an unprivileged process may raise its soft
limit up to the hard one

| Parameter | |
| :--- | :--- |
| `out` | filled with the limit in force |
| **returns** | 0, or a negative native code |

### set_open_file_limit

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

set this process's open-file limit. ceiling is ignored

| Parameter | |
| :--- | :--- |
| `limit` | the soft and hard limits to set |
| **returns** | 0, or a negative native code |

### pipe

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

| Parameter | |
| :--- | :--- |
| `fds` | pointer to two i32s; fds[0] = read end, fds[1] = write end |
| **returns** | 0 on success, or negative errno |

### ignore_sigpipe

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

| Parameter | |
| :--- | :--- |
| **returns** | 0 on success, or negative errno |

### sleep

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

| Parameter | |
| :--- | :--- |
| `nsec` | nanoseconds to sleep |

### cpu_features

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

| Parameter | |
| :--- | :--- |
| `out` | filled with the extensions the processor has |
| **returns** | 0, or a negative native code |

### cpu_dit

```mach
pub fun cpu_dit() i64
```

whether the processor and kernel provide the data-independent-timing mode

aarch64 reads HWCAP_DIT (bit 24) from AT_HWCAP through the same auxv reader
`cpu_features` uses; the kernel sets it when ID_AA64PFR0_EL1.DIT is 1. a
caller that runs before the runtime captured envp sees ENOSYS. no other
architecture has the mode

| Parameter | |
| :--- | :--- |
| **returns** | 1 when present, 0 when absent, or a negative native code |

### cpu_count

```mach
pub fun cpu_count() i64
```

the number of CPUs available to this process

popcounts the sched_getaffinity mask, so taskset/cgroup cpuset restrictions
are honoured; the kernel reports the mask size it wrote in the return value.
never returns less than 1.

| Parameter | |
| :--- | :--- |
| **returns** | usable CPU count (>= 1) |

### thread_affinity

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

read the calling thread's CPU affinity

CPU i is bit i % 64 of words[i / 64]. the kernel reports the bytes it wrote,
which is its own cpumask size, so out_count is that size in words and every
word the kernel wrote is copied, including trailing zero words.

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

| Parameter | |
| :--- | :--- |
| `words` | mask words, CPU i is bit i % 64 of words[i / 64] |
| `count` | number of mask words |
| **returns** | 0, EINVAL for an empty or disallowed set, or the native refusal |

### getcwd

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

the raw syscall returns the length INCLUDING the terminator; this layer
reports the path length the way darwin and windows do, so "length of path"
means one thing across the three backends (#432).

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `size` | buffer capacity in bytes, including room for the terminator |
| **returns** | length of the path, excluding the terminator, or negative errno |

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

### thread_wait

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

wraps the futex FUTEX_WAIT operation. returns immediately if *addr
does not equal expected. spurious wakeups are possible.

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

wake one thread blocked on a futex wait at addr

| Parameter | |
| :--- | :--- |
| `addr` | pointer to the futex word |
| **returns** | number of threads woken, or negative errno |

### io_queue_create

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_watch

```mach
pub fun io_queue_watch(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

registers a resource that has no registration on the queue yet. a resource
that is already registered is refused with EEXIST, never taken over

### io_queue_rearm

```mach
pub fun io_queue_rearm(queue: *std.system.os.shared.IoQueue, resource: usize, context: usize, events: u32) i64
```

arms again a registration the caller made with io_queue_watch

### duplicate_to

```mach
pub fun duplicate_to(from: usize, to: usize) i64
```

makes the descriptor to name what from names, closing whatever to named
before, in one step. the copy is not inherited across exec

| Parameter | |
| :--- | :--- |
| `from` | an open descriptor |
| `to` | the descriptor number to take over |
| **returns** | 0, or the native failure |

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

nil is invalid use and a closed queue is EBADF on every platform

### io_queue_close

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

### sock_send

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

send data on a connected socket

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `buf` | source buffer |
| `len` | number of bytes to send |
| **returns** | bytes sent, or negative errno |

### sock_recv

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

receive data from a connected socket

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `buf` | destination buffer |
| `len` | maximum bytes to receive |
| **returns** | bytes received, or negative errno |

### sock_peek_readable

```mach
pub fun sock_peek_readable(fd: usize) i64
```

peek at a stream socket without consuming or blocking

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| **returns** | 1 when a byte is readable, 0 at orderly end of stream, EAGAIN when nothing is ready yet, or the socket's negative errno |

### sock_recv_close_rights

```mach
pub fun sock_recv_close_rights(fd: usize, buffer: *u8, length: usize, address: *u8, address_length: *u32, control: *u8, capacity: usize) i64
```

receives bytes and closes every descriptor the kernel installed for them. installation is
close-on-exec, the kernel installs no descriptor it does not report (scm_detach_fds writes
the slot before fd_install and drops what does not fit under MSG_CTRUNC), and close always
releases a descriptor on linux, so the byte count is the outcome and the walk is complete.
address, when given, receives the sender and address_length its extent.

### local_stream_recv

```mach
pub fun local_stream_recv(fd: usize, buffer: *u8, length: usize) i64
```

byte reception for local streams: rights a peer attaches are observed and closed

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

close a socket file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| **returns** | 0 on success, or negative errno |

### sock_create

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

create a socket file descriptor

| Parameter | |
| :--- | :--- |
| `domain` | address family (AF_INET) |
| `typ` | socket type (SOCK_STREAM, SOCK_DGRAM) |
| `protocol` | protocol (0 for default) |
| `out` | receives the native-width handle |
| **returns** | 0 on success, or negative errno |

### sock_create_flags

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_bind

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

bind a socket to an address

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `addr` | pointer to sockaddr structure |
| `addrlen` | size of the sockaddr structure |
| **returns** | 0 on success, or negative errno |

### sock_listen

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

mark a socket as a passive listener

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `backlog` | maximum pending connection queue length |
| **returns** | 0 on success, or negative errno |

### sock_accept

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

accept a connection on a listening socket

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `addr` | pointer to sockaddr to fill with peer address |
| `addrlen` | pointer to sockaddr length (in/out) |
| `out` | receives the native-width accepted handle |
| **returns** | 0 on success, or negative errno |

### sock_accept_flags

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_connect

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

connect a socket to a remote address

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `addr` | pointer to sockaddr structure |
| `addrlen` | size of the sockaddr structure |
| **returns** | 0 on success, or negative errno |

### sock_sendto

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

send data to a specific address

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `buf` | source buffer |
| `len` | number of bytes to send |
| `flags` | send flags |
| `addr` | pointer to destination sockaddr |
| `addrlen` | size of the sockaddr structure |
| **returns** | bytes sent on success, or negative errno |

### sock_recvfrom

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

receive data and source address

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `buf` | destination buffer |
| `len` | maximum bytes to receive |
| `flags` | recv flags |
| `addr` | pointer to sockaddr to fill with source address |
| `addrlen` | pointer to sockaddr length (in/out) |
| **returns** | bytes received on success, or negative errno |

### sock_shutdown

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

shut down part or all of a socket connection

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `how` | SHUT_RD (0), SHUT_WR (1), or SHUT_RDWR (2) |
| **returns** | 0 on success, or negative errno |

### sock_setopt

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

set a socket option

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `level` | option level (SOL_SOCKET, etc.) |
| `opt` | option name (SO_REUSEADDR, etc.) |
| `value` | pointer to option value |
| `vallen` | size of option value |
| **returns** | 0 on success, or negative errno |

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

| Parameter | |
| :--- | :--- |
| `fd` | socket fd |
| `ms` | timeout in milliseconds, or 0 for no timeout |
| **returns** | 0 on success, or negative errno |

### random_fill

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

fill a buffer with cryptographic random bytes via getrandom

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `len` | number of bytes to fill |
| **returns** | 0 on success, or negative errno |

### error_message

```mach
pub fun error_message(code: i64) str
```

return a human-readable message for a negated errno code

| Parameter | |
| :--- | :--- |
| `code` | negated errno value (e.g., -2 for ENOENT) |
| **returns** | descriptive error message string |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `SYS_FUTEX` | `usize` | `202` where `$mach.build.arch == $mach.arch.x86_64`; `98` where `$mach.build.arch == $mach.arch.aarch64`; `98` where `$mach.build.arch == $mach.arch.riscv64`; `422` where `$mach.build.arch == $mach.arch.riscv32` | syscall numbers are architecture-specific: x86_64 has its own table, while aarch64 and riscv64 both use the generic asm-generic/unistd table |
| `FUTEX_WAIT` | `usize` | `0` | constants identical across linux architectures (asm-generic matches x86_64 for these), declared once at module scope |
| `FUTEX_WAKE` | `usize` | `1` |  |
| `FUTEX_WAIT_BITSET` | `usize` | `9` |  |
| `FUTEX_BITSET_MATCH_ANY` | `usize` | `0xffffffff` |  |
| `CLONE_VM` | `usize` | `0x00000100` |  |
| `CLONE_FS` | `usize` | `0x00000200` |  |
| `CLONE_FILES` | `usize` | `0x00000400` |  |
| `CLONE_SIGHAND` | `usize` | `0x00000800` |  |
| `CLONE_THREAD` | `usize` | `0x00010000` |  |
| `CLONE_SYSVSEM` | `usize` | `0x00040000` |  |
| `CLONE_SETTLS` | `usize` | `0x00080000` |  |
| `PROT_READ` | `i32` | `1` | the read-only protection, exported for the static-PIE RELRO re-protection in std.runtime.linux.reloc |
| `ENOSYS` | `i64` | `-38` |  |
| `separator` | `u8` | `'/'` | path |
| `STDIN_FD` | `i32` | `0` | portable constants |
| `STDOUT_FD` | `i32` | `1` |  |
| `STDERR_FD` | `i32` | `2` |  |
| `O_RDONLY` | `i32` | `0` |  |
| `O_WRONLY` | `i32` | `1` |  |
| `O_RDWR` | `i32` | `2` |  |
| `O_CREAT` | `i32` | `64` |  |
| `O_EXCL` | `i32` | `128` |  |
| `O_TRUNC` | `i32` | `512` |  |
| `O_APPEND` | `i32` | `1024` |  |
| `O_NONBLOCK` | `i32` | `0o4000` |  |
| `O_DIRECTORY` | `i32` | `0o40000` where `$mach.build.arch == $mach.arch.aarch64`; `0o200000` otherwise | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
| `O_NOFOLLOW` | `i32` | `0o100000` where `$mach.build.arch == $mach.arch.aarch64`; `0o400000` otherwise | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
| `O_DIRECT` | `i32` | `0o200000` where `$mach.build.arch == $mach.arch.aarch64`; `0o40000` otherwise | O_DIRECTORY, O_NOFOLLOW, and O_DIRECT are arch-gated, and ARM shifts them relative to asm-generic |
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
| `ERANGE` | `i64` | `-34` |  |
| `EADDRINUSE` | `i64` | `-98` |  |
| `ENETUNREACH` | `i64` | `-101` |  |
| `ECONNABORTED` | `i64` | `-103` |  |
| `ECONNRESET` | `i64` | `-104` |  |
| `ENOTCONN` | `i64` | `-107` |  |
| `ETIMEDOUT` | `i64` | `-110` |  |
| `ECONNREFUSED` | `i64` | `-111` |  |
| `EHOSTUNREACH` | `i64` | `-113` |  |
| `ECANCELED` | `i64` | `-125` |  |
| `EINTR_MAX_RETRIES` | `usize` | `8` |  |
| `THREAD_STACK_GUARD` | `usize` | `65536` | the inaccessible bytes below every spawned thread's stack, so an overflow faults instead of writing into the mapping below |
| `IO_EVENT_READ` | `u32` | `0x01` |  |
| `IO_EVENT_WRITE` | `u32` | `0x02` |  |
| `IO_EVENT_ERROR` | `u32` | `0x04` |  |
| `IO_EVENT_HANGUP` | `u32` | `0x08` |  |
| `IO_EVENT_WAKE` | `u32` | `0x10` |  |
| `AF_INET` | `i32` | `2` |  |
| `AF_INET6` | `i32` | `10` |  |
| `SOCK_STREAM` | `i32` | `1` |  |
| `SOCK_DGRAM` | `i32` | `2` |  |
| `SOCK_NONBLOCK` | `i32` | `O_NONBLOCK` |  |
| `SOCK_CLOEXEC` | `i32` | `0x80000` |  |
| `SOL_SOCKET` | `i32` | `1` |  |
| `SO_UNSUPPORTED` | `i32` | `-2147483648` |  |
| `SO_REUSEADDR` | `i32` | `2` |  |
| `SO_REUSEPORT` | `i32` | `15` |  |
| `SO_EXCLUSIVEADDRUSE` | `i32` | `SO_UNSUPPORTED` |  |
| `SO_KEEPALIVE` | `i32` | `9` |  |
| `SO_SNDBUF` | `i32` | `7` |  |
| `SO_RCVBUF` | `i32` | `8` |  |
| `SO_LINGER` | `i32` | `13` |  |
| `SO_RCVTIMEO` | `i32` | `66` where `$mach.build.arch == $mach.arch.riscv32`; `20` otherwise | riscv32 takes the 64-bit timeval sock_set_rcvtimeo writes only as SO_RCVTIMEO_NEW |
| `IPPROTO_IP` | `i32` | `0` |  |
| `IPPROTO_TCP` | `i32` | `6` |  |
| `IPPROTO_IPV6` | `i32` | `41` |  |
| `IP_TOS` | `i32` | `1` |  |
| `IPV6_V6ONLY` | `i32` | `26` |  |
| `IPV6_TCLASS` | `i32` | `67` |  |
| `TCP_NODELAY` | `i32` | `1` |  |
| `TCP_KEEPIDLE` | `i32` | `4` |  |
| `TCP_KEEPINTVL` | `i32` | `5` |  |
| `TCP_KEEPCNT` | `i32` | `6` |  |
| `TCP_FASTOPEN` | `i32` | `23` |  |
| `SHUT_RD` | `i32` | `0` |  |
| `SHUT_WR` | `i32` | `1` |  |
| `SHUT_RDWR` | `i32` | `2` |  |
| `SOCKADDR_IN_SIZE` | `usize` | `16` |  |
| `SOCKADDR_IN6_SIZE` | `usize` | `28` |  |
| `SOCKADDR_STORAGE_SIZE` | `usize` | `128` |  |
| `MSG_CTRUNC` | `i32` | `0x8` |  |
| `MSG_CMSG_CLOEXEC` | `i32` | `0x40000000` |  |
| `SCM_RIGHTS` | `i32` | `1` |  |
| `SCM_CREDENTIALS` | `i32` | `2` |  |
| `SCM_PIDFD` | `i32` | `4` |  |
| `SCM_MAX_FD` | `usize` | `253` | net/scm.h SCM_MAX_FD: sendmsg refuses a larger descriptor set, and a stream receive returns at most one set (unix_stream_read_generic stops after the record that carries it) |
| `LOCAL_CONTROL_CAPACITY` | `usize` | `1088` where `$mach.build.pointer_width == 8`; `1064` otherwise | CMSG_SPACE(253 descriptors) + CMSG_SPACE(ucred) + CMSG_SPACE(pidfd): the largest descriptor set together with the fixed-size records SO_PASSCRED and SO_PASSPIDFD prepend to it |
| `CONNECT_PENDING` | `i64` | `1` | what sock_connect_begin and sock_connect_poll return while the connect is in flight |
| `DNS_HOSTS_PATH` | `str` | `"/etc/hosts"` |  |

## Variables

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `_envp` (var) | `usize` | `0` | environment (set by runtime at program start) |
| `_pagesz` (var) | `usize` | `0` | the runtime page size in bytes, read from the auxiliary vector (AT_PAGESZ) at program start |

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

