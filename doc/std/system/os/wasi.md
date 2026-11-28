[std](../../README.md) / [system](../README.md) / [os](README.md) / **wasi**

# std.system.os.wasi

wasi OS interface with one implementation per preview

forwards the complete surface of the selected row. mach names one environment
of the wasi system, preview1, so one row is selected here, and a later preview
is its own module beside std.system.os.wasi.preview1 exporting this surface,
selected on this line and given its capability row in std.system.capability.

Source: [`src/system/os/wasi.mach`](../../../../src/system/os/wasi.mach)

| Forwards | |
| :--- | :--- |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`timespec`](#timespec), [`DirectoryCursor`](#directorycursor), [`DirectoryEntry`](#directoryentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`separator`](#separator) | path |
| [`STDIN_FD`](#stdin_fd) | constants |
| [`STDOUT_FD`](#stdout_fd), [`STDERR_FD`](#stderr_fd), [`O_RDONLY`](#o_rdonly), [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_NONBLOCK`](#o_nonblock), [`O_DIRECTORY`](#o_directory), [`O_NOFOLLOW`](#o_nofollow), [`AT_FDCWD`](#at_fdcwd), [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow), [`AT_REMOVEDIR`](#at_removedir), [`LOCK_SH`](#lock_sh), [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un), [`S_IFMT`](#s_ifmt), [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk), [`WNOHANG`](#wnohang), [`CLOCK_REALTIME`](#clock_realtime), [`CLOCK_MONOTONIC`](#clock_monotonic), [`EPERM`](#eperm), [`ENOENT`](#enoent), [`ESRCH`](#esrch), [`EINTR`](#eintr), [`EIO`](#eio), [`ENXIO`](#enxio), [`E2BIG`](#e2big), [`EBADF`](#ebadf), [`ECHILD`](#echild), [`EAGAIN`](#eagain), [`ENOMEM`](#enomem), [`EACCES`](#eacces), [`EFAULT`](#efault), [`EBUSY`](#ebusy), [`EEXIST`](#eexist), [`ENODEV`](#enodev), [`ENOTDIR`](#enotdir), [`EISDIR`](#eisdir), [`EINVAL`](#einval), [`ENFILE`](#enfile), [`EMFILE`](#emfile), [`ETXTBSY`](#etxtbsy), [`ENOSPC`](#enospc), [`EROFS`](#erofs), [`EPIPE`](#epipe), [`ENAMETOOLONG`](#enametoolong), [`ERANGE`](#erange), [`ENOTEMPTY`](#enotempty), [`ELOOP`](#eloop), [`ENOTSUP`](#enotsup), [`ETIMEDOUT`](#etimedout) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate), [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size), [`map_alignment`](#map_alignment), [`map_file`](#map_file), [`sync_file`](#sync_file) | |
| [`read`](#read) | files |
| [`write`](#write), [`write_vector`](#write_vector), [`read_at`](#read_at), [`write_at`](#write_at), [`open`](#open), [`open_native`](#open_native), [`close`](#close), [`sync_fd`](#sync_fd), [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at), [`set_mode_at_native`](#set_mode_at_native), [`file_identity`](#file_identity), [`identity_at`](#identity_at), [`identity_at_native`](#identity_at_native), [`retain_identity_at`](#retain_identity_at), [`retain_identity_at_native`](#retain_identity_at_native), [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path), [`stat_path_native`](#stat_path_native), [`stat_mode`](#stat_mode), [`stat_birth`](#stat_birth), [`unlink`](#unlink), [`unlink_native`](#unlink_native), [`rename`](#rename), [`rename_native`](#rename_native), [`symlink`](#symlink), [`symlink_native`](#symlink_native), [`make_dir`](#make_dir), [`make_dir_native`](#make_dir_native), [`directory_init`](#directory_init), [`directory_next`](#directory_next), [`directory_dnit`](#directory_dnit), [`access`](#access), [`access_native`](#access_native), [`seek`](#seek), [`lock_fd`](#lock_fd), [`pipe`](#pipe), [`getcwd`](#getcwd), [`getcwd_native`](#getcwd_native) | |
| [`capture_process`](#capture_process) | process |
| [`arguments`](#arguments), [`argument_total`](#argument_total), [`terminate`](#terminate), [`abort`](#abort), [`terminate_child`](#terminate_child), [`spawn`](#spawn), [`spawn_in`](#spawn_in), [`spawn_redirected`](#spawn_redirected), [`spawn_redirected_in`](#spawn_redirected_in), [`spawn_native`](#spawn_native), [`spawn_in_native`](#spawn_in_native), [`spawn_redirected_native`](#spawn_redirected_native), [`spawn_redirected_in_native`](#spawn_redirected_in_native), [`getpid`](#getpid), [`ignore_sigpipe`](#ignore_sigpipe), [`getenv`](#getenv), [`environ`](#environ), [`getenv_native`](#getenv_native), [`environ_native`](#environ_native), [`temp_dir`](#temp_dir), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`MemoryLimit`](#memorylimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`locked_memory_limit`](#locked_memory_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`sleep`](#sleep) | time and entropy |
| [`clock_gettime`](#clock_gettime), [`random_fill`](#random_fill) | |
| [`stack_bounds`](#stack_bounds) | core |
| [`error_kind`](#error_kind), [`error_message`](#error_message) | |

---

## Forwards

### stat_t

Forwards [`std.system.os.wasi.preview1.stat_t`](wasi/preview1.md#stat_t), only where `$mach.build.sys == $mach.sys.wasi`.

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

kernel ABI types

### timespec

Forwards [`std.system.os.wasi.preview1.timespec`](wasi/preview1.md#timespec), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec timespec {
    tv_sec:  i64;
    tv_nsec: i64;
}
```

time specification with seconds and nanoseconds

### DirectoryCursor

Forwards [`std.system.os.wasi.preview1.DirectoryCursor`](wasi/preview1.md#directorycursor), only where `$mach.build.sys == $mach.sys.wasi`.

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

### DirectoryEntry

Forwards [`std.system.os.wasi.preview1.DirectoryEntry`](wasi/preview1.md#directoryentry), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### DirectoryInitResult

Forwards [`std.system.os.wasi.preview1.DirectoryInitResult`](wasi/preview1.md#directoryinitresult), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### separator

Forwards [`std.system.os.wasi.shared.separator`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val separator: u8 = '/'
```

path

### STDIN_FD

Forwards [`std.system.os.wasi.shared.STDIN_FD`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val STDIN_FD:  i32 = 0
```

constants

### STDOUT_FD

Forwards [`std.system.os.wasi.shared.STDOUT_FD`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val STDOUT_FD: i32 = 1
```

### STDERR_FD

Forwards [`std.system.os.wasi.shared.STDERR_FD`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val STDERR_FD: i32 = 2
```

### O_RDONLY

Forwards [`std.system.os.wasi.shared.O_RDONLY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_RDONLY:    i32 = 0
```

### O_WRONLY

Forwards [`std.system.os.wasi.shared.O_WRONLY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_WRONLY:    i32 = 1
```

### O_RDWR

Forwards [`std.system.os.wasi.shared.O_RDWR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_RDWR:      i32 = 2
```

### O_CREAT

Forwards [`std.system.os.wasi.shared.O_CREAT`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_CREAT:     i32 = 64
```

### O_EXCL

Forwards [`std.system.os.wasi.shared.O_EXCL`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_EXCL:      i32 = 128
```

### O_TRUNC

Forwards [`std.system.os.wasi.shared.O_TRUNC`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_TRUNC:     i32 = 512
```

### O_APPEND

Forwards [`std.system.os.wasi.shared.O_APPEND`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_APPEND:    i32 = 1024
```

### O_NONBLOCK

Forwards [`std.system.os.wasi.shared.O_NONBLOCK`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_NONBLOCK:  i32 = 0o4000
```

### O_DIRECTORY

Forwards [`std.system.os.wasi.shared.O_DIRECTORY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_DIRECTORY: i32 = 0o200000
```

### O_NOFOLLOW

Forwards [`std.system.os.wasi.shared.O_NOFOLLOW`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val O_NOFOLLOW:  i32 = 0o400000
```

### AT_FDCWD

Forwards [`std.system.os.wasi.shared.AT_FDCWD`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val AT_FDCWD:            i32 = -100
```

the preview has no working directory, so this names the root the preopens hang off

### AT_SYMLINK_NOFOLLOW

Forwards [`std.system.os.wasi.shared.AT_SYMLINK_NOFOLLOW`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x100
```

### AT_REMOVEDIR

Forwards [`std.system.os.wasi.shared.AT_REMOVEDIR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val AT_REMOVEDIR:        i32 = 0x200
```

### LOCK_SH

Forwards [`std.system.os.wasi.shared.LOCK_SH`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val LOCK_SH: i32 = 1
```

### LOCK_EX

Forwards [`std.system.os.wasi.shared.LOCK_EX`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards [`std.system.os.wasi.shared.LOCK_NB`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards [`std.system.os.wasi.shared.LOCK_UN`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards [`std.system.os.wasi.shared.S_IFMT`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val S_IFMT:  u32 = 0o170000
```

### S_IFDIR

Forwards [`std.system.os.wasi.shared.S_IFDIR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards [`std.system.os.wasi.shared.S_IFREG`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards [`std.system.os.wasi.shared.S_IFLNK`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val S_IFLNK: u32 = 0o120000
```

### WNOHANG

Forwards [`std.system.os.wasi.shared.WNOHANG`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val WNOHANG:    i32 = 1
```

### CLOCK_REALTIME

Forwards [`std.system.os.wasi.shared.CLOCK_REALTIME`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val CLOCK_REALTIME:  i32 = 0
```

### CLOCK_MONOTONIC

Forwards [`std.system.os.wasi.shared.CLOCK_MONOTONIC`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val CLOCK_MONOTONIC: i32 = 1
```

### EPERM

Forwards [`std.system.os.wasi.shared.EPERM`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EPERM:        i64 = -63
```

### ENOENT

Forwards [`std.system.os.wasi.shared.ENOENT`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOENT:       i64 = -44
```

### ESRCH

Forwards [`std.system.os.wasi.shared.ESRCH`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ESRCH:        i64 = -71
```

### EINTR

Forwards [`std.system.os.wasi.shared.EINTR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EINTR:        i64 = -27
```

### EIO

Forwards [`std.system.os.wasi.shared.EIO`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EIO:          i64 = -29
```

### ENXIO

Forwards [`std.system.os.wasi.shared.ENXIO`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENXIO:        i64 = -60
```

### E2BIG

Forwards [`std.system.os.wasi.shared.E2BIG`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val E2BIG:        i64 = -1
```

### EBADF

Forwards [`std.system.os.wasi.shared.EBADF`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EBADF:        i64 = -8
```

### ECHILD

Forwards [`std.system.os.wasi.shared.ECHILD`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ECHILD:       i64 = -12
```

### EAGAIN

Forwards [`std.system.os.wasi.shared.EAGAIN`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EAGAIN:       i64 = -6
```

### ENOMEM

Forwards [`std.system.os.wasi.shared.ENOMEM`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOMEM:       i64 = -48
```

### EACCES

Forwards [`std.system.os.wasi.shared.EACCES`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EACCES:       i64 = -2
```

### EFAULT

Forwards [`std.system.os.wasi.shared.EFAULT`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EFAULT:       i64 = -21
```

### EBUSY

Forwards [`std.system.os.wasi.shared.EBUSY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EBUSY:        i64 = -10
```

### EEXIST

Forwards [`std.system.os.wasi.shared.EEXIST`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EEXIST:       i64 = -20
```

### ENODEV

Forwards [`std.system.os.wasi.shared.ENODEV`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENODEV:       i64 = -43
```

### ENOTDIR

Forwards [`std.system.os.wasi.shared.ENOTDIR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOTDIR:      i64 = -54
```

### EISDIR

Forwards [`std.system.os.wasi.shared.EISDIR`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EISDIR:       i64 = -31
```

### EINVAL

Forwards [`std.system.os.wasi.shared.EINVAL`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EINVAL:       i64 = -28
```

### ENFILE

Forwards [`std.system.os.wasi.shared.ENFILE`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENFILE:       i64 = -41
```

### EMFILE

Forwards [`std.system.os.wasi.shared.EMFILE`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EMFILE:       i64 = -33
```

### ETXTBSY

Forwards [`std.system.os.wasi.shared.ETXTBSY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ETXTBSY:      i64 = -74
```

### ENOSPC

Forwards [`std.system.os.wasi.shared.ENOSPC`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOSPC:       i64 = -51
```

### EROFS

Forwards [`std.system.os.wasi.shared.EROFS`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EROFS:        i64 = -69
```

### EPIPE

Forwards [`std.system.os.wasi.shared.EPIPE`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val EPIPE:        i64 = -64
```

### ENAMETOOLONG

Forwards [`std.system.os.wasi.shared.ENAMETOOLONG`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENAMETOOLONG: i64 = -37
```

### ERANGE

Forwards [`std.system.os.wasi.shared.ERANGE`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ERANGE:       i64 = -68
```

### ENOTEMPTY

Forwards [`std.system.os.wasi.shared.ENOTEMPTY`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOTEMPTY:    i64 = -55
```

### ELOOP

Forwards [`std.system.os.wasi.shared.ELOOP`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ELOOP:        i64 = -32
```

### ENOTSUP

Forwards [`std.system.os.wasi.shared.ENOTSUP`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ENOTSUP:      i64 = -58
```

### ETIMEDOUT

Forwards [`std.system.os.wasi.shared.ETIMEDOUT`](wasi/shared.md#constants), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val ETIMEDOUT:    i64 = -73
```

### allocate

Forwards [`std.system.os.wasi.shared.allocate`](wasi/shared.md#allocate), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards [`std.system.os.wasi.shared.deallocate`](wasi/shared.md#deallocate), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

keep pages for the next allocate, merged with their neighbours

### reallocate

Forwards [`std.system.os.wasi.shared.reallocate`](wasi/shared.md#reallocate), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a page allocation, in place when its pages still hold it

### heap_region_base

Forwards [`std.system.os.wasi.shared.heap_region_base`](wasi/shared.md#heap_region_base), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun heap_region_base() usize
```

the first address past what has been handed out

### heap_region_extend

Forwards [`std.system.os.wasi.shared.heap_region_extend`](wasi/shared.md#heap_region_extend), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun heap_region_extend(addr: usize) usize
```

move the region's end up to addr

the region is contiguous: it takes kept pages that start where it ends, then
new memory once it reaches the end of linear memory, so it stops growing
while pages `allocate` handed out lie past it

### protect

Forwards [`std.system.os.wasi.shared.protect`](wasi/shared.md#protect), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

linear memory has one protection, every page readable and writable

### lock

Forwards [`std.system.os.wasi.shared.lock`](wasi/shared.md#lock), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun lock(p: ptr, size: usize) i64
```

linear memory cannot be locked, so locking a region always fails

### unlock

Forwards [`std.system.os.wasi.shared.unlock`](wasi/shared.md#unlock), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun unlock(p: ptr, size: usize) i64
```

linear memory cannot be locked, so unlocking a region always fails

### advise

Forwards [`std.system.os.wasi.shared.advise`](wasi/shared.md#advise), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

linear memory takes no access advice, so advising always fails

### page_size

Forwards [`std.system.os.wasi.shared.page_size`](wasi/shared.md#page_size), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun page_size() usize
```

the wasm page size, 64 KiB, which every allocation here is counted in

### map_alignment

Forwards [`std.system.os.wasi.shared.map_alignment`](wasi/shared.md#map_alignment), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun map_alignment() usize
```

the alignment map_file requires of an offset, the wasm page size

### map_file

Forwards [`std.system.os.wasi.preview1.map_file`](wasi/preview1.md#map_file), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun map_file(fd: i32, offset: usize, size: usize, prot: u32) ptr
```

the preview cannot map files, so this always fails

### sync_file

Forwards [`std.system.os.wasi.preview1.sync_file`](wasi/preview1.md#sync_file), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

the preview cannot map files, so there is no mapping to flush

### read

Forwards [`std.system.os.wasi.preview1.read`](wasi/preview1.md#read), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun read(fd: i32, buf: *u8, count: usize) i64
```

files

### write

Forwards [`std.system.os.wasi.preview1.write`](wasi/preview1.md#write), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun write(fd: i32, buf: *u8, count: usize) i64
```

write bytes to a file descriptor

### write_vector

Forwards [`std.system.os.wasi.preview1.write_vector`](wasi/preview1.md#write_vector), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun write_vector(fd: i32, vectors: *std.system.os.shared.IoVector, count: usize) i64
```

write several buffers to a file descriptor in order, in one call

### read_at

Forwards [`std.system.os.wasi.preview1.read_at`](wasi/preview1.md#read_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun read_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

read bytes at a file offset without moving the descriptor offset

### write_at

Forwards [`std.system.os.wasi.preview1.write_at`](wasi/preview1.md#write_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun write_at(fd: i32, buf: *u8, count: usize, offset: u64) i64
```

write bytes at a file offset without moving the descriptor offset

### open

Forwards [`std.system.os.wasi.preview1.open`](wasi/preview1.md#open), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path, the rights asked for cut to what its directory may pass on

### open_native

Forwards [`std.system.os.wasi.preview1.open`](wasi/preview1.md#open), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64
```

open a path, the rights asked for cut to what its directory may pass on

### close

Forwards [`std.system.os.wasi.preview1.close`](wasi/preview1.md#close), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun close(fd: i32) i64
```

close a file descriptor

### sync_fd

Forwards [`std.system.os.wasi.preview1.sync_fd`](wasi/preview1.md#sync_fd), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun sync_fd(fd: i32) i64
```

the preview syncs files, and a host may refuse a directory, which is the host
not supporting it rather than a bad descriptor

### stat

Forwards [`std.system.os.wasi.preview1.stat`](wasi/preview1.md#stat), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stat(fd: i32, st: *stat_t) i64
```

get file status by file descriptor

### set_mode

Forwards [`std.system.os.wasi.preview1.set_mode`](wasi/preview1.md#set_mode), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun set_mode(fd: i32, mode: i32) i64
```

the preview has no permission bits, so setting them always fails

### set_mode_at

Forwards [`std.system.os.wasi.preview1.set_mode_at`](wasi/preview1.md#set_mode_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

the preview has no permission bits, so setting them always fails

### set_mode_at_native

Forwards [`std.system.os.wasi.preview1.set_mode_at`](wasi/preview1.md#set_mode_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun set_mode_at(dirfd: i32, name: *u8, mode: i32) i64
```

the preview has no permission bits, so setting them always fails

### file_identity

Forwards [`std.system.os.wasi.preview1.file_identity`](wasi/preview1.md#file_identity), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun file_identity(fd: i32, out: *std.system.file_identity.Identity) i64
```

the identity of the file a descriptor names, retaining nothing after the call

### identity_at

Forwards [`std.system.os.wasi.preview1.identity_at`](wasi/preview1.md#identity_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the entry path names, without following a final symlink

### identity_at_native

Forwards [`std.system.os.wasi.preview1.identity_at`](wasi/preview1.md#identity_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun identity_at(dirfd: i32, path: *u8, out: *std.system.file_identity.Identity) i64
```

the identity of the entry path names, without following a final symlink

### retain_identity_at

Forwards [`std.system.os.wasi.preview1.retain_identity_at`](wasi/preview1.md#retain_identity_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

a handle that only names a file does not exist here, so metadata alone is ENOTSUP

### retain_identity_at_native

Forwards [`std.system.os.wasi.preview1.retain_identity_at`](wasi/preview1.md#retain_identity_at), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun retain_identity_at(dirfd: i32, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity) i64
```

a handle that only names a file does not exist here, so metadata alone is ENOTSUP

### publication_capabilities

Forwards [`std.system.os.wasi.preview1.publication_capabilities`](wasi/preview1.md#publication_capabilities), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun publication_capabilities(fd: i32) i64
```

no file claims without advisory locks

### stat_path

Forwards [`std.system.os.wasi.preview1.stat_path`](wasi/preview1.md#stat_path), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

get file status of a path, an absolute or AT_FDCWD path resolved onto a preopen

### stat_path_native

Forwards [`std.system.os.wasi.preview1.stat_path`](wasi/preview1.md#stat_path), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stat_path(dirfd: i32, path: *u8, st: *stat_t, flags: i32) i64
```

get file status of a path, an absolute or AT_FDCWD path resolved onto a preopen

### stat_mode

Forwards [`std.system.os.wasi.preview1.stat_mode`](wasi/preview1.md#stat_mode), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stat_mode(st: *stat_t) u32
```

read the mode word from a filled stat buffer, the file type alone here

### stat_birth

Forwards [`std.system.os.wasi.preview1.stat_birth`](wasi/preview1.md#stat_birth), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stat_birth(st: *stat_t, sec: *i64, nsec: *i64) bool
```

the birth time of a stat record, which preview1 filestat does not carry

### unlink

Forwards [`std.system.os.wasi.preview1.unlink`](wasi/preview1.md#unlink), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

remove a file or directory, an absolute or AT_FDCWD path resolved onto a preopen

### unlink_native

Forwards [`std.system.os.wasi.preview1.unlink`](wasi/preview1.md#unlink), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun unlink(dirfd: i32, path: *u8, flags: i32) i64
```

remove a file or directory, an absolute or AT_FDCWD path resolved onto a preopen

### rename

Forwards [`std.system.os.wasi.preview1.rename`](wasi/preview1.md#rename), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

rename a file, an absolute or AT_FDCWD path resolved onto a preopen

### rename_native

Forwards [`std.system.os.wasi.preview1.rename`](wasi/preview1.md#rename), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64
```

rename a file, an absolute or AT_FDCWD path resolved onto a preopen

### symlink

Forwards [`std.system.os.wasi.preview1.symlink`](wasi/preview1.md#symlink), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

### symlink_native

Forwards [`std.system.os.wasi.preview1.symlink`](wasi/preview1.md#symlink), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

### make_dir

Forwards [`std.system.os.wasi.preview1.make_dir`](wasi/preview1.md#make_dir), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

create a directory, an absolute or AT_FDCWD path resolved onto a preopen

### make_dir_native

Forwards [`std.system.os.wasi.preview1.make_dir`](wasi/preview1.md#make_dir), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun make_dir(dirfd: i32, path: *u8, mode: i32) i64
```

create a directory, an absolute or AT_FDCWD path resolved onto a preopen

### directory_init

Forwards [`std.system.os.wasi.preview1.directory_init`](wasi/preview1.md#directory_init), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun directory_init(out: *DirectoryCursor, fd: i32) DirectoryInitResult
```

start enumerating a directory descriptor

### directory_next

Forwards [`std.system.os.wasi.preview1.directory_next`](wasi/preview1.md#directory_next), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

read the next entry of a directory

the entry's name is borrowed from the cursor's buffer until the next cursor
operation. a failure is kept, so every later call returns it again

### directory_dnit

Forwards [`std.system.os.wasi.preview1.directory_dnit`](wasi/preview1.md#directory_dnit), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

end an enumeration and release the cursor's buffer

### access

Forwards [`std.system.os.wasi.preview1.access`](wasi/preview1.md#access), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

check that a path exists, as the preview has no permission bits to test mode against

### access_native

Forwards [`std.system.os.wasi.preview1.access`](wasi/preview1.md#access), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun access(dirfd: i32, path: *u8, mode: i32, flags: i32) i64
```

check that a path exists, as the preview has no permission bits to test mode against

### seek

Forwards [`std.system.os.wasi.preview1.seek`](wasi/preview1.md#seek), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun seek(fd: i32, offset: i64, whence: i32) i64
```

a directory has no position here: each cursor reads from cookie zero, so
rewinding one moves nothing and any other seek on it is unsupported

### lock_fd

Forwards [`std.system.os.wasi.preview1.lock_fd`](wasi/preview1.md#lock_fd), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun lock_fd(fd: i32, op: i32) i64
```

the preview has no advisory locks, so locking always fails

### pipe

Forwards [`std.system.os.wasi.preview1.pipe`](wasi/preview1.md#pipe), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun pipe(fds: *i32) i64
```

the preview cannot create pipes, so this always fails

### getcwd

Forwards [`std.system.os.wasi.preview1.getcwd`](wasi/preview1.md#getcwd), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

the preview has one directory the program starts in, the root

### getcwd_native

Forwards [`std.system.os.wasi.preview1.getcwd`](wasi/preview1.md#getcwd), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

the preview has one directory the program starts in, the root

### capture_process

Forwards [`std.system.os.wasi.preview1.capture_process`](wasi/preview1.md#capture_process), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun capture_process() bool
```

process

### arguments

Forwards [`std.system.os.wasi.preview1.arguments`](wasi/preview1.md#arguments), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun arguments() **u8
```

the program's arguments

### argument_total

Forwards [`std.system.os.wasi.preview1.argument_total`](wasi/preview1.md#argument_total), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun argument_total() usize
```

how many arguments the program has

### terminate

Forwards [`std.system.os.wasi.preview1.terminate`](wasi/preview1.md#terminate), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
#[noreturn]
pub fun terminate(code: i64)
```

exit the process with the given code

### abort

Forwards [`std.system.os.wasi.preview1.abort`](wasi/preview1.md#abort), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
#[noreturn]
pub fun abort()
```

abort the process immediately with exit code 255

### terminate_child

Forwards [`std.system.os.wasi.preview1.terminate_child`](wasi/preview1.md#terminate_child), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun terminate_child(pid: i64) i64
```

the preview has no child processes, so this always fails

### spawn

Forwards [`std.system.os.wasi.preview1.spawn`](wasi/preview1.md#spawn), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

the preview cannot start processes, so this always fails

### spawn_in

Forwards [`std.system.os.wasi.preview1.spawn_in`](wasi/preview1.md#spawn_in), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

the preview cannot start processes, so this always fails

### spawn_redirected

Forwards [`std.system.os.wasi.preview1.spawn_redirected`](wasi/preview1.md#spawn_redirected), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

### spawn_redirected_in

Forwards [`std.system.os.wasi.preview1.spawn_redirected_in`](wasi/preview1.md#spawn_redirected_in), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

### spawn_native

Forwards [`std.system.os.wasi.preview1.spawn`](wasi/preview1.md#spawn), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

the preview cannot start processes, so this always fails

### spawn_in_native

Forwards [`std.system.os.wasi.preview1.spawn_in`](wasi/preview1.md#spawn_in), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

the preview cannot start processes, so this always fails

### spawn_redirected_native

Forwards [`std.system.os.wasi.preview1.spawn_redirected`](wasi/preview1.md#spawn_redirected), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: Environment, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

### spawn_redirected_in_native

Forwards [`std.system.os.wasi.preview1.spawn_redirected_in`](wasi/preview1.md#spawn_redirected_in), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8, stdin_fd: i32, stdout_fd: i32, stderr_fd: i32) i64
```

the preview cannot start processes, so this always fails

### getpid

Forwards [`std.system.os.wasi.preview1.getpid`](wasi/preview1.md#getpid), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun getpid() i64
```

the preview runs one process and knows no other

### ignore_sigpipe

Forwards [`std.system.os.wasi.preview1.ignore_sigpipe`](wasi/preview1.md#ignore_sigpipe), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun ignore_sigpipe() i64
```

the preview delivers no signals, so there is nothing to ignore

### getenv

Forwards [`std.system.os.wasi.preview1.getenv`](wasi/preview1.md#getenv), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation.

### environ

Forwards [`std.system.os.wasi.preview1.environ`](wasi/preview1.md#environ), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun environ() **u8
```

the program's environment

### getenv_native

Forwards [`std.system.os.wasi.preview1.getenv`](wasi/preview1.md#getenv), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation.

### environ_native

Forwards [`std.system.os.wasi.preview1.environ`](wasi/preview1.md#environ), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun environ() **u8
```

the program's environment

### temp_dir

Forwards [`std.system.os.wasi.preview1.temp_dir`](wasi/preview1.md#temp_dir), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun temp_dir(buf: *u8, cap: usize) i64
```

the directory designated for temporary files: $TMPDIR, else "/tmp"

### wait

Forwards [`std.system.os.wasi.preview1.wait`](wasi/preview1.md#wait), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun wait(pid: i64, status: *ProcessStatus, options: i32, rusage: *u8) WaitResult
```

the preview has no child processes, so waiting always fails

### wait_pid

Forwards [`std.system.os.wasi.preview1.wait_pid`](wasi/preview1.md#wait_pid), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun wait_pid(pid: i64, status: *ProcessStatus, options: i32) WaitResult
```

the preview has no child processes, so waiting always fails

### ProcessStatus

Forwards [`std.system.os.wasi.preview1.ProcessStatus`](wasi/preview1.md#processstatus), only where `$mach.build.sys == $mach.sys.wasi`.

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

Forwards [`std.system.os.wasi.preview1.FileLimit`](wasi/preview1.md#filelimit), only where `$mach.build.sys == $mach.sys.wasi`.

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

Forwards [`std.system.os.wasi.preview1.MemoryLimit`](wasi/preview1.md#memorylimit), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec MemoryLimit {
    soft: u64;
    hard: u64;
}
```

the locked-memory limit in bytes. soft is the limit in force and hard its
ceiling for an unprivileged raise

### LIMIT_UNLIMITED

Forwards [`std.system.os.wasi.preview1.LIMIT_UNLIMITED`](wasi/preview1.md#limit_unlimited), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards [`std.system.os.wasi.preview1.open_file_limit`](wasi/preview1.md#open_file_limit), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun open_file_limit(out: *FileLimit) i64
```

the preview states no open-file limit, so reading it always fails

### set_open_file_limit

Forwards [`std.system.os.wasi.preview1.set_open_file_limit`](wasi/preview1.md#set_open_file_limit), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun set_open_file_limit(limit: FileLimit) i64
```

the preview states no open-file limit, so setting it always fails

### locked_memory_limit

Forwards [`std.system.os.wasi.preview1.locked_memory_limit`](wasi/preview1.md#locked_memory_limit), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun locked_memory_limit(out: *MemoryLimit) i64
```

the preview states no locked-memory limit, so reading it always fails

### ProcessWaitError

Forwards [`std.system.os.wasi.preview1.ProcessWaitError`](wasi/preview1.md#processwaiterror), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

why a process wait or the release of a child's handle failed

### WaitResult

Forwards [`std.system.os.wasi.preview1.WaitResult`](wasi/preview1.md#waitresult), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_WAIT`](wasi/preview1.md#process_op_wait), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_STATUS`](wasi/preview1.md#process_op_status), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_CLOSE`](wasi/preview1.md#process_op_close), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_SPAWN`](wasi/preview1.md#process_op_spawn), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_READ`](wasi/preview1.md#process_op_read), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_PIPE`](wasi/preview1.md#process_op_pipe), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards [`std.system.os.wasi.preview1.PROCESS_OP_TERMINATE`](wasi/preview1.md#process_op_terminate), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards [`std.system.os.wasi.preview1.PROCESS_EXITED`](wasi/preview1.md#process_exited), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards [`std.system.os.wasi.preview1.PROCESS_SIGNALED`](wasi/preview1.md#process_signaled), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards [`std.system.os.wasi.preview1.PROCESS_STOPPED`](wasi/preview1.md#process_stopped), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards [`std.system.os.wasi.preview1.PROCESS_CONTINUED`](wasi/preview1.md#process_continued), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### sleep

Forwards [`std.system.os.wasi.preview1.sleep`](wasi/preview1.md#sleep), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun sleep(nsec: i64)
```

time and entropy

### clock_gettime

Forwards [`std.system.os.wasi.preview1.clock_gettime`](wasi/preview1.md#clock_gettime), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun clock_gettime(clock_id: i32, ts: *timespec) i64
```

get time from a clock source

### random_fill

Forwards [`std.system.os.wasi.preview1.random_fill`](wasi/preview1.md#random_fill), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

fill a buffer with cryptographic random bytes from the host

### stack_bounds

Forwards [`std.system.os.wasi.preview1.stack_bounds`](wasi/preview1.md#stack_bounds), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

core

### error_kind

Forwards [`std.system.os.errors.error_kind`](errors.md#error_kind), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun error_kind(code: i64) std.io.error.Kind
```

the portable kind of a native error code

### error_message

Forwards [`std.system.os.wasi.shared.error_message`](wasi/shared.md#error_message), only where `$mach.build.sys == $mach.sys.wasi`.

```mach
pub fun error_message(code: i64) str
```

the native text for a negative code

