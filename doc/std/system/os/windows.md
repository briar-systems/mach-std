[std](../../README.md) / [system](../README.md) / [os](README.md) / **windows**

# std.system.os.windows

windows OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need windows-specific functionality import this module
directly rather than going through std.system.os.

Source: [`src/system/os/windows.mach`](../../../../src/system/os/windows.mach)

| Forwards | |
| :--- | :--- |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`timespec`](#timespec), [`DirectoryCursor`](#directorycursor), [`DirectoryEntry`](#directoryentry), [`NativeEntry`](#nativeentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`separator`](#separator) | path |
| [`STDIN_FD`](#stdin_fd) | constants |
| [`STDOUT_FD`](#stdout_fd), [`STDERR_FD`](#stderr_fd), [`O_RDONLY`](#o_rdonly), [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_DIRECTORY`](#o_directory), [`AT_FDCWD`](#at_fdcwd), [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow), [`AT_REMOVEDIR`](#at_removedir) | |
| [`LOCK_SH`](#lock_sh) | advisory file-lock operations |
| [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un), [`S_IFMT`](#s_ifmt), [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk), [`WNOHANG`](#wnohang), [`WUNTRACED`](#wuntraced), [`WCONTINUED`](#wcontinued), [`CLOCK_REALTIME`](#clock_realtime), [`CLOCK_MONOTONIC`](#clock_monotonic), [`EPERM`](#eperm), [`ENOENT`](#enoent), [`ESRCH`](#esrch), [`EINTR`](#eintr), [`EIO`](#eio), [`ENXIO`](#enxio), [`E2BIG`](#e2big), [`EBADF`](#ebadf), [`ECHILD`](#echild), [`EAGAIN`](#eagain), [`ENOMEM`](#enomem), [`EACCES`](#eacces), [`EFAULT`](#efault), [`EBUSY`](#ebusy), [`EEXIST`](#eexist), [`ENODEV`](#enodev), [`ENOTDIR`](#enotdir), [`EISDIR`](#eisdir), [`EINVAL`](#einval), [`ENFILE`](#enfile), [`EMFILE`](#emfile), [`ETXTBSY`](#etxtbsy), [`ENOSPC`](#enospc), [`EROFS`](#erofs), [`EPIPE`](#epipe), [`ENAMETOOLONG`](#enametoolong), [`ERANGE`](#erange), [`ENOTEMPTY`](#enotempty), [`ELOOP`](#eloop), [`ENOTSUP`](#enotsup), [`EADDRINUSE`](#eaddrinuse), [`ENETUNREACH`](#enetunreach), [`ECONNABORTED`](#econnaborted), [`ECONNRESET`](#econnreset), [`ENOTCONN`](#enotconn), [`ETIMEDOUT`](#etimedout), [`ECONNREFUSED`](#econnrefused), [`EHOSTUNREACH`](#ehostunreach), [`ECANCELED`](#ecanceled), [`ENOTSOCK`](#enotsock), [`EINTR_MAX_RETRIES`](#eintr_max_retries) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size), [`map_file`](#map_file), [`sync_file`](#sync_file), [`unmap_file`](#unmap_file) | |
| [`read`](#read) | filesystem |
| [`write`](#write), [`read_at`](#read_at), [`write_at`](#write_at), [`open`](#open), [`open_native`](#open_native), [`native_path`](#native_path), [`native_path_release`](#native_path_release), [`native_spelling`](#native_spelling), [`confined_path`](#confined_path), [`open_root_utf8`](#open_root_utf8), [`open_root_native`](#open_root_native), [`open_relative_utf8`](#open_relative_utf8), [`open_relative_native`](#open_relative_native), [`make_dir_utf8`](#make_dir_utf8), [`remove_file_utf8`](#remove_file_utf8), [`remove_dir_utf8`](#remove_dir_utf8), [`close`](#close), [`sync_fd`](#sync_fd), [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at), [`set_mode_at_native`](#set_mode_at_native), [`file_identity`](#file_identity), [`identity_at`](#identity_at), [`identity_at_native`](#identity_at_native), [`retain_identity_at`](#retain_identity_at), [`retain_identity_at_native`](#retain_identity_at_native), [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path), [`stat_path_native`](#stat_path_native), [`stat_mode`](#stat_mode), [`unlink`](#unlink), [`unlink_native`](#unlink_native), [`unlink_force`](#unlink_force), [`unlink_force_native`](#unlink_force_native), [`rename`](#rename), [`rename_native`](#rename_native), [`rename_relative_utf8`](#rename_relative_utf8), [`rename_relative_native`](#rename_relative_native), [`symlink`](#symlink), [`symlink_native`](#symlink_native), [`make_dir`](#make_dir), [`make_dir_native`](#make_dir_native), [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_next_native`](#directory_next_native), [`directory_refused_native`](#directory_refused_native), [`directory_dnit`](#directory_dnit), [`access`](#access), [`access_native`](#access_native), [`seek`](#seek), [`lock_fd`](#lock_fd) | |
| [`terminate`](#terminate) | process |
| [`abort`](#abort), [`terminate_child`](#terminate_child), [`terminate_group`](#terminate_group), [`probe_group`](#probe_group), [`spawn`](#spawn), [`spawn_grouped`](#spawn_grouped), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_grouped`](#spawn_redirected_grouped), [`spawn_redirected_in`](#spawn_redirected_in), [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped), [`spawn_native`](#spawn_native), [`spawn_in_native`](#spawn_in_native), [`spawn_redirected_native`](#spawn_redirected_native), [`spawn_redirected_in_native`](#spawn_redirected_in_native), [`spawn_redirected_in_grouped_native`](#spawn_redirected_in_grouped_native), [`spawn_command_line`](#spawn_command_line), [`getpid`](#getpid), [`pipe`](#pipe), [`ignore_sigpipe`](#ignore_sigpipe), [`sleep`](#sleep), [`cpu_count`](#cpu_count), [`cpu_features`](#cpu_features), [`cpu_dit`](#cpu_dit), [`thread_affinity`](#thread_affinity), [`set_thread_affinity`](#set_thread_affinity), [`getcwd`](#getcwd), [`getcwd_native`](#getcwd_native), [`getenv`](#getenv), [`getenv_native`](#getenv_native), [`environment_name_compare`](#environment_name_compare), [`environment_name_compare_native`](#environment_name_compare_native), [`last_error`](#last_error), [`temp_dir`](#temp_dir), [`temp_dir_native`](#temp_dir_native), [`environ_native`](#environ_native), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`AF_INET`](#af_inet) | sockets |
| [`AF_INET6`](#af_inet6), [`SOCK_STREAM`](#sock_stream), [`SOCK_DGRAM`](#sock_dgram), [`SOL_SOCKET`](#sol_socket), [`SO_UNSUPPORTED`](#so_unsupported), [`SO_REUSEADDR`](#so_reuseaddr), [`SO_REUSEPORT`](#so_reuseport), [`SO_EXCLUSIVEADDRUSE`](#so_exclusiveaddruse), [`SO_KEEPALIVE`](#so_keepalive), [`SO_SNDBUF`](#so_sndbuf), [`SO_RCVBUF`](#so_rcvbuf), [`SO_LINGER`](#so_linger), [`SO_RCVTIMEO`](#so_rcvtimeo), [`IPPROTO_IP`](#ipproto_ip), [`IPPROTO_TCP`](#ipproto_tcp), [`IPPROTO_IPV6`](#ipproto_ipv6), [`IP_TOS`](#ip_tos), [`IPV6_V6ONLY`](#ipv6_v6only), [`IPV6_TCLASS`](#ipv6_tclass), [`TCP_NODELAY`](#tcp_nodelay), [`TCP_KEEPIDLE`](#tcp_keepidle), [`TCP_KEEPINTVL`](#tcp_keepintvl), [`TCP_KEEPCNT`](#tcp_keepcnt), [`TCP_FASTOPEN`](#tcp_fastopen), [`SHUT_RD`](#shut_rd), [`SHUT_WR`](#shut_wr), [`SHUT_RDWR`](#shut_rdwr), [`SOCKADDR_IN_SIZE`](#sockaddr_in_size), [`SOCKADDR_IN6_SIZE`](#sockaddr_in6_size), [`SOCKADDR_STORAGE_SIZE`](#sockaddr_storage_size), [`sock_send`](#sock_send), [`sock_recv`](#sock_recv), [`sock_close`](#sock_close), [`sock_create`](#sock_create), [`sock_create_flags`](#sock_create_flags), [`sock_bind`](#sock_bind), [`sock_listen`](#sock_listen), [`sock_accept`](#sock_accept), [`sock_accept_flags`](#sock_accept_flags), [`sock_connect`](#sock_connect), [`sock_sendto`](#sock_sendto), [`sock_recvfrom`](#sock_recvfrom), [`sock_shutdown`](#sock_shutdown), [`sock_setopt`](#sock_setopt), [`sock_getopt`](#sock_getopt), [`sock_local_addr`](#sock_local_addr), [`sock_remote_addr`](#sock_remote_addr), [`sock_inheritable`](#sock_inheritable), [`sock_connect_status`](#sock_connect_status), [`sock_connect_begin`](#sock_connect_begin), [`sock_connect_poll`](#sock_connect_poll), [`CONNECT_PENDING`](#connect_pending), [`local_endpoint_identity`](#local_endpoint_identity), [`local_endpoint_path`](#local_endpoint_path), [`IO_EVENT_READ`](#io_event_read), [`IO_EVENT_WRITE`](#io_event_write), [`IO_EVENT_ERROR`](#io_event_error), [`IO_EVENT_HANGUP`](#io_event_hangup), [`IO_EVENT_WAKE`](#io_event_wake), [`IoCompletion`](#iocompletion), [`io_queue_create`](#io_queue_create), [`io_queue_attach`](#io_queue_attach), [`io_queue_detach`](#io_queue_detach), [`io_queue_poll`](#io_queue_poll), [`io_queue_restore`](#io_queue_restore), [`io_queue_wait`](#io_queue_wait), [`io_queue_wake`](#io_queue_wake), [`io_queue_close`](#io_queue_close), [`io_queue_cancel`](#io_queue_cancel), [`sock_async_accept`](#sock_async_accept), [`sock_async_connect`](#sock_async_connect), [`sock_async_receive`](#sock_async_receive), [`sock_async_send`](#sock_async_send), [`sock_async_receive_message`](#sock_async_receive_message), [`sock_pending_bytes`](#sock_pending_bytes), [`sock_receive_message_ready`](#sock_receive_message_ready), [`sock_async_send_message`](#sock_async_send_message), [`sock_async_result`](#sock_async_result), [`sock_accept_context`](#sock_accept_context), [`sock_connect_context`](#sock_connect_context), [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | |
| [`DNS_HOSTS_PATH`](#dns_hosts_path) | dns |
| [`random_fill`](#random_fill) | random |
| [`thread_spawn`](#thread_spawn) | threads |
| [`thread_join`](#thread_join), [`thread_detach`](#thread_detach), [`thread_current_id`](#thread_current_id), [`thread_current_name`](#thread_current_name), [`thread_wait`](#thread_wait), [`thread_wait_until`](#thread_wait_until), [`thread_wake`](#thread_wake), [`thread_block`](#thread_block), [`thread_block_enter`](#thread_block_enter), [`stack_bounds`](#stack_bounds) | |
| [`running_under_wine`](#running_under_wine) | runtime environment |
| [`clock_gettime`](#clock_gettime) | time |
| [`error_kind`](#error_kind) | errno |
| [`error_message`](#error_message) | |

---

## Forwards

### stat_t

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stat_t`](windows/x86_64.md#stat_t), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stat_t`](windows/aarch64.md#stat_t), where `$mach.build.arch == $mach.arch.aarch64`

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

kernel ABI types

### timespec

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.timespec`](windows/x86_64.md#timespec), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.timespec`](windows/aarch64.md#timespec), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

### DirectoryCursor

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.DirectoryCursor`](windows/x86_64.md#directorycursor), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.DirectoryCursor`](windows/aarch64.md#directorycursor), where `$mach.build.arch == $mach.arch.aarch64`

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

### DirectoryEntry

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.DirectoryEntry`](windows/x86_64.md#directoryentry), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.DirectoryEntry`](windows/aarch64.md#directoryentry), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### NativeEntry

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.NativeEntry`](windows/x86_64.md#nativeentry), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.NativeEntry`](windows/aarch64.md#nativeentry), where `$mach.build.arch == $mach.arch.aarch64`

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

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.DirectoryInitResult`](windows/x86_64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.DirectoryInitResult`](windows/aarch64.md#directoryinitresult), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### separator

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.separator`](windows/x86_64.md#separator), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.separator`](windows/aarch64.md#separator), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val separator: u8 = '\\'
```

path

### STDIN_FD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.STDIN_FD`](windows/x86_64.md#stdin_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.STDIN_FD`](windows/aarch64.md#stdin_fd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val STDIN_FD:  i32 = 0
```

constants

### STDOUT_FD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.STDOUT_FD`](windows/x86_64.md#stdout_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.STDOUT_FD`](windows/aarch64.md#stdout_fd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val STDOUT_FD: i32 = 1
```

### STDERR_FD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.STDERR_FD`](windows/x86_64.md#stderr_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.STDERR_FD`](windows/aarch64.md#stderr_fd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val STDERR_FD: i32 = 2
```

### O_RDONLY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_RDONLY`](windows/x86_64.md#o_rdonly), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_RDONLY`](windows/aarch64.md#o_rdonly), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_RDONLY:    i32 = 0
```

### O_WRONLY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_WRONLY`](windows/x86_64.md#o_wronly), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_WRONLY`](windows/aarch64.md#o_wronly), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_WRONLY:    i32 = 1
```

### O_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_RDWR`](windows/x86_64.md#o_rdwr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_RDWR`](windows/aarch64.md#o_rdwr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_RDWR:      i32 = 2
```

### O_CREAT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_CREAT`](windows/x86_64.md#o_creat), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_CREAT`](windows/aarch64.md#o_creat), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_CREAT:     i32 = 0x100
```

### O_EXCL

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_EXCL`](windows/x86_64.md#o_excl), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_EXCL`](windows/aarch64.md#o_excl), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_EXCL:      i32 = 0x200
```

### O_TRUNC

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_TRUNC`](windows/x86_64.md#o_trunc), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_TRUNC`](windows/aarch64.md#o_trunc), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_TRUNC:     i32 = 0x400
```

### O_APPEND

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_APPEND`](windows/x86_64.md#o_append), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_APPEND`](windows/aarch64.md#o_append), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_APPEND:    i32 = 0x800
```

### O_DIRECTORY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.O_DIRECTORY`](windows/x86_64.md#o_directory), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.O_DIRECTORY`](windows/aarch64.md#o_directory), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val O_DIRECTORY: i32 = 0x10000
```

### AT_FDCWD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.AT_FDCWD`](windows/x86_64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.AT_FDCWD`](windows/aarch64.md#at_fdcwd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val AT_FDCWD:            i32 = -100
```

### AT_SYMLINK_NOFOLLOW

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.AT_SYMLINK_NOFOLLOW`](windows/x86_64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.AT_SYMLINK_NOFOLLOW`](windows/aarch64.md#at_symlink_nofollow), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0100
```

### AT_REMOVEDIR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.AT_REMOVEDIR`](windows/x86_64.md#at_removedir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.AT_REMOVEDIR`](windows/aarch64.md#at_removedir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val AT_REMOVEDIR:        i32 = 0x0200
```

### LOCK_SH

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.LOCK_SH`](windows/x86_64.md#lock_sh), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.LOCK_SH`](windows/aarch64.md#lock_sh), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val LOCK_SH: i32 = 1
```

advisory file-lock operations

### LOCK_EX

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.LOCK_EX`](windows/x86_64.md#lock_ex), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.LOCK_EX`](windows/aarch64.md#lock_ex), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.LOCK_NB`](windows/x86_64.md#lock_nb), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.LOCK_NB`](windows/aarch64.md#lock_nb), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.LOCK_UN`](windows/x86_64.md#lock_un), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.LOCK_UN`](windows/aarch64.md#lock_un), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.S_IFMT`](windows/x86_64.md#s_ifmt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.S_IFMT`](windows/aarch64.md#s_ifmt), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val S_IFMT:  u32 = 0o170000
```

### S_IFDIR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.S_IFDIR`](windows/x86_64.md#s_ifdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.S_IFDIR`](windows/aarch64.md#s_ifdir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.S_IFREG`](windows/x86_64.md#s_ifreg), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.S_IFREG`](windows/aarch64.md#s_ifreg), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.S_IFLNK`](windows/x86_64.md#s_iflnk), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.S_IFLNK`](windows/aarch64.md#s_iflnk), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val S_IFLNK: u32 = 0o120000
```

### WNOHANG

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.WNOHANG`](windows/x86_64.md#wnohang), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.WNOHANG`](windows/aarch64.md#wnohang), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val WNOHANG:    i32 = 1
```

### WUNTRACED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.WUNTRACED`](windows/x86_64.md#wuntraced), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.WUNTRACED`](windows/aarch64.md#wuntraced), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val WUNTRACED:  i32 = 2
```

### WCONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.WCONTINUED`](windows/x86_64.md#wcontinued), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.WCONTINUED`](windows/aarch64.md#wcontinued), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val WCONTINUED: i32 = 8
```

### CLOCK_REALTIME

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.CLOCK_REALTIME`](windows/x86_64.md#clock_realtime), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.CLOCK_REALTIME`](windows/aarch64.md#clock_realtime), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val CLOCK_REALTIME:  i32 = 0
```

### CLOCK_MONOTONIC

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.CLOCK_MONOTONIC`](windows/x86_64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.CLOCK_MONOTONIC`](windows/aarch64.md#clock_monotonic), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val CLOCK_MONOTONIC: i32 = 1
```

### EPERM

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EPERM`](windows/x86_64.md#eperm), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EPERM`](windows/aarch64.md#eperm), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EPERM:        i64 = -1
```

### ENOENT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOENT`](windows/x86_64.md#enoent), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOENT`](windows/aarch64.md#enoent), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOENT:       i64 = -2
```

### ESRCH

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ESRCH`](windows/x86_64.md#esrch), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ESRCH`](windows/aarch64.md#esrch), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ESRCH:        i64 = -3
```

### EINTR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EINTR`](windows/x86_64.md#eintr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EINTR`](windows/aarch64.md#eintr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EINTR:        i64 = -4
```

### EIO

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EIO`](windows/x86_64.md#eio), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EIO`](windows/aarch64.md#eio), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EIO:          i64 = -5
```

### ENXIO

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENXIO`](windows/x86_64.md#enxio), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENXIO`](windows/aarch64.md#enxio), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENXIO:        i64 = -6
```

### E2BIG

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.E2BIG`](windows/x86_64.md#e2big), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.E2BIG`](windows/aarch64.md#e2big), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val E2BIG:        i64 = -7
```

### EBADF

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EBADF`](windows/x86_64.md#ebadf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EBADF`](windows/aarch64.md#ebadf), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EBADF:        i64 = -9
```

### ECHILD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ECHILD`](windows/x86_64.md#echild), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ECHILD`](windows/aarch64.md#echild), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ECHILD:       i64 = -10
```

### EAGAIN

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EAGAIN`](windows/x86_64.md#eagain), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EAGAIN`](windows/aarch64.md#eagain), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EAGAIN:       i64 = -11
```

### ENOMEM

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOMEM`](windows/x86_64.md#enomem), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOMEM`](windows/aarch64.md#enomem), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOMEM:       i64 = -12
```

### EACCES

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EACCES`](windows/x86_64.md#eacces), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EACCES`](windows/aarch64.md#eacces), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EACCES:       i64 = -13
```

### EFAULT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EFAULT`](windows/x86_64.md#efault), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EFAULT`](windows/aarch64.md#efault), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EFAULT:       i64 = -14
```

### EBUSY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EBUSY`](windows/x86_64.md#ebusy), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EBUSY`](windows/aarch64.md#ebusy), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EBUSY:        i64 = -16
```

### EEXIST

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EEXIST`](windows/x86_64.md#eexist), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EEXIST`](windows/aarch64.md#eexist), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EEXIST:       i64 = -17
```

### ENODEV

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENODEV`](windows/x86_64.md#enodev), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENODEV`](windows/aarch64.md#enodev), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENODEV:       i64 = -19
```

### ENOTDIR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOTDIR`](windows/x86_64.md#enotdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOTDIR`](windows/aarch64.md#enotdir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOTDIR:      i64 = -20
```

### EISDIR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EISDIR`](windows/x86_64.md#eisdir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EISDIR`](windows/aarch64.md#eisdir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EISDIR:       i64 = -21
```

### EINVAL

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EINVAL`](windows/x86_64.md#einval), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EINVAL`](windows/aarch64.md#einval), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EINVAL:       i64 = -22
```

### ENFILE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENFILE`](windows/x86_64.md#enfile), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENFILE`](windows/aarch64.md#enfile), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENFILE:       i64 = -23
```

### EMFILE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EMFILE`](windows/x86_64.md#emfile), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EMFILE`](windows/aarch64.md#emfile), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EMFILE:       i64 = -24
```

### ETXTBSY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ETXTBSY`](windows/x86_64.md#etxtbsy), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ETXTBSY`](windows/aarch64.md#etxtbsy), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ETXTBSY:      i64 = -26
```

### ENOSPC

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOSPC`](windows/x86_64.md#enospc), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOSPC`](windows/aarch64.md#enospc), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOSPC:       i64 = -28
```

### EROFS

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EROFS`](windows/x86_64.md#erofs), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EROFS`](windows/aarch64.md#erofs), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EROFS:        i64 = -30
```

### EPIPE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EPIPE`](windows/x86_64.md#epipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EPIPE`](windows/aarch64.md#epipe), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EPIPE:        i64 = -32
```

### ENAMETOOLONG

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENAMETOOLONG`](windows/x86_64.md#enametoolong), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENAMETOOLONG`](windows/aarch64.md#enametoolong), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENAMETOOLONG: i64 = -36
```

### ERANGE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ERANGE`](windows/x86_64.md#erange), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ERANGE`](windows/aarch64.md#erange), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ERANGE:       i64 = -34
```

### ENOTEMPTY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOTEMPTY`](windows/x86_64.md#enotempty), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOTEMPTY`](windows/aarch64.md#enotempty), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOTEMPTY:    i64 = -39
```

### ELOOP

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ELOOP`](windows/x86_64.md#eloop), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ELOOP`](windows/aarch64.md#eloop), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ELOOP:        i64 = -40
```

### ENOTSUP

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ENOTSUP`](windows/x86_64.md#enotsup), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ENOTSUP`](windows/aarch64.md#enotsup), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val ENOTSUP:      i64 = -95
```

### EADDRINUSE

Forwards [`std.system.os.windows.shared.EADDRINUSE`](windows/shared.md#constants).

```mach
pub val EADDRINUSE:    i64 = -98
```

### ENETUNREACH

Forwards [`std.system.os.windows.shared.ENETUNREACH`](windows/shared.md#constants).

```mach
pub val ENETUNREACH:   i64 = -101
```

### ECONNABORTED

Forwards [`std.system.os.windows.shared.ECONNABORTED`](windows/shared.md#constants).

```mach
pub val ECONNABORTED:  i64 = -103
```

### ECONNRESET

Forwards [`std.system.os.windows.shared.ECONNRESET`](windows/shared.md#constants).

```mach
pub val ECONNRESET:    i64 = -104
```

### ENOTCONN

Forwards [`std.system.os.windows.shared.ENOTCONN`](windows/shared.md#constants).

```mach
pub val ENOTCONN:      i64 = -107
```

### ETIMEDOUT

Forwards [`std.system.os.windows.shared.ETIMEDOUT`](windows/shared.md#constants).

```mach
pub val ETIMEDOUT:     i64 = -110
```

### ECONNREFUSED

Forwards [`std.system.os.windows.shared.ECONNREFUSED`](windows/shared.md#constants).

```mach
pub val ECONNREFUSED:  i64 = -111
```

### EHOSTUNREACH

Forwards [`std.system.os.windows.shared.EHOSTUNREACH`](windows/shared.md#constants).

```mach
pub val EHOSTUNREACH:  i64 = -113
```

### ECANCELED

Forwards [`std.system.os.windows.shared.ECANCELED`](windows/shared.md#constants).

```mach
pub val ECANCELED:     i64 = -125
```

### ENOTSOCK

Forwards [`std.system.os.windows.shared.ENOTSOCK`](windows/shared.md#constants).

```mach
pub val ENOTSOCK:      i64 = -88
```

### EINTR_MAX_RETRIES

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.EINTR_MAX_RETRIES`](windows/x86_64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.EINTR_MAX_RETRIES`](windows/aarch64.md#eintr_max_retries), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val EINTR_MAX_RETRIES: usize = 8
```

### allocate

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.allocate`](windows/x86_64.md#allocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.allocate`](windows/aarch64.md#allocate), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.deallocate`](windows/x86_64.md#deallocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.deallocate`](windows/aarch64.md#deallocate), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

### reallocate

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.reallocate`](windows/x86_64.md#reallocate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.reallocate`](windows/aarch64.md#reallocate), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

### heap_region_base

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.heap_region_base`](windows/x86_64.md#heap_region_base), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.heap_region_base`](windows/aarch64.md#heap_region_base), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun heap_region_base() usize
```

### heap_region_extend

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.heap_region_extend`](windows/x86_64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.heap_region_extend`](windows/aarch64.md#heap_region_extend), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun heap_region_extend(addr: usize) usize
```

### protect

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.protect`](windows/x86_64.md#protect), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.protect`](windows/aarch64.md#protect), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

### lock

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.lock`](windows/x86_64.md#lock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.lock`](windows/aarch64.md#lock), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun lock(p: ptr, size: usize) i64
```

### unlock

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unlock`](windows/x86_64.md#unlock), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unlock`](windows/aarch64.md#unlock), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unlock(p: ptr, size: usize) i64
```

### advise

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.advise`](windows/x86_64.md#advise), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.advise`](windows/aarch64.md#advise), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

### page_size

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.page_size`](windows/x86_64.md#page_size), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.page_size`](windows/aarch64.md#page_size), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun page_size() usize
```

### map_file

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.map_file`](windows/x86_64.md#map_file), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.map_file`](windows/aarch64.md#map_file), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

map a file descriptor into memory via CreateFileMapping + MapViewOfFile

### sync_file

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sync_file`](windows/x86_64.md#sync_file), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sync_file`](windows/aarch64.md#sync_file), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via FlushViewOfFile

### unmap_file

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unmap_file`](windows/x86_64.md#unmap_file), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unmap_file`](windows/aarch64.md#unmap_file), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unmap_file(p: ptr, size: usize) i64
```

### read

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.read`](windows/x86_64.md#read), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.read`](windows/aarch64.md#read), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

filesystem

### write

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.write`](windows/x86_64.md#write), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.write`](windows/aarch64.md#write), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

### read_at

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.read_at`](windows/x86_64.md#read_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.read_at`](windows/aarch64.md#read_at), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun read_at(fd: i32, buffer: *u8, count: usize, offset: u64) i64
```

### write_at

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.write_at`](windows/x86_64.md#write_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.write_at`](windows/aarch64.md#write_at), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun write_at(fd: i32, buffer: *u8, count: usize, offset: u64) i64
```

### open

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open`](windows/x86_64.md#open), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open`](windows/aarch64.md#open), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

### open_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_native`](windows/x86_64.md#open_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_native`](windows/aarch64.md#open_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_native(dirfd: i32, path: *u16, flags: i32, mode: i32) i64
```

open a nul-terminated UTF-16 path as given: the units reach the W APIs
unchanged, so a name holding an unpaired surrogate opens what it names

### native_path

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.native_path`](windows/x86_64.md#native_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.native_path`](windows/aarch64.md#native_path), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun native_path(path: *u8, out: *std.system.os.shared.NativePath) i64
```

convert a UTF-8 path once into an owned native path, as every UTF-8
primitive does, for a caller that walks the name itself

### native_path_release

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.native_path_release`](windows/x86_64.md#native_path_release), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.native_path_release`](windows/aarch64.md#native_path_release), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun native_path_release(path: *std.system.os.shared.NativePath)
```

### native_spelling

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.native_spelling`](windows/x86_64.md#native_spelling), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.native_spelling`](windows/aarch64.md#native_spelling), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun native_spelling(name: *u16, length: usize, out: *u8, capacity: usize) i64
```

a name in UTF-16 units spelled in UTF-8 through the one converter, not
terminated: the byte count written, or measured when out is nil, EINVAL for
a name with no UTF-8 spelling, or ERANGE when out is too small

### confined_path

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.confined_path`](windows/x86_64.md#confined_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.confined_path`](windows/aarch64.md#confined_path), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun confined_path(path: *u8, out: *std.system.os.shared.NativePath) i64
```

release what native_path converted
a confined path, walked a component at a time, converted once: a path over
the converter's limit is ENAMETOOLONG, as each of its components would be

### open_root_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_root_utf8`](windows/x86_64.md#open_root_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_root_utf8`](windows/aarch64.md#open_root_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_root_utf8(path: *u8) i64
```

### open_root_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_root_native`](windows/x86_64.md#open_root_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_root_native`](windows/aarch64.md#open_root_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_root_native(path: *u16) i64
```

open a directory by a wide path, resolved by the W API

### open_relative_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_relative_utf8`](windows/x86_64.md#open_relative_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_relative_utf8`](windows/aarch64.md#open_relative_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_relative_utf8(dirfd: i32, path: *u8, path_length: usize, flags: i32, mode: i32) i64
```

open one utf-8 component from a pinned directory descriptor

### open_relative_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_relative_native`](windows/x86_64.md#open_relative_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_relative_native`](windows/aarch64.md#open_relative_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_relative_native(dirfd: i32, name: *u16, name_length: usize, flags: i32, mode: i32) i64
```

open one wide component from a pinned directory descriptor

### make_dir_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.make_dir_utf8`](windows/x86_64.md#make_dir_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.make_dir_utf8`](windows/aarch64.md#make_dir_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun make_dir_utf8(path: *u8) i64
```

### remove_file_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.remove_file_utf8`](windows/x86_64.md#remove_file_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.remove_file_utf8`](windows/aarch64.md#remove_file_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun remove_file_utf8(path: *u8) i64
```

### remove_dir_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.remove_dir_utf8`](windows/x86_64.md#remove_dir_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.remove_dir_utf8`](windows/aarch64.md#remove_dir_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun remove_dir_utf8(path: *u8) i64
```

### close

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.close`](windows/x86_64.md#close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.close`](windows/aarch64.md#close), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun close(fd: i32) i64
```

### sync_fd

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sync_fd`](windows/x86_64.md#sync_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sync_fd`](windows/aarch64.md#sync_fd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sync_fd(fd: i32) i64
```

flush file data or ntfs directory metadata through the pinned object
other windows filesystems cannot certify directory persistence and return enotsup

### stat

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stat`](windows/x86_64.md#stat), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stat`](windows/aarch64.md#stat), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

### set_mode

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.set_mode`](windows/x86_64.md#set_mode), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.set_mode`](windows/aarch64.md#set_mode), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

an owner-only mode is enforced with a protected dacl granting only the
current user, who also becomes the owner. any other mode has no faithful
windows form, since access control has no group or other split, so it
returns ENOTSUP and leaves the object unchanged

### set_mode_at

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.set_mode_at`](windows/x86_64.md#set_mode_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.set_mode_at`](windows/aarch64.md#set_mode_at), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

the same mapping as set_mode, for the object named relative to dirfd. a
reparse point is refused rather than followed

### set_mode_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.set_mode_at_native`](windows/x86_64.md#set_mode_at_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.set_mode_at_native`](windows/aarch64.md#set_mode_at_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun set_mode_at_native(dirfd: i32, name: *u16, mode: i32) i64
```

set_mode_at for a nul-terminated UTF-16 name, the units unchanged

### file_identity

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.file_identity`](windows/x86_64.md#file_identity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.file_identity`](windows/aarch64.md#file_identity), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

### identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.identity_at`](windows/x86_64.md#identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.identity_at`](windows/aarch64.md#identity_at), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.identity_at_native`](windows/x86_64.md#identity_at_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.identity_at_native`](windows/aarch64.md#identity_at_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun identity_at_native(dirfd: i32, path: *u16, out: *std.system.file_identity.Identity) i64
```

identity_at for a nul-terminated UTF-16 name, the units unchanged

### retain_identity_at

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.retain_identity_at`](windows/x86_64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.retain_identity_at`](windows/aarch64.md#retain_identity_at), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

### retain_identity_at_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.retain_identity_at_native`](windows/x86_64.md#retain_identity_at_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.retain_identity_at_native`](windows/aarch64.md#retain_identity_at_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun retain_identity_at_native(dirfd: i32, path: *u16, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

retain_identity_at for a nul-terminated UTF-16 name, the units unchanged

### publication_capabilities

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.publication_capabilities`](windows/x86_64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.publication_capabilities`](windows/aarch64.md#publication_capabilities), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun publication_capabilities(fd: i32) i64
```

### stat_path

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stat_path`](windows/x86_64.md#stat_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stat_path`](windows/aarch64.md#stat_path), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

### stat_path_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stat_path_native`](windows/x86_64.md#stat_path_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stat_path_native`](windows/aarch64.md#stat_path_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun stat_path_native(dirfd: i32, path: *u16, st: *stat_t, flags: i32) i64
```

stat_path for a nul-terminated UTF-16 name, the units unchanged

### stat_mode

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stat_mode`](windows/x86_64.md#stat_mode), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stat_mode`](windows/aarch64.md#stat_mode), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the type/permission bits from a filled stat buffer as a 32-bit word

st_mode is 32-bit in the synthesized windows stat_t; the accessor exists so
portable callers read the mode uniformly across platforms (darwin's is 16-bit).

### unlink

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unlink`](windows/x86_64.md#unlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unlink`](windows/aarch64.md#unlink), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

### unlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unlink_native`](windows/x86_64.md#unlink_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unlink_native`](windows/aarch64.md#unlink_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unlink_native(dirfd: i32, path: *u16, flags: i32) i64
```

remove a nul-terminated UTF-16 path as given, the units unchanged

### unlink_force

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unlink_force`](windows/x86_64.md#unlink_force), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unlink_force`](windows/aarch64.md#unlink_force), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unlink_force(dirfd: i32, path: *u8, flags: i32) i64
```

### unlink_force_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.unlink_force_native`](windows/x86_64.md#unlink_force_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.unlink_force_native`](windows/aarch64.md#unlink_force_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun unlink_force_native(dirfd: i32, path: *u16, flags: i32) i64
```

unlink_force for a nul-terminated UTF-16 name, the units unchanged

### rename

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.rename`](windows/x86_64.md#rename), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.rename`](windows/aarch64.md#rename), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

### rename_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.rename_native`](windows/x86_64.md#rename_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.rename_native`](windows/aarch64.md#rename_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun rename_native(olddir: i32, oldpath: *u16, newdir: i32, newpath: *u16) i64
```

rename for nul-terminated UTF-16 names, the units unchanged

### rename_relative_utf8

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.rename_relative_utf8`](windows/x86_64.md#rename_relative_utf8), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.rename_relative_utf8`](windows/aarch64.md#rename_relative_utf8), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun rename_relative_utf8(olddir: i32, oldpath: *u8, oldpath_length: usize, newdir: i32, newpath: *u8, newpath_length: usize) i64
```

### rename_relative_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.rename_relative_native`](windows/x86_64.md#rename_relative_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.rename_relative_native`](windows/aarch64.md#rename_relative_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun rename_relative_native(olddir: i32, old_name: *u16, old_length: usize, newdir: i32, new_name: *u16, new_length: usize) i64
```

rename one wide component to another between pinned directory descriptors

### symlink

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.symlink`](windows/x86_64.md#symlink), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.symlink`](windows/aarch64.md#symlink), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

relative targets remain relative, with native separators in the reparse data

### symlink_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.symlink_native`](windows/x86_64.md#symlink_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.symlink_native`](windows/aarch64.md#symlink_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun symlink_native(target: *u16, linkpath: *u16) i64
```

symlink for nul-terminated UTF-16 names, the units unchanged. the target is
copied, since its separators are made native in the copy

### make_dir

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.make_dir`](windows/x86_64.md#make_dir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.make_dir`](windows/aarch64.md#make_dir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

### make_dir_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.make_dir_native`](windows/x86_64.md#make_dir_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.make_dir_native`](windows/aarch64.md#make_dir_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun make_dir_native(dirfd: i32, path: *u16, mode: i32) i64
```

make_dir for a nul-terminated UTF-16 name, the units unchanged

### directory_init

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.directory_init`](windows/x86_64.md#directory_init), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.directory_init`](windows/aarch64.md#directory_init), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

fd and its aliases lend exclusive enumeration and seek access until close

### directory_next

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.directory_next`](windows/x86_64.md#directory_next), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.directory_next`](windows/aarch64.md#directory_next), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

the next entry spelled in UTF-8, converted once from the native entry. an
entry with no UTF-8 spelling is refused by itself: the converter's EINVAL,
out untouched, the native name kept for directory_refused_native, and the
next call goes on to the following entry

### directory_next_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.directory_next_native`](windows/x86_64.md#directory_next_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.directory_next_native`](windows/aarch64.md#directory_next_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun directory_next_native(cursor: *DirectoryCursor, out: *NativeEntry) i64
```

the next entry in UTF-16 units as the kernel gives it, so a name holding an
unpaired surrogate is yielded like any other

### directory_refused_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.directory_refused_native`](windows/x86_64.md#directory_refused_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.directory_refused_native`](windows/aarch64.md#directory_refused_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun directory_refused_native(cursor: *DirectoryCursor, out: *NativeEntry) i64
```

the entry the last directory_next refused for having no UTF-8 spelling, in
native units and borrowed like an entry: 1 with out filled, or 0 when the
last call refused nothing

### directory_dnit

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.directory_dnit`](windows/x86_64.md#directory_dnit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.directory_dnit`](windows/aarch64.md#directory_dnit), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

consumes the owner, including when native release reports failure

### access

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.access`](windows/x86_64.md#access), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.access`](windows/aarch64.md#access), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

### access_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.access_native`](windows/x86_64.md#access_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.access_native`](windows/aarch64.md#access_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun access_native(dirfd: i32, path: *u16, mode: i32, flags: i32) i64
```

access for a nul-terminated UTF-16 name, the units unchanged

### seek

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.seek`](windows/x86_64.md#seek), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.seek`](windows/aarch64.md#seek), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

### lock_fd

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.lock_fd`](windows/x86_64.md#lock_fd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.lock_fd`](windows/aarch64.md#lock_fd), where `$mach.build.arch == $mach.arch.aarch64`

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

### terminate

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.terminate`](windows/x86_64.md#terminate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.terminate`](windows/aarch64.md#terminate), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun terminate(code: i64)
```

process

### abort

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.abort`](windows/x86_64.md#abort), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.abort`](windows/aarch64.md#abort), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun abort()
```

### terminate_child

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.terminate_child`](windows/x86_64.md#terminate_child), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.terminate_child`](windows/aarch64.md#terminate_child), where `$mach.build.arch == $mach.arch.aarch64`

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

### terminate_group

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.terminate_group`](windows/x86_64.md#terminate_group), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.terminate_group`](windows/aarch64.md#terminate_group), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun terminate_group(group: i64) i64
```

terminate every process in a group's job without reaping its child

the group token is the child pid, pinned until its retained process handle
closes. reaping the child closes its job and ends every process left in it,
so a group whose child is gone has no process left: ESRCH, as kill gives for
an empty group on posix.

### probe_group

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.probe_group`](windows/x86_64.md#probe_group), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.probe_group`](windows/aarch64.md#probe_group), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun probe_group(group: i64) i64
```

whether any process is left in a group's job

reaping the group's child closes its job, and the job's kill-on-close limit
ends every process left in it, so a group whose child is gone has none left.

### spawn

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn`](windows/x86_64.md#spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn`](windows/aarch64.md#spawn), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

collapses onto spawn_redirected with all three streams inherited.

### spawn_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_grouped`](windows/x86_64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_grouped`](windows/aarch64.md#spawn_grouped), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_grouped(pathname: *u8, argv: **u8, envp: Environment, job_out: *isize) i64
```

create a child process running the given program, placed in its own new
job object (see spawn_redirected_in_grouped)

### spawn_in

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_in`](windows/x86_64.md#spawn_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_in`](windows/aarch64.md#spawn_in), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_redirected

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected`](windows/x86_64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected`](windows/aarch64.md#spawn_redirected), where `$mach.build.arch == $mach.arch.aarch64`

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

### spawn_redirected_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_grouped`](windows/x86_64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_grouped`](windows/aarch64.md#spawn_redirected_grouped), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_redirected_grouped(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32, job_out: *isize) i64
```

spawn a child with its standard streams bound to caller-supplied
descriptors, placed in its own new job object (see
spawn_redirected_in_grouped)

### spawn_redirected_in

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_in`](windows/x86_64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_in`](windows/aarch64.md#spawn_redirected_in), where `$mach.build.arch == $mach.arch.aarch64`

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

### spawn_redirected_in_grouped

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_in_grouped`](windows/x86_64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_in_grouped`](windows/aarch64.md#spawn_redirected_in_grouped), where `$mach.build.arch == $mach.arch.aarch64`

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

### spawn_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_native`](windows/x86_64.md#spawn_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_native`](windows/aarch64.md#spawn_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_native(pathname: *u16, argv: **u16, envp: NativeEnvironment) i64
```

spawn as spawn does, from an executable and arguments in UTF-16

### spawn_in_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_in_native`](windows/x86_64.md#spawn_in_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_in_native`](windows/aarch64.md#spawn_in_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_in_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16) i64
```

spawn as spawn_in does, from an executable, arguments and directory in UTF-16

### spawn_redirected_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_native`](windows/x86_64.md#spawn_redirected_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_native`](windows/aarch64.md#spawn_redirected_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_redirected_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn as spawn_redirected does, from an executable and arguments in UTF-16

### spawn_redirected_in_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_in_native`](windows/x86_64.md#spawn_redirected_in_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_in_native`](windows/aarch64.md#spawn_redirected_in_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_redirected_in_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

spawn as spawn_redirected_in does, from nul-terminated UTF-16 given as is

the executable, the directory and each environment entry reach
CreateProcessW unchanged, and each argument enters the command line unit for
unit under the CRT quoting, so an unpaired surrogate launches, starts in or
reaches the child as it was given

### spawn_redirected_in_grouped_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_redirected_in_grouped_native`](windows/x86_64.md#spawn_redirected_in_grouped_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_redirected_in_grouped_native`](windows/aarch64.md#spawn_redirected_in_grouped_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun spawn_redirected_in_grouped_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32, job_out: *isize) i64
```

spawn as spawn_redirected_in_grouped does, from nul-terminated UTF-16 given as is

### spawn_command_line

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.spawn_command_line`](windows/x86_64.md#spawn_command_line), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.spawn_command_line`](windows/aarch64.md#spawn_command_line), where `$mach.build.arch == $mach.arch.aarch64`

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

### getpid

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.getpid`](windows/x86_64.md#getpid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.getpid`](windows/aarch64.md#getpid), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun getpid() i64
```

return the current process ID

### pipe

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.pipe`](windows/x86_64.md#pipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.pipe`](windows/aarch64.md#pipe), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun pipe(fds: *i32) i64
```

create a unidirectional pipe

### ignore_sigpipe

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ignore_sigpipe`](windows/x86_64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ignore_sigpipe`](windows/aarch64.md#ignore_sigpipe), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

windows does not deliver SIGPIPE for a broken pipe, so this portable surface
is a no-op. writes already report EPIPE through their normal error return.

### sleep

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sleep`](windows/x86_64.md#sleep), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sleep`](windows/aarch64.md#sleep), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

### cpu_count

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.cpu_count`](windows/x86_64.md#cpu_count), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.cpu_count`](windows/aarch64.md#cpu_count), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun cpu_count() i64
```

the number of CPUs available to this process

GetActiveProcessorCount over all processor groups, so machines with more
than 64 logical processors report fully. never returns less than 1.

### cpu_features

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.cpu_features`](windows/x86_64.md#cpu_features), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.cpu_features`](windows/aarch64.md#cpu_features), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

the running processor's instruction-set extensions

x86_64 reads cpuid, which needs no OS. aarch64 asks the kernel, which reports
the armv8 crypto extensions as one feature

### cpu_dit

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.cpu_dit`](windows/x86_64.md#cpu_dit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.cpu_dit`](windows/aarch64.md#cpu_dit), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun cpu_dit() i64
```

windows offers no way to set the data-independent-timing mode

### thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_affinity`](windows/x86_64.md#thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_affinity`](windows/aarch64.md#thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

read the calling thread's CPU affinity, as global CPU indices

CPU i is bit i % 64 of words[i / 64]. out_count covers every active
processor across all groups, and only the thread's own group has bits set.

### set_thread_affinity

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.set_thread_affinity`](windows/x86_64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.set_thread_affinity`](windows/aarch64.md#set_thread_affinity), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

pin the calling thread to the CPUs set in words

every set CPU must lie in one processor group, since a thread's affinity is a
single group's mask. a set spanning groups is refused rather than truncated.

### getcwd

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.getcwd`](windows/x86_64.md#getcwd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.getcwd`](windows/aarch64.md#getcwd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

GetCurrentDirectoryW overloads its return: on success it is the length
written, and when the destination is too small it is the size required
INCLUDING the terminator, with nothing written. Passing both through as a
success let a caller read an untouched buffer and believe it held a path, so
the too-small case is reported as ERANGE the way linux and darwin report it.

### getcwd_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.getcwd_native`](windows/x86_64.md#getcwd_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.getcwd_native`](windows/aarch64.md#getcwd_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun getcwd_native(buf: *u16, size: usize) i64
```

getcwd in UTF-16 units, as the W API gives the path: a directory whose path
holds an unpaired surrogate is reported as it is. size counts units

### getenv

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.getenv`](windows/x86_64.md#getenv), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.getenv`](windows/aarch64.md#getenv), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

### getenv_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.getenv_native`](windows/x86_64.md#getenv_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.getenv_native`](windows/aarch64.md#getenv_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun getenv_native(name: *u16, buf: *u16, cap: usize) i64
```

getenv in UTF-16 units: the value is read with GetEnvironmentVariableW and
not converted, so one holding an unpaired surrogate reads as it is. below
cap it is copied with its terminator, and the full length is always returned

### environment_name_compare

Forwards [`std.system.os.windows.shared.environment_name_compare`](windows/shared.md#environment_name_compare).

```mach
pub fun environment_name_compare(left: *u8, right: *u8, output: *i32) i64
```

compare complete UTF-8 names, each converted once and compared as
environment_name_compare_native compares their units

### environment_name_compare_native

Forwards [`std.system.os.windows.shared.environment_name_compare_native`](windows/shared.md#environment_name_compare_native).

```mach
pub fun environment_name_compare_native(left: *u16, left_units: usize, right: *u16, right_units: usize, output: *i32) i64
```

compare complete names in UTF-16 units as given, with the operating system's
ordinal case table and no conversion, so unpaired surrogates compare as units

### last_error

Forwards [`std.system.os.windows.shared.last_error`](windows/shared.md#last_error).

```mach
pub fun last_error() i64
```

the calling thread's last Win32 error as a negated POSIX errno, for a
consumer that binds a kernel32 call of its own (std.terminal.windows)

### temp_dir

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.temp_dir`](windows/x86_64.md#temp_dir), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.temp_dir`](windows/aarch64.md#temp_dir), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

resolve the directory designated for temporary files

GetTempPathW consults TMP, then TEMP, then USERPROFILE, then the windows
directory, returning the first as a path that ends with a separator. it
follows the getenv truncation contract: ret \< cap means the path was
copied and null-terminated; ret >= cap means the buffer was too small and
ret is the full path length.

### temp_dir_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.temp_dir_native`](windows/x86_64.md#temp_dir_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.temp_dir_native`](windows/aarch64.md#temp_dir_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun temp_dir_native(buf: *u16, cap: usize) i64
```

temp_dir in UTF-16 units, under the same truncation contract with cap in units

### environ_native

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.environ_native`](windows/x86_64.md#environ_native), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.environ_native`](windows/aarch64.md#environ_native), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun environ_native() **u16
```

captures the block once as UTF-16 entries, unconverted, and skips hidden
drive-current-directory names

### wait

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.wait`](windows/x86_64.md#wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.wait`](windows/aarch64.md#wait), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

### wait_pid

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.wait_pid`](windows/x86_64.md#wait_pid), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.wait_pid`](windows/aarch64.md#wait_pid), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

### ProcessStatus

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ProcessStatus`](windows/x86_64.md#processstatus), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ProcessStatus`](windows/aarch64.md#processstatus), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

### FileLimit

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.FileLimit`](windows/x86_64.md#filelimit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.FileLimit`](windows/aarch64.md#filelimit), where `$mach.build.arch == $mach.arch.aarch64`

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

- [`std.system.os.windows.x86_64.LIMIT_UNLIMITED`](windows/x86_64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.LIMIT_UNLIMITED`](windows/aarch64.md#limit_unlimited), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.open_file_limit`](windows/x86_64.md#open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.open_file_limit`](windows/aarch64.md#open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

windows has no settable per-process descriptor limit: handles are bounded by
kernel memory, so neither query nor set has a faithful answer

### set_open_file_limit

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.set_open_file_limit`](windows/x86_64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.set_open_file_limit`](windows/aarch64.md#set_open_file_limit), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

### ProcessWaitError

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.ProcessWaitError`](windows/x86_64.md#processwaiterror), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.ProcessWaitError`](windows/aarch64.md#processwaiterror), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

### WaitResult

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.WaitResult`](windows/x86_64.md#waitresult), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.WaitResult`](windows/aarch64.md#waitresult), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_WAIT`](windows/x86_64.md#process_op_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_WAIT`](windows/aarch64.md#process_op_wait), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_STATUS`](windows/x86_64.md#process_op_status), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_STATUS`](windows/aarch64.md#process_op_status), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_CLOSE`](windows/x86_64.md#process_op_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_CLOSE`](windows/aarch64.md#process_op_close), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_SPAWN`](windows/x86_64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_SPAWN`](windows/aarch64.md#process_op_spawn), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_READ`](windows/x86_64.md#process_op_read), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_READ`](windows/aarch64.md#process_op_read), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_PIPE`](windows/x86_64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_PIPE`](windows/aarch64.md#process_op_pipe), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_OP_TERMINATE`](windows/x86_64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_OP_TERMINATE`](windows/aarch64.md#process_op_terminate), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_EXITED`](windows/x86_64.md#process_exited), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_EXITED`](windows/aarch64.md#process_exited), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_SIGNALED`](windows/x86_64.md#process_signaled), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_SIGNALED`](windows/aarch64.md#process_signaled), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_STOPPED`](windows/x86_64.md#process_stopped), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_STOPPED`](windows/aarch64.md#process_stopped), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.PROCESS_CONTINUED`](windows/x86_64.md#process_continued), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.PROCESS_CONTINUED`](windows/aarch64.md#process_continued), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### AF_INET

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.AF_INET`](windows/x86_64.md#af_inet), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.AF_INET`](windows/aarch64.md#af_inet), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val AF_INET:             i32 = 2
```

sockets

### AF_INET6

Forwards [`std.system.os.windows.shared.AF_INET6`](windows/shared.md#constants).

```mach
pub val AF_INET6:            i32 = 23
```

### SOCK_STREAM

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SOCK_STREAM`](windows/x86_64.md#sock_stream), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SOCK_STREAM`](windows/aarch64.md#sock_stream), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SOCK_STREAM:         i32 = 1
```

### SOCK_DGRAM

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SOCK_DGRAM`](windows/x86_64.md#sock_dgram), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SOCK_DGRAM`](windows/aarch64.md#sock_dgram), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SOCK_DGRAM:          i32 = 2
```

### SOL_SOCKET

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SOL_SOCKET`](windows/x86_64.md#sol_socket), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SOL_SOCKET`](windows/aarch64.md#sol_socket), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SOL_SOCKET:          i32 = 0xFFFF
```

### SO_UNSUPPORTED

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_UNSUPPORTED`](windows/x86_64.md#so_unsupported), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_UNSUPPORTED`](windows/aarch64.md#so_unsupported), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

### SO_REUSEADDR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_REUSEADDR`](windows/x86_64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_REUSEADDR`](windows/aarch64.md#so_reuseaddr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_REUSEADDR:        i32 = 4
```

### SO_REUSEPORT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_REUSEPORT`](windows/x86_64.md#so_reuseport), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_REUSEPORT`](windows/aarch64.md#so_reuseport), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_REUSEPORT:        i32 = SO_UNSUPPORTED
```

### SO_EXCLUSIVEADDRUSE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_EXCLUSIVEADDRUSE`](windows/x86_64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_EXCLUSIVEADDRUSE`](windows/aarch64.md#so_exclusiveaddruse), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = -5
```

### SO_KEEPALIVE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_KEEPALIVE`](windows/x86_64.md#so_keepalive), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_KEEPALIVE`](windows/aarch64.md#so_keepalive), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_KEEPALIVE:        i32 = 8
```

### SO_SNDBUF

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_SNDBUF`](windows/x86_64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_SNDBUF`](windows/aarch64.md#so_sndbuf), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_SNDBUF:           i32 = 0x1001
```

### SO_RCVBUF

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_RCVBUF`](windows/x86_64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_RCVBUF`](windows/aarch64.md#so_rcvbuf), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_RCVBUF:           i32 = 0x1002
```

### SO_LINGER

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_LINGER`](windows/x86_64.md#so_linger), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_LINGER`](windows/aarch64.md#so_linger), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_LINGER:           i32 = 0x0080
```

### SO_RCVTIMEO

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SO_RCVTIMEO`](windows/x86_64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SO_RCVTIMEO`](windows/aarch64.md#so_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SO_RCVTIMEO:         i32 = 0x1006
```

### IPPROTO_IP

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IPPROTO_IP`](windows/x86_64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IPPROTO_IP`](windows/aarch64.md#ipproto_ip), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IPPROTO_IP:          i32 = 0
```

### IPPROTO_TCP

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IPPROTO_TCP`](windows/x86_64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IPPROTO_TCP`](windows/aarch64.md#ipproto_tcp), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IPPROTO_TCP:         i32 = 6
```

### IPPROTO_IPV6

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IPPROTO_IPV6`](windows/x86_64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IPPROTO_IPV6`](windows/aarch64.md#ipproto_ipv6), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IPPROTO_IPV6:        i32 = 41
```

### IP_TOS

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IP_TOS`](windows/x86_64.md#ip_tos), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IP_TOS`](windows/aarch64.md#ip_tos), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IP_TOS:              i32 = 3
```

### IPV6_V6ONLY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IPV6_V6ONLY`](windows/x86_64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IPV6_V6ONLY`](windows/aarch64.md#ipv6_v6only), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IPV6_V6ONLY:         i32 = 27
```

### IPV6_TCLASS

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.IPV6_TCLASS`](windows/x86_64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.IPV6_TCLASS`](windows/aarch64.md#ipv6_tclass), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val IPV6_TCLASS:         i32 = 39
```

### TCP_NODELAY

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.TCP_NODELAY`](windows/x86_64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.TCP_NODELAY`](windows/aarch64.md#tcp_nodelay), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val TCP_NODELAY:         i32 = 1
```

### TCP_KEEPIDLE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.TCP_KEEPIDLE`](windows/x86_64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.TCP_KEEPIDLE`](windows/aarch64.md#tcp_keepidle), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val TCP_KEEPIDLE:        i32 = 3
```

### TCP_KEEPINTVL

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.TCP_KEEPINTVL`](windows/x86_64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.TCP_KEEPINTVL`](windows/aarch64.md#tcp_keepintvl), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val TCP_KEEPINTVL:       i32 = 17
```

### TCP_KEEPCNT

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.TCP_KEEPCNT`](windows/x86_64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.TCP_KEEPCNT`](windows/aarch64.md#tcp_keepcnt), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val TCP_KEEPCNT:         i32 = 16
```

### TCP_FASTOPEN

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.TCP_FASTOPEN`](windows/x86_64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.TCP_FASTOPEN`](windows/aarch64.md#tcp_fastopen), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val TCP_FASTOPEN:        i32 = 15
```

### SHUT_RD

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SHUT_RD`](windows/x86_64.md#shut_rd), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SHUT_RD`](windows/aarch64.md#shut_rd), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SHUT_RD:             i32 = 0
```

### SHUT_WR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SHUT_WR`](windows/x86_64.md#shut_wr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SHUT_WR`](windows/aarch64.md#shut_wr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SHUT_WR:             i32 = 1
```

### SHUT_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SHUT_RDWR`](windows/x86_64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SHUT_RDWR`](windows/aarch64.md#shut_rdwr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SHUT_RDWR:           i32 = 2
```

### SOCKADDR_IN_SIZE

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.SOCKADDR_IN_SIZE`](windows/x86_64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.SOCKADDR_IN_SIZE`](windows/aarch64.md#sockaddr_in_size), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

### SOCKADDR_IN6_SIZE

Forwards [`std.system.os.windows.shared.SOCKADDR_IN6_SIZE`](windows/shared.md#constants).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

### SOCKADDR_STORAGE_SIZE

Forwards [`std.system.os.windows.shared.SOCKADDR_STORAGE_SIZE`](windows/shared.md#constants).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

### sock_send

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_send`](windows/x86_64.md#sock_send), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_send`](windows/aarch64.md#sock_send), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

### sock_recv

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_recv`](windows/x86_64.md#sock_recv), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_recv`](windows/aarch64.md#sock_recv), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

### sock_close

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_close`](windows/x86_64.md#sock_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_close`](windows/aarch64.md#sock_close), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_close(fd: usize) i64
```

### sock_create

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_create`](windows/x86_64.md#sock_create), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_create`](windows/aarch64.md#sock_create), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

### sock_create_flags

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_create_flags`](windows/x86_64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_create_flags`](windows/aarch64.md#sock_create_flags), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_bind

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_bind`](windows/x86_64.md#sock_bind), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_bind`](windows/aarch64.md#sock_bind), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

### sock_listen

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_listen`](windows/x86_64.md#sock_listen), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_listen`](windows/aarch64.md#sock_listen), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

### sock_accept

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_accept`](windows/x86_64.md#sock_accept), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_accept`](windows/aarch64.md#sock_accept), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

### sock_accept_flags

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_accept_flags`](windows/x86_64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_accept_flags`](windows/aarch64.md#sock_accept_flags), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

### sock_connect

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_connect`](windows/x86_64.md#sock_connect), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_connect`](windows/aarch64.md#sock_connect), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

### sock_sendto

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_sendto`](windows/x86_64.md#sock_sendto), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_sendto`](windows/aarch64.md#sock_sendto), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

### sock_recvfrom

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_recvfrom`](windows/x86_64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_recvfrom`](windows/aarch64.md#sock_recvfrom), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

### sock_shutdown

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_shutdown`](windows/x86_64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_shutdown`](windows/aarch64.md#sock_shutdown), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

### sock_setopt

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_setopt`](windows/x86_64.md#sock_setopt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_setopt`](windows/aarch64.md#sock_setopt), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

### sock_getopt

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_getopt`](windows/x86_64.md#sock_getopt), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_getopt`](windows/aarch64.md#sock_getopt), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

### sock_local_addr

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_local_addr`](windows/x86_64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_local_addr`](windows/aarch64.md#sock_local_addr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_remote_addr

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_remote_addr`](windows/x86_64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_remote_addr`](windows/aarch64.md#sock_remote_addr), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

### sock_inheritable

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_inheritable`](windows/x86_64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_inheritable`](windows/aarch64.md#sock_inheritable), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

### sock_connect_status

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_connect_status`](windows/x86_64.md#sock_connect_status), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_connect_status`](windows/aarch64.md#sock_connect_status), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_connect_status(fd: usize) i64
```

a connect's own failure, read from SO_ERROR, or 0 when none is recorded

### sock_connect_begin

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_connect_begin`](windows/x86_64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_connect_begin`](windows/aarch64.md#sock_connect_begin), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

start a connect on a blocking socket without blocking on it

### sock_connect_poll

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_connect_poll`](windows/x86_64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_connect_poll`](windows/aarch64.md#sock_connect_poll), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_connect_poll(fd: usize) i64
```

ask whether a connect sock_connect_begin started has settled, without waiting

SO_CONNECT_TIME reads 0xffffffff until the socket is connected, which is
winsock's own answer: getpeername is not, since a socket can name its peer
before the connect completes

### CONNECT_PENDING

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.CONNECT_PENDING`](windows/x86_64.md#connect_pending), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.CONNECT_PENDING`](windows/aarch64.md#connect_pending), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val CONNECT_PENDING: i64 = 1
```

what sock_connect_begin and sock_connect_poll return while the connect is in flight

### local_endpoint_identity

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.local_endpoint_identity`](windows/x86_64.md#local_endpoint_identity), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.local_endpoint_identity`](windows/aarch64.md#local_endpoint_identity), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun local_endpoint_identity(path: *u8, device: *u64, file: *u64) i64
```

### local_endpoint_path

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.local_endpoint_path`](windows/x86_64.md#local_endpoint_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.local_endpoint_path`](windows/aarch64.md#local_endpoint_path), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun local_endpoint_path(name: *u16, output: *u8, capacity: usize) i64
```

the sun_path bytes of a nul-terminated UTF-16 socket path, converted once.
sun_path is a byte string spelled in UTF-8, as local_endpoint_identity reads
it back, so an unpaired surrogate has no spelling there and is refused here

### IO_EVENT_READ

Forwards [`std.system.os.windows.shared.IO_EVENT_READ`](windows/shared.md#constants).

```mach
pub val IO_EVENT_READ:   u32 = 0x01
```

### IO_EVENT_WRITE

Forwards [`std.system.os.windows.shared.IO_EVENT_WRITE`](windows/shared.md#constants).

```mach
pub val IO_EVENT_WRITE:  u32 = 0x02
```

### IO_EVENT_ERROR

Forwards [`std.system.os.windows.shared.IO_EVENT_ERROR`](windows/shared.md#constants).

```mach
pub val IO_EVENT_ERROR:  u32 = 0x04
```

### IO_EVENT_HANGUP

Forwards [`std.system.os.windows.shared.IO_EVENT_HANGUP`](windows/shared.md#constants).

```mach
pub val IO_EVENT_HANGUP: u32 = 0x08
```

### IO_EVENT_WAKE

Forwards [`std.system.os.windows.shared.IO_EVENT_WAKE`](windows/shared.md#constants).

```mach
pub val IO_EVENT_WAKE:   u32 = 0x10
```

### IoCompletion

Forwards [`std.system.os.windows.shared.IoCompletion`](windows/shared.md#iocompletion).

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

### io_queue_create

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_create`](windows/x86_64.md#io_queue_create), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_create`](windows/aarch64.md#io_queue_create), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_attach

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_attach`](windows/x86_64.md#io_queue_attach), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_attach`](windows/aarch64.md#io_queue_attach), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_attach(queue: *std.system.os.shared.IoQueue, resource: usize, source: u16) i64
```

every completion for resource reports source

### io_queue_detach

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_detach`](windows/x86_64.md#io_queue_detach), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_detach`](windows/aarch64.md#io_queue_detach), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_detach(queue: *std.system.os.shared.IoQueue, resource: usize) i64
```

resource leaves the completion port it is attached to, so another queue can
attach it. the resource must have no request outstanding. windows 8.1 and
later replace a handle's port this way

### io_queue_poll

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_poll`](windows/x86_64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_poll`](windows/aarch64.md#io_queue_poll), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_poll(queue: *std.system.os.shared.IoQueue, completions: *IoCompletion, capacity: usize, timeout_ms: i32) i64
```

context is the stable OVERLAPPED address, flags carries transferred bytes and
source comes from the completion key

### io_queue_restore

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_restore`](windows/x86_64.md#io_queue_restore), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_restore`](windows/aarch64.md#io_queue_restore), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_restore(queue: *std.system.os.shared.IoQueue, completion: IoCompletion) i64
```

move one dequeued packet to the tail without changing its portable status

the net.async backends no longer call this: their cancel is asynchronous, and
restoring foreign packets reorders them behind later ones. its presence is
not a recommendation to drain and restore a shared queue

### io_queue_wait

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_wait`](windows/x86_64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_wait`](windows/aarch64.md#io_queue_wait), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

### io_queue_wake

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_wake`](windows/x86_64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_wake`](windows/aarch64.md#io_queue_wake), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

nil is invalid use and a closed queue is EBADF on every platform

### io_queue_close

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_close`](windows/x86_64.md#io_queue_close), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_close`](windows/aarch64.md#io_queue_close), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

### io_queue_cancel

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.io_queue_cancel`](windows/x86_64.md#io_queue_cancel), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.io_queue_cancel`](windows/aarch64.md#io_queue_cancel), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun io_queue_cancel(resource: usize, overlapped: ptr) i64
```

### sock_async_accept

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_accept`](windows/x86_64.md#sock_async_accept), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_accept`](windows/aarch64.md#sock_async_accept), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_accept(listener: usize, accepted: usize, address: *u8, address_capacity: usize, bytes: *u32, overlapped: ptr) i64
```

### sock_async_connect

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_connect`](windows/x86_64.md#sock_async_connect), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_connect`](windows/aarch64.md#sock_async_connect), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_connect(resource: usize, address: *u8, address_length: usize, bytes: *u32, overlapped: ptr) i64
```

### sock_async_receive

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_receive`](windows/x86_64.md#sock_async_receive), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_receive`](windows/aarch64.md#sock_async_receive), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_receive(resource: usize, buffers: ptr, count: usize, flags: *u32, overlapped: ptr) i64
```

### sock_async_send

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_send`](windows/x86_64.md#sock_async_send), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_send`](windows/aarch64.md#sock_async_send), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_send(resource: usize, buffers: ptr, count: usize, flags: u32, overlapped: ptr) i64
```

### sock_async_receive_message

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_receive_message`](windows/x86_64.md#sock_async_receive_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_receive_message`](windows/aarch64.md#sock_async_receive_message), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_receive_message(resource: usize, message: ptr, overlapped: ptr) i64
```

### sock_pending_bytes

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_pending_bytes`](windows/x86_64.md#sock_pending_bytes), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_pending_bytes`](windows/aarch64.md#sock_pending_bytes), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_pending_bytes(resource: usize, out: *usize) i64
```

the bytes queued for reading on a socket. for a datagram socket a nonzero
count means a datagram is waiting, so a receive would not pend

### sock_receive_message_ready

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_receive_message_ready`](windows/x86_64.md#sock_receive_message_ready), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_receive_message_ready`](windows/aarch64.md#sock_receive_message_ready), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_receive_message_ready(resource: usize, message: ptr, bytes: *u32) i64
```

receive one message now, without an overlapped operation. the caller has
checked that a datagram is queued (sock_pending_bytes), so the call does not
wait

### sock_async_send_message

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_send_message`](windows/x86_64.md#sock_async_send_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_send_message`](windows/aarch64.md#sock_async_send_message), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_send_message(resource: usize, message: ptr, flags: u32, overlapped: ptr) i64
```

### sock_async_result

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_async_result`](windows/x86_64.md#sock_async_result), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_async_result`](windows/aarch64.md#sock_async_result), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_async_result(resource: usize, overlapped: ptr, bytes: *u32, flags: *u32, wait: bool) i64
```

### sock_accept_context

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_accept_context`](windows/x86_64.md#sock_accept_context), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_accept_context`](windows/aarch64.md#sock_accept_context), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_accept_context(accepted: usize, listener: usize) i64
```

### sock_connect_context

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_connect_context`](windows/x86_64.md#sock_connect_context), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_connect_context`](windows/aarch64.md#sock_connect_context), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_connect_context(resource: usize) i64
```

### sock_set_rcvtimeo

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.sock_set_rcvtimeo`](windows/x86_64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.sock_set_rcvtimeo`](windows/aarch64.md#sock_set_rcvtimeo), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

set the receive timeout on a socket

winsock takes SO_RCVTIMEO as a DWORD of milliseconds, not a timeval. ms == 0
clears the timeout, restoring indefinite blocking. once set, a recv with no
data pending fails with WSAETIMEDOUT (mapped to ETIMEDOUT) after the interval.

### DNS_HOSTS_PATH

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.DNS_HOSTS_PATH`](windows/x86_64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.DNS_HOSTS_PATH`](windows/aarch64.md#dns_hosts_path), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub val DNS_HOSTS_PATH: str = "C:/Windows/System32/drivers/etc/hosts"
```

dns

### random_fill

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.random_fill`](windows/x86_64.md#random_fill), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.random_fill`](windows/aarch64.md#random_fill), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

random

### thread_spawn

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_spawn`](windows/x86_64.md#thread_spawn), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_spawn`](windows/aarch64.md#thread_spawn), where `$mach.build.arch == $mach.arch.aarch64`

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

- [`std.system.os.windows.x86_64.thread_join`](windows/x86_64.md#thread_join), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_join`](windows/aarch64.md#thread_join), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

### thread_detach

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_detach`](windows/x86_64.md#thread_detach), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_detach`](windows/aarch64.md#thread_detach), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_detach(native: usize) i64
```

### thread_current_id

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_current_id`](windows/x86_64.md#thread_current_id), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_current_id`](windows/aarch64.md#thread_current_id), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_current_id() i64
```

### thread_current_name

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_current_name`](windows/x86_64.md#thread_current_name), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_current_name`](windows/aarch64.md#thread_current_name), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

### thread_wait

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_wait`](windows/x86_64.md#thread_wait), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_wait`](windows/aarch64.md#thread_wait), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

block until the value at addr changes from expected

wraps WaitOnAddress for 64-bit compare-and-wait. returns immediately
if *addr does not equal expected. spurious wakeups are possible.

### thread_wait_until

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_wait_until`](windows/x86_64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_wait_until`](windows/aarch64.md#thread_wait_until), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

block until the word changes or an absolute monotonic deadline is reached

### thread_wake

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_wake`](windows/x86_64.md#thread_wake), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_wake`](windows/aarch64.md#thread_wake), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_wake(addr: *i64) i64
```

wake one thread blocked on WaitOnAddress at addr

### thread_block

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_block`](windows/x86_64.md#thread_block), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_block`](windows/aarch64.md#thread_block), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

the calling thread's block, read from its TEB without a system call

### thread_block_enter

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.thread_block_enter`](windows/x86_64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.thread_block_enter`](windows/aarch64.md#thread_block_enter), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

install block as the calling thread's

### stack_bounds

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.stack_bounds`](windows/x86_64.md#stack_bounds), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.stack_bounds`](windows/aarch64.md#stack_bounds), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, read from its TEB without a system call

StackBase is the top of the stack and DeallocationStack the base of its
reserve, which the stack commits down toward as it grows, so the bounds hold
for every thread whoever created it. the block records none

### running_under_wine

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.running_under_wine`](windows/x86_64.md#running_under_wine), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.running_under_wine`](windows/aarch64.md#running_under_wine), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun running_under_wine() bool
```

runtime environment

### clock_gettime

Forwards the first of these whose condition holds:

- [`std.system.os.windows.x86_64.clock_gettime`](windows/x86_64.md#clock_gettime), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.clock_gettime`](windows/aarch64.md#clock_gettime), where `$mach.build.arch == $mach.arch.aarch64`

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

- [`std.system.os.windows.x86_64.error_message`](windows/x86_64.md#error_message), where `$mach.build.arch == $mach.arch.x86_64`
- [`std.system.os.windows.aarch64.error_message`](windows/aarch64.md#error_message), where `$mach.build.arch == $mach.arch.aarch64`

```mach
pub fun error_message(code: i64) str
```

