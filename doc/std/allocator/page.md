[std](../README.md) / [allocator](README.md) / **page**

# std.allocator.page

page allocator adapter

wraps platform page allocation functions for the Allocator interface. a
page allocation is page-aligned by nature, so an alignment up to the page
costs nothing. above the page the mapping is widened by the alignment and
the block placed inside it: posix trims the pages on either side, and
windows, which releases a reservation only whole, stashes the raw base in
the word ahead of the block.

Source: [`src/allocator/page.mach`](../../../src/allocator/page.mach)

Uses types from [`std.allocator`](../allocator.md).

| Functions | |
| :--- | :--- |
| [`make`](#make) | initialize a page-backed Allocator |

---

## Functions

### make

```mach
pub fun make(a: *std.allocator.Allocator) err[std.allocator.Error]
```

initialize a page-backed Allocator

| Parameter | |
| :--- | :--- |
| `a` | Allocator to initialize |
| **returns** | ok, or `invalid` when a is nil |

