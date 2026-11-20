[std](../README.md) / [allocator](README.md) / **heap**

# std.allocator.heap

general-purpose size-class heap

small requests are rounded up to a size class and carved from a span that
serves that one class. every span keeps its own free list, so a release is
a push and an acquire is a pop. a span that runs empty goes back to a cache
shared by all classes, which is what lets a class give memory back to
another class. requests above the largest class get a span of their own.

the backing memory comes from a `Source`, a two-call contract the core never
looks past. the native member maps and unmaps, and on wasi, whose linear memory
only grows, the OS layer keeps what is unmapped for the next map. a member that
cannot take memory back leaves `fn_release` nil and the core retains spans
instead of returning them. the core never assumes memory can come back.

a Heap is safe to share between threads: one lock covers the core. a heap
one thread owns, as one per unit of work, takes the allocator `allocator_owned`
wires, which takes no lock.

a thread std started keeps a cache of small blocks for each heap it uses
through the allocator `allocator` wires, up to BOUND heaps at once, so most of
its requests and releases there take no lock: a class it has no block of is
refilled with a batch under one lock, and a class it holds too many of gives a
batch back. the cache goes back to its heap when the thread ends
(thread.at_exit), when the thread binds more heaps than it keeps caches for,
and when the heap is torn down. a thread std did not start takes the lock
every time, since nothing would give its cache back when it ends. a block a
cache holds counts as live, and a release is checked against its span as it
would be under the lock.

it satisfies the std.allocator interface, so it drops in wherever an Allocator
is taken:

  var src: heap.Source;
  var h:   heap.Heap;
  var a:   allocator.Allocator;
  heap.native_source(?src);
  heap.init(?h, ?src, 0);
  heap.allocator(?a, ?h);

requests up to MAX_SMALL (8 KiB) round to one of 32 classes carved from
64 KiB spans. a larger request gets a span of its own, from its size up to
that rounded to 64 KiB, the address range the span takes in any case.

alignment is honoured for every request. a small request aligned beyond 16
bytes is served by the first class that is a multiple of it, and one aligned
beyond a span is placed by address in a span of its own. a resize stays in
place while the block still holds the request and uses at least half of it,
and otherwise moves to the right class and copies the overlap.

zallocate_raw skips zeroing for a block carved from a region the source
delivered zero-filled, and zeroes anything reused.

native_source maps through the platform, allocator_source draws spans from
another Allocator, and region_source carves them from one region of memory the
program states, which is the source on a target with no page mapper:

  var r: heap.Region;
  heap.region_source(?src, ?r, base, len);

a program that makes one heap after another, each torn down whole, gives
them a Pool to share: pool_source draws spans from it and gives them back to
it, so the next heap is handed the spans the last one used. the program states
how many bytes the pool may hold:

  var pool: heap.Pool;
  heap.pool_init(?pool, ?src, budget);
  heap.pool_source(?pooled, ?pool);
  heap.init(?h, ?pooled, 0);

native_source is only on a target with the pages capability. init's budget bounds the retained empty spans. a heap
over a source that cannot release keeps them past the budget, because there
is nowhere else for them to go, and one whose release is refused is kept too,
so dnit tries it again and reports the failure. allocator_source makes that choice once: over
a backing that does not reclaim it leaves fn_release nil, so the heap keeps
every span it obtained and reuses it, and mapped_bytes still counts them
after dnit because the backing never took them back.

the span header, not the caller's arguments, decides a block's class. a size
larger than the block's class is refused. releasing a pointer this heap never
handed out is refused as allocator.Error.release(-22): the heap checks that
the address starts a block in a span it owns, so another heap's pointer, an
interior address or a span header is rejected without disturbing the heap.
this is detection, not a guarantee: a pointer into an unrelated mapping can
fault when the heap probes for a span header, as with any allocator. check
walks every span and verifies the heap's own invariants.

