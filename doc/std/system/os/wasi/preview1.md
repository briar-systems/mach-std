[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [wasi](README.md) / **preview1**

# std.system.os.wasi.preview1

the os contract over wasi preview 1

every import below resolves from wasi_snapshot_preview1, the module the
target's environment names. a call answers with an errno and writes its
results through pointers.

the preview has no working directory and no absolute paths: a path is always
relative to a directory descriptor, and the host hands the program a set of
preopened directories at known names. an absolute path, or a relative one
against AT_FDCWD, which behaves as the root, is taken onto the preopen that
holds its longest leading part. a preopen named "." or "/" holds everything
no longer one does. a path under no preopen is ENOENT.

threads, the io queue, sockets and cpu features are groups this row does not
claim, so nothing here names them. everything the process group claims and
the preview cannot do answers ENOTSUP: there is no spawn, wait, pid or
open-file limit, and locks, modes and file mappings stop there too.

Source: [`src/system/os/wasi/preview1.mach`](../../../../../src/system/os/wasi/preview1.mach)

Uses types from [`std.system.file_identity`](../../file_identity.md).

| Type | | |
| :--- | :--- | :--- |
| [`stat_t`](#stat_t) | `rec` | the attributes of a file as the contract's consumers read them |
| [`timespec`](#timespec) | `rec` |  |
| [`DirectoryCursor`](#directorycursor) | `rec` |  |

| On `stat_t` | |
| :--- | :--- |
| [`stat`](#stat), [`stat_path`](#stat_path), [`stat_mode`](#stat_mode) | |

| On `timespec` | |
| :--- | :--- |
| [`clock_gettime`](#clock_gettime) | |

| On `DirectoryCursor` | |
| :--- | :--- |
| [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_dnit`](#directory_dnit) | |

| Functions | |
| :--- | :--- |
| [`read`](#read), [`write`](#write), [`read_at`](#read_at), [`write_at`](#write_at) | |
| [`open`](#open) | open a path, the rights asked for cut to what its directory may pass on |
| [`close`](#close) | |
| [`sync_fd`](#sync_fd) | the preview syncs files, and a host may refuse a directory, which is the host not supporting it rather than a bad descriptor |
| [`access`](#access), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at), [`file_identity`](#file_identity), [`identity_at`](#identity_at) | |
| [`retain_identity_at`](#retain_identity_at) | a handle that only names a file does not exist here, so metadata alone is ENOTSUP |
| [`publication_capabilities`](#publication_capabilities) | no file claims without advisory locks |
| [`unlink`](#unlink), [`rename`](#rename), [`symlink`](#symlink), [`make_dir`](#make_dir) | |
| [`seek`](#seek) | a directory has no position here: each cursor reads from cookie zero, so rewinding one moves nothing and any other seek on it is unsupported |
| [`lock_fd`](#lock_fd), [`pipe`](#pipe), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`getcwd`](#getcwd) | the preview has one directory the program starts in, the root |
| [`capture_process`](#capture_process) | take the arguments and the environment from the host, before main |
| [`arguments`](#arguments), [`argument_total`](#argument_total), [`environ`](#environ), [`getenv`](#getenv), [`terminate`](#terminate), [`abort`](#abort) | |
| [`getpid`](#getpid) | the preview runs one process and knows no other |
| [`terminate_child`](#terminate_child), [`spawn`](#spawn), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_in`](#spawn_redirected_in), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ignore_sigpipe`](#ignore_sigpipe), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`random_fill`](#random_fill) | |
| [`sleep`](#sleep) | block the one thread for nsec nanoseconds |
| [`stack_bounds`](#stack_bounds) | linear memory holds its stack with no bound the module can read |

| Forwards | |
| :--- | :--- |
| [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`Environment`](#environment), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |

---

## stat_t

```mach
pub rec stat_t {
    st_dev:        u64;
    st_ino:        u64;
    st_mode:       u32;
    st_nlink:      u64;
    st_size:       i64;
    st_atime:      i64;
    st_atime_nsec: i64;
    st_mtime:      i64;
    st_mtime_nsec: i64;
    st_ctime:      i64;
    st_ctime_nsec: i64;
}
```

the attributes of a file as the contract's consumers read them

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
    address: usize;
    fd:      i32;
    active:  bool;
    ended:   bool;
    error:   i64;
    buffer:  ptr;
    offset:  usize;
    count:   usize;
    cookie:  u64;
}
```

### directory_init

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

### directory_next

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

### directory_dnit

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

## Functions

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

### write_at

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

### open

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path, the rights asked for cut to what its directory may pass on

### close

```mach
pub fun close(fd: i32) i64
```

### sync_fd

```mach
pub fun sync_fd(fd: i32) i64
```

the preview syncs files, and a host may refuse a directory, which is the host
not supporting it rather than a bad descriptor

### access

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

### set_mode

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

### set_mode_at

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

### file_identity

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

### identity_at

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

### retain_identity_at

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

a handle that only names a file does not exist here, so metadata alone is ENOTSUP

### publication_capabilities

```mach
pub fun publication_capabilities(fd: i32) i64
```

no file claims without advisory locks

### unlink

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

### rename

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

### symlink

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

### make_dir

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

### seek

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

a directory has no position here: each cursor reads from cookie zero, so
rewinding one moves nothing and any other seek on it is unsupported

### lock_fd

```mach
pub fun lock_fd(fd: i32, op: i32) i64
```

### pipe

```mach
pub fun pipe(fds: *i32) i64
```

### map_file

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

### sync_file

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

### getcwd

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

the preview has one directory the program starts in, the root

### capture_process

```mach
pub fun capture_process() bool
```

take the arguments and the environment from the host, before main

| Parameter | |
| :--- | :--- |
| **returns** | whether they were read |

### arguments

```mach
pub fun arguments() **u8
```

### argument_total

```mach
pub fun argument_total() usize
```

### environ

```mach
pub fun environ() **u8
```

### getenv

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

### terminate

```mach
pub fun terminate(code: i64)
```

### abort

```mach
pub fun abort()
```

### getpid

```mach
pub fun getpid() i64
```

the preview runs one process and knows no other

### terminate_child

```mach
pub fun terminate_child(pid: i64) i64
```

### spawn

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

### spawn_in

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

### spawn_redirected

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

### wait

```mach
pub fun wait(pid: i64, status: *ProcessStatus, options: i32, rusage: *u8) WaitResult
```

### wait_pid

```mach
pub fun wait_pid(pid: i64, status: *ProcessStatus, options: i32) WaitResult
```

### ignore_sigpipe

```mach
pub fun ignore_sigpipe() i64
```

### open_file_limit

```mach
pub fun open_file_limit(out: *FileLimit) i64
```

### set_open_file_limit

```mach
pub fun set_open_file_limit(limit: FileLimit) i64
```

### random_fill

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

### sleep

```mach
pub fun sleep(nsec: i64)
```

block the one thread for nsec nanoseconds

### stack_bounds

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

linear memory holds its stack with no bound the module can read

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

### Environment

Forwards [`std.system.os.shared.Environment`](../shared.md#environment).

```mach
pub def Environment: EnvironmentOf[u8]
```

the environment of a UTF-8 spawn, its entries in UTF-8

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

