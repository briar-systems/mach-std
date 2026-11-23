[std](../../README.md) / [net](../README.md) / **local**

# std.net.local

portable local byte-stream descriptors and endpoint ownership

a stream has one closing owner. its receive queue is borrowed exclusively for
each read, across every raw or duplicated alias: a concurrent receive, receive
shutdown or close through another alias is invalid. peer writes and
operations on unrelated descriptors may run concurrently.

reads deliver bytes only. a peer may attach descriptor rights to those bytes,
and the stream never hands them to the caller or lets them occupy its
descriptor table:

- linux receives with MSG_CMSG_CLOEXEC into control storage sized for the
  kernel's bound (SCM_MAX_FD plus the SO_PASSCRED and SO_PASSPIDFD records)
  and closes every SCM_RIGHTS and SCM_PIDFD descriptor it reports. the storage
  is zero-filled first, so a native failure after rights were installed is
  still walked. MSG_CTRUNC means the kernel dropped records it could not
  report, and it installs none it does not report, so the walk is complete.
  std.system.os.linux.sock_recv_close_rights is that primitive with caller
  storage, and local_stream_recv supplies the bound.
- darwin inspects without consuming (MSG_PEEK with one control header),
  refuses any ancillary data or truncation as UNSUPPORTED, and otherwise
  consumes at most the inspected byte count. a zero-length read does not
  inspect. a refusal leaves the socket open with its queued rights still owned
  by it, and closing the stream releases them. native failures keep their
  cause, and buffer contents on failure are unspecified.
- windows local sockets carry no rights, so reads are plain.

raw os sock_recv and sock_receive_message keep native ancillary behaviour and
do not give this byte-only contract.

a filesystem endpoint is named by the bytes of its path. filesystem takes the
path as UTF-8 and filesystem_native in std.runtime.native units: bytes on
linux and darwin, passed through unchanged, and UTF-16 on windows, converted
once to UTF-8. windows sun_path is a byte string too, so the kernel cannot
name a socket at a path holding an unpaired surrogate, which has no UTF-8
spelling. filesystem_native refuses such a path with INVALID before any
socket call.

The directory's root module is [`std.net.local`](../local.md).

| Module | |
| :--- | :--- |
| [`endpoint`](endpoint.md) | tagged local transport endpoints and target capabilities |
| [`types`](types.md) | local transport descriptor and ownership types |
| [`unix`](unix.md) | unix-domain local byte streams |
| [`windows`](windows.md) | windows af_unix local byte streams |

