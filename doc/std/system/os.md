[std](../README.md) / [system](README.md) / **os**

# std.system.os

the OS contract: a small set of primitives, one implementation per OS

the primitives fall into capability groups (core, pages, clock, entropy,
threads, files, io queue, sockets, process). std.system.capability says which
groups a target provides, and a target that claims a group exports every
member of it: each `fwd` below fails the build where the per-OS module lacks
the name. OS-CONTRACT.md lists the members and the assumptions the contract
holds. for platform-specific functionality, import the target module directly
(e.g. std.system.os.linux).

Source: [`src/system/os.mach`](../../../src/system/os.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.system.file_identity`](file_identity.md), [`std.system.os.shared`](os/shared.md).

| Functions | |
| :--- | :--- |
| [`stdin`](#stdin) | the process's standard input, output and error |
| [`stdout`](#stdout), [`stderr`](#stderr) | |
| [`working_dir`](#working_dir) | the directory handle that resolves a relative path against the working directory |
| [`allocate_secret`](#allocate_secret) | a zero-initialized welded region of size bytes, written through out |
| [`free_secret`](#free_secret) | release a region allocate_secret returned, without wiping it |
| [`allocate_secret_typed`](#allocate_secret_typed) | a zero-initialized region of total bytes typed as T, written through out |
| [`free_secret_typed`](#free_secret_typed) | release a region allocate_secret_typed returned, without wiping it |
| [`random_fill_secret`](#random_fill_secret) | fill up to RANDOM_FILL_SECRET_MAX welded bytes from the csprng in one call |
| [`read_at_secret`](#read_at_secret) | one positioned read into welded storage |
| [`write_at_secret`](#write_at_secret) | one positioned write from welded storage |
| [`map_file`](#map_file) | map a file's pages |
| [`read`](#read) | read up to count bytes |
| [`write`](#write) | write up to count bytes |
| [`open`](#open) | open a UTF-8 path relative to dir |
| [`open_native`](#open_native) | open a name given in the host's native units relative to dir |
| [`native_path`](#native_path) | convert a UTF-8 path once into native units, as each UTF-8 primitive does, for a caller that walks or splits the name before it reaches the kernel |
| [`native_path_dnit`](#native_path_dnit) | release a path native_path gave, owned or borrowed |
| [`native_spelling`](#native_spelling) | a native name spelled in UTF-8, the reverse of native_path, not terminated |
| [`close`](#close) | |
| [`sync_fd`](#sync_fd) | windows directory sync certifies ntfs only and returns enotsup on other filesystems |
| [`stat`](#stat), [`set_mode`](#set_mode), [`set_mode_at`](#set_mode_at) | |
| [`set_mode_at_native`](#set_mode_at_native) | set_mode_at for a name in the host's native units, which reach the kernel unchanged |
| [`file_identity`](#file_identity), [`identity_at`](#identity_at) | |
| [`identity_at_native`](#identity_at_native) | identity_at for a name in the host's native units |
| [`retain_identity_at`](#retain_identity_at) | open path relative to dir and pin its identity |
| [`retain_identity_at_native`](#retain_identity_at_native) | retain_identity_at for a name in the host's native units |
| [`publication_capabilities`](#publication_capabilities), [`stat_path`](#stat_path) | |
| [`stat_path_native`](#stat_path_native) | stat_path for a name in the host's native units |
| [`unlink`](#unlink) | remove a UTF-8 path relative to dir, converted as open converts it |
| [`unlink_native`](#unlink_native) | remove a name given in the host's native units, which reach the kernel unchanged |
| [`rename`](#rename) | |
| [`rename_native`](#rename_native) | rename names given in the host's native units |
| [`make_dir`](#make_dir) | |
| [`make_dir_native`](#make_dir_native) | make_dir for a name in the host's native units |
| [`directory_init`](#directory_init) | initialize a cursor in its final storage |
| [`directory_next_native`](#directory_next_native) | next in the host's native units: one borrowed entry, zero eof or a terminal negative error |
| [`directory_refused_native`](#directory_refused_native) | the entry the last directory_next refused for having no UTF-8 spelling |
| [`access`](#access) | |
| [`access_native`](#access_native) | access for a name in the host's native units |
| [`seek`](#seek), [`lock_fd`](#lock_fd) | |
| [`exit`](#exit) | end the process with status, never returning |
| [`spawn_redirected`](#spawn_redirected) | spawn with the child's standard handles replaced |
| [`spawn_redirected_in`](#spawn_redirected_in) | |
| [`spawn_redirected_native`](#spawn_redirected_native) | spawn_redirected from an executable, arguments and environment in native units |
| [`spawn_redirected_in_native`](#spawn_redirected_in_native) | spawn_redirected_in from an executable, arguments, environment and directory in native units |
| [`pipe`](#pipe) | a unidirectional pipe |
| [`realtime`](#realtime) | read the wall-clock time |
| [`monotonic`](#monotonic) | read the monotonic clock |
| [`error_message`](#error_message) | the native text for a code, "not an error" for one that is not negative |
| [`error`](#error) | the io error for a native code a primitive returned |
| [`message`](#message) | the text for an io error: the native message when a native code is behind it, otherwise the name of its kind |

| Constants | |
| :--- | :--- |
| [`INVALID_HANDLE`](#constants) | the handle no resource ever has |

| Forwards | |
| :--- | :--- |
| [`Timespec`](#timespec) | abstract types |
| [`IoQueue`](#ioqueue), [`NativePath`](#nativepath) | |
| [`stat_t`](#stat_t) | kernel ABI types |
| [`DirectoryCursor`](#directorycursor) | initialize cursors in final storage and keep the borrowed fd open until close |
| [`DirectoryEntry`](#directoryentry), [`NativeEntry`](#nativeentry), [`DirectoryInitResult`](#directoryinitresult) | |
| [`O_RDONLY`](#o_rdonly) | file access modes |
| [`O_WRONLY`](#o_wronly), [`O_RDWR`](#o_rdwr), [`O_CREAT`](#o_creat), [`O_EXCL`](#o_excl), [`O_TRUNC`](#o_trunc), [`O_APPEND`](#o_append), [`O_DIRECTORY`](#o_directory) | |
| [`AT_SYMLINK_NOFOLLOW`](#at_symlink_nofollow) | directory helpers |
| [`AT_REMOVEDIR`](#at_removedir) | |
| [`LOCK_SH`](#lock_sh) | advisory file-lock operations |
| [`LOCK_EX`](#lock_ex), [`LOCK_NB`](#lock_nb), [`LOCK_UN`](#lock_un) | |
| [`S_IFMT`](#s_ifmt) | stat mode flags |
| [`S_IFDIR`](#s_ifdir), [`S_IFREG`](#s_ifreg), [`S_IFLNK`](#s_iflnk) | |
| [`SEEK_SET`](#seek_set) | seek whence |
| [`SEEK_CUR`](#seek_cur), [`SEEK_END`](#seek_end) | |
| [`PROT_NONE`](#prot_none) | memory protection |
| [`PROT_READ`](#prot_read), [`PROT_WRITE`](#prot_write), [`PROT_EXEC`](#prot_exec) | |
| [`ADVISE_NORMAL`](#advise_normal) | memory advisory hints |
| [`ADVISE_RANDOM`](#advise_random), [`ADVISE_SEQUENTIAL`](#advise_sequential), [`ADVISE_WILL_NEED`](#advise_will_need), [`ADVISE_DONT_NEED`](#advise_dont_need) | |
| [`allocate`](#allocate) | memory |
| [`deallocate`](#deallocate), [`reallocate`](#reallocate) | |
| [`RANDOM_FILL_SECRET_MAX`](#random_fill_secret_max) | the most bytes one random_fill_secret call accepts |
| [`SECRET_ALIGN`](#secret_align) | the alignment every secret allocation starts on |
| [`SECRET_LOCKS`](#secret_locks) | whether this host locks secret pages |
| [`SecretStatus`](#secretstatus) | how a secret allocation ended: a native code, and whether the host refused the lock |
| [`heap_region_base`](#heap_region_base), [`heap_region_extend`](#heap_region_extend), [`protect`](#protect), [`lock`](#lock), [`unlock`](#unlock), [`advise`](#advise), [`page_size`](#page_size), [`sync_file`](#sync_file), [`PUBLICATION_CLAIMS`](#publication_claims), [`PUBLICATION_RETAIN_REPLACE`](#publication_retain_replace), [`PUBLICATION_READ_RETAIN_REPLACE`](#publication_read_retain_replace), [`symlink`](#symlink) | |
| [`symlink_native`](#symlink_native) | symlink(target, linkpath) for names in the host's native units |
| [`directory_next`](#directory_next) | next returns one borrowed entry, zero eof or a negative error |
| [`directory_dnit`](#directory_dnit) | close consumes the cursor and reports cleanup independently of iteration |
| [`abort`](#abort) | |
| [`stack_bounds`](#stack_bounds) | the calling thread's stack bounds, low to one past high, read without a system call from what the implementation recorded once; false where it knows none |
| [`panic_sink`](#panic_sink) | write msg to the process's error stream and end the process, never returning |
| [`terminate_child`](#terminate_child) | |
| [`EnvironmentOf`](#environmentof) | the spawns take the executable, the arguments, the environment entries and the working directory as UTF-8 or, in the _native forms, as nul-terminated std.runtime.native units that reach the kernel unchanged |
| [`Environment`](#environment), [`NativeEnvironment`](#nativeenvironment), [`spawn`](#spawn), [`spawn_in`](#spawn_in), [`spawn_native`](#spawn_native), [`spawn_in_native`](#spawn_in_native), [`getpid`](#getpid) | |
| [`ignore_sigpipe`](#ignore_sigpipe) | ignore SIGPIPE for this process |
| [`sleep`](#sleep) | |
| [`cpu_features`](#cpu_features) | a group a target does not claim has no member here, so naming one fails the build |
| [`cpu_dit`](#cpu_dit) | a group a target does not claim has no member here, so naming one fails the build |
| [`cpu_count`](#cpu_count), [`thread_affinity`](#thread_affinity), [`set_thread_affinity`](#set_thread_affinity), [`getcwd`](#getcwd) | |
| [`getcwd_native`](#getcwd_native) | getcwd(buf, size) in the host's native units, size counted in units, so a working directory whose path has no UTF-8 spelling is still reported |
| [`getenv`](#getenv) | |
| [`getenv_native`](#getenv_native) | getenv(name, buf, cap) in the host's native units, cap and the length counted in units, so a value with no UTF-8 spelling is still read |
| [`environ_native`](#environ_native) | the environment as the host holds it: a nil-terminated array of nul-terminated NAME=value entries in native units, captured once and kept for the life of the process, or nil when it cannot be read |
| [`WNOHANG`](#wnohang), [`wait`](#wait), [`wait_pid`](#wait_pid), [`ProcessStatus`](#processstatus), [`FileLimit`](#filelimit), [`LIMIT_UNLIMITED`](#limit_unlimited), [`open_file_limit`](#open_file_limit), [`set_open_file_limit`](#set_open_file_limit), [`ProcessWaitError`](#processwaiterror), [`WaitResult`](#waitresult), [`PROCESS_OP_WAIT`](#process_op_wait), [`PROCESS_OP_STATUS`](#process_op_status), [`PROCESS_OP_CLOSE`](#process_op_close), [`PROCESS_OP_SPAWN`](#process_op_spawn), [`PROCESS_OP_READ`](#process_op_read), [`PROCESS_OP_PIPE`](#process_op_pipe), [`PROCESS_OP_TERMINATE`](#process_op_terminate), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`io_queue_create`](#io_queue_create) | completion wait queue |
| [`io_queue_wait`](#io_queue_wait) | completion wait queue |
| [`io_queue_wake`](#io_queue_wake) | completion wait queue |
| [`io_queue_close`](#io_queue_close) | completion wait queue |
| [`AF_INET`](#af_inet) | sockets |
| [`AF_INET6`](#af_inet6) | sockets |
| [`SOCK_STREAM`](#sock_stream) | sockets |
| [`SOCK_DGRAM`](#sock_dgram) | sockets |
| [`SOL_SOCKET`](#sol_socket) | sockets |
| [`SO_UNSUPPORTED`](#so_unsupported) | sockets |
| [`SO_REUSEADDR`](#so_reuseaddr) | sockets |
| [`SO_REUSEPORT`](#so_reuseport) | sockets |
| [`SO_EXCLUSIVEADDRUSE`](#so_exclusiveaddruse) | sockets |
| [`SO_KEEPALIVE`](#so_keepalive) | sockets |
| [`SO_SNDBUF`](#so_sndbuf) | sockets |
| [`SO_RCVBUF`](#so_rcvbuf) | sockets |
| [`SO_LINGER`](#so_linger) | sockets |
| [`SO_RCVTIMEO`](#so_rcvtimeo) | sockets |
| [`IPPROTO_IP`](#ipproto_ip) | sockets |
| [`IPPROTO_TCP`](#ipproto_tcp) | sockets |
| [`IPPROTO_IPV6`](#ipproto_ipv6) | sockets |
| [`IP_TOS`](#ip_tos) | sockets |
| [`IPV6_V6ONLY`](#ipv6_v6only) | sockets |
| [`IPV6_TCLASS`](#ipv6_tclass) | sockets |
| [`TCP_NODELAY`](#tcp_nodelay) | sockets |
| [`TCP_KEEPIDLE`](#tcp_keepidle) | sockets |
| [`TCP_KEEPINTVL`](#tcp_keepintvl) | sockets |
| [`TCP_KEEPCNT`](#tcp_keepcnt) | sockets |
| [`TCP_FASTOPEN`](#tcp_fastopen) | sockets |
| [`SHUT_RD`](#shut_rd) | sockets |
| [`SHUT_WR`](#shut_wr) | sockets |
| [`SHUT_RDWR`](#shut_rdwr) | sockets |
| [`SOCKADDR_IN_SIZE`](#sockaddr_in_size) | sockets |
| [`SOCKADDR_IN6_SIZE`](#sockaddr_in6_size) | sockets |
| [`SOCKADDR_STORAGE_SIZE`](#sockaddr_storage_size) | sockets |
| [`sock_send`](#sock_send) | sockets |
| [`sock_recv`](#sock_recv) | sockets |
| [`sock_close`](#sock_close) | sockets |
| [`sock_create`](#sock_create) | sockets |
| [`sock_create_flags`](#sock_create_flags) | sockets |
| [`sock_bind`](#sock_bind) | sockets |
| [`sock_listen`](#sock_listen) | sockets |
| [`sock_accept`](#sock_accept) | sockets |
| [`sock_accept_flags`](#sock_accept_flags) | sockets |
| [`sock_connect`](#sock_connect) | sockets |
| [`sock_sendto`](#sock_sendto) | sockets |
| [`sock_recvfrom`](#sock_recvfrom) | sockets |
| [`sock_shutdown`](#sock_shutdown) | sockets |
| [`sock_setopt`](#sock_setopt) | sockets |
| [`sock_getopt`](#sock_getopt) | sockets |
| [`sock_local_addr`](#sock_local_addr) | sockets |
| [`sock_remote_addr`](#sock_remote_addr) | sockets |
| [`sock_inheritable`](#sock_inheritable) | sockets |
| [`sock_connect_begin`](#sock_connect_begin) | sockets |
| [`sock_connect_poll`](#sock_connect_poll) | sockets |
| [`CONNECT_PENDING`](#connect_pending) | sockets |
| [`sock_set_rcvtimeo`](#sock_set_rcvtimeo) | sockets |
| [`DNS_HOSTS_PATH`](#dns_hosts_path) | sockets |
| [`random_fill`](#random_fill) | random |
| [`thread_spawn`](#thread_spawn) | threads |
| [`thread_join`](#thread_join) | threads |
| [`thread_detach`](#thread_detach) | threads |
| [`thread_current_id`](#thread_current_id) | threads |
| [`thread_current_name`](#thread_current_name) | threads |
| [`thread_wait`](#thread_wait) | threads |
| [`thread_wait_until`](#thread_wait_until) | threads |
| [`thread_wake`](#thread_wake) | threads |
| [`ThreadBlock`](#threadblock) | threads |
| [`thread_block`](#thread_block) | the calling thread's block, read without a system call; nil where none is installed |
| [`thread_block_enter`](#thread_block_enter) | install block as the calling thread's; the runtime does this for the main thread |
| [`error_kind`](#error_kind) | |

---

## Functions

### stdin

```mach
pub fun stdin() usize
```

the process's standard input, output and error

### stdout

```mach
pub fun stdout() usize
```

### stderr

```mach
pub fun stderr() usize
```

### working_dir

```mach
pub fun working_dir() usize
```

the directory handle that resolves a relative path against the working directory

### allocate_secret

```mach
pub fun allocate_secret(size: usize, out: **^u8) SecretStatus
```

a zero-initialized welded region of size bytes, written through out

### free_secret

```mach
pub fun free_secret(data: *^u8, size: usize) i64
```

release a region allocate_secret returned, without wiping it

### allocate_secret_typed

```mach
pub fun allocate_secret_typed[T](total: usize, out: **T) SecretStatus
```

a zero-initialized region of total bytes typed as T, written through out

### free_secret_typed

```mach
pub fun free_secret_typed[T](base: *T, total: usize) i64
```

release a region allocate_secret_typed returned, without wiping it

### random_fill_secret

```mach
pub fun random_fill_secret(data: *^u8, len: usize) i64
```

fill up to RANDOM_FILL_SECRET_MAX welded bytes from the csprng in one call

| Parameter | |
| :--- | :--- |
| **returns** | bytes filled, possibly fewer than len, or a negative native code |

### read_at_secret

```mach
pub fun read_at_secret(handle: usize, data: *^u8, len: usize, offset: u64) i64
```

one positioned read into welded storage

| Parameter | |
| :--- | :--- |
| **returns** | bytes delivered, zero at end of file, or a negative native code |

### write_at_secret

```mach
pub fun write_at_secret(handle: usize, data: *^u8, len: usize, offset: u64) i64
```

one positioned write from welded storage

| Parameter | |
| :--- | :--- |
| **returns** | bytes persisted, or a negative native code |

### map_file

```mach
pub fun map_file(handle: usize, offset: usize, size: usize, prot: u32) ptr
```

map a file's pages

### read

```mach
pub fun read(handle: usize, buf: *u8, count: usize) i64
```

read up to count bytes

| Parameter | |
| :--- | :--- |
| **returns** | bytes read, zero at end of file, or a negative native code |

### write

```mach
pub fun write(handle: usize, buf: *u8, count: usize) i64
```

write up to count bytes

| Parameter | |
| :--- | :--- |
| **returns** | bytes written, or a negative native code |

### open

```mach
pub fun open(dir: usize, path: *u8, flags: i32, mode: i32, out: *usize) i64
```

open a UTF-8 path relative to dir

on linux and darwin the bytes are the native name, so this is open_native.
on windows the path is converted to UTF-16 once, refusing malformed UTF-8,
and opened by open_native

| Parameter | |
| :--- | :--- |
| `dir` | a directory handle, or working_dir() |
| `out` | the new handle, written only on success |
| **returns** | 0, or a negative native code |

### open_native

```mach
pub fun open_native(dir: usize, name: *Unit, flags: i32, mode: i32, out: *usize) i64
```

open a name given in the host's native units relative to dir

the units reach the kernel unchanged: UTF-16 to the W APIs on windows, so an
unpaired surrogate opens what it names, and bytes to the open syscall on
linux and darwin, valid UTF-8 or not

| Parameter | |
| :--- | :--- |
| `dir` | a directory handle, or working_dir() |
| `name` | the nul-terminated name, in std.runtime.native units |
| `out` | the new handle, written only on success |
| **returns** | 0, or a negative native code |

### native_path

```mach
pub fun native_path(path: *u8, out: *NativePath) i64
```

convert a UTF-8 path once into native units, as each UTF-8 primitive does,
for a caller that walks or splits the name before it reaches the kernel

on linux and darwin the bytes already are the native name, so the path is
borrowed and only nil is refused. on windows it is converted to an owned
UTF-16 path with the refusals of every UTF-8 primitive: nil, empty or
malformed UTF-8 is EINVAL and a path over the converter's limit ERANGE

| Parameter | |
| :--- | :--- |
| `out` | the native path, written only on success and released with native_path_release |
| **returns** | 0, or a negative native code |

### native_path_dnit

```mach
pub fun native_path_dnit(path: *NativePath)
```

release a path native_path gave, owned or borrowed

### native_spelling

```mach
pub fun native_spelling(name: *Unit, length: usize, out: *u8, capacity: usize) i64
```

a native name spelled in UTF-8, the reverse of native_path, not terminated

| Parameter | |
| :--- | :--- |
| `name` | the name in native units |
| `length` | its length in units |
| `out` | destination for the bytes, or nil to measure |
| **returns** | the byte count written or measured, EINVAL for a name with no UTF-8 spelling, which only windows can hold, or ERANGE when out is too small. linux and darwin names are bytes, spelled as they are |

### close

```mach
pub fun close(handle: usize) i64
```

### sync_fd

```mach
pub fun sync_fd(handle: usize) i64
```

windows directory sync certifies ntfs only and returns enotsup on other filesystems

### stat

```mach
pub fun stat(handle: usize, st: *impl.stat_t) i64
```

### set_mode

```mach
pub fun set_mode(handle: usize, mode: i32) i64
```

### set_mode_at

```mach
pub fun set_mode_at(dir: usize, name: *u8, mode: i32) i64
```

### set_mode_at_native

```mach
pub fun set_mode_at_native(dir: usize, name: *Unit, mode: i32) i64
```

set_mode_at for a name in the host's native units, which reach the kernel unchanged

### file_identity

```mach
pub fun file_identity(handle: usize, out: *std.system.file_identity.Identity) i64
```

### identity_at

```mach
pub fun identity_at(dir: usize, path: *u8, out: *std.system.file_identity.Identity) i64
```

### identity_at_native

```mach
pub fun identity_at_native(dir: usize, name: *Unit, out: *std.system.file_identity.Identity) i64
```

identity_at for a name in the host's native units

### retain_identity_at

```mach
pub fun retain_identity_at(dir: usize, path: *u8, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity, handle: *usize) i64
```

open path relative to dir and pin its identity

| Parameter | |
| :--- | :--- |
| `handle` | the retained handle, written only on success |
| **returns** | 0, or a negative native code |

### retain_identity_at_native

```mach
pub fun retain_identity_at_native(dir: usize, name: *Unit, access: std.system.file_identity.Access, out: *std.system.file_identity.Identity, handle: *usize) i64
```

retain_identity_at for a name in the host's native units

### publication_capabilities

```mach
pub fun publication_capabilities(handle: usize) i64
```

### stat_path

```mach
pub fun stat_path(dir: usize, path: *u8, st: *impl.stat_t, flags: i32) i64
```

### stat_path_native

```mach
pub fun stat_path_native(dir: usize, name: *Unit, st: *impl.stat_t, flags: i32) i64
```

stat_path for a name in the host's native units

### unlink

```mach
pub fun unlink(dir: usize, path: *u8, flags: i32) i64
```

remove a UTF-8 path relative to dir, converted as open converts it

### unlink_native

```mach
pub fun unlink_native(dir: usize, name: *Unit, flags: i32) i64
```

remove a name given in the host's native units, which reach the kernel unchanged

### rename

```mach
pub fun rename(old_dir: usize, old_path: *u8, new_dir: usize, new_path: *u8) i64
```

### rename_native

```mach
pub fun rename_native(old_dir: usize, old_name: *Unit, new_dir: usize, new_name: *Unit) i64
```

rename names given in the host's native units

### make_dir

```mach
pub fun make_dir(dir: usize, path: *u8, mode: i32) i64
```

### make_dir_native

```mach
pub fun make_dir_native(dir: usize, name: *Unit, mode: i32) i64
```

make_dir for a name in the host's native units

### directory_init

```mach
pub fun directory_init(out: *impl.DirectoryCursor, handle: usize) impl.DirectoryInitResult
```

initialize a cursor in its final storage. it borrows handle until close

### directory_next_native

```mach
pub fun directory_next_native(cursor: *impl.DirectoryCursor, out: *NativeEntry) i64
```

next in the host's native units: one borrowed entry, zero eof or a terminal
negative error. every entry is yielded, whatever its spelling

### directory_refused_native

```mach
pub fun directory_refused_native(cursor: *impl.DirectoryCursor, out: *NativeEntry) i64
```

the entry the last directory_next refused for having no UTF-8 spelling

| Parameter | |
| :--- | :--- |
| `out` | the entry in native units, borrowed until the next cursor operation |
| **returns** | 1 with out filled, 0 when the last call refused no entry, or EINVAL for a cursor that is not active. linux and darwin names are bytes, so there it is always 0 |

### access

```mach
pub fun access(dir: usize, path: *u8, mode: i32, flags: i32) i64
```

### access_native

```mach
pub fun access_native(dir: usize, name: *Unit, mode: i32, flags: i32) i64
```

access for a name in the host's native units

### seek

```mach
pub fun seek(handle: usize, offset: i64, whence: i32) i64
```

### lock_fd

```mach
pub fun lock_fd(handle: usize, op: i32) i64
```

### exit

```mach
pub fun exit(status: u32)
```

end the process with status, never returning

### spawn_redirected

```mach
pub fun spawn_redirected(pathname: *u8, argv: **u8, envp: std.system.os.shared.Environment, input: usize, output: usize, error_out: usize) i64
```

spawn with the child's standard handles replaced

| Parameter | |
| :--- | :--- |
| **returns** | the child's pid, or a negative native code |

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: *u8, argv: **u8, envp: std.system.os.shared.Environment, cwd: *u8, input: usize, output: usize, error_out: usize) i64
```

### spawn_redirected_native

```mach
pub fun spawn_redirected_native(pathname: *Unit, argv: **Unit, envp: std.system.os.shared.NativeEnvironment, input: usize, output: usize, error_out: usize) i64
```

spawn_redirected from an executable, arguments and environment in native units

### spawn_redirected_in_native

```mach
pub fun spawn_redirected_in_native(pathname: *Unit, argv: **Unit, envp: std.system.os.shared.NativeEnvironment, cwd: *Unit, input: usize, output: usize, error_out: usize) i64
```

spawn_redirected_in from an executable, arguments, environment and directory
in native units

### pipe

```mach
pub fun pipe(read_end: *usize, write_end: *usize) i64
```

a unidirectional pipe

| Parameter | |
| :--- | :--- |
| `read_end` | the reading handle, written only on success |
| `write_end` | the writing handle, written only on success |
| **returns** | 0, or a negative native code |

### realtime

```mach
pub fun realtime(out: *Timespec) i64
```

read the wall-clock time

| Parameter | |
| :--- | :--- |
| `out` | pointer to Timespec to populate |
| **returns** | 0 on success, negative errno on failure |

### monotonic

```mach
pub fun monotonic(out: *Timespec) i64
```

read the monotonic clock

| Parameter | |
| :--- | :--- |
| `out` | pointer to Timespec to populate |
| **returns** | 0 on success, negative errno on failure |

### error_message

```mach
pub fun error_message(code: i64) str
```

the native text for a code, "not an error" for one that is not negative

### error

```mach
pub fun error(code: i64, operation: std.io.error.Operation) std.io.error.Error
```

the io error for a native code a primitive returned

| Parameter | |
| :--- | :--- |
| `code` | the primitive's negative return |
| `operation` | the operation that failed |
| **returns** | the error, classified by error_kind and keeping the native code |

### message

```mach
pub fun message(failure: std.io.error.Error) str
```

the text for an io error: the native message when a native code is behind
it, otherwise the name of its kind

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `INVALID_HANDLE` | `usize` | `io_handle.INVALID_VALUE` | the handle no resource ever has |

## Forwards

### Timespec

Forwards [`std.system.os.shared.Timespec`](os/shared.md#timespec).

```mach
pub rec Timespec {
    sec:  i64;
    nsec: i64;
}
```

abstract types

### IoQueue

Forwards [`std.system.os.shared.IoQueue`](os/shared.md#ioqueue).

```mach
pub rec IoQueue {
    handle:       usize;
    wake:         usize;
    wake_pending: usize;
}
```

native wait queue state owned by the portable completion runtime

### NativePath

Forwards [`std.system.os.shared.NativePath`](os/shared.md#nativepath).

```mach
pub rec NativePath {
    units: *Unit;
    size:  usize;
}
```

a whole path in native units, nul-terminated, as native_path gives it

### stat_t

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.stat_t`](os/linux.md#stat_t).

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

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.stat_t`](os/darwin.md#stat_t).

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

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.stat_t`](os/windows.md#stat_t).

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

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.stat_t`](os/wasi.md#stat_t).

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

### DirectoryCursor

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.DirectoryCursor`](os/linux.md#directorycursor).

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

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.DirectoryCursor`](os/darwin.md#directorycursor).

```mach
pub rec DirectoryCursor {
    address: usize;
    active:  bool;
    ended:   bool;
    error:   i64;
    stream:  std.system.os.darwin.libsystem.DirectoryStream;
}
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.DirectoryCursor`](os/windows.md#directorycursor).

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

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.DirectoryCursor`](os/wasi.md#directorycursor).

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

initialize cursors in final storage and keep the borrowed fd open until close

### DirectoryEntry

Forwards the first of these whose condition holds:

- [`std.system.os.linux.DirectoryEntry`](os/linux.md#directoryentry), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.DirectoryEntry`](os/darwin.md#directoryentry), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.DirectoryEntry`](os/windows.md#directoryentry), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.DirectoryEntry`](os/wasi.md#directoryentry), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub rec DirectoryEntry {
    name:      str;
    length:    usize;
    type_hint: u8;
}
```

the name is borrowed until the next cursor operation, including eof or failure

### NativeEntry

Forwards [`std.system.os.shared.NativeEntry`](os/shared.md#nativeentry).

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

- [`std.system.os.linux.DirectoryInitResult`](os/linux.md#directoryinitresult), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.DirectoryInitResult`](os/darwin.md#directoryinitresult), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.DirectoryInitResult`](os/windows.md#directoryinitresult), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.DirectoryInitResult`](os/wasi.md#directoryinitresult), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub rec DirectoryInitResult {
    code:         i64;
    cleanup_code: i64;
}
```

initialization failure and failed duplicate cleanup remain independent

### O_RDONLY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.O_RDONLY`](os/linux.md#o_rdonly), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.O_RDONLY`](os/darwin.md#o_rdonly), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.O_RDONLY`](os/windows.md#o_rdonly), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.O_RDONLY`](os/wasi.md#o_rdonly), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val O_RDONLY:   i32 = 0
```

file access modes

### O_WRONLY

Forwards the first of these whose condition holds:

- [`std.system.os.linux.O_WRONLY`](os/linux.md#o_wronly), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.O_WRONLY`](os/darwin.md#o_wronly), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.O_WRONLY`](os/windows.md#o_wronly), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.O_WRONLY`](os/wasi.md#o_wronly), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val O_WRONLY:   i32 = 1
```

### O_RDWR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.O_RDWR`](os/linux.md#o_rdwr), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.O_RDWR`](os/darwin.md#o_rdwr), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.O_RDWR`](os/windows.md#o_rdwr), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.O_RDWR`](os/wasi.md#o_rdwr), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val O_RDWR:     i32 = 2
```

### O_CREAT

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.O_CREAT`](os/linux.md#o_creat).

```mach
pub val O_CREAT:    i32 = 64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.O_CREAT`](os/darwin.md#o_creat).

```mach
pub val O_CREAT:     i32 = 0x200
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.O_CREAT`](os/windows.md#o_creat).

```mach
pub val O_CREAT:     i32 = 0x100
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.O_CREAT`](os/wasi.md#o_creat).

```mach
pub val O_CREAT:     i32 = 64
```

### O_EXCL

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.O_EXCL`](os/linux.md#o_excl).

```mach
pub val O_EXCL:     i32 = 128
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.O_EXCL`](os/darwin.md#o_excl).

```mach
pub val O_EXCL:      i32 = 0x800
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.O_EXCL`](os/windows.md#o_excl).

```mach
pub val O_EXCL:      i32 = 0x200
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.O_EXCL`](os/wasi.md#o_excl).

```mach
pub val O_EXCL:      i32 = 128
```

### O_TRUNC

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.O_TRUNC`](os/linux.md#o_trunc).

```mach
pub val O_TRUNC:    i32 = 512
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.O_TRUNC`](os/darwin.md#o_trunc).

```mach
pub val O_TRUNC:     i32 = 0x400
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.O_TRUNC`](os/windows.md#o_trunc).

```mach
pub val O_TRUNC:     i32 = 0x400
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.O_TRUNC`](os/wasi.md#o_trunc).

```mach
pub val O_TRUNC:     i32 = 512
```

### O_APPEND

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.O_APPEND`](os/linux.md#o_append).

```mach
pub val O_APPEND:   i32 = 1024
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.O_APPEND`](os/darwin.md#o_append).

```mach
pub val O_APPEND:    i32 = 8
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.O_APPEND`](os/windows.md#o_append).

```mach
pub val O_APPEND:    i32 = 0x800
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.O_APPEND`](os/wasi.md#o_append).

```mach
pub val O_APPEND:    i32 = 1024
```

### O_DIRECTORY

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.O_DIRECTORY`](os/linux.md#o_directory).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub val O_DIRECTORY: i32 = 0o40000
```

Otherwise:

```mach
pub val O_DIRECTORY: i32 = 0o200000
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.O_DIRECTORY`](os/darwin.md#o_directory).

```mach
pub val O_DIRECTORY: i32 = 0x100000
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.O_DIRECTORY`](os/windows.md#o_directory).

```mach
pub val O_DIRECTORY: i32 = 0x10000
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.O_DIRECTORY`](os/wasi.md#o_directory).

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

### AT_SYMLINK_NOFOLLOW

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.AT_SYMLINK_NOFOLLOW`](os/linux.md#at_symlink_nofollow).

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0100
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.AT_SYMLINK_NOFOLLOW`](os/darwin.md#at_symlink_nofollow).

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0020
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.AT_SYMLINK_NOFOLLOW`](os/windows.md#at_symlink_nofollow).

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x0100
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.AT_SYMLINK_NOFOLLOW`](os/wasi.md#at_symlink_nofollow).

```mach
pub val AT_SYMLINK_NOFOLLOW: i32 = 0x100
```

directory helpers

### AT_REMOVEDIR

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.AT_REMOVEDIR`](os/linux.md#at_removedir).

```mach
pub val AT_REMOVEDIR:        i32 = 0x0200
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.AT_REMOVEDIR`](os/darwin.md#at_removedir).

```mach
pub val AT_REMOVEDIR:        i32 = 0x0080
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.AT_REMOVEDIR`](os/windows.md#at_removedir).

```mach
pub val AT_REMOVEDIR:        i32 = 0x0200
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.AT_REMOVEDIR`](os/wasi.md#at_removedir).

```mach
pub val AT_REMOVEDIR:        i32 = 0x200
```

### LOCK_SH

Forwards the first of these whose condition holds:

- [`std.system.os.linux.LOCK_SH`](os/linux.md#lock_sh), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.LOCK_SH`](os/darwin.md#lock_sh), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.LOCK_SH`](os/windows.md#lock_sh), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.LOCK_SH`](os/wasi.md#lock_sh), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val LOCK_SH: i32 = 1
```

advisory file-lock operations

### LOCK_EX

Forwards the first of these whose condition holds:

- [`std.system.os.linux.LOCK_EX`](os/linux.md#lock_ex), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.LOCK_EX`](os/darwin.md#lock_ex), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.LOCK_EX`](os/windows.md#lock_ex), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.LOCK_EX`](os/wasi.md#lock_ex), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val LOCK_EX: i32 = 2
```

### LOCK_NB

Forwards the first of these whose condition holds:

- [`std.system.os.linux.LOCK_NB`](os/linux.md#lock_nb), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.LOCK_NB`](os/darwin.md#lock_nb), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.LOCK_NB`](os/windows.md#lock_nb), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.LOCK_NB`](os/wasi.md#lock_nb), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val LOCK_NB: i32 = 4
```

### LOCK_UN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.LOCK_UN`](os/linux.md#lock_un), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.LOCK_UN`](os/darwin.md#lock_un), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.LOCK_UN`](os/windows.md#lock_un), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.LOCK_UN`](os/wasi.md#lock_un), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val LOCK_UN: i32 = 8
```

### S_IFMT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.S_IFMT`](os/linux.md#s_ifmt), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.S_IFMT`](os/darwin.md#s_ifmt), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.S_IFMT`](os/windows.md#s_ifmt), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.S_IFMT`](os/wasi.md#s_ifmt), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val S_IFMT:  u32 = 0o170000
```

stat mode flags

### S_IFDIR

Forwards the first of these whose condition holds:

- [`std.system.os.linux.S_IFDIR`](os/linux.md#s_ifdir), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.S_IFDIR`](os/darwin.md#s_ifdir), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.S_IFDIR`](os/windows.md#s_ifdir), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.S_IFDIR`](os/wasi.md#s_ifdir), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val S_IFDIR: u32 = 0o040000
```

### S_IFREG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.S_IFREG`](os/linux.md#s_ifreg), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.S_IFREG`](os/darwin.md#s_ifreg), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.S_IFREG`](os/windows.md#s_ifreg), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.S_IFREG`](os/wasi.md#s_ifreg), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val S_IFREG: u32 = 0o100000
```

### S_IFLNK

Forwards the first of these whose condition holds:

- [`std.system.os.linux.S_IFLNK`](os/linux.md#s_iflnk), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.S_IFLNK`](os/darwin.md#s_iflnk), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.S_IFLNK`](os/windows.md#s_iflnk), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.S_IFLNK`](os/wasi.md#s_iflnk), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val S_IFLNK: u32 = 0o120000
```

### SEEK_SET

Forwards [`std.system.os.shared.SEEK_SET`](os/shared.md#constants).

```mach
pub val SEEK_SET: i32 = 0
```

seek whence

### SEEK_CUR

Forwards [`std.system.os.shared.SEEK_CUR`](os/shared.md#constants).

```mach
pub val SEEK_CUR: i32 = 1
```

### SEEK_END

Forwards [`std.system.os.shared.SEEK_END`](os/shared.md#constants).

```mach
pub val SEEK_END: i32 = 2
```

### PROT_NONE

Forwards [`std.system.os.shared.PROT_NONE`](os/shared.md#constants).

```mach
pub val PROT_NONE:  u32 = 0b000
```

memory protection

### PROT_READ

Forwards [`std.system.os.shared.PROT_READ`](os/shared.md#constants).

```mach
pub val PROT_READ:  u32 = 0b001
```

### PROT_WRITE

Forwards [`std.system.os.shared.PROT_WRITE`](os/shared.md#constants).

```mach
pub val PROT_WRITE: u32 = 0b010
```

### PROT_EXEC

Forwards [`std.system.os.shared.PROT_EXEC`](os/shared.md#constants).

```mach
pub val PROT_EXEC:  u32 = 0b100
```

### ADVISE_NORMAL

Forwards [`std.system.os.shared.ADVISE_NORMAL`](os/shared.md#constants).

```mach
pub val ADVISE_NORMAL:     u32 = 0
```

memory advisory hints

### ADVISE_RANDOM

Forwards [`std.system.os.shared.ADVISE_RANDOM`](os/shared.md#constants).

```mach
pub val ADVISE_RANDOM:     u32 = 1
```

### ADVISE_SEQUENTIAL

Forwards [`std.system.os.shared.ADVISE_SEQUENTIAL`](os/shared.md#constants).

```mach
pub val ADVISE_SEQUENTIAL: u32 = 2
```

### ADVISE_WILL_NEED

Forwards [`std.system.os.shared.ADVISE_WILL_NEED`](os/shared.md#constants).

```mach
pub val ADVISE_WILL_NEED:  u32 = 3
```

### ADVISE_DONT_NEED

Forwards [`std.system.os.shared.ADVISE_DONT_NEED`](os/shared.md#constants).

```mach
pub val ADVISE_DONT_NEED:  u32 = 4
```

### allocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.allocate`](os/linux.md#allocate), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.allocate`](os/darwin.md#allocate), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.allocate`](os/windows.md#allocate), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.allocate`](os/wasi.md#allocate), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun allocate(size: usize) ptr
```

memory

### deallocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.deallocate`](os/linux.md#deallocate), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.deallocate`](os/darwin.md#deallocate), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.deallocate`](os/windows.md#deallocate), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.deallocate`](os/wasi.md#deallocate), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun deallocate(p: ptr, size: usize) i64
```

free memory via munmap

### reallocate

Forwards the first of these whose condition holds:

- [`std.system.os.linux.reallocate`](os/linux.md#reallocate), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.reallocate`](os/darwin.md#reallocate), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.reallocate`](os/windows.md#reallocate), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.reallocate`](os/wasi.md#reallocate), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a memory region via mremap

### RANDOM_FILL_SECRET_MAX

Forwards [`std.system.os.secret.RANDOM_FILL_MAX`](os/secret.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.darwin`:

```mach
pub val RANDOM_FILL_MAX: usize = 256
```

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub val RANDOM_FILL_MAX: usize = 0xFFFFFFFF
```

Otherwise:

```mach
pub val RANDOM_FILL_MAX: usize = ~(0::usize)
```

the most bytes one random_fill_secret call accepts

### SECRET_ALIGN

Forwards [`std.system.os.secret.ALIGN`](os/secret.md#constants).

```mach
pub val ALIGN: usize = 4096
```

the alignment every secret allocation starts on

### SECRET_LOCKS

Forwards [`std.system.os.secret.LOCKS`](os/secret.md#constants).

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.linux`:

```mach
pub val LOCKS: bool = true
```

Where `$mach.build.sys == $mach.sys.darwin`:

```mach
pub val LOCKS: bool = true
```

Where `$mach.build.sys == $mach.sys.wasi`:

```mach
pub val LOCKS: bool = false
```

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub val LOCKS: bool = true
```

whether this host locks secret pages. every secret allocation is locked,
guarded and, where the host can say so, kept out of dumps, or it fails

### SecretStatus

Forwards [`std.system.os.secret.Status`](os/secret.md#status).

```mach
pub rec Status {
    code: i64;
    lock: bool;
}
```

how a secret allocation ended: a native code, and whether the host refused
the lock

### heap_region_base

Forwards the first of these whose condition holds:

- [`std.system.os.linux.heap_region_base`](os/linux.md#heap_region_base), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.heap_region_base`](os/darwin.md#heap_region_base), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.heap_region_base`](os/windows.md#heap_region_base), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.heap_region_base`](os/wasi.md#heap_region_base), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun heap_region_base() usize
```

query the current program break via brk(0)

### heap_region_extend

Forwards the first of these whose condition holds:

- [`std.system.os.linux.heap_region_extend`](os/linux.md#heap_region_extend), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.heap_region_extend`](os/darwin.md#heap_region_extend), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.heap_region_extend`](os/windows.md#heap_region_extend), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.heap_region_extend`](os/wasi.md#heap_region_extend), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun heap_region_extend(addr: usize) usize
```

set the program break to addr via brk

### protect

Forwards the first of these whose condition holds:

- [`std.system.os.linux.protect`](os/linux.md#protect), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.protect`](os/darwin.md#protect), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.protect`](os/windows.md#protect), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.protect`](os/wasi.md#protect), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun protect(p: ptr, size: usize, prot: u32) i64
```

change protection on a memory region via mprotect

### lock

Forwards the first of these whose condition holds:

- [`std.system.os.linux.lock`](os/linux.md#lock), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.lock`](os/darwin.md#lock), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.lock`](os/windows.md#lock), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.lock`](os/wasi.md#lock), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun lock(p: ptr, size: usize) i64
```

lock a memory region into physical RAM via mlock

### unlock

Forwards the first of these whose condition holds:

- [`std.system.os.linux.unlock`](os/linux.md#unlock), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.unlock`](os/darwin.md#unlock), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.unlock`](os/windows.md#unlock), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.unlock`](os/wasi.md#unlock), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun unlock(p: ptr, size: usize) i64
```

unlock a previously locked memory region via munlock

### advise

Forwards the first of these whose condition holds:

- [`std.system.os.linux.advise`](os/linux.md#advise), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.advise`](os/darwin.md#advise), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.advise`](os/windows.md#advise), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.advise`](os/wasi.md#advise), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun advise(p: ptr, size: usize, advice: u32) i64
```

advise the kernel on expected access patterns via madvise

### page_size

Forwards the first of these whose condition holds:

- [`std.system.os.linux.page_size`](os/linux.md#page_size), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.page_size`](os/darwin.md#page_size), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.page_size`](os/windows.md#page_size), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.page_size`](os/wasi.md#page_size), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun page_size() usize
```

return the system page size

riscv32 linux uses 4 KiB base pages (Sv32's leaf),
but it reads the runtime AT_PAGESZ the entrypoint captured
(shared.capture_pagesz) for one page-size source of truth. AT_PAGESZ is
mandatory on linux, so a 0 here means the auxv lacked it or a caller ran before
runtime init; page_size() panics rather than fabricating a default.

### sync_file

Forwards the first of these whose condition holds:

- [`std.system.os.linux.sync_file`](os/linux.md#sync_file), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.sync_file`](os/darwin.md#sync_file), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.sync_file`](os/windows.md#sync_file), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.sync_file`](os/wasi.md#sync_file), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun sync_file(p: ptr, size: usize) i64
```

flush a memory-mapped region to its backing file via msync

### PUBLICATION_CLAIMS

Forwards [`std.system.os.shared.PUBLICATION_CLAIMS`](os/shared.md#constants).

```mach
pub val PUBLICATION_CLAIMS:              i64 = 1
```

independently qualified cooperative publication capabilities

### PUBLICATION_RETAIN_REPLACE

Forwards [`std.system.os.shared.PUBLICATION_RETAIN_REPLACE`](os/shared.md#constants).

```mach
pub val PUBLICATION_RETAIN_REPLACE:      i64 = 2
```

### PUBLICATION_READ_RETAIN_REPLACE

Forwards [`std.system.os.shared.PUBLICATION_READ_RETAIN_REPLACE`](os/shared.md#constants).

```mach
pub val PUBLICATION_READ_RETAIN_REPLACE: i64 = 4
```

### symlink

Forwards the first of these whose condition holds:

- [`std.system.os.linux.symlink`](os/linux.md#symlink), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.symlink`](os/darwin.md#symlink), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.symlink`](os/windows.md#symlink), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.symlink`](os/wasi.md#symlink), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

create a symbolic link at linkpath pointing to target

target is stored verbatim: a relative target stays relative, so the link
keeps resolving correctly after the containing tree is moved.

### symlink_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.symlink_native`](os/linux.md#symlink_native).

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.symlink_native`](os/darwin.md#symlink_native).

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.symlink_native`](os/windows.md#symlink_native).

```mach
pub fun symlink_native(target: *u16, linkpath: *u16) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.symlink_native`](os/wasi.md#symlink_native).

```mach
pub fun symlink(target: *u8, linkpath: *u8) i64
```

symlink(target, linkpath) for names in the host's native units

### directory_next

Forwards the first of these whose condition holds:

- [`std.system.os.linux.directory_next`](os/linux.md#directory_next), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.directory_next`](os/darwin.md#directory_next), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.directory_next`](os/windows.md#directory_next), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.directory_next`](os/wasi.md#directory_next), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun directory_next(cursor: *DirectoryCursor, out: *DirectoryEntry) i64
```

next returns one borrowed entry, zero eof or a negative error. the error is
terminal except for an entry with no UTF-8 spelling, which only a windows
directory can hold: that entry alone is refused with EINVAL, its native name
is read with directory_refused_native, and the next call goes on

### directory_dnit

Forwards the first of these whose condition holds:

- [`std.system.os.linux.directory_dnit`](os/linux.md#directory_dnit), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.directory_dnit`](os/darwin.md#directory_dnit), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.directory_dnit`](os/windows.md#directory_dnit), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.directory_dnit`](os/wasi.md#directory_dnit), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun directory_dnit(cursor: *DirectoryCursor) i64
```

close consumes the cursor and reports cleanup independently of iteration

### abort

Forwards the first of these whose condition holds:

- [`std.system.os.linux.abort`](os/linux.md#abort), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.abort`](os/darwin.md#abort), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.abort`](os/windows.md#abort), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.abort`](os/wasi.md#abort), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun abort()
```

abort the process immediately with exit code 255

### stack_bounds

Forwards the first of these whose condition holds:

- [`std.system.os.linux.stack_bounds`](os/linux.md#stack_bounds), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.stack_bounds`](os/darwin.md#stack_bounds), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.stack_bounds`](os/windows.md#stack_bounds), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.stack_bounds`](os/wasi.md#stack_bounds), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun stack_bounds(low: *usize, high: *usize) bool
```

the calling thread's stack bounds, low to one past high, read without a system
call from what the implementation recorded once; false where it knows none

### panic_sink

Forwards [`std.system.panic.panic_sink`](panic.md#panic_sink).

Declared by the first of these arms whose condition holds.

Where `$mach.build.sys == $mach.sys.linux`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.darwin`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.wasi`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.windows`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

Where `$mach.build.sys == $mach.sys.freestanding`:

```mach
pub fun panic_sink(msg: *u8, len: usize)
```

write msg to the process's error stream and end the process, never returning

### terminate_child

Forwards the first of these whose condition holds:

- [`std.system.os.linux.terminate_child`](os/linux.md#terminate_child), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.terminate_child`](os/darwin.md#terminate_child), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.terminate_child`](os/windows.md#terminate_child), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.terminate_child`](os/wasi.md#terminate_child), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun terminate_child(pid: i64) i64
```

forcefully stop a spawned child without reaping it

waitid with WNOWAIT first asks the kernel to verify that `pid` is still a
child of this process. this rejects unknown and already-reaped PIDs before
kill can affect them, while preserving an exited child's wait status.
callers must not concurrently reap this child through wait or wait_pid: a
reaper could release the numeric PID between the ownership check and kill.

### EnvironmentOf

Forwards [`std.system.os.shared.EnvironmentOf`](os/shared.md#environmentof).

```mach
pub tag EnvironmentOf[T]: u8 {
    given: **T;
    inherit;
}
```

the spawns take the executable, the arguments, the environment entries and
the working directory as UTF-8 or, in the _native forms, as nul-terminated
std.runtime.native units that reach the kernel unchanged. on linux and
darwin the bytes are the native form, so the two are one call. on windows
each UTF-8 string is converted to UTF-16 once, refusing malformed UTF-8, and
spawned by the native form, so an unpaired surrogate is reached only natively.
every spawn takes the child's environment as an Environment, or a
NativeEnvironment in the native forms: given entries, or inherit for this
process's own environment unconverted. a nil given array is refused with EINVAL

### Environment

Forwards [`std.system.os.shared.Environment`](os/shared.md#environment).

```mach
pub def Environment: EnvironmentOf[u8]
```

the environment of a UTF-8 spawn, its entries in UTF-8

### NativeEnvironment

Forwards [`std.system.os.shared.NativeEnvironment`](os/shared.md#nativeenvironment).

```mach
pub def NativeEnvironment: EnvironmentOf[Unit]
```

the environment of a native spawn, its entries in std.runtime.native units.
on linux and darwin the units are bytes, so it is Environment itself

### spawn

Forwards the first of these whose condition holds:

- [`std.system.os.linux.spawn`](os/linux.md#spawn), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.spawn`](os/darwin.md#spawn), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.spawn`](os/windows.md#spawn), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.spawn`](os/wasi.md#spawn), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

### spawn_in

Forwards the first of these whose condition holds:

- [`std.system.os.linux.spawn_in`](os/linux.md#spawn_in), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.spawn_in`](os/darwin.md#spawn_in), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.spawn_in`](os/windows.md#spawn_in), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.spawn_in`](os/wasi.md#spawn_in), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### spawn_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.spawn_native`](os/linux.md#spawn_native).

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.spawn_native`](os/darwin.md#spawn_native).

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.spawn_native`](os/windows.md#spawn_native).

```mach
pub fun spawn_native(pathname: *u16, argv: **u16, envp: NativeEnvironment) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.spawn_native`](os/wasi.md#spawn_native).

```mach
pub fun spawn(pathname: *u8, argv: **u8, envp: Environment) i64
```

create a child process running the given program

closes inherited file descriptors >= 3 in the child before exec to
prevent leaking parent FDs (pipes, sockets, etc.) to the child.

### spawn_in_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.spawn_in_native`](os/linux.md#spawn_in_native).

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.spawn_in_native`](os/darwin.md#spawn_in_native).

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.spawn_in_native`](os/windows.md#spawn_in_native).

```mach
pub fun spawn_in_native(pathname: *u16, argv: **u16, envp: NativeEnvironment, cwd: *u16) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.spawn_in_native`](os/wasi.md#spawn_in_native).

```mach
pub fun spawn_in(pathname: *u8, argv: **u8, envp: Environment, cwd: *u8) i64
```

create a child process running the given program from `cwd`

### getpid

Forwards the first of these whose condition holds:

- [`std.system.os.linux.getpid`](os/linux.md#getpid), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.getpid`](os/darwin.md#getpid), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.getpid`](os/windows.md#getpid), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.getpid`](os/wasi.md#getpid), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun getpid() i64
```

return the current process ID

### ignore_sigpipe

Forwards the first of these whose condition holds:

- [`std.system.os.linux.ignore_sigpipe`](os/linux.md#ignore_sigpipe), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.ignore_sigpipe`](os/darwin.md#ignore_sigpipe), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.ignore_sigpipe`](os/windows.md#ignore_sigpipe), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.ignore_sigpipe`](os/wasi.md#ignore_sigpipe), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun ignore_sigpipe() i64
```

ignore SIGPIPE for this process

on POSIX this changes the process-wide signal disposition, so subsequent
writes from every thread return EPIPE instead of terminating the process.
windows has no SIGPIPE and returns success without changing process state.

### sleep

Forwards the first of these whose condition holds:

- [`std.system.os.linux.sleep`](os/linux.md#sleep), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.sleep`](os/darwin.md#sleep), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.sleep`](os/windows.md#sleep), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.sleep`](os/wasi.md#sleep), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun sleep(nsec: i64)
```

suspend execution for the given number of nanoseconds

### cpu_features

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.cpu_features`](os/linux.md#cpu_features).

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.cpu_features`](os/darwin.md#cpu_features).

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.cpu_features`](os/windows.md#cpu_features).

```mach
pub fun cpu_features(out: *std.system.cpu.features.Features) i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.cpu_features`](os/wasi.md).

a group a target does not claim has no member here, so naming one fails the build

### cpu_dit

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.cpu_dit`](os/linux.md#cpu_dit).

```mach
pub fun cpu_dit() i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.cpu_dit`](os/darwin.md#cpu_dit).

```mach
pub fun cpu_dit() i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.cpu_dit`](os/windows.md#cpu_dit).

```mach
pub fun cpu_dit() i64
```

Where `capability.HAS_CPU_FEATURES` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.cpu_dit`](os/wasi.md).

a group a target does not claim has no member here, so naming one fails the build

### cpu_count

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.cpu_count`](os/linux.md#cpu_count).

```mach
pub fun cpu_count() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.cpu_count`](os/darwin.md#cpu_count).

```mach
pub fun cpu_count() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.cpu_count`](os/windows.md#cpu_count).

```mach
pub fun cpu_count() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.cpu_count`](os/wasi.md).

the number of CPUs available to this process

popcounts the sched_getaffinity mask, so taskset/cgroup cpuset restrictions
are honoured; the kernel reports the mask size it wrote in the return value.
never returns less than 1.

### thread_affinity

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_affinity`](os/linux.md#thread_affinity).

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_affinity`](os/darwin.md#thread_affinity).

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_affinity`](os/windows.md#thread_affinity).

```mach
pub fun thread_affinity(words: *u64, capacity: usize, out_count: *usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_affinity`](os/wasi.md).

read the calling thread's CPU affinity

CPU i is bit i % 64 of words[i / 64]. the kernel reports the bytes it wrote,
which is its own cpumask size, so out_count is that size in words and every
word the kernel wrote is copied, including trailing zero words.

### set_thread_affinity

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.set_thread_affinity`](os/linux.md#set_thread_affinity).

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.set_thread_affinity`](os/darwin.md#set_thread_affinity).

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.set_thread_affinity`](os/windows.md#set_thread_affinity).

```mach
pub fun set_thread_affinity(words: *u64, count: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.set_thread_affinity`](os/wasi.md).

pin the calling thread to the CPUs set in words

### getcwd

Forwards the first of these whose condition holds:

- [`std.system.os.linux.getcwd`](os/linux.md#getcwd), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.getcwd`](os/darwin.md#getcwd), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.getcwd`](os/windows.md#getcwd), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.getcwd`](os/wasi.md#getcwd), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

get the current working directory

the raw syscall returns the length INCLUDING the terminator; this layer
reports the path length the way darwin and windows do, so "length of path"
means one thing across the three backends (#432).

### getcwd_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.getcwd_native`](os/linux.md#getcwd_native).

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.getcwd_native`](os/darwin.md#getcwd_native).

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.getcwd_native`](os/windows.md#getcwd_native).

```mach
pub fun getcwd_native(buf: *u16, size: usize) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.getcwd_native`](os/wasi.md#getcwd_native).

```mach
pub fun getcwd(buf: *u8, size: usize) i64
```

getcwd(buf, size) in the host's native units, size counted in units, so a
working directory whose path has no UTF-8 spelling is still reported

### getenv

Forwards the first of these whose condition holds:

- [`std.system.os.linux.getenv`](os/linux.md#getenv), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.getenv`](os/darwin.md#getenv), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.getenv`](os/windows.md#getenv), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.getenv`](os/wasi.md#getenv), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

look up an environment variable by name

when the value fits (ret \< cap) it is copied and null-terminated.
always returns the full value length, so ret >= cap signals truncation
(buffer contents unspecified) and ret + 1 is the capacity to retry with.

### getenv_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.getenv_native`](os/linux.md#getenv_native).

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.getenv_native`](os/darwin.md#getenv_native).

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.getenv_native`](os/windows.md#getenv_native).

```mach
pub fun getenv_native(name: *u16, buf: *u16, cap: usize) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.getenv_native`](os/wasi.md#getenv_native).

```mach
pub fun getenv(name: *u8, buf: *u8, cap: usize) i64
```

getenv(name, buf, cap) in the host's native units, cap and the length counted
in units, so a value with no UTF-8 spelling is still read. getenv refuses one
with EINVAL

### environ_native

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.environ_native`](os/linux.md#environ_native).

```mach
pub fun environ() **u8
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.environ_native`](os/darwin.md#environ_native).

```mach
pub fun environ() **u8
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.environ_native`](os/windows.md#environ_native).

```mach
pub fun environ_native() **u16
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.environ_native`](os/wasi.md#environ_native).

```mach
pub fun environ() **u8
```

the environment as the host holds it: a nil-terminated array of nul-terminated
NAME=value entries in native units, captured once and kept for the life of
the process, or nil when it cannot be read. linux and darwin give the envp the
kernel passed. windows captures its block once as UTF-16 and skips the hidden
drive-current-directory names. it is the one capture, and
std.process.env.environ is its UTF-8 projection

### WNOHANG

Forwards the first of these whose condition holds:

- [`std.system.os.linux.WNOHANG`](os/linux.md#wnohang), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.WNOHANG`](os/darwin.md#wnohang), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.WNOHANG`](os/windows.md#wnohang), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.WNOHANG`](os/wasi.md#wnohang), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val WNOHANG:    i32 = 1
```

### wait

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.wait`](os/linux.md#wait).

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.wait`](os/darwin.md#wait).

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.wait`](os/windows.md#wait).

```mach
pub fun wait(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32, rusage: *u8) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.wait`](os/wasi.md#wait).

```mach
pub fun wait(pid: i64, status: *ProcessStatus, options: i32, rusage: *u8) WaitResult
```

failures and no-event results leave the caller's status unchanged

### wait_pid

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.wait_pid`](os/linux.md#wait_pid).

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.wait_pid`](os/darwin.md#wait_pid).

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.wait_pid`](os/windows.md#wait_pid).

```mach
pub fun wait_pid(pid: i64, status: *std.system.os.shared.ProcessStatus, options: i32) std.system.os.shared.WaitResult
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.wait_pid`](os/wasi.md#wait_pid).

```mach
pub fun wait_pid(pid: i64, status: *ProcessStatus, options: i32) WaitResult
```

### ProcessStatus

Forwards the first of these whose condition holds:

- [`std.system.os.linux.ProcessStatus`](os/linux.md#processstatus), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.ProcessStatus`](os/darwin.md#processstatus), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.ProcessStatus`](os/windows.md#processstatus), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.ProcessStatus`](os/wasi.md#processstatus), where `$mach.build.sys == $mach.sys.wasi`

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

- [`std.system.os.linux.FileLimit`](os/linux.md#filelimit), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.FileLimit`](os/darwin.md#filelimit), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.FileLimit`](os/windows.md#filelimit), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.FileLimit`](os/wasi.md#filelimit), where `$mach.build.sys == $mach.sys.wasi`

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

- [`std.system.os.linux.LIMIT_UNLIMITED`](os/linux.md#limit_unlimited), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.LIMIT_UNLIMITED`](os/darwin.md#limit_unlimited), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.LIMIT_UNLIMITED`](os/windows.md#limit_unlimited), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.LIMIT_UNLIMITED`](os/wasi.md#limit_unlimited), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val LIMIT_UNLIMITED: u64 = 0xffffffffffffffff
```

a limit with no bound

### open_file_limit

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.open_file_limit`](os/linux.md#open_file_limit).

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.open_file_limit`](os/darwin.md#open_file_limit).

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.open_file_limit`](os/windows.md#open_file_limit).

```mach
pub fun open_file_limit(out: *std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.open_file_limit`](os/wasi.md#open_file_limit).

```mach
pub fun open_file_limit(out: *FileLimit) i64
```

read this process's open-file limit. linux's RLIM_INFINITY is all ones, the
same value as LIMIT_UNLIMITED, and an unprivileged process may raise its soft
limit up to the hard one

### set_open_file_limit

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.set_open_file_limit`](os/linux.md#set_open_file_limit).

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.set_open_file_limit`](os/darwin.md#set_open_file_limit).

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.set_open_file_limit`](os/windows.md#set_open_file_limit).

```mach
pub fun set_open_file_limit(limit: std.system.os.shared.FileLimit) i64
```

Where `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.set_open_file_limit`](os/wasi.md#set_open_file_limit).

```mach
pub fun set_open_file_limit(limit: FileLimit) i64
```

set this process's open-file limit. ceiling is ignored

### ProcessWaitError

Forwards the first of these whose condition holds:

- [`std.system.os.linux.ProcessWaitError`](os/linux.md#processwaiterror), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.ProcessWaitError`](os/darwin.md#processwaiterror), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.ProcessWaitError`](os/windows.md#processwaiterror), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.ProcessWaitError`](os/wasi.md#processwaiterror), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub rec ProcessWaitError {
    code:        i64;
    native_code: u32;
    operation:   u8;
}
```

### WaitResult

Forwards the first of these whose condition holds:

- [`std.system.os.linux.WaitResult`](os/linux.md#waitresult), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.WaitResult`](os/darwin.md#waitresult), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.WaitResult`](os/windows.md#waitresult), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.WaitResult`](os/wasi.md#waitresult), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub rec WaitResult {
    pid:   i64;
    error: ProcessWaitError;
}
```

pid is positive for an observation, zero for no event or an error

### PROCESS_OP_WAIT

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_WAIT`](os/linux.md#process_op_wait), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_WAIT`](os/darwin.md#process_op_wait), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_WAIT`](os/windows.md#process_op_wait), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_WAIT`](os/wasi.md#process_op_wait), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_WAIT:      u8 = 1
```

### PROCESS_OP_STATUS

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_STATUS`](os/linux.md#process_op_status), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_STATUS`](os/darwin.md#process_op_status), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_STATUS`](os/windows.md#process_op_status), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_STATUS`](os/wasi.md#process_op_status), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_STATUS:    u8 = 2
```

### PROCESS_OP_CLOSE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_CLOSE`](os/linux.md#process_op_close), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_CLOSE`](os/darwin.md#process_op_close), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_CLOSE`](os/windows.md#process_op_close), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_CLOSE`](os/wasi.md#process_op_close), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_CLOSE:     u8 = 3
```

### PROCESS_OP_SPAWN

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_SPAWN`](os/linux.md#process_op_spawn), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_SPAWN`](os/darwin.md#process_op_spawn), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_SPAWN`](os/windows.md#process_op_spawn), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_SPAWN`](os/wasi.md#process_op_spawn), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_SPAWN:     u8 = 4
```

### PROCESS_OP_READ

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_READ`](os/linux.md#process_op_read), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_READ`](os/darwin.md#process_op_read), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_READ`](os/windows.md#process_op_read), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_READ`](os/wasi.md#process_op_read), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_READ:      u8 = 5
```

### PROCESS_OP_PIPE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_PIPE`](os/linux.md#process_op_pipe), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_PIPE`](os/darwin.md#process_op_pipe), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_PIPE`](os/windows.md#process_op_pipe), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_PIPE`](os/wasi.md#process_op_pipe), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_PIPE:      u8 = 6
```

### PROCESS_OP_TERMINATE

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_OP_TERMINATE`](os/linux.md#process_op_terminate), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_OP_TERMINATE`](os/darwin.md#process_op_terminate), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_OP_TERMINATE`](os/windows.md#process_op_terminate), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_OP_TERMINATE`](os/wasi.md#process_op_terminate), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_OP_TERMINATE: u8 = 7
```

### PROCESS_EXITED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_EXITED`](os/linux.md#process_exited), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_EXITED`](os/darwin.md#process_exited), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_EXITED`](os/windows.md#process_exited), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_EXITED`](os/wasi.md#process_exited), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_SIGNALED`](os/linux.md#process_signaled), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_SIGNALED`](os/darwin.md#process_signaled), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_SIGNALED`](os/windows.md#process_signaled), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_SIGNALED`](os/wasi.md#process_signaled), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_STOPPED`](os/linux.md#process_stopped), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_STOPPED`](os/darwin.md#process_stopped), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_STOPPED`](os/windows.md#process_stopped), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_STOPPED`](os/wasi.md#process_stopped), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards the first of these whose condition holds:

- [`std.system.os.linux.PROCESS_CONTINUED`](os/linux.md#process_continued), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.PROCESS_CONTINUED`](os/darwin.md#process_continued), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.PROCESS_CONTINUED`](os/windows.md#process_continued), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.PROCESS_CONTINUED`](os/wasi.md#process_continued), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### io_queue_create

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.io_queue_create`](os/linux.md#io_queue_create).

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.io_queue_create`](os/darwin.md#io_queue_create).

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.io_queue_create`](os/windows.md#io_queue_create).

```mach
pub fun io_queue_create(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.io_queue_create`](os/wasi.md).

completion wait queue

### io_queue_wait

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.io_queue_wait`](os/linux.md#io_queue_wait).

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.io_queue_wait`](os/darwin.md#io_queue_wait).

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.io_queue_wait`](os/windows.md#io_queue_wait).

```mach
pub fun io_queue_wait(queue: *std.system.os.shared.IoQueue, timeout_ms: i32) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.io_queue_wait`](os/wasi.md).

completion wait queue

### io_queue_wake

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.io_queue_wake`](os/linux.md#io_queue_wake).

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.io_queue_wake`](os/darwin.md#io_queue_wake).

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.io_queue_wake`](os/windows.md#io_queue_wake).

```mach
pub fun io_queue_wake(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.io_queue_wake`](os/wasi.md).

completion wait queue

### io_queue_close

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.io_queue_close`](os/linux.md#io_queue_close).

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.io_queue_close`](os/darwin.md#io_queue_close).

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.io_queue_close`](os/windows.md#io_queue_close).

```mach
pub fun io_queue_close(queue: *std.system.os.shared.IoQueue) i64
```

Where `capability.HAS_IO_QUEUE` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.io_queue_close`](os/wasi.md).

completion wait queue

### AF_INET

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.AF_INET`](os/linux.md#af_inet).

```mach
pub val AF_INET:             i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.AF_INET`](os/darwin.md#af_inet).

```mach
pub val AF_INET:             i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.AF_INET`](os/windows.md#af_inet).

```mach
pub val AF_INET:             i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.AF_INET`](os/wasi.md).

sockets

### AF_INET6

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.AF_INET6`](os/linux.md#af_inet6).

```mach
pub val AF_INET6:            i32 = 10
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.AF_INET6`](os/darwin.md#af_inet6).

```mach
pub val AF_INET6:            i32 = 30
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.AF_INET6`](os/windows.md#af_inet6).

```mach
pub val AF_INET6:            i32 = 23
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.AF_INET6`](os/wasi.md).

sockets

### SOCK_STREAM

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOCK_STREAM`](os/linux.md#sock_stream).

```mach
pub val SOCK_STREAM:         i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOCK_STREAM`](os/darwin.md#sock_stream).

```mach
pub val SOCK_STREAM:         i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOCK_STREAM`](os/windows.md#sock_stream).

```mach
pub val SOCK_STREAM:         i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOCK_STREAM`](os/wasi.md).

sockets

### SOCK_DGRAM

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOCK_DGRAM`](os/linux.md#sock_dgram).

```mach
pub val SOCK_DGRAM:          i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOCK_DGRAM`](os/darwin.md#sock_dgram).

```mach
pub val SOCK_DGRAM:          i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOCK_DGRAM`](os/windows.md#sock_dgram).

```mach
pub val SOCK_DGRAM:          i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOCK_DGRAM`](os/wasi.md).

sockets

### SOL_SOCKET

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOL_SOCKET`](os/linux.md#sol_socket).

```mach
pub val SOL_SOCKET:          i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOL_SOCKET`](os/darwin.md#sol_socket).

```mach
pub val SOL_SOCKET:          i32 = 0xFFFF
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOL_SOCKET`](os/windows.md#sol_socket).

```mach
pub val SOL_SOCKET:          i32 = 0xFFFF
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOL_SOCKET`](os/wasi.md).

sockets

### SO_UNSUPPORTED

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_UNSUPPORTED`](os/linux.md#so_unsupported).

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_UNSUPPORTED`](os/darwin.md#so_unsupported).

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_UNSUPPORTED`](os/windows.md#so_unsupported).

```mach
pub val SO_UNSUPPORTED:      i32 = -2147483648
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_UNSUPPORTED`](os/wasi.md).

sockets

### SO_REUSEADDR

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_REUSEADDR`](os/linux.md#so_reuseaddr).

```mach
pub val SO_REUSEADDR:        i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_REUSEADDR`](os/darwin.md#so_reuseaddr).

```mach
pub val SO_REUSEADDR:        i32 = 4
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_REUSEADDR`](os/windows.md#so_reuseaddr).

```mach
pub val SO_REUSEADDR:        i32 = 4
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_REUSEADDR`](os/wasi.md).

sockets

### SO_REUSEPORT

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_REUSEPORT`](os/linux.md#so_reuseport).

```mach
pub val SO_REUSEPORT:        i32 = 15
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_REUSEPORT`](os/darwin.md#so_reuseport).

```mach
pub val SO_REUSEPORT:        i32 = 0x0200
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_REUSEPORT`](os/windows.md#so_reuseport).

```mach
pub val SO_REUSEPORT:        i32 = SO_UNSUPPORTED
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_REUSEPORT`](os/wasi.md).

sockets

### SO_EXCLUSIVEADDRUSE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_EXCLUSIVEADDRUSE`](os/linux.md#so_exclusiveaddruse).

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = SO_UNSUPPORTED
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_EXCLUSIVEADDRUSE`](os/darwin.md#so_exclusiveaddruse).

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = SO_UNSUPPORTED
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_EXCLUSIVEADDRUSE`](os/windows.md#so_exclusiveaddruse).

```mach
pub val SO_EXCLUSIVEADDRUSE: i32 = -5
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_EXCLUSIVEADDRUSE`](os/wasi.md).

sockets

### SO_KEEPALIVE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_KEEPALIVE`](os/linux.md#so_keepalive).

```mach
pub val SO_KEEPALIVE:        i32 = 9
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_KEEPALIVE`](os/darwin.md#so_keepalive).

```mach
pub val SO_KEEPALIVE:        i32 = 0x0008
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_KEEPALIVE`](os/windows.md#so_keepalive).

```mach
pub val SO_KEEPALIVE:        i32 = 8
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_KEEPALIVE`](os/wasi.md).

sockets

### SO_SNDBUF

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_SNDBUF`](os/linux.md#so_sndbuf).

```mach
pub val SO_SNDBUF:           i32 = 7
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_SNDBUF`](os/darwin.md#so_sndbuf).

```mach
pub val SO_SNDBUF:           i32 = 0x1001
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_SNDBUF`](os/windows.md#so_sndbuf).

```mach
pub val SO_SNDBUF:           i32 = 0x1001
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_SNDBUF`](os/wasi.md).

sockets

### SO_RCVBUF

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_RCVBUF`](os/linux.md#so_rcvbuf).

```mach
pub val SO_RCVBUF:           i32 = 8
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_RCVBUF`](os/darwin.md#so_rcvbuf).

```mach
pub val SO_RCVBUF:           i32 = 0x1002
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_RCVBUF`](os/windows.md#so_rcvbuf).

```mach
pub val SO_RCVBUF:           i32 = 0x1002
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_RCVBUF`](os/wasi.md).

sockets

### SO_LINGER

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_LINGER`](os/linux.md#so_linger).

```mach
pub val SO_LINGER:           i32 = 13
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_LINGER`](os/darwin.md#so_linger).

```mach
pub val SO_LINGER:           i32 = 0x0080
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_LINGER`](os/windows.md#so_linger).

```mach
pub val SO_LINGER:           i32 = 0x0080
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_LINGER`](os/wasi.md).

sockets

### SO_RCVTIMEO

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SO_RCVTIMEO`](os/linux.md#so_rcvtimeo).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.riscv32`:

```mach
pub val SO_RCVTIMEO: i32 = 66
```

Otherwise:

```mach
pub val SO_RCVTIMEO: i32 = 20
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SO_RCVTIMEO`](os/darwin.md#so_rcvtimeo).

```mach
pub val SO_RCVTIMEO:         i32 = 0x1006
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SO_RCVTIMEO`](os/windows.md#so_rcvtimeo).

```mach
pub val SO_RCVTIMEO:         i32 = 0x1006
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SO_RCVTIMEO`](os/wasi.md).

sockets

### IPPROTO_IP

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IPPROTO_IP`](os/linux.md#ipproto_ip).

```mach
pub val IPPROTO_IP:    i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IPPROTO_IP`](os/darwin.md#ipproto_ip).

```mach
pub val IPPROTO_IP:          i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IPPROTO_IP`](os/windows.md#ipproto_ip).

```mach
pub val IPPROTO_IP:          i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IPPROTO_IP`](os/wasi.md).

sockets

### IPPROTO_TCP

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IPPROTO_TCP`](os/linux.md#ipproto_tcp).

```mach
pub val IPPROTO_TCP:   i32 = 6
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IPPROTO_TCP`](os/darwin.md#ipproto_tcp).

```mach
pub val IPPROTO_TCP:         i32 = 6
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IPPROTO_TCP`](os/windows.md#ipproto_tcp).

```mach
pub val IPPROTO_TCP:         i32 = 6
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IPPROTO_TCP`](os/wasi.md).

sockets

### IPPROTO_IPV6

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IPPROTO_IPV6`](os/linux.md#ipproto_ipv6).

```mach
pub val IPPROTO_IPV6:  i32 = 41
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IPPROTO_IPV6`](os/darwin.md#ipproto_ipv6).

```mach
pub val IPPROTO_IPV6:        i32 = 41
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IPPROTO_IPV6`](os/windows.md#ipproto_ipv6).

```mach
pub val IPPROTO_IPV6:        i32 = 41
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IPPROTO_IPV6`](os/wasi.md).

sockets

### IP_TOS

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IP_TOS`](os/linux.md#ip_tos).

```mach
pub val IP_TOS:        i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IP_TOS`](os/darwin.md#ip_tos).

```mach
pub val IP_TOS:              i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IP_TOS`](os/windows.md#ip_tos).

```mach
pub val IP_TOS:              i32 = 3
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IP_TOS`](os/wasi.md).

sockets

### IPV6_V6ONLY

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IPV6_V6ONLY`](os/linux.md#ipv6_v6only).

```mach
pub val IPV6_V6ONLY:   i32 = 26
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IPV6_V6ONLY`](os/darwin.md#ipv6_v6only).

```mach
pub val IPV6_V6ONLY:         i32 = 27
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IPV6_V6ONLY`](os/windows.md#ipv6_v6only).

```mach
pub val IPV6_V6ONLY:         i32 = 27
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IPV6_V6ONLY`](os/wasi.md).

sockets

### IPV6_TCLASS

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.IPV6_TCLASS`](os/linux.md#ipv6_tclass).

```mach
pub val IPV6_TCLASS:   i32 = 67
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.IPV6_TCLASS`](os/darwin.md#ipv6_tclass).

```mach
pub val IPV6_TCLASS:         i32 = 36
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.IPV6_TCLASS`](os/windows.md#ipv6_tclass).

```mach
pub val IPV6_TCLASS:         i32 = 39
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.IPV6_TCLASS`](os/wasi.md).

sockets

### TCP_NODELAY

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.TCP_NODELAY`](os/linux.md#tcp_nodelay).

```mach
pub val TCP_NODELAY:   i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.TCP_NODELAY`](os/darwin.md#tcp_nodelay).

```mach
pub val TCP_NODELAY:         i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.TCP_NODELAY`](os/windows.md#tcp_nodelay).

```mach
pub val TCP_NODELAY:         i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.TCP_NODELAY`](os/wasi.md).

sockets

### TCP_KEEPIDLE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.TCP_KEEPIDLE`](os/linux.md#tcp_keepidle).

```mach
pub val TCP_KEEPIDLE:  i32 = 4
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.TCP_KEEPIDLE`](os/darwin.md#tcp_keepidle).

```mach
pub val TCP_KEEPIDLE:        i32 = 0x10
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.TCP_KEEPIDLE`](os/windows.md#tcp_keepidle).

```mach
pub val TCP_KEEPIDLE:        i32 = 3
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.TCP_KEEPIDLE`](os/wasi.md).

sockets

### TCP_KEEPINTVL

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.TCP_KEEPINTVL`](os/linux.md#tcp_keepintvl).

```mach
pub val TCP_KEEPINTVL: i32 = 5
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.TCP_KEEPINTVL`](os/darwin.md#tcp_keepintvl).

```mach
pub val TCP_KEEPINTVL:       i32 = 0x101
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.TCP_KEEPINTVL`](os/windows.md#tcp_keepintvl).

```mach
pub val TCP_KEEPINTVL:       i32 = 17
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.TCP_KEEPINTVL`](os/wasi.md).

sockets

### TCP_KEEPCNT

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.TCP_KEEPCNT`](os/linux.md#tcp_keepcnt).

```mach
pub val TCP_KEEPCNT:   i32 = 6
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.TCP_KEEPCNT`](os/darwin.md#tcp_keepcnt).

```mach
pub val TCP_KEEPCNT:         i32 = 0x102
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.TCP_KEEPCNT`](os/windows.md#tcp_keepcnt).

```mach
pub val TCP_KEEPCNT:         i32 = 16
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.TCP_KEEPCNT`](os/wasi.md).

sockets

### TCP_FASTOPEN

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.TCP_FASTOPEN`](os/linux.md#tcp_fastopen).

```mach
pub val TCP_FASTOPEN:  i32 = 23
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.TCP_FASTOPEN`](os/darwin.md#tcp_fastopen).

```mach
pub val TCP_FASTOPEN:        i32 = 0x105
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.TCP_FASTOPEN`](os/windows.md#tcp_fastopen).

```mach
pub val TCP_FASTOPEN:        i32 = 15
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.TCP_FASTOPEN`](os/wasi.md).

sockets

### SHUT_RD

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SHUT_RD`](os/linux.md#shut_rd).

```mach
pub val SHUT_RD:       i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SHUT_RD`](os/darwin.md#shut_rd).

```mach
pub val SHUT_RD:             i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SHUT_RD`](os/windows.md#shut_rd).

```mach
pub val SHUT_RD:             i32 = 0
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SHUT_RD`](os/wasi.md).

