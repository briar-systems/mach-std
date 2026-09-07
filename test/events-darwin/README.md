# Darwin completion boundary

This focused fixture uses the published Mach 4.30 compiler in debug and release
on both Darwin architectures. It changes no public completion API.

The SDK C gate checks public kqueue/kevent signatures, constants and native
kevent/timespec layout. Mach's pointer-only Kevent storage has the same 32-byte
extent, stride and field offsets as native struct kevent. Its alignment is
stronger than Apple's packed four-byte alignment. The verifier checks sufficient
alignment rather than claiming equal alignment or a compatible by-value ABI.
The compiler also checks that owned IoCompletion output storage accommodates it.

The native fixture covers simultaneous read/write readiness, distinct contexts,
one-shot consumption, rearming, filter deletion, EOF, wake, zero-count polling,
CLOEXEC and descriptor cleanup. A host acknowledgement releases a worker that
wakes an indefinite queue poll. The outcome must be valid regardless of which thread reaches the kernel first.
This handshake does not prove that both scheduling interleavings occurred. No sleep is an oracle.
Closed-queue errors match an independent C producer and leave output unchanged.
Nil and oversized-capacity rejection are checked separately.

The verifier appends provider.mach only to its private backend snapshot and adds
scripted.mach only to its private fixture source. Creation controls use actual
native EBADF producers after each acquisition stage. Cleanup deliberately changes
errno after closing to prove the primary error was already captured. Descriptor
counts and the unpublished queue state are checked independently. Scripted event
records prove full-width contexts and counts, signed error translation, EOF,
filter flags, exact timeout conversion and unchanged output on zero progress.
These are explicit result-boundary controls, not invented kernel observations.

Independent source controls must fail at their named runtime assertions. Exact
source and baseline/native/scripted executable hashes are retained after restore.
Existing Darwin async tests exercise callers after the focused fixture.

The Linux and Windows nil wake/close discrepancy is recorded for the portable
completion contract under #618. This fixture and migration own Darwin only.
