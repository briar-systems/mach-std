[std](../README.md) / [memory](README.md) / **table**

# std.memory.table

chunked element storage whose live elements never move

Source: [`src/memory/table.mach`](../../../src/memory/table.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Table`](#table) | `rec` | chunk 0 holds `1 << shift` elements and chunk k holds `1 << (shift + k - 1)`, so capacity doubles per chunk and an element address is fixed once handed out allocator: where every chunk comes from and goes back to |
| [`Pool`](#pool) | `rec` | the free indices of a table, handed out lowest chunk first and oldest first within a chunk, so steady churn drains the high chunks and an index waits behind the other free ones of its chunk |

| On `Table` | |
| :--- | :--- |
| [`init`](#init) | a table whose chunks come from a |
| [`grow`](#grow) | appended elements are uninitialised and the caller owns their first write |
| [`reserve`](#reserve) | |
| [`chunk_of`](#chunk_of) | the chunk holding index, for an index below the capacity |
| [`chunk_start`](#chunk_start) | the first index chunk holds |
| [`chunk_capacity`](#chunk_capacity) | how many elements chunk holds |
| [`shrink`](#shrink) | return the last chunk to the table's allocator |
| [`at`](#at) | |
| [`index_of`](#index_of) | recover an element's index from its address, for callers that hand the address itself out as a resource identity |
| [`dnit`](#dnit) | return every chunk to the table's allocator |
| [`aliases`](#aliases) | |
| [`trim`](#trim) | release the capacity a peak left behind |
| [`trim_backed`](#trim_backed) | trim for a table that has promised capacity no element holds yet |

| On `Pool` | |
| :--- | :--- |
| [`pool_make`](#pool_make) | an empty pool whose elements link through the usize at byte offset link |
| [`pool_adopt`](#pool_adopt) | every index of the owner's newest chunk joins the pool free, in index order |
| [`pool_untouched`](#pool_untouched) | whether the pool has never handed index out since its chunk was adopted, so neither the pool nor a taker has written it |
| [`pool_touched_from`](#pool_touched_from) | the lowest touched index at or past index, or NO_INDEX when none is left |
| [`pool_oldest`](#pool_oldest) | chunk's oldest free index, which stays free, or NO_INDEX when chunk has none free |
| [`pool_newest`](#pool_newest) | chunk's newest free index, the last pool_take_head would hand out, or NO_INDEX when chunk has none free |
| [`pool_peek`](#pool_peek) | the index pool_take would hand out, which stays free, or NO_INDEX |
| [`pool_take_fresh`](#pool_take_fresh) | pool_take that says whether the index it hands out was untouched until now, so its taker writes the element in full before any other read |
| [`pool_take_head`](#pool_take_head) | chunk's oldest free index, now taken, or NO_INDEX when chunk has none free |
| [`pool_take`](#pool_take) | the lowest chunk's oldest free index, now taken, or NO_INDEX when every index is taken |
| [`pool_put`](#pool_put) | a taken index goes back to the pool, behind the other free ones of its chunk |
| [`pool_shrink`](#pool_shrink) | release the owner's last chunk, whose indices are all free, with its list |
| [`pool_trim`](#pool_trim) | trim for a pooled table, whose floor is the pool's |
| [`pool_trim_backed`](#pool_trim_backed) | trim_backed for a pooled table, whose floor is the pool's |

| Constants | |
| :--- | :--- |
| [`DIRECTORY`](#constants) | the directory is inline and fixed, so growth never moves it either |
| [`ELEMENT_ALIGN`](#constants) | every chunk is requested at this alignment, so an element type may need at most this much |
| [`NO_INDEX`](#constants) | |

---

## Table

```mach
pub rec Table {
    allocator:    std.allocator.Allocator;
    chunks:       [DIRECTORY]ptr;
    element_size: usize;
    shift:        usize;
    chunk_count:  usize;
    capacity:     usize;
}
```

chunk 0 holds `1 << shift` elements and chunk k holds `1 << (shift + k - 1)`,
so capacity doubles per chunk and an element address is fixed once handed out
allocator: where every chunk comes from and goes back to

### init

```mach
pub fun init(table: *Table, a: *std.allocator.Allocator, element_size: usize, initial: usize) bool
```

a table whose chunks come from a

the table keeps a copy of a, so the allocator's context must outlive the
table. the only failure is a refused or unrepresentable allocation, so the
result carries no cause

| Parameter | |
| :--- | :--- |
| `table` | the table to initialize |
| `a` | the allocator every chunk is taken from and returned to |
| `element_size` | bytes per element, whose alignment is at most ELEMENT_ALIGN |
| `initial` | the first chunk's element count, rounded up to a power of two |
| **returns** | whether the table was made |

### grow

```mach
pub fun grow(table: *Table) bool
```

appended elements are uninitialised and the caller owns their first write

### reserve

```mach
pub fun reserve(table: *Table, count: usize) bool
```

### chunk_of

```mach
pub fun chunk_of(table: *Table, index: usize) usize
```

the chunk holding index, for an index below the capacity

### chunk_start

```mach
pub fun chunk_start(table: *Table, chunk: usize) usize
```

the first index chunk holds

### chunk_capacity

```mach
pub fun chunk_capacity(table: *Table, chunk: usize) usize
```

how many elements chunk holds

### shrink

```mach
pub fun shrink(table: *Table) err[std.allocator.Error]
```

return the last chunk to the table's allocator

the first chunk is never released, and every element below the new capacity
stays where it was. the caller owns knowing that no element of the released
chunk is still in use. over an allocator that does not reclaim, a released
chunk could never be reused and growing again would take fresh bytes, so the
table keeps it and a shrink is refused

| Parameter | |
| :--- | :--- |
| `table` | the table to shrink |
| **returns** | ok, invalid for a nil table, one with a single chunk or one whose allocator does not reclaim, or the allocator's refusal, which leaves the table and its last chunk as they were |

### at

```mach
pub fun at(table: *Table, index: usize) ptr
```

### index_of

```mach
pub fun index_of(table: *Table, address: usize) usize
```

recover an element's index from its address, for callers that hand the
address itself out as a resource identity

### dnit

```mach
pub fun dnit(table: *Table) err[std.allocator.Error]
```

return every chunk to the table's allocator

every chunk is released even after one release fails, and the table is empty
afterwards either way. destroying an empty or never-made table succeeds

| Parameter | |
| :--- | :--- |
| `table` | the table to destroy |
| **returns** | ok, or the first refusal the allocator reported |

### aliases

```mach
pub fun aliases(table: *Table, data: *u8, len: usize) bool
```

### trim

```mach
pub fun trim(table: *Table, live: *usize, generation: usize, floor: *u32) usize
```

release the capacity a peak left behind. the last chunk goes once it and the
chunk below it both hold nothing live, so one empty chunk always remains as
slack and a load crossing a chunk boundary back and forth never reallocates.
only empty chunks are released, so nothing live moves. over an allocator
that does not reclaim nothing is released and the table keeps its peak, as
shrink does

an element that carries a generation keeps it as a u32 at byte offset
generation, and floor rises to the highest one a released chunk held. an
element made in a regrown chunk starts from floor, so no handle issued in the
released chunk matches it

| Parameter | |
| :--- | :--- |
| `live` | the live element count of each chunk, DIRECTORY entries |
| `generation` | byte offset of the elements' u32 generation, or NO_INDEX for elements that carry none |
| `floor` | raised to the released chunks' highest generation, nil when generation is NO_INDEX |
| **returns** | chunks released. a refused release stops there and keeps the chunk |

### trim_backed

```mach
pub fun trim_backed(table: *Table, live: *usize, generation: usize, floor: *u32, backed: usize) usize
```

trim for a table that has promised capacity no element holds yet. the lowest
backed indices count as live whatever their chunks' live counts say, so a
chunk goes only once the promise fits below the chunk under it, and the
capacity never falls below backed

| Parameter | |
| :--- | :--- |
| `backed` | elements that must stay backed, as though they filled the lowest indices |
| **returns** | chunks released |

## Pool

```mach
pub rec Pool {
    live:     [DIRECTORY]usize;
    head:     [DIRECTORY]usize;
    tail:     [DIRECTORY]usize;
    frontier: [DIRECTORY]usize;
    lowest:   usize;
    link:     usize;
    floor:    u32;
}
```

the free indices of a table, handed out lowest chunk first and oldest first
within a chunk, so steady churn drains the high chunks and an index waits
behind the other free ones of its chunk. an index the pool has never handed
out is older than every index given back, and the pool reads and writes none
of its bytes, so a chunk's untouched tail costs address space and not
resident memory. the free lists of indices given back link through a usize
inside each free element, so the pool allocates nothing

| Field | Type | |
| :--- | :--- | :--- |
| `live` | `[DIRECTORY]usize` | taken indices per chunk |
| `head` | `[DIRECTORY]usize` | each chunk's oldest index given back and free |
| `tail` | `[DIRECTORY]usize` | each chunk's newest index given back and free |
| `frontier` | `[DIRECTORY]usize` | each chunk's lowest index never handed out, the chunk's end once every index has been |
| `lowest` | `usize` | no chunk below this one holds a free index |
| `link` | `usize` | byte offset of the usize link inside an element |
| `floor` | `u32` | the generation an element of a regrown chunk starts from, above every generation a released chunk issued (pool_trim) |

### pool_make

```mach
pub fun pool_make(pool: *Pool, link: usize)
```

an empty pool whose elements link through the usize at byte offset link

### pool_adopt

```mach
pub fun pool_adopt(pool: *Pool, owner: *Table)
```

every index of the owner's newest chunk joins the pool free, in index order.
the pool writes nothing into the chunk: an index stays untouched until the
pool first hands it out, and pool_untouched says which are, so a caller may
initialise an element when it is first taken instead of here

### pool_untouched

```mach
pub fun pool_untouched(pool: *Pool, owner: *Table, index: usize) bool
```

whether the pool has never handed index out since its chunk was adopted, so
neither the pool nor a taker has written it. an index past the owner's
capacity counts as untouched

### pool_touched_from

```mach
pub fun pool_touched_from(pool: *Pool, owner: *Table, index: usize) usize
```

the lowest touched index at or past index, or NO_INDEX when none is left. a
scan over a pooled table walks it instead of the capacity, so it reads no
element the pool never handed out

### pool_oldest

```mach
pub fun pool_oldest(pool: *Pool, owner: *Table, chunk: usize) usize
```

chunk's oldest free index, which stays free, or NO_INDEX when chunk has none
free

### pool_newest

```mach
pub fun pool_newest(pool: *Pool, owner: *Table, chunk: usize) usize
```

chunk's newest free index, the last pool_take_head would hand out, or
NO_INDEX when chunk has none free

### pool_peek

```mach
pub fun pool_peek(pool: *Pool, owner: *Table) usize
```

the index pool_take would hand out, which stays free, or NO_INDEX

### pool_take_fresh

```mach
pub fun pool_take_fresh(pool: *Pool, owner: *Table, fresh: *bool) usize
```

pool_take that says whether the index it hands out was untouched until now,
so its taker writes the element in full before any other read

### pool_take_head

```mach
pub fun pool_take_head(pool: *Pool, owner: *Table, chunk: usize) usize
```

chunk's oldest free index, now taken, or NO_INDEX when chunk has none free.
a taken index's link holds NO_INDEX

### pool_take

```mach
pub fun pool_take(pool: *Pool, owner: *Table) usize
```

the lowest chunk's oldest free index, now taken, or NO_INDEX when every
index is taken

### pool_put

```mach
pub fun pool_put(pool: *Pool, owner: *Table, index: usize)
```

a taken index goes back to the pool, behind the other free ones of its chunk

### pool_shrink

```mach
pub fun pool_shrink(pool: *Pool, owner: *Table) bool
```

release the owner's last chunk, whose indices are all free, with its list

| Parameter | |
| :--- | :--- |
| **returns** | whether the chunk was released. a refusal keeps the chunk and its list |

### pool_trim

```mach
pub fun pool_trim(pool: *Pool, owner: *Table, generation: usize) usize
```

trim for a pooled table, whose floor is the pool's

| Parameter | |
| :--- | :--- |
| `generation` | byte offset of the elements' u32 generation, or NO_INDEX |
| **returns** | chunks released |

### pool_trim_backed

```mach
pub fun pool_trim_backed(pool: *Pool, owner: *Table, generation: usize, backed: usize) usize
```

trim_backed for a pooled table, whose floor is the pool's

| Parameter | |
| :--- | :--- |
| `generation` | byte offset of the elements' u32 generation, or NO_INDEX |
| `backed` | elements that must stay backed, as in trim_backed |
| **returns** | chunks released |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `DIRECTORY` | `usize` | `40` | the directory is inline and fixed, so growth never moves it either |
| `ELEMENT_ALIGN` | `usize` | `16` | every chunk is requested at this alignment, so an element type may need at most this much |
| `NO_INDEX` | `usize` | `~(0::usize)` |  |

