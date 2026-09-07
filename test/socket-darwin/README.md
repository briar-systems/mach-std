# Darwin socket boundary probe

Run natively on both Darwin architectures with debug and release builds. Snapshot
the exact std manifest and source under this fixture's `dep/std`, then build the
Mach probe with the matching target, profile and explicit `-o bin/socket`.

Compile `layout.c` with the native SDK using C11 and warnings as errors. It checks
all fifteen public function signatures and retains a reference to every symbol.
Compare its output to `bin/socket layout` and inspect the C object's undefined
symbols against the Mach image's imports. This detects SDK aliases as well as
record size, alignment and field offsets.

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
