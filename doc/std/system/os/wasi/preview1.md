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

Uses types from [`std.system.file_identity`](../../file_identity.md), [`std.system.os.shared`](../shared.md).

| Type | | |
| :--- | :--- | :--- |
| [`stat_t`](#stat_t) | `rec` | the attributes of a file as the contract's consumers read them |
| [`timespec`](#timespec) | `rec` | time specification with seconds and nanoseconds |
| [`DirectoryCursor`](#directorycursor) | `rec` | an open enumeration of one directory descriptor's entries |

| On `stat_t` | |
| :--- | :--- |
| [`stat`](#stat) | get file status by file descriptor |
| [`stat_path`](#stat_path) | get file status of a path, an absolute or AT_FDCWD path resolved onto a preopen |
| [`stat_mode`](#stat_mode) | read the mode word from a filled stat buffer, the file type alone here |
| [`stat_birth`](#stat_birth) | the birth time of a stat record, which preview1 filestat does not carry |

| On `timespec` | |
| :--- | :--- |
| [`clock_gettime`](#clock_gettime) | get time from a clock source |

| On `DirectoryCursor` | |
| :--- | :--- |
| [`directory_init`](#directory_init) | start enumerating a directory descriptor |
| [`directory_next`](#directory_next) | read the next entry of a directory |
| [`directory_dnit`](#directory_dnit) | end an enumeration and release the cursor's buffer |

| Functions | |
| :--- | :--- |
| [`read`](#read) | read bytes from a file descriptor |
| [`write`](#write) | write bytes to a file descriptor |
| [`write_vector`](#write_vector) | write several buffers to a file descriptor in order, in one call |
| [`read_at`](#read_at) | read bytes at a file offset without moving the descriptor offset |
| [`write_at`](#write_at) | write bytes at a file offset without moving the descriptor offset |
| [`open`](#open) | open a path, the rights asked for cut to what its directory may pass on |
| [`close`](#close) | close a file descriptor |
| [`sync_fd`](#sync_fd) | the preview syncs files, and a host may refuse a directory, which is the host not supporting it rather than a bad descriptor |
| [`access`](#access) | check that a path exists, as the preview has no permission bits to test mode against |
| [`set_mode`](#set_mode) | the preview has no permission bits, so setting them always fails |
| [`set_mode_at`](#set_mode_at) | the preview has no permission bits, so setting them always fails |
| [`file_identity`](#file_identity) | the identity of the file a descriptor names, retaining nothing after the call |
| [`identity_at`](#identity_at) | the identity of the entry path names, without following a final symlink |
| [`retain_identity_at`](#retain_identity_at) | a handle that only names a file does not exist here, so metadata alone is ENOTSUP |
| [`publication_capabilities`](#publication_capabilities) | no file claims without advisory locks |
| [`unlink`](#unlink) | remove a file or directory, an absolute or AT_FDCWD path resolved onto a preopen |
| [`rename`](#rename) | rename a file, an absolute or AT_FDCWD path resolved onto a preopen |
| [`symlink`](#symlink) | create a symbolic link at linkpath pointing to target |
| [`make_dir`](#make_dir) | create a directory, an absolute or AT_FDCWD path resolved onto a preopen |
| [`seek`](#seek) | a directory has no position here: each cursor reads from cookie zero, so rewinding one moves nothing and any other seek on it is unsupported |
| [`lock_fd`](#lock_fd) | the preview has no advisory locks, so locking always fails |
| [`pipe`](#pipe) | the preview cannot create pipes, so this always fails |
| [`map_file`](#map_file) | the preview cannot map files, so this always fails |
| [`sync_file`](#sync_file) | the preview cannot map files, so there is no mapping to flush |
| [`getcwd`](#getcwd) | the preview has one directory the program starts in, the root |
| [`capture_process`](#capture_process) | take the arguments and the environment from the host, before main |
| [`arguments`](#arguments) | the program's arguments capture_process read |
| [`argument_total`](#argument_total) | how many arguments capture_process read |
| [`environ`](#environ) | the environment capture_process read |
| [`getenv`](#getenv) | look up an environment variable by name |
| [`temp_dir`](#temp_dir) | the directory designated for temporary files: $TMPDIR, else "/tmp" |
| [`terminate`](#terminate) | exit the process with the given code |
| [`abort`](#abort) | abort the process immediately with exit code 255 |
| [`getpid`](#getpid) | the preview runs one process and knows no other |
| [`terminate_child`](#terminate_child) | the preview has no child processes, so this always fails |
| [`spawn`](#spawn) | the preview cannot start processes, so this always fails |
| [`spawn_in`](#spawn_in) | the preview cannot start processes, so this always fails |
| [`spawn_redirected`](#spawn_redirected) | the preview cannot start processes, so this always fails |
| [`spawn_redirected_in`](#spawn_redirected_in) | the preview cannot start processes, so this always fails |
| [`wait`](#wait) | the preview has no child processes, so waiting always fails |
| [`wait_pid`](#wait_pid) | the preview has no child processes, so waiting always fails |
| [`ignore_sigpipe`](#ignore_sigpipe) | the preview delivers no signals, so there is nothing to ignore |
| [`open_file_limit`](#open_file_limit) | the preview states no open-file limit, so reading it always fails |
| [`set_open_file_limit`](#set_open_file_limit) | the preview states no open-file limit, so setting it always fails |
| [`random_fill`](#random_fill) | fill a buffer with cryptographic random bytes from the host |
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

get file status by file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `st` | pointer to stat_t to fill |
| **returns** | 0 on success, or a negative native code |

### stat_path

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

get file status of a path, an absolute or AT_FDCWD path resolved onto a preopen

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `st` | pointer to stat_t to fill |
| `flags` | AT_SYMLINK_NOFOLLOW to stat a final symlink itself |
| **returns** | 0 on success, ENOENT for a path under no preopen, or a negative native code |

### stat_mode

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the mode word from a filled stat buffer, the file type alone here

| Parameter | |
| :--- | :--- |
| `st` | pointer to a filled stat_t |
| **returns** | the mode bits |

### stat_birth

```mach
pub fun stat_birth(st: *stat_t, sec: *i64, nsec: *i64) bool
```

the birth time of a stat record, which preview1 filestat does not carry

| Parameter | |
| :--- | :--- |
| `st` | pointer to a filled stat_t |
| `sec` | left unwritten |
| `nsec` | left unwritten |
| **returns** | false |

## timespec

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

| Field | Type | |
| :--- | :--- | :--- |
| `tv_sec` | `i64` | whole seconds |
| `tv_nsec` | `i64` | nanoseconds within the second |

### clock_gettime

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

get time from a clock source

| Parameter | |
| :--- | :--- |
| `clock_id` | clock to query (CLOCK_REALTIME, CLOCK_MONOTONIC) |
| `ts` | pointer to timespec to fill, untouched on failure |
| **returns** | 0 on success, or a negative native code |

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

an open enumeration of one directory descriptor's entries

| Field | Type | |
| :--- | :--- | :--- |
| `address` | `usize` | the cursor's own address, set by directory_init, so a moved or uninitialized cursor is refused |
| `fd` | `i32` | the directory descriptor being enumerated |
| `active` | `bool` | whether directory_init succeeded and directory_dnit has not run |
| `ended` | `bool` | whether the host reported the end of the directory |
| `error` | `i64` | the native code of the failure that stopped enumeration, kept and returned by every later directory_next |
| `buffer` | `ptr` | DIRECTORY_BUFFER_SIZE bytes owned by the cursor, entries in the first half and the yielded name in the second |
| `offset` | `usize` | the byte offset of the next unread entry in buffer |
| `count` | `usize` | the bytes the last fd_readdir filled |
| `cookie` | `u64` | where the next fd_readdir resumes |

### directory_init

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

start enumerating a directory descriptor

| Parameter | |
| :--- | :--- |
| `out` | the cursor, zeroed or one directory_dnit closed |
| `fd` | an open directory descriptor, lent to the cursor until directory_dnit |
| **returns** | a zero code, or EINVAL for a cursor in use, ENOTDIR, ENOMEM or a native code |

### directory_next

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

read the next entry of a directory

the entry's name is borrowed from the cursor's buffer until the next cursor
operation. a failure is kept, so every later call returns it again

| Parameter | |
| :--- | :--- |
| `cursor` | a cursor directory_init made active |
| `out` | receives the entry, untouched unless 1 is returned |
| **returns** | 1 for an entry, 0 at the end, EINVAL for an inactive or moved cursor, ENAMETOOLONG for an entry that does not fit the buffer, or a native code |

### directory_dnit

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

end an enumeration and release the cursor's buffer

| Parameter | |
| :--- | :--- |
| `cursor` | a cursor directory_init opened, or one already ended |
| **returns** | 0, EINVAL for a cursor never opened or since moved, or the code of a failed release |

## Functions

### read

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

read bytes from a file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | destination buffer |
| `count` | maximum bytes to read |
| **returns** | bytes read, or a negative native code |

### write

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | source buffer |
| `count` | bytes to write |
| **returns** | bytes written, or a negative native code |

### write_vector

```mach
pub fun write_vector(fd: i32, vectors: *std.system.os.shared.IoVector, count: usize) i64
```

write several buffers to a file descriptor in order, in one call

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `vectors` | the buffers, in order |
| `count` | number of buffers |
| **returns** | bytes written, which may stop short of the whole, or a negative native code |

### read_at

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

read bytes at a file offset without moving the descriptor offset

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | destination buffer |
| `count` | maximum bytes to read |
| `offset` | file offset to read at |
| **returns** | bytes read, or a negative native code |

### write_at

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

write bytes at a file offset without moving the descriptor offset

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `buf` | source buffer |
| `count` | bytes to write |
| `offset` | file offset to write at |
| **returns** | bytes written, or a negative native code |

### open

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path, the rights asked for cut to what its directory may pass on

### close

```mach
pub fun close(fd: i32) i64
```

close a file descriptor

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| **returns** | 0 on success, or a negative native code |

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

check that a path exists, as the preview has no permission bits to test mode against

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `mode` | access mode flags, ignored |
| `flags` | AT_SYMLINK_NOFOLLOW to check a final symlink itself |
| **returns** | 0 when the path exists, or a negative native code |

### set_mode

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

the preview has no permission bits, so setting them always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### set_mode_at

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

the preview has no permission bits, so setting them always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### file_identity

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

the identity of the file a descriptor names, retaining nothing after the call

| Parameter | |
| :--- | :--- |
| `fd` | file descriptor |
| `out` | receives the identity, untouched on failure |
| **returns** | 0 on success, or a negative native code |

### identity_at

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the entry path names, without following a final symlink

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `out` | receives the identity, untouched on failure |
| **returns** | 0 on success, or a negative native code |

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

remove a file or directory, an absolute or AT_FDCWD path resolved onto a preopen

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `flags` | AT_REMOVEDIR to remove a directory |
| **returns** | 0 on success, or a negative native code |

### rename

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

rename a file, an absolute or AT_FDCWD path resolved onto a preopen

| Parameter | |
| :--- | :--- |
| `olddir` | source directory fd (or AT_FDCWD) |
| `oldpath` | source path |
| `newdir` | destination directory fd (or AT_FDCWD) |
| `newpath` | destination path |
| **returns** | 0 on success, or a negative native code |

### symlink

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

| Parameter | |
| :--- | :--- |
| `target` | path the link points to, stored as given |
| `linkpath` | path of the link to create, resolved onto a preopen |
| **returns** | 0 on success, or a negative native code |

### make_dir

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

create a directory, an absolute or AT_FDCWD path resolved onto a preopen

| Parameter | |
| :--- | :--- |
| `dirfd` | directory fd (or AT_FDCWD) |
| `path` | null-terminated path |
| `mode` | permission bits, ignored as the preview has none |
| **returns** | 0 on success, or a negative native code |

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

the preview has no advisory locks, so locking always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### pipe

```mach
pub fun pipe(fds: *i32) i64
```

the preview cannot create pipes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### map_file

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

the preview cannot map files, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | nil |

### sync_file

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

the preview cannot map files, so there is no mapping to flush

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

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

the program's arguments capture_process read

| Parameter | |
| :--- | :--- |
| **returns** | a nil-terminated array of nul-terminated arguments, nil before capture |

### argument_total

```mach
pub fun argument_total() usize
```

how many arguments capture_process read

| Parameter | |
| :--- | :--- |
| **returns** | the argument count, 0 before capture |

### environ

```mach
pub fun environ() **u8
```

the environment capture_process read

| Parameter | |
| :--- | :--- |
| **returns** | a nil-terminated array of NAME=value entries, nil before capture |

### getenv

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation.

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

### terminate

```mach
pub fun terminate(code: i64)
```

exit the process with the given code

| Parameter | |
| :--- | :--- |
| `code` | exit code, passed to the host as a u32 |

### abort

```mach
pub fun abort()
```

abort the process immediately with exit code 255

### getpid

```mach
pub fun getpid() i64
```

the preview runs one process and knows no other

### terminate_child

```mach
pub fun terminate_child(pid: i64) i64
```

the preview has no child processes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### spawn

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

the preview cannot start processes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### spawn_in

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

the preview cannot start processes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### spawn_redirected

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### wait

```mach
pub fun wait(pid: i64, status: *ProcessStatus, options: i32, rusage: *u8) WaitResult
```

the preview has no child processes, so waiting always fails

| Parameter | |
| :--- | :--- |
| **returns** | a zero pid with an ENOTSUP error naming PROCESS_OP_WAIT |

### wait_pid

```mach
pub fun wait_pid(pid: i64, status: *ProcessStatus, options: i32) WaitResult
```

the preview has no child processes, so waiting always fails

| Parameter | |
| :--- | :--- |
| **returns** | a zero pid with an ENOTSUP error naming PROCESS_OP_WAIT |

### ignore_sigpipe

```mach
pub fun ignore_sigpipe() i64
```

the preview delivers no signals, so there is nothing to ignore

| Parameter | |
| :--- | :--- |
| **returns** | 0 |

### open_file_limit

```mach
pub fun open_file_limit(out: *FileLimit) i64
```

the preview states no open-file limit, so reading it always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### set_open_file_limit

```mach
pub fun set_open_file_limit(limit: FileLimit) i64
```

the preview states no open-file limit, so setting it always fails

| Parameter | |
| :--- | :--- |
| **returns** | ENOTSUP |

### random_fill

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

fill a buffer with cryptographic random bytes from the host

| Parameter | |
| :--- | :--- |
| `buf` | destination buffer |
| `len` | number of bytes to fill |
| **returns** | 0 on success, or a negative native code |

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

one observed change in a child's state

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

why a process wait or the release of a child's handle failed

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

