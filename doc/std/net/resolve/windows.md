[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **windows**

# std.net.resolve.windows

windows winsock system resolver adapter

Source: [`src/net/resolve/windows.mach`](../../../../src/net/resolve/windows.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.resolve.types`](types.md), [`std.sync.cancel`](../../sync/cancel.md).

| Functions | |
| :--- | :--- |
| [`resolve`](#resolve) | resolve through the system's GetAddrInfoExW, under the scope |

---

## Functions

### resolve

```mach
pub fun resolve(scope: *std.sync.cancel.Scope, query: *std.net.resolve.types.Query, owner: *std.allocator.Allocator, limits: std.net.resolve.types.ResultLimits, output: *std.net.resolve.types.Resolution) std.net.resolve.types.Error
```

resolve through the system's GetAddrInfoExW, under the scope

the call runs asynchronously, completed by the system on a thread of its own
into a request the library owns: copies of the query's strings, the hints, the
overlapped block and the result. the caller waits for it under the scope and
returns within shared.POLL_MSEC of the scope ending, with the scope's reason,
after asking GetAddrInfoExCancel to end the call. the completion that follows,
whenever the system delivers it, frees the request and its result, so nothing
of the caller's is touched after the return

