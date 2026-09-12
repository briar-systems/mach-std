# Darwin socket boundary probe

Run natively on both Darwin architectures with debug and release builds. Snapshot
the exact std manifest and source under this fixture's `dep/std`, then build the
Mach probe with the matching target, profile and explicit `-o bin/socket`.

Compile `layout.c` with the native SDK using C11 and warnings as errors. It checks
all fifteen public function signatures and retains a reference to every symbol.
Compare its output to `bin/socket layout` and inspect the C object's undefined
symbols against the Mach image's imports. This detects SDK aliases as well as
record size, alignment and field offsets. Run the C probe with `option` and
compare its raw SO_KEEPALIVE value and length with the Mach `stream` output.
An enabled native option need only be nonzero, not normalized to one. Endpoint
checks compare the address fields, excluding reserved sockaddr padding.

The `errors`, `stream`, `vectors`, `messages` and `datagrams` modes must each exit
zero. Stream and datagram traffic stays local. Blocking network reads have receive
timeouts. The stream mode checks accepted flags before publication, endpoint
agreement, options, would-block and shutdown EOF. The vector mode saturates a
bounded local socket buffer, requires a positive partial count, and compares every
received byte. The message mode verifies scatter/gather, transferred descriptor
ownership, payload and ancillary truncation, and descriptor counts after discarded
rights. The datagram mode checks explicit destination and returned source lengths.

`create-refusal` and `accept-refusal` are verification-only entry points for a
controlled native flag-configuration error. The verifier must inject EIO into the
corresponding configuration result, require the invalid output sentinel and
unchanged descriptor count, then remove only the cleanup close and require the
specific descriptor-leak failure. These modes are not baseline success tests.

Use the existing native fixture to run the socket, TCP, UDP and Darwin async tests
as additional coverage. Record source/compiler provenance and a clear compiler
process census before every Mach build or test. Timeouts and compilation failures
never count as successful runtime controls.

The nil-control receive uses a plain datagram with no ancillary data and checks payload truncation, zero returned control length and no acquired descriptor. Its raw result, flags, length and descriptor-count delta must match `control.c` on the same host. A nil control buffer requests no ancillary output, so this case does not require `MSG_CTRUNC`. The separate nonempty rights transfer and returned-flags control retain their strict checks.

Darwin can install an unreported descriptor when receiving `SCM_RIGHTS` with a nil control pointer. Native C reproduces this kernel behavior. This raw boundary does not promise safe descriptor discard. The rights-transfer fixture supplies a sufficient control buffer and closes the returned descriptor.

## Local byte ownership controls

The `local-bytes`, `local-async` and `internet-async-capability` modes exercise the
std 2.0 byte-only contract. All must exit zero on both Darwin architectures.
The first queues a clean prefix followed by two messages with sixteen rights
apiece. It requires the exact clean prefix, a zero-length no-op, an actual EFAULT
peek, eight typed ancillary refusals and unchanged descriptor count. Closing the
stream must release all queued pipe writers, observed as pipe EOF. The async mode
requires an unsupported completion with zero bytes, then successful queued close
and pipe EOF. The internet backend mode refuses a local handle before claiming a
token or owner slot, retains EBADF for an invalid handle, and proves that the
refused caller-owned local handle remains usable.

These fixture processes may count their descriptors. Production never does.
The 12-byte control region holds one native header solely to detect ancillary
presence. It is not claimed to fit a rights payload. `layout.c` checks the native
header size/alignment and MSG_PEEK value without changing the existing layout
output. Existing raw adequate-buffer descriptor-transfer coverage remains intact.

A removed-peek control must fail an exact ownership/value assertion in these new
modes. Compile refusal, timeout or signal is not acceptance. The previously
retained nil/tiny/plain-read leak probes need not run again. Source review also
requires the consuming length to be the returned peek count, not the original
request. No claim is made that the original-length mutation necessarily crosses
a control-record boundary on XNU's current record traversal.
