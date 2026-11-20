[std](../README.md) / [sync](README.md) / **thread**

# std.sync.thread

thread creation and resource ownership

every spawned thread has one private owner record. the public handle may move
after spawn because target trampolines refer to that record, never the handle.
a joinable thread leaves the record for join. detach transfers it to the
exiting thread, which releases it after the user context has been destroyed.

where a thread comes from
a static linux executable has no loader, so std creates its threads itself
with clone. macOS and Windows threads always come from the system (pthread_create
through libSystem, and CreateThread). a loader-hosted linux process is one the
kernel started with an interpreter, or a shared library, which is loader-hosted
by construction. thread-locals and any C runtime's per-thread state exist there
only on threads the host creates, so std never clones one. spawn goes through
a backend the program installs, and with none installed it returns
ThreadError.unsupported and starts nothing.

a shared library, a dynamic executable or anything that links a C library on
linux therefore needs a backend before any std thread can start, including the
ones std.log, std.io.runtime and std.sync.worker_pool spawn. std names no libc
symbol, so a host-thread backend is a package of its own, and a program installs
it by depending on it and importing one of its modules, which is what puts its
definitions in the link. replacement is link time only, so a shared library that
carries std needs the backend in its own link, and no other image can supply
it. exactly one backend belongs in a link, and two fail it. the override is the
three symbols OS-CONTRACT.md specifies, and nothing checks their shapes.

Source: [`src/sync/thread.mach`](../../../src/sync/thread.mach)

