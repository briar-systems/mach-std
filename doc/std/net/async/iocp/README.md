[std](../../../README.md) / [net](../../README.md) / [async](../README.md) / **iocp**

# std.net.async.iocp

per-socket bookkeeping shared by the windows completion port backends
backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface)

the core decides what each state change on a socket makes due and makes no
native call itself, so a backend performs whatever a decision asks for and
every decision costs the same whatever else the backend holds. a backend
embeds one Link in each operation and hands the core the operation table and
the link's offset, so the core never owns or moves an operation

The directory's root module is [`std.net.async.iocp`](../iocp.md).

| Module | |
| :--- | :--- |
| [`port`](port.md) | the completion port layer shared by the windows net.async backends backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface) |

