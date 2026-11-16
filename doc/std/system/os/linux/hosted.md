[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / [linux](README.md) / **hosted**

# std.system.os.linux.hosted

thread creation in a loader-hosted process

a thread there has to carry the initial-exec thread-locals of every module and
the C runtime's per-thread state, and only the host's own thread creation
builds those. std names no host symbol, so it reaches that creation through
three link-time defaults, which a backend package replaces with strong
definitions of the same names. the pairing is unchecked: a replacement takes
exactly these shapes. all three or none, as a handle only means something to
the backend that made it. replacement is link time only, so each image that
carries std and spawns has the backend in its own link. a secret never crosses
this seam.

Source: [`src/system/os/linux/hosted.mach`](../../../../../src/system/os/linux/hosted.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Entry`](#entry) | `def` | what a backend starts: the thread runs entry(arg) and exits with its result |

| Functions | |
| :--- | :--- |
| [`thread_spawn`](#thread_spawn) | create a thread through the backend, or refuse with its answer |
| [`thread_join`](#thread_join) | wait for a thread thread_spawn made to end |
| [`thread_detach`](#thread_detach) | give up the handle of a thread thread_spawn made |

---

## Entry

```mach
pub def Entry: fun(*u8) *u8
```

what a backend starts: the thread runs entry(arg) and exits with its result

## Functions

### thread_spawn

```mach
pub fun thread_spawn(
    wipe: fun(), f: fun(*u8), arg: *u8, state: *i64, reclaimable: *i64,
    owner: ptr, owner_size: usize, name: *u8,
    stack_reserve: usize, stack_commit: usize, native: *usize,
) i64
```

create a thread through the backend, or refuse with its answer

with no backend installed that answer is ENOTSUP, before anything starts. the
thread gets no std block, so its stack bounds are unknown, as on any thread
the host created

| Parameter | |
| :--- | :--- |
| `wipe` | wipes the calling thread's thread-local block as the thread ends |
| **returns** | thread ID on success, or negative errno on failure |

### thread_join

```mach
pub fun thread_join(native: usize) i64
```

wait for a thread thread_spawn made to end

### thread_detach

```mach
pub fun thread_detach(native: usize) i64
```

give up the handle of a thread thread_spawn made

