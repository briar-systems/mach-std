[std](../README.md) / [memory](README.md) / **buffers**

# std.memory.buffers

on-demand buffers with caller-declared size classes, byte budgets and wake-ups

a `Source` hands out address-stable chunks to accounts. `Pool` is std's source:
the caller declares up to MAX_CLASSES size classes, a request is served from
the smallest class that fits its bytes, alignment and secrecy, and a request
larger than every class takes the oversize path, one contiguous block from the
backing that is returned to it at release.

budgets are bytes. every account has a budget per lane (the pool declares how
many lanes there are) and may reserve bytes at open; growth past a reservation
competes for the global budget less every reservation. a refusal is a result,
never a crash:
  budget     the account's own lane limit. never registered, since the
             account's own releases end it
  exhausted  the shared remainder is gone
  memory     a backing refused
  misuse     a stale ref, a foreign chunk, a held or in-flight violation, or
             a concurrent entry
an account refused as exhausted or memory is registered, when it asks, at most
once and in FIFO order. each release wakes the oldest waiter: it moves to the
ready list, `ready` drains ready handles oldest first, and the optional notify
callback runs once per account woken. without notify a release makes no
callbacks and never allocates.

a secret class is backed by welded storage from std.memory.secret, held as a
borrow so the pool itself carries no welded pointer: its chunks carry no plain
data pointer, `secret` gives the welded view, and release wipes the whole
chunk. `secret_typed[T]` views a held secret chunk as T values instead, with
T's own secrecy shape, so a record with secret fields lives in the chunk with
no cast. a hold sees its chunk one way only: once as bytes, the typed view is
refused, and once as T, the byte view and every other type are refused, so no
byte or field of one view aliases a byte of different secrecy in another. the
next hold starts over on wiped storage. secret chunks are served through
`SecretSource`, never through `Source`, so only a holder of a `SecretSource`
is welded. welded storage needs the pages capability (HAS_PAGES), so a secret
class or request is refused on a target without it (WELDED is false), and so
is one whose alignment exceeds SECRET_ALIGN_MAX, the alignment welded storage
guarantees. a
bring-your-own-OS implementation gets secret classes by providing the os
contract's secret primitives.

acquire is O(1) when a class serves it from a retained chunk; otherwise it costs
one backing allocation. `backing_allocations` in the snapshot counts them, so a
host can size each class's high_water for a steady state that never touches the
backing.

chunks never move while held. payloads are separate backing allocations and a
class keeps up to its high_water released chunks for reuse; only the slot
metadata lives in a growable table, and nothing hands its addresses out.
opening an account reserves slot metadata for its reservation, so an acquire
inside the reservation never fails on metadata. a reserved slot costs address
space until it is first taken, and is written then. the table gives back what a
peak grew: a chunk of it goes once it and the chunk below it hold no slot in
use and no reservation needs them, so one empty chunk stays as slack. a held
slot never moves, and a ref from a released chunk is refused once the table
grows again.

a pool is serialized-use: it is never entered concurrently. it is not tied to
a thread, so work may hand a pool between threads as long as the hand-off is
serialized. every call claims an entrant flag and a concurrent call is refused
as misuse with no effect, a refused release leaving the chunk owned by its
caller. one pool per worker is the intended deployment. callbacks (notify,
trap, backings) must not call back into the pool.

