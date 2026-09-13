# Darwin VM boundary probe

The native verifier builds this fixture with the checksum-verified published Mach 4.30.0 compiler on both Darwin architectures in debug and release. A local dep/std snapshot supplies the exact candidate source.

Before Mach execution, native.c checks SDK signatures, LP64 widths, constants and actual public import spellings. Its real error results and valid lock/advice results must match Mach exactly. Lock error probes use an owned mapping and SIZE_MAX minus one page as the length. The requested end overflows and remains below the start after page rounding. A separate native map/protect/unmap/protect sequence validates the release oracle before Mach execution. The Mach reallocation test checks that protection of each released range fails, rather than interpreting residency as mapping ownership. Its write to a read-only mapping establishes the host fault signal used by the Mach protection probe. Both children must first print the readiness marker. No timeout counts as a protection fault.

The mapping mode requires an exclusively owned sparse file supplied by the verifier. Byte0 is A and byte0x140000000 is B. The probe maps the latter offset, requires B, writes Z and syncs. The host independently checks the old byte and mapped byte. This catches accidental 32-bit offset truncation without allocating gigabytes of resident memory.

Each heap test runs in its own process. Preparation-time native failure controls verify that failed reservation publishes no base and failed protection publishes no extended end. They inject native results only in verification source, never in production. The existing mapping and allocator guard tests run against the baseline snapshot separately.

The public API retains nil on mapping failure and negative errno on integer-result failure. mmap uses MAP_FAILED, not nil or a broad signed-address check. Mapping offsets outside signed off_t are rejected before conversion. No allocator, heap reservation size, mapping ownership or concurrency contract changes.
