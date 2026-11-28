[std](../../README.md) / [system](../README.md) / [os](README.md) / **linux**

# std.system.os.linux

linux OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need linux-specific functionality import this module
directly rather than going through std.system.os.

Source: [`src/system/os/linux.mach`](../../../../src/system/os/linux.mach)

| Forwards | |
| :--- | :--- |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`timespec`](#timespec), [`DirectoryCursor`](#directorycursor), [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`separator`](#separator) | path |
| [`STDIN_FD`](#stdin_fd) | constants |
| [`STDOUT_FD`](#stdout_fd), [`STDERR_FD`](#stderr_fd), [`O_RDONLY`](#o_rdonly), [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_NONBLOCK`](#o_nonblock), [`O_DIRECTORY`](#o_directory), [`O_NOFOLLOW`](#o_nofollow), [`AT_FDCWD`](#at_fdcwd), [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow), [`AT_REMOVEDIR`](#at_removedir) | |
| [`LOCK_SH`](#lock_sh) | advisory file-lock operations |
| [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un), [`S_IFMT`](#s_ifmt), [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk), [`WNOHANG`](#wnohang), [`WUNTRACED`](#wuntraced), [`WCONTINUED`](#wcontinued), [`CLOCK_REALTIME`](#clock_realtime), [`CLOCK_MONOTONIC`](#clock_monotonic), [`EPERM`](#eperm), [`ENOENT`](#enoent), [`ESRCH`](#esrch), [`EINTR`](#eintr), [`EIO`](#eio), [`ENXIO`](#enxio), [`E2BIG`](#e2big), [`EBADF`](#ebadf), [`ECHILD`](#echild), [`EAGAIN`](#eagain), [`ENOMEM`](#enomem), [`EACCES`](#eacces), [`EFAULT`](#efault), [`EBUSY`](#ebusy), [`EEXIST`](#eexist), [`ENODEV`](#enodev), [`ENOTDIR`](#enotdir), [`EISDIR`](#eisdir), [`EINVAL`](#einval), [`ENFILE`](#enfile), [`EMFILE`](#emfile), [`ETXTBSY`](#etxtbsy), [`ENOSPC`](#enospc), [`EROFS`](#erofs), [`EPIPE`](#epipe), [`ENAMETOOLONG`](#enametoolong), [`ERANGE`](#erange), [`ENOTEMPTY`](#enotempty), [`ELOOP`](#eloop), [`ENOTSUP`](#enotsup), [`EADDRINUSE`](#eaddrinuse), [`ENETUNREACH`](#enetunreach), [`ECONNABORTED`](#econnaborted), [`ECONNRESET`](#econnreset), [`ENOTCONN`](#enotconn), [`ETIMEDOUT`](#etimedout), [`ECONNREFUSED`](#econnrefused), [`EHOSTUNREACH`](#ehostunreach), [`ECANCELED`](#ecanceled), [`EINTR_MAX_RETRIES`](#eintr_max_retries) | |
| [`has_numa`](#has_numa) | feature detection |
| [`has_huge_pages`](#has_huge_pages) | |
| [`syscall0`](#syscall0) | syscall wrappers |
| [`syscall1`](#syscall1), [`syscall2`](#syscall2), [`syscall3`](#syscall3), [`syscall4`](#syscall4), [`syscall5`](#syscall5), [`syscall6`](#syscall6) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size), [`map_alignment`](#map_alignment), [`allocate_huge`](#allocate_huge), [`numa_node_count`](#numa_node_count), [`numa_current_node`](#numa_current_node), [`numa_allocate`](#numa_allocate), [`numa_move`](#numa_move), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`read`](#read) | filesystem |
| [`write`](#write), [`write_vector`](#write_vector), [`read_at`](#read_at), [`write_at`](#write_at), [`open`](#open) | |
| [`open_native`](#open_native) | the kernel takes a name as bytes, so the native-unit open is open itself |
| [`close`](#close), [`sync_fd`](#sync_fd), [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at) | |
| [`set_mode_at_native`](#set_mode_at_native) | every name below reaches the kernel as bytes, so each native form is the UTF-8 primitive itself |
| [`file_identity`](#file_identity), [`identity_at`](#identity_at), [`identity_at_native`](#identity_at_native), [`retain_identity_at`](#retain_identity_at), [`retain_identity_at_native`](#retain_identity_at_native), [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path), [`stat_path_native`](#stat_path_native), [`stat_mode`](#stat_mode), [`stat_birth`](#stat_birth), [`unlink`](#unlink), [`unlink_native`](#unlink_native), [`rename`](#rename), [`rename_native`](#rename_native), [`symlink`](#symlink), [`symlink_native`](#symlink_native), [`make_dir`](#make_dir), [`make_dir_native`](#make_dir_native), [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_dnit`](#directory_dnit), [`access`](#access), [`access_native`](#access_native), [`seek`](#seek), [`lock_fd`](#lock_fd) | |
| [`terminate`](#terminate) | process |
| [`abort`](#abort), [`terminate_child`](#terminate_child), [`setpgid`](#setpgid), [`getpgid`](#getpgid), [`terminate_group`](#terminate_group), [`kill_group`](#kill_group), [`probe_group`](#probe_group), [`process_watch`](#process_watch), [`process_unwatch`](#process_unwatch), [`spawn`](#spawn), [`spawn_grouped`](#spawn_grouped), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_grouped`](#spawn_redirected_grouped), [`spawn_redirected_in`](#spawn_redirected_in), [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | |
| [`spawn_native`](#spawn_native) | the kernel takes paths and arguments as bytes, so the native-unit spawns are the spawns themselves |
| [`spawn_in_native`](#spawn_in_native), [`spawn_redirected_native`](#spawn_redirected_native), [`spawn_redirected_in_native`](#spawn_redirected_in_native), [`spawn_redirected_in_grouped_native`](#spawn_redirected_in_grouped_native), [`getpid`](#getpid), [`running_under_user_emulation`](#running_under_user_emulation), [`pipe`](#pipe), [`ignore_sigpipe`](#ignore_sigpipe), [`sleep`](#sleep), [`cpu_count`](#cpu_count), [`cpu_features`](#cpu_features), [`cpu_dit`](#cpu_dit), [`thread_affinity`](#thread_affinity), [`set_thread_affinity`](#set_thread_affinity), [`getcwd`](#getcwd), [`getcwd_native`](#getcwd_native), [`getenv`](#getenv), [`environ`](#environ) | |
| [`getenv_native`](#getenv_native) | the environment is the bytes the kernel passed, so its native reads are the reads themselves |
| [`environ_native`](#environ_native), [`temp_dir`](#temp_dir), [`fork`](#fork), [`vfork`](#vfork), [`exec`](#exec), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`MemoryLimit`](#memorylimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`locked_memory_limit`](#locked_memory_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`AF_INET`](#af_inet) | sockets |
| [`AF_INET6`](#af_inet6), [`SOCK_STREAM`](#sock_stream), [`SOCK_DGRAM`](#sock_dgram), [`SOCK_NONBLOCK`](#sock_nonblock), [`SOCK_CLOEXEC`](#sock_cloexec), [`SOL_SOCKET`](#sol_socket), [`SO_UNSUPPORTED`](#so_unsupported), [`SO_REUSEADDR`](#so_reuseaddr), [`SO_REUSEPORT`](#so_reuseport), [`SO_EXCLUSIVEADDRUSE`](#so_exclusiveaddruse), [`SO_KEEPALIVE`](#so_keepalive), [`SO_SNDBUF`](#so_sndbuf), [`SO_RCVBUF`](#so_rcvbuf), [`SO_LINGER`](#so_linger), [`SO_RCVTIMEO`](#so_rcvtimeo), [`IPPROTO_IP`](#ipproto_ip), [`IPPROTO_TCP`](#ipproto_tcp), [`IPPROTO_IPV6`](#ipproto_ipv6), [`IP_TOS`](#ip_tos), [`IPV6_V6ONLY`](#ipv6_v6only), [`IPV6_TCLASS`](#ipv6_tclass), [`TCP_NODELAY`](#tcp_nodelay), [`TCP_KEEPIDLE`](#tcp_keepidle), [`TCP_KEEPINTVL`](#tcp_keepintvl), [`TCP_KEEPCNT`](#tcp_keepcnt), [`TCP_FASTOPEN`](#tcp_fastopen), [`SHUT_RD`](#shut_rd), [`SHUT_WR`](#shut_wr), [`SHUT_RDWR`](#shut_rdwr), [`SOCKADDR_IN_SIZE`](#sockaddr_in_size), [`SOCKADDR_IN6_SIZE`](#sockaddr_in6_size), [`SOCKADDR_STORAGE_SIZE`](#sockaddr_storage_size), [`sock_send`](#sock_send), [`sock_recv`](#sock_recv), [`IoVector`](#iovector), [`sock_write_vector`](#sock_write_vector), [`sock_send_message`](#sock_send_message), [`sock_receive_message`](#sock_receive_message), [`MSG_CTRUNC`](#msg_ctrunc), [`MSG_CMSG_CLOEXEC`](#msg_cmsg_cloexec), [`SCM_RIGHTS`](#scm_rights), [`SCM_CREDENTIALS`](#scm_credentials), [`SCM_PIDFD`](#scm_pidfd), [`SCM_MAX_FD`](#scm_max_fd), [`LOCAL_CONTROL_CAPACITY`](#local_control_capacity), [`sock_recv_close_rights`](#sock_recv_close_rights), [`local_stream_recv`](#local_stream_recv), [`sock_set_nonblocking`](#sock_set_nonblocking), [`sock_connect_begin`](#sock_connect_begin), [`sock_connect_poll`](#sock_connect_poll), [`CONNECT_PENDING`](#connect_pending), [`sock_close`](#sock_close), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto), [`sock_recvfrom`](#sock_recvfrom), [`sock_peek_readable`](#sock_peek_readable), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable), [`IoCompletion`](#iocompletion), [`IO_EVENT_READ`](#io_event_read), [`IO_EVENT_WRITE`](#io_event_write), [`IO_EVENT_ERROR`](#io_event_error), [`IO_EVENT_HANGUP`](#io_event_hangup), [`IO_EVENT_WAKE`](#io_event_wake), [`io_queue_create`](#io_queue_create), [`io_queue_wait`](#io_queue_wait), [`io_queue_watch`](#io_queue_watch), [`io_queue_rearm`](#io_queue_rearm), [`duplicate_to`](#duplicate_to), [`io_queue_unwatch`](#io_queue_unwatch), [`io_queue_poll`](#io_queue_poll), [`io_queue_wake`](#io_queue_wake), [`io_queue_close`](#io_queue_close), [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | |
| [`DNS_HOSTS_PATH`](#dns_hosts_path) | dns |
| [`random_fill`](#random_fill) | random |
| [`thread_spawn`](#thread_spawn) | threads |
| [`thread_join`](#thread_join), [`thread_detach`](#thread_detach), [`thread_current_id`](#thread_current_id), [`thread_current_name`](#thread_current_name), [`thread_wait`](#thread_wait), [`thread_wait_until`](#thread_wait_until), [`thread_wake`](#thread_wake), [`thread_block`](#thread_block), [`thread_block_enter`](#thread_block_enter), [`stack_bounds`](#stack_bounds) | |
| [`clock_gettime`](#clock_gettime) | time |
| [`error_kind`](#error_kind) | errno |
| [`error_message`](#error_message) | |

---

## Forwards

### stat_t

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat_t`](linux/x86_64.md#stat_t), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat_t`](linux/aarch64.md#stat_t), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat_t`](linux/riscv64.md#stat_t), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat_t`](linux/riscv32.md#stat_t), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec stat_t {
    st_dev:             u64;
    st_ino:             u64;
    st_mode:            u32;
    st_nlink:           u32;
    st_uid:             u32;
    st_gid:             u32;
    st_rdev:            u64;
    st_size:            i64;
    st_blksize:         i32;
    st_blocks:          i64;
    st_atime:           i64;
    st_atime_nsec:      i64;
    st_mtime:           i64;
    st_mtime_nsec:      i64;
    st_ctime:           i64;
    st_ctime_nsec:      i64;
    st_birthtime:       i64;
    st_birthtime_nsec:  i64;
    st_birthtime_known: bool;
}
```

kernel ABI types

### timespec

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.timespec`](linux/x86_64.md#timespec), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.timespec`](linux/aarch64.md#timespec), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.timespec`](linux/riscv64.md#timespec), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.timespec`](linux/riscv32.md#timespec), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

### DirectoryCursor

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.DirectoryCursor`](linux/x86_64.md#directorycursor), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.DirectoryCursor`](linux/aarch64.md#directorycursor), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.DirectoryCursor`](linux/riscv64.md#directorycursor), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.DirectoryCursor`](linux/riscv32.md#directorycursor), where `$mach.build.arch == $mach.arch.riscv32`

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

an open enumeration of one directory descriptor's entries

### DirectoryEntry

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.DirectoryEntry`](linux/x86_64.md#directoryentry), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.DirectoryEntry`](linux/aarch64.md#directoryentry), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.DirectoryEntry`](linux/riscv64.md#directoryentry), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.DirectoryEntry`](linux/riscv32.md#directoryentry), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### DirectoryInitResult

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.DirectoryInitResult`](linux/x86_64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.DirectoryInitResult`](linux/aarch64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.DirectoryInitResult`](linux/riscv64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.DirectoryInitResult`](linux/riscv32.md#directoryinitresult), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### separator

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.separator`](linux/x86_64.md#separator), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.separator`](linux/aarch64.md#separator), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.separator`](linux/riscv64.md#separator), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.separator`](linux/riscv32.md#separator), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val separator: u8 = '/'
```

path

### STDIN_FD

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.STDIN_FD`](linux/x86_64.md#stdin_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.STDIN_FD`](linux/aarch64.md#stdin_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.STDIN_FD`](linux/riscv64.md#stdin_fd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.STDIN_FD`](linux/riscv32.md#stdin_fd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val STDIN_FD:  i32 = 0
```

constants

### STDOUT_FD

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.STDOUT_FD`](linux/x86_64.md#stdout_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.STDOUT_FD`](linux/aarch64.md#stdout_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.STDOUT_FD`](linux/riscv64.md#stdout_fd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.STDOUT_FD`](linux/riscv32.md#stdout_fd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val STDOUT_FD: i32 = 1
```

### STDERR_FD

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.STDERR_FD`](linux/x86_64.md#stderr_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.STDERR_FD`](linux/aarch64.md#stderr_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.STDERR_FD`](linux/riscv64.md#stderr_fd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.STDERR_FD`](linux/riscv32.md#stderr_fd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val STDERR_FD: i32 = 2
```

### O_RDONLY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_RDONLY`](linux/x86_64.md#o_rdonly), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_RDONLY`](linux/aarch64.md#o_rdonly), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_RDONLY`](linux/riscv64.md#o_rdonly), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_RDONLY`](linux/riscv32.md#o_rdonly), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_RDONLY:   i32 = 0
```

### O_WRONLY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_WRONLY`](linux/x86_64.md#o_wronly), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_WRONLY`](linux/aarch64.md#o_wronly), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_WRONLY`](linux/riscv64.md#o_wronly), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_WRONLY`](linux/riscv32.md#o_wronly), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_WRONLY:   i32 = 1
```

### O_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_RDWR`](linux/x86_64.md#o_rdwr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_RDWR`](linux/aarch64.md#o_rdwr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_RDWR`](linux/riscv64.md#o_rdwr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_RDWR`](linux/riscv32.md#o_rdwr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_RDWR:     i32 = 2
```

### O_CREAT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_CREAT`](linux/x86_64.md#o_creat), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_CREAT`](linux/aarch64.md#o_creat), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_CREAT`](linux/riscv64.md#o_creat), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_CREAT`](linux/riscv32.md#o_creat), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_CREAT:    i32 = 64
```

### O_EXCL

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_EXCL`](linux/x86_64.md#o_excl), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_EXCL`](linux/aarch64.md#o_excl), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_EXCL`](linux/riscv64.md#o_excl), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_EXCL`](linux/riscv32.md#o_excl), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_EXCL:     i32 = 128
```

### O_TRUNC

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_TRUNC`](linux/x86_64.md#o_trunc), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_TRUNC`](linux/aarch64.md#o_trunc), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_TRUNC`](linux/riscv64.md#o_trunc), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_TRUNC`](linux/riscv32.md#o_trunc), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_TRUNC:    i32 = 512
```

### O_APPEND

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_APPEND`](linux/x86_64.md#o_append), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_APPEND`](linux/aarch64.md#o_append), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_APPEND`](linux/riscv64.md#o_append), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_APPEND`](linux/riscv32.md#o_append), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_APPEND:   i32 = 1024
```

### O_NONBLOCK

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_NONBLOCK`](linux/x86_64.md#o_nonblock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_NONBLOCK`](linux/aarch64.md#o_nonblock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_NONBLOCK`](linux/riscv64.md#o_nonblock), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_NONBLOCK`](linux/riscv32.md#o_nonblock), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val O_NONBLOCK: i32 = 0o4000
```

### O_DIRECTORY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_DIRECTORY`](linux/x86_64.md#o_directory), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_DIRECTORY`](linux/aarch64.md#o_directory), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_DIRECTORY`](linux/riscv64.md#o_directory), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_DIRECTORY`](linux/riscv32.md#o_directory), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.O_NOFOLLOW`](linux/x86_64.md#o_nofollow), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.O_NOFOLLOW`](linux/aarch64.md#o_nofollow), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.O_NOFOLLOW`](linux/riscv64.md#o_nofollow), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.O_NOFOLLOW`](linux/riscv32.md#o_nofollow), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.AT_FDCWD`](linux/x86_64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.AT_FDCWD`](linux/aarch64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.AT_FDCWD`](linux/riscv64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.AT_FDCWD`](linux/riscv32.md#at_fdcwd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val AT_FDCWD:            i32 = -100
```

### AT_SYMLINK_NOFOLLOW

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.AT_SYMLINK_NOFOLLOW`](linux/x86_64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.AT_SYMLINK_NOFOLLOW`](linux/aarch64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.AT_SYMLINK_NOFOLLOW`](linux/riscv64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.AT_SYMLINK_NOFOLLOW`](linux/riscv32.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0100
```

### AT_REMOVEDIR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.AT_REMOVEDIR`](linux/x86_64.md#at_removedir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.AT_REMOVEDIR`](linux/aarch64.md#at_removedir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.AT_REMOVEDIR`](linux/riscv64.md#at_removedir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.AT_REMOVEDIR`](linux/riscv32.md#at_removedir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val AT_REMOVEDIR:        i32 = 0x0200
```

### LOCK_SH

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.LOCK_SH`](linux/x86_64.md#lock_sh), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.LOCK_SH`](linux/aarch64.md#lock_sh), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.LOCK_SH`](linux/riscv64.md#lock_sh), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.LOCK_SH`](linux/riscv32.md#lock_sh), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val LOCK_SH: i32 = 1
```

advisory file-lock operations

### LOCK_EX

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.LOCK_EX`](linux/x86_64.md#lock_ex), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.LOCK_EX`](linux/aarch64.md#lock_ex), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.LOCK_EX`](linux/riscv64.md#lock_ex), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.LOCK_EX`](linux/riscv32.md#lock_ex), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.LOCK_NB`](linux/x86_64.md#lock_nb), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.LOCK_NB`](linux/aarch64.md#lock_nb), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.LOCK_NB`](linux/riscv64.md#lock_nb), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.LOCK_NB`](linux/riscv32.md#lock_nb), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.LOCK_UN`](linux/x86_64.md#lock_un), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.LOCK_UN`](linux/aarch64.md#lock_un), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.LOCK_UN`](linux/riscv64.md#lock_un), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.LOCK_UN`](linux/riscv32.md#lock_un), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.S_IFMT`](linux/x86_64.md#s_ifmt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.S_IFMT`](linux/aarch64.md#s_ifmt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.S_IFMT`](linux/riscv64.md#s_ifmt), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.S_IFMT`](linux/riscv32.md#s_ifmt), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val S_IFMT:  u32 = 0o170000
```

### S_IFDIR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.S_IFDIR`](linux/x86_64.md#s_ifdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.S_IFDIR`](linux/aarch64.md#s_ifdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.S_IFDIR`](linux/riscv64.md#s_ifdir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.S_IFDIR`](linux/riscv32.md#s_ifdir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.S_IFREG`](linux/x86_64.md#s_ifreg), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.S_IFREG`](linux/aarch64.md#s_ifreg), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.S_IFREG`](linux/riscv64.md#s_ifreg), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.S_IFREG`](linux/riscv32.md#s_ifreg), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.S_IFLNK`](linux/x86_64.md#s_iflnk), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.S_IFLNK`](linux/aarch64.md#s_iflnk), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.S_IFLNK`](linux/riscv64.md#s_iflnk), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.S_IFLNK`](linux/riscv32.md#s_iflnk), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val S_IFLNK: u32 = 0o120000
```

### WNOHANG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.WNOHANG`](linux/x86_64.md#wnohang), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.WNOHANG`](linux/aarch64.md#wnohang), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.WNOHANG`](linux/riscv64.md#wnohang), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.WNOHANG`](linux/riscv32.md#wnohang), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val WNOHANG:    i32 = 1
```

### WUNTRACED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.WUNTRACED`](linux/x86_64.md#wuntraced), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.WUNTRACED`](linux/aarch64.md#wuntraced), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.WUNTRACED`](linux/riscv64.md#wuntraced), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.WUNTRACED`](linux/riscv32.md#wuntraced), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val WUNTRACED:  i32 = 2
```

### WCONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.WCONTINUED`](linux/x86_64.md#wcontinued), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.WCONTINUED`](linux/aarch64.md#wcontinued), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.WCONTINUED`](linux/riscv64.md#wcontinued), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.WCONTINUED`](linux/riscv32.md#wcontinued), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val WCONTINUED: i32 = 8
```

### CLOCK_REALTIME

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.CLOCK_REALTIME`](linux/x86_64.md#clock_realtime), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.CLOCK_REALTIME`](linux/aarch64.md#clock_realtime), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.CLOCK_REALTIME`](linux/riscv64.md#clock_realtime), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.CLOCK_REALTIME`](linux/riscv32.md#clock_realtime), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val CLOCK_REALTIME:  i32 = 0
```

### CLOCK_MONOTONIC

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.CLOCK_MONOTONIC`](linux/x86_64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.CLOCK_MONOTONIC`](linux/aarch64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.CLOCK_MONOTONIC`](linux/riscv64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.CLOCK_MONOTONIC`](linux/riscv32.md#clock_monotonic), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val CLOCK_MONOTONIC: i32 = 1
```

### EPERM

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EPERM`](linux/x86_64.md#eperm), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EPERM`](linux/aarch64.md#eperm), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EPERM`](linux/riscv64.md#eperm), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EPERM`](linux/riscv32.md#eperm), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EPERM:        i64 = -1
```

### ENOENT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOENT`](linux/x86_64.md#enoent), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOENT`](linux/aarch64.md#enoent), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOENT`](linux/riscv64.md#enoent), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOENT`](linux/riscv32.md#enoent), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOENT:       i64 = -2
```

### ESRCH

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ESRCH`](linux/x86_64.md#esrch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ESRCH`](linux/aarch64.md#esrch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ESRCH`](linux/riscv64.md#esrch), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ESRCH`](linux/riscv32.md#esrch), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ESRCH:        i64 = -3
```

### EINTR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EINTR`](linux/x86_64.md#eintr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EINTR`](linux/aarch64.md#eintr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EINTR`](linux/riscv64.md#eintr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EINTR`](linux/riscv32.md#eintr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EINTR:        i64 = -4
```

### EIO

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EIO`](linux/x86_64.md#eio), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EIO`](linux/aarch64.md#eio), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EIO`](linux/riscv64.md#eio), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EIO`](linux/riscv32.md#eio), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EIO:          i64 = -5
```

### ENXIO

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENXIO`](linux/x86_64.md#enxio), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENXIO`](linux/aarch64.md#enxio), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENXIO`](linux/riscv64.md#enxio), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENXIO`](linux/riscv32.md#enxio), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENXIO:        i64 = -6
```

### E2BIG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.E2BIG`](linux/x86_64.md#e2big), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.E2BIG`](linux/aarch64.md#e2big), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.E2BIG`](linux/riscv64.md#e2big), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.E2BIG`](linux/riscv32.md#e2big), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val E2BIG:        i64 = -7
```

### EBADF

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EBADF`](linux/x86_64.md#ebadf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EBADF`](linux/aarch64.md#ebadf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EBADF`](linux/riscv64.md#ebadf), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EBADF`](linux/riscv32.md#ebadf), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EBADF:        i64 = -9
```

### ECHILD

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ECHILD`](linux/x86_64.md#echild), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ECHILD`](linux/aarch64.md#echild), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ECHILD`](linux/riscv64.md#echild), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ECHILD`](linux/riscv32.md#echild), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ECHILD:       i64 = -10
```

### EAGAIN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EAGAIN`](linux/x86_64.md#eagain), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EAGAIN`](linux/aarch64.md#eagain), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EAGAIN`](linux/riscv64.md#eagain), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EAGAIN`](linux/riscv32.md#eagain), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EAGAIN:       i64 = -11
```

### ENOMEM

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOMEM`](linux/x86_64.md#enomem), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOMEM`](linux/aarch64.md#enomem), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOMEM`](linux/riscv64.md#enomem), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOMEM`](linux/riscv32.md#enomem), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOMEM:       i64 = -12
```

### EACCES

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EACCES`](linux/x86_64.md#eacces), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EACCES`](linux/aarch64.md#eacces), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EACCES`](linux/riscv64.md#eacces), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EACCES`](linux/riscv32.md#eacces), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EACCES:       i64 = -13
```

### EFAULT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EFAULT`](linux/x86_64.md#efault), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EFAULT`](linux/aarch64.md#efault), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EFAULT`](linux/riscv64.md#efault), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EFAULT`](linux/riscv32.md#efault), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EFAULT:       i64 = -14
```

### EBUSY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EBUSY`](linux/x86_64.md#ebusy), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EBUSY`](linux/aarch64.md#ebusy), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EBUSY`](linux/riscv64.md#ebusy), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EBUSY`](linux/riscv32.md#ebusy), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EBUSY:        i64 = -16
```

### EEXIST

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EEXIST`](linux/x86_64.md#eexist), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EEXIST`](linux/aarch64.md#eexist), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EEXIST`](linux/riscv64.md#eexist), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EEXIST`](linux/riscv32.md#eexist), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EEXIST:       i64 = -17
```

### ENODEV

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENODEV`](linux/x86_64.md#enodev), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENODEV`](linux/aarch64.md#enodev), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENODEV`](linux/riscv64.md#enodev), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENODEV`](linux/riscv32.md#enodev), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENODEV:       i64 = -19
```

### ENOTDIR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOTDIR`](linux/x86_64.md#enotdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOTDIR`](linux/aarch64.md#enotdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOTDIR`](linux/riscv64.md#enotdir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOTDIR`](linux/riscv32.md#enotdir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOTDIR:      i64 = -20
```

### EISDIR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EISDIR`](linux/x86_64.md#eisdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EISDIR`](linux/aarch64.md#eisdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EISDIR`](linux/riscv64.md#eisdir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EISDIR`](linux/riscv32.md#eisdir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EISDIR:       i64 = -21
```

### EINVAL

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EINVAL`](linux/x86_64.md#einval), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EINVAL`](linux/aarch64.md#einval), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EINVAL`](linux/riscv64.md#einval), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EINVAL`](linux/riscv32.md#einval), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EINVAL:       i64 = -22
```

### ENFILE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENFILE`](linux/x86_64.md#enfile), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENFILE`](linux/aarch64.md#enfile), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENFILE`](linux/riscv64.md#enfile), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENFILE`](linux/riscv32.md#enfile), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENFILE:       i64 = -23
```

### EMFILE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EMFILE`](linux/x86_64.md#emfile), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EMFILE`](linux/aarch64.md#emfile), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EMFILE`](linux/riscv64.md#emfile), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EMFILE`](linux/riscv32.md#emfile), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EMFILE:       i64 = -24
```

### ETXTBSY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ETXTBSY`](linux/x86_64.md#etxtbsy), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ETXTBSY`](linux/aarch64.md#etxtbsy), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ETXTBSY`](linux/riscv64.md#etxtbsy), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ETXTBSY`](linux/riscv32.md#etxtbsy), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ETXTBSY:      i64 = -26
```

### ENOSPC

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOSPC`](linux/x86_64.md#enospc), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOSPC`](linux/aarch64.md#enospc), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOSPC`](linux/riscv64.md#enospc), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOSPC`](linux/riscv32.md#enospc), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOSPC:       i64 = -28
```

### EROFS

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EROFS`](linux/x86_64.md#erofs), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EROFS`](linux/aarch64.md#erofs), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EROFS`](linux/riscv64.md#erofs), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EROFS`](linux/riscv32.md#erofs), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EROFS:        i64 = -30
```

### EPIPE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EPIPE`](linux/x86_64.md#epipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EPIPE`](linux/aarch64.md#epipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EPIPE`](linux/riscv64.md#epipe), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EPIPE`](linux/riscv32.md#epipe), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EPIPE:        i64 = -32
```

### ENAMETOOLONG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENAMETOOLONG`](linux/x86_64.md#enametoolong), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENAMETOOLONG`](linux/aarch64.md#enametoolong), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENAMETOOLONG`](linux/riscv64.md#enametoolong), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENAMETOOLONG`](linux/riscv32.md#enametoolong), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENAMETOOLONG: i64 = -36
```

### ERANGE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ERANGE`](linux/x86_64.md#erange), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ERANGE`](linux/aarch64.md#erange), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ERANGE`](linux/riscv64.md#erange), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ERANGE`](linux/riscv32.md#erange), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ERANGE:       i64 = -34
```

### ENOTEMPTY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOTEMPTY`](linux/x86_64.md#enotempty), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOTEMPTY`](linux/aarch64.md#enotempty), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOTEMPTY`](linux/riscv64.md#enotempty), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOTEMPTY`](linux/riscv32.md#enotempty), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOTEMPTY:    i64 = -39
```

### ELOOP

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ELOOP`](linux/x86_64.md#eloop), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ELOOP`](linux/aarch64.md#eloop), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ELOOP`](linux/riscv64.md#eloop), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ELOOP`](linux/riscv32.md#eloop), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ELOOP:        i64 = -40
```

### ENOTSUP

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ENOTSUP`](linux/x86_64.md#enotsup), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ENOTSUP`](linux/aarch64.md#enotsup), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ENOTSUP`](linux/riscv64.md#enotsup), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ENOTSUP`](linux/riscv32.md#enotsup), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val ENOTSUP:      i64 = -95
```

### EADDRINUSE

Forwards [`std.system.os.linux.shared.EADDRINUSE`](linux/shared.md#constants).

```mach
pub val EADDRINUSE:   i64 = -98
```

### ENETUNREACH

Forwards [`std.system.os.linux.shared.ENETUNREACH`](linux/shared.md#constants).

```mach
pub val ENETUNREACH:  i64 = -101
```

### ECONNABORTED

Forwards [`std.system.os.linux.shared.ECONNABORTED`](linux/shared.md#constants).

```mach
pub val ECONNABORTED: i64 = -103
```

### ECONNRESET

Forwards [`std.system.os.linux.shared.ECONNRESET`](linux/shared.md#constants).

```mach
pub val ECONNRESET:   i64 = -104
```

### ENOTCONN

Forwards [`std.system.os.linux.shared.ENOTCONN`](linux/shared.md#constants).

```mach
pub val ENOTCONN:     i64 = -107
```

### ETIMEDOUT

Forwards [`std.system.os.linux.shared.ETIMEDOUT`](linux/shared.md#constants).

```mach
pub val ETIMEDOUT:    i64 = -110
```

### ECONNREFUSED

Forwards [`std.system.os.linux.shared.ECONNREFUSED`](linux/shared.md#constants).

```mach
pub val ECONNREFUSED: i64 = -111
```

### EHOSTUNREACH

Forwards [`std.system.os.linux.shared.EHOSTUNREACH`](linux/shared.md#constants).

```mach
pub val EHOSTUNREACH: i64 = -113
```

### ECANCELED

Forwards [`std.system.os.linux.shared.ECANCELED`](linux/shared.md#constants).

```mach
pub val ECANCELED:    i64 = -125
```

### EINTR_MAX_RETRIES

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.EINTR_MAX_RETRIES`](linux/x86_64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.EINTR_MAX_RETRIES`](linux/aarch64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.EINTR_MAX_RETRIES`](linux/riscv64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.EINTR_MAX_RETRIES`](linux/riscv32.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val EINTR_MAX_RETRIES: usize = 8
```

### has_numa

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.has_numa`](linux/x86_64.md#has_numa), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.has_numa`](linux/aarch64.md#has_numa), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.has_numa`](linux/riscv64.md#has_numa), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.has_numa`](linux/riscv32.md#has_numa), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun has_numa() bool
```

feature detection

### has_huge_pages

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.has_huge_pages`](linux/x86_64.md#has_huge_pages), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.has_huge_pages`](linux/aarch64.md#has_huge_pages), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.has_huge_pages`](linux/riscv64.md#has_huge_pages), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.has_huge_pages`](linux/riscv32.md#has_huge_pages), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun has_huge_pages() bool
```

check if the kernel supports huge page allocation

### syscall0

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall0`](linux/x86_64.md#syscall0), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall0`](linux/aarch64.md#syscall0), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall0`](linux/riscv64.md#syscall0), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall0`](linux/riscv32.md#syscall0), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall0(n: usize) i64
```

syscall wrappers

### syscall1

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall1`](linux/x86_64.md#syscall1), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall1`](linux/aarch64.md#syscall1), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall1`](linux/riscv64.md#syscall1), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall1`](linux/riscv32.md#syscall1), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall1(n: usize, a0: usize) i64
```

execute a syscall with 1 argument

### syscall2

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall2`](linux/x86_64.md#syscall2), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall2`](linux/aarch64.md#syscall2), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall2`](linux/riscv64.md#syscall2), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall2`](linux/riscv32.md#syscall2), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall2(n: usize, a0: usize, a1: usize) i64
```

execute a syscall with 2 arguments

### syscall3

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall3`](linux/x86_64.md#syscall3), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall3`](linux/aarch64.md#syscall3), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall3`](linux/riscv64.md#syscall3), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall3`](linux/riscv32.md#syscall3), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall3(n: usize, a0: usize, a1: usize, a2: usize) i64
```

execute a syscall with 3 arguments

### syscall4

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall4`](linux/x86_64.md#syscall4), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall4`](linux/aarch64.md#syscall4), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall4`](linux/riscv64.md#syscall4), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall4`](linux/riscv32.md#syscall4), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall4(n: usize, a0: usize, a1: usize, a2: usize, a3: usize) i64
```

execute a syscall with 4 arguments

### syscall5

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall5`](linux/x86_64.md#syscall5), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall5`](linux/aarch64.md#syscall5), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall5`](linux/riscv64.md#syscall5), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall5`](linux/riscv32.md#syscall5), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall5(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize) i64
```

execute a syscall with 5 arguments

### syscall6

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.syscall6`](linux/x86_64.md#syscall6), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.syscall6`](linux/aarch64.md#syscall6), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.syscall6`](linux/riscv64.md#syscall6), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.syscall6`](linux/riscv32.md#syscall6), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun syscall6(n: usize, a0: usize, a1: usize, a2: usize, a3: usize, a4: usize, a5: usize) i64
```

execute a syscall with 6 arguments

### allocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.allocate`](linux/x86_64.md#allocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.allocate`](linux/aarch64.md#allocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.allocate`](linux/riscv64.md#allocate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.allocate`](linux/riscv32.md#allocate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.deallocate`](linux/x86_64.md#deallocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.deallocate`](linux/aarch64.md#deallocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.deallocate`](linux/riscv64.md#deallocate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.deallocate`](linux/riscv32.md#deallocate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

free memory via munmap

### reallocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.reallocate`](linux/x86_64.md#reallocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.reallocate`](linux/aarch64.md#reallocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.reallocate`](linux/riscv64.md#reallocate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.reallocate`](linux/riscv32.md#reallocate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a memory region via mremap

### heap_region_base

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.heap_region_base`](linux/x86_64.md#heap_region_base), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.heap_region_base`](linux/aarch64.md#heap_region_base), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.heap_region_base`](linux/riscv64.md#heap_region_base), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.heap_region_base`](linux/riscv32.md#heap_region_base), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun heap_region_base() usize
```

query the current program break via brk(0)

### heap_region_extend

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.heap_region_extend`](linux/x86_64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.heap_region_extend`](linux/aarch64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.heap_region_extend`](linux/riscv64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.heap_region_extend`](linux/riscv32.md#heap_region_extend), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun heap_region_extend(addr: usize) usize
```

set the program break to addr via brk

### protect

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.protect`](linux/x86_64.md#protect), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.protect`](linux/aarch64.md#protect), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.protect`](linux/riscv64.md#protect), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.protect`](linux/riscv32.md#protect), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

change protection on a memory region via mprotect

### lock

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.lock`](linux/x86_64.md#lock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.lock`](linux/aarch64.md#lock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.lock`](linux/riscv64.md#lock), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.lock`](linux/riscv32.md#lock), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun lock(p: ptr, size: usize) i64
```

lock a memory region into physical RAM via mlock

### unlock

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.unlock`](linux/x86_64.md#unlock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.unlock`](linux/aarch64.md#unlock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.unlock`](linux/riscv64.md#unlock), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.unlock`](linux/riscv32.md#unlock), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun unlock(p: ptr, size: usize) i64
```

unlock a previously locked memory region via munlock

### advise

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.advise`](linux/x86_64.md#advise), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.advise`](linux/aarch64.md#advise), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.advise`](linux/riscv64.md#advise), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.advise`](linux/riscv32.md#advise), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

advise the kernel on expected access patterns via madvise

### page_size

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.page_size`](linux/x86_64.md#page_size), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.page_size`](linux/aarch64.md#page_size), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.page_size`](linux/riscv64.md#page_size), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.page_size`](linux/riscv32.md#page_size), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun page_size() usize
```

return the system page size

x86_64 linux always presents a 4 KiB base page, but it reads the runtime
AT_PAGESZ the entrypoint captured (shared.capture_pagesz) for one page-size
source of truth across the linux arches. AT_PAGESZ is mandatory on linux, so a
0 here means the auxv lacked it or a caller ran before runtime init;
page_size() panics rather than fabricating a default.

### map_alignment

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.map_alignment`](linux/x86_64.md#map_alignment), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.map_alignment`](linux/aarch64.md#map_alignment), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.map_alignment`](linux/riscv64.md#map_alignment), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.map_alignment`](linux/riscv32.md#map_alignment), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun map_alignment() usize
```

the alignment map_file requires of an offset, the page size

### allocate_huge

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.allocate_huge`](linux/x86_64.md#allocate_huge), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.allocate_huge`](linux/aarch64.md#allocate_huge), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.allocate_huge`](linux/riscv64.md#allocate_huge), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.allocate_huge`](linux/riscv32.md#allocate_huge), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun allocate_huge(size: usize, page_size: usize) ptr
```

allocate memory backed by huge pages via mmap

### numa_node_count

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.numa_node_count`](linux/x86_64.md#numa_node_count), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.numa_node_count`](linux/aarch64.md#numa_node_count), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.numa_node_count`](linux/riscv64.md#numa_node_count), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.numa_node_count`](linux/riscv32.md#numa_node_count), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun numa_node_count() usize
```

return the number of NUMA nodes via get_mempolicy

### numa_current_node

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.numa_current_node`](linux/x86_64.md#numa_current_node), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.numa_current_node`](linux/aarch64.md#numa_current_node), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.numa_current_node`](linux/riscv64.md#numa_current_node), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.numa_current_node`](linux/riscv32.md#numa_current_node), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun numa_current_node() usize
```

return the NUMA node of the current CPU via getcpu

### numa_allocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.numa_allocate`](linux/x86_64.md#numa_allocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.numa_allocate`](linux/aarch64.md#numa_allocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.numa_allocate`](linux/riscv64.md#numa_allocate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.numa_allocate`](linux/riscv32.md#numa_allocate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun numa_allocate(size: usize, node: usize) ptr
```

allocate memory pinned to a specific NUMA node

### numa_move

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.numa_move`](linux/x86_64.md#numa_move), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.numa_move`](linux/aarch64.md#numa_move), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.numa_move`](linux/riscv64.md#numa_move), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.numa_move`](linux/riscv32.md#numa_move), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun numa_move(p: ptr, size: usize, node: usize) i64
```

move a memory region to a different NUMA node via mbind

### map_file

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.map_file`](linux/x86_64.md#map_file), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.map_file`](linux/aarch64.md#map_file), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.map_file`](linux/riscv64.md#map_file), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.map_file`](linux/riscv32.md#map_file), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map a file descriptor into memory via mmap

### sync_file

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sync_file`](linux/x86_64.md#sync_file), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sync_file`](linux/aarch64.md#sync_file), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sync_file`](linux/riscv64.md#sync_file), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sync_file`](linux/riscv32.md#sync_file), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via msync

### read

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.read`](linux/x86_64.md#read), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.read`](linux/aarch64.md#read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.read`](linux/riscv64.md#read), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.read`](linux/riscv32.md#read), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

filesystem

### write

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.write`](linux/x86_64.md#write), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.write`](linux/aarch64.md#write), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.write`](linux/riscv64.md#write), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.write`](linux/riscv32.md#write), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a file descriptor

retries automatically on EINTR.

### write_vector

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.write_vector`](linux/x86_64.md#write_vector), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.write_vector`](linux/aarch64.md#write_vector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.write_vector`](linux/riscv64.md#write_vector), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.write_vector`](linux/riscv32.md#write_vector), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun write_vector(fd: i32, vectors: *IoVector, count: usize) i64
```

write several buffers to a file descriptor in order, in one call

retries automatically on EINTR.

### read_at

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.read_at`](linux/x86_64.md#read_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.read_at`](linux/aarch64.md#read_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.read_at`](linux/riscv64.md#read_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.read_at`](linux/riscv32.md#read_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

positioned file access does not mutate the descriptor offset

### write_at

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.write_at`](linux/x86_64.md#write_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.write_at`](linux/aarch64.md#write_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.write_at`](linux/riscv64.md#write_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.write_at`](linux/riscv32.md#write_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

write bytes at a file offset without moving the descriptor offset

retries automatically on EINTR.

### open

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.open`](linux/x86_64.md#open), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.open`](linux/aarch64.md#open), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.open`](linux/riscv64.md#open), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.open`](linux/riscv32.md#open), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

openat: open a file relative to a directory file descriptor

retries automatically on EINTR.

### open_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.open`](linux/x86_64.md#open), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.open`](linux/aarch64.md#open), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.open`](linux/riscv64.md#open), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.open`](linux/riscv32.md#open), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

the kernel takes a name as bytes, so the native-unit open is open itself

### close

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.close`](linux/x86_64.md#close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.close`](linux/aarch64.md#close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.close`](linux/riscv64.md#close), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.close`](linux/riscv32.md#close), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun close(fd: i32) i64
```

close a file descriptor

### sync_fd

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sync_fd`](linux/x86_64.md#sync_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sync_fd`](linux/aarch64.md#sync_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sync_fd`](linux/riscv64.md#sync_fd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sync_fd`](linux/riscv32.md#sync_fd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sync_fd(fd: i32) i64
```

flush an open file's data and metadata to its backing storage

### stat

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat`](linux/x86_64.md#stat), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat`](linux/aarch64.md#stat), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat`](linux/riscv64.md#stat), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat`](linux/riscv32.md#stat), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

get file status by file descriptor

### set_mode

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.set_mode`](linux/x86_64.md#set_mode), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.set_mode`](linux/aarch64.md#set_mode), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.set_mode`](linux/riscv64.md#set_mode), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.set_mode`](linux/riscv32.md#set_mode), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

set permission bits through a held descriptor

### set_mode_at

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.set_mode_at`](linux/x86_64.md#set_mode_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.set_mode_at`](linux/aarch64.md#set_mode_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.set_mode_at`](linux/riscv64.md#set_mode_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.set_mode_at`](linux/riscv32.md#set_mode_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

no following fallback is permitted when the flags-aware syscall is unavailable

### set_mode_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.set_mode_at`](linux/x86_64.md#set_mode_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.set_mode_at`](linux/aarch64.md#set_mode_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.set_mode_at`](linux/riscv64.md#set_mode_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.set_mode_at`](linux/riscv32.md#set_mode_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

every name below reaches the kernel as bytes, so each native form is the
UTF-8 primitive itself

### file_identity

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.file_identity`](linux/x86_64.md#file_identity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.file_identity`](linux/aarch64.md#file_identity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.file_identity`](linux/riscv64.md#file_identity), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.file_identity`](linux/riscv32.md#file_identity), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

observational ids do not retain an object after this call

### identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.identity_at`](linux/x86_64.md#identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.identity_at`](linux/aarch64.md#identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.identity_at`](linux/riscv64.md#identity_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.identity_at`](linux/riscv32.md#identity_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the entry path names, without following a final symlink

### identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.identity_at`](linux/x86_64.md#identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.identity_at`](linux/aarch64.md#identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.identity_at`](linux/riscv64.md#identity_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.identity_at`](linux/riscv32.md#identity_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the entry path names, without following a final symlink

### retain_identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.retain_identity_at`](linux/x86_64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.retain_identity_at`](linux/aarch64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.retain_identity_at`](linux/riscv64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.retain_identity_at`](linux/riscv32.md#retain_identity_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_path pins the entry without acquiring content-read permission

### retain_identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.retain_identity_at`](linux/x86_64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.retain_identity_at`](linux/aarch64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.retain_identity_at`](linux/riscv64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.retain_identity_at`](linux/riscv32.md#retain_identity_at), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_path pins the entry without acquiring content-read permission

### publication_capabilities

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.publication_capabilities`](linux/x86_64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.publication_capabilities`](linux/aarch64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.publication_capabilities`](linux/riscv64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.publication_capabilities`](linux/riscv32.md#publication_capabilities), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun publication_capabilities(fd: i32) i64
```

the cooperative publication capabilities of the filesystem fd lives on

ext4, tmpfs, xfs and btrfs report every capability, and any other
filesystem reports none

### stat_path

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat_path`](linux/x86_64.md#stat_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat_path`](linux/aarch64.md#stat_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat_path`](linux/riscv64.md#stat_path), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat_path`](linux/riscv32.md#stat_path), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

get file status relative to a directory fd

### stat_path_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat_path`](linux/x86_64.md#stat_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat_path`](linux/aarch64.md#stat_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat_path`](linux/riscv64.md#stat_path), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat_path`](linux/riscv32.md#stat_path), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

get file status relative to a directory fd

### stat_mode

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat_mode`](linux/x86_64.md#stat_mode), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat_mode`](linux/aarch64.md#stat_mode), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat_mode`](linux/riscv64.md#stat_mode), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat_mode`](linux/riscv32.md#stat_mode), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 32-bit in the linux stat ABI; the accessor exists so portable
callers read the mode uniformly across platforms (darwin's mode is 16-bit).

### stat_birth

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stat_birth`](linux/x86_64.md#stat_birth), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stat_birth`](linux/aarch64.md#stat_birth), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stat_birth`](linux/riscv64.md#stat_birth), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stat_birth`](linux/riscv32.md#stat_birth), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stat_birth(st: *stat_t, sec: *i64, nsec: *i64) bool
```

the birth time of a stat record, when the filesystem recorded one

### unlink

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.unlink`](linux/x86_64.md#unlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.unlink`](linux/aarch64.md#unlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.unlink`](linux/riscv64.md#unlink), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.unlink`](linux/riscv32.md#unlink), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

unlinkat: remove a file or directory relative to a directory fd

### unlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.unlink`](linux/x86_64.md#unlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.unlink`](linux/aarch64.md#unlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.unlink`](linux/riscv64.md#unlink), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.unlink`](linux/riscv32.md#unlink), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

unlinkat: remove a file or directory relative to a directory fd

### rename

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.rename`](linux/x86_64.md#rename), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.rename`](linux/aarch64.md#rename), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.rename`](linux/riscv64.md#rename), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.rename`](linux/riscv32.md#rename), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

renameat: rename a file relative to directory fds

### rename_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.rename`](linux/x86_64.md#rename), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.rename`](linux/aarch64.md#rename), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.rename`](linux/riscv64.md#rename), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.rename`](linux/riscv32.md#rename), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

renameat: rename a file relative to directory fds

### symlink

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.symlink`](linux/x86_64.md#symlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.symlink`](linux/aarch64.md#symlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.symlink`](linux/riscv64.md#symlink), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.symlink`](linux/riscv32.md#symlink), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### symlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.symlink`](linux/x86_64.md#symlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.symlink`](linux/aarch64.md#symlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.symlink`](linux/riscv64.md#symlink), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.symlink`](linux/riscv32.md#symlink), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### make_dir

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.make_dir`](linux/x86_64.md#make_dir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.make_dir`](linux/aarch64.md#make_dir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.make_dir`](linux/riscv64.md#make_dir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.make_dir`](linux/riscv32.md#make_dir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

mkdirat: create a directory relative to a directory fd

### make_dir_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.make_dir`](linux/x86_64.md#make_dir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.make_dir`](linux/aarch64.md#make_dir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.make_dir`](linux/riscv64.md#make_dir), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.make_dir`](linux/riscv32.md#make_dir), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

mkdirat: create a directory relative to a directory fd

### directory_init

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.directory_init`](linux/x86_64.md#directory_init), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.directory_init`](linux/aarch64.md#directory_init), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.directory_init`](linux/riscv64.md#directory_init), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.directory_init`](linux/riscv32.md#directory_init), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.directory_next`](linux/x86_64.md#directory_next), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.directory_next`](linux/aarch64.md#directory_next), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.directory_next`](linux/riscv64.md#directory_next), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.directory_next`](linux/riscv32.md#directory_next), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

read the next entry of a directory

the entry's name is borrowed from the cursor's buffer until the next cursor
operation. a malformed record fails with EIO, and a failure is kept, so every
later call returns it again

### directory_dnit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.directory_dnit`](linux/x86_64.md#directory_dnit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.directory_dnit`](linux/aarch64.md#directory_dnit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.directory_dnit`](linux/riscv64.md#directory_dnit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.directory_dnit`](linux/riscv32.md#directory_dnit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

consumes the owner, including when native release reports failure

### access

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.access`](linux/x86_64.md#access), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.access`](linux/aarch64.md#access), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.access`](linux/riscv64.md#access), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.access`](linux/riscv32.md#access), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

faccessat: check file accessibility relative to a directory fd

### access_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.access`](linux/x86_64.md#access), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.access`](linux/aarch64.md#access), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.access`](linux/riscv64.md#access), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.access`](linux/riscv32.md#access), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

faccessat: check file accessibility relative to a directory fd

### seek

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.seek`](linux/x86_64.md#seek), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.seek`](linux/aarch64.md#seek), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.seek`](linux/riscv64.md#seek), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.seek`](linux/riscv32.md#seek), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

lseek: reposition read/write offset of a file descriptor

### lock_fd

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.lock_fd`](linux/x86_64.md#lock_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.lock_fd`](linux/aarch64.md#lock_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.lock_fd`](linux/riscv64.md#lock_fd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.lock_fd`](linux/riscv32.md#lock_fd), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.terminate`](linux/x86_64.md#terminate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.terminate`](linux/aarch64.md#terminate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.terminate`](linux/riscv64.md#terminate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.terminate`](linux/riscv32.md#terminate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
#[noreturn]
pub fun terminate(code: i64)
```

process

### abort

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.abort`](linux/x86_64.md#abort), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.abort`](linux/aarch64.md#abort), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.abort`](linux/riscv64.md#abort), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.abort`](linux/riscv32.md#abort), where `$mach.build.arch == $mach.arch.riscv32`

```mach
#[noreturn]
pub fun abort()
```

abort the process immediately with exit code 255

### terminate_child

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.terminate_child`](linux/x86_64.md#terminate_child), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.terminate_child`](linux/aarch64.md#terminate_child), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.terminate_child`](linux/riscv64.md#terminate_child), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.terminate_child`](linux/riscv32.md#terminate_child), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.setpgid`](linux/x86_64.md#setpgid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.setpgid`](linux/aarch64.md#setpgid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.setpgid`](linux/riscv64.md#setpgid), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.setpgid`](linux/riscv32.md#setpgid), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun setpgid(pid: i64, pgid: i64) i64
```

setpgid: set (or join) the process group ID of a process

### getpgid

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getpgid`](linux/x86_64.md#getpgid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getpgid`](linux/aarch64.md#getpgid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getpgid`](linux/riscv64.md#getpgid), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getpgid`](linux/riscv32.md#getpgid), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getpgid(pid: i64) i64
```

getpgid: read the process group ID of a process

### terminate_group

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.terminate_group`](linux/x86_64.md#terminate_group), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.terminate_group`](linux/aarch64.md#terminate_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.terminate_group`](linux/riscv64.md#terminate_group), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.terminate_group`](linux/riscv32.md#terminate_group), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun terminate_group(pgid: i64) i64
```

signal every process in a group without reaping any of them

unlike terminate_child, there is no waitid ownership probe first: a process
group is not tracked as a child of this process, so kill(-pgid, SIGTERM) is
the only available primitive. surviving members stay individually waitable
through wait/wait_any exactly as before.

### kill_group

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.kill_group`](linux/x86_64.md#kill_group), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.kill_group`](linux/aarch64.md#kill_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.kill_group`](linux/riscv64.md#kill_group), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.kill_group`](linux/riscv32.md#kill_group), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun kill_group(pgid: i64) i64
```

forcefully stop every process in a group without reaping any of them

the group's members get SIGKILL, which none of them can catch or ignore.
as with terminate_group there is no ownership probe, and members stay
individually waitable.

### probe_group

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.probe_group`](linux/x86_64.md#probe_group), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.probe_group`](linux/aarch64.md#probe_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.probe_group`](linux/riscv64.md#probe_group), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.probe_group`](linux/riscv32.md#probe_group), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun probe_group(pgid: i64) i64
```

whether any process is left in a group, without signalling it

kill(-pgid, 0) checks for members and delivers nothing. a member this
process may not signal still counts, so EPERM reads as present.

### process_watch

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.process_watch`](linux/x86_64.md#process_watch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.process_watch`](linux/aarch64.md#process_watch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.process_watch`](linux/riscv64.md#process_watch), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.process_watch`](linux/riscv32.md#process_watch), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun process_watch(queue: *std.system.os.shared.IoQueue, pid: i64, context: u64) i64
```

make the end of the child `pid` a readiness event on `queue`, so the queue's
wait returns once the child ends. a pidfd names the child: it reads ready
from the moment the child ends, reaped or not, and is not inherited across exec

### process_unwatch

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.process_unwatch`](linux/x86_64.md#process_unwatch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.process_unwatch`](linux/aarch64.md#process_unwatch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.process_unwatch`](linux/riscv64.md#process_unwatch), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.process_unwatch`](linux/riscv32.md#process_unwatch), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired

### spawn

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn`](linux/x86_64.md#spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn`](linux/aarch64.md#spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn`](linux/riscv64.md#spawn), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn`](linux/riscv32.md#spawn), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

### spawn_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_grouped`](linux/x86_64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_grouped`](linux/aarch64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_grouped`](linux/riscv64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_grouped`](linux/riscv32.md#spawn_grouped), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program, placed as the leader of
its own new process group (see spawn_redirected_in_grouped)

### spawn_in

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_in`](linux/x86_64.md#spawn_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_in`](linux/aarch64.md#spawn_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_in`](linux/riscv64.md#spawn_in), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_in`](linux/riscv32.md#spawn_in), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected`](linux/x86_64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected`](linux/aarch64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected`](linux/riscv64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected`](linux/riscv32.md#spawn_redirected), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected_grouped`](linux/x86_64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected_grouped`](linux/aarch64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected_grouped`](linux/riscv64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected_grouped`](linux/riscv32.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed as the leader of its own new process group (see
spawn_redirected_in_grouped)

### spawn_redirected_in

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected_in`](linux/x86_64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected_in`](linux/aarch64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected_in`](linux/riscv64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected_in`](linux/riscv32.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected_in_grouped`](linux/x86_64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected_in_grouped`](linux/aarch64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected_in_grouped`](linux/riscv64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected_in_grouped`](linux/riscv32.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

identical to spawn_redirected_in except the child calls setpgid(0, 0)
between the clone and the exec (see spawn_main), and the parent ALSO
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

### spawn_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn`](linux/x86_64.md#spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn`](linux/aarch64.md#spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn`](linux/riscv64.md#spawn), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn`](linux/riscv32.md#spawn), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

the kernel takes paths and arguments as bytes, so the native-unit spawns are the spawns themselves

### spawn_in_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_in`](linux/x86_64.md#spawn_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_in`](linux/aarch64.md#spawn_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_in`](linux/riscv64.md#spawn_in), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_in`](linux/riscv32.md#spawn_in), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected`](linux/x86_64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected`](linux/aarch64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected`](linux/riscv64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected`](linux/riscv32.md#spawn_redirected), where `$mach.build.arch == $mach.arch.riscv32`

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

### spawn_redirected_in_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected_in`](linux/x86_64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected_in`](linux/aarch64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected_in`](linux/riscv64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected_in`](linux/riscv32.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.riscv32`

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

### spawn_redirected_in_grouped_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.spawn_redirected_in_grouped`](linux/x86_64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.spawn_redirected_in_grouped`](linux/aarch64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.spawn_redirected_in_grouped`](linux/riscv64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.spawn_redirected_in_grouped`](linux/riscv32.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

identical to spawn_redirected_in except the child calls setpgid(0, 0)
between the clone and the exec (see spawn_main), and the parent ALSO
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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getpid`](linux/x86_64.md#getpid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getpid`](linux/aarch64.md#getpid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getpid`](linux/riscv64.md#getpid), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getpid`](linux/riscv32.md#getpid), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getpid() i64
```

return the current process ID

### running_under_user_emulation

Forwards [`std.system.os.linux.shared.running_under_user_emulation`](linux/shared.md#running_under_user_emulation).

```mach
pub fun running_under_user_emulation() bool
```

detect a user-mode emulator such as qemu-user

the kernel names a process after the image it executed (/proc/self/comm, at most
fifteen bytes), while an emulator presents the guest's own command line through
/proc/self/cmdline. natively the two name the same executable; under emulation the
comm names the emulator. tests use this to decline what an emulator's syscall
translation cannot reproduce, as running_under_wine does on windows.

### pipe

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.pipe`](linux/x86_64.md#pipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.pipe`](linux/aarch64.md#pipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.pipe`](linux/riscv64.md#pipe), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.pipe`](linux/riscv32.md#pipe), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

### ignore_sigpipe

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ignore_sigpipe`](linux/x86_64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ignore_sigpipe`](linux/aarch64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ignore_sigpipe`](linux/riscv64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ignore_sigpipe`](linux/riscv32.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sleep`](linux/x86_64.md#sleep), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sleep`](linux/aarch64.md#sleep), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sleep`](linux/riscv64.md#sleep), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sleep`](linux/riscv32.md#sleep), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

### cpu_count

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.cpu_count`](linux/x86_64.md#cpu_count), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.cpu_count`](linux/aarch64.md#cpu_count), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.cpu_count`](linux/riscv64.md#cpu_count), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.cpu_count`](linux/riscv32.md#cpu_count), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun cpu_count() i64
```

the number of CPUs available to this process

popcounts the sched_getaffinity mask, so taskset/cgroup cpuset restrictions
are honoured; the kernel reports the mask size it wrote in the return value.
never returns less than 1.

### cpu_features

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.cpu_features`](linux/x86_64.md#cpu_features), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.cpu_features`](linux/aarch64.md#cpu_features), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.cpu_features`](linux/riscv64.md#cpu_features), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.cpu_features`](linux/riscv32.md#cpu_features), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.cpu_dit`](linux/x86_64.md#cpu_dit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.cpu_dit`](linux/aarch64.md#cpu_dit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.cpu_dit`](linux/riscv64.md#cpu_dit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.cpu_dit`](linux/riscv32.md#cpu_dit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun cpu_dit() i64
```

whether the processor and kernel provide the data-independent-timing mode

aarch64 reads HWCAP_DIT (bit 24) from AT_HWCAP through the same auxv reader
`cpu_features` uses; the kernel sets it when ID_AA64PFR0_EL1.DIT is 1. a
caller that runs before the runtime captured envp sees ENOSYS. no other
architecture has the mode

### thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_affinity`](linux/x86_64.md#thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_affinity`](linux/aarch64.md#thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_affinity`](linux/riscv64.md#thread_affinity), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_affinity`](linux/riscv32.md#thread_affinity), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

read the calling thread's CPU affinity

CPU i is bit i % 64 of words[i / 64]. the kernel reports the bytes it wrote,
which is its own cpumask size, so out_count is that size in words and every
word the kernel wrote is copied, including trailing zero words.

### set_thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.set_thread_affinity`](linux/x86_64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.set_thread_affinity`](linux/aarch64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.set_thread_affinity`](linux/riscv64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.set_thread_affinity`](linux/riscv32.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

pin the calling thread to the CPUs set in words

### getcwd

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getcwd`](linux/x86_64.md#getcwd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getcwd`](linux/aarch64.md#getcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getcwd`](linux/riscv64.md#getcwd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getcwd`](linux/riscv32.md#getcwd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

the raw syscall returns the length INCLUDING the terminator; this layer
reports the path length the way darwin and windows do, so "length of path"
means one thing across the three backends (#432).

### getcwd_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getcwd`](linux/x86_64.md#getcwd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getcwd`](linux/aarch64.md#getcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getcwd`](linux/riscv64.md#getcwd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getcwd`](linux/riscv32.md#getcwd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

the raw syscall returns the length INCLUDING the terminator; this layer
reports the path length the way darwin and windows do, so "length of path"
means one thing across the three backends (#432).

### getenv

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getenv`](linux/x86_64.md#getenv), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getenv`](linux/aarch64.md#getenv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getenv`](linux/riscv64.md#getenv), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getenv`](linux/riscv32.md#getenv), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

### environ

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.environ`](linux/x86_64.md#environ), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.environ`](linux/aarch64.md#environ), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.environ`](linux/riscv64.md#environ), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.environ`](linux/riscv32.md#environ), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### getenv_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.getenv`](linux/x86_64.md#getenv), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.getenv`](linux/aarch64.md#getenv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.getenv`](linux/riscv64.md#getenv), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.getenv`](linux/riscv32.md#getenv), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

the environment is the bytes the kernel passed, so its native reads are the reads themselves

### environ_native

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.environ`](linux/x86_64.md#environ), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.environ`](linux/aarch64.md#environ), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.environ`](linux/riscv64.md#environ), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.environ`](linux/riscv32.md#environ), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### temp_dir

Forwards [`std.system.os.linux.shared.temp_dir`](linux/shared.md#temp_dir).

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

the directory designated for temporary files: $TMPDIR, else "/tmp"

### fork

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.fork`](linux/x86_64.md#fork), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.fork`](linux/aarch64.md#fork), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.fork`](linux/riscv64.md#fork), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.fork`](linux/riscv32.md#fork), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun fork() i64
```

create a new child process

### vfork

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.vfork`](linux/x86_64.md#vfork), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.vfork`](linux/aarch64.md#vfork), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.vfork`](linux/riscv64.md#vfork), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.vfork`](linux/riscv32.md#vfork), where `$mach.build.arch == $mach.arch.riscv32`

```mach
#[naked]
pub fun vfork() i64
```

create child process sharing memory with parent. the child runs on the
parent's stack until it execs or exits, so this stub keeps no frame and holds
its return address in a register across the syscall

### exec

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.exec`](linux/x86_64.md#exec), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.exec`](linux/aarch64.md#exec), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.exec`](linux/riscv64.md#exec), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.exec`](linux/riscv32.md#exec), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun exec(pathname: *u8, argv: **u8, envp: Environment) i64
```

execve: replace the current process image with a new program

### wait

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.wait`](linux/x86_64.md#wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.wait`](linux/aarch64.md#wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.wait`](linux/riscv64.md#wait), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.wait`](linux/riscv32.md#wait), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

failures and no-event results leave the caller's status unchanged

### wait_pid

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.wait_pid`](linux/x86_64.md#wait_pid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.wait_pid`](linux/aarch64.md#wait_pid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.wait_pid`](linux/riscv64.md#wait_pid), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.wait_pid`](linux/riscv32.md#wait_pid), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

wait for a child state, as wait does with no resource usage

### ProcessStatus

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ProcessStatus`](linux/x86_64.md#processstatus), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ProcessStatus`](linux/aarch64.md#processstatus), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ProcessStatus`](linux/riscv64.md#processstatus), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ProcessStatus`](linux/riscv32.md#processstatus), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

one observed change in a child's state

### FileLimit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.FileLimit`](linux/x86_64.md#filelimit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.FileLimit`](linux/aarch64.md#filelimit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.FileLimit`](linux/riscv64.md#filelimit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.FileLimit`](linux/riscv32.md#filelimit), where `$mach.build.arch == $mach.arch.riscv32`

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

### MemoryLimit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.MemoryLimit`](linux/x86_64.md#memorylimit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.MemoryLimit`](linux/aarch64.md#memorylimit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.MemoryLimit`](linux/riscv64.md#memorylimit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.MemoryLimit`](linux/riscv32.md#memorylimit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec MemoryLimit {
    soft: u64;
    hard: u64;
}
```

the locked-memory limit in bytes. soft is the limit in force and hard its
ceiling for an unprivileged raise

### LIMIT_UNLIMITED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.LIMIT_UNLIMITED`](linux/x86_64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.LIMIT_UNLIMITED`](linux/aarch64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.LIMIT_UNLIMITED`](linux/riscv64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.LIMIT_UNLIMITED`](linux/riscv32.md#limit_unlimited), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.open_file_limit`](linux/x86_64.md#open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.open_file_limit`](linux/aarch64.md#open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.open_file_limit`](linux/riscv64.md#open_file_limit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.open_file_limit`](linux/riscv32.md#open_file_limit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

read this process's open-file limit. linux's RLIM_INFINITY is all ones, the
same value as LIMIT_UNLIMITED, and an unprivileged process may raise its soft
limit up to the hard one

### set_open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.set_open_file_limit`](linux/x86_64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.set_open_file_limit`](linux/aarch64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.set_open_file_limit`](linux/riscv64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.set_open_file_limit`](linux/riscv32.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

set this process's open-file limit. ceiling is ignored

### locked_memory_limit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.locked_memory_limit`](linux/x86_64.md#locked_memory_limit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.locked_memory_limit`](linux/aarch64.md#locked_memory_limit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.locked_memory_limit`](linux/riscv64.md#locked_memory_limit), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.locked_memory_limit`](linux/riscv32.md#locked_memory_limit), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun locked_memory_limit(out: *std.system.os.shared.MemoryLimit) i64
```

read this process's locked-memory limit in bytes

### ProcessWaitError

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.ProcessWaitError`](linux/x86_64.md#processwaiterror), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.ProcessWaitError`](linux/aarch64.md#processwaiterror), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.ProcessWaitError`](linux/riscv64.md#processwaiterror), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.ProcessWaitError`](linux/riscv32.md#processwaiterror), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

why a process wait or the release of a child's handle failed

### WaitResult

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.WaitResult`](linux/x86_64.md#waitresult), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.WaitResult`](linux/aarch64.md#waitresult), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.WaitResult`](linux/riscv64.md#waitresult), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.WaitResult`](linux/riscv32.md#waitresult), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_WAIT`](linux/x86_64.md#process_op_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_WAIT`](linux/aarch64.md#process_op_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_WAIT`](linux/riscv64.md#process_op_wait), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_WAIT`](linux/riscv32.md#process_op_wait), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_STATUS`](linux/x86_64.md#process_op_status), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_STATUS`](linux/aarch64.md#process_op_status), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_STATUS`](linux/riscv64.md#process_op_status), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_STATUS`](linux/riscv32.md#process_op_status), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_CLOSE`](linux/x86_64.md#process_op_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_CLOSE`](linux/aarch64.md#process_op_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_CLOSE`](linux/riscv64.md#process_op_close), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_CLOSE`](linux/riscv32.md#process_op_close), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_SPAWN`](linux/x86_64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_SPAWN`](linux/aarch64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_SPAWN`](linux/riscv64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_SPAWN`](linux/riscv32.md#process_op_spawn), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_READ`](linux/x86_64.md#process_op_read), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_READ`](linux/aarch64.md#process_op_read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_READ`](linux/riscv64.md#process_op_read), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_READ`](linux/riscv32.md#process_op_read), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_PIPE`](linux/x86_64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_PIPE`](linux/aarch64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_PIPE`](linux/riscv64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_PIPE`](linux/riscv32.md#process_op_pipe), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_OP_TERMINATE`](linux/x86_64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_OP_TERMINATE`](linux/aarch64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_OP_TERMINATE`](linux/riscv64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_OP_TERMINATE`](linux/riscv32.md#process_op_terminate), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_EXITED`](linux/x86_64.md#process_exited), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_EXITED`](linux/aarch64.md#process_exited), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_EXITED`](linux/riscv64.md#process_exited), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_EXITED`](linux/riscv32.md#process_exited), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_SIGNALED`](linux/x86_64.md#process_signaled), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_SIGNALED`](linux/aarch64.md#process_signaled), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_SIGNALED`](linux/riscv64.md#process_signaled), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_SIGNALED`](linux/riscv32.md#process_signaled), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_STOPPED`](linux/x86_64.md#process_stopped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_STOPPED`](linux/aarch64.md#process_stopped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_STOPPED`](linux/riscv64.md#process_stopped), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_STOPPED`](linux/riscv32.md#process_stopped), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.PROCESS_CONTINUED`](linux/x86_64.md#process_continued), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.PROCESS_CONTINUED`](linux/aarch64.md#process_continued), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.PROCESS_CONTINUED`](linux/riscv64.md#process_continued), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.PROCESS_CONTINUED`](linux/riscv32.md#process_continued), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### AF_INET

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.AF_INET`](linux/x86_64.md#af_inet), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.AF_INET`](linux/aarch64.md#af_inet), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.AF_INET`](linux/riscv64.md#af_inet), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.AF_INET`](linux/riscv32.md#af_inet), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val AF_INET:             i32 = 2
```

sockets

### AF_INET6

Forwards [`std.system.os.linux.shared.AF_INET6`](linux/shared.md#constants).

```mach
pub val AF_INET6:            i32 = 10
```

### SOCK_STREAM

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOCK_STREAM`](linux/x86_64.md#sock_stream), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOCK_STREAM`](linux/aarch64.md#sock_stream), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOCK_STREAM`](linux/riscv64.md#sock_stream), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOCK_STREAM`](linux/riscv32.md#sock_stream), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOCK_STREAM:         i32 = 1
```

### SOCK_DGRAM

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOCK_DGRAM`](linux/x86_64.md#sock_dgram), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOCK_DGRAM`](linux/aarch64.md#sock_dgram), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOCK_DGRAM`](linux/riscv64.md#sock_dgram), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOCK_DGRAM`](linux/riscv32.md#sock_dgram), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOCK_DGRAM:          i32 = 2
```

### SOCK_NONBLOCK

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOCK_NONBLOCK`](linux/x86_64.md#sock_nonblock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOCK_NONBLOCK`](linux/aarch64.md#sock_nonblock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOCK_NONBLOCK`](linux/riscv64.md#sock_nonblock), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOCK_NONBLOCK`](linux/riscv32.md#sock_nonblock), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOCK_NONBLOCK:       i32 = O_NONBLOCK
```

### SOCK_CLOEXEC

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOCK_CLOEXEC`](linux/x86_64.md#sock_cloexec), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOCK_CLOEXEC`](linux/aarch64.md#sock_cloexec), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOCK_CLOEXEC`](linux/riscv64.md#sock_cloexec), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOCK_CLOEXEC`](linux/riscv32.md#sock_cloexec), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOCK_CLOEXEC:        i32 = 0x80000
```

### SOL_SOCKET

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOL_SOCKET`](linux/x86_64.md#sol_socket), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOL_SOCKET`](linux/aarch64.md#sol_socket), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOL_SOCKET`](linux/riscv64.md#sol_socket), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOL_SOCKET`](linux/riscv32.md#sol_socket), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOL_SOCKET:          i32 = 1
```

### SO_UNSUPPORTED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_UNSUPPORTED`](linux/x86_64.md#so_unsupported), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_UNSUPPORTED`](linux/aarch64.md#so_unsupported), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_UNSUPPORTED`](linux/riscv64.md#so_unsupported), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_UNSUPPORTED`](linux/riscv32.md#so_unsupported), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

### SO_REUSEADDR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_REUSEADDR`](linux/x86_64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_REUSEADDR`](linux/aarch64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_REUSEADDR`](linux/riscv64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_REUSEADDR`](linux/riscv32.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_REUSEADDR:        i32 = 2
```

### SO_REUSEPORT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_REUSEPORT`](linux/x86_64.md#so_reuseport), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_REUSEPORT`](linux/aarch64.md#so_reuseport), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_REUSEPORT`](linux/riscv64.md#so_reuseport), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_REUSEPORT`](linux/riscv32.md#so_reuseport), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_REUSEPORT:        i32 = 15
```

### SO_EXCLUSIVEADDRUSE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_EXCLUSIVEADDRUSE`](linux/x86_64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_EXCLUSIVEADDRUSE`](linux/aarch64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_EXCLUSIVEADDRUSE`](linux/riscv64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_EXCLUSIVEADDRUSE`](linux/riscv32.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = SO_UNSUPPORTED
```

### SO_KEEPALIVE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_KEEPALIVE`](linux/x86_64.md#so_keepalive), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_KEEPALIVE`](linux/aarch64.md#so_keepalive), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_KEEPALIVE`](linux/riscv64.md#so_keepalive), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_KEEPALIVE`](linux/riscv32.md#so_keepalive), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_KEEPALIVE:        i32 = 9
```

### SO_SNDBUF

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_SNDBUF`](linux/x86_64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_SNDBUF`](linux/aarch64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_SNDBUF`](linux/riscv64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_SNDBUF`](linux/riscv32.md#so_sndbuf), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_SNDBUF:           i32 = 7
```

### SO_RCVBUF

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_RCVBUF`](linux/x86_64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_RCVBUF`](linux/aarch64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_RCVBUF`](linux/riscv64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_RCVBUF`](linux/riscv32.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_RCVBUF:           i32 = 8
```

### SO_LINGER

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_LINGER`](linux/x86_64.md#so_linger), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_LINGER`](linux/aarch64.md#so_linger), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_LINGER`](linux/riscv64.md#so_linger), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_LINGER`](linux/riscv32.md#so_linger), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SO_LINGER:           i32 = 13
```

### SO_RCVTIMEO

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SO_RCVTIMEO`](linux/x86_64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SO_RCVTIMEO`](linux/aarch64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SO_RCVTIMEO`](linux/riscv64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SO_RCVTIMEO`](linux/riscv32.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.riscv32`

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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IPPROTO_IP`](linux/x86_64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IPPROTO_IP`](linux/aarch64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IPPROTO_IP`](linux/riscv64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IPPROTO_IP`](linux/riscv32.md#ipproto_ip), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IPPROTO_IP:    i32 = 0
```

### IPPROTO_TCP

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IPPROTO_TCP`](linux/x86_64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IPPROTO_TCP`](linux/aarch64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IPPROTO_TCP`](linux/riscv64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IPPROTO_TCP`](linux/riscv32.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IPPROTO_TCP:   i32 = 6
```

### IPPROTO_IPV6

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IPPROTO_IPV6`](linux/x86_64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IPPROTO_IPV6`](linux/aarch64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IPPROTO_IPV6`](linux/riscv64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IPPROTO_IPV6`](linux/riscv32.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IPPROTO_IPV6:  i32 = 41
```

### IP_TOS

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IP_TOS`](linux/x86_64.md#ip_tos), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IP_TOS`](linux/aarch64.md#ip_tos), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IP_TOS`](linux/riscv64.md#ip_tos), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IP_TOS`](linux/riscv32.md#ip_tos), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IP_TOS:        i32 = 1
```

### IPV6_V6ONLY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IPV6_V6ONLY`](linux/x86_64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IPV6_V6ONLY`](linux/aarch64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IPV6_V6ONLY`](linux/riscv64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IPV6_V6ONLY`](linux/riscv32.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IPV6_V6ONLY:   i32 = 26
```

### IPV6_TCLASS

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IPV6_TCLASS`](linux/x86_64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IPV6_TCLASS`](linux/aarch64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IPV6_TCLASS`](linux/riscv64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IPV6_TCLASS`](linux/riscv32.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IPV6_TCLASS:   i32 = 67
```

### TCP_NODELAY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.TCP_NODELAY`](linux/x86_64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.TCP_NODELAY`](linux/aarch64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.TCP_NODELAY`](linux/riscv64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.TCP_NODELAY`](linux/riscv32.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val TCP_NODELAY:   i32 = 1
```

### TCP_KEEPIDLE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.TCP_KEEPIDLE`](linux/x86_64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.TCP_KEEPIDLE`](linux/aarch64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.TCP_KEEPIDLE`](linux/riscv64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.TCP_KEEPIDLE`](linux/riscv32.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val TCP_KEEPIDLE:  i32 = 4
```

### TCP_KEEPINTVL

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.TCP_KEEPINTVL`](linux/x86_64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.TCP_KEEPINTVL`](linux/aarch64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.TCP_KEEPINTVL`](linux/riscv64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.TCP_KEEPINTVL`](linux/riscv32.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val TCP_KEEPINTVL: i32 = 5
```

### TCP_KEEPCNT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.TCP_KEEPCNT`](linux/x86_64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.TCP_KEEPCNT`](linux/aarch64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.TCP_KEEPCNT`](linux/riscv64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.TCP_KEEPCNT`](linux/riscv32.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val TCP_KEEPCNT:   i32 = 6
```

### TCP_FASTOPEN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.TCP_FASTOPEN`](linux/x86_64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.TCP_FASTOPEN`](linux/aarch64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.TCP_FASTOPEN`](linux/riscv64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.TCP_FASTOPEN`](linux/riscv32.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val TCP_FASTOPEN:  i32 = 23
```

### SHUT_RD

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SHUT_RD`](linux/x86_64.md#shut_rd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SHUT_RD`](linux/aarch64.md#shut_rd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SHUT_RD`](linux/riscv64.md#shut_rd), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SHUT_RD`](linux/riscv32.md#shut_rd), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SHUT_RD:       i32 = 0
```

### SHUT_WR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SHUT_WR`](linux/x86_64.md#shut_wr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SHUT_WR`](linux/aarch64.md#shut_wr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SHUT_WR`](linux/riscv64.md#shut_wr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SHUT_WR`](linux/riscv32.md#shut_wr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SHUT_WR:       i32 = 1
```

### SHUT_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SHUT_RDWR`](linux/x86_64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SHUT_RDWR`](linux/aarch64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SHUT_RDWR`](linux/riscv64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SHUT_RDWR`](linux/riscv32.md#shut_rdwr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SHUT_RDWR:     i32 = 2
```

### SOCKADDR_IN_SIZE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.SOCKADDR_IN_SIZE`](linux/x86_64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.SOCKADDR_IN_SIZE`](linux/aarch64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.SOCKADDR_IN_SIZE`](linux/riscv64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.SOCKADDR_IN_SIZE`](linux/riscv32.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

### SOCKADDR_IN6_SIZE

Forwards [`std.system.os.linux.shared.SOCKADDR_IN6_SIZE`](linux/shared.md#constants).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

### SOCKADDR_STORAGE_SIZE

Forwards [`std.system.os.linux.shared.SOCKADDR_STORAGE_SIZE`](linux/shared.md#constants).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

### sock_send

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_send`](linux/x86_64.md#sock_send), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_send`](linux/aarch64.md#sock_send), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_send`](linux/riscv64.md#sock_send), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_send`](linux/riscv32.md#sock_send), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

send data on a connected socket

### sock_recv

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_recv`](linux/x86_64.md#sock_recv), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_recv`](linux/aarch64.md#sock_recv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_recv`](linux/riscv64.md#sock_recv), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_recv`](linux/riscv32.md#sock_recv), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

receive data from a connected socket

### IoVector

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IoVector`](linux/x86_64.md#iovector), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IoVector`](linux/aarch64.md#iovector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IoVector`](linux/riscv64.md#iovector), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IoVector`](linux/riscv32.md#iovector), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec IoVector {
    data:   *u8;
    length: usize;
}
```

one buffer of a gather write, laid out as struct iovec on linux and darwin
and as wasi's ciovec

### sock_write_vector

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_write_vector`](linux/x86_64.md#sock_write_vector), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_write_vector`](linux/aarch64.md#sock_write_vector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_write_vector`](linux/riscv64.md#sock_write_vector), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_write_vector`](linux/riscv32.md#sock_write_vector), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_write_vector(fd: usize, vectors: *IoVector, count: usize) i64
```

write several buffers to a socket in one call

### sock_send_message

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_send_message`](linux/x86_64.md#sock_send_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_send_message`](linux/aarch64.md#sock_send_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_send_message`](linux/riscv64.md#sock_send_message), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_send_message`](linux/riscv32.md#sock_send_message), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_send_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: u32, control: *u8, control_length: usize) i64
```

send buffers with an optional address and control records, without SIGPIPE

### sock_receive_message

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_receive_message`](linux/x86_64.md#sock_receive_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_receive_message`](linux/aarch64.md#sock_receive_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_receive_message`](linux/riscv64.md#sock_receive_message), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_receive_message`](linux/riscv32.md#sock_receive_message), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_receive_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: *u32, control: *u8, control_length: *usize, flags: *i32) i64
```

receive into buffers along with the sender's address and control records

### MSG_CTRUNC

Forwards [`std.system.os.linux.shared.MSG_CTRUNC`](linux/shared.md#constants).

```mach
pub val MSG_CTRUNC:       i32 = 0x8
```

### MSG_CMSG_CLOEXEC

Forwards [`std.system.os.linux.shared.MSG_CMSG_CLOEXEC`](linux/shared.md#constants).

```mach
pub val MSG_CMSG_CLOEXEC: i32 = 0x40000000
```

### SCM_RIGHTS

Forwards [`std.system.os.linux.shared.SCM_RIGHTS`](linux/shared.md#constants).

```mach
pub val SCM_RIGHTS:       i32 = 1
```

### SCM_CREDENTIALS

Forwards [`std.system.os.linux.shared.SCM_CREDENTIALS`](linux/shared.md#constants).

```mach
pub val SCM_CREDENTIALS:  i32 = 2
```

### SCM_PIDFD

Forwards [`std.system.os.linux.shared.SCM_PIDFD`](linux/shared.md#constants).

```mach
pub val SCM_PIDFD:        i32 = 4
```

### SCM_MAX_FD

Forwards [`std.system.os.linux.shared.SCM_MAX_FD`](linux/shared.md#constants).

```mach
pub val SCM_MAX_FD: usize = 253
```

net/scm.h SCM_MAX_FD: sendmsg refuses a larger descriptor set, and a stream receive
returns at most one set (unix_stream_read_generic stops after the record that carries it)

### LOCAL_CONTROL_CAPACITY

Forwards [`std.system.os.linux.shared.LOCAL_CONTROL_CAPACITY`](linux/shared.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.pointer_width == 8`:

```mach
pub val LOCAL_CONTROL_CAPACITY: usize = 1088
```

Otherwise:

```mach
pub val LOCAL_CONTROL_CAPACITY: usize = 1064
```

CMSG_SPACE(253 descriptors) + CMSG_SPACE(ucred) + CMSG_SPACE(pidfd): the largest descriptor
set together with the fixed-size records SO_PASSCRED and SO_PASSPIDFD prepend to it

### sock_recv_close_rights

Forwards [`std.system.os.linux.shared.sock_recv_close_rights`](linux/shared.md#sock_recv_close_rights).

```mach
pub fun sock_recv_close_rights(fd: usize, buffer: *u8, length: usize, address: *u8, address_length: *u32, control: *u8, capacity: usize) i64
```

receives bytes and closes every descriptor the kernel installed for them. installation is
close-on-exec, the kernel installs no descriptor it does not report (scm_detach_fds writes
the slot before fd_install and drops what does not fit under MSG_CTRUNC), and close always
releases a descriptor on linux, so the byte count is the outcome and the walk is complete.
address, when given, receives the sender and address_length its extent.

### local_stream_recv

Forwards [`std.system.os.linux.shared.local_stream_recv`](linux/shared.md#local_stream_recv).

```mach
pub fun local_stream_recv(fd: usize, buffer: *u8, length: usize) i64
```

byte reception for local streams: rights a peer attaches are observed and closed

### sock_set_nonblocking

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_set_nonblocking`](linux/x86_64.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_set_nonblocking`](linux/aarch64.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_set_nonblocking`](linux/riscv64.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_set_nonblocking`](linux/riscv32.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_set_nonblocking(fd: usize, enabled: bool) i64
```

switch a socket between blocking and nonblocking

### sock_connect_begin

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_connect_begin`](linux/x86_64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_connect_begin`](linux/aarch64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_connect_begin`](linux/riscv64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_connect_begin`](linux/riscv32.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

start a connect on a nonblocking socket

### sock_connect_poll

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_connect_poll`](linux/x86_64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_connect_poll`](linux/aarch64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_connect_poll`](linux/riscv64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_connect_poll`](linux/riscv32.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

### CONNECT_PENDING

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.CONNECT_PENDING`](linux/x86_64.md#connect_pending), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.CONNECT_PENDING`](linux/aarch64.md#connect_pending), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.CONNECT_PENDING`](linux/riscv64.md#connect_pending), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.CONNECT_PENDING`](linux/riscv32.md#connect_pending), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val CONNECT_PENDING: i64 = 1
```

what sock_connect_begin and sock_connect_poll return while the connect is in flight

### sock_close

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_close`](linux/x86_64.md#sock_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_close`](linux/aarch64.md#sock_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_close`](linux/riscv64.md#sock_close), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_close`](linux/riscv32.md#sock_close), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_close(fd: usize) i64
```

close a socket file descriptor

### sock_create

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_create`](linux/x86_64.md#sock_create), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_create`](linux/aarch64.md#sock_create), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_create`](linux/riscv64.md#sock_create), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_create`](linux/riscv32.md#sock_create), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

create a socket file descriptor

### sock_create_flags

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_create_flags`](linux/x86_64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_create_flags`](linux/aarch64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_create_flags`](linux/riscv64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_create_flags`](linux/riscv32.md#sock_create_flags), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

create a socket file descriptor with its blocking and inheritance chosen

### sock_bind

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_bind`](linux/x86_64.md#sock_bind), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_bind`](linux/aarch64.md#sock_bind), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_bind`](linux/riscv64.md#sock_bind), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_bind`](linux/riscv32.md#sock_bind), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

bind a socket to an address

### sock_listen

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_listen`](linux/x86_64.md#sock_listen), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_listen`](linux/aarch64.md#sock_listen), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_listen`](linux/riscv64.md#sock_listen), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_listen`](linux/riscv32.md#sock_listen), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

mark a socket as a passive listener

### sock_accept

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_accept`](linux/x86_64.md#sock_accept), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_accept`](linux/aarch64.md#sock_accept), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_accept`](linux/riscv64.md#sock_accept), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_accept`](linux/riscv32.md#sock_accept), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

accept a connection on a listening socket

### sock_accept_flags

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_accept_flags`](linux/x86_64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_accept_flags`](linux/aarch64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_accept_flags`](linux/riscv64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_accept_flags`](linux/riscv32.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

accept a connection with the accepted socket's blocking and inheritance chosen

### sock_connect

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_connect`](linux/x86_64.md#sock_connect), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_connect`](linux/aarch64.md#sock_connect), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_connect`](linux/riscv64.md#sock_connect), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_connect`](linux/riscv32.md#sock_connect), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

connect a socket to a remote address

### sock_sendto

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_sendto`](linux/x86_64.md#sock_sendto), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_sendto`](linux/aarch64.md#sock_sendto), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_sendto`](linux/riscv64.md#sock_sendto), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_sendto`](linux/riscv32.md#sock_sendto), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

send data to a specific address

### sock_recvfrom

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_recvfrom`](linux/x86_64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_recvfrom`](linux/aarch64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_recvfrom`](linux/riscv64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_recvfrom`](linux/riscv32.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

receive data and source address

### sock_peek_readable

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_peek_readable`](linux/x86_64.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_peek_readable`](linux/aarch64.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_peek_readable`](linux/riscv64.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_peek_readable`](linux/riscv32.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_peek_readable(fd: usize) i64
```

peek at a stream socket without consuming or blocking

### sock_shutdown

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_shutdown`](linux/x86_64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_shutdown`](linux/aarch64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_shutdown`](linux/riscv64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_shutdown`](linux/riscv32.md#sock_shutdown), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

shut down part or all of a socket connection

### sock_setopt

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_setopt`](linux/x86_64.md#sock_setopt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_setopt`](linux/aarch64.md#sock_setopt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_setopt`](linux/riscv64.md#sock_setopt), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_setopt`](linux/riscv32.md#sock_setopt), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

set a socket option

### sock_getopt

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_getopt`](linux/x86_64.md#sock_getopt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_getopt`](linux/aarch64.md#sock_getopt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_getopt`](linux/riscv64.md#sock_getopt), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_getopt`](linux/riscv32.md#sock_getopt), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

read a socket option

### sock_local_addr

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_local_addr`](linux/x86_64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_local_addr`](linux/aarch64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_local_addr`](linux/riscv64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_local_addr`](linux/riscv32.md#sock_local_addr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

the address a socket is bound to

### sock_remote_addr

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_remote_addr`](linux/x86_64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_remote_addr`](linux/aarch64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_remote_addr`](linux/riscv64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_remote_addr`](linux/riscv32.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

the address of a connected socket's peer

### sock_inheritable

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_inheritable`](linux/x86_64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_inheritable`](linux/aarch64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_inheritable`](linux/riscv64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_inheritable`](linux/riscv32.md#sock_inheritable), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

whether a socket stays open across exec

### IoCompletion

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IoCompletion`](linux/x86_64.md#iocompletion), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IoCompletion`](linux/aarch64.md#iocompletion), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IoCompletion`](linux/riscv64.md#iocompletion), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IoCompletion`](linux/riscv32.md#iocompletion), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub rec IoCompletion {
    context: u64;
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

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IO_EVENT_READ`](linux/x86_64.md#io_event_read), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IO_EVENT_READ`](linux/aarch64.md#io_event_read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IO_EVENT_READ`](linux/riscv64.md#io_event_read), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IO_EVENT_READ`](linux/riscv32.md#io_event_read), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IO_EVENT_READ:   u32 = 0x01
```

### IO_EVENT_WRITE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IO_EVENT_WRITE`](linux/x86_64.md#io_event_write), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IO_EVENT_WRITE`](linux/aarch64.md#io_event_write), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IO_EVENT_WRITE`](linux/riscv64.md#io_event_write), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IO_EVENT_WRITE`](linux/riscv32.md#io_event_write), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IO_EVENT_WRITE:  u32 = 0x02
```

### IO_EVENT_ERROR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IO_EVENT_ERROR`](linux/x86_64.md#io_event_error), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IO_EVENT_ERROR`](linux/aarch64.md#io_event_error), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IO_EVENT_ERROR`](linux/riscv64.md#io_event_error), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IO_EVENT_ERROR`](linux/riscv32.md#io_event_error), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IO_EVENT_ERROR:  u32 = 0x04
```

### IO_EVENT_HANGUP

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IO_EVENT_HANGUP`](linux/x86_64.md#io_event_hangup), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IO_EVENT_HANGUP`](linux/aarch64.md#io_event_hangup), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IO_EVENT_HANGUP`](linux/riscv64.md#io_event_hangup), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IO_EVENT_HANGUP`](linux/riscv32.md#io_event_hangup), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IO_EVENT_HANGUP: u32 = 0x08
```

### IO_EVENT_WAKE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.IO_EVENT_WAKE`](linux/x86_64.md#io_event_wake), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.IO_EVENT_WAKE`](linux/aarch64.md#io_event_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.IO_EVENT_WAKE`](linux/riscv64.md#io_event_wake), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.IO_EVENT_WAKE`](linux/riscv32.md#io_event_wake), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val IO_EVENT_WAKE:   u32 = 0x10
```

### io_queue_create

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_create`](linux/x86_64.md#io_queue_create), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_create`](linux/aarch64.md#io_queue_create), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_create`](linux/riscv64.md#io_queue_create), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_create`](linux/riscv32.md#io_queue_create), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

open a completion queue: an epoll instance with a wake eventfd watched
under context 0

### io_queue_wait

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_wait`](linux/x86_64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_wait`](linux/aarch64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_wait`](linux/riscv64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_wait`](linux/riscv32.md#io_queue_wait), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

wait for one completion and discard it

### io_queue_watch

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_watch`](linux/x86_64.md#io_queue_watch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_watch`](linux/aarch64.md#io_queue_watch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_watch`](linux/riscv64.md#io_queue_watch), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_watch`](linux/riscv32.md#io_queue_watch), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_watch(queue: *std.system.os.shared.IoQueue, resource: usize, context: u64, events: u32) i64
```

registers a resource that has no registration on the queue yet. a resource
that is already registered is refused with EEXIST, never taken over

### io_queue_rearm

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_rearm`](linux/x86_64.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_rearm`](linux/aarch64.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_rearm`](linux/riscv64.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_rearm`](linux/riscv32.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_rearm(queue: *std.system.os.shared.IoQueue, resource: usize, context: u64, events: u32) i64
```

arms again a registration the caller made with io_queue_watch

### duplicate_to

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.duplicate_to`](linux/x86_64.md#duplicate_to), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.duplicate_to`](linux/aarch64.md#duplicate_to), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.duplicate_to`](linux/riscv64.md#duplicate_to), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.duplicate_to`](linux/riscv32.md#duplicate_to), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun duplicate_to(from: usize, to: usize) i64
```

makes the descriptor to name what from names, closing whatever to named
before, in one step. the copy is not inherited across exec

### io_queue_unwatch

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_unwatch`](linux/x86_64.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_unwatch`](linux/aarch64.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_unwatch`](linux/riscv64.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_unwatch`](linux/riscv32.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_unwatch(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

remove a resource's registration from the queue

### io_queue_poll

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_poll`](linux/x86_64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_poll`](linux/aarch64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_poll`](linux/riscv64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_poll`](linux/riscv32.md#io_queue_poll), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

completions is also the kernel scratch buffer. normalization runs backwards
so expanding packed x86-64 epoll records cannot overwrite unread records.

### io_queue_wake

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_wake`](linux/x86_64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_wake`](linux/aarch64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_wake`](linux/riscv64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_wake`](linux/riscv32.md#io_queue_wake), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

nil is invalid use and a closed queue is EBADF on every platform

### io_queue_close

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.io_queue_close`](linux/x86_64.md#io_queue_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.io_queue_close`](linux/aarch64.md#io_queue_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.io_queue_close`](linux/riscv64.md#io_queue_close), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.io_queue_close`](linux/riscv32.md#io_queue_close), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

close a queue's descriptors and mark it closed

### sock_set_rcvtimeo

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.sock_set_rcvtimeo`](linux/x86_64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.sock_set_rcvtimeo`](linux/aarch64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.sock_set_rcvtimeo`](linux/riscv64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.sock_set_rcvtimeo`](linux/riscv32.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

set the receive timeout on a socket

writes a struct timeval (tv_sec, tv_usec) derived from ms as the SO_RCVTIMEO
option value. ms == 0 clears the timeout, restoring indefinite blocking. once
set, a recv with no data pending fails with EAGAIN after the interval elapses.

### DNS_HOSTS_PATH

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.DNS_HOSTS_PATH`](linux/x86_64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.DNS_HOSTS_PATH`](linux/aarch64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.DNS_HOSTS_PATH`](linux/riscv64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.DNS_HOSTS_PATH`](linux/riscv32.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub val DNS_HOSTS_PATH: str = "/etc/hosts"
```

dns

### random_fill

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.random_fill`](linux/x86_64.md#random_fill), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.random_fill`](linux/aarch64.md#random_fill), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.random_fill`](linux/riscv64.md#random_fill), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.random_fill`](linux/riscv32.md#random_fill), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

random

### thread_spawn

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_spawn`](linux/x86_64.md#thread_spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_spawn`](linux/aarch64.md#thread_spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_spawn`](linux/riscv64.md#thread_spawn), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_spawn`](linux/riscv32.md#thread_spawn), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

threads

### thread_join

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_join`](linux/x86_64.md#thread_join), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_join`](linux/aarch64.md#thread_join), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_join`](linux/riscv64.md#thread_join), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_join`](linux/riscv32.md#thread_join), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

wait for a thread thread_spawn made to end and its stack to be released

### thread_detach

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_detach`](linux/x86_64.md#thread_detach), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_detach`](linux/aarch64.md#thread_detach), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_detach`](linux/riscv64.md#thread_detach), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_detach`](linux/riscv32.md#thread_detach), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_detach(native: usize) i64
```

give up joining a thread thread_spawn made

a std thread needs nothing here, as the join state the caller holds decides
who releases the owner block. a loader-hosted thread's handle is handed back
to the backend

### thread_current_id

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_current_id`](linux/x86_64.md#thread_current_id), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_current_id`](linux/aarch64.md#thread_current_id), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_current_id`](linux/riscv64.md#thread_current_id), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_current_id`](linux/riscv32.md#thread_current_id), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_current_id() i64
```

the calling thread's kernel thread id

### thread_current_name

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_current_name`](linux/x86_64.md#thread_current_name), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_current_name`](linux/aarch64.md#thread_current_name), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_current_name`](linux/riscv64.md#thread_current_name), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_current_name`](linux/riscv32.md#thread_current_name), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

read the calling thread's native diagnostic name

### thread_wait

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_wait`](linux/x86_64.md#thread_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_wait`](linux/aarch64.md#thread_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_wait`](linux/riscv64.md#thread_wait), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_wait`](linux/riscv32.md#thread_wait), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

wraps the futex FUTEX_WAIT operation. returns immediately if *addr
does not equal expected. spurious wakeups are possible.

### thread_wait_until

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_wait_until`](linux/x86_64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_wait_until`](linux/aarch64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_wait_until`](linux/riscv64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_wait_until`](linux/riscv32.md#thread_wait_until), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

block until the word changes or an absolute monotonic deadline is reached

### thread_wake

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_wake`](linux/x86_64.md#thread_wake), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_wake`](linux/aarch64.md#thread_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_wake`](linux/riscv64.md#thread_wake), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_wake`](linux/riscv32.md#thread_wake), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_wake(addr: *i64) i64
```

wake one thread blocked on a futex wait at addr

### thread_block

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_block`](linux/x86_64.md#thread_block), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_block`](linux/aarch64.md#thread_block), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_block`](linux/riscv64.md#thread_block), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_block`](linux/riscv32.md#thread_block), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, read through fs:[0] without a system call

the psABI has the first word of every thread control block point to itself,
so this is the fs base whoever owns it. that is std's block where std owns the
thread pointer, and a C runtime's control block on a thread the C runtime
owns: the main thread under a loader, or a thread C code created. std reads
nothing through that one. a thread whose fs base is 0 faults here, which only
a raw clone that sets it so can make.

### thread_block_enter

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.thread_block_enter`](linux/x86_64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.thread_block_enter`](linux/aarch64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.thread_block_enter`](linux/riscv64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.thread_block_enter`](linux/riscv32.md#thread_block_enter), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's, as its fs base

a block thread_spawn or main_thread_block laid out carries the thread-local
block below it. one laid out anywhere else reaches no thread-locals

### stack_bounds

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.stack_bounds`](linux/x86_64.md#stack_bounds), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.stack_bounds`](linux/aarch64.md#stack_bounds), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.stack_bounds`](linux/riscv64.md#stack_bounds), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.stack_bounds`](linux/riscv32.md#stack_bounds), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, read without a system call

### clock_gettime

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.clock_gettime`](linux/x86_64.md#clock_gettime), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.clock_gettime`](linux/aarch64.md#clock_gettime), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.clock_gettime`](linux/riscv64.md#clock_gettime), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.clock_gettime`](linux/riscv32.md#clock_gettime), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

time

### error_kind

Forwards [`std.system.os.errors.error_kind`](errors.md#error_kind).

```mach
pub fun error_kind(code: i64) std.io.error.Kind
```

errno

### error_message

Forwards the first of these whose condition holds:

- [`std.system.os.linux.x86_64.error_message`](linux/x86_64.md#error_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.linux.aarch64.error_message`](linux/aarch64.md#error_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.linux.riscv64.error_message`](linux/riscv64.md#error_message), where `$mach.build.arch == $mach.arch.riscv64`
- [`std.system.os.linux.riscv32.error_message`](linux/riscv32.md#error_message), where `$mach.build.arch == $mach.arch.riscv32`

```mach
pub fun error_message(code: i64) str
```

return a human-readable message for a negated errno code

