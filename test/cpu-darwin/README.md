# Darwin active CPU query probe

The native verifier uses checksum-verified published Mach4.30.0 on both Darwin architectures in debug and release. SDK C checks the exact sysctlbyname signature and LP64 widths. Native object imports and Mach's single libSystem dependency are retained.

Native C and Mach observe hw.activecpu around the ordinary wrapper and also record hw.ncpu. Those samples are observations, not an equality or mathematical bound on changes between calls. Each direct query must return a complete positive int. An invalid-name native C call establishes the actual failure value required from the direct Mach binding.

The verifier appends provider.mach only to its owned std snapshot and copies scripted.mach into the fixture only for instrumentation. It checks the exact hw.activecpu selector, pointer shape, int capacity and read-only request. It returns7 for the exact selector, tests zero/negative counts, short/long lengths and the largest positive int. Its failed-query case invokes the real native invalid-name query, then deliberately publishes a positive output with that failure result so the wrapper must honor the result guard independently. No scripted state is part of production.

Six source mutations produce eight runtime controls per profile. They alter selector, capacity, failed-result handling, output-length handling, nonpositive handling and result width. Every control must reach its exact child assertion. Native and scripted baselines are restored and rerun. Timeouts and compile failures never count as semantic evidence.

The production API reports the currently active processor count with its existing minimum-one policy. It does not promise per-process affinity limits, cache topology, a stable value over time or an error-reporting API.