sockets

### SHUT_WR

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SHUT_WR`](os/linux.md#shut_wr).

```mach
pub val SHUT_WR:       i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SHUT_WR`](os/darwin.md#shut_wr).

```mach
pub val SHUT_WR:             i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SHUT_WR`](os/windows.md#shut_wr).

```mach
pub val SHUT_WR:             i32 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SHUT_WR`](os/wasi.md).

sockets

### SHUT_RDWR

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SHUT_RDWR`](os/linux.md#shut_rdwr).

```mach
pub val SHUT_RDWR:     i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SHUT_RDWR`](os/darwin.md#shut_rdwr).

```mach
pub val SHUT_RDWR:           i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SHUT_RDWR`](os/windows.md#shut_rdwr).

```mach
pub val SHUT_RDWR:           i32 = 2
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SHUT_RDWR`](os/wasi.md).

sockets

### SOCKADDR_IN_SIZE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOCKADDR_IN_SIZE`](os/linux.md#sockaddr_in_size).

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOCKADDR_IN_SIZE`](os/darwin.md#sockaddr_in_size).

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOCKADDR_IN_SIZE`](os/windows.md#sockaddr_in_size).

```mach
pub val SOCKADDR_IN_SIZE:      usize = 16
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOCKADDR_IN_SIZE`](os/wasi.md).

