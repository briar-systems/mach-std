# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- manifest: Re-touched the self-manifest to RFC-exact totality per mach#1964/mach#1979.

## [0.18.0] - 2026-07-07

Overhauls the build manifest and test manifests to comply with the v2 build system schema.

### Changed
- manifest: Migrated self-manifest and test manifests to v2 schema (`[artifact.*]`).

## [0.17.0] - 2026-07-04

Harden no-libc `--pie` linux binaries with static-PIE self-relocation and fatal
`PT_GNU_RELRO` re-protection, add process-parallelism primitives, and grow a
unified JSON stack — streaming NDJSON emit, float parsing, and RFC 8259
escaping. Makes `[target.linux-arm64]` permanent behind a qemu CI lane, and
fixes the critical arm64 `--pie` startup crash and windows mixed-DLL link
correctness. Built with mach 2.14.1.

### Added

- chrono: `format_duration` — renders a `Duration` into a caller-supplied buffer
  as a human string (`0ms`, `<1ms`, `Nus`, `Nms`, `N.Ns`, `NmNs`; minutes is the
  top band, negatives carry a leading `-`), returning the null-terminated `str`
  aliasing the buffer or `nil` when capacity is short. A 24-byte buffer holds
  every i64 duration; ASCII-only, no allocation (mach#1774).
- format: `{:<N}` left-align spec flag — a `<` immediately after `:` writes the
  value then space-pads on the right; the zero flag is ignored for left-align.
  Right-align specs (`{:N}`, `{:0N}`, `{:08x}`) are byte-identical (mach#1774).
- runtime/linux: static-PIE self-relocation — a no-libc `mach build --pie` image
  applies its own ELF `R_*_RELATIVE` relocations before `main`. `_rt_relocate`
  recovers the load bias from the kernel auxv (`AT_PHDR` vs the link-time
  `PT_PHDR`) and slides every `.rela.dyn` entry; it is position-independent by
  construction, runs from `_rt_init`, and is gated on `$mach.build.pie` so a
  non-PIE build links none of it (mach#1727).
- runtime/linux: `PT_GNU_RELRO` re-protection — after applying the RELATIVE
  relocations, `_rt_relocate` `mprotect`s the linker's `PT_GNU_RELRO` region
  (relocated constants in `.rodata`, mapped writable for self-relocation) back to
  `PROT_READ`, so those constants are read-only before `main`. Page-exact and
  reloc-independent: it captures `AT_PAGESZ`, gates on the region being a whole
  number of runtime pages, and skips (leaving it writable) on a kernel page
  larger than the image's 4 KiB segment alignment (mach#1778).
- process: `exec.spawn_redirected` — spawn without waiting, with stdout and/or
  stderr bound to caller-supplied descriptors (stdin stays inherited); and
  `exec.wait_any` — block until any child exits, returning the reaped child's
  handle. POSIX `wait(-1)` semantics on every platform (the windows layer
  multi-waits across its tracked child handles) (#331).
- system: `os.cpu_count` — the number of CPUs available to the process; linux
  popcounts the `sched_getaffinity` mask (honouring taskset/cgroup cpusets),
  darwin reads `hw.ncpu` via `__sysctl`, windows uses
  `GetActiveProcessorCount(ALL_PROCESSOR_GROUPS)`. Never less than 1 (#331).
- data/json: streaming NDJSON emitter — `Object`/`Array` with `object_begin`/
  `object_end`, the nesting primitives `object_end_value`/`field_object_begin`/
  `field_array_begin`/`array_end`/`array_object_begin`, and the members
  `field_str`/`field_str_or_null`/`field_null`/`field_i64`/`field_bool` write
  one-object-per-line JSON (objects nest onto a single line) through a
  caller-owned `io.Writer`, plus `write_json_string` for a lone escaped string
  literal. `mach.cli.json` moves into std as the one JSON emission home; the
  tree `emit` and the streaming surface now share a single escape core
  (`escape_unit`) with an explicit policy: `ESCAPE_VERBATIM` (structural, UTF-8
  verbatim) for `emit`, and `ESCAPE_ENSURE_ASCII` (RFC 3629 decode to `\uXXXX`,
  astral surrogate pairs, U+FFFD on invalid input) for the stream. Both surfaces
  are byte-identical to their pre-unification output (#338).
- data/json: float number parsing — numbers now accept the full RFC 8259 grammar
  (`int frac? exp?`); a number carrying a fraction or exponent parses as a float
  (correctly rounded through `std.text.parse`'s bignum decimal→f64 machinery over
  the zero-copy source span), while integer-looking numbers still yield an `i64`
  on the byte-identical path. `Value` gains `value_is_float` and `value_float`
  (an integer widens to `f64`); `value_number` is unchanged, and `emit` writes
  floats in shortest round-trippable form (#349).
- data/json: `value_string_decode(v, buf, len) -> Result[usize, str]` — resolves a
  string value's raw on-wire escapes into logical bytes in a caller buffer, the
  inverse of the emit escaper. Handles `\" \\ \/ \b \f \n \r \t` and `\uXXXX` (a
  high+low surrogate pair combines into one astral code point via the validated
  `std.text.utf8` encoder), and errors on malformed escapes. The parser keeps its
  zero-copy raw-bytes representation; decoding is paid only at the consumption
  point, resolving the parse-vs-emit representation asymmetry (#340).
- build/ci: a permanent `[target.linux-arm64]` (aarch64/linux/aapcs64) makes std
  cross-buildable to aarch64 out of the box, and a `cross-arm64` CI lane
  cross-builds the unit suite and runs it under `qemu-aarch64` for an automatic
  aarch64 regression signal over the full suite (#280).

### Fixed

- runtime/linux: RELRO re-protection is now fatal on any failure. `_rt_relocate`'s
  `PT_GNU_RELRO` re-protection was best-effort — it skipped a region not congruent
  with the runtime page and ignored the `mprotect` result. Now that the ELF writer
  aligns every segment to the target's max page (≥ any supported kernel page,
  mach#1845), the region is always a whole number of runtime pages, so an absent
  `AT_PAGESZ`, a congruence mismatch, or a failed `mprotect` is a broken
  environment or a violated layout contract. The extracted `relro_reprotect`
  panics naming the violated invariant in each case — the glibc stance, matching
  `os.page_size`'s `AT_PAGESZ` precedent (#336) — so a `--pie` binary either runs
  fully hardened or dies loudly; no silent-unhardened path remains (#347).
- runtime/linux: `_rt_relocate` now re-protects the RELRO segment's actual mapped
  extent — taken from its backing `PT_LOAD` and rounded up to `AT_PAGESZ` — rather
  than the ELF writer's page-padded `p_memsz`. On a 4 KiB-page aarch64 kernel the
  padded `PT_GNU_RELRO` `p_memsz` (64 KiB, mach#1845) spanned an unmapped gap, so
  the `mprotect` failed with `ENOMEM` and, being fatal (#347), crashed every
  `--pie` binary at startup. Std half of the arm64 startup fix (mach#1885).
- system: `os.page_size` on linux now returns the runtime `AT_PAGESZ` the
  entrypoint captures from the auxiliary vector at startup, instead of a
  hardcoded 4096 — correct on aarch64 kernels configured for 16 KiB or 64 KiB
  pages. The runtime publishes the auxv page size into the OS layer
  (`capture_pagesz`) right after `_envp`, post-relocation, giving page_size() one
  source of truth; `std.runtime.linux.reloc` keeps its own pre-relocation read
  for the RELRO mprotect. `AT_PAGESZ` is mandatory on linux, so page_size()
  panics when it is unavailable rather than fabricating a default (#336).
- data/json: `emit` now escapes string values and object keys per RFC 8259 —
  `"` → `\"`, `\` → `\\`, control bytes (0x00–0x1F) via the short escapes
  `\b \t \n \f \r` or else `\u00xx`, all other bytes (including valid UTF-8)
  verbatim. Values or keys holding a quote, backslash, or control byte previously
  emitted invalid JSON (#337).
- system/os/windows: every `ext fun` (61 kernel32 imports plus the windows
  runtime entrypoint) now carries an explicit `#[library]` decorator naming its
  providing DLL. The unattributed imports previously relied on the COFF fallback
  binding them to dependency 0 — correct only while `kernel32.dll` sorted first —
  so the first mixed-DLL link (e.g. also linking `glfw3.dll`) mis-bound whole DLL
  sets and hit `STATUS_ENTRYPOINT_NOT_FOUND` at load. Purely additive (#334).

## [0.16.2] - 2026-06-28

Enter aarch64 darwin executables through the `LC_MAIN` register convention and
correct three darwin syscall numbers, so arm64-darwin binaries run. Built with
mach 2.9.0.

### Fixed

- runtime/darwin: enter the aarch64 `_start` through the PIE `LC_MAIN` register
  convention — capture argc/argv/envp from x0/x1/x2 as dyld hands them, instead
  of reading them off the stack. darwin arm64 executables are `LC_MAIN` images
  (#324).
- os/darwin: correct the `mkdirat` (475), `unlinkat` (472), and `faccessat`
  (466) syscall numbers; the prior 464/466/468 were wrong (464 is
  `openat_nocancel`), so directory and path operations hit the wrong trap once
  arm64-darwin binaries actually ran (#324).

## [0.16.1] - 2026-06-28

Rewrite the aarch64 darwin `_start` entry in mach's inline-asm dialect so
aarch64-darwin links. Built with mach 2.9.0.

### Fixed

- runtime/darwin: rewrite the aarch64 `_start` in mach's inline-asm dialect —
  bare immediates, an explicit `lsl`+`add` for the envp scale, and no explicit
  stack realignment (sp is 16-byte aligned on kernel entry). The prior standard
  ARM syntax used `#`-prefixed immediates (mach's comment char), a 4-operand
  shifted-register add, and a bitmask-immediate `and`, all of which mach's
  dialect rejects — so darwin-aarch64 could not link. Semantics are preserved
  (#320).

## [0.16.0] - 2026-06-28

Add a riscv64-linux target — runtime entry, syscall layer, and atomics — with a
qemu-backed CI lane, and fix the darwin entry so the darwin cross-build links and
encodes. Built with mach 2.9.0.

### Added

- runtime: riscv64-linux `_start` entry plus the linux syscall stubs and os
  module for riscv64 (#306).
- sync/atomic: riscv64 atomic arms built on the A extension (`.aqrl` AMOs,
  `lr.d`/`sc.d`, and FENCE barriers) (#308).
- ci: a cross-riscv64 qemu lane that exercises the riscv64-linux runtime end to
  end.

### Fixed

- runtime/darwin: export `_rt_argc` / `_rt_argv` / `_rt_envp` with `#[symbol]` so
  the darwin entry links instead of failing with `undefined symbol: _rt_argc`
  (#314).
- os/darwin: load the aarch64 syscall number and arguments with `ldr` instead of
  `mov`, which rejected the slot-bound operands at encode time (#315).
- doc: rework the linux `page_size` docstring so it no longer trips the doclint
  'documented component' warning (#310).

## [0.15.0] - 2026-06-25

Expose the FNV-1a seed as a `pub val FNV_INIT` constant and publish the offset
and prime, replacing the `init()` accessor. The compiler's type interners fold
from the constant seed directly. Built with mach 2.5.9.

### Changed

- crypto/hash: `fnv1a` exposes `pub val FNV_INIT` (and `pub` `FNV_OFFSET` /
  `FNV_PRIME`) instead of `pub fun init()`. Callers fold from the constant seed
  rather than a function that returned it (#1600 on briar-systems/mach).

### Removed

- crypto/hash: `fnv1a.init()` is removed in favour of `FNV_INIT` (breaking; no
  in-tree consumers).

## [0.14.1] - 2026-06-23

Restore linear-time `str_region_equals`, eliminating a whole-source scan that
made the compiler's parser quadratic and stalled stdlib-heavy front-end builds.
Built with mach 2.5.2.

### Fixed

- string: `str_region_equals` no longer calls `str_len` over the entire source
  buffer to bounds-check. The parser's keyword matcher (`at_kw`) calls it per
  keyword probe per token, so the whole-source scan made parsing O(file²) and
  caused multi-second pauses during the front-end of large builds. The scan is
  now bounded to the compared region with a NUL-terminator guard, restoring
  linear-time comparison (#301).

## [0.14.0] - 2026-06-19

Migrate all decorator syntax from backtick form to `#[attr]`. Built with mach 2.3.0.

### Changed

- all: migrate decorators to `#[attr]` syntax (`symbol`, `library`) across runtime
  entrypoints and system OS bindings.

## [0.13.0] - 2026-06-19

Process spawning no longer copies the parent's address space, so `mach test`
and other fork-heavy programs stay robust on swapless `vm.overcommit_memory=0`
hosts. Built with the mach 2.0.1 compiler.

### Fixed

- os: `spawn`/`spawn_redirected` (linux) now `clone(CLONE_VM|CLONE_VFORK|
  SIGCHLD)` the child onto a private stack and a pinned trampoline instead of
  `fork()`. Sharing the address space skips fork's copy-on-write commit
  accounting, so spawn no longer fails with `ENOMEM` on a swapless
  `vm.overcommit_memory=0` host (e.g. GitHub runners), and the fix benefits
  every fork-heavy mach program. Verified on x86_64 and aarch64 (mach#1487).

### Changed

- allocator: the generic `deallocate[T]` now returns `Result[bool, str]` —
  ok(true) on success (including the nil-pointer / count == 0 no-op), err on a
  non-zero status — aligning it with `allocate`/`reallocate`. `deallocate_raw`
  stays the raw i64 primitive; callers that inspected the status were updated
  (#291).

### Documented

- format: documented that `f32` widens to `f64` and prints as that value (no
  f32-specific shortest round-trip), with added tests for f32 widening, the
  smaller integer widths (i8/i16/i32, u16/u32), and negative signed hex (#293).

## [0.12.0] - 2026-06-19

The v1.7 collapse — every legacy comptime spelling is gone, replaced by the
new-only forms. Built with the mach v1.7.0 compiler.

### Changed

- comptime: migrated to the provenance-rooted build namespace — every
  `$mach.target.{os,arch,pointer_width}` read is now `$mach.build.*` (#283).

### Removed

- the legacy `$<sym>.symbol` / `$<sym>.library` setter directives, replaced by
  leading backtick `` `symbol("…")` `` / `` `library("…")` `` decorators (the
  `mach.toml [os.*] libs` link set is unchanged; the decorator only routes to it)
  (#283).

## [0.11.0] - 2026-06-19

Format and print are rebuilt on the v1.7 comptime variadic packs, which also
**re-enables variadic formatting on aarch64-linux** — the C-style `va_list`
machinery and its arch gates are gone, so `format`/`print` work on every target.
Float support is now complete: correctly-rounded parsing *and* shortest
round-trippable formatting. Built with the mach v1.7.0 compiler.

### Added

- format: `write_f64` — correctly-rounded shortest float formatting (dragon4),
  and a `{}` hole on an `f64` (#282).
- text: correctly-rounded `parse_f64` (round-trippable) via exact `std.math.bignum`
  (a fixed 128-limb big-int) (#287, #288).

### Changed

- format/print rewritten onto comptime variadic packs — `vformat`/`format`/
  `printf`/`eprintf`/`printlnf`/`eprintlnf` take a `va: ...` pack consumed by
  `$each` + `$type_of` dispatch, monomorphized per call. `{}` is type-directed
  (integers decimal; `str`, `ptr`, `f64`), with `{:c}` (byte→char), `{:x}`/`{:X}`
  hex, width and `0`-padding, and `{{`/`}}` escapes. Writes are `Result`-threaded,
  the returned count is the true bytes written, and hole/arg-count mismatches
  error both ways (`ERR_FEW_HOLES`/`ERR_MANY_HOLES`) (#282).
- **aarch64-linux variadic formatting re-enabled** — `format`/`print` are no
  longer arch-gated; they work on aarch64 under AAPCS64 (resolves #276) (#282).

### Removed

- the C-style `va_arg`/`va_start`/`va_list` machinery, replaced by comptime packs
  (#282).

## [0.10.0] - 2026-06-13

Filesystem symlink and recursive-removal primitives, giving the compiler's
dep machinery `symlink`/`remove_all` to replace its `ln -s`/`rm -rf`
shell-outs (cross-platform, including native windows).

### Added

- `std.filesystem.symlink(target, linkpath)` creates a symbolic link
  (`symlink(2)` on posix, `CreateSymbolicLinkA` on windows). Relative targets
  are preserved verbatim so links keep resolving after their containing tree
  is moved. The windows path requests unprivileged creation and reports a
  privilege refusal as "operation not permitted". This gives the compiler's
  dep machinery a primitive to replace its `ln -s` shell-out (#257).
- `std.filesystem.remove_all(a, path)` removes a file, directory, or symbolic
  link recursively, depth-first. Symbolic links are removed as links and never
  followed, so a link pointing outside the tree leaves its target untouched;
  removing a missing path succeeds. Replaces the dep machinery's `rm -rf`
  shell-out (#257).
- `std.filesystem.info_link(p)` is the `lstat` counterpart of `info_path`,
  reporting a symbolic link's own metadata without following it.
- `std.system.os.symlink(target, linkpath)` wires the new OS primitive through
  the linux, darwin, and windows layers.

## [0.9.0] - 2026-06-13

Native-windows temp-file support: the temp directory is resolved per-OS at
use time (GetTempPathA on windows, $TMPDIR with /tmp fallback on posix). With v0.8.0's
loader fixes this completes the std side of the compiler's native windows
CI lane (briar-systems/mach#1351); the exec-fixture half of #258 was already
fixed in v0.7.0's OS-gated tests and ships via the pin bump.

### Added

- `std.system.os.temp_dir(buf, cap)` resolves the OS temporary directory at
  use time under the `env.get` truncation contract. Lookup order is per-OS:
  posix consults `$TMPDIR` and falls back to `/tmp`; windows uses
  `GetTempPathA` (`TMP` → `TEMP` → `USERPROFILE` → the windows directory).
  `std.types.path.is_separator` is now public.

### Fixed

- `std.filesystem.temp_create` no longer hardcodes `/tmp`, which does not
  exist on native windows; it resolves the temp directory per call via
  `os.temp_dir`, fixing temp-file creation (and everything routed through it)
  on windows while preserving posix behavior (#258).

## [0.8.0] - 2026-06-12

Native-windows loader compliance: the wait-on-address family is pinned to its
real apiset DLL (mach exes previously failed to load on real windows), and the
path module understands drive-letter and UNC absolute roots. Unblocks the
compiler's native windows CI lane.

### Added

- `std.types.path` now recognizes windows absolute roots: drive-letter
  roots (`C:\`, `C:/`) and UNC roots (`\\server\share`) are absolute, and
  `is_root`/`filename`/`extension`/`stem`/`parent` never split inside them
  (`parent("C:\foo")` → `C:\`, `parent("\\server\share\foo")` →
  `\\server\share`, each root being its own parent). A bare drive reference
  `C:` is drive-relative — a root unit but not absolute, matching Win32.
  POSIX behavior is unchanged (#248).

### Fixed

- Windows `WaitOnAddress`/`WakeByAddressSingle` are now pinned to
  `api-ms-win-core-synch-l1-2-0.dll` (added to `[os.windows] libs`). Real
  windows' kernel32 does not export the wait-on-address family — only wine's
  does — so the unpinned imports bound to kernel32 and the native loader
  rejected every mach exe with `STATUS_ENTRYPOINT_NOT_FOUND` before main
  (#253).

## [0.7.0] - 2026-06-12

Windows-stabilization release: native process spawning (CreateProcess backend
with stdio redirection and capture), correct per-DLL import attribution
(ws2_32/advapi32), dual-separator path parsing, RFC 6761 localhost resolution,
and darwin fork/vfork child-indicator fixes. Requires mach v1.5.0 (per-symbol
DLL attribution).

### Added

- `std.process.exec.capture(pathname, argv, envp, buf, cap) Result[Capture, str]`
  — run a child and collect its stdout into `buf`, draining the pipe to EOF so a
  child outproducing the buffer never blocks; always reports the full output
  length, so `len > cap` signals truncation (raw bytes, no terminator slot — a
  `len == cap` capture is complete, unlike `env.get` whose boundary is
  `ret >= cap`). Backed by a new `std.system.os.spawn_redirected(pathname,
  argv, envp, stdin_fd, stdout_fd, stderr_fd)` stdio-redirection primitive
  (fork + per-stream dup2 + exec, -1 inheriting the parent's stream; child
  exits 126 on redirect failure, 127 on exec failure) on linux and darwin,
  onto which `spawn` now collapses (#188, capture half).
- Native windows exec backend: `spawn`/`spawn_redirected`/`run`/`capture`
  over `CreateProcessA` + `WaitForSingleObject` + `GetExitCodeProcess`, with
  argv joined per the windows command-line quoting rules (a joined line over
  the 32 KiB limit fails with `E2BIG` instead of truncating), `envp` mapped
  to a CreateProcess environment block (nil inherits), and stdio redirection
  via `STARTF_USESTDHANDLES` with inheritance scoped to exactly the child's
  std handles through `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` (inherit flags are
  restored after the spawn, so concurrent spawns cannot leak pipe ends into
  unrelated children; a spawn with no redirection inherits the parent's
  streams natively). The read path treats a broken anonymous pipe as EOF so
  `capture` drains cleanly. `environ()` is now populated from
  `GetEnvironmentStrings` (hidden `=X:` drive-cwd entries excluded) rather
  than always nil (#221, #188 windows half). `os.WNOHANG` is now forwarded
  portably alongside `wait`/`wait_pid`.
- `std.system.os.windows.running_under_wine() bool` — detect the wine
  compatibility layer by probing ntdll for the wine-only `wine_get_version`
  export. The two `std.sync.thread` spawn/join tests use it to skip under
  wine, whose kernel32 lacks the `WaitOnAddress`/`WakeByAddressSingle`
  exports that real windows 8+ provides; the thread sync code is unchanged
  and correct on real windows (#244).

### Fixed

- Windows DLL import attribution: the winsock bindings (`WSAStartup`,
  `WSAGetLastError`, `socket`/`bind`/`listen`/`accept`/`connect`/`sendto`/
  `recvfrom`/`shutdown`/`setsockopt`/`send`/`recv`, `closesocket`) now import
  from `ws2_32.dll` and `SystemFunction036` (RtlGenRandom) from `advapi32.dll`
  via the compiler's per-symbol `$<sym>.library` attribution, instead of every
  import collapsing onto `kernel32.dll` and aborting at call time. `ws2_32.dll`
  and `advapi32.dll` are added to the windows link libraries, and the `SleepW`
  binding is renamed to its real export `Sleep` (#235, #241).
- `std.net.dns.resolve` now resolves `localhost` and any `.localhost`
  subdomain to `127.0.0.1` per RFC 6761, without consulting the hosts file or
  a nameserver, so loopback resolution is portable on platforms (e.g. windows)
  whose hosts file ships localhost commented out; `lookup_hosts` stays a pure
  hosts-file reader (#242).
- darwin `fork()` now reads the XNU child-indicator register (rdx on
  x86_64, x1 on aarch64) and returns 0 in the child instead of the child
  PID, so `spawn`/`spawn_redirected` take the exec path in the child rather
  than duplicating the parent program (#232).
- darwin `vfork()` reads the same XNU child-indicator register as `fork()` and
  returns 0 in the child instead of the child PID, fixing the identical
  child-indicator bug in the previously plain `syscall0` wrapper (#234).
- windows `spawn`/`spawn_redirected` now reserve a process-table slot before
  `CreateProcessA`, so an exhausted table fails with `EAGAIN` without launching
  a child that could never be waited on; a `WAIT_FAILED` in `wait`/`wait_pid`
  now purges the dead handle (best-effort close + slot freed) instead of
  leaking the slot — the wait-any path probes each snapshot handle, purges the
  unwaitable ones, and retries the multi-wait once so one poisoned handle
  cannot block reaping of healthy children (#238).
- `std.types.path` parsing (`is_abs`/`is_root`/`filename`/`extension`/`stem`/
  `parent` and `join`'s separator-already-present check) now accepts both `/`
  and `\` as component separators on windows, matching the Win32 file APIs,
  while construction still emits the platform separator and `parent` preserves
  the input's leading separator for root results; posix is unchanged (`\`
  stays a legal filename byte). Fixes 7 `/`-form path tests under windows
  (#243).

## [0.6.0] - 2026-06-12

Bug-clearing release: all three known-failing tests are fixed for real (thread
clone race, json key lookup, env PATH harness dependency), and the environment
vector is now accessible. The thread fix required a breaking `spawn` signature
change, hence the minor bump.

### Added

- `std.process.env.environ() **u8` — the captured environment vector (`_envp`),
  forwarded through every OS layer next to `getenv`; documented always-nil on
  windows until a windows environment-block reader exists (#188, accessor half).
- `std.data.json.value_key_len(v, index) usize` — byte length of an object key,
  parallel to `value_key` (#196).

### Changed

- **BREAKING**: `std.sync.thread.spawn(f: fun()) Thread` is now
  `spawn(f: fun(), t: *Thread)`. The handle is caller-owned and initialized in
  place: the child thread writes its completion flag through the handle, so the
  record must live at a stable address for the thread's lifetime — a by-value
  return handed the child the address of a dead frame and made `join` wait
  forever (#195).
- json object keys keep their byte lengths (`keys_len` parallel array);
  `value_find` compares length-bounded and key emission uses the stored length
  instead of assuming null termination. `value_key` is documented as
  non-null-terminated (#196).
- the `env: get PATH` test is harness-independent: it asserts termination and
  repeatability when PATH is inherited instead of requiring an inherited
  environment the test harness does not currently provide (#197).

### Fixed

- thread spawn/join no longer deadlocks: parent/child discrimination after
  `clone` happens entirely in registers (the child jumps straight to the
  trampoline), eliminating the shared-stack-slot race under `CLONE_VM` (#195).
- `json.value_find` matches keys again — lookups previously failed for every
  key because non-terminated key slices were compared null-terminated (#196).

## [0.5.0] - 2026-06-12

Manifest migrated to the v1.4.0 format and windows link requirements declared
once via the os overlay, plus the memory/string primitives added since 0.4.2.

### Added

- `std.memory.raw_equal(a, b: ptr, n: usize) bool` — allocation-free byte-wise memory
  comparison with documented nil contract (n==0 vacuously true; equal pointers trivially
  true; one-sided nil with n>0 is false) (#204).
- `std.memory.equal[T](a, b: *T, n: usize) bool` — typed wrapper over `raw_equal` (#204).
- `std.types.string.view_index_char(v: StrView, c: char) Result[usize, str]` — first
  occurrence of a character within a view (#204).
- `std.types.string.view_contains_char(v: StrView, c: char) bool` — membership test
  delegating to `view_index_char` (#204).
- `[os.windows] libs = ["kernel32.dll"]` os overlay — std's windows runtime link
  requirement, declared once and cascaded to every windows consumer build via the
  v1.4.0 manifest os-component overlay.

### Changed

- `mach.toml` converted to the v1.4.0 manifest schema: `dir_src`/`dir_out`/`dir_dep`
  become `src`/`dep` plus explicit `out`/`obj`/`ir`/`asm`/`tests` path templates;
  `[targets.linux]` becomes `[target.linux]`; the library `mode = "library"` /
  `entrypoint = "lib.mach"` pair becomes `[lib.std] entry = "lib.mach" kind = "static"`.
  v1.4.0 reads only this format.
- `data/toml`: internal `str_eq_n` removed; call site migrated to `memory.raw_equal`
  (behavioral match: both are byte-wise n-byte comparisons over `str = *char = *u8`) (#204).

## [0.4.3] - 2026-06-11

Patch release: process exit now terminates all threads on linux.

### Fixed

- `_start` (linux x86_64) and the linux OS-layer process-exit paths
  (`terminate`, backing `process.exec.exit`/`abort`/panic, and the spawn
  child's exec-failure exit) used `SYS_exit`, which ends only the calling
  thread — any program with a live non-main thread hung after `main`
  returned. All process exits now use `SYS_exit_group`; thread exits keep
  `SYS_exit`. darwin (`exit` ends the whole task) and windows
  (`ExitProcess`) were already correct (#205).

## [0.4.2] - 2026-06-10

Patch release: SysV stack-alignment fix in the program entrypoint.

### Fixed

- `_start` (linux and darwin x86_64) entered every callee with an 8-byte
  misaligned stack, violating the SysV call invariant — invisible to pure-Mach
  programs but a SIGSEGV for any C callee using aligned SSE accesses (#200).

## [0.4.1] - 2026-06-10

First tagged release carrying the 0.3.0 and 0.4.0 work (neither was tagged);
`main` advances from 0.2.5 straight to 0.4.1.

### Fixed
- Corrected the expected length in the `ip: ipv4_format` test — a single-octet
  address such as `127.0.0.1` formats to 9 bytes, not 7. The function was
  correct; only the test assertion was wrong.

### Known Issues
These tests fail or hang under `mach test` and are tracked for follow-up. All
three are gaps in modules added during the 0.4.x rework (after 0.2.5), not
regressions:
- `thread: spawn and join` / `thread: is_done after join` deadlock — the clone
  parent/child discrimination is a shared-memory race ([#195](https://github.com/briar-systems/mach-std/issues/195)).
- `json: value_find on object` never matches — object keys are stored as
  non-null-terminated source slices but compared with `str_equals` ([#196](https://github.com/briar-systems/mach-std/issues/196)).
- `env: get PATH returns positive length` — the std code is correct; `mach test`
  execs the test binary with an empty environment ([#197](https://github.com/briar-systems/mach-std/issues/197)).

## [0.4.0] - 2026-03-10

### Added
- Multi-target OS layer with darwin (x86_64, aarch64) and windows (x86_64) backends
- Socket primitives in the OS layer (sock_create, sock_bind, sock_listen, sock_accept, sock_connect, sock_sendto, sock_recvfrom, sock_shutdown, sock_setopt)
- OS-level random_fill primitive (getrandom on linux, getentropy on darwin, RtlGenRandom on windows)
- Thread primitives for darwin (bsdthread_create, ulock) and windows (CreateThread, WaitOnAddress)
- aarch64 atomic backend (ldaxr/stlxr)
- New modules: chrono, encoding (hex, base64), format, io (buffer, reader, writer), log, math, process (args, env, exec), rand (xoshiro256**)
- New collection types: bitset, deque, heap, set, sort
- Page allocator, char type, utf8 module, json parser, crypto/hash (sha256, sha512)
- Platform-specific runtime modules for linux, darwin, and windows

### Changed
- Restructured OS layer: extracted constants into per-ISA files, added shared.mach for cross-platform values, proper forwarding chains through ISA → OS → os.mach
- Removed non-portable symbols from os.mach surface (syscall wrappers, CLOCK_*, wait flags, EINTR_MAX_RETRIES, huge page sizes)
- Rewrote crypto/rand to use os.random_fill — eliminated OS-specific backend
- Rewrote net/tcp, net/udp, net/dns to use OS layer socket primitives — eliminated OS-specific backends
- Eliminated thread globals on all platforms (stack-based parameter passing on linux, lpParameter on windows)
- Updated core types, allocator, collections, memory, print, and filesystem modules

### Removed
- Legacy platform/ abstraction layer (replaced by system/os/)
- Superseded modules: fmt, stream, time, text/ascii, text/builder, text/buffer_writer, types/int, io/bytebuf

## [0.3.0] - 2025-11-18

### Added
- `std.collections` with new `Slice` type for safer array/slice handling
- Added `std.os` and `std.arch` modules and implementations for platform/architecture detection
- Introduced readonly pointers.

### Changed
- Complete rework of most modules to be up to date with latest Mach language features including readonly pointers, the removal of slices, and the new native `str` type.
- Complete rework of the fundamental structure of the standard library.
- Too many to reasonably count.

### Fixed
- Several bugs across all modules.

## [0.2.5] - 2025-11-17

### Fixed
- Corrected import and syntax errors in `semver.mach`
- Fixed `Path` cloning function to properly initialize `Path` struct from cloned `String`
  - NOTE: This fix addresses an issue where the previous implementation *correctly* cast a `String` to a `Path`. `Path` is an alias for `String`, so this should be allowed, but was causing sema errors. Patch for now.

## [0.2.4] - 2025-11-17

### Added
- Added `Semver` type and parsing functions in `src/types/semver.mach`

## [0.2.3] - 2025-11-17

### Changed
- Removed `list_new` function in favor of direct `List` initialization with error handling via `Option`.

## [0.2.2] - 2025-11-17

### Changed
- Migrated the dedicated compiler modules into the main `mach` repository for separation of concerns.

### Fixed
- Stabilized `List` initialization and deallocation to avoid dangling state during collection reuse.

## [0.2.1] - 2025-11-15

### Fixed
- Updated OS conditional checks to use '$mach.build.target.os' for platform-specific imports

## [0.2.0] - 2025-11-15

### Changed
- Moved runtime logic to new system/runtime.mach file and updated imports accordingly

## [0.1.1] - 2025-11-15

### Fixed
- Removed unnecessary dereference operator in realtime_timespec function for windows
- Added missing import for std.types.size and updated function signature for get_system_time_as_file_time for windows
- Standardized import formatting and added missing syscall constants for darwin

## [0.1.0] - 2025-11-15

### Added
- Initial release of mach-std as a standalone standard library
- Core type system with List, Option, Result, and String types
- Platform-specific runtime support for Linux, Darwin, and Windows
- System modules including memory management, time, and environment handling
- I/O modules for console, filesystem, and path operations
- Text processing utilities (ASCII, parsing)
- Data serialization support (JSON, TOML)
- Cryptographic hashing functionality
- Language tooling modules (lexer, parser, AST, compiler driver)
- Cross-platform system call abstractions
- Memory manipulation functions (memset, memcpy)
- Runtime entry points and panic mechanisms for all supported platforms

### Changed
- Migrated from main mach repository to dedicated mach-std repository
- Standardized string type usage to `String` across the codebase
- Refactored function naming for consistency (e.g., `length` to `len`)
- Updated to use instance method syntax for string formatting
- Improved error handling patterns with Result and Option types
- Enhanced platform-specific implementations for better consistency

### Fixed
- String handling in format functions with proper pointer dereferencing
- Environment variable retrieval to use direct file reading on Linux
- UTF-16 to UTF-8 conversion for Windows argument handling
- Conditional compilation directives for platform-specific code
