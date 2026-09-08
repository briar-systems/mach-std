# Public directory cursor proof

The native C fixture checks SDK signatures, offsets, length widths, descriptor
flags and the actual fdopendir failure contract. Compile its object separately
and inspect undefined symbols on each Darwin architecture before accepting the
Mach aliases. The nominal C name array is recorded, never treated as a maximum.
Compare field offsets and sufficient pointer alignment, not full struct sizes.

The Mach fixture checks non-directory refusal, unchanged original descriptor
flags, failed-initialization duplicate cleanup, actual held-root rename, relative
access through a borrowed name, stale errno before readdir EOF, and exact live
fd counts before and after ownership. Descriptor counts cover getdtablesize and
refuse unexpected fcntl errors. Run each selection in its own scratch directory.
Failures preserve the fixture directory for diagnosis.

Run `layout`, `errors` and `borrowed` with both native Darwin profiles, then the
portable inline `std.system.os.directory` and filesystem allocation/removal/
transaction regressions on all supported native hosts. The Windows inline
capacity provider intentionally supplies records longer than the local NTFS
component limit. It proves delivery of native variable records and documented
capacity status handling, not creation of such names on NTFS. The Linux inline
record test similarly separates ABI validation from filesystem creation limits.

Native build/test activation belongs to the root agent. This directory contains
fixture source only and makes no completed runtime claim.
