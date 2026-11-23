[std](../../README.md) / [net](../README.md) / **async**

# std.net.async

portable bounded asynchronous TCP and UDP

ownership: a socket this driver has seen in a submission is closed through
the driver (submit_stream_close, submit_datagram_close), never directly. a
socket closed outside the driver is detected on its next submission through
either handle: the old socket's pending work completes CLOSED with code 0,
a submission through the old handle is refused the same way, and the socket
that now holds the native value keeps its own state. the driver tells the
two apart by the handle's opening (std.io.handle.socket), so wrap a native
socket once and pass that handle around

cancellation: an operation cancelled through its scope completes CANCELLED
once the platform gives up its buffers. on windows that happens when the
aborted request reports back, so the completion can arrive after the cancel
returns and destroy stays busy until it does (awaiting_cancellations). a
cancelled completion still reports the transfer that finished before the
cancellation: a read's bytes, which the caller must consume, a write's sent
bytes and a batch's datagrams (submit_read, submit_write), and the socket an
accept took, which the caller owns (accepted)

The directory's root module is [`std.net.async`](../async.md).

| Module | |
| :--- | :--- |
| [`darwin`](darwin.md) | the darwin part of the linux and darwin readiness backend for internet sockets backend for std.net.async, signatures may change in a minor release (README, API surface) std.net.async.unix holds the backend |
| [`iocp`](iocp.md) | per-socket bookkeeping shared by the windows completion port backends backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface) |
| [`linux`](linux.md) | the linux part of the linux and darwin readiness backend for internet sockets backend for std.net.async, signatures may change in a minor release (README, API surface) std.net.async.unix holds the backend |
| [`local`](local.md) | portable bounded asynchronous local byte streams |
| [`readiness`](readiness.md) | bounded readiness engine shared by the linux and darwin socket backends engine for std.net.async.unix and std.net.async.local.unix, signatures may change in a minor release (README, API surface) a backend brings a Protocol: its operation record, the one nonblocking try at an operation, and how it admits a socket |
| [`retired`](retired.md) | the openings detach retired, across every driver in the process |
| [`types`](types.md) | portable asynchronous network descriptors |
| [`unix`](unix.md) | bounded linux and darwin readiness backend for internet sockets backend for std.net.async, signatures may change in a minor release (README, API surface) the engine is std.net.async.readiness, and std.net.async.linux and .darwin hold the control-message layout that differs between the two |
| [`windows`](windows.md) | bounded windows IOCP backend and overlapped socket operations backend for std.net.async, signatures may change in a minor release (README, API surface) |

| Directory | |
| :--- | :--- |
| [`iocp/`](iocp/README.md) | per-socket bookkeeping shared by the windows completion port backends backend for std.net.async and std.net.async.local, signatures may change in a minor release (README, API surface) |
| [`local/`](local/README.md) | portable bounded asynchronous local byte streams |

