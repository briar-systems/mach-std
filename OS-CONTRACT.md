# The std.system.os contract

`std.system.os` is a small, explicit contract of OS primitives with one implementation per operating system (`std.system.os.linux`, `.darwin`, `.windows`). Everything else in std is built on top of it. This page describes the contract as it stands in std **4.0.0** (epic #697).

## Capability groups

The contract is split into independent groups. `std.system.capability` exports one comptime flag per group. A module gates OS-bound code on a flag with `$if`, and the unselected branch, OS-bound imports included, is discarded before resolution:

```mach
use std.system.capability;

$if (capability.HAS_FILES) {
    use std.system.os;
    # code that needs files
}
```

Every group is present on linux, darwin and windows. None is present on any other target, freestanding included. `HOSTED` is the core group, which every other group implies.

A target that claims a group exports every member listed here. `src/system/capability/conformance.mach` names every member of every group that the per-OS module supplies, so a missing member fails the build on any target that claims the group. Members `std.system.os` defines itself (the secret primitives `allocate_secret`, `allocate_secret_typed`, `release_secret`, `release_secret_typed`, `random_fill_secret`, `read_at_secret` and `write_at_secret`, `stdin`, `stdout`, `stderr`, `working_dir`, `exit`, `panic_sink`, and `realtime`, `monotonic`, `error`, `error_message` and `message`) exist wherever the module compiles, so the test doesn't name them. The test also keeps the positioned secret transfers inside the files lane, which `test/secret/verify.sh` enforces.

| flag | group | purpose |
| --- | --- | --- |
| `HOSTED` | core | required by every hosted std module: the translation of a native code into an `io.error.Error` (`error`, `error_kind`, `error_message`, `message`), and process termination |
| `HAS_PAGES` | pages | page allocation, protection, locking and advice, and secret-welded storage |
| `HAS_CLOCK` | clock | the realtime and monotonic clocks, and sleep |
| `HAS_ENTROPY` | entropy | cryptographic random fill, public and secret |
| `HAS_THREADS` | threads | thread spawn and join, futex-shaped wait and wake, and the cpu count |
| `HAS_FILES` | files | descriptors, positioned and secret I/O, stat, directories, identity, publication, pipes and the working directory |
| `HAS_IO_QUEUE` | io queue | the native completion or readiness queue |
| `HAS_SOCKETS` | sockets | stream, datagram and local sockets, their options and address codecs |
| `HAS_PROCESS` | process | spawn, wait, status decoding, the environment and signal disposition |

## Members

### core (`HOSTED`)

`abort`, `error`, `error_kind`, `error_message`, `exit`, `message`, `panic_sink`

### pages (`HAS_PAGES`)

`ADVISE_DONT_NEED`, `ADVISE_NORMAL`, `ADVISE_RANDOM`, `ADVISE_SEQUENTIAL`, `ADVISE_WILL_NEED`, `PROT_EXEC`, `PROT_NONE`, `PROT_READ`, `PROT_WRITE`, `advise`, `allocate`, `allocate_secret`, `allocate_secret_typed`, `deallocate`, `heap_region_base`, `heap_region_extend`, `lock`, `page_size`, `protect`, `reallocate`, `release_secret`, `release_secret_typed`, `unlock`

### clock (`HAS_CLOCK`)

`Timespec`, `monotonic`, `realtime`, `sleep`

### entropy (`HAS_ENTROPY`)

`RANDOM_FILL_SECRET_MAX`, `random_fill`, `random_fill_secret`

### threads (`HAS_THREADS`)

`cpu_count`, `thread_current_id`, `thread_current_name`, `thread_detach`, `thread_join`, `thread_spawn`, `thread_wait`, `thread_wait_until`, `thread_wake`

### files (`HAS_FILES`)

`AT_REMOVEDIR`, `AT_SYMLINK_NOFOLLOW`, `DirectoryCursor`, `DirectoryEntry`, `DirectoryInitResult`, `INVALID_HANDLE`, `LOCK_EX`, `LOCK_NB`, `LOCK_SH`, `LOCK_UN`, `O_APPEND`, `O_CREAT`, `O_DIRECTORY`, `O_EXCL`, `O_RDONLY`, `O_RDWR`, `O_TRUNC`, `O_WRONLY`, `PUBLICATION_CLAIMS`, `PUBLICATION_READ_RETAIN_REPLACE`, `PUBLICATION_RETAIN_REPLACE`, `SEEK_CUR`, `SEEK_END`, `SEEK_SET`, `S_IFDIR`, `S_IFLNK`, `S_IFMT`, `S_IFREG`, `access`, `close`, `directory_close`, `directory_init`, `directory_next`, `file_identity`, `getcwd`, `identity_at`, `lock_fd`, `make_dir`, `map_file`, `open`, `pipe`, `publication_capabilities`, `read`, `read_at_secret`, `rename`, `retain_identity_at`, `seek`, `set_mode`, `set_mode_at`, `stat`, `stat_path`, `stat_t`, `stderr`, `stdin`, `stdout`, `symlink`, `sync_fd`, `sync_file`, `unlink`, `working_dir`, `write`, `write_at_secret`

### io queue (`HAS_IO_QUEUE`)

`IoQueue`, `io_queue_close`, `io_queue_create`, `io_queue_wait`, `io_queue_wake`

### sockets (`HAS_SOCKETS`)

`AF_INET`, `AF_INET6`, `DNS_HOSTS_PATH`, `IPPROTO_IP`, `IPPROTO_IPV6`, `IPPROTO_TCP`, `IPV6_TCLASS`, `IPV6_V6ONLY`, `IP_TOS`, `SHUT_RD`, `SHUT_RDWR`, `SHUT_WR`, `SOCKADDR_IN6_SIZE`, `SOCKADDR_IN_SIZE`, `SOCKADDR_STORAGE_SIZE`, `SOCK_DGRAM`, `SOCK_STREAM`, `SOL_SOCKET`, `SO_EXCLUSIVEADDRUSE`, `SO_KEEPALIVE`, `SO_LINGER`, `SO_RCVBUF`, `SO_RCVTIMEO`, `SO_REUSEADDR`, `SO_REUSEPORT`, `SO_SNDBUF`, `SO_UNSUPPORTED`, `TCP_FASTOPEN`, `TCP_KEEPCNT`, `TCP_KEEPIDLE`, `TCP_KEEPINTVL`, `TCP_NODELAY`, `sock_accept`, `sock_accept_flags`, `sock_bind`, `sock_close`, `sock_connect`, `sock_create`, `sock_create_flags`, `sock_getopt`, `sock_inheritable`, `sock_listen`, `sock_local_addr`, `sock_recv`, `sock_recvfrom`, `sock_remote_addr`, `sock_send`, `sock_sendto`, `sock_set_rcvtimeo`, `sock_setopt`, `sock_shutdown`

### process (`HAS_PROCESS`)

`PROCESS_CONTINUED`, `PROCESS_EXITED`, `PROCESS_OP_CLOSE`, `PROCESS_OP_PIPE`, `PROCESS_OP_READ`, `PROCESS_OP_SPAWN`, `PROCESS_OP_STATUS`, `PROCESS_OP_TERMINATE`, `PROCESS_OP_WAIT`, `PROCESS_SIGNALED`, `PROCESS_STOPPED`, `ProcessStatus`, `ProcessWaitError`, `WNOHANG`, `WaitResult`, `environ`, `getenv`, `getpid`, `ignore_sigpipe`, `spawn`, `spawn_in`, `spawn_redirected`, `spawn_redirected_in`, `terminate_child`, `wait`, `wait_pid`

## Assumptions

The contract is designed so that a user-supplied implementation, for a kernel or UEFI, can provide it without changing any consumer. It holds to these assumptions:

- **A1, codes.** A fallible primitive returns `i64`: `>= 0` is success and `< 0` is an opaque native code. Only the implementation interprets a code. The `E*` constants are not on the portable surface, only in the per-OS modules, and `os.error_kind(code)` is the only portable reading of a code.
- **A2, handles.** Resources are pointer-width opaque values. Descriptors are `usize` handles. A primitive that creates one returns it through an out parameter with an `i64` status, `INVALID_HANDLE` means none, and the standard handles and the working directory are functions (`stdin()`, `stdout()`, `stderr()`, `working_dir()`). The per-OS modules keep their native `i32` descriptors.
- **A3, no ambient process model.** Nothing assumes environment variables, a working directory, signals, standard streams or a process table unless it belongs to the group that provides them (process, files).
- **A4, secret shape.** Primitives that touch secret-welded storage take `*^u8` and never downgrade it.
- **A5, no hidden initialization.** The implementation owns its state. std calls no init hook beyond what `std.runtime` or the embedder already runs.
- **A6, memory.** Pages come back zeroed and page-aligned. `protect`, `lock` and `advise` may be unsupported, and callers accept that.

## Changes from 3.x

- The errno constants left the portable surface. `os.error(code, op)`, `os.error_kind(code)`, `os.error_message(code)` and `os.message(Error)` form the error part of the core group.
- Logic built on top of the primitives moved out: secret borrows to `std.memory.secret`, sockaddr codecs to `std.net.ip`, status decoders and `spawn_shell` to `std.process.exec`, `temp_dir`, `unlink_force` and `stat_mode` to `std.filesystem.native`, and the path separator to `std.types.path.separator()`.
- Descriptors became `usize` handles, `terminate` became `exit(status: u32)`, and `panic_sink` joined the core group.

How a user-supplied implementation is selected is an open design question. The candidates are comptime module selection, link-time symbols, dependency substitution and a runtime function table. Any of them needs the `HAS_*` flags to stay comptime.
