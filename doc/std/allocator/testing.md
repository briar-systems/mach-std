[std](../README.md) / [allocator](README.md) / **testing**

# std.allocator.testing

an allocator built to make memory bugs fail loudly in tests

the production allocators are forgiving in ways that hide defects. a page
allocator hands back kernel-zeroed memory, so reading an uninitialized field
looks like reading a zero. it rounds every request up to a page, so reading
one byte past the end of a small object lands in slack that is still mapped
and still readable. and it never runs out, so the failure path of every
allocating function goes untested. this allocator removes all three
forgivenesses.

## strict sizes

an allocation is placed as close to the end of a mapped page as its
alignment allows, and the page immediately after it is mapped unreadable.
a request whose size is a multiple of its alignment ends on the last byte
of the page, so reading or writing even one byte past it faults at the exact
moment it happens; any other request leaves fewer than `align` bytes of
slack before the guard. the cost is one guard page per live allocation,
which is why this belongs in tests and not in production. a host that cannot
protect a page (wasi's linear memory) places blocks the same way with the
guard page left readable, so an overrun there is not caught, and poison,
failure injection and accounting are unchanged.

## poison

fresh memory is filled with `POISON_NEW` rather than left zeroed, so code that
reads a field it never wrote sees an implausible value instead of a plausible
zero. freed memory is overwritten with `POISON_FREE` before the mapping is
torn down, so a use-after-free that happens to reach still-mapped memory reads
an implausible value too.

## fail at N

`fail_at_ordinal` makes the Nth allocation from this allocator fail, counting
from one. `fail_from_ordinal` refuses the Nth and every later one, so
`fail_from_ordinal(t, 1)` gives an allocator that refuses everything and
only counts what it was asked. a test that runs the same operation once per
ordinal, from one to the number of allocations the operation makes,
exercises every allocation-failure path in it. `live` and `leaked` then say
whether the operation cleaned up after itself on each of those paths, which
is the property that matters and the one that is otherwise almost impossible
to check.

## the walk

`walk` does that loop. it runs an attempt at ordinal zero to learn how many
requests the operation makes, then once per ordinal from one to that count,
with a fresh instance each time. the attempt builds its fixture through the
instance, calls `arm`, runs the operation, asserts what the operation
promised and tears the fixture down. `arm` starts the counted window, so a
fixture built before it does not shift the ordinal the operation is refused
at. after every attempt the walk checks that nothing is outstanding, nothing
was released wrongly, tracking never filled, and the armed refusal fired
exactly once.

## accounting

every allocation is recorded until it is freed. `live` is how many are
outstanding, `leaked` is whether any are, and a free of a pointer this
allocator did not hand out, or handed out and already took back, is counted
as a double free rather than being ignored. a free or a reallocate that
names a block with a size other than the one it was handed out at is counted
as a size mismatch.

Source: [`src/allocator/testing.mach`](../../../src/allocator/testing.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Testing`](#testing) | `rec` | a tracking, guarding, failing allocator |
| [`Outcome`](#outcome) | `rec` | how a walk ended |

| On `Testing` | |
| :--- | :--- |
| [`init`](#init) | initialize a testing allocator |
| [`allocator_of`](#allocator_of) | the allocator interface to hand to the code under test |
| [`fail_at_ordinal`](#fail_at_ordinal) | make the `n`th allocation from now fail, counting the allocations this instance has already served |
| [`fail_from_ordinal`](#fail_from_ordinal) | make the `n`th allocation and every one after it fail, counting as `fail_at_ordinal` does |
| [`refuse_reallocates`](#refuse_reallocates) | refuse every reallocate of an existing block while `on`, leaving allocates to the ordinal rules |
| [`clear_failure`](#clear_failure) | stop failing allocations |
| [`arm`](#arm) | start the counted window of a walk attempt |
| [`counted`](#counted) | how many allocation requests have been made since `arm` |
| [`reallocate_count`](#reallocate_count) | how many reallocates of an existing block to a nonzero size were requested, refused or not |
| [`last_reallocated`](#last_reallocated) | the block the most recent counted reallocate named, nil before any |
| [`last_old_size`](#last_old_size) | the old size the most recent counted reallocate named |
| [`refused_count`](#refused_count) | how many requests failure injection refused |
| [`last_request_size`](#last_request_size) | the size of the most recent allocate or reallocate request, refused or not |
| [`owns`](#owns) | true when `p` is an allocation this instance currently holds |
| [`live_count`](#live_count) | how many allocations are outstanding |
| [`peak_live_count`](#peak_live_count) | the most allocations that were outstanding at once since `init` |
| [`live_byte_count`](#live_byte_count) | how many bytes the outstanding allocations hold, at the sizes requested |
| [`total_count`](#total_count) | how many allocations this instance has ever served |
| [`attempt_count`](#attempt_count) | how many allocation requests have been made, including the refused ones |
| [`leaked`](#leaked) | true when anything allocated through this instance was never freed |
| [`double_free_count`](#double_free_count) | how many frees named a pointer this instance did not currently own |
| [`size_mismatch_count`](#size_mismatch_count) | how many frees and reallocates named an owned block with another size |
| [`tracking_exhausted`](#tracking_exhausted) | true when tracking filled up, which makes the other counters unreliable |
| [`clean`](#clean) | nothing outstanding, nothing released wrongly, and tracking never filled |
| [`dnit`](#dnit) | release everything still outstanding, the tracking table with it, and reset the live counters |

| On `Outcome` | |
| :--- | :--- |
| [`walk`](#walk) | run `attempt` once per ordinal: zero first, then one to the count the baseline made |

| Constants | |
| :--- | :--- |
| [`POISON_NEW`](#constants) | filled into memory as it is handed out, so an uninitialized read is visible |
| [`POISON_FREE`](#constants) | written over memory as it is taken back, so a use-after-free is visible |
| [`MAX_TRACKED`](#constants) | how many live allocations one instance can track at once |
| [`WALK_NONALLOCATING`](#constants) | the attempt made no request at ordinal zero |
| [`WALK_LEAK`](#constants) | the attempt left an allocation outstanding |
| [`WALK_MISMATCH`](#constants) | the attempt released a block it did not own, twice, or with the wrong size |
| [`WALK_OVERFLOW`](#constants) | the attempt held more live allocations than one instance tracks |
| [`WALK_UNFIRED`](#constants) | the armed ordinal was never reached, or was refused more than once |

---

## Testing

```mach
pub rec Testing {
    # the interface to hand to code under test
    a: std.allocator.Allocator;

    # the ordinal of the allocation that must fail, counting from one; zero
    # means never fail
    fail_at: usize;
    # keep refusing every request after `fail_at`
    sticky: bool;
    # how many allocation requests have been made
    attempts: usize;
    # how many requests failure injection refused
    refused: usize;
    # the size of the most recent allocate or reallocate request
    last_size: usize;

    # refuse every reallocate of an existing block
    refuse_reallocates: bool;
    # reallocates of an existing block to a nonzero size, refused or not
    reallocates: usize;
    # the block and the old size the most recent such reallocate named
    last_reallocated: ptr;
    last_old_size:    usize;

    # the walk's ordinal for this attempt, zero for the baseline
    ordinal: usize;
    # `attempts` when `arm` ran
    armed_at: usize;

    # how many allocations are outstanding
    live: usize;
    # the most that were outstanding at once
    peak_live: usize;
    # the bytes they hold, as requested
    live_bytes: usize;
    # how many allocations have ever been made
    total: usize;
    # frees of a pointer this allocator did not currently own
    double_frees: usize;
    # frees and reallocates of an owned block that named another size
    size_mismatches: usize;
    # allocations refused because tracking is full rather than because of
    # `fail_at`; a test that trips this needs a bigger `MAX_TRACKED`
    exhausted: usize;

    # the table of SLOTS blocks, on pages of its own so the instance fits any stack
    blocks: *Block;
}
```

a tracking, guarding, failing allocator

create with `init`, hand `?state.a` to the code under test, and read the
counters afterwards. one instance is not safe to share across threads.

### init

```mach
pub fun init(t: *Testing) err[std.allocator.Error]
```

initialize a testing allocator

the instance owns its tracking table and the mappings it hands out, so it
must outlive every allocation made through it, and `dnit` must run while
those are still reachable.

| Parameter | |
| :--- | :--- |
| `t` | the instance to initialize |
| **returns** | ok, `invalid` when t is nil, or `exhausted` when the table cannot be mapped |

### allocator_of

```mach
pub fun allocator_of(t: *Testing) *std.allocator.Allocator
```

the allocator interface to hand to the code under test

### fail_at_ordinal

```mach
pub fun fail_at_ordinal(t: *Testing, n: usize)
```

make the `n`th allocation from now fail, counting the allocations this
instance has already served

passing zero disables failure injection.

### fail_from_ordinal

```mach
pub fun fail_from_ordinal(t: *Testing, n: usize)
```

make the `n`th allocation and every one after it fail, counting as
`fail_at_ordinal` does

passing zero disables failure injection. on a fresh instance, one refuses
every request while still counting them.

### refuse_reallocates

```mach
pub fun refuse_reallocates(t: *Testing, on: bool)
```

refuse every reallocate of an existing block while `on`, leaving allocates to
the ordinal rules

a refused reallocate still counts as an attempt and as a reallocate.

### clear_failure

```mach
pub fun clear_failure(t: *Testing)
```

stop failing allocations

### arm

```mach
pub fun arm(t: *Testing)
```

start the counted window of a walk attempt

requests made before this are the fixture's. from here `counted` measures,
and the attempt's ordinal, when it has one, is refused counting from here.

### counted

```mach
pub fun counted(t: *Testing) usize
```

how many allocation requests have been made since `arm`

### reallocate_count

```mach
pub fun reallocate_count(t: *Testing) usize
```

how many reallocates of an existing block to a nonzero size were requested,
refused or not

a reallocate from nil is an allocate and one to zero is a free; neither
counts here.

### last_reallocated

```mach
pub fun last_reallocated(t: *Testing) ptr
```

the block the most recent counted reallocate named, nil before any

### last_old_size

```mach
pub fun last_old_size(t: *Testing) usize
```

the old size the most recent counted reallocate named

### refused_count

```mach
pub fun refused_count(t: *Testing) usize
```

how many requests failure injection refused

### last_request_size

```mach
pub fun last_request_size(t: *Testing) usize
```

the size of the most recent allocate or reallocate request, refused or not

### owns

```mach
pub fun owns(t: *Testing, p: ptr) bool
```

true when `p` is an allocation this instance currently holds

### live_count

```mach
pub fun live_count(t: *Testing) usize
```

how many allocations are outstanding

### peak_live_count

```mach
pub fun peak_live_count(t: *Testing) usize
```

the most allocations that were outstanding at once since `init`

a reallocate holds the old and the new block together for a moment, so it
counts one more.

### live_byte_count

```mach
pub fun live_byte_count(t: *Testing) usize
```

how many bytes the outstanding allocations hold, at the sizes requested

### total_count

```mach
pub fun total_count(t: *Testing) usize
```

how many allocations this instance has ever served

### attempt_count

```mach
pub fun attempt_count(t: *Testing) usize
```

how many allocation requests have been made, including the refused ones

### leaked

```mach
pub fun leaked(t: *Testing) bool
```

true when anything allocated through this instance was never freed

### double_free_count

```mach
pub fun double_free_count(t: *Testing) usize
```

how many frees named a pointer this instance did not currently own

### size_mismatch_count

```mach
pub fun size_mismatch_count(t: *Testing) usize
```

how many frees and reallocates named an owned block with another size

### tracking_exhausted

```mach
pub fun tracking_exhausted(t: *Testing) bool
```

true when tracking filled up, which makes the other counters unreliable

### clean

```mach
pub fun clean(t: *Testing) bool
```

nothing outstanding, nothing released wrongly, and tracking never filled

### dnit

```mach
pub fun dnit(t: *Testing) usize
```

release everything still outstanding, the tracking table with it, and reset
the live counters

leaks are reported by `leaked` before this runs. afterwards the instance
holds nothing, a second dnit reclaims nothing, and `init` makes it usable again.

| Parameter | |
| :--- | :--- |
| **returns** | how many live allocations had to be reclaimed, which is the leak count |

## Outcome

```mach
pub rec Outcome {
    # zero when every attempt passed, else the failing attempt's own code or
    # one of the WALK_ codes
    code: i32;
    # the ordinal that failed, zero when the walk passed
    ordinal: usize;
    # the requests the operation made at ordinal zero
    attempts: usize;
}
```

how a walk ended

### walk

```mach
pub fun walk[C](context: *C, attempt: fun(*C, *Testing) i32) Outcome
```

run `attempt` once per ordinal: zero first, then one to the count the
baseline made

each attempt gets a fresh instance, builds its fixture through it, calls
`arm`, runs the operation, asserts its promises and tears the fixture down,
returning zero on a pass. the walk stops at the first failing ordinal. an
operation that makes no request at ordinal zero ends the walk with
`WALK_NONALLOCATING`, so the test can say so instead of probing nothing.

| Parameter | |
| :--- | :--- |
| `context` | handed to every attempt unchanged |
| `attempt` | one run of the operation under the instance |
| **returns** | how the walk ended |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `POISON_NEW` | `u8` | `0xAA` | filled into memory as it is handed out, so an uninitialized read is visible |
| `POISON_FREE` | `u8` | `0xDE` | written over memory as it is taken back, so a use-after-free is visible |
| `MAX_TRACKED` | `usize` | `4096` | how many live allocations one instance can track at once |
| `WALK_NONALLOCATING` | `i32` | `-1` | the attempt made no request at ordinal zero |
| `WALK_LEAK` | `i32` | `-2` | the attempt left an allocation outstanding |
| `WALK_MISMATCH` | `i32` | `-3` | the attempt released a block it did not own, twice, or with the wrong size |
| `WALK_OVERFLOW` | `i32` | `-4` | the attempt held more live allocations than one instance tracks |
| `WALK_UNFIRED` | `i32` | `-5` | the armed ordinal was never reached, or was refused more than once |