sockets

### SOCKADDR_IN6_SIZE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOCKADDR_IN6_SIZE`](os/linux.md#sockaddr_in6_size).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOCKADDR_IN6_SIZE`](os/darwin.md#sockaddr_in6_size).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOCKADDR_IN6_SIZE`](os/windows.md#sockaddr_in6_size).

```mach
pub val SOCKADDR_IN6_SIZE:     usize = 28
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOCKADDR_IN6_SIZE`](os/wasi.md).

sockets

### SOCKADDR_STORAGE_SIZE

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.SOCKADDR_STORAGE_SIZE`](os/linux.md#sockaddr_storage_size).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.SOCKADDR_STORAGE_SIZE`](os/darwin.md#sockaddr_storage_size).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.SOCKADDR_STORAGE_SIZE`](os/windows.md#sockaddr_storage_size).

```mach
pub val SOCKADDR_STORAGE_SIZE: usize = 128
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.SOCKADDR_STORAGE_SIZE`](os/wasi.md).

sockets

### sock_send

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_send`](os/linux.md#sock_send).

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_send`](os/darwin.md#sock_send).

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_send`](os/windows.md#sock_send).

```mach
pub fun sock_send(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_send`](os/wasi.md).

sockets

### sock_recv

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_recv`](os/linux.md#sock_recv).

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_recv`](os/darwin.md#sock_recv).

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_recv`](os/windows.md#sock_recv).

```mach
pub fun sock_recv(fd: usize, buf: *u8, len: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_recv`](os/wasi.md).

sockets

### sock_close

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_close`](os/linux.md#sock_close).

```mach
pub fun sock_close(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_close`](os/darwin.md#sock_close).

```mach
pub fun sock_close(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_close`](os/windows.md#sock_close).

```mach
pub fun sock_close(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_close`](os/wasi.md).

sockets

### sock_create

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_create`](os/linux.md#sock_create).

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_create`](os/darwin.md#sock_create).

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_create`](os/windows.md#sock_create).

```mach
pub fun sock_create(domain: i32, typ: i32, protocol: i32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_create`](os/wasi.md).

sockets

### sock_create_flags

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_create_flags`](os/linux.md#sock_create_flags).

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_create_flags`](os/darwin.md#sock_create_flags).

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_create_flags`](os/windows.md#sock_create_flags).

```mach
pub fun sock_create_flags(domain: i32, typ: i32, protocol: i32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_create_flags`](os/wasi.md).

sockets

### sock_bind

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_bind`](os/linux.md#sock_bind).

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_bind`](os/darwin.md#sock_bind).

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_bind`](os/windows.md#sock_bind).

```mach
pub fun sock_bind(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_bind`](os/wasi.md).

sockets

### sock_listen

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_listen`](os/linux.md#sock_listen).

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_listen`](os/darwin.md#sock_listen).

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_listen`](os/windows.md#sock_listen).

```mach
pub fun sock_listen(fd: usize, backlog: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_listen`](os/wasi.md).

sockets

### sock_accept

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_accept`](os/linux.md#sock_accept).

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_accept`](os/darwin.md#sock_accept).

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_accept`](os/windows.md#sock_accept).

```mach
pub fun sock_accept(fd: usize, addr: *u8, addrlen: *u32, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_accept`](os/wasi.md).

sockets

### sock_accept_flags

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_accept_flags`](os/linux.md#sock_accept_flags).

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_accept_flags`](os/darwin.md#sock_accept_flags).

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_accept_flags`](os/windows.md#sock_accept_flags).

```mach
pub fun sock_accept_flags(fd: usize, addr: *u8, addrlen: *u32, nonblocking: bool, non_inheritable: bool, out: *usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_accept_flags`](os/wasi.md).

sockets

### sock_connect

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_connect`](os/linux.md#sock_connect).

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_connect`](os/darwin.md#sock_connect).

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_connect`](os/windows.md#sock_connect).

```mach
pub fun sock_connect(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_connect`](os/wasi.md).

sockets

### sock_sendto

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_sendto`](os/linux.md#sock_sendto).

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_sendto`](os/darwin.md#sock_sendto).

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_sendto`](os/windows.md#sock_sendto).

```mach
pub fun sock_sendto(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_sendto`](os/wasi.md).

sockets

### sock_recvfrom

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_recvfrom`](os/linux.md#sock_recvfrom).

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_recvfrom`](os/darwin.md#sock_recvfrom).

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_recvfrom`](os/windows.md#sock_recvfrom).

```mach
pub fun sock_recvfrom(fd: usize, buf: *u8, len: usize, flags: i32, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_recvfrom`](os/wasi.md).

sockets

### sock_shutdown

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_shutdown`](os/linux.md#sock_shutdown).

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_shutdown`](os/darwin.md#sock_shutdown).

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_shutdown`](os/windows.md#sock_shutdown).

```mach
pub fun sock_shutdown(fd: usize, how: i32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_shutdown`](os/wasi.md).

sockets

### sock_setopt

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_setopt`](os/linux.md#sock_setopt).

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_setopt`](os/darwin.md#sock_setopt).

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_setopt`](os/windows.md#sock_setopt).

```mach
pub fun sock_setopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_setopt`](os/wasi.md).

sockets

### sock_getopt

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_getopt`](os/linux.md#sock_getopt).

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_getopt`](os/darwin.md#sock_getopt).

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_getopt`](os/windows.md#sock_getopt).

```mach
pub fun sock_getopt(fd: usize, level: i32, opt: i32, value: *u8, vallen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_getopt`](os/wasi.md).

sockets

### sock_local_addr

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_local_addr`](os/linux.md#sock_local_addr).

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_local_addr`](os/darwin.md#sock_local_addr).

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_local_addr`](os/windows.md#sock_local_addr).

```mach
pub fun sock_local_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_local_addr`](os/wasi.md).

sockets

### sock_remote_addr

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_remote_addr`](os/linux.md#sock_remote_addr).

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_remote_addr`](os/darwin.md#sock_remote_addr).

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_remote_addr`](os/windows.md#sock_remote_addr).

```mach
pub fun sock_remote_addr(fd: usize, addr: *u8, addrlen: *u32) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_remote_addr`](os/wasi.md).

sockets

### sock_inheritable

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_inheritable`](os/linux.md#sock_inheritable).

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_inheritable`](os/darwin.md#sock_inheritable).

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_inheritable`](os/windows.md#sock_inheritable).

```mach
pub fun sock_inheritable(fd: usize, out: *bool) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_inheritable`](os/wasi.md).

sockets

### sock_connect_begin

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_connect_begin`](os/linux.md#sock_connect_begin).

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_connect_begin`](os/darwin.md#sock_connect_begin).

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_connect_begin`](os/windows.md#sock_connect_begin).

```mach
pub fun sock_connect_begin(fd: usize, addr: *u8, addrlen: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_connect_begin`](os/wasi.md).

sockets

### sock_connect_poll

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_connect_poll`](os/linux.md#sock_connect_poll).

```mach
pub fun sock_connect_poll(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_connect_poll`](os/darwin.md#sock_connect_poll).

```mach
pub fun sock_connect_poll(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_connect_poll`](os/windows.md#sock_connect_poll).

```mach
pub fun sock_connect_poll(fd: usize) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_connect_poll`](os/wasi.md).

sockets

### CONNECT_PENDING

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.CONNECT_PENDING`](os/linux.md#connect_pending).

```mach
pub val CONNECT_PENDING: i64 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.CONNECT_PENDING`](os/darwin.md#connect_pending).

```mach
pub val CONNECT_PENDING: i64 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.CONNECT_PENDING`](os/windows.md#connect_pending).

```mach
pub val CONNECT_PENDING: i64 = 1
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.CONNECT_PENDING`](os/wasi.md).

sockets

### sock_set_rcvtimeo

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.sock_set_rcvtimeo`](os/linux.md#sock_set_rcvtimeo).

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.sock_set_rcvtimeo`](os/darwin.md#sock_set_rcvtimeo).

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.sock_set_rcvtimeo`](os/windows.md#sock_set_rcvtimeo).

```mach
pub fun sock_set_rcvtimeo(fd: usize, ms: u64) i64
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.sock_set_rcvtimeo`](os/wasi.md).

sockets

### DNS_HOSTS_PATH

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.DNS_HOSTS_PATH`](os/linux.md#dns_hosts_path).

```mach
pub val DNS_HOSTS_PATH: str = "/etc/hosts"
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.DNS_HOSTS_PATH`](os/darwin.md#dns_hosts_path).

```mach
pub val DNS_HOSTS_PATH: str = "/etc/hosts"
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.DNS_HOSTS_PATH`](os/windows.md#dns_hosts_path).

```mach
pub val DNS_HOSTS_PATH: str = "C:/Windows/System32/drivers/etc/hosts"
```

Where `capability.HAS_SOCKETS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.DNS_HOSTS_PATH`](os/wasi.md).

sockets

### random_fill

Forwards the first of these whose condition holds:

- [`std.system.os.linux.random_fill`](os/linux.md#random_fill), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.random_fill`](os/darwin.md#random_fill), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.random_fill`](os/windows.md#random_fill), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.random_fill`](os/wasi.md#random_fill), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun random_fill(buf: *u8, len: usize) i64
```

random

### thread_spawn

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_spawn`](os/linux.md#thread_spawn).

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_spawn`](os/darwin.md#thread_spawn).

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_spawn`](os/windows.md#thread_spawn).

```mach
pub fun thread_spawn(
    f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_spawn`](os/wasi.md).

