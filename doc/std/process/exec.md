[std](../README.md) / [process](README.md) / **exec**

# std.process.exec

process spawning and management

Source: [`src/process/exec.mach`](../../../src/process/exec.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.io.error`](../io/error.md), [`std.process.env`](env.md), [`std.sync.cancel`](../sync/cancel.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Child`](#child) | `rec` | handle to a spawned child process |
| [`Failure`](#failure) | `rec` | a failed process operation |
| [`OutputFailure`](#outputfailure) | `rec` | the drain of a captured child's output failed |
| [`Error`](#error) | `tag` | why a process operation failed |
| [`Reaped`](#reaped) | `rec` | a child reaped by wait_any |
| [`Output`](#output) | `rec` | result of running a child process and collecting its stdout |
| [`SpawnOptions`](#spawnoptions) | `rec` | how spawn_with_options starts a child, spawn_options giving the defaults |
| [`NativeSpawnOptions`](#nativespawnoptions) | `rec` | how spawn_native_with_options starts a child: SpawnOptions with the working directory in native units |
| [`Supervised`](#supervised) | `rec` | how a supervised child ended |

| On `Child` | |
| :--- | :--- |
| [`spawn_shell`](#spawn_shell) | start a command through the host command interpreter, from `cwd` |
| [`spawn_native`](#spawn_native) | start a process from native units without waiting (see spawn_native_with_options) |
| [`spawn`](#spawn) | start a process without waiting |
| [`spawn_redirected`](#spawn_redirected) | start a process without waiting, with its stdout and/or stderr bound to caller-supplied descriptors, stdin inherited (see SpawnOptions) |
| [`spawn_grouped`](#spawn_grouped) | start a process without waiting, placed as the leader of its own new process group (see SpawnOptions) |
| [`spawn_redirected_grouped`](#spawn_redirected_grouped) | start a process without waiting, with its stdout and/or stderr bound to caller-supplied descriptors, placed as the leader of its own new process group (see SpawnOptions) |
| [`spawn_in`](#spawn_in) | start a process in a given working directory without waiting (see SpawnOptions) |
| [`spawn_redirected_in`](#spawn_redirected_in) | start a process in a given working directory with its standard streams bound to caller-supplied descriptors |
| [`spawn_redirected_in_grouped`](#spawn_redirected_in_grouped) | start a process in a given working directory, with redirected streams, as the leader of its own group (see SpawnOptions) |
| [`terminate_child`](#terminate_child) | forcefully stop a child without reaping it |
| [`terminate_group`](#terminate_group) | signal every process in a child's group, reaching descendants that spawned their own children in turn |
| [`wait`](#wait) | wait for a child process to exit |
| [`try_wait`](#try_wait) | reap a child if it has already exited, without blocking |
| [`wait_within`](#wait_within) | run a child to completion under a cancellation scope, terminating its whole group if the scope ends first |

| On `Error` | |
| :--- | :--- |
| [`retained`](#retained) | the child an error still owns: pid zero when none was retained |
| [`error_message`](#error_message) | a rendering of the error for diagnostics |
| [`run`](#run) | spawn a process and wait for it to exit |
| [`run_native`](#run_native) | spawn a process from native units and wait for it to exit (see spawn_native) |
| [`run_shell`](#run_shell) | run a command through the host command interpreter, from `cwd` |
| [`resolve`](#resolve) | resolve a user-named program to a spawnable path using PATH |
| [`resolve_in`](#resolve_in) | resolve a program name against a caller-supplied search list |

| On `Reaped` | |
| :--- | :--- |
| [`wait_any`](#wait_any) | block until any child of this process exits |

| On `Output` | |
| :--- | :--- |
| [`output`](#output-1) | run a process and collect its complete standard output |
| [`output_native`](#output_native) | run a process from native units and collect its stdout, as output does (see spawn_native) |

| On `SpawnOptions` | |
| :--- | :--- |
| [`spawn_options`](#spawn_options) | the options of a plain spawn: this process's directory, every stream inherited, and this process's group |
| [`spawn_with_options`](#spawn_with_options) | start a process without waiting, as `options` describes |

| On `NativeSpawnOptions` | |
| :--- | :--- |
| [`native_spawn_options`](#native_spawn_options) | the native options of a plain spawn, as spawn_options gives them |
| [`spawn_native_with_options`](#spawn_native_with_options) | start a process without waiting, from an executable, arguments, environment and working directory in std.runtime.native units, as `options` describes |

| Functions | |
| :--- | :--- |
| [`exited`](#exited) | check if the process exited normally |
| [`code`](#code) | get the exit code of a normally exited process |
| [`signaled`](#signaled) | check if the process was killed by a signal |
| [`signal`](#signal) | get the signal number that killed the process |
| [`stopped`](#stopped) | check if the process was stopped by a signal |
| [`stop_signal`](#stop_signal) | get the signal number that stopped the process |
| [`continued`](#continued) | check if a stopped process was continued |
| [`exit`](#exit) | terminate the current process |

| Forwards | |
| :--- | :--- |
| [`ExitStatus`](#exitstatus), [`PROCESS_EXITED`](#process_exited), [`PROCESS_SIGNALED`](#process_signaled), [`PROCESS_STOPPED`](#process_stopped), [`PROCESS_CONTINUED`](#process_continued) | |
| [`Environment`](#environment) | the environment a spawn hands its child, given or inherited |
| [`NativeEnvironment`](#nativeenvironment) | |

---

## Child

```mach
pub rec Child {
    pid:  i64;
    pgid: i64;
}
```

handle to a spawned child process

| Field | Type | |
| :--- | :--- | :--- |
| `pid` | `i64` | process id of the child |
| `pgid` | `i64` | 0 if the child was not placed in its own group (see SpawnOptions.grouped); otherwise the group token needed to signal the whole group - on linux/darwin this is the posix process group id (pgid == pid, since the child is its own group's leader); on windows it is a tracked group token backed by the retained child process |

### spawn_shell

```mach
pub fun spawn_shell(command: str, cwd: str, envp: std.system.os.Environment) res[Child, Error]
```

start a command through the host command interpreter, from `cwd`

the same interpreter and conventions as run_shell, without waiting

| Parameter | |
| :--- | :--- |
| `command` | the command line to run |
| `cwd` | working directory for the child, or nil to inherit |
| `envp` | the child's environment, given entries or inherited |
| **returns** | the running child, or the refusal |

### spawn_native

```mach
pub fun spawn_native(pathname: *Unit, argv: **Unit, envp: std.system.os.NativeEnvironment) res[Child, Error]
```

start a process from native units without waiting (see
spawn_native_with_options)

| Parameter | |
| :--- | :--- |
| **returns** | child handle, or the spawn failure |

### spawn

```mach
pub fun spawn(pathname: str, argv: **u8, envp: std.system.os.Environment) res[Child, Error]
```

start a process without waiting

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | child handle, or the spawn failure |

### spawn_redirected

```mach
pub fun spawn_redirected(pathname: str, argv: **u8, envp: std.system.os.Environment, stdout_fd: usize, stderr_fd: usize) res[Child, Error]
```

start a process without waiting, with its stdout and/or stderr bound to
caller-supplied descriptors, stdin inherited (see SpawnOptions)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `stdout_fd` | handle for the child's stdout, or os.INVALID_HANDLE to inherit |
| `stderr_fd` | handle for the child's stderr, or os.INVALID_HANDLE to inherit |
| **returns** | child handle, or the spawn failure |

### spawn_grouped

```mach
pub fun spawn_grouped(pathname: str, argv: **u8, envp: std.system.os.Environment) res[Child, Error]
```

start a process without waiting, placed as the leader of its own new
process group (see SpawnOptions)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | child handle, or the spawn failure |

### spawn_redirected_grouped

```mach
pub fun spawn_redirected_grouped(pathname: str, argv: **u8, envp: std.system.os.Environment, stdout_fd: usize, stderr_fd: usize) res[Child, Error]
```

start a process without waiting, with its stdout and/or stderr bound to
caller-supplied descriptors, placed as the leader of its own new process
group (see SpawnOptions)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `stdout_fd` | handle for the child's stdout, or os.INVALID_HANDLE to inherit |
| `stderr_fd` | handle for the child's stderr, or os.INVALID_HANDLE to inherit |
| **returns** | child handle, or the spawn failure |

### spawn_in

```mach
pub fun spawn_in(pathname: str, argv: **u8, envp: std.system.os.Environment, cwd: str) res[Child, Error]
```

start a process in a given working directory without waiting (see
SpawnOptions)

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `cwd` | directory to run in, or empty to inherit this process's |
| **returns** | child handle, or the spawn failure |

### spawn_redirected_in

```mach
pub fun spawn_redirected_in(pathname: str, argv: **u8, envp: std.system.os.Environment, cwd: str,
    stdin_fd: usize, stdout_fd: usize,
    stderr_fd: usize) res[Child, Error]
```

start a process in a given working directory with its standard streams bound
to caller-supplied descriptors

| Parameter | |
| :--- | :--- |
| `cwd` | directory to run in, or empty to inherit this process's |
| `stdin_fd` | handle for the child's stdin, or os.INVALID_HANDLE to inherit |
| `stdout_fd` | handle for the child's stdout, or os.INVALID_HANDLE to inherit |
| `stderr_fd` | handle for the child's stderr, or os.INVALID_HANDLE to inherit |
| **returns** | child handle, or the spawn failure |

### spawn_redirected_in_grouped

```mach
pub fun spawn_redirected_in_grouped(pathname: str, argv: **u8, envp: std.system.os.Environment, cwd: str,
    stdin_fd: usize, stdout_fd: usize,
    stderr_fd: usize) res[Child, Error]
```

start a process in a given working directory, with redirected streams, as the
leader of its own group (see SpawnOptions)

| Parameter | |
| :--- | :--- |
| **returns** | child handle whose pgid identifies the group, or the spawn failure |

### terminate_child

```mach
pub fun terminate_child(child: Child) err[Error]
```

forcefully stop a child without reaping it

the child remains waitable after this succeeds. callers must still pass it
to wait (or collect it through wait_any) to obtain its status and release
retained platform resources.

terminate_child, wait, and wait_any must not run concurrently for the same
child. once one of the wait operations begins reaping a child, its numeric
process ID can be released for reuse.

| Parameter | |
| :--- | :--- |
| `child` | child handle from spawn |
| **returns** | the native failure, which keeps the child with the caller |

### terminate_group

```mach
pub fun terminate_group(child: Child) err[Error]
```

signal every process in a child's group, reaching descendants that spawned
their own children in turn

`ungrouped` when `child` was not spawned grouped (child.pgid == 0): there is
no group to signal.
member processes remain individually waitable afterward, exactly as
terminate_child leaves a single child waitable.

| Parameter | |
| :--- | :--- |
| `child` | child handle from a grouped spawn |
| **returns** | the native failure, which keeps the child with the caller |

### wait

```mach
pub fun wait(child: Child) res[ExitStatus, Error]
```

wait for a child process to exit

a signal that interrupts the wait is not a failure and is not reported as
one: the wait is reissued until the child is reaped. the os layer bounds its
own retries and surfaces exhaustion as EINTR, so a wrapper that treated that
sentinel as terminal would turn a transient interruption into a permanent
error and leave the child unreaped.

| Parameter | |
| :--- | :--- |
| `child` | child handle from spawn |
| **returns** | exit status, or a typed error retaining any unreaped child |

### try_wait

```mach
pub fun try_wait(child: Child) res[opt[ExitStatus], Error]
```

reap a child if it has already exited, without blocking

this is the piece a caller needs to enforce a deadline: blocking in wait
gives up the ability to notice that a scope expired, so a supervisor polls
with this instead and keeps its own timing.

a child that is still running is not an error; the result is simply absent.
an interrupted probe is likewise not an error: it is reissued, so absent
always means still running and never means interrupted.

| Parameter | |
| :--- | :--- |
| `child` | child handle from any spawn |
| **returns** | the exit status if it has terminated, absent if it is still running, or a typed error retaining any unreaped child |

### wait_within

```mach
pub fun wait_within(child: Child, scope: *std.sync.cancel.Scope) res[Supervised, Error]
```

run a child to completion under a cancellation scope, terminating its whole
group if the scope ends first

this is the piece that makes a deadline mean something for a process. a scope
with a deadline is only a promise until somebody enforces it, and enforcing it
on a single child is not enough when that child spawned children of its own: a
build step that runs a shell that runs a compiler leaves the compiler running
if only the shell is signalled. so the group is what gets terminated, which is
why the child should come from one of the grouped spawns.

successful supervision reaps the child. a wait or termination failure returns
its retained child for explicit retry or cleanup, alongside the original cause.

a child that is not in a group is still supervised; expiry then terminates
just that child, and any grandchildren it started survive. that is a weaker
guarantee, not a silent one: prefer a grouped spawn when the child may spawn.

| Parameter | |
| :--- | :--- |
| `child` | child handle, ideally from a grouped spawn |
| `scope` | the scope whose deadline or cancellation bounds the child |
| **returns** | how it ended, or a typed error retaining any unreaped child |

## Failure

```mach
pub rec Failure {
    kind:        std.io.error.Kind;
    code:        i64;
    native_code: u32;
    operation:   u8;
    child:       Child;
}
```

a failed process operation

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `std.io.error.Kind` | the portable classification |
| `code` | `i64` | the native code behind the failure, zero when the refusal is this module's own |
| `native_code` | `u32` | the exact windows GetLastError; zero on posix |
| `operation` | `u8` | the os.PROCESS_OP_* stage that failed |
| `child` | `Child` | the unreaped child transferred to the caller, pid zero for none |

## OutputFailure

```mach
pub rec OutputFailure {
    read:  ReadError;
    child: Child;
    wait:  opt[std.system.os.ProcessWaitError];
}
```

the drain of a captured child's output failed

| Field | Type | |
| :--- | :--- | :--- |
| `read` | `ReadError` | the reader's failure, with the bytes delivered before it |
| `child` | `Child` | the unreaped child transferred to the caller when the wait that followed the drain failed too, pid zero when the wait reaped it |
| `wait` | `opt[std.system.os.ProcessWaitError]` | that wait's native failure, absent when the wait succeeded |

## Error

```mach
pub tag Error: u8 {
    native: Failure;
    output: OutputFailure;
    alloc:  std.allocator.Error;
    env:    std.process.env.EnvError;
    empty_name;
    unset;
    not_found;
    ungrouped;
    unsupported;
    query: std.io.error.Error;
}
```

why a process operation failed

| Case | Payload | |
| :--- | :--- | :--- |
| `native` | `Failure` | a spawn, pipe, wait, status query, close or termination refused by the platform; the child it retains is the caller's to wait for again, or to terminate first, before releasing ownership |
| `output` | `OutputFailure` | the capture drain failed (the wait's outcome is inside) |
| `alloc` | `std.allocator.Error` | an owned path copy was refused |
| `env` | `std.process.env.EnvError` | the PATH read failed |
| `empty_name` |  | the program name is empty |
| `unset` |  | PATH is not set |
| `not_found` |  | the name is on no directory of the search list |
| `ungrouped` |  | the child was not spawned into a group, so no group can be signalled |
| `unsupported` |  | process groups do not exist on this platform |
| `query` | `std.io.error.Error` | the name was found nowhere, and at least one candidate could not be examined (the last such failure); the search continues past a refused query the way execvp does, so a hit still wins |

### retained

```mach
pub fun retained(error: Error) Child
```

the child an error still owns: pid zero when none was retained. do not
discard an error while it owns a child; wait for it or terminate it first

### error_message

```mach
pub fun error_message(error: Error) str
```

a rendering of the error for diagnostics

### run

```mach
pub fun run(pathname: str, argv: **u8, envp: std.system.os.Environment) res[ExitStatus, Error]
```

spawn a process and wait for it to exit

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | exit status, or an error retaining an unreaped child |

### run_native

```mach
pub fun run_native(pathname: *Unit, argv: **Unit, envp: std.system.os.NativeEnvironment) res[ExitStatus, Error]
```

spawn a process from native units and wait for it to exit (see spawn_native)

| Parameter | |
| :--- | :--- |
| **returns** | exit status, or an error retaining an unreaped child |

### run_shell

```mach
pub fun run_shell(command: str, cwd: str, envp: std.system.os.Environment) res[ExitStatus, Error]
```

run a command through the host command interpreter, from `cwd`

The interpreter and its command-line conventions are the platform's, not the
caller's: posix hands `sh -c <command>` straight to execve, while windows
resolves %ComSpec% and emits `"<comspec>" /s /c "<command verbatim>"`. That
split matters because a command line's encoding is a property of the program
being spawned - the CRT argv convention every other spawn here uses is not
what cmd.exe parses, so a caller assembling its own shell invocation would
have to know which convention applies and would get it wrong.

`cwd` is applied in the child, so the caller's own working directory is
untouched and the directory never enters the command line.

| Parameter | |
| :--- | :--- |
| `command` | the command line to run |
| `cwd` | working directory for the child, or nil to inherit |
| `envp` | the child's environment, given entries or inherited |
| **returns** | exit status, or an error retaining an unreaped child |

### resolve

```mach
pub fun resolve(a: *std.allocator.Allocator, name: str) res[str, Error]
```

resolve a user-named program to a spawnable path using PATH

none of the spawn entry points searches PATH: execve resolves nothing, and
the windows layer passes a non-NULL lpApplicationName. a caller spawning a
program the USER names rather than a fixed path resolves it here first.

PATH is the only source. the current directory is never consulted, so a
binary committed into a working tree cannot shadow the real tool.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `name` | program name, bare or already pathed |
| **returns** | an owned spawnable path (extent is its length plus the terminator, released with text.string.str_free), or the failure |

### resolve_in

```mach
pub fun resolve_in(a: *std.allocator.Allocator, name: str, search: str) res[str, Error]
```

resolve a program name against a caller-supplied search list

the search policy, with the environment read left to `resolve`. a caller with
its own list - a configured toolchain directory, a sandbox - searches it here
without going through PATH, and the policy stays testable without a way to
set an environment variable.

`search` is PATH-shaped and is NOT modified: entries separated by `;` on
windows and `:` elsewhere. an EMPTY entry is skipped rather than treated as
the current directory, which is the whole point of this function existing -
letting the OS search would put the working directory ahead of the real tool
on windows.

a name that already spells a path is returned unresolved and unprobed. the
result is owned by the caller in BOTH cases, so the free is unconditional.
returning the borrowed argument for pathed names would make ownership depend
on the value, which is how a caller ends up leaking one path and double
freeing the other.

a refused copy anywhere in the walk is the allocator's error, never a
directory silently skipped: a search that could not look everywhere does
not get to answer `not_found`.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `name` | program name, bare or already pathed |
| `search` | PATH-shaped list of directories, searched in order |
| **returns** | an owned spawnable path, or the failure |

## Reaped

```mach
pub rec Reaped {
    child:  Child;
    status: ExitStatus;
}
```

a child reaped by wait_any

| Field | Type | |
| :--- | :--- | :--- |
| `child` | `Child` | the reaped child's handle |
| `status` | `ExitStatus` | its exit status |

### wait_any

```mach
pub fun wait_any() res[Reaped, Error]
```

block until any child of this process exits

POSIX wait(-1) semantics on every platform (the windows layer emulates the
-1 pid by waiting across its tracked child handles). the returned pair
identifies which child was reaped and how it exited, so a caller juggling
several children can map the exit back to its work item. errs when there is
no child to wait for.

serialize waits on the same child, and wait_any with all waits and termination
an error without a selected child leaves every existing child owner with its caller

an interrupting signal is retried rather than reported, as in wait.

| Parameter | |
| :--- | :--- |
| **returns** | the reaped child and its exit status, or a typed wait error |

## Output

```mach
pub rec Output {
    status: ExitStatus;
    bytes:  Vector[u8];
}
```

result of running a child process and collecting its stdout

| Field | Type | |
| :--- | :--- | :--- |
| `status` | `ExitStatus` | exit status of the child process |
| `bytes` | `Vector[u8]` | the child's complete stdout, owned by the caller's allocator |

### output

```mach
pub fun output(a: *std.allocator.Allocator, pathname: str, argv: **u8, envp: std.system.os.Environment) res[Output, Error]
```

run a process and collect its complete standard output

spawns the child with stdout bound to a pipe and drains it to end-of-file
through io.read_all over the pipe's read end, so output of any length is
captured and the child never blocks on a full pipe. a wait is attempted even
when the drain fails, and a failed wait returns the remaining child owner.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the captured output |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| **returns** | the exit status and captured stdout, or an error |

### output_native

```mach
pub fun output_native(a: *std.allocator.Allocator, pathname: *Unit, argv: **Unit, envp: std.system.os.NativeEnvironment) res[Output, Error]
```

run a process from native units and collect its stdout, as output does (see
spawn_native)

| Parameter | |
| :--- | :--- |
| **returns** | the exit status and captured stdout, or an error |

## SpawnOptions

```mach
pub rec SpawnOptions {
    cwd:     str;
    stdin:   usize;
    stdout:  usize;
    stderr:  usize;
    grouped: bool;
}
```

how spawn_with_options starts a child, spawn_options giving the defaults

the working directory is applied in the child after the fork and before the
exec, so this process's own directory is never disturbed and two spawns into
different directories cannot race. the parent keeps ownership of every
redirected handle: close it after the child exits, or right after the spawn
to let a pipe's read end see end-of-file.

a grouped child leads a new process group (a job object on windows), so
terminate_group later reaches the whole tree at once. a caller whose child
may spawn children of its own, such as a shell running a compiler, wants
this: terminate_child would leave the grandchildren orphaned and running.

| Field | Type | |
| :--- | :--- | :--- |
| `cwd` | `str` | directory to run in, or empty to inherit this process's |
| `stdin` | `usize` | handle for the child's stdin, or os.INVALID_HANDLE to inherit |
| `stdout` | `usize` | handle for the child's stdout, or os.INVALID_HANDLE to inherit |
| `stderr` | `usize` | handle for the child's stderr, or os.INVALID_HANDLE to inherit |
| `grouped` | `bool` | place the child as the leader of its own new process group |

### spawn_options

```mach
pub fun spawn_options() SpawnOptions
```

the options of a plain spawn: this process's directory, every stream
inherited, and this process's group

### spawn_with_options

```mach
pub fun spawn_with_options(pathname: str, argv: **u8, envp: std.system.os.Environment, options: SpawnOptions) res[Child, Error]
```

start a process without waiting, as `options` describes

every spawn of this module is this one with some options set.

| Parameter | |
| :--- | :--- |
| `pathname` | path to executable |
| `argv` | null-terminated argument array |
| `envp` | the child's environment, given entries or inherited |
| `options` | directory, stream redirections and grouping (see SpawnOptions) |
| **returns** | child handle, whose pgid names the group when grouped, or the spawn failure |

## NativeSpawnOptions

```mach
pub rec NativeSpawnOptions {
    cwd:     *Unit;
    stdin:   usize;
    stdout:  usize;
    stderr:  usize;
    grouped: bool;
}
```

how spawn_native_with_options starts a child: SpawnOptions with the working
directory in native units

| Field | Type | |
| :--- | :--- | :--- |
| `cwd` | `*Unit` | nul-terminated directory to run in, or nil or empty to inherit |
| `stdin` | `usize` | handle for the child's stdin, or os.INVALID_HANDLE to inherit |
| `stdout` | `usize` | handle for the child's stdout, or os.INVALID_HANDLE to inherit |
| `stderr` | `usize` | handle for the child's stderr, or os.INVALID_HANDLE to inherit |
| `grouped` | `bool` | place the child as the leader of its own new process group |

### native_spawn_options

```mach
pub fun native_spawn_options() NativeSpawnOptions
```

the native options of a plain spawn, as spawn_options gives them

### spawn_native_with_options

```mach
pub fun spawn_native_with_options(pathname: *Unit, argv: **Unit, envp: std.system.os.NativeEnvironment, options: NativeSpawnOptions) res[Child, Error]
```

start a process without waiting, from an executable, arguments, environment
and working directory in std.runtime.native units, as `options` describes

the units reach the kernel unchanged: bytes on linux and darwin, valid UTF-8
or not, and UTF-16 on windows, where an unpaired surrogate launches, starts
in or reaches the child as given. an argument read from std.runtime.native
passes to a child exactly. spawn_with_options is this call for UTF-8, and on
windows it converts each string once and runs this

| Parameter | |
| :--- | :--- |
| `pathname` | nul-terminated path to executable |
| `argv` | null-terminated array of nul-terminated arguments |
| `envp` | the child's environment, given native entries or inherited |
| `options` | directory, stream redirections and grouping |
| **returns** | child handle, whose pgid names the group when grouped, or the spawn failure |

## Supervised

```mach
pub rec Supervised {
    status: ExitStatus;
    # true when the deadline or a cancellation ended it rather than the child
    # finishing on its own
    terminated: bool;
    # the reason the scope carried when it ended, ACTIVE when the child won
    reason: std.sync.cancel.Reason;
}
```

how a supervised child ended

## Functions

### exited

```mach
pub fun exited(status: ExitStatus) bool
```

check if the process exited normally

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | true if the process called exit |

### code

```mach
pub fun code(status: ExitStatus) u32
```

get the exit code of a normally exited process

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | full u32 exit code, only valid if exited() is true |

### signaled

```mach
pub fun signaled(status: ExitStatus) bool
```

check if the process was killed by a signal

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | true if terminated by signal |

### signal

```mach
pub fun signal(status: ExitStatus) i32
```

get the signal number that killed the process

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | signal number |

### stopped

```mach
pub fun stopped(status: ExitStatus) bool
```

check if the process was stopped by a signal

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | true for a stop observation |

### stop_signal

```mach
pub fun stop_signal(status: ExitStatus) i32
```

get the signal number that stopped the process

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | signal number, only valid if stopped() is true |

### continued

```mach
pub fun continued(status: ExitStatus) bool
```

check if a stopped process was continued

| Parameter | |
| :--- | :--- |
| `status` | exit status to inspect |
| **returns** | true for a continuation observation |

### exit

```mach
pub fun exit(code: i64)
```

terminate the current process

| Parameter | |
| :--- | :--- |
| `code` | exit code |

## Forwards

### ExitStatus

Forwards [`std.system.os.ProcessStatus`](../system/os.md#processstatus), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub rec ProcessStatus {
    kind:        u8;
    code:        u32;
    signal:      i32;
    core_dumped: bool;
}
```

### PROCESS_EXITED

Forwards [`std.system.os.PROCESS_EXITED`](../system/os.md#process_exited), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub val PROCESS_EXITED:    u8 = 1
```

a process state observation, with a full native windows exit code

### PROCESS_SIGNALED

Forwards [`std.system.os.PROCESS_SIGNALED`](../system/os.md#process_signaled), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub val PROCESS_SIGNALED:  u8 = 2
```

### PROCESS_STOPPED

Forwards [`std.system.os.PROCESS_STOPPED`](../system/os.md#process_stopped), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub val PROCESS_STOPPED:   u8 = 3
```

### PROCESS_CONTINUED

Forwards [`std.system.os.PROCESS_CONTINUED`](../system/os.md#process_continued), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub val PROCESS_CONTINUED: u8 = 4
```

### Environment

Forwards [`std.system.os.Environment`](../system/os.md#environment), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub def Environment: EnvironmentOf[u8]
```

the environment a spawn hands its child, given or inherited

Environment.inherit{} is the one way to pass this process's environment on.
the child gets it in native units with no conversion: CreateProcessW's NULL
environment on windows, the envp the kernel gave this process on linux and
darwin, so a variable with no UTF-8 spelling reaches the child as it is.
Environment.given{envp} hands the child exactly the NAME=value entries of a
nil-terminated array, and a nil array is refused with an INVALID error.
NativeEnvironment is the native spawns' form, its entries in
std.runtime.native units

### NativeEnvironment

Forwards [`std.system.os.NativeEnvironment`](../system/os.md#nativeenvironment), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_PROCESS && capability.HAS_THREADS`.

```mach
pub def NativeEnvironment: EnvironmentOf[Unit]
```

the environment of a native spawn, its entries in std.runtime.native units.
on linux and darwin the units are bytes, so it is Environment itself

