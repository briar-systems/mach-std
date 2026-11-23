[std](../README.md) / [memory](README.md) / **linear**

# std.memory.linear

the pages of a wasm linear memory, which only grows

`memory.size` reads how many 64 KiB pages the memory holds and `memory.grow`
adds pages past its end, zero filled by the host. nothing gives a page back
to the host, so pages a caller gives back stay here, in address order and
merged, and the next allocation takes them first. the heap region is the run
of pages from the first one past what was handed out when it was first asked
for. this is the machine's own memory, the same on every wasm target with or
without a system, so the wasi layer and std's heap on a freestanding module
both draw on it.

Source: [`src/memory/linear.mach`](../../../src/memory/linear.mach)

| Functions | |
| :--- | :--- |
| [`page_size`](#page_size) | the wasm page size, 64 KiB, which every allocation here is counted in |
| [`allocate`](#allocate) | whole zero-filled pages, kept ones first |
| [`deallocate`](#deallocate) | keep pages for the next allocate, merged with their neighbours |
| [`reallocate`](#reallocate) | resize a page allocation, in place when its pages still hold it |
| [`heap_region_base`](#heap_region_base) | the first address past what has been handed out |
| [`heap_region_extend`](#heap_region_extend) | move the region's end up to addr |

---

## Functions

### page_size

```mach
pub fun page_size() usize
```

the wasm page size, 64 KiB, which every allocation here is counted in

| Parameter | |
| :--- | :--- |
| **returns** | page size in bytes |

### allocate

```mach
pub fun allocate(size: usize) ptr
```

whole zero-filled pages, kept ones first

| Parameter | |
| :--- | :--- |
| `size` | bytes wanted |
| **returns** | the pages, or nil when memory is exhausted |

### deallocate

```mach
pub fun deallocate(p: ptr, size: usize) bool
```

keep pages for the next allocate, merged with their neighbours

| Parameter | |
| :--- | :--- |
| `p` | the pages, on a page boundary |
| `size` | their size in bytes |
| **returns** | false for an address off a page, which is kept nowhere |

### reallocate

```mach
pub fun reallocate(p: ptr, old_size: usize, new_size: usize) ptr
```

resize a page allocation, in place when its pages still hold it

### heap_region_base

```mach
pub fun heap_region_base() usize
```

the first address past what has been handed out

### heap_region_extend

```mach
pub fun heap_region_extend(addr: usize) usize
```

move the region's end up to addr

the region is contiguous: it takes kept pages that start where it ends, then
new memory once it reaches the end of linear memory, so it stops growing
while pages `allocate` handed out lie past it

| Parameter | |
| :--- | :--- |
| `addr` | the address wanted |
| **returns** | the address reached, on a page and at least addr, which stays put when addr is out of reach |