Source: [`src/memory/buffers.mach`](../../../src/memory/buffers.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.memory.table`](table.md).

| Type | | |
| :--- | :--- | :--- |
| [`Request`](#request) | `rec` | what a caller asks for |
| [`Ref`](#ref) | `rec` | a chunk's identity: an index and a generation, stale once released |
| [`Chunk`](#chunk) | `rec` | a held chunk |
| [`Status`](#status) | `tag` | how an acquisition ended |
| [`Reason`](#reason) | `tag` | why a call was refused |
| [`Acquired`](#acquired) | `rec` | the outcome of an acquisition |
| [`Budgets`](#budgets) | `rec` | the per-lane byte budgets an account opens with |
| [`Account`](#account) | `rec` | an owner of chunks and budgets, embedded by the caller |
| [`Shape`](#shape) | `rec` | the typed shape a held secret chunk is viewed as, built by the typed views |
| [`Source`](#source) | `rec` | the interface every plain buffer source implements |
| [`SecretSource`](#secretsource) | `rec` | the interface for secret-welded chunks |
| [`ClassConfig`](#classconfig) | `rec` | one declared size class |
| [`Config`](#config) | `rec` | pool configuration |
| [`ClassCounters`](#classcounters) | `rec` | one class's counters in a snapshot |
| [`Snapshot`](#snapshot) | `rec` | a point-in-time view of a pool |
| [`Pool`](#pool) | `rec` | std's buffer source |

| On `Source` | |
| :--- | :--- |
| [`source_account_init`](#source_account_init) | open an account on a source |
| [`source_account_dnit`](#source_account_dnit) | close an account, dropping any registration it holds |
| [`source_acquire`](#source_acquire) | acquire one chunk from a source |
| [`source_acquire_n`](#source_acquire_n) | acquire every requested chunk, or none of them |
| [`source_release`](#source_release) | release a chunk to its source |
| [`source_data`](#source_data) | the address of a held plain chunk, nil when the ref is stale |
| [`source_retain`](#source_retain) | count one more in-flight user of a held chunk |
| [`source_settle`](#source_settle) | count one in-flight user of a held chunk finished |
| [`source_in_flight`](#source_in_flight) | whether a held chunk has in-flight users |
| [`source_ready`](#source_ready) | drain woken account handles into output, oldest first |
| [`source_lanes`](#source_lanes) | budget lanes per account the source declares |
| [`source_measure`](#source_measure) | the bytes an acquisition of `request` would charge on a source |

| On `SecretSource` | |
| :--- | :--- |
| [`secret_source_lanes`](#secret_source_lanes) | budget lanes per account a secret source declares, as `source_lanes` |
| [`secret_source_measure`](#secret_source_measure) | the bytes an acquisition would charge on a secret source, as `source_measure` |
| [`secret_source_account_init`](#secret_source_account_init) | open an account on a secret source, as `source_account_init` |
| [`secret_source_account_dnit`](#secret_source_account_dnit) | close an account on a secret source |
| [`secret_source_acquire`](#secret_source_acquire) | acquire one secret chunk, `request.secret` must be set |
| [`secret_source_release`](#secret_source_release) | release a secret chunk, wiping it in full |
| [`secret_source_view`](#secret_source_view) | the welded view of a held secret chunk, nil when stale, as `secret` |
| [`secret_source_view_typed`](#secret_source_view_typed) | a held secret chunk viewed as count values of T, as `secret_typed` |

| On `Config` | |
| :--- | :--- |
| [`arena_bytes`](#arena_bytes) | bytes an allocator.fixed arena needs to hold a pool's slot metadata and the given number of plain chunks of every class, for embedded use |

| On `Pool` | |
| :--- | :--- |
| [`init`](#init) | make a pool |
| [`dnit`](#dnit) | release every retained chunk and the slot metadata |
| [`account_init`](#account_init) | open an account |
| [`account_dnit`](#account_dnit) | close an account holding no chunks, unlinking any registration |
| [`acquire`](#acquire) | acquire one chunk |
| [`acquire_n`](#acquire_n) | acquire every requested chunk or none |
| [`release`](#release) | give a chunk back |
| [`secret`](#secret) | the welded view of a held secret chunk, nil for a plain or stale one, or one this hold already views as a type |
| [`secret_bind`](#secret_bind) | bind a held secret chunk to a typed shape for the rest of its hold |
| [`secret_typed`](#secret_typed) | a held secret chunk viewed as count values of T, with T's secrecy shape |
| [`data`](#data) | the address of a held plain chunk, nil when the ref is stale or secret |
| [`retain`](#retain) | count an in-flight user, such as an operation the chunk was handed to |
| [`settle`](#settle) | end one in-flight use |
| [`in_flight`](#in_flight) | whether a held chunk has in-flight users |
| [`lanes`](#lanes) | budget lanes per account, fixed at make |
| [`measure`](#measure) | the bytes `acquire` would charge for a request, without acquiring |
| [`ready`](#ready) | drain the handles of woken accounts, oldest first |
| [`snapshot`](#snapshot-1) | a point-in-time view of the pool's counters |
| [`source`](#source-1) | the pool as a Source, borrowing the pool |
| [`secret_source`](#secret_source) | the pool as a SecretSource, borrowing the pool |

| Constants | |
| :--- | :--- |
| [`MAX_CLASSES`](#constants), [`MAX_LANES`](#constants), [`OVERSIZE`](#constants) | |
| [`WELDED`](#constants) | welded storage goes through std.memory.secret borrows, so no welded pointer is ever held behind the pool's untyped context |
| [`SECRET_ALIGN_MAX`](#constants) | the largest alignment a secret class or request may declare: every welded allocation starts on a page boundary at least this aligned |

---

## Request

```mach
pub rec Request {
    bytes:  usize;
    align:  usize;
    lane:   u8;
    secret: bool;
}
```

what a caller asks for

| Field | Type | |
| :--- | :--- | :--- |
| `bytes` | `usize` | the bytes needed, served rounded up to a class or exactly by oversize |
| `align` | `usize` | the alignment needed, 0 for the default of 16, at most SECRET_ALIGN_MAX for a secret request |
| `lane` | `u8` | the budget lane the bytes are charged to |
| `secret` | `bool` | whether the chunk must be secret-welded |

## Ref

```mach
pub rec Ref {
    index:      u32;
    generation: u32;
}
```

a chunk's identity: an index and a generation, stale once released

## Chunk

```mach
pub rec Chunk {
    ref:   Ref;
    class: u16;
    bytes: usize;
    data:  *u8;
}
```

a held chunk

| Field | Type | |
| :--- | :--- | :--- |
| `ref` | `Ref` | identity for release, data, retain and settle |
| `class` | `u16` | the class index, or OVERSIZE |
| `bytes` | `usize` | usable bytes, at least what was requested |
| `data` | `*u8` | the address, nil for a secret chunk (see `secret`) |

## Status

```mach
pub tag Status: u8 {
    ok;
    blocked;
    error;
}
```

how an acquisition ended

| Case | Payload | |
| :--- | :--- | :--- |
| `ok` |  | the chunk was acquired |
| `blocked` |  | a budget, the shared budget or a backing refused, see the reason |
| `error` |  | the call was misuse and had no effect |

## Reason

```mach
pub tag Reason: u8 {
    none;
    budget;
    exhausted;
    memory;
    misuse;
}
```

why a call was refused

| Case | Payload | |
| :--- | :--- | :--- |
| `none` |  | it was not |
| `budget` |  | the account's own lane budget, never registered for a wake-up |
| `exhausted` |  | the global budget less every reservation is gone |
| `memory` |  | a backing or the slot metadata refused |
| `misuse` |  | a stale ref, a foreign chunk, a held or in-flight violation, a malformed request or a concurrent entry |

## Acquired

```mach
pub rec Acquired {
    status: Status;
    reason: Reason;
    chunk:  Chunk;
}
```

the outcome of an acquisition

| Field | Type | |
| :--- | :--- | :--- |
| `status` | `Status` | how it ended |
| `reason` | `Reason` | none on success, otherwise why it was refused |
| `chunk` | `Chunk` | the chunk on success, the first of the set for acquire_n, zeroed otherwise |

## Budgets

```mach
pub rec Budgets {
    lanes: usize;
    bytes: [8]usize;
}
```

the per-lane byte budgets an account opens with

the count travels inside the value: `lanes` says how many of `bytes` are
filled, and `account_init` refuses as misuse unless it equals the pool's
lane count. a caller cannot supply fewer budgets than the pool reads,
because there is no pointer to read past. `bytes` is `MAX_LANES` long, as
`Account.budgets` is.

| Field | Type | |
| :--- | :--- | :--- |
| `lanes` | `usize` | how many budgets are filled, which must equal the pool's lanes |
| `bytes` | `[8]usize` | the budget per lane, in bytes |

## Account

```mach
pub rec Account {
    pool:           *Pool;
    handle:         u64;
    budgets:        [8]usize;
    used:           [8]usize;
    reserve:        usize;
    reserved_slots: usize;
    held:           usize;
    chunks:         usize;
    open:           bool;
    waiting:        bool;
    is_ready:       bool;
    prev:           *Account;
    next:           *Account;
}
```

an owner of chunks and budgets, embedded by the caller

the fields belong to the source that opened it. it must not move while open.

## Shape

```mach
pub rec Shape {
    kind:  u64;
    size:  usize;
    align: usize;
    count: usize;
}
```

the typed shape a held secret chunk is viewed as, built by the typed views

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `u64` | the element type's identity, from `$type_id` |
| `size` | `usize` | bytes per element |
| `align` | `usize` | the element alignment |
| `count` | `usize` | elements in the view |

## Source

```mach
pub rec Source {
    ctx:              ptr;
    fn_open_account:  fun(ptr, *Account, u64, Budgets, usize) Reason;
    fn_close_account: fun(ptr, *Account) Reason;
    fn_acquire:       fun(ptr, *Account, Request, bool) Acquired;
    fn_acquire_n:     fun(ptr, *Account, *Request, usize, *Chunk, bool) Acquired;
    fn_release:       fun(ptr, *Account, Chunk) Reason;
    fn_data:          fun(ptr, Ref) *u8;
    fn_retain:        fun(ptr, Ref) Reason;
    fn_settle:        fun(ptr, Ref) Reason;
    fn_in_flight:     fun(ptr, Ref) bool;
    fn_ready:         fun(ptr, *u64, usize) usize;
    fn_lanes:         fun(ptr) usize;
    fn_measure:       fun(ptr, Request) usize;
}
```

the interface every plain buffer source implements

a consumer drives a source only through these members, through the `source_*`
functions below, so a host may supply its own source in place of `Pool`. a
source serves plain chunks only and refuses a secret request as misuse. its
type holds nothing welded, so a record holding a source passes through `ptr`

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to every callback |
| `fn_open_account` | `fun(ptr, *Account, u64, Budgets, usize) Reason` | open (account, handle, budgets, reserve) |
| `fn_close_account` | `fun(ptr, *Account) Reason` | close an account, giving up its registration |
| `fn_acquire` | `fun(ptr, *Account, Request, bool) Acquired` | one chunk for (account, request, register on refusal) |
| `fn_acquire_n` | `fun(ptr, *Account, *Request, usize, *Chunk, bool) Acquired` | a set of chunks, all or nothing, written to the output array |
| `fn_release` | `fun(ptr, *Account, Chunk) Reason` | give a chunk back, `none` on success |
| `fn_data` | `fun(ptr, Ref) *u8` | the address of a held plain chunk, nil when stale |
| `fn_retain` | `fun(ptr, Ref) Reason` | count one more in-flight user of a held chunk |
| `fn_settle` | `fun(ptr, Ref) Reason` | count one in-flight user finished |
| `fn_in_flight` | `fun(ptr, Ref) bool` | whether a held chunk has in-flight users |
| `fn_ready` | `fun(ptr, *u64, usize) usize` | drain woken account handles, oldest first, returning the count |
| `fn_lanes` | `fun(ptr) usize` | budget lanes per account, 0 when undeclared |
| `fn_measure` | `fun(ptr, Request) usize` | the bytes an acquisition would charge, 0 when refused |

### source_account_init

```mach
pub fun source_account_init(s: *Source, account: *Account, handle: u64, budgets: Budgets, reserve: usize) Reason
```

open an account on a source

| Parameter | |
| :--- | :--- |
| `s` | the source |
| `account` | caller-embedded account, which must not move while open |
| `handle` | the value `source_ready` reports when the account is woken |
| `budgets` | one byte budget per lane the source declares, `budgets.lanes` equal to `source_lanes` |
| `reserve` | bytes reserved for the account at open |
| **returns** | `none` on success, or the refusal |

### source_account_dnit

```mach
pub fun source_account_dnit(s: *Source, account: *Account) Reason
```

close an account, dropping any registration it holds

### source_acquire

```mach
pub fun source_acquire(s: *Source, account: *Account, request: Request, register: bool) Acquired
```

acquire one chunk from a source

| Parameter | |
| :--- | :--- |
| `register` | whether an exhausted or memory refusal registers the account |

### source_acquire_n

```mach
pub fun source_acquire_n(s: *Source, account: *Account, requests: *Request, count: usize, out: *Chunk, register: bool) Acquired
```

acquire every requested chunk, or none of them

### source_release

```mach
pub fun source_release(s: *Source, account: *Account, chunk: Chunk) Reason
```

release a chunk to its source

### source_data

```mach
pub fun source_data(s: *Source, ref: Ref) *u8
```

the address of a held plain chunk, nil when the ref is stale

### source_retain

```mach
pub fun source_retain(s: *Source, ref: Ref) Reason
```

count one more in-flight user of a held chunk

### source_settle

```mach
pub fun source_settle(s: *Source, ref: Ref) Reason
```

count one in-flight user of a held chunk finished

### source_in_flight

```mach
pub fun source_in_flight(s: *Source, ref: Ref) bool
```

whether a held chunk has in-flight users

### source_ready

```mach
pub fun source_ready(s: *Source, output: *u64, capacity: usize) usize
```

drain woken account handles into output, oldest first

| Parameter | |
| :--- | :--- |
| **returns** | how many handles were written, at most capacity |

### source_lanes

```mach
pub fun source_lanes(s: *Source) usize
```

budget lanes per account the source declares

`source_account_init` refuses a `Budgets` whose `lanes` differs from this

| Parameter | |
| :--- | :--- |
| **returns** | the lane count, 0 when the source declares none |

### source_measure

```mach
pub fun source_measure(s: *Source, request: Request) usize
```

the bytes an acquisition of `request` would charge on a source

what `source_acquire` charges the account's lane for this request, so a
borrower can size a budget before acquiring

| Parameter | |
| :--- | :--- |
| **returns** | the charge, 0 when the source declines to measure or would refuse |

## SecretSource

```mach
pub rec SecretSource {
    ctx:              ptr;
    fn_open_account:  fun(ptr, *Account, u64, Budgets, usize) Reason;
    fn_close_account: fun(ptr, *Account) Reason;
    fn_acquire:       fun(ptr, *Account, Request, bool) Acquired;
    fn_release:       fun(ptr, *Account, Chunk) Reason;
    fn_view:          fun(ptr, Chunk) *^u8;
    fn_lanes:         fun(ptr) usize;
    fn_measure:       fun(ptr, Request) usize;
    fn_bind:          fun(ptr, Chunk, Shape) *^u8;
}
```

the interface for secret-welded chunks

a secret consumer drives it through the `secret_source_*` functions below. it
serves secret chunks only and refuses a plain request as misuse. `fn_view`
returns a welded pointer, so a record holding a secret source is welded

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to every callback |
| `fn_open_account` | `fun(ptr, *Account, u64, Budgets, usize) Reason` | open (account, handle, budgets, reserve) |
| `fn_close_account` | `fun(ptr, *Account) Reason` | close an account, giving up its registration |
| `fn_acquire` | `fun(ptr, *Account, Request, bool) Acquired` | one secret chunk for (account, request, register on refusal) |
| `fn_release` | `fun(ptr, *Account, Chunk) Reason` | give a secret chunk back, wiped in full, `none` on success |
| `fn_view` | `fun(ptr, Chunk) *^u8` | the welded view of a held secret chunk, nil when stale |
| `fn_lanes` | `fun(ptr) usize` | budget lanes per account, 0 when undeclared |
| `fn_measure` | `fun(ptr, Request) usize` | the bytes an acquisition would charge, 0 when refused |
| `fn_bind` | `fun(ptr, Chunk, Shape) *^u8` | bind a held secret chunk to a typed shape, as `secret_bind` |

### secret_source_lanes

```mach
pub fun secret_source_lanes(s: *SecretSource) usize
```

budget lanes per account a secret source declares, as `source_lanes`

### secret_source_measure

```mach
pub fun secret_source_measure(s: *SecretSource, request: Request) usize
```

the bytes an acquisition would charge on a secret source, as `source_measure`

### secret_source_account_init

```mach
pub fun secret_source_account_init(s: *SecretSource, account: *Account, handle: u64, budgets: Budgets, reserve: usize) Reason
```

open an account on a secret source, as `source_account_init`

### secret_source_account_dnit

```mach
pub fun secret_source_account_dnit(s: *SecretSource, account: *Account) Reason
```

close an account on a secret source

### secret_source_acquire

```mach
pub fun secret_source_acquire(s: *SecretSource, account: *Account, request: Request, register: bool) Acquired
```

acquire one secret chunk, `request.secret` must be set

| Parameter | |
| :--- | :--- |
| `register` | whether an exhausted or memory refusal registers the account |

### secret_source_release

```mach
pub fun secret_source_release(s: *SecretSource, account: *Account, chunk: Chunk) Reason
```

release a secret chunk, wiping it in full

### secret_source_view

```mach
pub fun secret_source_view(s: *SecretSource, chunk: Chunk) *^u8
```

the welded view of a held secret chunk, nil when stale, as `secret`

### secret_source_view_typed

```mach
pub fun secret_source_view_typed[T](s: *SecretSource, chunk: Chunk, count: usize) *T
```

a held secret chunk viewed as count values of T, as `secret_typed`

nil as well for a source without `fn_bind`, or storage it returns that is not
aligned for T

## ClassConfig

```mach
pub rec ClassConfig {
    size:       usize;
    align:      usize;
    secret:     bool;
    high_water: usize;
}
```

one declared size class

| Field | Type | |
| :--- | :--- | :--- |
| `size` | `usize` | usable bytes per chunk |
| `align` | `usize` | chunk alignment, 0 for the default of 16, at most SECRET_ALIGN_MAX for a secret class |
| `secret` | `bool` | whether chunks are secret-welded |
| `high_water` | `usize` | released chunks kept for reuse, the rest go back to the backing |

## Config

```mach
pub rec Config {
    classes:        *ClassConfig;
    class_count:    usize;
    lanes:          u8;
    global_budget:  usize;
    initial_slots:  usize;
    notify:         fun(ptr, u64);
    notify_context: ptr;
    trap:           fun(ptr);
    trap_context:   ptr;
}
```

pool configuration

| Field | Type | |
| :--- | :--- | :--- |
| `classes` | `*ClassConfig` | the class declarations, copied at make |
| `class_count` | `usize` | how many, at most MAX_CLASSES |
| `lanes` | `u8` | budget lanes per account, 1 to MAX_LANES |
| `global_budget` | `usize` | total bytes the pool may hand out |
| `initial_slots` | `usize` | slot metadata to create up front, 0 for a small default |
| `notify` | `fun(ptr, u64)` | optional, called once per account woken with its handle |
| `notify_context` | `ptr` | first argument to notify |
| `trap` | `fun(ptr)` | optional, called on every misuse refusal |
| `trap_context` | `ptr` | first argument to trap |

### arena_bytes

```mach
pub fun arena_bytes(config: Config, chunks: *usize) res[usize, std.allocator.Error]
```

bytes an allocator.fixed arena needs to hold a pool's slot metadata and the
given number of plain chunks of every class, for embedded use

a fixed arena does not reclaim, so the slot table never gives back what a
peak grew and the metadata part of the bound holds however often a peak
returns. a chunk given back past its class high_water still goes to the
arena, which never reuses it, so the chunk part holds only while every class
keeps its chunks with a high_water that covers them

| Parameter | |
| :--- | :--- |
| `config` | the pool configuration |
| `chunks` | chunks per class, one entry per class |
| **returns** | the byte count, or the overflow refusal |

## ClassCounters

```mach
pub rec ClassCounters {
    size:                usize;
    live:                usize;
    peak:                usize;
    retained:            usize;
    held_bytes:          usize;
    acquisitions:        u64;
    releases:            u64;
    refusals:            u64;
    backing_allocations: u64;
}
```

one class's counters in a snapshot

| Field | Type | |
| :--- | :--- | :--- |
| `size` | `usize` | usable bytes per chunk |
| `live` | `usize` | chunks held |
| `peak` | `usize` | the most chunks held at once |
| `retained` | `usize` | released chunks kept for reuse |
| `held_bytes` | `usize` | live times size |
| `acquisitions` | `u64` | chunks acquired |
| `releases` | `u64` | chunks released |
| `refusals` | `u64` | acquisitions refused |
| `backing_allocations` | `u64` | chunks taken from the backing |

## Snapshot

```mach
pub rec Snapshot {
    classes:             [32]ClassCounters;
    class_count:         usize;
    bytes_live:          usize;
    bytes_peak:          usize;
    reserved:            usize;
    overflow:            usize;
    accounts:            usize;
    waiters:             usize;
    ready:               usize;
    misuse:              u64;
    oversize_live:       usize;
    oversize_bytes:      usize;
    acquisitions:        u64;
    oversize_acquired:   u64;
    oversize_returned:   u64;
    refusals:            u64;
    budget_refusals:     u64;
    backing_allocations: u64;
    release_failures:    u64;
}
```

a point-in-time view of a pool

## Pool

```mach
pub rec Pool {
    entrant:             i64;
    misuse:              i64;
    made:                bool;
    classes:             [32]ClassState;
    class_count:         usize;
    lanes:               usize;
    global_budget:       usize;
    reserved_total:      usize;
    overflow_used:       usize;
    bytes_live:          usize;
    bytes_peak:          usize;
    slots:               std.memory.table.Table;
    slot_pool:           std.memory.table.Pool;
    retained_in:         [table.DIRECTORY]usize;
    slots_in_use:        usize;
    slots_retained:      usize;
    slots_reserved:      usize;
    plain:               std.allocator.Allocator;
    notify:              fun(ptr, u64);
    notify_context:      ptr;
    trap:                fun(ptr);
    trap_context:        ptr;
    wait_head:           *Account;
    wait_tail:           *Account;
    ready_head:          *Account;
    ready_tail:          *Account;
    accounts:            usize;
    waiters:             usize;
    ready_count:         usize;
    oversize_live:       usize;
    oversize_bytes:      usize;
    acquisitions:        u64;
    oversize_acquired:   u64;
    oversize_returned:   u64;
    refusals:            u64;
    budget_refusals:     u64;
    backing_allocations: u64;
    # backing releases the backing refused
    release_failures: u64;
}
```

std's buffer source

### init

```mach
pub fun init(pool: *Pool, config: Config, plain: *std.allocator.Allocator) bool
```

make a pool

| Parameter | |
| :--- | :--- |
| `pool` | the pool to initialize |
| `config` | the classes and budgets, copied |
| `plain` | the backing for plain chunks and slot metadata, copied, whose context must outlive the pool |
| **returns** | whether the pool was made, refused when a secret class declares an alignment above SECRET_ALIGN_MAX, which is zero on a target without welded storage |

### dnit

```mach
pub fun dnit(pool: *Pool) bool
```

release every retained chunk and the slot metadata

refused while any account is open, so no held chunk is ever leaked or freed
under its owner

### account_init

```mach
pub fun account_init(pool: *Pool, account: *Account, handle: u64, budgets: Budgets, reserve: usize) Reason
```

open an account

| Parameter | |
| :--- | :--- |
| `pool` | the pool |
| `account` | caller-embedded storage that must not move while open |
| `handle` | the caller's identity, reported by ready and notify |
| `budgets` | one byte budget per lane, with `budgets.lanes` equal to `lanes(pool)` |
| `reserve` | bytes reserved out of the global budget for this account |
| **returns** | none, exhausted when the reservation cannot be granted, memory when its metadata cannot be backed, or misuse, which a lane count that differs from the pool's is |

### account_dnit

```mach
pub fun account_dnit(pool: *Pool, account: *Account) Reason
```

close an account holding no chunks, unlinking any registration

### acquire

```mach
pub fun acquire(pool: *Pool, account: *Account, request: Request, register: bool) Acquired
```

acquire one chunk

| Parameter | |
| :--- | :--- |
| `register` | on exhausted or memory, register the account for one wake-up |

### acquire_n

```mach
pub fun acquire_n(pool: *Pool, account: *Account, requests: *Request, count: usize, out: *Chunk, register: bool) Acquired
```

acquire every requested chunk or none

a partial set is released inside the pool, without waking anyone, before the
refusal is reported. `out` holds count chunks on success

### release

```mach
pub fun release(pool: *Pool, account: *Account, chunk: Chunk) Reason
```

give a chunk back

a secret chunk is wiped in full. the oldest waiter, if any, is woken. a
refused release leaves the chunk held by its caller

### secret

```mach
pub fun secret(pool: *Pool, chunk: Chunk) *^u8
```

the welded view of a held secret chunk, nil for a plain or stale one, or one
this hold already views as a type

### secret_bind

```mach
pub fun secret_bind(pool: *Pool, chunk: Chunk, shape: Shape) *^u8
```

bind a held secret chunk to a typed shape for the rest of its hold

this is the pool's side of the typed views. it returns the chunk's storage for
`secret_typed` or `secret_source_view_typed` to retype, and a source's
`fn_bind` forwards here. it is not a byte view: reading or writing the result
as bytes breaks the one-way rule the binding exists for. nil for a plain, stale
or foreign chunk, a shape that does not fit, storage not aligned for the
shape, a chunk this hold already views as bytes, or one bound to another type

| Parameter | |
| :--- | :--- |
| `shape` | the element type's identity, size and alignment, and the count |

### secret_typed

```mach
pub fun secret_typed[T](pool: *Pool, chunk: Chunk, count: usize) *T
```

a held secret chunk viewed as count values of T, with T's secrecy shape

T may be any record, secret fields, nested records and secret arrays
included. the chunk's storage is used as is: it is zero at the first view of
a fresh hold, and release wipes every byte of it. the view binds the hold to
T, so later calls with T give the same address for any count that fits, and
`secret` and a view as any other type are refused until the chunk is released

| Parameter | |
| :--- | :--- |
| `count` | T values the view holds |
| **returns** | the view, or nil for a plain, stale or foreign chunk, a zero or overflowing count, `count * $size_of(T)` past the chunk's bytes, a class or request alignment below `$align_of(T)`, a chunk this hold already views as bytes, or one it views as another type |

### data

```mach
pub fun data(pool: *Pool, ref: Ref) *u8
```

the address of a held plain chunk, nil when the ref is stale or secret

### retain

```mach
pub fun retain(pool: *Pool, ref: Ref) Reason
```

count an in-flight user, such as an operation the chunk was handed to

### settle

```mach
pub fun settle(pool: *Pool, ref: Ref) Reason
```

end one in-flight use

### in_flight

```mach
pub fun in_flight(pool: *Pool, ref: Ref) bool
```

whether a held chunk has in-flight users

### lanes

```mach
pub fun lanes(pool: *Pool) usize
```

budget lanes per account, fixed at make

| Parameter | |
| :--- | :--- |
| **returns** | the configured count, 0 for a nil or unmade pool |

### measure

```mach
pub fun measure(pool: *Pool, request: Request) usize
```

the bytes `acquire` would charge for a request, without acquiring

the same class selection and rounding as `acquire`: the smallest fitting
class's size, or the request rounded up to its alignment when no class fits

| Parameter | |
| :--- | :--- |
| **returns** | the charge, 0 for a nil or unmade pool, a request `acquire` would refuse as misuse, or a rounding that overflows |

### ready

```mach
pub fun ready(pool: *Pool, output: *u64, capacity: usize) usize
```

drain the handles of woken accounts, oldest first

| Parameter | |
| :--- | :--- |
| **returns** | handles written, at most capacity |

### snapshot

```mach
pub fun snapshot(pool: *Pool, output: *Snapshot) bool
```

a point-in-time view of the pool's counters

### source

```mach
pub fun source(pool: *Pool) Source
```

the pool as a Source, borrowing the pool

### secret_source

```mach
pub fun secret_source(pool: *Pool) SecretSource
```

the pool as a SecretSource, borrowing the pool

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_CLASSES` | `usize` | `32` |  |
| `MAX_LANES` | `usize` | `8` |  |
| `OVERSIZE` | `u16` | `0xffff` |  |
| `WELDED` | `bool` | `true` where `capability.HAS_PAGES`; `false` otherwise | welded storage goes through std.memory.secret borrows, so no welded pointer is ever held behind the pool's untyped context |
| `SECRET_ALIGN_MAX` | `usize` | `secret_memory.ALIGN` where `capability.HAS_PAGES`; `0` otherwise | the largest alignment a secret class or request may declare: every welded allocation starts on a page boundary at least this aligned |

