[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **darwin**

# std.net.resolve.darwin

darwin libsystem resolver adapter

Source: [`src/net/resolve/darwin.mach`](../../../../src/net/resolve/darwin.mach)

Uses types from [`std.allocator`](../../allocator.md), [`std.net.resolve.types`](types.md), [`std.sync.cancel`](../../sync/cancel.md).

| Functions | |
| :--- | :--- |
| [`resolve`](#resolve) | resolve through the system's getaddrinfo, under the scope |

---

## Functions

### resolve

```mach
pub fun resolve(scope: *std.sync.cancel.Scope, query: *std.net.resolve.types.Query, owner: *std.allocator.Allocator, limits: std.net.resolve.types.ResultLimits, output: *std.net.resolve.types.Resolution) std.net.resolve.types.Error
```

resolve through the system's getaddrinfo, under the scope

getaddrinfo cannot be interrupted, so it runs on a helper thread that owns
the request: copies of the query's strings, the hints and the result. the
caller waits for it under the scope and returns within shared.POLL_MSEC of
the scope ending, with the scope's reason. the helper then finishes when the
system lets it and frees the request and its result itself, so nothing of the
caller's is touched after the return. each lookup costs a thread, which may
outlive the call by the system's own timeout, and a process that exits while
one runs ends it with every other thread