threads

### thread_join

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_join`](os/linux.md#thread_join).

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_join`](os/darwin.md#thread_join).

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_join`](os/windows.md#thread_join).

```mach
pub fun thread_join(native: usize, reclaimable: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_join`](os/wasi.md).

threads

### thread_detach

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_detach`](os/linux.md#thread_detach).

```mach
pub fun thread_detach(native: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_detach`](os/darwin.md#thread_detach).

```mach
pub fun thread_detach(native: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_detach`](os/windows.md#thread_detach).

```mach
pub fun thread_detach(native: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_detach`](os/wasi.md).

threads

### thread_current_id

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_current_id`](os/linux.md#thread_current_id).

```mach
pub fun thread_current_id() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_current_id`](os/darwin.md#thread_current_id).

```mach
pub fun thread_current_id() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_current_id`](os/windows.md#thread_current_id).

```mach
pub fun thread_current_id() i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_current_id`](os/wasi.md).

threads

### thread_current_name

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_current_name`](os/linux.md#thread_current_name).

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_current_name`](os/darwin.md#thread_current_name).

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_current_name`](os/windows.md#thread_current_name).

```mach
pub fun thread_current_name(name: *u8, cap: usize) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_current_name`](os/wasi.md).

threads

### thread_wait

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_wait`](os/linux.md#thread_wait).

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_wait`](os/darwin.md#thread_wait).

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_wait`](os/windows.md#thread_wait).

```mach
pub fun thread_wait(addr: *i64, expected: i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_wait`](os/wasi.md).

threads

### thread_wait_until

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_wait_until`](os/linux.md#thread_wait_until).

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_wait_until`](os/darwin.md#thread_wait_until).

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_wait_until`](os/windows.md#thread_wait_until).

```mach
pub fun thread_wait_until(addr: *i64, expected: i64, deadline: *std.system.os.shared.Timespec) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_wait_until`](os/wasi.md).

threads

### thread_wake

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_wake`](os/linux.md#thread_wake).

```mach
pub fun thread_wake(addr: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_wake`](os/darwin.md#thread_wake).

```mach
pub fun thread_wake(addr: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_wake`](os/windows.md#thread_wake).

```mach
pub fun thread_wake(addr: *i64) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_wake`](os/wasi.md).

threads

### ThreadBlock

Forwards [`std.system.os.shared.ThreadBlock`](os/shared.md#threadblock), only where `capability.HAS_THREADS`.

```mach
pub rec ThreadBlock {
    self_addr:  usize;
    stack_low:  usize;
    stack_high: usize;
}
```

threads

### thread_block

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_block`](os/linux.md#thread_block).

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_block`](os/darwin.md#thread_block).

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_block`](os/windows.md#thread_block).

```mach
pub fun thread_block() *std.system.os.shared.ThreadBlock
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_block`](os/wasi.md).

the calling thread's block, read without a system call; nil where none is installed

### thread_block_enter

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.linux`: [`std.system.os.linux.thread_block_enter`](os/linux.md#thread_block_enter).

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.darwin`: [`std.system.os.darwin.thread_block_enter`](os/darwin.md#thread_block_enter).

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.windows`: [`std.system.os.windows.thread_block_enter`](os/windows.md#thread_block_enter).

```mach
pub fun thread_block_enter(block: *std.system.os.shared.ThreadBlock) i64
```

Where `capability.HAS_THREADS` and `$mach.build.sys == $mach.sys.wasi`: [`std.system.os.wasi.thread_block_enter`](os/wasi.md).

install block as the calling thread's; the runtime does this for the main thread

### error_kind

Forwards the first of these whose condition holds:

- [`std.system.os.linux.error_kind`](os/linux.md#error_kind), where `$mach.build.sys == $mach.sys.linux`
- [`std.system.os.darwin.error_kind`](os/darwin.md#error_kind), where `$mach.build.sys == $mach.sys.darwin`
- [`std.system.os.windows.error_kind`](os/windows.md#error_kind), where `$mach.build.sys == $mach.sys.windows`
- [`std.system.os.wasi.error_kind`](os/wasi.md#error_kind), where `$mach.build.sys == $mach.sys.wasi`

```mach
pub fun error_kind(code: i64) std.io.error.Kind
```

the portable kind of a native error code