Uses types from [`std.io.error`](../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`ThreadError`](#threaderror) | `tag` | a refused thread operation |
| [`Operation`](#operation) | `def` |  |
| [`Config`](#config) | `rec` | portable thread creation policy |
| [`Thread`](#thread) | `rec` | handle to a spawned thread |
| [`Token`](#token) | `def` | the calling thread's identity, as current_token returns it |
| [`CpuSet`](#cpuset) | `rec` | a set of CPUs over words the caller owns |

| On `ThreadError` | |
| :--- | :--- |
| [`code`](#code) | the portable status code of an error, for diagnostics that keep an i64 |

| On `Config` | |
| :--- | :--- |
| [`config_default`](#config_default) | initialize a thread configuration with portable defaults |
| [`spawn_with_config`](#spawn_with_config) | spawn with borrowed caller context and explicit configuration |
| [`spawn_owned_with_config`](#spawn_owned_with_config) | spawn with owned caller context and explicit configuration |
| [`spawn_config`](#spawn_config) | spawn a zero-argument function with explicit configuration |

| On `Thread` | |
| :--- | :--- |
| [`spawn_with`](#spawn_with) | spawn with borrowed caller context and default configuration |
| [`spawn_owned`](#spawn_owned) | spawn with owned caller context and default configuration |
| [`spawn`](#spawn) | spawn a zero-argument function with default configuration |
| [`join`](#join) | join and release every library-owned resource |
| [`detach`](#detach) | transfer ownership to the running or completed thread |
| [`is_done`](#is_done) | check whether a joinable thread body has finished |
| [`diagnostic_id`](#diagnostic_id) | return the stable native diagnostic identifier captured at spawn |

| On `Token` | |
| :--- | :--- |
| [`current_token`](#current_token) | the calling thread's identity, read without a system call |

| On `CpuSet` | |
| :--- | :--- |
| [`cpu_set`](#cpu_set) | an empty CPU set over caller-provided words |
| [`cpu_set_clear`](#cpu_set_clear) | remove every CPU from the set |
| [`cpu_set_add`](#cpu_set_add) | add a CPU to the set |
| [`cpu_set_contains`](#cpu_set_contains) | whether a CPU is in the set |
| [`cpu_set_size`](#cpu_set_size) | the number of CPUs in the set |
| [`cpu_set_nth`](#cpu_set_nth) | the n-th CPU in the set, counting from zero in ascending index order |
| [`current_affinity`](#current_affinity) | read the calling thread's CPU affinity into set |
| [`set_current_affinity`](#set_current_affinity) | pin the calling thread to the CPUs in set |

| Functions | |
| :--- | :--- |
| [`affinity_words`](#affinity_words) | the number of words a CPU set needs to hold the calling thread's affinity |
| [`pin_current_to`](#pin_current_to) | pin the calling thread to one CPU |
| [`allowed_cpus`](#allowed_cpus) | list the CPUs the calling thread may run on, in ascending index order |

| Constants | |
| :--- | :--- |
| [`ERROR_INVALID`](#constants), [`ERROR_NO_MEMORY`](#constants), [`ERROR_UNSUPPORTED`](#constants), [`DEFAULT_STACK_RESERVE`](#constants), [`MIN_STACK_RESERVE`](#constants), [`MAX_NAME_BYTES`](#constants) | |

---

## ThreadError

```mach
pub tag ThreadError: u8 { invalid; exhausted; unsupported; native: i64; }
```

a refused thread operation

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a configuration outside the portable policy, or a handle that is not joinable (never spawned, already joined or detached) |
| `exhausted` |  | the owner record could not be allocated |
| `unsupported` |  | the target refused a policy it does not implement (stack commit), or a loader-hosted linux process has no thread backend installed |
| `native` | `i64` | the target refused with its negative code, kept whole |

### code

```mach
pub fun code(e: ThreadError) i64
```

the portable status code of an error, for diagnostics that keep an i64

| Parameter | |
| :--- | :--- |
| `e` | error to convert |
| **returns** | a negative code, the native code itself for ThreadError.native |

## Operation

```mach
pub def Operation: err[ThreadError]
```

## Config

```mach
pub rec Config {
    stack_reserve: usize;
    stack_commit:  usize;
    name:          str;
}
```

portable thread creation policy

| Field | Type | |
| :--- | :--- | :--- |
| `stack_reserve` | `usize` | virtual address space reserved for the stack, or 0 for default |
| `stack_commit` | `usize` | initial committed stack bytes, or 0 for the target default |
| `name` | `str` | nil or a portable ASCII diagnostic name of at most 15 bytes |

### config_default

```mach
pub fun config_default(c: *Config)
```

initialize a thread configuration with portable defaults

| Parameter | |
| :--- | :--- |
| `c` | configuration to fill with the default reserve, no commit and no name |

### spawn_with_config

```mach
pub fun spawn_with_config(f: fun(*u8), arg: *u8, c: *Config, t: *Thread) Operation
```

spawn with borrowed caller context and explicit configuration

arg must remain valid until the entry returns. ownership stays with the caller.

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread with arg |
| `arg` | borrowed context passed to f |
| `c` | creation policy, validated before anything is allocated |
| `t` | handle filled in, its tid holding the failure code on refusal |
| **returns** | ok, invalid for a config outside the policy, exhausted, unsupported, or the native refusal |

### spawn_owned_with_config

```mach
pub fun spawn_owned_with_config(f: fun(*u8), arg: *u8, destroy: fun(*u8), c: *Config, t: *Thread) Operation
```

spawn with owned caller context and explicit configuration

destroy runs exactly once after the entry returns, including an early return.
if spawning fails, destroy runs before this call returns.

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread with arg |
| `arg` | owned context passed to f and then to destroy |
| `destroy` | releases arg |
| `c` | creation policy, validated before anything is allocated |
| `t` | handle filled in, its tid holding the failure code on refusal |
| **returns** | as spawn_with_config |

### spawn_config

```mach
pub fun spawn_config(f: fun(), c: *Config, t: *Thread) Operation
```

spawn a zero-argument function with explicit configuration

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread |
| `c` | creation policy |
| `t` | handle filled in |
| **returns** | as spawn_with_config |

## Thread

```mach
pub rec Thread {
    tid:   i64;
    stack: usize;
    done:  i64;
}
```

handle to a spawned thread

| Field | Type | |
| :--- | :--- | :--- |
| `tid` | `i64` | stable native diagnostic identifier, or a negative spawn error |
| `stack` | `usize` | opaque resource-owner address, retained for source compatibility |
| `done` | `i64` | 0 while joinable, 1 after join, -1 after detach |

### spawn_with

```mach
pub fun spawn_with(f: fun(*u8), arg: *u8, t: *Thread) Operation
```

spawn with borrowed caller context and default configuration

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread with arg |
| `arg` | borrowed context passed to f, valid until f returns |
| `t` | handle filled in |
| **returns** | as spawn_with_config |

### spawn_owned

```mach
pub fun spawn_owned(f: fun(*u8), arg: *u8, destroy: fun(*u8), t: *Thread) Operation
```

spawn with owned caller context and default configuration

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread with arg |
| `arg` | owned context passed to f and then to destroy |
| `destroy` | releases arg, run once after f returns or before a refusal returns |
| `t` | handle filled in |
| **returns** | as spawn_with_config |

### spawn

```mach
pub fun spawn(f: fun(), t: *Thread) Operation
```

spawn a zero-argument function with default configuration

| Parameter | |
| :--- | :--- |
| `f` | entry function run on the new thread |
| `t` | handle filled in |
| **returns** | as spawn_with_config |

### join

```mach
pub fun join(t: *Thread) Operation
```

join and release every library-owned resource

| Parameter | |
| :--- | :--- |
| `t` | handle of a joinable thread |
| **returns** | ok once joined and released, invalid for a handle that is not joinable, or the target's refusal with the handle still joinable |

### detach

```mach
pub fun detach(t: *Thread) Operation
```

transfer ownership to the running or completed thread

| Parameter | |
| :--- | :--- |
| `t` | handle of a joinable thread |
| **returns** | ok once the thread owns its record, invalid for a handle that is not joinable, or the target's refusal with the handle still joinable |

### is_done

```mach
pub fun is_done(t: *Thread) bool
```

check whether a joinable thread body has finished

| Parameter | |
| :--- | :--- |
| `t` | thread handle |
| **returns** | true once the body finished or the handle was joined, false after detach |

### diagnostic_id

```mach
pub fun diagnostic_id(t: *Thread) i64
```

return the stable native diagnostic identifier captured at spawn

| Parameter | |
| :--- | :--- |
| `t` | thread handle |
| **returns** | its tid, negative when the spawn failed |

## Token

```mach
pub def Token: i64
```

the calling thread's identity, as current_token returns it

a token is positive and never 0, so a caller may keep 0 for "no thread". two
live threads never share one, and one thread reads the same token for its
whole life. a thread that has ended may leave its token to a later thread.

### current_token

```mach
pub fun current_token() Token
```

the calling thread's identity, read without a system call

the token is the address os.thread_block reads. on linux that is the thread
pointer, whoever owns it: std's block on the main thread of a static image and
on every thread std spawns, and the C runtime's on the main thread under a
loader and on a thread C code created. each thread has its own, so the token
is distinct and costs no system call on all of them. a raw clone without
CLONE_SETTLS inherits its parent's thread pointer and so its parent's token,
and must not call into std. on darwin and windows a thread std did not create
has no block, and its token falls back to its thread id. no freestanding
target has threads, so this is not built there.

## CpuSet

```mach
pub rec CpuSet {
    words:    *u64;
    capacity: usize;
    count:    usize;
}
```

a set of CPUs over words the caller owns

CPU i is bit i % 64 of words[i / 64]. count is how many leading words are
meaningful, capacity how many the caller provided. nothing is allocated.

| Field | Type | |
| :--- | :--- | :--- |
| `words` | `*u64` | the mask words |
| `capacity` | `usize` | words available at words |
| `count` | `usize` | words in use, never more than capacity |

### cpu_set

```mach
pub fun cpu_set(words: *u64, capacity: usize) CpuSet
```

an empty CPU set over caller-provided words

| Parameter | |
| :--- | :--- |
| `words` | storage for the mask words |
| `capacity` | number of words at words |
| **returns** | the set, with every word cleared |

### cpu_set_clear

```mach
pub fun cpu_set_clear(set: *CpuSet)
```

remove every CPU from the set

| Parameter | |
| :--- | :--- |
| `set` | set whose capacity words are all cleared |

### cpu_set_add

```mach
pub fun cpu_set_add(set: *CpuSet, cpu: usize) bool
```

add a CPU to the set

| Parameter | |
| :--- | :--- |
| `set` | set to add to |
| `cpu` | global CPU index |
| **returns** | false when the CPU does not fit the set's words |

### cpu_set_contains

```mach
pub fun cpu_set_contains(set: *CpuSet, cpu: usize) bool
```

whether a CPU is in the set

| Parameter | |
| :--- | :--- |
| `set` | set to read |
| `cpu` | global CPU index |
| **returns** | true when cpu is in the set |

### cpu_set_size

```mach
pub fun cpu_set_size(set: *CpuSet) usize
```

the number of CPUs in the set

| Parameter | |
| :--- | :--- |
| `set` | set to read |
| **returns** | count of set bits over the words in use |

### cpu_set_nth

```mach
pub fun cpu_set_nth(set: *CpuSet, n: usize) opt[usize]
```

the n-th CPU in the set, counting from zero in ascending index order

| Parameter | |
| :--- | :--- |
| `set` | set to read |
| `n` | zero-based position among the CPUs in the set |
| **returns** | the CPU index, or none when the set holds n CPUs or fewer |

### current_affinity

```mach
pub fun current_affinity(set: *CpuSet) err[std.io.error.Error]
```

read the calling thread's CPU affinity into set

a set too small for the platform's mask is refused with RANGE; size it with
affinity_words first. darwin has no CPU affinity and refuses with UNSUPPORTED.

| Parameter | |
| :--- | :--- |
| `set` | set whose words receive the mask |
| **returns** | ok with set.count updated, or the refusal |

### set_current_affinity

```mach
pub fun set_current_affinity(set: *CpuSet) err[std.io.error.Error]
```

pin the calling thread to the CPUs in set

| Parameter | |
| :--- | :--- |
| `set` | CPUs to allow |
| **returns** | ok, INVALID for an empty set or CPUs the process may not use, UNSUPPORTED where the platform cannot express the set, or the refusal |

## Functions

### affinity_words

```mach
pub fun affinity_words() res[usize, std.io.error.Error]
```

the number of words a CPU set needs to hold the calling thread's affinity

| Parameter | |
| :--- | :--- |
| **returns** | the word count, or the refusal |

### pin_current_to

```mach
pub fun pin_current_to(cpu: usize) err[std.io.error.Error]
```

pin the calling thread to one CPU

| Parameter | |
| :--- | :--- |
| `cpu` | global CPU index, as allowed_cpus reports it |
| **returns** | ok, INVALID for a CPU the process may not use, or the refusal |

### allowed_cpus

```mach
pub fun allowed_cpus(out: *usize, capacity: usize, out_count: *usize) err[std.io.error.Error]
```

list the CPUs the calling thread may run on, in ascending index order

a consumer that runs one worker per CPU pins worker i to out[i].

| Parameter | |
| :--- | :--- |
| `out` | destination for global CPU indices |
| `capacity` | entries available at out |
| `out_count` | CPUs listed, or CPUs available when capacity is too small |
| **returns** | ok, RANGE when capacity is too small, or the refusal |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `ERROR_INVALID` | `i64` | `-22` |  |
| `ERROR_NO_MEMORY` | `i64` | `-12` |  |
| `ERROR_UNSUPPORTED` | `i64` | `-95` |  |
| `DEFAULT_STACK_RESERVE` | `usize` | `2097152` |  |
| `MIN_STACK_RESERVE` | `usize` | `65536` |  |
| `MAX_NAME_BYTES` | `usize` | `15` |  |

