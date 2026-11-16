[std](../README.md) / **allocator**

# std.allocator

generic allocator interface and utilities

this is intended to be the glue between platform memory primitives and higher
level containers/types

The directory's root module is [`std.allocator`](../allocator.md).

| Module | |
| :--- | :--- |
| [`arena`](arena.md) | arena allocator implementation |
| [`bump`](bump.md) | brk-based bump allocator |
| [`fixed`](fixed.md) | fixed-buffer bump allocator |
| [`heap`](heap.md) | general-purpose size-class heap |
| [`page`](page.md) | page allocator adapter |
| [`testing`](testing.md) | an allocator built to make memory bugs fail loudly in tests |

