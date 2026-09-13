# Darwin ordinary entropy boundary probe

The native verifier uses the checksum-verified published Mach 4.30.0 compiler on both Darwin architectures in debug and release. SDK C signature, minimum-platform annotation and actual import spelling are checked before Mach execution. Native C errors establish the exact producer values required from the ordinary wrapper. Oversized native failure must leave its owned buffer unchanged.

Baseline smoke probes cover zero length and spans of 1,255,256,257,512 and1025 bytes with exact surrounding guards. They check actual native completion without treating random output as a deterministic oracle or asserting statistical quality. Existing crypto/rand tests run separately.

The verifier appends provider.mach only to its owned std snapshot and copies scripted.mach into the fixture source only for instrumentation. The public production declaration and loop have no scripted-provider state. The provider records exact destination addresses, chunk lengths and call counts while filling a known pattern. On its selected second call it invokes the real native getentropy with an oversized request. The test requires the actual native error, the completed256-byte prefix and an unchanged suffix. This proves the existing partial-prefix contract rather than adding rollback or secret-storage wiping.

Six independent mutations break the chunk limit, destination advancement, progress, last-byte completion, stop-on-failure and errno sign. Every mutation must reach its named runtime assertion. Source and fixture are restored exactly, and both restored native and scripted baselines run again. No timeout or compilation failure counts as a passing mutation.

The secret-shaped getentropy declaration and its stronger wipe-on-failure owner remain separate. This migration does not erase secret pointer types, change Linux/Windows, add a random generator or change the ordinary entropy source.
