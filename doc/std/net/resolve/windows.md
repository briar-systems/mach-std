[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **windows**

# std.net.resolve.windows

windows winsock system resolver adapter

Source: [`src/net/resolve/windows.mach`](../../../../src/net/resolve/windows.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.resolve.types`](types.md).

| Functions | |
| :--- | :--- |
| [`resolve`](#resolve) | |

---

## Functions

### resolve

```mach
pub fun resolve(query: *std.net.resolve.types.Query, owner: *std.allocator.Allocator, limits: std.net.resolve.types.ResultLimits, output: *std.net.resolve.types.Resolution) std.net.resolve.types.Error
```