Source: [`src/allocator/heap.mach`](../../../src/allocator/heap.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.sync.mutex`](../sync/mutex.md).

| Type | | |
| :--- | :--- | :--- |
| [`Source`](#source) | `rec` | where a heap's backing memory comes from |
| [`Grant`](#grant) | `rec` | a span a source granted |
| [`Heap`](#heap) | `rec` | size-class heap state |
| [`Region`](#region) | `rec` | the state of a region source: the part of the region not yet handed out |
| [`Pool`](#pool) | `rec` | spans kept between heaps |

| On `Source` | |
| :--- | :--- |
| [`native_source`](#native_source) | fill in a Source backed by the host's page mapper |
| [`allocator_source`](#allocator_source) | fill in a Source backed by another allocator |
| [`region_source`](#region_source) | fill in a Source that carves spans from one region of memory |
| [`pool_source`](#pool_source) | fill in a Source that draws spans from a pool and gives them back to it |

| On `Heap` | |
| :--- | :--- |
| [`init`](#init) | initialize a Heap over a span source |
| [`allocator`](#allocator) | wire up an Allocator backed by this Heap |
| [`allocator_owned`](#allocator_owned) | wire up an Allocator backed by this Heap for one owner, taking no lock, so only one thread at a time may call it or anything else on the heap |
| [`dnit`](#dnit) | release every span back to the source and zero the heap state |
| [`zallocate_raw`](#zallocate_raw) | allocate `size` bytes of zeroed memory at `align` |
| [`live_bytes`](#live_bytes) | bytes in live blocks, counted as the class size or payload capacity charged for each one rather than the size requested |
| [`mapped_bytes`](#mapped_bytes) | bytes of the spans obtained from the source and not yet returned, each counted at the size the heap asked for, never at a larger grant |
| [`peak_mapped_bytes`](#peak_mapped_bytes) | high water mark of mapped_bytes over the heap's life |
| [`live_blocks`](#live_blocks) | live block count |
| [`allocated_blocks`](#allocated_blocks) | blocks handed out over the heap's life, never decremented |
| [`allocated_bytes`](#allocated_bytes) | bytes handed out over the heap's life, counted as the class size or payload capacity charged for each block as live_bytes counts it, never decremented |
| [`check`](#check) | verify the heap's own invariants |

| On `Pool` | |
| :--- | :--- |
| [`pool_init`](#pool_init) | initialize a Pool over a span source |
| [`pool_dnit`](#pool_dnit) | give every held span back to the source |

| Constants | |
| :--- | :--- |
| [`CLASS_COUNT`](#constants) | number of small size classes |
| [`MAX_SMALL`](#constants) | largest request served from a size class |
| [`SPAN_SIZE`](#constants) | span size for size-class spans, and the address granularity of every span |
| [`SPAN_ALIGN`](#constants) | |
| [`DEFAULT_CACHE`](#constants) | default byte budget for retained empty spans |
| [`PAGE_FLOOR`](#constants) | the granule a span's size rounds to on a target with no host page size |

---

## Source

```mach
pub rec Source {
    ctx:        ptr;
    fn_obtain:  fun(ptr, usize, usize) opt[Grant];
    fn_release: fun(ptr, ptr, usize) i64;
    stale:      bool;
    cuts:       bool;
}
```

where a heap's backing memory comes from

fn_obtain(ctx, least, most) returns a span of `least` to `most` bytes at an
address that is a multiple of SPAN_ALIGN, zero-filled unless the source is
`stale`, and the size it granted. every granted byte is the holder's to use.
`least` and `most` are always multiples of the host page size, or of
PAGE_FLOOR on a target with no pages, and `least` is never above `most`.

fn_release(ctx, span, size) returns a span obtained earlier, at the size it
was granted, 0 on success or a negative backend native code. it is nil for a
source that cannot return memory; the core then retains every span for reuse
and never calls it. a source that `cuts` also takes a granted span back in
pieces cut at multiples of SPAN_ALIGN from its base, each piece on its own.

| Field | Type | |
| :--- | :--- | :--- |
| `ctx` | `ptr` | opaque context passed to both callbacks |
| `fn_obtain` | `fun(ptr, usize, usize) opt[Grant]` | acquire a span, or none when the source is exhausted |
| `fn_release` | `fun(ptr, ptr, usize) i64` | return a span, or nil when the source cannot reclaim |
| `stale` | `bool` | a span it gives may hold what was written to it before |
| `cuts` | `bool` | a span it gives may come back in pieces |

### native_source

Only where `capability.HAS_PAGES`.

```mach
pub fun native_source(s: *Source)
```

fill in a Source backed by the host's page mapper

spans come from the platform mapper over-mapped and trimmed to SPAN_ALIGN,
and are returned to it whole.

| Parameter | |
| :--- | :--- |
| `s` | Source to initialize |

### allocator_source

```mach
pub fun allocator_source(s: *Source, backing: *std.allocator.Allocator)
```

fill in a Source backed by another allocator

spans are requested at SPAN_ALIGN and zeroed on the way out, so any backing
allocator that honors alignment can host a heap: a fixed buffer, an arena,
the page allocator, or the testing allocator for span-level accounting. a
backing that hands back a span off the SPAN_ALIGN grid gets it straight back
and the request is refused.

over a backing that does not reclaim (`allocator.reclaims` is false), giving
a span back would only spend the backing, so the source cannot release: the
heap keeps its spans, reuses them for any class, and growing past the budget
again takes nothing more from the backing. the backing's retains flag is read
here, so it must be settled before this call.

| Parameter | |
| :--- | :--- |
| `s` | Source to initialize |
| `backing` | allocator spans are drawn from (must outlive the heap) |

### region_source

```mach
pub fun region_source(s: *Source, r: *Region, base: ptr, len: usize)
```

fill in a Source that carves spans from one region of memory

the program states the region, such as a RAM range on bare metal that its
manifest leaves free, and every span comes from it in address order at
SPAN_ALIGN. a span is zeroed on the way out, since the region holds whatever
was there before. the region cannot take a span back, so fn_release is nil
and the heap keeps every span it obtained and reuses it, the way it does over
a backing that does not reclaim. a request the rest of the region cannot
hold is refused.

| Parameter | |
| :--- | :--- |
| `s` | Source to initialize |
| `r` | region state the source keeps (must outlive the heap) |
| `base` | first byte of the region |
| `len` | region length in bytes |

### pool_source

```mach
pub fun pool_source(s: *Source, p: *Pool)
```

fill in a Source that draws spans from a pool and gives them back to it

| Parameter | |
| :--- | :--- |
| `s` | Source to initialize |
| `p` | pool the spans are drawn from (must outlive the heap) |

## Grant

```mach
pub rec Grant {
    base: ptr;
    size: usize;
}
```

a span a source granted

| Field | Type | |
| :--- | :--- | :--- |
| `base` | `ptr` | its first byte, a multiple of SPAN_ALIGN |
| `size` | `usize` | the bytes it holds, from the least to the most asked for |

## Heap

```mach
pub rec Heap {
    src:  Source;
    lock: std.sync.mutex.Mutex;

    partial: [32]*Span;
    full:    [32]*Span;

    spans: *Span;
    cache: *Span;
    large: *Span;
    huge:  *Span;

    held:   usize;
    budget: usize;

    live:   usize;
    mapped: usize;
    peak:   usize;
    blocks: usize;

    total_blocks: usize;
    total_bytes:  usize;

    idx_small: [64]u8;
    idx_mid:   [64]u8;

    id:      usize;
    caches:  *Cache;
    spare:   *Cache;
    records: *Span;
    carved:  usize;
}
```

size-class heap state

`partial` holds spans of a class with a block to give, `full` the rest.
`spans` caches empty class spans for any class, `cache` freed large spans,
and `large` and `huge` track live spans that own a single block. a heap is
initialized once and then shared; every field below is under `lock`.

| Field | Type | |
| :--- | :--- | :--- |
| `src` | `Source` | span source |
| `lock` | `std.sync.mutex.Mutex` | covers the whole core |
| `partial` | `[32]*Span` | per class, spans with a free block |
| `full` | `[32]*Span` | per class, spans with none |
| `spans` | `*Span` | empty class spans held for reuse |
| `cache` | `*Span` | freed large spans held for reuse |
| `large` | `*Span` | live spans holding one block reachable by address masking |
| `huge` | `*Span` | live spans holding one block aligned at or past SPAN_ALIGN |
| `held` | `usize` | bytes in `spans` and `cache` |
| `budget` | `usize` | byte ceiling for `held` before a span is handed back to the source |
| `live` | `usize` | bytes in live blocks, counted as class size or payload capacity |
| `mapped` | `usize` | bytes of the spans obtained from the source and not yet released, each counted at the size the heap uses |
| `peak` | `usize` | high water mark of `mapped` |
| `blocks` | `usize` | live block count |
| `total_blocks` | `usize` | blocks handed out over the heap's life, never decremented |
| `total_bytes` | `usize` | bytes charged for them, counted as `live` counts and never decremented |
| `idx_small` | `[64]u8` | class index for each 16 byte step of a size up to 1024 |
| `idx_mid` | `[64]u8` | class index for each 128 byte step of a size up to MAX_SMALL |
| `id` | `usize` | the heap's identity, never shared with another heap of the process |
| `caches` | `*Cache` | the thread caches bound to the heap |
| `spare` | `*Cache` | cache records given back, for the next thread that binds |
| `records` | `*Span` | the span cache records are carved from, nil before the first |
| `carved` | `usize` | records carved from it |

### init

```mach
pub fun init(h: *Heap, src: *Source, budget: usize) err[std.allocator.Error]
```

initialize a Heap over a span source

the source is copied into the heap, so the caller's Source may be discarded;
whatever the source's ctx points at must outlive the heap.

| Parameter | |
| :--- | :--- |
| `h` | Heap to initialize |
| `src` | span source the heap draws from |
| `budget` | byte ceiling for retained empty spans, 0 for the default |
| **returns** | ok, or `invalid` for a nil heap, a nil source, or a source with no obtain callback |

### allocator

```mach
pub fun allocator(a: *std.allocator.Allocator, h: *Heap) err[std.allocator.Error]
```

wire up an Allocator backed by this Heap

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| `h` | initialized Heap (must outlive the Allocator) |
| **returns** | ok, or `invalid` when either pointer is nil |

### allocator_owned

```mach
pub fun allocator_owned(a: *std.allocator.Allocator, h: *Heap) err[std.allocator.Error]
```

wire up an Allocator backed by this Heap for one owner, taking no lock, so
only one thread at a time may call it or anything else on the heap

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| `h` | initialized Heap (must outlive the Allocator) |
| **returns** | ok, or `invalid` when either pointer is nil |

### dnit

```mach
pub fun dnit(h: *Heap) err[std.allocator.Error]
```

release every span back to the source and zero the heap state

live blocks are abandoned, so this is a teardown of the whole heap and not a
way to free one allocation. every span is attempted even when one release
fails, and the first failure is what is reported.

| Parameter | |
| :--- | :--- |
| `h` | Heap to destroy |
| **returns** | ok, or the first negative backend native code as `release` |

### zallocate_raw

```mach
pub fun zallocate_raw(h: *Heap, size: usize, align: usize) res[ptr, std.allocator.Error]
```

allocate `size` bytes of zeroed memory at `align`

a block carved from a region the source delivered zeroed is returned as is,
so a fresh span costs no write. anything reused is zeroed explicitly.

| Parameter | |
| :--- | :--- |
| `h` | Heap to allocate from |
| `size` | number of bytes (0 returns nil) |
| `align` | alignment in bytes, a power of two |
| **returns** | ptr to zeroed memory, or the refusal |

### live_bytes

```mach
pub fun live_bytes(h: *Heap) usize
```

bytes in live blocks, counted as the class size or payload capacity charged
for each one rather than the size requested

### mapped_bytes

```mach
pub fun mapped_bytes(h: *Heap) usize
```

bytes of the spans obtained from the source and not yet returned, each
counted at the size the heap asked for, never at a larger grant

### peak_mapped_bytes

```mach
pub fun peak_mapped_bytes(h: *Heap) usize
```

high water mark of mapped_bytes over the heap's life

### live_blocks

```mach
pub fun live_blocks(h: *Heap) usize
```

live block count

### allocated_blocks

```mach
pub fun allocated_blocks(h: *Heap) usize
```

blocks handed out over the heap's life, never decremented

### allocated_bytes

```mach
pub fun allocated_bytes(h: *Heap) usize
```

bytes handed out over the heap's life, counted as the class size or payload
capacity charged for each block as live_bytes counts it, never decremented

### check

```mach
pub fun check(h: *Heap) bool
```

verify the heap's own invariants

walks every span the heap holds and checks its header, its position, its
free list and the accounting totals against what the spans say. intended
for tests and for a caller that suspects heap corruption.

| Parameter | |
| :--- | :--- |
| `h` | Heap to check |
| **returns** | true when every invariant holds |

## Region

```mach
pub rec Region {
    next: usize;
    stop: usize;
}
```

the state of a region source: the part of the region not yet handed out

| Field | Type | |
| :--- | :--- | :--- |
| `next` | `usize` | first byte not yet handed out |
| `stop` | `usize` | one past the region's last byte |

## Pool

```mach
pub rec Pool {
    src:    Source;
    lock:   std.sync.mutex.Mutex;
    bins:   [POOL_BINS]*Held;
    newest: *Held;
    oldest: *Held;
    held:   usize;
    budget: usize;
}
```

spans kept between heaps

a heap gives its spans back to its source when it is torn down or runs past
its budget. over the host mapper that unmaps them, and the next heap maps and
faults the same memory in again. a pool stands between heaps and their real
source: a span given back is held at the size it was granted and granted
again, whole, to the next request whose range takes it, the smallest such
span and of those the last given back. a heap uses only the least of a
grant, so which span a heap is handed, which depends on what other heaps
gave back, never changes what the heap does or counts. nothing is rounded, so no byte of a
span lies past what its holder was granted. when no held span is in range and
the source cuts, the smallest span past the range is cut: its first bytes,
the request rounded to SPAN_ALIGN when the range takes that, are granted and
the rest stays held, so a pool holding large spans serves a smaller request
without going to its source. when a span given back would
take the held bytes past the budget, the spans held longest go back to the
source first, since the next requests take the last given back. a request no
held span fits goes to the source as it is, and so does a span past the
largest bin. a held span keeps what was written to it, so a pool's source is
stale.

| Field | Type | |
| :--- | :--- | :--- |
| `src` | `Source` | where spans come from and go back to |
| `lock` | `std.sync.mutex.Mutex` | covers every field below |
| `bins` | `[POOL_BINS]*Held` | held spans by size, latest given back first |
| `newest` | `*Held` | the span given back last |
| `oldest` | `*Held` | the span held longest |
| `held` | `usize` | bytes in the bins |
| `budget` | `usize` | byte ceiling for `held`, past which the oldest spans go back to the source |

### pool_init

```mach
pub fun pool_init(p: *Pool, src: *Source, budget: usize) err[std.allocator.Error]
```

initialize a Pool over a span source

the source is copied into the pool, and whatever its ctx points at must
outlive the pool. a pool over a source that cannot release holds every span
given back to it, whatever the budget.

| Parameter | |
| :--- | :--- |
| `p` | Pool to initialize |
| `src` | span source the pool draws from |
| `budget` | byte ceiling for held spans, 0 for no ceiling |
| **returns** | ok, or `invalid` for a nil pool, a nil source, or a source with no obtain callback |

### pool_dnit

```mach
pub fun pool_dnit(p: *Pool) err[std.allocator.Error]
```

give every held span back to the source. every heap drawing from the pool
must be torn down first

| Parameter | |
| :--- | :--- |
| `p` | Pool to tear down |
| **returns** | ok, or the first status the source refused a span with |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `CLASS_COUNT` | `usize` | `32` | number of small size classes |
| `MAX_SMALL` | `usize` | `8192` | largest request served from a size class |
| `SPAN_SIZE` | `usize` | `65536` | span size for size-class spans, and the address granularity of every span |
| `SPAN_ALIGN` | `usize` | `65536` |  |
| `DEFAULT_CACHE` | `usize` | `4194304` | default byte budget for retained empty spans |
| `PAGE_FLOOR` | `usize` | `4096` | the granule a span's size rounds to on a target with no host page size |

