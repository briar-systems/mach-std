# Darwin VM boundary probe

`verify.py` checks the darwin virtual memory boundary against the host SDK. Run it
on a native darwin host whose architecture matches the target, once per profile:

```sh
python3 test/vm-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/vm-darwin/verify.py <mach> darwin-aarch64 release
```

`test/lib/darwin_fixture.py` owns how a darwin fixture is built and run: std
resolves from the tree under test through `../..`, the C oracles build with the host
SDK, and a pass prints one JSON record with the compiler, the std commit and every
check result. Any failure or timeout exits nonzero with the failing check.
`test/lib/darwin-fixtures.py <mach> <target> <profile>` runs every fixture that owns
a `verify.py` and declares the target in its `mach.toml`. std CI
builds its compiler from `MACH_REF` in `.github/workflows/ci.yml`, and that is the
compiler to pass.

Before the Mach probe builds, `native.c` runs as the oracle:

- It statically checks the SDK signatures, LP64 widths and constants.
- Its `errors` and `access` results are recorded for comparison. Lock error probes
  use an owned mapping and SIZE_MAX minus one page as the length, so the requested
  end overflows and stays below the start after page rounding.
- `released` maps, protects and unmaps a page and requires protecting the released
  range to fail, which validates the release check the Mach `basic` mode relies on.
- `denied` writes to a read-only mapping after printing `fault-ready`. The signal it
  dies by is the host fault signal.

Then the Mach probe runs, each mode in its own process:

- `layout` equals the native widths, and every function `native.c` declares with
  `CHECK` is imported by the Mach image under the spelling the SDK binds.
- `errors` and `access` print exactly what `native.c` printed. The public API keeps
  nil on mapping failure and negative errno on integer-result failure.
- `basic` grows an allocation, checks its contents and requires protection of each
  released range to fail, rather than reading residency as mapping ownership.
- `heap` extends the heap region and checks its end, and `adapters` drives the page
  and bump allocators. Both exit zero and print nothing.
- `denied` prints `fault-ready` and dies by the same signal as `native.c`. Exiting,
  printing anything else or timing out is a failure.
- `mapping` gets a sparse file the verifier creates exclusively, with byte 0 set to
  A and byte 0x140000000 set to B. The probe rejects an invalid descriptor, an unaligned offset, offsets
  outside signed off_t and empty lengths, then maps the far offset, requires B,
  writes Z and syncs. The verifier then reads A at byte 0 and Z at the far offset,
  which catches a 32-bit offset truncation without gigabytes of resident memory.

`heap-refusal` and `heap-refused` are verification-only modes that pass only against
a std whose heap reservation or protection fails. The verifier does not run them.
