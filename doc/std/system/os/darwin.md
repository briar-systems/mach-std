[std](../../README.md) / [system](../README.md) / [os](README.md) / **darwin**

# std.system.os.darwin

darwin OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need darwin-specific functionality import this module
directly rather than going through std.system.os.

Source: [`src/system/os/darwin.mach`](../../../../src/system/os/darwin.mach)

| Forwards | |
| :--- | :--- |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`timespec`](#timespec), [`DirectoryCursor`](#directorycursor), [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`separator`](#separator) | path |
| [`STDIN_FD`](#stdin_fd) | constants |
| [`STDOUT_FD`](#stdout_fd), [`STDERR_FD`](#stderr_fd), [`O_RDONLY`](#o_rdonly), [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_NONBLOCK`](#o_nonblock), [`O_DIRECTORY`](#o_directory), [`O_NOFOLLOW`](#o_nofollow), [`AT_FDCWD`](#at_fdcwd), [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow), [`AT_REMOVEDIR`](#at_removedir) | |
| [`LOCK_SH`](#lock_sh) | advisory file-lock operations |
| [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un), [`S_IFMT`](#s_ifmt), [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk), [`WNOHANG`](#wnohang), [`WUNTRACED`](#wuntraced), [`WCONTINUED`](#wcontinued), [`CLOCK_REALTIME`](#clock_realtime), [`CLOCK_MONOTONIC`](#clock_monotonic), [`EPERM`](#eperm), [`ENOENT`](#enoent), [`ESRCH`](#esrch), [`EINTR`](#eintr), [`EIO`](#eio), [`ENXIO`](#enxio), [`E2BIG`](#e2big), [`EBADF`](#ebadf), [`ECHILD`](#echild), [`EAGAIN`](#eagain), [`ENOMEM`](#enomem), [`EACCES`](#eacces), [`EFAULT`](#efault), [`EBUSY`](#ebusy), [`EEXIST`](#eexist), [`ENODEV`](#enodev), [`ENOTDIR`](#enotdir), [`EISDIR`](#eisdir), [`EINVAL`](#einval), [`ENFILE`](#enfile), [`EMFILE`](#emfile), [`ETXTBSY`](#etxtbsy), [`ENOSPC`](#enospc), [`EROFS`](#erofs), [`EPIPE`](#epipe), [`ELOOP`](#eloop), [`ENAMETOOLONG`](#enametoolong), [`ERANGE`](#erange), [`ENOTEMPTY`](#enotempty), [`ENOTSUP`](#enotsup), [`EADDRINUSE`](#eaddrinuse), [`ENETUNREACH`](#enetunreach), [`ECONNABORTED`](#econnaborted), [`ECONNRESET`](#econnreset), [`ENOTCONN`](#enotconn), [`ETIMEDOUT`](#etimedout), [`ECONNREFUSED`](#econnrefused), [`EHOSTUNREACH`](#ehostunreach), [`ECANCELED`](#ecanceled), [`EINTR_MAX_RETRIES`](#eintr_max_retries) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size), [`map_alignment`](#map_alignment), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`read`](#read) | filesystem |
| [`write`](#write), [`write_vector`](#write_vector), [`read_at`](#read_at), [`write_at`](#write_at), [`open`](#open) | |
| [`open_native`](#open_native) | the kernel takes a name as bytes, so the native-unit open is open itself |
| [`close`](#close), [`sync_fd`](#sync_fd), [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at) | |
| [`set_mode_at_native`](#set_mode_at_native) | every name below reaches the kernel as bytes, so each native form is the UTF-8 primitive itself |
| [`file_identity`](#file_identity), [`identity_at`](#identity_at), [`identity_at_native`](#identity_at_native), [`retain_identity_at`](#retain_identity_at), [`retain_identity_at_native`](#retain_identity_at_native), [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path), [`stat_path_native`](#stat_path_native), [`stat_mode`](#stat_mode), [`stat_birth`](#stat_birth), [`unlink`](#unlink), [`unlink_native`](#unlink_native), [`rename`](#rename), [`rename_native`](#rename_native), [`symlink`](#symlink), [`symlink_native`](#symlink_native), [`make_dir`](#make_dir), [`make_dir_native`](#make_dir_native), [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_dnit`](#directory_dnit), [`access`](#access), [`access_native`](#access_native), [`seek`](#seek), [`lock_fd`](#lock_fd) | |
| [`terminate`](#terminate) | process |
| [`abort`](#abort), [`terminate_child`](#terminate_child), [`setpgid`](#setpgid), [`getpgid`](#getpgid), [`terminate_group`](#terminate_group), [`kill_group`](#kill_group), [`probe_group`](#probe_group), [`process_watch`](#process_watch), [`process_unwatch`](#process_unwatch), [`spawn`](#spawn), [`spawn_grouped`](#spawn_grouped), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_grouped`](#spawn_redirected_grouped), [`spawn_redirected_in`](#spawn_redirected_in), [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | |
| [`spawn_native`](#spawn_native) | the kernel takes paths and arguments as bytes, so the native-unit spawns are the spawns themselves |
| [`spawn_in_native`](#spawn_in_native), [`spawn_redirected_native`](#spawn_redirected_native), [`spawn_redirected_in_native`](#spawn_redirected_in_native), [`spawn_redirected_in_grouped_native`](#spawn_redirected_in_grouped_native), [`getpid`](#getpid), [`pipe`](#pipe), [`ignore_sigpipe`](#ignore_sigpipe), [`sleep`](#sleep), [`cpu_count`](#cpu_count), [`cpu_features`](#cpu_features), [`cpu_dit`](#cpu_dit), [`thread_affinity`](#thread_affinity), [`set_thread_affinity`](#set_thread_affinity), [`getcwd`](#getcwd), [`getcwd_native`](#getcwd_native), [`getenv`](#getenv), [`environ`](#environ) | |
| [`getenv_native`](#getenv_native) | the environment is the bytes the kernel passed, so its native reads are the reads themselves |
| [`environ_native`](#environ_native), [`temp_dir`](#temp_dir), [`fork`](#fork), [`vfork`](#vfork), [`exec`](#exec), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`AF_INET`](#af_inet) | sockets |
| [`AF_INET6`](#af_inet6), [`SOCK_STREAM`](#sock_stream), [`SOCK_DGRAM`](#sock_dgram), [`SOL_SOCKET`](#sol_socket), [`SO_UNSUPPORTED`](#so_unsupported), [`SO_REUSEADDR`](#so_reuseaddr), [`SO_REUSEPORT`](#so_reuseport), [`SO_EXCLUSIVEADDRUSE`](#so_exclusiveaddruse), [`SO_KEEPALIVE`](#so_keepalive), [`SO_SNDBUF`](#so_sndbuf), [`SO_RCVBUF`](#so_rcvbuf), [`SO_LINGER`](#so_linger), [`SO_RCVTIMEO`](#so_rcvtimeo), [`IPPROTO_IP`](#ipproto_ip), [`IPPROTO_TCP`](#ipproto_tcp), [`IPPROTO_IPV6`](#ipproto_ipv6), [`IP_TOS`](#ip_tos), [`IPV6_V6ONLY`](#ipv6_v6only), [`IPV6_TCLASS`](#ipv6_tclass), [`TCP_NODELAY`](#tcp_nodelay), [`TCP_KEEPIDLE`](#tcp_keepidle), [`TCP_KEEPINTVL`](#tcp_keepintvl), [`TCP_KEEPCNT`](#tcp_keepcnt), [`TCP_FASTOPEN`](#tcp_fastopen), [`SHUT_RD`](#shut_rd), [`SHUT_WR`](#shut_wr), [`SHUT_RDWR`](#shut_rdwr), [`SOCKADDR_IN_SIZE`](#sockaddr_in_size), [`SOCKADDR_IN6_SIZE`](#sockaddr_in6_size), [`SOCKADDR_STORAGE_SIZE`](#sockaddr_storage_size), [`sock_send`](#sock_send), [`sock_recv`](#sock_recv), [`local_stream_recv`](#local_stream_recv), [`IoVector`](#iovector), [`sock_write_vector`](#sock_write_vector), [`sock_send_message`](#sock_send_message), [`sock_receive_message`](#sock_receive_message), [`sock_set_nonblocking`](#sock_set_nonblocking), [`sock_connect_begin`](#sock_connect_begin), [`sock_connect_poll`](#sock_connect_poll), [`CONNECT_PENDING`](#connect_pending), [`sock_close`](#sock_close), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto), [`sock_recvfrom`](#sock_recvfrom), [`sock_peek_readable`](#sock_peek_readable), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable), [`IoCompletion`](#iocompletion), [`IO_EVENT_READ`](#io_event_read), [`IO_EVENT_WRITE`](#io_event_write), [`IO_EVENT_ERROR`](#io_event_error), [`IO_EVENT_HANGUP`](#io_event_hangup), [`IO_EVENT_WAKE`](#io_event_wake), [`io_queue_create`](#io_queue_create), [`io_queue_wait`](#io_queue_wait), [`io_queue_watch`](#io_queue_watch), [`io_queue_rearm`](#io_queue_rearm), [`duplicate_to`](#duplicate_to), [`io_queue_unwatch`](#io_queue_unwatch), [`io_queue_poll`](#io_queue_poll), [`io_queue_wake`](#io_queue_wake), [`io_queue_close`](#io_queue_close), [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | |
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

- [`std.system.os.darwin.aarch64.stat_t`](darwin/aarch64.md#stat_t), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat_t`](darwin/x86_64.md#stat_t), where `$mach.build.arch == $mach.arch.x86_64`

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

kernel ABI types

### timespec

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.timespec`](darwin/aarch64.md#timespec), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.timespec`](darwin/x86_64.md#timespec), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

### DirectoryCursor

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.DirectoryCursor`](darwin/aarch64.md#directorycursor), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.DirectoryCursor`](darwin/x86_64.md#directorycursor), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub rec DirectoryCursor {
    address: usize;
    active:  bool;
    ended:   bool;
    error:   i64;
    stream:  std.system.os.darwin.libsystem.DirectoryStream;
}
```

an open directory enumeration, which directory_init fills in place

### DirectoryEntry

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.DirectoryEntry`](darwin/aarch64.md#directoryentry), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.DirectoryEntry`](darwin/x86_64.md#directoryentry), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.DirectoryInitResult`](darwin/aarch64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.DirectoryInitResult`](darwin/x86_64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### separator

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.separator`](darwin/aarch64.md#separator), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.separator`](darwin/x86_64.md#separator), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val separator: u8 = '/'
```

path

### STDIN_FD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.STDIN_FD`](darwin/aarch64.md#stdin_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.STDIN_FD`](darwin/x86_64.md#stdin_fd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val STDIN_FD:  i32 = 0
```

constants

### STDOUT_FD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.STDOUT_FD`](darwin/aarch64.md#stdout_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.STDOUT_FD`](darwin/x86_64.md#stdout_fd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val STDOUT_FD: i32 = 1
```

### STDERR_FD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.STDERR_FD`](darwin/aarch64.md#stderr_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.STDERR_FD`](darwin/x86_64.md#stderr_fd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val STDERR_FD: i32 = 2
```

### O_RDONLY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_RDONLY`](darwin/aarch64.md#o_rdonly), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_RDONLY`](darwin/x86_64.md#o_rdonly), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_RDONLY:    i32 = 0
```

### O_WRONLY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_WRONLY`](darwin/aarch64.md#o_wronly), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_WRONLY`](darwin/x86_64.md#o_wronly), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_WRONLY:    i32 = 1
```

### O_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_RDWR`](darwin/aarch64.md#o_rdwr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_RDWR`](darwin/x86_64.md#o_rdwr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_RDWR:      i32 = 2
```

### O_CREAT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_CREAT`](darwin/aarch64.md#o_creat), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_CREAT`](darwin/x86_64.md#o_creat), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_CREAT:     i32 = 0x200
```

### O_EXCL

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_EXCL`](darwin/aarch64.md#o_excl), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_EXCL`](darwin/x86_64.md#o_excl), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_EXCL:      i32 = 0x800
```

### O_TRUNC

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_TRUNC`](darwin/aarch64.md#o_trunc), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_TRUNC`](darwin/x86_64.md#o_trunc), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_TRUNC:     i32 = 0x400
```

### O_APPEND

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_APPEND`](darwin/aarch64.md#o_append), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_APPEND`](darwin/x86_64.md#o_append), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_APPEND:    i32 = 8
```

### O_NONBLOCK

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_NONBLOCK`](darwin/aarch64.md#o_nonblock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_NONBLOCK`](darwin/x86_64.md#o_nonblock), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_NONBLOCK: i32 = 4
```

### O_DIRECTORY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_DIRECTORY`](darwin/aarch64.md#o_directory), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_DIRECTORY`](darwin/x86_64.md#o_directory), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_DIRECTORY: i32 = 0x100000
```

### O_NOFOLLOW

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.O_NOFOLLOW`](darwin/aarch64.md#o_nofollow), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.O_NOFOLLOW`](darwin/x86_64.md#o_nofollow), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val O_NOFOLLOW:  i32 = 0x00000100
```

### AT_FDCWD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.AT_FDCWD`](darwin/aarch64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.AT_FDCWD`](darwin/x86_64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val AT_FDCWD:            i32 = -2
```

### AT_SYMLINK_NOFOLLOW

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.AT_SYMLINK_NOFOLLOW`](darwin/aarch64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.AT_SYMLINK_NOFOLLOW`](darwin/x86_64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0020
```

### AT_REMOVEDIR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.AT_REMOVEDIR`](darwin/aarch64.md#at_removedir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.AT_REMOVEDIR`](darwin/x86_64.md#at_removedir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val AT_REMOVEDIR:        i32 = 0x0080
```

### LOCK_SH

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.LOCK_SH`](darwin/aarch64.md#lock_sh), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.LOCK_SH`](darwin/x86_64.md#lock_sh), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val LOCK_SH: i32 = 1
```

advisory file-lock operations

### LOCK_EX

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.LOCK_EX`](darwin/aarch64.md#lock_ex), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.LOCK_EX`](darwin/x86_64.md#lock_ex), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.LOCK_NB`](darwin/aarch64.md#lock_nb), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.LOCK_NB`](darwin/x86_64.md#lock_nb), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.LOCK_UN`](darwin/aarch64.md#lock_un), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.LOCK_UN`](darwin/x86_64.md#lock_un), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.S_IFMT`](darwin/aarch64.md#s_ifmt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.S_IFMT`](darwin/x86_64.md#s_ifmt), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val S_IFMT:  u32 = 0o170000
```

### S_IFDIR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.S_IFDIR`](darwin/aarch64.md#s_ifdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.S_IFDIR`](darwin/x86_64.md#s_ifdir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.S_IFREG`](darwin/aarch64.md#s_ifreg), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.S_IFREG`](darwin/x86_64.md#s_ifreg), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.S_IFLNK`](darwin/aarch64.md#s_iflnk), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.S_IFLNK`](darwin/x86_64.md#s_iflnk), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val S_IFLNK: u32 = 0o120000
```

### WNOHANG

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.WNOHANG`](darwin/aarch64.md#wnohang), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.WNOHANG`](darwin/x86_64.md#wnohang), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val WNOHANG:    i32 = 1
```

### WUNTRACED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.WUNTRACED`](darwin/aarch64.md#wuntraced), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.WUNTRACED`](darwin/x86_64.md#wuntraced), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val WUNTRACED:  i32 = 2
```

### WCONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.WCONTINUED`](darwin/aarch64.md#wcontinued), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.WCONTINUED`](darwin/x86_64.md#wcontinued), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val WCONTINUED: i32 = 0x10
```

### CLOCK_REALTIME

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.CLOCK_REALTIME`](darwin/aarch64.md#clock_realtime), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.CLOCK_REALTIME`](darwin/x86_64.md#clock_realtime), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val CLOCK_REALTIME:  i32 = 0
```

### CLOCK_MONOTONIC

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.CLOCK_MONOTONIC`](darwin/aarch64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.CLOCK_MONOTONIC`](darwin/x86_64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val CLOCK_MONOTONIC: i32 = 6
```

### EPERM

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EPERM`](darwin/aarch64.md#eperm), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EPERM`](darwin/x86_64.md#eperm), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EPERM:        i64 = -1
```

### ENOENT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOENT`](darwin/aarch64.md#enoent), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOENT`](darwin/x86_64.md#enoent), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOENT:       i64 = -2
```

### ESRCH

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ESRCH`](darwin/aarch64.md#esrch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ESRCH`](darwin/x86_64.md#esrch), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ESRCH:        i64 = -3
```

### EINTR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EINTR`](darwin/aarch64.md#eintr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EINTR`](darwin/x86_64.md#eintr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EINTR:        i64 = -4
```

### EIO

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EIO`](darwin/aarch64.md#eio), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EIO`](darwin/x86_64.md#eio), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EIO:          i64 = -5
```

### ENXIO

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENXIO`](darwin/aarch64.md#enxio), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENXIO`](darwin/x86_64.md#enxio), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENXIO:        i64 = -6
```

### E2BIG

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.E2BIG`](darwin/aarch64.md#e2big), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.E2BIG`](darwin/x86_64.md#e2big), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val E2BIG:        i64 = -7
```

### EBADF

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EBADF`](darwin/aarch64.md#ebadf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EBADF`](darwin/x86_64.md#ebadf), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EBADF:        i64 = -9
```

### ECHILD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ECHILD`](darwin/aarch64.md#echild), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ECHILD`](darwin/x86_64.md#echild), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ECHILD:       i64 = -10
```

### EAGAIN

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EAGAIN`](darwin/aarch64.md#eagain), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EAGAIN`](darwin/x86_64.md#eagain), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EAGAIN:       i64 = -35
```

### ENOMEM

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOMEM`](darwin/aarch64.md#enomem), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOMEM`](darwin/x86_64.md#enomem), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOMEM:       i64 = -12
```

### EACCES

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EACCES`](darwin/aarch64.md#eacces), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EACCES`](darwin/x86_64.md#eacces), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EACCES:       i64 = -13
```

### EFAULT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EFAULT`](darwin/aarch64.md#efault), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EFAULT`](darwin/x86_64.md#efault), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EFAULT:       i64 = -14
```

### EBUSY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EBUSY`](darwin/aarch64.md#ebusy), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EBUSY`](darwin/x86_64.md#ebusy), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EBUSY:        i64 = -16
```

### EEXIST

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EEXIST`](darwin/aarch64.md#eexist), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EEXIST`](darwin/x86_64.md#eexist), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EEXIST:       i64 = -17
```

### ENODEV

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENODEV`](darwin/aarch64.md#enodev), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENODEV`](darwin/x86_64.md#enodev), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENODEV:       i64 = -19
```

### ENOTDIR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOTDIR`](darwin/aarch64.md#enotdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOTDIR`](darwin/x86_64.md#enotdir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOTDIR:      i64 = -20
```

### EISDIR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EISDIR`](darwin/aarch64.md#eisdir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EISDIR`](darwin/x86_64.md#eisdir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EISDIR:       i64 = -21
```

### EINVAL

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EINVAL`](darwin/aarch64.md#einval), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EINVAL`](darwin/x86_64.md#einval), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EINVAL:       i64 = -22
```

### ENFILE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENFILE`](darwin/aarch64.md#enfile), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENFILE`](darwin/x86_64.md#enfile), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENFILE:       i64 = -23
```

### EMFILE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EMFILE`](darwin/aarch64.md#emfile), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EMFILE`](darwin/x86_64.md#emfile), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EMFILE:       i64 = -24
```

### ETXTBSY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ETXTBSY`](darwin/aarch64.md#etxtbsy), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ETXTBSY`](darwin/x86_64.md#etxtbsy), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ETXTBSY:      i64 = -26
```

### ENOSPC

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOSPC`](darwin/aarch64.md#enospc), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOSPC`](darwin/x86_64.md#enospc), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOSPC:       i64 = -28
```

### EROFS

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EROFS`](darwin/aarch64.md#erofs), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EROFS`](darwin/x86_64.md#erofs), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EROFS:        i64 = -30
```

### EPIPE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EPIPE`](darwin/aarch64.md#epipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EPIPE`](darwin/x86_64.md#epipe), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EPIPE:        i64 = -32
```

### ELOOP

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ELOOP`](darwin/aarch64.md#eloop), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ELOOP`](darwin/x86_64.md#eloop), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ELOOP:        i64 = -62
```

### ENAMETOOLONG

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENAMETOOLONG`](darwin/aarch64.md#enametoolong), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENAMETOOLONG`](darwin/x86_64.md#enametoolong), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENAMETOOLONG: i64 = -63
```

### ERANGE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ERANGE`](darwin/aarch64.md#erange), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ERANGE`](darwin/x86_64.md#erange), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ERANGE:       i64 = -34
```

### ENOTEMPTY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOTEMPTY`](darwin/aarch64.md#enotempty), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOTEMPTY`](darwin/x86_64.md#enotempty), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOTEMPTY:    i64 = -66
```

### ENOTSUP

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ENOTSUP`](darwin/aarch64.md#enotsup), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ENOTSUP`](darwin/x86_64.md#enotsup), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val ENOTSUP:      i64 = -45
```

### EADDRINUSE

Forwards [`std.system.os.darwin.shared.EADDRINUSE`](darwin/shared.md#constants).

```mach
pub val EADDRINUSE:   i64 = -48
```

### ENETUNREACH

Forwards [`std.system.os.darwin.shared.ENETUNREACH`](darwin/shared.md#constants).

```mach
pub val ENETUNREACH:  i64 = -51
```

### ECONNABORTED

Forwards [`std.system.os.darwin.shared.ECONNABORTED`](darwin/shared.md#constants).

```mach
pub val ECONNABORTED: i64 = -53
```

### ECONNRESET

Forwards [`std.system.os.darwin.shared.ECONNRESET`](darwin/shared.md#constants).

```mach
pub val ECONNRESET:   i64 = -54
```

### ENOTCONN

Forwards [`std.system.os.darwin.shared.ENOTCONN`](darwin/shared.md#constants).

```mach
pub val ENOTCONN:     i64 = -57
```

### ETIMEDOUT

Forwards [`std.system.os.darwin.shared.ETIMEDOUT`](darwin/shared.md#constants).

```mach
pub val ETIMEDOUT:    i64 = -60
```

### ECONNREFUSED

Forwards [`std.system.os.darwin.shared.ECONNREFUSED`](darwin/shared.md#constants).

```mach
pub val ECONNREFUSED: i64 = -61
```

### EHOSTUNREACH

Forwards [`std.system.os.darwin.shared.EHOSTUNREACH`](darwin/shared.md#constants).

```mach
pub val EHOSTUNREACH: i64 = -65
```

### ECANCELED

Forwards [`std.system.os.darwin.shared.ECANCELED`](darwin/shared.md#constants).

```mach
pub val ECANCELED:    i64 = -89
```

### EINTR_MAX_RETRIES

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.EINTR_MAX_RETRIES`](darwin/aarch64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.EINTR_MAX_RETRIES`](darwin/x86_64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val EINTR_MAX_RETRIES: usize = 8
```

### allocate

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.allocate`](darwin/aarch64.md#allocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.allocate`](darwin/x86_64.md#allocate), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.deallocate`](darwin/aarch64.md#deallocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.deallocate`](darwin/x86_64.md#deallocate), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

unmap memory allocate mapped

### reallocate

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.reallocate`](darwin/aarch64.md#reallocate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.reallocate`](darwin/x86_64.md#reallocate), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

darwin has no mremap, allocate new, copy, free old

### heap_region_base

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.heap_region_base`](darwin/aarch64.md#heap_region_base), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.heap_region_base`](darwin/x86_64.md#heap_region_base), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun heap_region_base() usize
```

the current end of the simulated program break

the first call reserves HEAP_RESERVE bytes of inaccessible address space, and
the break starts at its base

### heap_region_extend

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.heap_region_extend`](darwin/aarch64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.heap_region_extend`](darwin/x86_64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun heap_region_extend(addr: usize) usize
```

move the simulated program break up to addr

the pages between the old and the new break are made read-write. the break
never moves down and never past the reserve

### protect

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.protect`](darwin/aarch64.md#protect), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.protect`](darwin/x86_64.md#protect), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

change the protection of a memory region

### lock

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.lock`](darwin/aarch64.md#lock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.lock`](darwin/x86_64.md#lock), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun lock(p: ptr, size: usize) i64
```

lock a memory region into physical memory, keeping it out of swap

### unlock

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.unlock`](darwin/aarch64.md#unlock), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.unlock`](darwin/x86_64.md#unlock), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun unlock(p: ptr, size: usize) i64
```

unlock a memory region lock locked

### advise

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.advise`](darwin/aarch64.md#advise), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.advise`](darwin/x86_64.md#advise), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

advise the kernel how a memory region will be accessed

### page_size

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.page_size`](darwin/aarch64.md#page_size), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.page_size`](darwin/x86_64.md#page_size), where `$mach.build.arch == $mach.arch.x86_64`

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub fun page_size() usize
```

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
pub fun page_size() usize
```

### map_alignment

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.map_alignment`](darwin/aarch64.md#map_alignment), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.map_alignment`](darwin/x86_64.md#map_alignment), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun map_alignment() usize
```

the alignment map_file requires of an offset, the page size

### map_file

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.map_file`](darwin/aarch64.md#map_file), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.map_file`](darwin/x86_64.md#map_file), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map part of a file into memory, shared with the file

### sync_file

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sync_file`](darwin/aarch64.md#sync_file), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sync_file`](darwin/x86_64.md#sync_file), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a shared file mapping to its file and wait for the write

### read

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.read`](darwin/aarch64.md#read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.read`](darwin/x86_64.md#read), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

filesystem

### write

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.write`](darwin/aarch64.md#write), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.write`](darwin/x86_64.md#write), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a descriptor

a call EINTR interrupts is tried again, for at most EINTR_MAX_RETRIES attempts
in all

### write_vector

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.write_vector`](darwin/aarch64.md#write_vector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.write_vector`](darwin/x86_64.md#write_vector), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun write_vector(fd: i32, vectors: *IoVector, count: usize) i64
```

write several buffers to a file descriptor in order, in one call

a call EINTR interrupts is tried again, for at most EINTR_MAX_RETRIES attempts
in all

### read_at

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.read_at`](darwin/aarch64.md#read_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.read_at`](darwin/x86_64.md#read_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

positioned file access does not mutate the descriptor offset

### write_at

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.write_at`](darwin/aarch64.md#write_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.write_at`](darwin/x86_64.md#write_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

write bytes at a file offset without moving the descriptor offset

a call EINTR interrupts is tried again, for at most EINTR_MAX_RETRIES attempts
in all

### open

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.open`](darwin/aarch64.md#open), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.open`](darwin/x86_64.md#open), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path relative to a directory descriptor

`mode` is only consulted by the kernel when `flags` carries O_CREAT, so it is
passed in the variadic tail only in that case. the two forms are not
interchangeable spellings of one call: apple arm64 passes the whole variadic
tail on the stack, so the no-O_CREAT form genuinely passes nothing rather
than passing an ignored register.

### open_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.open`](darwin/aarch64.md#open), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.open`](darwin/x86_64.md#open), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

the kernel takes a name as bytes, so the native-unit open is open itself

### close

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.close`](darwin/aarch64.md#close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.close`](darwin/x86_64.md#close), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun close(fd: i32) i64
```

close a descriptor

a failed close does NOT mean the descriptor is still open: darwin has already
released it by the time an error is reported. callers must not retry, and
none do - the return exists to surface a deferred write error.

### sync_fd

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sync_fd`](darwin/aarch64.md#sync_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sync_fd`](darwin/x86_64.md#sync_fd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sync_fd(fd: i32) i64
```

flush an open file's data and metadata to its backing storage

### stat

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stat`](darwin/aarch64.md#stat), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat`](darwin/x86_64.md#stat), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

read an open file's metadata

### set_mode

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.set_mode`](darwin/aarch64.md#set_mode), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.set_mode`](darwin/x86_64.md#set_mode), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

set a file's permission bits through an open descriptor

### set_mode_at

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.set_mode_at`](darwin/aarch64.md#set_mode_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.set_mode_at`](darwin/x86_64.md#set_mode_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

set the permission bits of a path relative to a directory, without following
a final symlink

### set_mode_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.set_mode_at`](darwin/aarch64.md#set_mode_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.set_mode_at`](darwin/x86_64.md#set_mode_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

every name below reaches the kernel as bytes, so each native form is the
UTF-8 primitive itself

### file_identity

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.file_identity`](darwin/aarch64.md#file_identity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.file_identity`](darwin/x86_64.md#file_identity), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

observational ids do not retain an object after this call

### identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.identity_at`](darwin/aarch64.md#identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.identity_at`](darwin/x86_64.md#identity_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the object a path relative to a directory names, without
following a final symlink

the identity is observational and retains nothing

### identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.identity_at`](darwin/aarch64.md#identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.identity_at`](darwin/x86_64.md#identity_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the object a path relative to a directory names, without
following a final symlink

the identity is observational and retains nothing

### retain_identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.retain_identity_at`](darwin/aarch64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.retain_identity_at`](darwin/x86_64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_evtonly retains identity without data i/o after explicit read authorization

### retain_identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.retain_identity_at`](darwin/aarch64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.retain_identity_at`](darwin/x86_64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

o_evtonly retains identity without data i/o after explicit read authorization

### publication_capabilities

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.publication_capabilities`](darwin/aarch64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.publication_capabilities`](darwin/x86_64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun publication_capabilities(fd: i32) i64
```

the cooperative publication capabilities of the filesystem holding fd

only a local apfs or hfs volume has any, and it has PUBLICATION_CLAIMS and
PUBLICATION_READ_RETAIN_REPLACE

### stat_path

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stat_path`](darwin/aarch64.md#stat_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat_path`](darwin/x86_64.md#stat_path), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

read a path's metadata relative to a directory

### stat_path_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stat_path`](darwin/aarch64.md#stat_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat_path`](darwin/x86_64.md#stat_path), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

read a path's metadata relative to a directory

### stat_mode

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stat_mode`](darwin/aarch64.md#stat_mode), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat_mode`](darwin/x86_64.md#stat_mode), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 16-bit in the darwin stat64 ABI (mode_t is __uint16_t); widen it
so portable callers read the mode uniformly with the 32-bit platforms.

### stat_birth

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stat_birth`](darwin/aarch64.md#stat_birth), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stat_birth`](darwin/x86_64.md#stat_birth), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stat_birth(st: *stat_t, sec: *i64, nsec: *i64) bool
```

the birth time of a stat record

### unlink

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.unlink`](darwin/aarch64.md#unlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.unlink`](darwin/x86_64.md#unlink), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

remove a name relative to a directory

### unlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.unlink`](darwin/aarch64.md#unlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.unlink`](darwin/x86_64.md#unlink), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

remove a name relative to a directory

### rename

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.rename`](darwin/aarch64.md#rename), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.rename`](darwin/x86_64.md#rename), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

rename a path, each side relative to its own directory

### rename_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.rename`](darwin/aarch64.md#rename), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.rename`](darwin/x86_64.md#rename), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

rename a path, each side relative to its own directory

### symlink

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.symlink`](darwin/aarch64.md#symlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.symlink`](darwin/x86_64.md#symlink), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### symlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.symlink`](darwin/aarch64.md#symlink), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.symlink`](darwin/x86_64.md#symlink), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### make_dir

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.make_dir`](darwin/aarch64.md#make_dir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.make_dir`](darwin/x86_64.md#make_dir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

create a directory relative to a directory

### make_dir_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.make_dir`](darwin/aarch64.md#make_dir), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.make_dir`](darwin/x86_64.md#make_dir), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

create a directory relative to a directory

### directory_init

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.directory_init`](darwin/aarch64.md#directory_init), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.directory_init`](darwin/x86_64.md#directory_init), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.directory_next`](darwin/aarch64.md#directory_next), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.directory_next`](darwin/x86_64.md#directory_next), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

read the next entry of a directory cursor

a failure is sticky, so every later call returns the same code. a record
with an empty name, a name or terminator past its extent, or a null byte
inside the name is EIO

### directory_dnit

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.directory_dnit`](darwin/aarch64.md#directory_dnit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.directory_dnit`](darwin/x86_64.md#directory_dnit), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

closedir consumes its stream even when the underlying close fails

### access

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.access`](darwin/aarch64.md#access), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.access`](darwin/x86_64.md#access), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

check access to a path relative to a directory

### access_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.access`](darwin/aarch64.md#access), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.access`](darwin/x86_64.md#access), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

check access to a path relative to a directory

### seek

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.seek`](darwin/aarch64.md#seek), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.seek`](darwin/x86_64.md#seek), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

reposition a descriptor's offset

lseek's failure sentinel is exactly -1, not "negative": the success value is
a file offset, which is never negative but IS returned as a signed 64-bit
number that a caller may legitimately compare against. testing for the
documented sentinel rather than for a sign keeps that distinction.

### lock_fd

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.lock_fd`](darwin/aarch64.md#lock_fd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.lock_fd`](darwin/x86_64.md#lock_fd), where `$mach.build.arch == $mach.arch.x86_64`

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

### terminate

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.terminate`](darwin/aarch64.md#terminate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.terminate`](darwin/x86_64.md#terminate), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun terminate(code: i64)
```

process

### abort

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.abort`](darwin/aarch64.md#abort), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.abort`](darwin/x86_64.md#abort), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun abort()
```

abort the process immediately with exit code 255

the process-wide SIGABRT is what a debugger or crash reporter sees; if it
is ignored or handled, the exit below still ends the process.

### terminate_child

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.terminate_child`](darwin/aarch64.md#terminate_child), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.terminate_child`](darwin/x86_64.md#terminate_child), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.setpgid`](darwin/aarch64.md#setpgid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.setpgid`](darwin/x86_64.md#setpgid), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun setpgid(pid: i64, pgid: i64) i64
```

setpgid: set (or join) the process group ID of a process

### getpgid

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getpgid`](darwin/aarch64.md#getpgid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getpgid`](darwin/x86_64.md#getpgid), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun getpgid(pid: i64) i64
```

getpgid: read the process group ID of a process

### terminate_group

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.terminate_group`](darwin/aarch64.md#terminate_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.terminate_group`](darwin/x86_64.md#terminate_group), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.kill_group`](darwin/aarch64.md#kill_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.kill_group`](darwin/x86_64.md#kill_group), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun kill_group(pgid: i64) i64
```

forcefully stop every process in a group without reaping any of them

the group's members get SIGKILL, which none of them can catch or ignore.
as with terminate_group there is no ownership probe, and members stay
individually waitable.

### probe_group

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.probe_group`](darwin/aarch64.md#probe_group), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.probe_group`](darwin/x86_64.md#probe_group), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun probe_group(pgid: i64) i64
```

whether any process is left in a group, without signalling it

kill(-pgid, 0) checks for members and delivers nothing. a member this
process may not signal still counts, so EPERM reads as present.

### process_watch

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.process_watch`](darwin/aarch64.md#process_watch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.process_watch`](darwin/x86_64.md#process_watch), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun process_watch(queue: *std.system.os.shared.IoQueue, pid: i64, context: u64) i64
```

make the end of the child `pid` a readiness event on `queue`, so the queue's
wait returns once the child ends: a one-shot EVFILT_PROC NOTE_EXIT filter

### process_unwatch

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.process_unwatch`](darwin/aarch64.md#process_unwatch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.process_unwatch`](darwin/x86_64.md#process_unwatch), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun process_unwatch(queue: *std.system.os.shared.IoQueue, watch: i64) i64
```

release a watch process_watch made, whether or not it fired

### spawn

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn`](darwin/aarch64.md#spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn`](darwin/x86_64.md#spawn), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

### spawn_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_grouped`](darwin/aarch64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_grouped`](darwin/x86_64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program, placed as the leader of
its own new process group (see spawn_redirected_in_grouped)

### spawn_in

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_in`](darwin/aarch64.md#spawn_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_in`](darwin/x86_64.md#spawn_in), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_redirected`](darwin/aarch64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected`](darwin/x86_64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.spawn_redirected_grouped`](darwin/aarch64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected_grouped`](darwin/x86_64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed as the leader of its own new process group (see
spawn_redirected_in_grouped)

### spawn_redirected_in

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_redirected_in`](darwin/aarch64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected_in`](darwin/x86_64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory

`cwd` is the directory the child starts in, or nil to inherit the parent's.
the chdir happens in the child, after the fork, so the parent's own
working directory is untouched. passing it here rather than prefixing a `cd`
onto a shell command keeps the path out of the command line, where it would
have to survive a quoting convention the target program may not share
(mach#2587).

### spawn_redirected_in_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_redirected_in_grouped`](darwin/aarch64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected_in_grouped`](darwin/x86_64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

the child alone creates the group and acknowledges it through a private pipe.
the parent returns only after receiving readiness, so immediate group signals
cannot race establishment. failed handshakes close their pipes and reap the
unexposed child before returning the native error.

### spawn_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn`](darwin/aarch64.md#spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn`](darwin/x86_64.md#spawn), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

the kernel takes paths and arguments as bytes, so the native-unit spawns are the spawns themselves

### spawn_in_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_in`](darwin/aarch64.md#spawn_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_in`](darwin/x86_64.md#spawn_in), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_redirected`](darwin/aarch64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected`](darwin/x86_64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.spawn_redirected_in`](darwin/aarch64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected_in`](darwin/x86_64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory

`cwd` is the directory the child starts in, or nil to inherit the parent's.
the chdir happens in the child, after the fork, so the parent's own
working directory is untouched. passing it here rather than prefixing a `cd`
onto a shell command keeps the path out of the command line, where it would
have to survive a quoting convention the target program may not share
(mach#2587).

### spawn_redirected_in_grouped_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.spawn_redirected_in_grouped`](darwin/aarch64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.spawn_redirected_in_grouped`](darwin/x86_64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun spawn_redirected_in_grouped(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn a child with redirected streams and an explicit working directory,
placed as the leader of its own new process group

the child alone creates the group and acknowledges it through a private pipe.
the parent returns only after receiving readiness, so immediate group signals
cannot race establishment. failed handshakes close their pipes and reap the
unexposed child before returning the native error.

### getpid

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getpid`](darwin/aarch64.md#getpid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getpid`](darwin/x86_64.md#getpid), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun getpid() i64
```

return the current process ID

### pipe

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.pipe`](darwin/aarch64.md#pipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.pipe`](darwin/x86_64.md#pipe), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

this was hand-written asm for one reason: the raw XNU pipe trap returns the
two descriptors in x0/x1 and signals failure through the carry flag, and the
syscall DSL captures neither. libSystem's pipe(2) is an ordinary C function
that writes both descriptors through the caller's array and reports failure
as -1, so the arch-specific asm has nothing left to do and the wrapper is now
identical on both darwin architectures - it lives here only because `pipe` is
part of the per-arch module's published surface.

### ignore_sigpipe

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ignore_sigpipe`](darwin/aarch64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ignore_sigpipe`](darwin/x86_64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

signal(3) installs the disposition through public libSystem. it is
process-wide, so subsequent writes from every thread return EPIPE when their
pipe has no reader instead of terminating the process.

### sleep

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sleep`](darwin/aarch64.md#sleep), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sleep`](darwin/x86_64.md#sleep), where `$mach.build.arch == $mach.arch.x86_64`

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

### cpu_count

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.cpu_count`](darwin/aarch64.md#cpu_count), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.cpu_count`](darwin/x86_64.md#cpu_count), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun cpu_count() i64
```

the currently active processor count
reads hw.activecpu, with a minimum of one if the query fails

### cpu_features

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.cpu_features`](darwin/aarch64.md#cpu_features), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.cpu_features`](darwin/x86_64.md#cpu_features), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

the running processor's instruction-set extensions

x86_64 reads cpuid, which needs no OS. aarch64 asks sysctl for
hw.optional.arm.FEAT_SHA256, FEAT_AES and FEAT_PMULL, each an int that is 0
or absent when the processor lacks it, as hw.activecpu is read above

### cpu_dit

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.cpu_dit`](darwin/aarch64.md#cpu_dit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.cpu_dit`](darwin/x86_64.md#cpu_dit), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun cpu_dit() i64
```

whether the processor provides the data-independent-timing mode

aarch64 asks sysctl for hw.optional.arm.FEAT_DIT, as `cpu_features` asks for
FEAT_SHA256. a failed read counts as absent, since the caller fails closed

### thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_affinity`](darwin/aarch64.md#thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_affinity`](darwin/x86_64.md#thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

darwin has no hard CPU affinity: THREAD_AFFINITY_POLICY is a scheduling hint
over tags, not a CPU set, so neither affinity primitive is offered

### set_thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.set_thread_affinity`](darwin/aarch64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.set_thread_affinity`](darwin/x86_64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

darwin has no hard CPU affinity, so a thread cannot be pinned

### getcwd

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getcwd`](darwin/aarch64.md#getcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getcwd`](darwin/x86_64.md#getcwd), where `$mach.build.arch == $mach.arch.x86_64`

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

### getcwd_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getcwd`](darwin/aarch64.md#getcwd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getcwd`](darwin/x86_64.md#getcwd), where `$mach.build.arch == $mach.arch.x86_64`

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

### getenv

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getenv`](darwin/aarch64.md#getenv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getenv`](darwin/x86_64.md#getenv), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

### environ

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.environ`](darwin/aarch64.md#environ), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.environ`](darwin/x86_64.md#environ), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### getenv_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.getenv`](darwin/aarch64.md#getenv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.getenv`](darwin/x86_64.md#getenv), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

the environment is the bytes the kernel passed, so its native reads are the reads themselves

### environ_native

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.environ`](darwin/aarch64.md#environ), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.environ`](darwin/x86_64.md#environ), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun environ() **u8
```

pointer to the environment captured by the runtime at program
start (null-terminated array of "NAME=value" strings). nil before
runtime init.

### temp_dir

Forwards [`std.system.os.darwin.shared.temp_dir`](darwin/shared.md#temp_dir).

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

the directory designated for temporary files: $TMPDIR, else "/tmp"

### fork

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.fork`](darwin/aarch64.md#fork), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.fork`](darwin/x86_64.md#fork), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun fork() i64
```

create a child process by duplicating the caller

### vfork

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.vfork`](darwin/aarch64.md#vfork), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.vfork`](darwin/x86_64.md#vfork), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun vfork() i64
```

create a child process through vfork(2)

the wrapper promises the fork contract only; see the libsystem module.

### exec

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.exec`](darwin/aarch64.md#exec), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.exec`](darwin/x86_64.md#exec), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun exec(pathname: *u8, argv: **u8, envp: Environment) i64
```

replace the calling process image; returns only on failure

### wait

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.wait`](darwin/aarch64.md#wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.wait`](darwin/x86_64.md#wait), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

failures and no-event results leave the caller's status unchanged

### wait_pid

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.wait_pid`](darwin/aarch64.md#wait_pid), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.wait_pid`](darwin/x86_64.md#wait_pid), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

wait for a child to change state, as wait does without resource usage

### ProcessStatus

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ProcessStatus`](darwin/aarch64.md#processstatus), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ProcessStatus`](darwin/x86_64.md#processstatus), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.FileLimit`](darwin/aarch64.md#filelimit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.FileLimit`](darwin/x86_64.md#filelimit), where `$mach.build.arch == $mach.arch.x86_64`

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

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.LIMIT_UNLIMITED`](darwin/aarch64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.LIMIT_UNLIMITED`](darwin/x86_64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.open_file_limit`](darwin/aarch64.md#open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.open_file_limit`](darwin/x86_64.md#open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

read this process's open-file limit.

darwin refuses a soft limit above kern.maxfilesperproc even when the hard
limit is RLIM_INFINITY (setrlimit(2) COMPATIBILITY), so the ceiling is the
smaller of the two. this is the rule Go's runtime applies before raising the
limit (os/rlimit_darwin.go)

### set_open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.set_open_file_limit`](darwin/aarch64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.set_open_file_limit`](darwin/x86_64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

set this process's open-file limit. ceiling is ignored, and darwin's own
refusal of a soft limit above its per-process maximum passes through

### ProcessWaitError

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.ProcessWaitError`](darwin/aarch64.md#processwaiterror), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.ProcessWaitError`](darwin/x86_64.md#processwaiterror), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.WaitResult`](darwin/aarch64.md#waitresult), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.WaitResult`](darwin/x86_64.md#waitresult), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_WAIT`](darwin/aarch64.md#process_op_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_WAIT`](darwin/x86_64.md#process_op_wait), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_STATUS`](darwin/aarch64.md#process_op_status), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_STATUS`](darwin/x86_64.md#process_op_status), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_CLOSE`](darwin/aarch64.md#process_op_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_CLOSE`](darwin/x86_64.md#process_op_close), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_SPAWN`](darwin/aarch64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_SPAWN`](darwin/x86_64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_READ`](darwin/aarch64.md#process_op_read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_READ`](darwin/x86_64.md#process_op_read), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_PIPE`](darwin/aarch64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_PIPE`](darwin/x86_64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_OP_TERMINATE`](darwin/aarch64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_OP_TERMINATE`](darwin/x86_64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_EXITED`](darwin/aarch64.md#process_exited), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_EXITED`](darwin/x86_64.md#process_exited), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_SIGNALED`](darwin/aarch64.md#process_signaled), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_SIGNALED`](darwin/x86_64.md#process_signaled), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_STOPPED`](darwin/aarch64.md#process_stopped), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_STOPPED`](darwin/x86_64.md#process_stopped), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.PROCESS_CONTINUED`](darwin/aarch64.md#process_continued), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.PROCESS_CONTINUED`](darwin/x86_64.md#process_continued), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### AF_INET

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.AF_INET`](darwin/aarch64.md#af_inet), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.AF_INET`](darwin/x86_64.md#af_inet), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val AF_INET:             i32 = 2
```

sockets

### AF_INET6

Forwards [`std.system.os.darwin.shared.AF_INET6`](darwin/shared.md#constants).

```mach
pub val AF_INET6:            i32 = 30
```

### SOCK_STREAM

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SOCK_STREAM`](darwin/aarch64.md#sock_stream), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SOCK_STREAM`](darwin/x86_64.md#sock_stream), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SOCK_STREAM:         i32 = 1
```

### SOCK_DGRAM

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SOCK_DGRAM`](darwin/aarch64.md#sock_dgram), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SOCK_DGRAM`](darwin/x86_64.md#sock_dgram), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SOCK_DGRAM:          i32 = 2
```

### SOL_SOCKET

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SOL_SOCKET`](darwin/aarch64.md#sol_socket), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SOL_SOCKET`](darwin/x86_64.md#sol_socket), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SOL_SOCKET:          i32 = 0xFFFF
```

### SO_UNSUPPORTED

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_UNSUPPORTED`](darwin/aarch64.md#so_unsupported), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_UNSUPPORTED`](darwin/x86_64.md#so_unsupported), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

### SO_REUSEADDR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_REUSEADDR`](darwin/aarch64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_REUSEADDR`](darwin/x86_64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_REUSEADDR:        i32 = 4
```

### SO_REUSEPORT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_REUSEPORT`](darwin/aarch64.md#so_reuseport), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_REUSEPORT`](darwin/x86_64.md#so_reuseport), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_REUSEPORT:        i32 = 0x0200
```

### SO_EXCLUSIVEADDRUSE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_EXCLUSIVEADDRUSE`](darwin/aarch64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_EXCLUSIVEADDRUSE`](darwin/x86_64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = SO_UNSUPPORTED
```

### SO_KEEPALIVE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_KEEPALIVE`](darwin/aarch64.md#so_keepalive), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_KEEPALIVE`](darwin/x86_64.md#so_keepalive), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_KEEPALIVE:        i32 = 0x0008
```

### SO_SNDBUF

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_SNDBUF`](darwin/aarch64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_SNDBUF`](darwin/x86_64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_SNDBUF:           i32 = 0x1001
```

### SO_RCVBUF

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_RCVBUF`](darwin/aarch64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_RCVBUF`](darwin/x86_64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_RCVBUF:           i32 = 0x1002
```

### SO_LINGER

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_LINGER`](darwin/aarch64.md#so_linger), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_LINGER`](darwin/x86_64.md#so_linger), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_LINGER:           i32 = 0x0080
```

### SO_RCVTIMEO

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SO_RCVTIMEO`](darwin/aarch64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SO_RCVTIMEO`](darwin/x86_64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SO_RCVTIMEO:         i32 = 0x1006
```

### IPPROTO_IP

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IPPROTO_IP`](darwin/aarch64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IPPROTO_IP`](darwin/x86_64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IPPROTO_IP:          i32 = 0
```

### IPPROTO_TCP

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IPPROTO_TCP`](darwin/aarch64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IPPROTO_TCP`](darwin/x86_64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IPPROTO_TCP:         i32 = 6
```

### IPPROTO_IPV6

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IPPROTO_IPV6`](darwin/aarch64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IPPROTO_IPV6`](darwin/x86_64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IPPROTO_IPV6:        i32 = 41
```

### IP_TOS

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IP_TOS`](darwin/aarch64.md#ip_tos), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IP_TOS`](darwin/x86_64.md#ip_tos), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IP_TOS:              i32 = 1
```

### IPV6_V6ONLY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IPV6_V6ONLY`](darwin/aarch64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IPV6_V6ONLY`](darwin/x86_64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IPV6_V6ONLY:         i32 = 27
```

### IPV6_TCLASS

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IPV6_TCLASS`](darwin/aarch64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IPV6_TCLASS`](darwin/x86_64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IPV6_TCLASS:         i32 = 36
```

### TCP_NODELAY

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.TCP_NODELAY`](darwin/aarch64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.TCP_NODELAY`](darwin/x86_64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val TCP_NODELAY:         i32 = 1
```

### TCP_KEEPIDLE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.TCP_KEEPIDLE`](darwin/aarch64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.TCP_KEEPIDLE`](darwin/x86_64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val TCP_KEEPIDLE:        i32 = 0x10
```

### TCP_KEEPINTVL

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.TCP_KEEPINTVL`](darwin/aarch64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.TCP_KEEPINTVL`](darwin/x86_64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val TCP_KEEPINTVL:       i32 = 0x101
```

### TCP_KEEPCNT

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.TCP_KEEPCNT`](darwin/aarch64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.TCP_KEEPCNT`](darwin/x86_64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val TCP_KEEPCNT:         i32 = 0x102
```

### TCP_FASTOPEN

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.TCP_FASTOPEN`](darwin/aarch64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.TCP_FASTOPEN`](darwin/x86_64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val TCP_FASTOPEN:        i32 = 0x105
```

### SHUT_RD

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SHUT_RD`](darwin/aarch64.md#shut_rd), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SHUT_RD`](darwin/x86_64.md#shut_rd), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SHUT_RD:             i32 = 0
```

### SHUT_WR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SHUT_WR`](darwin/aarch64.md#shut_wr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SHUT_WR`](darwin/x86_64.md#shut_wr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SHUT_WR:             i32 = 1
```

### SHUT_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SHUT_RDWR`](darwin/aarch64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SHUT_RDWR`](darwin/x86_64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SHUT_RDWR:           i32 = 2
```

### SOCKADDR_IN_SIZE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.SOCKADDR_IN_SIZE`](darwin/aarch64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.SOCKADDR_IN_SIZE`](darwin/x86_64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

### SOCKADDR_IN6_SIZE

Forwards [`std.system.os.darwin.shared.SOCKADDR_IN6_SIZE`](darwin/shared.md#constants).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

### SOCKADDR_STORAGE_SIZE

Forwards [`std.system.os.darwin.shared.SOCKADDR_STORAGE_SIZE`](darwin/shared.md#constants).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

### sock_send

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_send`](darwin/aarch64.md#sock_send), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_send`](darwin/x86_64.md#sock_send), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

send bytes on a connected socket through write

### sock_recv

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_recv`](darwin/aarch64.md#sock_recv), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_recv`](darwin/x86_64.md#sock_recv), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

raw native read semantics do not safely discard ancillary descriptor rights.
a darwin peer can send scm_rights that install descriptors without returning them.

### local_stream_recv

Forwards [`std.system.os.darwin.shared.local_stream_recv`](darwin/shared.md#local_stream_recv).

```mach
pub fun local_stream_recv(fd: usize, buffer: *u8, length: usize) i64
```

exclusively borrow the receive queue through peek and consume, including all aliases.
ancillary refusal leaves the socket and its queued rights owned by the caller.

### IoVector

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IoVector`](darwin/aarch64.md#iovector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IoVector`](darwin/x86_64.md#iovector), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.sock_write_vector`](darwin/aarch64.md#sock_write_vector), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_write_vector`](darwin/x86_64.md#sock_write_vector), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_write_vector(fd: usize, vectors: *IoVector, count: usize) i64
```

write a gather list to a socket

### sock_send_message

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_send_message`](darwin/aarch64.md#sock_send_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_send_message`](darwin/x86_64.md#sock_send_message), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_send_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: u32, control: *u8, control_length: usize) i64
```

send a gather list with an optional address and ancillary data

### sock_receive_message

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_receive_message`](darwin/aarch64.md#sock_receive_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_receive_message`](darwin/x86_64.md#sock_receive_message), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_receive_message(fd: usize, vectors: *IoVector, vector_count: usize, address: *u8, address_length: *u32, control: *u8, control_length: *usize, flags: *i32) i64
```

raw recvmsg preserves native ancillary ownership and truncation behavior.
darwin can install unreported scm_rights descriptors with nil or undersized control.
callers receiving rights must provide adequate control storage and close each result.

### sock_set_nonblocking

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_set_nonblocking`](darwin/aarch64.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_set_nonblocking`](darwin/x86_64.md#sock_set_nonblocking), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_set_nonblocking(fd: usize, enabled: bool) i64
```

switch a socket between blocking and nonblocking

### sock_connect_begin

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_connect_begin`](darwin/aarch64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_connect_begin`](darwin/x86_64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

start a connect on a nonblocking socket

### sock_connect_poll

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_connect_poll`](darwin/aarch64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_connect_poll`](darwin/x86_64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

### CONNECT_PENDING

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.CONNECT_PENDING`](darwin/aarch64.md#connect_pending), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.CONNECT_PENDING`](darwin/x86_64.md#connect_pending), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val CONNECT_PENDING: i64 = 1
```

what sock_connect_begin and sock_connect_poll return while the connect is in flight

### sock_close

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_close`](darwin/aarch64.md#sock_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_close`](darwin/x86_64.md#sock_close), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_close(fd: usize) i64
```

close a socket

### sock_create

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_create`](darwin/aarch64.md#sock_create), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_create`](darwin/x86_64.md#sock_create), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

create a blocking, close-on-exec socket

### sock_create_flags

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_create_flags`](darwin/aarch64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_create_flags`](darwin/x86_64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

create a socket with chosen blocking and inheritance

### sock_bind

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_bind`](darwin/aarch64.md#sock_bind), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_bind`](darwin/x86_64.md#sock_bind), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

bind a socket to a local address

### sock_listen

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_listen`](darwin/aarch64.md#sock_listen), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_listen`](darwin/x86_64.md#sock_listen), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

mark a socket as accepting connections

### sock_accept

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_accept`](darwin/aarch64.md#sock_accept), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_accept`](darwin/x86_64.md#sock_accept), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

accept a connection as a blocking, close-on-exec socket

### sock_accept_flags

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_accept_flags`](darwin/aarch64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_accept_flags`](darwin/x86_64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

accept a connection with chosen blocking and inheritance

### sock_connect

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_connect`](darwin/aarch64.md#sock_connect), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_connect`](darwin/x86_64.md#sock_connect), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

connect a socket to a peer

### sock_sendto

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_sendto`](darwin/aarch64.md#sock_sendto), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_sendto`](darwin/x86_64.md#sock_sendto), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

send bytes to an address

### sock_recvfrom

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_recvfrom`](darwin/aarch64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_recvfrom`](darwin/x86_64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

receive bytes with the sender's address

### sock_peek_readable

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_peek_readable`](darwin/aarch64.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_peek_readable`](darwin/x86_64.md#sock_peek_readable), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_peek_readable(fd: usize) i64
```

peek at a stream socket without consuming or blocking

### sock_shutdown

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_shutdown`](darwin/aarch64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_shutdown`](darwin/x86_64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

shut down one or both directions of a socket

### sock_setopt

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_setopt`](darwin/aarch64.md#sock_setopt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_setopt`](darwin/x86_64.md#sock_setopt), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

set a socket option

### sock_getopt

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_getopt`](darwin/aarch64.md#sock_getopt), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_getopt`](darwin/x86_64.md#sock_getopt), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

read a socket option

### sock_local_addr

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_local_addr`](darwin/aarch64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_local_addr`](darwin/x86_64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

read a socket's local address

### sock_remote_addr

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_remote_addr`](darwin/aarch64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_remote_addr`](darwin/x86_64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

read a connected socket's peer address

### sock_inheritable

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_inheritable`](darwin/aarch64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_inheritable`](darwin/x86_64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

whether a child process would inherit a socket

### IoCompletion

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IoCompletion`](darwin/aarch64.md#iocompletion), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IoCompletion`](darwin/x86_64.md#iocompletion), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.IO_EVENT_READ`](darwin/aarch64.md#io_event_read), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IO_EVENT_READ`](darwin/x86_64.md#io_event_read), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IO_EVENT_READ:   u32 = 0x01
```

### IO_EVENT_WRITE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IO_EVENT_WRITE`](darwin/aarch64.md#io_event_write), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IO_EVENT_WRITE`](darwin/x86_64.md#io_event_write), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IO_EVENT_WRITE:  u32 = 0x02
```

### IO_EVENT_ERROR

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IO_EVENT_ERROR`](darwin/aarch64.md#io_event_error), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IO_EVENT_ERROR`](darwin/x86_64.md#io_event_error), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IO_EVENT_ERROR:  u32 = 0x04
```

### IO_EVENT_HANGUP

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IO_EVENT_HANGUP`](darwin/aarch64.md#io_event_hangup), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IO_EVENT_HANGUP`](darwin/x86_64.md#io_event_hangup), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IO_EVENT_HANGUP: u32 = 0x08
```

### IO_EVENT_WAKE

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.IO_EVENT_WAKE`](darwin/aarch64.md#io_event_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.IO_EVENT_WAKE`](darwin/x86_64.md#io_event_wake), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val IO_EVENT_WAKE:   u32 = 0x10
```

### io_queue_create

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_create`](darwin/aarch64.md#io_queue_create), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_create`](darwin/x86_64.md#io_queue_create), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

open a close-on-exec kqueue for queue, with the user event io_queue_wake
posts already registered

### io_queue_wait

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_wait`](darwin/aarch64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_wait`](darwin/x86_64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

wait up to timeout_ms for one completion and discard it

### io_queue_watch

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_watch`](darwin/aarch64.md#io_queue_watch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_watch`](darwin/x86_64.md#io_queue_watch), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_watch(queue: *std.system.os.shared.IoQueue, resource: usize, context: u64, events: u32) i64
```

register one-shot readiness interest in a descriptor

each requested direction gets its own one-shot filter, which fires once until
it is armed again. registering an existing filter updates it

### io_queue_rearm

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_rearm`](darwin/aarch64.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_rearm`](darwin/x86_64.md#io_queue_rearm), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_rearm(queue: *std.system.os.shared.IoQueue, resource: usize, context: u64, events: u32) i64
```

arms again a registration the caller made with io_queue_watch. kqueue's
EV_ADD updates an existing filter, and the kernel drops every filter when the
descriptor closes, so re-arming and registering are the same change

### duplicate_to

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.duplicate_to`](darwin/aarch64.md#duplicate_to), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.duplicate_to`](darwin/x86_64.md#duplicate_to), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun duplicate_to(from: usize, to: usize) i64
```

makes the descriptor to name what from names, closing whatever to named
before, in one step

### io_queue_unwatch

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_unwatch`](darwin/aarch64.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_unwatch`](darwin/x86_64.md#io_queue_unwatch), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_unwatch(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

drop both readiness filters of a descriptor, where one that is not
registered is not an error

### io_queue_poll

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_poll`](darwin/aarch64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_poll`](darwin/x86_64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

collect ready completions, waiting up to timeout_ms

completions is also the native kevent buffer, and each record is rewritten in
place. a wake reports IO_EVENT_WAKE with source 0

### io_queue_wake

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_wake`](darwin/aarch64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_wake`](darwin/x86_64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

wake a thread waiting on queue

only the first request before a poll harvests the wake posts the event, and
later requests in that window return 0 having posted nothing

### io_queue_close

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.io_queue_close`](darwin/aarch64.md#io_queue_close), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.io_queue_close`](darwin/x86_64.md#io_queue_close), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

close the kqueue behind queue, where closing a closed queue returns 0

### sock_set_rcvtimeo

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.sock_set_rcvtimeo`](darwin/aarch64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.sock_set_rcvtimeo`](darwin/x86_64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`

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

### DNS_HOSTS_PATH

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.DNS_HOSTS_PATH`](darwin/aarch64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.DNS_HOSTS_PATH`](darwin/x86_64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub val DNS_HOSTS_PATH: str = "/etc/hosts"
```

dns

### random_fill

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.random_fill`](darwin/aarch64.md#random_fill), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.random_fill`](darwin/x86_64.md#random_fill), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

random

### thread_spawn

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_spawn`](darwin/aarch64.md#thread_spawn), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_spawn`](darwin/x86_64.md#thread_spawn), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.thread_join`](darwin/aarch64.md#thread_join), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_join`](darwin/x86_64.md#thread_join), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

wait for a thread thread_spawn created to end, and release its native handle

### thread_detach

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_detach`](darwin/aarch64.md#thread_detach), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_detach`](darwin/x86_64.md#thread_detach), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_detach(native: usize) i64
```

hand a thread's native teardown to libpthread, so it is never joined

### thread_current_id

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_current_id`](darwin/aarch64.md#thread_current_id), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_current_id`](darwin/x86_64.md#thread_current_id), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_current_id() i64
```

the calling thread's system-wide id

### thread_current_name

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_current_name`](darwin/aarch64.md#thread_current_name), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_current_name`](darwin/x86_64.md#thread_current_name), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

copy the calling thread's name into name, null-terminated

### thread_wait

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_wait`](darwin/aarch64.md#thread_wait), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_wait`](darwin/x86_64.md#thread_wait), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

returns immediately if *addr does not equal expected. spurious wakeups are
possible and are expected: bucket sharing means a wake for a different
address can land here (see the bucket-table note above), so every caller must
re-test its own condition in a loop.

### thread_wait_until

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_wait_until`](darwin/aarch64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_wait_until`](darwin/x86_64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

block until the word changes or an absolute monotonic deadline is reached

### thread_wake

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_wake`](darwin/aarch64.md#thread_wake), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_wake`](darwin/x86_64.md#thread_wake), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_wake(addr: *i64) i64
```

wake threads blocked in thread_wait on addr

broadcasts rather than signals: buckets are shared by address hash, so a
signal could be delivered to a waiter on an unrelated address and the wake
this call was meant to deliver would be lost.

### thread_block

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_block`](darwin/aarch64.md#thread_block), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_block`](darwin/x86_64.md#thread_block), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, read from its pthread TSD without a system call

### thread_block_enter

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.thread_block_enter`](darwin/aarch64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.thread_block_enter`](darwin/x86_64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's

### stack_bounds

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.stack_bounds`](darwin/aarch64.md#stack_bounds), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.stack_bounds`](darwin/x86_64.md#stack_bounds), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, recorded in its block when it was
installed, or asked of libpthread on a thread std did not create

### clock_gettime

Forwards the first of these whose condition holds:

- [`std.system.os.darwin.aarch64.clock_gettime`](darwin/aarch64.md#clock_gettime), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.clock_gettime`](darwin/x86_64.md#clock_gettime), where `$mach.build.arch == $mach.arch.x86_64`

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

- [`std.system.os.darwin.aarch64.error_message`](darwin/aarch64.md#error_message), where `$mach.build.arch == $mach.arch.aarch64`
- [`std.system.os.darwin.x86_64.error_message`](darwin/x86_64.md#error_message), where `$mach.build.arch == $mach.arch.x86_64`

```mach
pub fun error_message(code: i64) str
```

a human-readable message for a negated errno

