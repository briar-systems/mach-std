[std](../../../README.md) / [net](../../README.md) / [async](../README.md) / **local**

# std.net.async.local

portable bounded asynchronous local byte streams

reads follow std.net.local's byte-only receive contract, under this backend's
read lane ownership. a buffer stays borrowed until its completion, and a
darwin refusal completes with zero bytes and leaves the stream open. the
generic linux and darwin net.async backends accept only ip socket handles,
checked before registration, so a local handle never reaches a byte path that
does not own rights: use this backend for local streams.

cancellation follows std.net.async: on windows a cancelled operation completes
once its aborted request reports back, and a cancelled completion reports the
bytes a read took, which the caller must consume, or a write sent
(submit_read, submit_write)

The directory's root module is [`std.net.async.local`](../local.md).

| Module | |
| :--- | :--- |
| [`unix`](unix.md) | bounded local unix readiness backend backend for std.net.async.local, signatures may change in a minor release (README, API surface) the engine is std.net.async.readiness |
| [`windows`](windows.md) | bounded windows iocp backend for af_unix streams backend for std.net.async.local, signatures may change in a minor release (README, API surface) |

