# Process completion producer

This fixture supplies exit values from an independently compiled native C child.
The Mach parent checks `run`, `output`, and `wait_any`, including consumption and
an unchanged status output after `ECHILD`. Windows preserves all 32 bits of
`0`, `1`, `255`, `256`, `259`, `0x10000`, and `0xc0000005`. The last value is
explicitly passed to `ExitProcess`, so it is an exit value and supplies no
exception provenance. POSIX preserves the native low eight exit bits.

On POSIX, the native child also raises `SIGTERM` and `SIGSTOP`. The parent
observes signal termination and a nonconsuming stopped state, checks a no-event
probe leaves output unchanged, then explicitly kills and reaps the stopped child.
Native continuation encodings and core-dump flags have separate inline decoder
regressions.

The existing inline Windows tests use actual native failures. One substitutes a
synchronization-only duplicate while retaining the original process handle.
Waiting succeeds but `GetExitCodeProcess` is denied, then restoring the original
handle permits a retry. Another protects the process handle from closure.
Closing its job succeeds, process cleanup fails, the group token remains safe,
and removing that protection permits complete cleanup. These are native access
and close failures, not injected return codes.

The inline output ownership test supplies a failed wait after an allocated
capture. It checks exact allocator ownership and child/error propagation. It is
a result-boundary test, not an actual OS wait failure through `output`.

## Public surface

`os.ProcessStatus` has `kind: u8`, `code: u32`, `signal: i32`, and
`core_dumped: bool`. Kinds are `PROCESS_EXITED`, `PROCESS_SIGNALED`,
`PROCESS_STOPPED`, and `PROCESS_CONTINUED`. Kind zero is uninitialized, not a
successful exit. `code` is meaningful only for `PROCESS_EXITED`. `signal` is
meaningful for signal termination and stopping. `core_dumped` records the POSIX
wait-status core flag, without promising that a core file was produced.

```mach
os.wait(pid: i64, status: *os.ProcessStatus, options: i32, rusage: *u8) os.WaitResult
os.wait_pid(pid: i64, status: *os.ProcessStatus, options: i32) os.WaitResult
```

`WaitResult` contains `pid: i64` and `error: ProcessWaitError`. A positive PID is
a state observation. PID zero with `error.code == 0` is no event. A negative
`error.code` is an operation failure. No event and failure leave the supplied
status unchanged. The status pointer may be nil. Successful exit or signal
reaping consumes the child. Stop and continuation observations retain it.

`ProcessWaitError` contains `code: i64`, `native_code: u32`, and `operation: u8`.
`code` is the negative mapped OS error. Windows preserves the exact
`GetLastError` in `native_code`. POSIX uses zero there, with its errno retained in
`code`. `PROCESS_OP_WAIT`, `PROCESS_OP_STATUS`, and `PROCESS_OP_CLOSE` identify
the failed native stage. Windows accepts only zero or `WNOHANG` options and nil
rusage, and explicitly refuses unsupported requests.

`exec.ExitStatus` is the same complete status. `exec.code(status)` returns `u32`.
Every operation reports through the v5 canonical tags with `exec.Error` as the
domain tag:

| Function | Outcome |
| --- | --- |
| `run`, `run_shell`, `wait` | `res[ExitStatus, Error]` |
| `try_wait` | `res[opt[ExitStatus], Error]` |
| `wait_any` | `res[Reaped, Error]` |
| `output` | `res[Output, Error]` |
| `wait_within` | `res[Supervised, Error]` |
| `spawn*` | `res[Child, Error]` |
| `terminate_child`, `terminate_group` | `err[Error]` |
| `resolve`, `resolve_in` | `res[str, Error]` |

`Error` is a tag: `native: Failure` (a refused spawn, pipe, wait, status query,
close or termination with `code`, `native_code`, `operation` and the retained
`child`), `output: OutputFailure` (a failed capture drain with the reader's
`ReadError`, the retained `child` and the wait's failure beside it),
`alloc`, `env`, `empty_name`, `unset`, `not_found`, `ungrouped` and
`unsupported`. `exec.retained(error)` is the child an error still owns, pid
zero for none, and `error_message(error)` renders it. Spawn, pipe, read, and
termination stages use the corresponding `PROCESS_OP_*` values. If reading
fails and waiting also fails, reading remains primary and the wait cause is
kept beside it. Captured bytes are released on a failed wait.

A positive retained child transfers the remaining child owner to the caller.
Call `exec.wait(exec.retained(error))` again, or explicitly call
`terminate_child` or `terminate_group` before waiting if that is the caller's
policy. Do not discard the error while it owns a child. A zero child means no
selected pending child, including spawn refusal and `ECHILD`. An error from
`wait_any` selects no child and leaves every existing child owner with its
caller.

Serialize operations on the same child. Serialize `wait_any` with other waits
and termination of tracked children. This excludes closing native wait handles
concurrently and using a process ID after another operation reaps it. A grouped
Windows child carries a tracked group token backed by its retained process
handle. The token is valid only while the child remains owned, just like its
PID. On POSIX, `pgid` remains the native process group ID.

Windows queries completion before closing anything. Checked job closure happens
first, then checked process closure. A failed cleanup retains each still-live
handle in its existing slot. The process handle pins the PID throughout retries.
The observed completion is cached only while cleanup is pending. Closing the job
also closes its cancellation scope, so a later group termination during that
partial cleanup is an already-complete success. Final process closure consumes
the slot and invalidates its group token.

## Focused native check

`verify.sh [mach] [target] [runner]` builds the C child with `$CC` (default
`cc`), materializes this checkout under `dep/std`, builds the probe and runs
it against the child; CI runs it on every native leg beside the tracked child
termination probe. The `std.system.os.process_status` and `std.process.exec`
inline tests cover the decoders and the result boundary.

References:

- [GetExitCodeProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess)
- [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [CloseHandle](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [Windows process ID lifetime](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information)
- [Darwin wait status macros](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/sys/wait.h)
- [Linux wait status macros](https://github.com/bminor/glibc/blob/master/bits/waitstatus.h)
