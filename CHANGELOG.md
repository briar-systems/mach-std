# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [7.0.0] - 2026-09-19

std 7.0.0 keeps `mach = "^5.8"`; nothing in it needs 5.9. Two things are
silent to the compiler and need a rebuild or a reading rather than a fix at
the call site:

- `data.toml.Value` grew by two `Span`s. Anything that links std and stores a
  `Value` or a `Table` across the boundary must be rebuilt against 7.0.0.
- `io.runtime.make` keeps a copy of the allocator it is handed, so that
  allocator's context must outlive the runtime. A stack-local allocator that
  goes out of scope before `io.runtime.destroy` is a use after free, not a
  refusal.

The one changed signature, `io.runtime.make(runtime, a, initial)`, is a
compile-time refusal at the caller, so a program that builds against 7.0.0
has already moved. Three changes can newly fail or differ at run time in code
that already compiles:

- A refusal from the runtime's allocator is now its only ceiling: a
  submission that used to grow a private page allocator fails with
  `RESOURCE_EXHAUSTED` (`ENOMEM` inside a backend) when `a` refuses, with
  nothing live moved and every operation still settling once.
- `allocator.page`, `allocator.testing` and `allocator.arena` honor `align`,
  so a block's address may differ from 6.x (only ever more aligned), and
  `page` maps wider than the request for an alignment above the page.
- `allocator.heap` refuses, as `exhausted`, a span whose base is not a
  multiple of `SPAN_ALIGN`, where 6.x carved it and then lost its small
  blocks. Only a `Source` outside the base contract reaches this.

### Added

- `data.toml.Span` and, on every parsed `Value`, `span` and `key`: the byte
  offset and length in the document handed to `parse` of the value's literal
  as written and of the key token that maps to it, so a consumer can report a
  semantic problem against the source without text-matching. A table a
  header defines is positioned at the header line, a table a dotted key or an
  inner header segment created at that segment, and each `[[header]]`
  element at its header. A value not produced by `parse` carries the zero
  span in both. `Value` grows, so anything that links std and stores a
  `Value` or a `Table` must be rebuilt (#811).

### Changed

- **Breaking**: `io.runtime.make(runtime, a, initial)` takes the allocator
  every one of the runtime's allocations comes from, as `memory.table.make`
  does, and keeps a copy of it, so `a`'s context must outlive the runtime.
  The runtime no longer builds a page allocator of its own; its tables and
  its native event batch come from `a`, and `net.async`, `net.async.local`
  and their backends draw from `runtime.allocator` instead of a private page
  allocator. A refusal from `a` is the runtime's only ceiling, so a test
  allocator reaches every refusal branch: the submission fails with
  `RESOURCE_EXHAUSTED` (`ENOMEM` inside a backend), nothing live moves, and
  every operation still settles once. See MIGRATION.md (#677).
- `allocator.heap` tests run every behavioural case against a member
  matrix: the host mapper, `allocator_source` over `fixed`, and a mapper at
  the weakest base the contract allows. A new `Source` member is one more
  row (#665). `allocator_source` over `page` and over `testing` are rows
  too (#851).

### Fixed

- `allocator.page`, `allocator.testing` and `allocator.arena` honor the
  `align` argument, as the `Allocator` contract states. `page` widens the
  mapping and places the block for an alignment above the page (posix trims
  the pages around it, windows stashes the raw base ahead of it), `testing`
  places the block as close to its guard as the alignment allows, with fewer
  than `align` bytes of slack when the size is not a multiple of it, and
  `arena` aligns the address rather than the offset into its chunk. Before
  this, `testing` returned addresses aligned to nothing, `page` to the page
  and `arena` to the chunk header (#851).
- `allocator.heap`: a span whose base is not a multiple of `SPAN_ALIGN` is
  handed back to the source and the request refused as `exhausted`, instead
  of being carved and then missed by the small-block lookup. The padding
  `take_large` added above `SPAN_ALIGN` is gone: the source's base contract
  already bounds the payload offset by the requested alignment (#665).

## [6.1.0] - 2026-09-19

### Added

- `map.clone[K, V](m, alloc)` / `clone_by` and `set.clone` / `clone_by`: a
  copy of a map or set on another allocator without rehashing. The control
  bytes, keys and values are copied as they are, the copy answers every
  lookup the original does, the two share no storage afterwards, and a
  refused acquisition leaves nothing allocated (#847).
- `map.Iter`, `map.Entry[K, V]`, `map.iter` / `iter_by` and `map.next` /
  `next_by`, with `set.iter` / `iter_by` / `next` / `next_by` yielding `*K`:
  a cursor over a map's live entries that hides the slot layout. A step
  skips empty and deleted slots, so a whole walk costs the capacity; the
  order is unspecified, the entry just yielded may be removed, and an insert
  may grow the table and end the walk (#847).

## [6.0.0] - 2026-09-19

std 6.0.0 keeps `mach = "^5.8"`; nothing in it needs 5.9. Every removed or
changed signature below is a compile-time refusal at the caller, so a
program that builds against 6.0.0 has already moved. Three changes can
newly fail or differ at run time in code that already compiles:

- `buffers.open_account` and the source forms refuse, as counted misuse
  with the trap fired, a `Budgets` whose `lanes` differs from the pool's.
- `sort.binary_search` reports the first of several equal elements, where
  5.x reported whichever the probe met.
- The hash of a `str`, an integer or a record key is a different value:
  `natural.hash` is not the 5.x `map.hash_*`, and hashes were never stable
  across std versions.

### Added

- `std.collections.natural`: the natural order, equality and hash of a type,
  resolved at compile time. `less[T]`, `eq[T]` and `hash[T]` use the operator
  on integers and floats, content on `str`, and a lexicographic walk over a
  record's fields in declaration order (nested records descended); a pointer,
  union, tag, array, vector or `^` secret is refused at compile time with a
  written message. Every collection that orders or hashes reads this module
  (#655).
- `sort.sort_stable[T](data, len, scratch)` and `sort_stable_by`: a stable
  merge sort over a caller-supplied scratch buffer of `len / 2` elements,
  with no allocation (#655).
- `sort.sort_by`, `sort.is_sorted_by`, `sort.binary_search_by`: the
  comparator-taking forms of the three, with the comparator called through
  its pointer per comparison (#655).
- `heap.HeapBy[T]` with `init_by(alloc, cmp)` and the `_by` operations: a
  heap ordered by a stored comparator, called through its pointer per
  comparison, the spelling for an order the element type does not carry
  (#659).
- `map.MapBy[K, V]` and `set.SetBy[K]` with `init_by(alloc, hash_fn, eq_fn)`
  and the `_by` operations: a map or set keyed by stored, typed functions
  (`fun(*K) u64`, `fun(*K, *K) bool`), called through their pointers per
  probe, the spelling for a key the type does not carry a hash or equality
  for (#656).
- `std.crypto.ct.is_zero[T]`, `eq[T]`, `lt[T]` and `gt[T]`: the four
  comparison families as one generic each over `^T`, each `#[oblivious]` and
  `#[inline]`. Every instance is validated constant-time on its own, and the
  release lowering of each width is unchanged instruction for instruction on
  x86_64 and aarch64 (#660).

### Changed

- **Breaking.** `sort.sort`, `sort.is_sorted` and `sort.binary_search` no
  longer take a comparator: they order by `natural.less[T]`, so the compare in
  the emitted loop is the operator on `T` and no call is made per comparison.
  A caller with a comparator moves to the `_by` form (MIGRATION.md) (#655).
- `sort.sort` is pattern-defeating quicksort instead of Shell sort: O(n log n)
  worst case, insertion sort below 24 elements, a bounded insertion pass that
  confirms an already sorted range, an equal-elements partition, and a
  heapsort fallback after log2(n) bad partitions. Every scan is bounded by
  the range, so a comparator that contradicts itself leaves a permutation and
  never reads out of bounds. Sorting one million random `i64` drops from
  1148 ms to 85 ms by the natural order and 112 ms through a comparator
  (#655).
- `sort.binary_search` reports the first of several equal elements as `found`
  (#655).
- **Breaking.** `heap.Heap[T]` is `heap.Heap[T, D]` with `D` one of
  `heap.Min` or `heap.Max`, ordered by `natural.less[T]`. The `cmp` field and
  `init`'s `cmp` argument are gone, and every operation takes `[T, D]`. The
  sift compares with the operator on `T` directly: `push` and `pop` on a
  `Heap[i64, Min]` contain no indirect call in release output. A comparator
  moves to `HeapBy[T]` (MIGRATION.md). Pushing and popping one million
  random `i64` drops from 223 ms to 171 ms, and one thousand from 49 ns to
  26 ns per operation (#659).
- **Breaking.** `map.Map[K, V]` and `set.Set[K]` key by the natural hash and
  equality of `K`: `init` takes only the allocator, the `hash_fn`/`eq_fn`
  fields are gone, and so are the `ptr`-typed helpers `map.hash_str`,
  `eq_str`, `hash_i64`, `eq_i64`, `hash_u64`, `eq_u64`, `hash_u32`, `eq_u32`.
  A custom key moves to `MapBy` / `SetBy` (MIGRATION.md) (#656).
- The map probes over control bytes and masks instead of dividing: capacity
  is a power of two, the slot for a hash and every probe step is a mask, and
  one control byte per slot holds emptiness, deletion, or seven bits of the
  key's hash, so a mismatch is rejected without touching the key buffer.
  `find_slot` for a `Map[u64, u64]` contains no divide and no call of any
  kind in release output. Strings hash eight bytes at a time. Looking up one
  hundred thousand `u64` keys drops from 29 ns to 19 ns per hit and from
  21 ns to 15 ns per miss, one million from 39 ns to 28 ns per hit (#656).
- **Breaking.** `buffers.open_account`, `source_open_account` and
  `secret_source_open_account` take the per-lane budgets as a
  `buffers.Budgets` value (`lanes` plus `[8]usize` bytes) instead of a
  `*usize` the pool read `lanes` entries from, and `Source.fn_open_account`
  / `SecretSource.fn_open_account` change to match. A `lanes` that differs
  from the pool's is refused as counted misuse with the trap fired, so a
  short budget array can no longer be read past its end (#804) and a count
  mismatch is a loud refusal at open rather than lanes silently opened with
  budget 0 (MIGRATION.md) (#807).

### Removed

- **Breaking.** The twenty width-named constant-time comparisons in
  `std.crypto.ct`, `is_zero_u8`/`u16`/`u32`/`u64`/`usize`, `eq_*`, `lt_*`
  and `gt_*`. #660 (above) made each the generic at one width; the generic
  is the surface: `ct.lt_u32(a, b)` becomes `ct.lt[u32](a, b)`, and
  likewise for the other nineteen. Every instance lowers, in release, to the
  same instructions the removed function did, on x86_64 and aarch64 (#839).

## [5.8.0] - 2026-09-19

std now requires mach 5.8.0 (`mach = "^5.8"`): every aarch64-linux and
aarch64-darwin link reads `__mach_dit_required`, the cell that release's
linker defines (briar-systems/mach#3508), and the runtime spells the DIT
enable sequence with the asm mnemonics it adds.

### Added

- The aarch64 data-independent-timing mode. When the linker's
  `__mach_dit_required` byte says the link admits a secret integer multiply,
  `_rt_init` on aarch64 linux and darwin turns PSTATE.DIT on before `main`, and
  every thread trampoline std owns turns it on for its thread. A processor or
  kernel without the mode (linux: HWCAP_DIT absent from AT_HWCAP, darwin:
  `hw.optional.arm.FEAT_DIT` 0 or unreadable) makes the program refuse to
  start through the panic sink with status 255 and the contract's one-line
  message, before any secret multiply could run. `std.system.dit` holds the
  policy (`decide`), the cell (`required`), the enable sequence and the
  refusal text. The `cpu` capability group gains `cpu_dit()`, the OS's answer
  on whether the mode is available, sharing the reader `cpu_features` uses.
  `test/dit` runs a secret-multiply program and a plain one on the aarch64
  legs, and under `qemu-aarch64 -cpu cortex-a57` shows the refusal (#831).

## [5.7.1] - 2026-09-19

std now requires mach 5.5.2 (`mach = "^5.5.2"`): the hardware SHA-256 bodies
carry `#[oblivious]`, which needs the constant-time checker's view of welded
pointers inside inline asm that mach#3640 added.

### Fixed

- `sha256.sha_ni_block` and `sha256.sha2_block` carry `#[oblivious]`, so the
  constant-time checker holds the timing argument for the secret SHA-256 path
  through hardware that 5.6.0 could only state in prose. `test/sha256/oblivious`
  pins that the checker sees an oblivious asm body over a welded pointer: a
  branch on a loaded secret word and an address that rides one are both
  refused (#829).

## [5.7.0] - 2026-09-18

Rebuild everything that links std, do not just recompile against the new
sources. `buffers.Source` and `buffers.SecretSource` each grew by one word
(`fn_measure`). Source that builds these records still compiles unchanged, but
an object file built against 5.6.x that stores or passes one uses the old
layout, still links, and reads a stray word as the measure callback.

### Added

- `buffers.measure`, `buffers.source_measure` and `buffers.secret_source_measure`
  report the bytes `acquire` would charge for a request without acquiring it:
  the smallest fitting class's size, or the request rounded up to its alignment
  when no class fits, through the same code path `acquire` charges by. 0 for a
  request `acquire` would refuse as misuse. `Source` and `SecretSource` gain an
  `fn_measure` member, set by `buffers.source` and `buffers.secret_source` (#825).
- `sha512.SecretState512` with `init_secret512`, `update_secret512`,
  `final_secret512` and `destroy_secret512`: SHA-512 over secret-typed data
  with the same engine, block layout and welding contract as the SHA-384 entry,
  a 64-byte digest to `*^u8` (#823).

## [5.6.0] - 2026-09-18

### Added
- Secret-typed SHA-256 and SHA-384. `sha256.SecretState` holds `^u32` words
  and a `[64]^u8` block, with `init_secret`, `update_secret(s, *^u8, len)`,
  `final_secret(s, *^u8)` and `destroy_secret`, which zeroizes the words and
  the block so a destroyed state is all zero. `sha512.SecretState384` is the
  same entry for SHA-384 (`init_secret384`, `update_secret384`,
  `final_secret384`, `destroy_secret384`). The contract is the welding: a
  record embedding a secret state is welded, `update_secret` takes `*^u8`
  only so public bytes are lifted at the call site, the digest goes to `*^u8`
  and declassifying is the caller's decision, and no cast joins a secret
  state to the public `State`. `test/sha256/refusals` pins each with a build
  that must fail. The secret SHA-256 path uses the same SHA-NI and ARMv8 SHA2
  dispatch as the public one through a generic instance of the same asm body,
  so an HMAC key schedule runs at hardware speed; the portable compressions
  are `#[oblivious]` at the secret instance. Design by mach-crypto's steward
  (briar-systems/mach-crypto#122), which lets crypto drop its own SHA-2
  (#819).

## [5.5.0] - 2026-09-18

std now requires mach 5.5.0 (`mach = "^5.5"`): the hardware SHA-256 paths use
the instruction-set extension rows that release added.

### Added
- `std.crypto.hash.sha256` compresses with SHA-NI on x86_64 and ARMv8 SHA2 on
  aarch64 when the processor has them, chosen once at run time and cached.
  `init`, `update`, `final` and `hash` are unchanged, and `sha256.accelerated()`
  says which backend is in use. Measured at -O2 over 4 MiB (`test/sha256`):
  x86_64-linux portable 22.8 ns/byte, SHA-NI 0.66 ns/byte, 34x. The aarch64
  numbers are in the CI logs of the aarch64-linux and aarch64-darwin legs.
  The hardware functions are outliers under `#[extensions(...)]`: the
  dispatcher's run-time check is what puts control in them, and calling one
  on a processor without the extensions faults (#730).
- `std.system.cpu.features()` reports the running processor's instruction-set
  extensions as a per-isa record whose field names are the compiler's own
  (`sha`, `ssse3`, `sse41` on x86_64, `sha2` on aarch64, the isa letters on
  riscv). Each field has a `SELECTED_*` value reading
  `$mach.build.extensions.<name>`, so the record fails to compile the moment
  the compiler drops or renames a row. x86_64 reads cpuid and needs no OS.
  aarch64 reads the OS: `std.system.os` gains the `cpu` capability group
  (`HAS_CPU_FEATURES`) with one primitive, `cpu_features`, which linux fills
  from the auxv `AT_HWCAP` and darwin from sysctl. `std.system.cpu` builds
  freestanding and is in the ratchet (#730).

### Changed
- The tag-triggered workflow is `.github/workflows/cd.yml`, the family's name
  for it, and it serializes runs per tag so a duplicate tag push waits and
  then finds the release already published (#812, #814).

## [5.4.0] - 2026-09-17

Rebuild everything that links std, do not just recompile against the new
sources. `buffers.Source` and `buffers.SecretSource` each grew by one word
(`fn_lanes`). Source that builds these records still compiles unchanged, but an
object file built against 5.3.x that stores or passes one uses the old layout,
still links, and misreads the lane count.

### Added
- `buffers.source_lanes`, `buffers.secret_source_lanes` and `buffers.lanes`
  report how many per-lane budgets a source reads at account open, 0 when it
  declares none. `Source` and `SecretSource` gain an `fn_lanes` member, set by
  `buffers.source` and `buffers.secret_source`. A caller with a fixed-size
  budget array should check the count and refuse a source whose count differs:
  opening an account reads exactly that many budgets from the pointer it is
  given, so a shorter array is read past its end and the stray words become
  budgets. A hand-written `Source` or `SecretSource` that leaves `fn_lanes` out
  still compiles and reports 0, and a wrapper should forward the member of the
  source it wraps (#804).

### Changed
- A std module that needs an OS capability the target lacks now refuses a
  freestanding build with exactly one diagnostic naming what it needs, for
  example `std.filesystem needs the files capability
  (std.system.capability.HAS_FILES)`, instead of hundreds of resolution errors.
  Each OS-bound module gates its OS-bound imports on the capability flags it
  uses directly. `std.system.os`, `std.system.panic` and `std.runtime` say they
  need a linux, darwin or windows target, and the per-OS runtime and terminal
  modules name their own target. `std.system.os.secret` no longer repeats
  `std.system.os`'s refusal. `test/freestanding/verify.sh` enforces the single
  diagnostic for every module that does not build (#695).

### Documentation
- The README states what the version number promises. The driver and library
  modules are covered. The seven `std.net.async` backend modules may change
  signatures in a minor release. Calling past a driver is expected, so a
  caller that does should check this file when upgrading (#799, #802).

## [5.3.0] - 2026-09-17

Rebuild everything that links std before running it on 5.3.0. The runtime's
operation records changed layout, and a build made against 5.2.x still links
with no compile error.

Correction to 5.2.0: its "Known divergence" note said Linux and Darwin never
lose bytes when a read is cancelled. That was wrong. Losing the bytes of a
cancelled read was a contract defect on every backend, which Windows hit far
more often. 5.3.0 fixes it everywhere: a cancelled completion now carries the
transfer that finished before the cancellation, and a caller that cancels a
read must consume `bytes` from the cancelled completion. Code that treats
every error completion as empty loses exactly what it lost before.

### Fixed
- A cancelled or timed-out completion dropped the bytes that had already
  landed in, or left, the caller's storage, on every backend (#793). On Linux
  and Darwin a read that finished while its cancel was underway lost its
  bytes: the runtime refused the completion that raced the cancel, and a cancel
  that found a read already finished but not yet published withdrew it. A
  `complete_copy` that raced a cancel lost its copy the same way. Windows hit
  this far more often, since every read or datagram receive whose data arrived
  before its cancel was discarded. The 5.2.0 note that Linux and Darwin never
  lose bytes on cancel was wrong.

### Added
- `io.runtime.complete_cancellation_transfer(runtime, token, bytes, items,
  end_of_stream)` publishes an asynchronous cancellation together with the
  transfer its request finished first. `complete_cancellation` is now the
  zero-transfer form of it (#793).

### Changed
- A cancelled, timed-out or closed completion still has `has_error` set and
  its reason in `error`, and now also reports in `bytes`, `items` and
  `end_of_stream` the transfer that finished before the cancellation took
  effect. A caller that cancels a read must consume `bytes` from the cancelled
  completion, since the stream will not return them again. A cancelled write
  reports the bytes it sent, and a cancelled datagram batch the datagrams it
  filled (#793).
- A `complete`, `complete_batch` or `complete_copy` that loses to a
  cancellation already underway now succeeds, and its transfer rides on the
  cancelled completion. `complete_opened` and `fail` are still refused with
  `CLOSED`, so a source keeps and closes a socket it could not hand over (#793).
- Backend signature change: `cancel` in `net.async.linux`, `net.async.darwin`,
  `net.async.local.unix` and `net.async.iocp.port` takes a third argument,
  `finished: *opt[types.NativeCompletion]`, through which the backend hands
  back an operation that had already finished, so the driver reports its
  transfer with the cancellation. These are backend modules driven by
  `net.async` and `net.async.local`, not the supported entry point. Code that
  uses the drivers needs no change. Code that calls a backend's `cancel`
  directly must pass the new argument, or `nil` to keep the old behavior (#793).

### Deprecated
- `net.async.discarded_reads` and `net.async.local.discarded_reads` always
  return 0 and set `*bytes` to 0, since a cancelled read no longer discards
  anything. They will be removed in 6.0 (#793).

## [5.2.0] - 2026-09-17

Rebuild everything that links std before running it on 5.2.0. The layout of
the Windows `net.async` and `net.async.local` backend records changed, and so
did their `Driver`. A build made against 5.1.x still links and runs without any
compile error, but it reads those records the old way, which is not safe. No
source change is needed. std now declares `mach = "^5.3"`, so it builds with
mach 5.3.0 or later within 5.x.

### Behavior changes
- On Windows, cancelling a `net.async` operation the kernel already holds no
  longer blocks. The cancel returns at once, and the operation completes as
  cancelled once the aborted request reports back. `destroy` refuses with
  `EBUSY` until it does, and `awaiting_cancellations(driver)` shows how many
  are outstanding (#744).
- On Windows, a write that finished before its cancel may have reached the
  peer although it completes as cancelled (#744).

### Known divergence, being changed
On Windows, a read or datagram receive whose data arrived before its cancel
completes as cancelled and its bytes are discarded, although the peer
considers them delivered. Linux and Darwin read only after readiness is
dispatched, so a cancel there never loses bytes. This is not settled
behavior: #793 changes it so that a cancelled completion carries the bytes it
received, planned for 5.3.0. Do not build on the discard. Until then, a caller
that cancels a read it still wants bytes from can lose them on Windows, even
where a higher layer promises to keep what the transport gave it, so use a
deadline and keep reading until the stream drains instead. 5.1.x lost the same
bytes without counting them. `discarded_reads(driver, bytes)` now counts the
reads and the bytes (#744, #793).

### Added
- `net.async.discarded_reads` and `net.async.awaiting_cancellations`, with the
  same pair on `net.async.local`. Both read 0 on Linux and Darwin (#744).
- `net.async.types.STATUS_CANCELLED`, the backend status of an operation whose
  asynchronous cancel has settled (#744).

### Changed
- The Windows `net.async` backends keep a record per socket, found through a
  hash of the socket value, with a ready list for controls and a queue of held
  reads per socket. A flush, a completion, a write and a shutdown cost 0, 2, 2
  and 1 steps at 1k, 10k and 100k live operations, where they cost 2, 7, 1 and
  2 steps per live operation. Both backends share one core
  (`net.async.iocp`), which makes the decisions and does no native I/O, and one
  Windows layer (`net.async.iocp.port`), which holds cancel and dispatch
  (#744).
- `os.io_queue_restore` is no longer used by `net.async`. It stays available
  (#744).
- A Windows `net.async` or `net.async.local` cancel no longer wakes the
  runtime's native waiter and waits for it to leave the native wait. The cancel
  only requests the abort, and the packet settles it through dispatch. Each
  backend declares `CANCEL_NEEDS_NATIVE_CONTROL`, which stays true on Linux and
  Darwin, where cancel ends native access synchronously (#787).
- The layout of the Windows `net.async` and `net.async.local` backend records,
  and so of their `Driver`, changed. Rebuild everything that links std (#744).

## [5.1.0] - 2026-09-17

Rebuild everything that links std before running it on 5.1.0. The layout of
`sync.cancel.Scope` changed: `callback_count` is now an atomic `i64` where it
was a `usize`. The size of the record is unchanged, so code built against 5.0.x
still links and runs without any compile error, but it reads and writes that
field the old way, which is not safe. `os.shared.IoQueue`,
`memory.buffers.Snapshot` and every platform's `IoCompletion` also gained
fields. No source change is needed in code that does not build those records
by hand.

### Behavior changes
Both of these are correct, and both can turn a program that worked on 5.0.x
into one that fails:
- A `net.async` backend's `destroy` panics if a native registration would
  outlive it, where 5.0.x left the registration behind silently. `destroy`
  still releases idle sockets itself, so the panic points to a defect in std's
  registration accounting, not to caller misuse. Report it with the backend
  and platform (#740).
- On Windows, a `net.async` backend's `destroy` refuses with `EBUSY` while the
  kernel still owns one of its operations. Poll until the backend is idle, then
  destroy it again (#740).

### Added
- `io.runtime.NativeEvent.source` (and `source` on every platform's
  `IoCompletion`): the id of the source a native event belongs to, 0 for a
  wake. epoll and kqueue read it from the top 16 bits of the registered
  context (`os.shared.IO_SOURCE_SHIFT`, `io_source_context`,
  `io_context_source`). IOCP reads it from the completion key, which
  `io_queue_attach` now takes (#739).
- `io.runtime.unrouted_events(runtime)` counts native events whose source id
  matched no registered source. A nonzero count is expected when a source is
  released between a batch harvest and its dispatch (#739).
- `memory.buffers.Snapshot.release_failures` counts backing releases the
  allocator or the secret store refused. The pool cannot recover that memory,
  so the count is the only signal it leaked (#779).

### Changed
- `io.runtime` sends each native event straight to the source its id names,
  instead of offering it to every source in turn. Per-event dispatch is one
  offer at 1, 10 and 100 sources, where it was 1, 10 and 100 offers. Wakes still reach
  every source (#739).
- `sync.cancel` locks per scope instead of per tree. attach and unregister
  take only their scope's lock, so threads registering on separate child
  scopes no longer contend. At 8 threads on per-thread children, attach plus
  unregister totals 78M/s, where it was 5.8M/s. Single-threaded use is
  slower: about 6% on attach and unregister, and about 12% on the full
  make_child, attach, unregister and destroy lifecycle, because destroy now
  takes the parent's lock and then the scope's. A scope shared by threads still
  serializes, and the module now documents per-worker roots and per-connection
  child scopes as the intended shape. `Scope.callback_count` is now an atomic
  `i64`, which leaves the size of `Scope` unchanged (#754).
- `io.runtime` recycles source ids, so a runtime has no lifetime limit on
  registrations. The limit was 65,535. A released id waits until every native
  collection that began before its release has ended, so an event harvested
  for the old source can never reach the new one. The wire id stays 16 bits,
  so at most 65,535 sources can be registered at once. The two invariants this
  rests on are enforced and tested: a source with a live operation cannot be
  released, and a backend's `destroy` removes every native registration and
  waits for the kernel (see Behavior changes) (#740).
- Native wakes are coalesced. `os.shared.IoQueue` gains `wake_pending`, so only
  the first wake request since the last poll posts a native wake (an eventfd
  write, a `NOTE_TRIGGER` kevent or an IOCP packet), and later requests post
  nothing until a poll takes it. The poll clears the flag after draining the
  wake and before the caller looks for work, so no request is lost. N
  operations completed between two waits now post 1 wake at 1k, 10k and 100k,
  where they posted N. `IoQueue.wakes_posted` counts posted wakes (#753).
- `net.resolve` keeps runtime-owned lookups waiting to publish on an intrusive
  list, finds an operation from its runtime token through a hash of the token
  index, remembers each queued completion's ring position, and claims slots
  from a free list. Runtime dispatch, cancel and release no longer scan every
  resolver slot. Each costs one step at 1k, 10k and 100k slots, where each
  cost R steps before. `Resolver` gains a `steps` counter used by the scaling
  test (#742).
- `net.async.local` claims stream and listener entries from free lists instead
  of scanning up to the high-water mark on every accept, connect and bind. A
  claim after churn costs one step at 1k, 10k and 100k streams, where it cost n
  steps before (#743).

### Fixed
- A registration that loses a race with runtime close no longer leaves a
  source slot stuck, which made `destroy` report busy forever. This defect is
  separate from id recycling, and was found while doing it.
- The `memory.buffers` `source_*` and `secret_source_*` wrappers refuse a nil
  source or a nil member as misuse, instead of calling through nil. Found in
  the #775 sweep (#778).
- `memory.buffers` no longer ignores a refused backing release. Plain and
  secret releases, and the cleanup after a failed secret borrow, count the
  failure in `release_failures`. Found in the #775 sweep (#779).
- On Windows, canceling a stream operation after its socket's close no longer
  panics the runtime with "source cancellation lost operation ownership". The
  close had already asked the kernel to abort the operation, and the cancel
  refused it with EBADF. It now waits for the aborted packet, as it does for an
  operation it aborts itself. The local-socket backend already did (#786).

## [5.0.1] - 2026-09-17

Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.

### Fixed
- `memory.buffers` no longer crashes when a fresh chunk is acquired after
  released chunks were retained. Retained chunks keep their slots, but the slot
  table's demand left them out, so the table could be full with no room for the
  new chunk, and the missing slot was written through nil. The demand now counts
  held, retained and reserved slots. A pool that still finds no slot refuses
  with `Reason.memory` and returns the backing it just allocated (#775).

## [5.0.0] - 2026-09-17

Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.
MIGRATION.md covers the breaking changes.

### Added
- `time.Instant`, a monotonic instant that is distinct from the wall-clock
  `time.Time` and never converts to or from it. Read it with `time.instant()`,
  which needs the clock capability. The arithmetic is `instant_add`,
  `instant_sub`, `instant_before`, `instant_after` and `instant_equal`, and it
  builds freestanding. `time.elapsed(start)` and `time.remaining(deadline)`
  measure against the monotonic clock (#752).

### Changed
- **Breaking:** every deadline is an `Instant`.
  - `cancel.make_root(scope, deadline: opt[Instant])` and
    `cancel.make_child(scope, parent, deadline: opt[Instant])` replace the
    `has_deadline` flag and its placeholder `Time`.
  - `cancel.expire` takes the current `Instant`, and `cancel.Deadline.at` is an
    `Instant`.
  - These now take an `Instant` deadline: `io.runtime.submit_timer`,
    `io.runtime.submit_timer_scoped`, `sync.condition.wait_until`,
    `sync.channel.send_until`, `sync.channel.receive_until`,
    `sync.worker_pool.submit_until` and `net.resolve.wait_until`.
  - A wall-clock `Time` passed as a deadline no longer compiles
    (`test/deadline`). MIGRATION.md has the before and after (#752).
- **Breaking:** `time.Time` is wall-clock only. `time.now`, `time.since` and
  `time.until` read the calendar clock, which can jump (#752).
- `io.runtime` keeps one refcounted deadline entry per (scope, deadline), not
  one per operation. N operations under one scope hold a single heap entry, and
  submission and completion cost stays flat from 1k to 100k operations. Expiry
  still ends every operation still registered in the scope (#741).
- The license copyright is held by Briar Systems LLC. The MIT terms are unchanged (#765).
- **Breaking:** `std.memory.buffers.Source` gained `fn_open_account`,
  `fn_close_account`, `fn_data`, `fn_retain`, `fn_settle`, `fn_in_flight` and
  `fn_ready`, so a consumer can drive a whole buffer lifecycle through the
  interface alone. `source(pool)` fills every member, and new `source_*` free
  functions call through a `*Source` without touching the function pointers (#767).
- **Breaking:** secret chunks moved from `buffers.Source` to a new
  `buffers.SecretSource`. `Source` no longer has `fn_secret`, and
  `source_secret` is gone. A plain `Source` holds nothing welded, so a record
  holding a `Source` or a `*Source` passes through `ptr` (io.runtime
  completions, thread args, cancel callbacks). `SecretSource` has open and
  close account, acquire, release and `fn_view`, and only its holder is welded.
  `secret_source(pool)` builds one, and the `secret_source_*` functions call
  through it. A `Source` refuses a secret request as misuse, and a
  `SecretSource` refuses a plain one (#771).

### Removed
- **Breaking:** `time.monotonic`. Use `time.instant` (#752).

## [4.2.0] - 2026-09-17

Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.

### Added
- `std.memory.buffers`: one shared on-demand buffer source (`Source`) and std's
  implementation (`Pool`).
  - Classes are caller-declared, and a request larger than every class takes an
    oversize path that is budgeted and returned to the backing at once.
  - Budgets are in bytes, per account lane plus a global budget. An account may
    reserve bytes, and its slot metadata is reserved at open.
  - A refusal is typed (budget, exhausted, memory, misuse). Exhausted and
    memory refusals register the account for a FIFO wake-up, drained with
    `ready` or reported through an optional `notify`.
  - `acquire_n` is all-or-nothing.
  - Secret classes hold welded `std.memory.secret` storage that is wiped in full
    on release. They need the pages capability.
  - `retain`, `settle` and `in_flight` track in-flight users.
  - Chunks are address-stable.
  - Use is serialized, enforced by an entrant check rather than a thread check.
  - `snapshot` reports counters, including `backing_allocations` per class and
    in total, so `high_water` can be sized for a steady state that never touches
    the backing. `arena_bytes` sizes an `allocator.fixed` arena.
  - Acquire, release and wake cost stays flat from 1k to 100k chunks. The module
    builds freestanding (#760).
- `std.memory.secret.borrow_data` returns the welded storage of a live borrow
  (#760).
- `net.async.submit_readable` and `net.async.local.submit_readable` wait until a
  stream is readable, at orderly end of stream, or failed, without holding a
  buffer, so an idle connection needs no read buffer. The completion has the new
  kind `io.runtime.READABLE` and zero bytes, with `end_of_stream` set at EOF.
  Nothing is read, and the wait queues in order with reads on the same stream.
  Linux and darwin settle readiness with a non-consuming peek, and windows posts
  a zero-byte overlapped receive and settles it with the queued byte count
  (#759).

## [4.1.0] - 2026-09-17

Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.

### Added
- `std.process.limits`: read and set the open-file limit. `open_files()` returns
  a `FileLimit` with the soft limit in force, the hard limit, and the highest
  soft limit this process may set (`ceiling`); `set_open_files(limit)` sets the
  soft and hard limits; `raise_open_files()` raises the soft limit to the
  ceiling. A soft limit above the hard one is `INVALID`, raising the hard limit
  without privilege is `PERMISSION`, and windows, which has no such limit,
  reports `UNSUPPORTED`. The OS contract's process group gains
  `open_file_limit` and `set_open_file_limit` (#746).


- `std.system.os.thread_affinity(words, capacity, out_count)` and
  `set_thread_affinity(words, count)` read and pin the calling thread's CPU
  affinity, in the threads capability group. The mask is caller-sized words with
  no fixed CPU limit, and a short buffer reports `RANGE` with the words needed.
  windows numbers CPUs across processor groups and refuses a set spanning groups
  as `UNSUPPORTED`; darwin has no hard affinity and returns `UNSUPPORTED`.
  `std.sync.thread` adds `CpuSet` over caller words (`cpu_set`, `cpu_set_add`,
  `cpu_set_contains`, `cpu_set_size`, `cpu_set_nth`, `cpu_set_clear`),
  `current_affinity`, `affinity_words`, `set_current_affinity`,
  `pin_current_to` and `allowed_cpus`, which lists the CPUs the thread may run on
  in ascending order so worker i can pin to the i-th (#755).
- Listeners and datagram sockets take options applied before bind, so a
  multi-core server can bind one `SO_REUSEPORT` socket per thread:
  `net.socket.BindOptions { reuse_address, reuse_port }` and
  `net.socket.bind_options()`; `net.tcp.ListenOptions { bind, backlog }`,
  `net.tcp.listen_options(backlog)`, `net.tcp.listen_with` and
  `net.tcp.listen_with_options`; `net.udp.bind_with` and
  `net.udp.bind_with_options`; `net.async.listen_with` and
  `net.async.bind_datagram_with`. The defaults match `listen` and `bind`
  exactly. `reuse_port` where the target has no `SO_REUSEPORT` (windows) is
  refused as `UNSUPPORTED` before any socket is created (#738).

### Changed
- The README is trimmed to what std is, how to add it, supported compilers and
  targets, and links. The versioning policy moved to CONTRIBUTING.md, and the
  API contract sections moved into their modules' doc comments (#756).
- `chrono.time` and `sync.cancel` document that deadlines are monotonic and must
  be built from `time.monotonic()`. `time.now`, `since` and `until` are documented
  as wall-clock only, and `make_root`/`make_child` warn that a wall-clock deadline
  never fires. This is documentation only, with no behaviour change (#750).
- Releases run through the family's shared release workflow (briar-systems/.github
  `mach-release.yml`): it verifies the tag, version and changelog section, runs
  the full CI, then publishes. The release-archive check that no test-only fault
  module ships now runs in CI on every x86_64-linux run (#735).

### Fixed
- On linux, darwin and local unix sockets, `net.async` keeps a socket registered
  from its first operation until it is closed through the driver. It used to
  unregister and forget the socket whenever its queue emptied, so every blocked
  operation paid an address lookup, a registration and an unregistration. Now
  only the first operation looks the socket up and registers it, and every
  later one rearms the existing registration. A datagram socket is configured
  once instead of on every receive. An idle socket costs one resource record
  until it is closed through the driver, and destroying a driver releases any
  idle ones (#737).
- The backends' socket map deletes by shifting the probe run back instead of
  leaving tombstones, so lookups no longer grow longer as a server opens and
  closes sockets. After heavy churn a miss used to scan the whole map, for
  example 262,145 probes at 100,000 sockets. It now stops at the first empty
  slot (#737).
- On linux, when a rearm finds that a socket's registration has vanished, the
  socket was closed outside the driver. The pending operation completes as
  closed, and the socket now behind that value is registered only when it is
  submitted with its own handle (#737).

## [4.0.1] - 2026-09-16

Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.

### Fixed
- On linux and darwin, a `net.async` datagram send batch with a packet whose
  `length` exceeds its `capacity`, whose buffer is missing, or whose peer family
  is unsupported is refused as a whole before any native call, as on windows:
  the send completes with an `INVALID` (or `UNSUPPORTED`) error and nothing
  from the batch is sent. They used to send the packets up to the bad one
  (#720).

## [4.0.0] - 2026-09-16

The OS layering from #697 is complete: `std.system.os` is a small contract of primitives, error translation lives in the OS layer, logic built on top of it moved out, and descriptors cross it as pointer-width handles. Every breaking change and its replacement is in MIGRATION.md. Requires mach 5.2.0 or later. Tested with mach 5.2.1, the family CI seed.

### Added
- `std.system.os.error(code, operation)` builds the `io.error.Error` for a
  native code a primitive returned, and `std.system.os.error_kind(code)` is the
  portable reading of such a code. A caller that checks a raw primitive return
  compares `os.error_kind(n)` with a kind, never the code with an errno.
  `std.system.os.error_message(code)` gives the native text (#688).
- `io.error.kind_name(kind)` names a kind, for an error with no native code
  behind it (#688).
- `ELOOP` on linux and windows, where windows maps
  `ERROR_CANT_RESOLVE_FILENAME` to it (#688).
- `std.filesystem.removal.Error` has a `kind`. `removal.from_native(code)`
  builds one for a native failure and `removal.contained()` for a component or
  depth removal refuses (#693).
- `std.process.exec.Failure` has a `kind`, the portable classification of the
  failure (#693).
- `std.memory.secret`: secret-welded storage built on the os contract's secret
  primitives. `allocate`, `deallocate`, `allocate_typed`, `deallocate_typed`,
  `random_fill`, `Borrow` and `borrow_open`, `borrow_close`, `borrow_size`,
  `borrow_wipe`, `borrow_fill`, `borrow_drain`, `borrow_copy`,
  `borrow_read_at` and `borrow_write_at`. Fallible calls return
  `err[io.error.Error]` (the positioned transfers return
  `res[usize, io.error.Error]`) instead of a negative errno (#692).
- The os contract's secret primitives, each one native call that keeps the
  welded pointer shape: `std.system.os.allocate_secret`, `release_secret`,
  `allocate_secret_typed`, `release_secret_typed`, `random_fill_secret`
  (at most `RANDOM_FILL_SECRET_MAX` bytes per call), `read_at_secret` and
  `write_at_secret`. They do not wipe or retry (#692).
- `std.net.ip.sockaddr_family(sa)` reads the family a sockaddr buffer carries
  (#692).
- `std.process.exec.stopped`, `stop_signal` and `continued` read stop and
  continuation observations (#692).
- `std.filesystem.native` holds `stat_mode`, `unlink_force` and `temp_dir`
  (#692).
- `std.process.exec.spawn_shell(command, cwd, envp)` starts a command through
  the host interpreter without waiting. `run_shell` is built on it. The
  interpreter choice is a per-OS table in `std.process.exec`: `/bin/sh -c`
  on posix, and on windows `%ComSpec%` (falling back to the System32
  `cmd.exe`) with the verbatim `"<shell>" /s /c "<command>"` line (#692).
- `std.system.os.windows.spawn_command_line(application, command_line, envp,
  cwd)` spawns from a verbatim native command line. It is a per-OS escape
  hatch outside the contract: the contract's argv spawns encode arguments with
  the CRT convention, which cmd.exe does not parse (#692).
- `std.system.os.INVALID_HANDLE`, the handle no resource has, and
  `os.stdin()`, `os.stdout()`, `os.stderr()` and `os.working_dir()`, the
  process's standard handles and the directory handle that resolves a path
  against the working directory. They are functions because a future
  implementation may only learn them at run time (#694).
- `std.system.os.exit(status: u32)` ends the process, and
  `std.system.os.panic_sink(msg, len)` writes to the error stream and ends the
  process. The per-OS panic arms in `std.system.panic` are these sinks (#694).

- `std.io.handle.socket(value)` wraps a native socket the process has just
  opened or accepted, stamping the handle with a process-wide opening. Every
  std socket constructor uses it (#716).
- `std.net.async.stream(completion)` turns a successful accept or connect
  completion into the stream the driver knows, opening included (#716).
- `io.runtime.Completion.opening` and `io.runtime.complete_opened`: a completion
  that hands over a socket carries its opening (#716).
- `std.system.os.linux.io_queue_rearm` and `std.system.os.darwin.io_queue_rearm`
  re-arm a registration the caller made, and `duplicate_to(from, to)` in the
  same modules replaces a descriptor number in one step (#716).

### Changed
- **Breaking.** `memory.table.make(table, a, element_size, initial)` takes the
  `allocator.Allocator` every chunk is taken from and returned to, and
  `memory.table.destroy` returns `err[allocator.Error]` instead of an `i64`. A
  refused release is reported as `release` with the backend's native code, and
  the table is still emptied. Chunks are requested at `memory.table.ELEMENT_ALIGN`
  (16), the largest alignment an element type may need. memory.table no longer
  depends on the OS layer and now builds freestanding (#689).
- **Breaking.** `memory.table.Table` has an `allocator` field holding a copy of
  the allocator passed to `make`, so the allocator's context must outlive the
  table (#689).
- `io.runtime.Runtime`, `net.async.Driver`, `net.async.local.Driver` and every
  `net.async` backend hold the allocator their tables use in an `allocator`
  field, which `make` sets to a page allocator (#689).
- The freestanding ratchet includes `std.memory.table` (#689).
- **Breaking.** Native codes classify with the full kind set. A code that used
  to be `OTHER` now gets its own kind: `EIO` is `IO`, `ENOENT` is `NOT_FOUND`,
  `EEXIST` is `EXISTS`, `ENOTDIR` is `NOT_DIRECTORY`, `EISDIR` is
  `IS_DIRECTORY`, `ENOTEMPTY` is `NOT_EMPTY`, `ENAMETOOLONG` is
  `NAME_TOO_LONG`, `EBUSY` is `BUSY`, `ERANGE` is `RANGE`, `ECHILD` is
  `NO_CHILD` and `ELOOP` is `LOOP`. On windows every unmapped native error was
  already `EIO`, so it now reads as `IO` (#688).
- **Breaking.** `std.system.os.message` takes an `io.error.Error`, not a code.
  It gives the native text when a native code is behind the error and the
  kind's name otherwise. The code form is `std.system.os.error_message` (#688).
- **Breaking.** An error std raises itself, with no native call behind it,
  now has `code` 0 and states its kind. Before, it borrowed an errno such as
  `EBADF` for a closed handle or `EINVAL` for invalid use, so a caller that
  compared `code` with those errnos must compare `kind` instead (#688).
- **Breaking.** `std.terminal.control_failure` and `read_failure` are defined
  in `std.terminal`. `std.terminal.error` holds only the outcome tags and
  `code` (#688).
- **Breaking.** Modules outside the OS layer compare kinds, never errno.
  A refusal std makes on its own carries a kind and code 0, a native failure
  keeps its code, and a raw primitive return is read with `os.error_kind`
  (#693). This changes what several public results hold:
  - `std.filesystem.removal.Error.code` is 0 for a refusal, and an entry name
    a native listing returns that is not a single component is a containment
    refusal, not `EIO`.
  - `std.filesystem.transaction.ownership` functions return
    `err[removal.Error]` instead of an `i64` code.
  - `std.filesystem.transaction` maps an ownership refusal to its own kinds:
    invalid use is `INVALID`, a held root lock is `LOCK_HELD`, an unsupported
    backend is `UNSUPPORTED`, and a claim that already exists or a claims
    entry that is not a directory is `CONFLICT`. A native `EINVAL` elsewhere
    in a publication is `IO` with its code.
  - `std.process.exec.Failure.code` is 0 when the refusal is the module's own,
    such as waiting on a child that was never spawned.
  - `std.io.file`, `std.io.file.adapter`, `std.filesystem`, `std.process.events`
    and `std.net.local` report their own refusals with `io.error.make`.
  - `std.net.local.endpoint.to_sockaddr` and `from_sockaddr` return
    `err[io_error.Kind]` instead of an `i64` code.
  - `std.net.resolve` completions that fail carry the resolver's kind directly
    (`NO_NAME` is `NOT_FOUND`, `TEMPORARY` is `WOULD_BLOCK`) and keep the
    resolver's native code when there is one.
  - `std.process.events` reports a failed windows console handler install or
    restore with its native error instead of `EINVAL`.
- **Breaking.** `std.system.os.getenv` reports an unset variable as a native
  code that `os.error_kind` reads as `NOT_FOUND` (`ENOENT`), not the `-1`
  sentinel, which shared the native code space with `EPERM` (#692).
- **Breaking.** The sockaddr layout is written once in `std.net.ip`.
  `to_sockaddr` and `from_sockaddr` no longer go through the OS layer (#692).
- **Breaking.** Every descriptor that crosses the `std.system.os` contract is
  a pointer-width handle (`usize`), not an `i32` (#694). A primitive that makes
  a handle writes it through an out parameter and returns only a status, so a
  handle value can never be read as a negative native code:
  - `read`, `write`, `close`, `sync_fd`, `stat`, `set_mode`, `file_identity`,
    `publication_capabilities`, `seek`, `lock_fd`, `map_file`,
    `directory_init`, `read_at_secret` and `write_at_secret` take
    `handle: usize`.
  - `set_mode_at`, `identity_at`, `stat_path`, `unlink`, `make_dir`, `access`
    and `rename` take `dir: usize` directory handles.
  - `open(dir, path, flags, mode, out: *usize) i64` returns 0 and writes the
    handle, where it used to return the descriptor.
  - `retain_identity_at(dir, path, access, out, handle: *usize) i64` does the
    same.
  - `pipe(read_end: *usize, write_end: *usize) i64` replaces `pipe(fds: *i32)`.
  - `spawn_redirected` and `spawn_redirected_in` take `usize` standard
    handles, and `INVALID_HANDLE` keeps the parent's, where `-1` did.
  - A missing handle is `INVALID_HANDLE`, never a negative value: a `usize`
    compared with `< 0` is always false.

  Worked example:

  ```mach
  # before
  val fd: i64 = os.open(os.AT_FDCWD, path, os.O_RDONLY, 0);
  if (fd < 0) { ret fail(fd); }
  val n: i64 = os.read(fd::i32, buf, len);
  os.close(fd::i32);

  # after
  var fd:     usize = os.INVALID_HANDLE;
  val opened: i64   = os.open(os.working_dir(), path, os.O_RDONLY, 0, ?fd);
  if (opened < 0) { ret fail(opened); }
  val n: i64 = os.read(fd, buf, len);
  os.close(fd);
  ```

  A pipe: `var r: usize; var w: usize; os.pipe(?r, ?w);` replaces
  `var fds: [2]i32; os.pipe(?fds[0]);`. Code that needs a raw native
  descriptor, for example to pass it through `SCM_RIGHTS`, uses the per-OS
  module (`std.system.os.linux` and friends), which keeps its native `i32`
  shape.
- **Breaking.** The descriptors std's own APIs hold or accept are handles too
  (#694):
  - `std.filesystem.transaction.root_fd` and `root_home_fd` return `usize`,
    and `INVALID_HANDLE` for an invalid root.
  - `std.filesystem.transaction.ownership`: `control_fd`, `root_init`,
    `root_init_with_home` and `root_set_home` use `usize`, and so do the `Root`,
    `Lock` and `Borrow` descriptor fields.
  - `std.filesystem.removal.tree` and `private_tree` take a `usize` directory
    handle.
  - `std.filesystem.native.unlink_force` takes `dir: usize`.
  - `std.process.exec.spawn_redirected`, `spawn_redirected_grouped`,
    `spawn_redirected_in` and `spawn_redirected_in_grouped` take `usize`
    handles, and `os.INVALID_HANDLE` inherits the parent's stream.
  - `std.memory.secret.borrow_read_at` and `borrow_write_at` take
    `file: usize`.
  - `std.net.resolve.lines.Reader.fd` is a `usize`.

- **Breaking.** A socket a `net.async` driver has seen is closed through the
  driver (`submit_stream_close`, `submit_datagram_close`). `io.handle.SocketHandle`
  gains an `opening`, and the linux, darwin and windows backends key their state
  by native value and opening together. A socket closed outside its driver is
  detected on the next submission through either handle:
  - its pending work completes `CLOSED` with code 0
  - a submission through the old handle is refused the same way
  - the socket that now holds the native value keeps its own state and
    registration

  Before, the backends keyed state by the native value alone, so a reused value
  inherited the old socket's pending operations, and a later cancel could
  unregister the new owner (#716).
- **Breaking.** `std.system.os.linux.io_queue_watch` only registers: a
  descriptor that is already registered is refused with `EEXIST` instead of
  being taken over, and a caller re-arms its own registration with
  `io_queue_rearm`. A backend resource unregisters only a registration it made
  (#716).
- **Migration.** Close a socket a driver knows through that driver. hedge's
  `listener.close_connection` (`tcp.stream_close` on a driver-tracked stream) is
  the known case. Build accepted and connected streams with
  `net.async.stream(completion)`, and wrap any other native socket once with
  `io.handle.socket` and pass that handle around: two handles wrapped from one
  live socket look like two sockets, and the driver treats the older one as
  closed (#716).

### Removed
- **Breaking.** `io.error.from_code` and `io.error.message`. Use
  `std.system.os.error` and `std.system.os.message`, or `io.error.make` for an
  error with no native code. `std.io.error` no longer depends on the OS layer
  and builds freestanding, and so does `std.terminal.error` (#688).
- **Breaking.** The 38 `E*` constants on `std.system.os` (`EPERM` through
  `ECANCELED`). Compare `std.system.os.error_kind(code)` with an `io.error`
  kind. The per-OS modules (`std.system.os.linux`, `.darwin`, `.windows`) keep
  their constants for code that is already OS-specific. `std.io.writer` no
  longer depends on the OS layer and builds freestanding (#693).
- **Breaking.** Logic built on the os primitives leaves `std.system.os`, with
  no forwarder (#692):

  | removed | use instead |
  | --- | --- |
  | `os.secret_allocate` | `std.memory.secret.allocate` |
  | `os.secret_deallocate` | `std.memory.secret.deallocate` |
  | `os.secret_allocate_typed` | `std.memory.secret.allocate_typed` |
  | `os.secret_deallocate_typed` | `std.memory.secret.deallocate_typed` |
  | `os.secret_random_fill` | `std.memory.secret.random_fill` |
  | `os.SecretBorrow` | `std.memory.secret.Borrow` |
  | `os.secret_borrow_*` | `std.memory.secret.borrow_*` |
  | `os.sock_addr_init`, `sock_addr6_init` | `std.net.ip.to_sockaddr` |
  | `os.sock_addr_read`, `sock_addr6_read` | `std.net.ip.from_sockaddr` |
  | `os.sock_addr_family` | `std.net.ip.sockaddr_family` |
  | `os.has_exited` | `std.process.exec.exited` |
  | `os.exit_code` | `std.process.exec.code` |
  | `os.was_signaled` | `std.process.exec.signaled` |
  | `os.term_signal` | `std.process.exec.signal` |
  | `os.was_stopped` | `std.process.exec.stopped` |
  | `os.stop_signal` | `std.process.exec.stop_signal` |
  | `os.was_continued` | `std.process.exec.continued` |
  | `os.stat_mode` | `std.filesystem.native.stat_mode` |
  | `os.unlink_force` | `std.filesystem.native.unlink_force` |
  | `os.temp_dir` | `std.filesystem.native.temp_dir` |
  | `os.NOT_FOUND` | `os.error_kind(n) == io.error.NOT_FOUND` |
  | `os.spawn_shell(command, envp, cwd) i64` | `std.process.exec.spawn_shell(command, cwd, envp) res[Child, Error]` |
  | `os.separator` | `std.types.path.separator()` |

  The sockaddr and status helpers, and `spawn_shell`, are also gone from the
  per-OS modules.

  What stays in the contract, on purpose: `ProcessStatus` with its
  `PROCESS_*` kind and stage values, since the native wait and spawn
  primitives produce them. `getenv` reports an unset variable as `ENOENT`
  rather than moving a sentinel to its caller. `stat_mode`, `unlink_force`
  and `temp_dir` sit in the leaf module `std.filesystem.native` because
  `std.filesystem`, its removal and transaction modules, and `std.net.local`
  all use them.
- **Breaking.** `std.system.os.STDIN_FD`, `STDOUT_FD`, `STDERR_FD` and
  `AT_FDCWD`. Use `os.stdin()`, `os.stdout()`, `os.stderr()` and
  `os.working_dir()`. The per-OS modules keep the native constants (#694).
- **Breaking.** `std.system.os.terminate`. Use `os.exit(status: u32)` (#694).

## [3.3.0] - 2026-09-16

Requires mach 5.2.0 or later: the capability gates need the compiler fix in briar-systems/mach#3469. Tested with mach 5.2.1, the family CI seed.

### Added
- `net.async.submit_listener_close(driver, scope, listener, context)` closes a
  TCP listener the driver knows about, so the backend unregisters it. Every
  accept still pending on it completes cancelled, and the listener's handle is
  invalidated. A listener that has had an accept submitted is closed this way,
  not with `tcp.listener_close`, the same as streams and datagram sockets
  close through `submit_stream_close` and `submit_datagram_close` (#724).
- `std.system.capability`: comptime flags for the OS capability groups a
  target provides, `HOSTED`, `HAS_PAGES`, `HAS_CLOCK`, `HAS_ENTROPY`,
  `HAS_THREADS`, `HAS_FILES`, `HAS_IO_QUEUE`, `HAS_SOCKETS` and `HAS_PROCESS`.
  A module gates on them with `$if`, which discards an OS-bound branch before
  resolution. The module imports nothing OS-bound and builds freestanding. Every
  flag is set on linux, darwin and windows, and none is set on any other target
  (#685).

### Changed
- Core modules keep their test-only code, and the test-only imports of
  `std.allocator.page`, `std.allocator.testing` and `std.system.os`, behind
  `std.system.capability.HOSTED`, so importing them no longer pulls in the OS
  layer. `io.error.from_code` and `io.error.message`, and
  `std.terminal.error`'s `control_failure` and `read_failure`, exist only where
  the OS layer does. Nothing changes on linux, darwin or windows. 57 modules
  now build for a freestanding target, up from 37: the collections, compress,
  `data.json`, `data.toml`, `derive`, `encoding.binary`, `format`, `io.error`,
  `io.reader`, `io.writer`, `terminal.error`, `types.semver` and
  `allocator.arena` (#686).
- `std.chrono.time`'s `Time` and its arithmetic no longer need the OS
  layer. `now`, `monotonic`, `since` and `until` exist only where the clock
  group does (`std.system.capability.HAS_CLOCK`). `std.types.path.separator`
  is a target constant rather than a read of `std.system.os`. In
  `std.log.record`, `system_clock` also requires the clock group, a record with
  a caller-supplied timestamp or clock works on every target, and an error
  field includes its native message only where the OS layer can translate the
  code. Nothing changes on linux, darwin or windows. `chrono.time`,
  `chrono.date`, `chrono.format`, `types.path` and `log.record` now build
  freestanding, 62 modules in all (#690).
- `OS-CONTRACT.md` documents the `std.system.os` contract: its
  capability groups, the members of each group as of 3.x, and the assumptions
  a user-supplied implementation can rely on. `std.system.capability.conformance`
  names every member of every group a target claims, so a missing member fails
  the build (#691).

### Fixed
- A spawned child whose redirected stream is the descriptor it already is, such
  as `stdout_fd = 1` or `stderr_fd = 2`, now runs. On linux aarch64 and riscv64
  the redirect used `dup3`, which refuses a descriptor onto itself, so the child
  exited 126 before exec. On every linux arch and on darwin, such a stream now
  also survives exec when it was close-on-exec: the redirect clears the flag
  instead of duplicating, where `dup2` onto itself used to leave it set. Windows
  hands handles to the child without duplicating them and was not affected
  (#722).

## [3.2.1] - 2026-09-16

Tested with mach 5.2.1, the family CI seed.

### Fixed
- A `net.resolve` resolver on an `io.runtime` no longer claims native events
  that belong to other sources. Its dispatch returned "claimed" whenever it
  published a result, and the runtime stops offering an event at the first
  claim, so a resolver registered before a `net.async` driver could swallow a
  socket's oneshot readiness. The socket was then never re-armed and its
  pending operation never completed. The resolver owns no native context and
  now never claims one, and `io.runtime.DispatchFun` documents the rule
  (#715).
- On windows, a pending `net.async` datagram receive batch completes as soon as
  a datagram is available and carries every datagram already queued, up to its
  count, as on linux and darwin. It used to wait until the whole batch had
  arrived, so a server that kept `receive_batch(16)` pending waited for sixteen
  datagrams under light traffic. After the first datagram the windows backend
  now takes only datagrams that are already queued, with a synchronous
  receive, and never posts a receive that could wait. The batch contract is
  documented on `submit_receive_batch` (#718).
- The `net.async` packet record documents `capacity` and `length`. A send
  refuses a length above the packet's capacity, which the windows backend
  already enforced (#711).
- `net.async` has regression coverage for a pending datagram receive under
  load: a flood past the receive buffer with one thread and with a submitting
  thread, and scoped batch-of-one sends with cancelled child scopes and table
  growth. The #711 stall report traced to the caller, not std, so no library
  behaviour changed for it (#711).

## [3.2.0] - 2026-09-16

### Added
- CI holds std's freestanding build to a checked-in list. `test/freestanding/verify.sh`
  builds every module for `freestanding-x86_64` and fails when a listed module
  stops building, when a module that builds is not listed, or when the list
  names a module that does not exist. The list starts at the 36 modules that
  build today (#684).
- `io.error.make(kind, operation)` builds an error std raised itself, with no
  native code behind it: `code` and `cleanup_code` are 0. A caller that needs a
  synthetic error states its kind here instead of borrowing an errno (#687).
- `io.error.Kind` gains `NOT_FOUND`, `EXISTS`, `NOT_DIRECTORY`,
  `IS_DIRECTORY`, `NOT_EMPTY`, `NAME_TOO_LONG`, `BUSY`, `IO`, `RANGE`,
  `NO_CHILD` and `LOOP`, numbered 15 to 25 after `OTHER`. Existing values keep
  their numbers. `from_code` does not produce the new kinds yet, so every code
  classifies exactly as before (#687).

### Changed
- CI follows the family contract in briar-systems/.github (briar-systems/mach#3447).
  One `ci.yml` calls the shared library pipeline and ends in a `gate` job. linux
  x86_64, windows x86_64 and darwin aarch64 run on every pull request into dev.
  arm64 linux, darwin x86_64, riscv64 under qemu and the cross-backend build run
  on pull requests into main, on a dispatch that names them, and on every
  release. Nothing runs on push. Each host's verifiers run from
  `.github/ci/verify.sh`, `mach fmt --check` now runs, and the compiler is the
  family's pinned mach release, 5.1.0 where CI used 5.0.0 (#699).
- `mach.toml` declares `windows-x86_64`, so std's own manifest builds its
  windows artifact. This needs mach 5.1.0 or later for the debug profile,
  which earlier releases refuse on windows (#699).
- The backend artifact checks call every libSystem import they name. mach 5.1.0
  binds only the imports a program can reach, so the darwin checks no longer
  saw `_fstat`, `_getentropy` and the process imports in a probe that never
  called them (#699).
- **Behaviour change.** A fixed-capacity sink in `std.format`, `std.derive`
  and `std.data.json` reports running out of room as
  `io.error.make(RESOURCE_EXHAUSTED, OP_WRITE)`. The kind is unchanged, but
  `code` is now 0 instead of the target's `ENOSPC` (#687).
- The allocator interface documents backend release failures as a negative
  backend native code rather than an errno (#687).

### Fixed
- **Security.** On Windows, an owner-only mode (no group or other bits, such as
  0600 or 0700) is now enforced. Files and directories created with such a
  mode, through `open`, `make_dir` and everything built on them
  (`filesystem.create`, `write_bytes`, `create_dir`, `replace_bytes_atomic`,
  transactions), get a protected DACL with one ACE granting only the current
  user, who is also made the owner. Before this, the mode was ignored and the
  object inherited its parent's default DACL, so other principals could read a
  0600 private key. A directory's ACE is inherited by what is later created in
  it, since Windows lets any principal traverse past a directory's own DACL by
  default (#703).
- **Security.** On Windows, `set_mode` and `set_mode_at` apply the same
  owner-only mapping instead of always returning `ENOTSUP`. Any other mode,
  including group or other bits and setuid, setgid or sticky bits, has no
  faithful Windows form, so it still returns `ENOTSUP` (kind `UNSUPPORTED`) and
  leaves the object unchanged. `set_mode_at` refuses a reparse point rather than
  following it (#703).
- On Windows, `stat` and `stat_path` report the mode an owner-only protected
  DACL enforces (for example `0600` or `0700`) instead of always reporting
  `0644` for files and `0755` for directories. Any other DACL still reports
  those defaults (#703).
- std now links `advapi32.dll` on Windows (#703).
- Transactional directory preparation widens an owner-denying directory to
  owner access while its children are built and restores the requested mode
  afterwards, on Windows as on other platforms. `filesystem.removal` likewise
  widens a private directory it has to descend into. Both steps used to be
  skipped on Windows, which would now leave a 0000 directory unbuildable (#703).

## [3.1.0] - 2026-09-16

### Added
- `std.simd.matmul`: exact widening integer dot products and matrix
  multiplication. `dot_i8`, `dot_u8`, `dot_i16`, `dot_u16` and `matmul_i8`,
  `matmul_u8`, `matmul_i16`, `matmul_u16` widen both operands to the
  accumulator's lanes before they multiply (i8 to i32x4, u8 to u32x4, i16 to
  i64x2, u16 to u64x2), since mach has no widening vector operator. A result is
  exact up to the `TERMS_*` bound for its element type, and a longer sum returns
  `Error.terms` instead of wrapping. Matrices are dense and row-major. i32 and
  u32 elements are not offered because no wider lane exists to accumulate them
  exactly (#390).
- `std.simd.reduce`: `dot_i32x4` and `dot_u32x4` (wrapping), and
  `hsum_i64x2` and `hsum_u64x2` (#390).
- `io.runtime.notify(runtime)`: wakes a blocked `wait` so it collects every
  source again without ending it. A source that queues completions off the
  native queue calls this instead of `wake`. `net.resolve` now does (#676).
- `io.runtime.WaitPlan.woken`: set when `prepare_wait` answers a caller's
  `wake`. Such a plan also has `wait` unset (#676).

### Changed
- **Behaviour change.** Only a caller's `io.runtime.wake` ends
  `io.runtime.wait` early. `wait` returns 0 only when its timeout has passed, a
  caller woke the runtime, or the runtime is closed with nothing left to
  return. The runtime's own wakes, such as the one a submission posts, no
  longer end a wait: it keeps waiting for the time that remains. This reverses
  the empty return #658 documented in 2.2.0. A return that carries completions
  also answers a pending wake. Callers that already loop on an empty return
  stay correct and now see fewer of them (#676).
- An external driver built on `io.runtime.prepare_wait` follows the same
  contract: a poll that comes back with nothing drained is not a reason to
  stop, so the driver prepares again with the time it has left and ends early
  only on a plan with `woken` set. `prepare_wait` consumes the caller wake it
  reports (#676).
- The `net.async`, `net.resolve` and `io.file` tests wait once where they used
  to retry an empty wait, so they exercise the contract directly (#676).

## [3.0.1] - 2026-09-16

### Fixed
- The native suite is green again on every platform, which is what failed the
  3.0.0 release workflow and left 3.0.0 unpublished. The local-socket and
  Windows accept tests still asserted that a third submission against a runtime
  or backend made at two is refused. #653 made that size initial, so the tests
  now assert that the submission grows the table and that every operation
  settles exactly once. The net.async accept, fairness and batching tests
  assumed that loopback bytes and handshakes are readable as soon as the send
  returns, and that a `wait` after a submission never comes back empty. darwin
  delivers loopback asynchronously, and a consumed submission wake ends a
  `wait`. The tests now tolerate both, and the fairness and batching tests
  still fail against the pre-#658 `wait` (#673). No library code changed.

## [3.0.0] - 2026-09-16

### Added
- `io.runtime.wait`'s batching is now covered by a test: one call may return a
  completion that was already queued together with one its own native collect
  produced, so a consumer must not act on a call carrying at most one completion
  per resource (#670). Nothing changed in the runtime; the behaviour was
  unasserted and a downstream consumer built on the opposite assumption.
- `memory.table`: chunked element storage whose live elements never move. A
  table appends a chunk to a fixed inline directory instead of reallocating, so
  an address handed out stays valid for the life of the table and only the
  index-to-address mapping has to be recomputed. `make`, `grow`, `reserve`,
  `at`, `index_of`, `destroy` and `aliases` (#653).
- `io.runtime.capacity(runtime)`: the slot table's current size, which is what
  the runtime has grown to rather than anything it was promised (#653).

### Changed
- **Breaking.** `io.runtime.make(runtime, initial)` takes an initial size, not
  a maximum. The slot, timer and source tables grow on demand and only memory
  bounds them, so a submission past the initial size grows the runtime instead
  of returning `RESOURCE_EXHAUSTED`. A server no longer has to know its peak
  concurrency at startup (#653).
- **Breaking.** `io.runtime.Runtime` no longer has a `capacity` field. Read the
  current size with `io.runtime.capacity(runtime)` and the size the runtime was
  made at with `runtime.initial`. `net.async.make` and `net.async.local.make`
  size themselves from `runtime.initial` and grow with the runtime (#653).
- Growth moves nothing a completion context or a caller holds a pointer to. The
  runtime's slots, timers and sources, the `net.async` drivers' slot, listener
  and stream tables, and every backend's operation, resource, completion and
  attachment tables are `memory.table`s: a growth appends a chunk and leaves
  every live element at the address it already had. A completion queued against
  a slot now lives in that slot and the queue links slots, so there is no second
  ring to size (#653).
- **Breaking.** The linux and unix backends' completion context is now a 16-bit
  source id, a 32-bit resource index and a 16-bit generation, in place of a
  16-bit source id, a 16-bit index and a 32-bit generation. The index no longer
  bounds the resource table at 65535 and `make` no longer refuses an initial
  size above `0xffff`. The narrower generation is what stale-completion
  detection costs: a resource index has to be recycled a multiple of 65535
  times between a context being orphaned and arriving for a stale completion to
  pass as live, where it was a multiple of 2^32. Generations are allocated
  inside the wire field, so the stored value and the encoded one are the same
  number and no comparison is made across a truncation (#653).
- The runtime and every backend harvest native readiness in fixed 256-entry
  batches and drain a full batch without blocking, rather than sizing the
  readiness buffer from the slot capacity. Source dispatch iterates registered
  sources rather than the whole slot capacity, and slot and operation claims
  take from a free list rather than scanning (#653).

## [2.2.0] - 2026-09-16

### Fixed
- `io.runtime.wait` collects native readiness without blocking on every call,
  before it returns ready completions, so a resource whose operations complete
  at submission no longer keeps `epoll_wait` from being reached and starves
  every other watched resource. A wake consumed by that collection still ends
  the call, so `wake` keeps interrupting the next `wait`. `io.runtime.prepare_wait`
  reports the same for an external driver: ready completions now yield a plan
  that polls with a zero timeout instead of one that declines to poll at all
  (#658).
### Added
- `std.allocator.heap`: a general-purpose size-class heap that reuses freed blocks and is safe to share between threads (#657). Small requests are carved from per-class spans with a free list per span, spans return to a cache every class draws from, and larger requests get a span of their own. Alignment is honored for every request, a resize stays in place while the block still fits and still uses half of it, and releasing a pointer the heap never handed out is refused with `-22` as `allocator.Error.release`. Backing memory comes from a `heap.Source`, with a native mapper member, an `Allocator`-backed member, and support for a grow-only source that can never return memory. No existing consumer's allocator changed.
- `io.writer.Buffered`, `io.writer.buffered`, `io.writer.flush` and `io.writer.pushed`: a writer that stages bytes in caller-owned storage and forwards full buffers to an inner writer, with an explicit flush, sticky failure and a request at or above the buffer's size passed straight through. `pushed` is the authoritative count of bytes the inner writer took, so a caller can report a true total after a staged pass (#654).
- `io.writer.reprefix`: the same `WriteError` with its persisted prefix replaced, for restating a failure against a count the caller measured itself (#654).
### Changed
- `format`: literal text between holes now reaches the writer as one call per maximal run rather than one per byte, and padding is written in chunks of up to 32 fill bytes rather than one byte at a time. Output is unchanged (#654).
- `print`: `printf`, `eprintf`, `printlnf`, `eprintlnf`, `println` and `eprintln` format into a 512-byte stack buffer and flush once before returning. A call whose output fits the buffer issues one write. Nothing is held across calls, so ordering and the interleaving of stdout and stderr are unchanged, and the reported byte count is the bytes that reached the fd (#654).

## [2.1.0] - 2026-09-13

### Added

- `log.record.field_text(key, data, len)`: a length-delimited text field rendered and escaped like `field_string`, for views that carry no terminator (#599).

## [2.0.0] - 2026-09-12

The breaking result, option and tag migration for Mach 5.0.0 (std #617,
#618). Every fallible or absent public outcome is spelled with the v5
canonical tags `res[T, E]`, `opt[T]` and `err[E]` declared in
`std.types.result`, `std.types.option` and `std.types.error`, with a closed
domain error tag per module in place
of strings, sentinels and optional-error returns. `MIGRATION.md` at the
repository root is the retained-surface inventory: the representation rules,
the frozen signatures per domain and the per-API tables. This changelog
names the surface by domain and does not repeat those tables. Compatible
additions after the v5 migration are assigned to std 2.1.0; 2.0.0 is the
breaking surface and the fixes that shipped with it. Compiler and std
version numbers are independent.

### Removed

- `std.types.result` and `std.types.option` (`Result`, `Option`, `Void`,
  `ok`, `err`, `ok_void`, `void_of`, `some`, `none`, `is_*`, `unwrap*`) and
  their `std` forwards. No compatibility export survives: the three canonical
  tags are the only outcome spelling, `sel place.case` is the test, the
  guarded payload place is the read and `Type.case{...}` is the construction.
  The compiler at mach `33d60001e` consumed nothing of the removed modules.

### Changed

- The canonical tags live in `std.types.result`, `std.types.option` and
  `std.types.error`, one module per tag; `std.types.canonical` is gone and
  a consumer spells `use std.types.result.res;`, `use std.types.option.opt;`
  or `use std.types.error.err;`. The module names reuse the names the
  removed legacy modules held; nothing in them is called `Result` or
  `Option`. `std.lib.libstd` forwards the three under their leaf names and
  `std.io.error` as `io_error` (std #617).
- **Breaking, by domain (Mach 5.0.0).** Each line names the domain and the
  `MIGRATION.md` section holding its frozen signatures and per-API table:
  - allocator, allocator backends and collections: `res[_, allocator.Error]`,
    `err[allocator.Error]`, `opt` for absence, `SearchPosition` for
    `binary_search`, backends and containers initialized in place
    ("Frozen core signatures": `std.allocator`, Allocator backends,
    Collections).
  - types and text foundations (`types.string`, `view`, `path`, `semver`,
    `text.string`): `StrError`, `SemverError`, `res`/`opt` constructors and
    searches ("Frozen core signatures": Types).
  - text, encoding, data and compression: `ParseError`, `FormatError`,
    `InputError`, `EncodeError`, `DecodeError`, `JsonError`, `TomlError`,
    `InflateError` with `Defect`, `Committed` and `Fault`; the gzip lifecycle
    settles a stored failure and refuses input after `finish` ("Text,
    encoding, data and compression (S2)", "Compression").
  - I/O: `ReadError`, `WriteError`, `StateError`; readers, writers, handles,
    the file adapter and the completion runtime return `res`/`err` over
    `io_error.Error` with retained descriptors and queued completions in the
    error ("I/O (S3a)").
  - filesystem: handle operations `res[T, io_error.Error]` or
    `err[io_error.Error]`, composite operations `res[T, FsError]` or
    `err[FsError]` with `published` for a replacement whose directory flush
    failed after the rename, `removal.Error` and `transaction.Error`
    ("Filesystem (S3b)").
  - process and network: `EnvError`, `exec.Error` with `retained` naming the
    unreaped child, `ip.ParseError`, the socket, local, async and resolver
    families over `io_error.Error` and `types.Error`, `lookup.Outcome` a tag
    ("Process and network (S3c)").
  - synchronization and clocks: `ThreadError`, `StateError`, `InitError`,
    `channel.Status[T]`, `worker_pool.Status`, `condition.WaitStatus` and
    `cancel.Reason` as tags, `time.Clock` `res[Time, io_error.Error]`
    ("Synchronization and clocks (S4a)").
  - crypto and random: `crypto.rand.fill` `err[io_error.Error]` with the
    completed prefix left in the buffer; hashes, `ct` and `rand` unchanged
    ("Crypto and random (S4a)").
  - terminal and logging: `TermError`, `SinkError`, `WriteStatus`,
    `EncodeStatus` and `ClockError` as tags, `WriteReport.error` and every
    `ERR_*` string gone, sinks initialized in place ("Terminal and logging
    (S4b)").
  - runtime and OS, math and SIMD: the native boundary (foreign ABI widths,
    native constants, negative errno, nil sentinels) is unchanged on purpose;
    `math.mat4.mat4_inverse` is `opt[Mat4]` ("Runtime and OS", "Math and
    SIMD").

- `std.types.result`, `std.types.option` and `std.types.error` declare
  `res[T, E]`, `opt[T]` and `err[E]` as ordinary std tags, one module per
  tag, and pin them to the language contract (case order, case codes, zero
  defaults, discriminator layout, reflection and nesting); the compiler
  seeds nothing (mach #3226, PR #3278).

- Linux local byte reads (`net.local.stream_read` and the local async backend)
  receive with `MSG_CMSG_CLOEXEC` and control storage sized for the kernel's
  descriptor bound, and close every right a peer attached, including after a
  native failure that followed installation. The generic Linux async backend
  refuses non-internet socket handles before registration, as Darwin's does.
  Completion queue wake on a closed queue is `EBADF` on Linux and Windows,
  matching Darwin. `std.system.os.linux.running_under_user_emulation` names
  a user-mode emulator the way `windows.running_under_wine` names wine.

- Directory root opening and descent preserve the primary failure and first
  cleanup error, consuming newly acquired descriptors on a failed advance.

- Process waits preserve complete Windows exit codes and explicit POSIX state
  observations. Typed wait failures retain native causes and unreaped child
  ownership. Windows cleanup retries keep process and group tokens valid.

- The eight `std.sync.atomic` wrappers (`load`, `store`, `cas`, `fetch_add`,
  `fetch_sub`, `exchange`, `fence`, `spin_hint`) are `#[inline]`: a release
  build folds each into its caller while retaining the instruction sequences
  and their memory-ordering effects (mach #3110, std #618).

- Linux and Darwin expose `O_NONBLOCK` through their file-open interfaces.

- Darwin local byte reads reject ancillary input before installing descriptor
  rights and retain socket ownership on refusal. Local async reads share that
  boundary. Generic Darwin async operations reject non-internet socket handles.

- Directory enumeration uses an explicitly owned cursor and borrowed entries on
  every backend. Darwin uses public fdopendir, readdir and closedir. Native record
  lengths govern delivery, with terminal errors and explicit cleanup. Filesystem
  directory collection and recursive removal retain primary and cleanup errors.

- Completion queue wake and close reject nil owners consistently on Linux, Windows
  and Darwin, preserving live wake and repeated-close behavior.

- Darwin completion queues use public kqueue and kevent with typed native storage,
  preserving event translation and descriptor cleanup. Wake and close reject nil queues.

- Gzip decodes complete concatenated streams. `finish` declares end-of-input and
  drains buffered output, with terminal completion only after every member verifies.
  Later corruption and trailing junk fail instead of returning prefix success.

- Darwin CPU discovery uses public sysctlbyname with hw.activecpu, returning the
  current active count instead of the boot maximum and retaining a minimum of one.

- Darwin ordinary entropy filling uses the public libSystem getentropy interface,
  preserving bounded chunks, immediate errors and the completed prefix on failure.

- Crypto and secret-storage tests use explicit typed declassification with the
  published Mach 4.30.0 compiler. The legacy spelling is removed from current source.

- Darwin virtual-memory primitives use typed public libSystem interfaces, preserving
  mapping ownership, native failure sentinels and heap publication ordering.

### Added

- A publication root can keep its transaction control files under a separate
  home (std #642, mach #3310): `filesystem.transaction.root_open_with_home`,
  `root_adopt_home` and `root_home_fd` place the lock sentinel, claims
  directory and backup container under the home instead of beside the
  destination, a child of a homed root is homed at `home/leaf`, and roots
  opened without a home are unchanged.
- Welded secret buffers persist and reload through the file completion
  adapter (std #550): `std.io.file.attach_secret_scratch`,
  `submit_secret_write` and `submit_secret_read` take `*^u8` plus a length on
  the public lane's requests, workers, cancellation settlement, partial
  progress and completions, with the read prefix landing in the caller's
  welded storage when its completion is dequeued and the scratch span wiped
  when the request retires. `std.system.os.secret` gains the borrow table
  (`Borrow`, `borrow_open`/`close`/`size`/`wipe`/`fill`/`drain`/`copy`,
  `borrow_read_at`/`borrow_write_at`, forwarded as `os.secret_borrow_*`): a
  welded pointer lent to an index-and-generation handle that is not an
  address, the one boundary where the pointer reaches the kernel. Design,
  per-outcome storage contents and wipe timing are in `MIGRATION.md`.

- `std.filesystem.FsError` (`io`, `alloc`, `read`, `write`, `removal`,
  `exhausted`, `published`), the domain tag of the composite filesystem
  operations, and `std.io.error.Error.cleanup_code`, the first cleanup failure
  observed beside a primary refusal.

- `std.types.string.OwnedString` with `owned_adopt`, `owned_dup` and
  `owned_release`: owned text that records its allocation extent, for producers
  whose buffer may be larger than the text it holds.

- `MIGRATION.md`, the std 2.0.0 retained-surface inventory: representation per
  public outcome-bearing API, the frozen foundation signatures, the corrections
  to the S0 census, the translation shims each later lane removes and what the
  lanes owe.

- The CI bootstrap chain gains the v5 migration compiler stage (mach
  `8464568d`, fixpoint) after the audited 4.30 stage, so std compiles v5
  syntax with a compiler it built from source.

## [1.0.2] - 2026-09-10

### Fixed

- The manifest declares explicit `debug` and `release` build profiles, so the
  Mach v5 compiler chain accepts the published 1.0.x line. Builds under the
  audited 4.30 compiler are unchanged.

## [1.0.1] - 2026-09-07

### Fixed

- CI rebuilds the audited compiler from published 4.26.5 and fixed source pins after withdrawal of the 4.30.0 release.

- Directory listing releases copied names and vector storage on enumeration or
  allocation failure, including a name awaiting vector growth. Its ownership
  documentation now requires callers to free each returned name before the vector.

## [1.0.0] - 2026-09-07

The audited standard library defines its stable public API under Semantic
Versioning 2.0.0. This major release includes the ownership and filesystem API
changes below. Mach 4.30.0 uses this API generation as its transition dependency.
The later breaking result/option/tag migration for Mach v5 will ship as std 2.0.0.

### Added

- Caller-journaled file commits retain originals under separately reserved backup
  claims and report partial rename effects, durability and cleanup errors without
  implicit rollback. Child roots and staged-child identity observations use held
  directory capabilities, including complete subtree staging for a new source root.

- Same-object preparation explicitly selects maximum prior access. Metadata-only
  remains the default. Read-authorized Darwin callers retain event-only references
  on supported local filesystems without reading content or changing permissions.

- Cooperative publication ownership primitives keep roots, locks and borrowers
  in final storage, reject copied owners, and exclude recovery while borrowers
  remain live. Fresh claim directories use native destination-name equivalence
  and admit work only after successful initialization. Sessions own stable
  destination claims before worker admission. Active transaction or mutation
  borrowers exclude simultaneous use without releasing the planned reservation
  (#583).

- Explicit filesystem identity observations preserve complete native identifiers
  and serialize one backend-qualified local representation. Windows identities
  retain the full 64-bit volume serial and 128-bit file ID without a pathname
  query, including while an unlinked object remains open. Unsupported
  identity domains remain distinct from presence and type observations.
  `filesystem.Metadata` no longer carries an implicit truncated identity.
  `identity_of` and `identity_link` query it explicitly, and portable watch
  scans retain the complete observation separately. Transaction entry probes
  report presence and type without identity queries, and explicit root, entry
  and staging identity APIs use the same complete representation. Rooted
  containment relies on nofollow opens instead of truncated identity checks
  between unretained observations (#583).


- `std.types.path.root` borrows an indivisible root prefix through the existing
  `std.types.view.View`, preserving native drive and UNC spelling without
  allocating or splitting the root (#608).

### Fixed

- Process tests use Darwin's installed `/usr/bin/true` and `/usr/bin/false`.
  Remove the five failure exceptions caused by the old nonexistent `/bin` paths.

- Windows file descriptors grow through stable pages instead of stopping at 256.
  Closed descriptors are reused, live wait addresses remain fixed during growth,
  and allocation failures preserve existing owners and report their actual error.

- Transaction preparation selects preconditions and durability before retaining
  any prior object or creating staging. Commit and abort consume final-storage
  transactions and release their active destination borrow on every path.
  Mutation helpers require the same planned Claim capabilities, recovery rejects
  live claims and workers, and failed recovery keeps admission closed (#583).
- Subtree preparation flushes file data through its original writable handles
  and completes directory modes and barriers in child-first order. Explicit
  directory modes apply even when files introduce their parents first. Private
  mode `000` trees remain abortable and recoverable without granting content-read
  access to files or changing public objects. Permissive durability reports every
  missing child barrier instead of allowing an outer directory flush to hide it
  (#612).


- Darwin grouped spawning gives the child sole authority to create its process
  group and waits for explicit readiness before exposing the PID. Concurrent
  launches no longer race two native group creators.

- Whole-file string reads reject unrepresentable sizes before allocation and
  release the exact buffer on read or close failure.

- The native Windows harness selects optimization level 0 without requesting
  unsupported COFF debug symbols. ELF and Mach-O debug runs retain symbols, and
  release ownership coverage remains at optimization level 2 (#615).

- Recursive removal shares a rooted nofollow walker with transaction cleanup.
  Windows force deletion removes read-only entries without changing surviving
  hardlink attributes on supporting filesystems. SMB read-only entries report
  unsupported, ordinary file removal remains strict, and root or dot removal
  requests are rejected before mutation (#613).

- Atomic byte replacement flushes the parent directory on Windows through the
  native NTFS durability backend. Unsupported directory persistence and flush
  failures remain errors after publication (#607).
- Windows rename atomically replaces destinations with open handles on
  supporting filesystems. Existing
  handles retain the old file while new opens see the replacement, through both
  public path operations and rooted filesystem publication. SMB retains its
  supported basic rename operation and refuses held destinations (#607).
- Path segment depth excludes Windows drive and UNC root units, including
  drive-relative paths and parent climbs below their anchor (#609).
- Windows process environments, executable names, arguments, working directories,
  and directory queries preserve UTF-8 through native UTF-16 APIs. Environment
  name comparison follows host identity and Windows blocks use native name order
  (#603).
- Filesystem transaction directory listing releases a copied entry name when
  vector growth fails, preserving exact allocation ownership under memory
  pressure (#605).
- Public filesystem Root opening and removal allocate each path component from
  its exact UTF-8 length and verify opened directory identities. Valid Unicode
  names are no longer rejected by a fixed byte buffer (#601).
- Subtree publication retains its held root after ancestor renames. Staged
  directories and files are created through directory descriptors, and staged
  symlinks cannot redirect inventory writes (#575). The subtree API and descent
  state no longer carry unused absolute path metadata.
- Filesystem transactions publish valid maximum-length destination names using
  short staging names and a persistent descriptor-relative backup directory.
  Recovery resolves only the requested destination, preserving other backups
  and malformed residue (#581).
- Publication rejects reserved journal and lock names with portable ASCII
  case-insensitive matching, preventing recovery from deleting published content
  under an internal name (#581).
- The OS boundary reports filename overflow as `ENAMETOOLONG` on every target,
  including Windows UTF-16 component validation (#581).
- Windows symbolic links preserve UTF-8 link names and relative targets through
  UTF-16 conversion. Target normalization and directory probing use the actual
  converted lengths instead of fixed byte buffers (#580).
- Windows filesystem transactions honor directory descriptors for publication,
  metadata, rename, directory creation, and removal. Operations use native
  handles and retain their root when its pathname is renamed or replaced
  (#574).
- Windows file creation, metadata, rename, and removal accept UTF-8 paths
  consistently with handle-based directory enumeration (#574).
- Windows directory enumeration remains attached to its open handle, preserves
  every entry across output-buffer boundaries, supports full Unicode component
  lengths, and supports rewind for
  transaction recovery and recursive cleanup (#574).
- Native Windows relative path components reject alternate-stream syntax and
  path separators. Metadata and deletion inspect reparse points without
  following their targets (#574).

## [0.37.2] - 2026-09-04

### Fixed

- TOML table cleanup stores the value in a local before taking its address,
  complying with Mach's refusal of addresses of call temporaries (#571).

## [0.37.1] - 2026-09-04

### Added

- `std.filesystem.transaction.root_remove_tree` removes a subtree through
  its root directory capability (#569).

## [0.37.0] - 2026-09-04

### Changed

- The producer callback passed to `std.filesystem.transaction.prepare` returns
  `Result[Void, str]`. Return an error to abort production. Callbacks returning
  `Result[bool, str]` must migrate to the new signature (#567).

## [0.36.1] - 2026-09-04

### Added

- `std.types.result.void_of[T, E]` discards a successful payload while
  preserving the error, adapting a result to `Result[Void, E]` (#565).

## [0.36.0] - 2026-09-03

### Added

- `std.types.result.Void` and `ok_void[E]` represent success without a
  payload (#563).

## [0.35.2] - 2026-09-02

### Fixed

- TOML parsing bounds nested values and reports excessive nesting rather
  than exhausting the stack (#561).

## [0.35.1] - 2026-09-02

### Fixed

- Darwin external imports explicitly name libSystem, whose exported manifest
  requirement uses `/usr/lib/libSystem.B.dylib` (#559).

## [0.35.0] - 2026-09-02

### Added

- Filesystem transactions provide staged publication, validation, commit,
  abort, recovery, root directory capabilities and contained entry operations
  (#557).
- Advisory whole-file locks support coordinating filesystem publishers (#557).
- The allocator fault harness can refuse a chosen allocation or reallocation
  to exercise failure cleanup (#557).
- Process supervision supports deadlines and reports spawn failures (#557).

### Fixed

- Process waits retry an interrupted wait instead of reporting failure (#557).

## [0.34.0] - 2026-09-01

### Added

#### system: deeply secret typed storage

- `std.system.os.secret_allocate_typed[T]` and `secret_deallocate_typed[T]`
  preserve the exact `*T` shape for records with deeply secret fields across
  allocation, complete typed-layout wiping, and native release (#553).
- Typed owners are zero-initialized and correctly aligned, including explicit
  over-alignment. Checked element and allocation geometry rejects overflow, and
  deallocation validates the original count before changing storage (#553).
- Native lifecycle and compile-refusal tests plus six-target debug and release
  IR and assembly gates cover Linux x86_64, aarch64, and riscv64, Darwin x86_64
  and aarch64, and Windows x86_64 (#553).

## [0.33.0] - 2026-08-28

### Added

#### system: secret-welded storage primitives

- `std.system.os.secret_allocate`, `secret_deallocate`, and
  `secret_random_fill` preserve `*^u8` from zero-initialized native allocation
  through failure-atomic entropy initialization and wipe-before-release without
  constructing a public pointer alias (#546).
- Linux uses direct native syscalls without libc, Darwin uses supported
  libSystem entry points, and Windows uses VirtualAlloc, VirtualFree, and
  BCryptGenRandom (#546).
- The existing Windows `std.system.os.random_fill` now uses checked,
  chunked BCryptGenRandom calls instead of a mismatched legacy BOOLEAN ABI
  declaration (#546).
- Native lifecycle tests, compile-time pointer-erasure refusals, and six-target
  debug and release IR and assembly gates cover the new boundary (#546).

## [0.32.0] - 2026-08-28

### Added

#### io: complete owned-region alias queries

- Maximum-address-safe public range validation, inclusive overlap comparison,
  and checked array-size calculation establish one fail-closed ownership
  vocabulary (#542).
- `std.io.runtime.aliases` covers the runtime descriptor and all completion,
  timer, source, and native-event allocations (#542).
- `std.net.async.aliases` and `std.net.async.local.aliases` cover driver state,
  every Linux, Darwin, Windows, and local backend allocation, and the borrowed
  runtime (#542).

### Changed

- Cross-backend probes now instantiate asynchronous network modules in debug
  and release with verified IR and emitted assembly (#542).
- Native CI runs ownership tests through the optimized pipeline on every
  supported architecture (#542).

## [0.31.0] - 2026-08-28

### Added

#### net: native DNS resolution on linux

- Native resolver modules under `std.net.resolve`: resolv.conf policy, hosts-file
  lookup, `/etc/services` names, an RFC 1035 wire codec with bounded
  decompression, RFC 6724 destination ordering, and nameserver transport with
  per-server timeouts, attempts, rotation, search-domain and ndots handling, and
  TCP fallback on truncation (#538).
- `udp.socket_set_recv_timeout` bounds blocking receives, matching the TCP
  stream surface (#538).

### Changed

- The linux resolver adapter composes numeric, RFC 6761 localhost, hosts-file,
  and DNS resolution natively; glibc `getaddrinfo` is no longer called, the
  linux libc link requirement is gone, and linux binaries are statically linked
  with no `PT_INTERP` (#538).
- `net.dns` reuses the resolver modules, gaining multi-nameserver retry and
  search-domain handling on its DNS path (#538).

### Removed

- The `[link.libc-*]` manifest entries, the CI libc sysroots and toolchain
  wrappers, and the `os.dns_nameserver` primitive on all targets (#538).

## [0.30.0] - 2026-08-28

### Added

#### process: whole-tree child termination

- `spawn_grouped` and `spawn_redirected_grouped` place a child in its own
  containment group at spawn; `Child.pgid` carries the group token and
  `terminate_group` signals the entire tree, so a child's own descendants no
  longer outlive its termination (#534).
- Unix backends use process groups: the child claims its group before exec, and
  the parent claims it again from its side, a double-set that also holds under
  emulators that downgrade vfork suspension. Darwin's real fork uses the same
  mitigation (#534).
- Windows uses a job object with kill-on-close, assigned while the child is
  created suspended and resumed only after assignment, so no grandchild can be
  spawned outside the job. The job handle closes exactly where the process
  handle closes, on reap (#534).

## [0.29.0] - 2026-08-27

### Added

#### io: a bounded production completion runtime

- Native resource handles and normalized I/O errors establish one ownership and
  failure contract across supported targets (#484).
- The operation-completion runtime provides bounded submission, completion
  dequeue, native source composition, monotonic timers, wakeups, hierarchical
  cancellation, and explicit close and drain behavior (#487, #488, #489, #495).
- Asynchronous file operations report transfer metadata and preserve buffer
  ownership through cancellation and teardown (#491).

#### net: transport-neutral asynchronous networking

- IP endpoints are dual-stack and transport-neutral, with atomic socket flags and
  production socket options (#485, #486).
- TCP and UDP use the shared completion runtime on Linux, Darwin, and Windows
  (#490).
- System name resolution is asynchronous, bounded, cancellable, and attached to
  runtime lifecycle ownership (#501).
- Local byte streams provide tagged filesystem and Linux abstract endpoints,
  managed listeners and streams, peer identity capabilities, owned path cleanup,
  and completion-driven operation across Linux, Darwin, and Windows (#502).

#### sync and process: reusable concurrent services

- Sleeping mutexes, conditions, semaphores, and once initialization avoid
  spin-based waiting (#492).
- Bounded channels and worker pools provide reusable backpressure and worker
  ownership contracts (#493).
- Portable process events expose termination and reload requests (#494).

#### encoding and output: transactional bounded writes

- Structured record output is atomic, so concurrent writers cannot publish
  partial records (#497).
- Bounded byte cursors and transactional builders preserve their position and
  output on failure (#498).

#### test and CI: deterministic native acceptance

- Deterministic I/O and allocation fault facilities exercise failure ownership in
  debug and optimized builds (#499).
- The complete runtime suite runs natively on supported Linux, Darwin, and Windows
  targets, with cross-riscv64 and cross-backend coverage (#500).

### Fixed

- Thread resources are reclaimed on every target, including process-local Windows
  rollback checks (#496, #520).
- Darwin asynchronous backend tests are completion-driven and close cancellation
  has deterministic ownership (#524, #527).
- The thread-resource fixture uses Mach's default project-local output path (#529).

## [0.28.2] - 2026-08-25

### Fixed

#### collections(vector): deinitialization clears released storage

`Vector.dnit` returned after releasing its allocation without clearing `data`,
`len`, or `cap`. A repeated call could therefore submit the same allocation for
deallocation again. Successful teardown now commits an empty descriptor, and a
regression test exercises repeated teardown.

## [0.28.1] - 2026-08-21

### Fixed

#### types(path): a cleaned path is freed to exactly nothing (#478)

`clean` worked in a buffer sized for its INPUT and returned it untrimmed, so a caller
freeing the result with `str_free` - which releases `str_len + 1` - returned less than
was taken and leaked the difference. Every other allocating function here reserves
exactly `str_len + 1`; cleaning cannot know its output length until it has produced
it, so the working buffer is now shrunk before it is handed back rather than making
this one return value the odd one out.

Caught by leak assertions one repo over (briar-systems/mach#3001), which is exactly
how far a size mismatch travels before anyone notices - so the new test asserts the
balance directly, through a counting allocator, on the inputs whose cleaned length
differs most from their input length.

## [0.28.0] - 2026-08-21

### Added

#### types(path): `clean` normalizes a path lexically (#472)

`path.clean(a, p)` collapses `.`, resolves safe `..`, squashes separator runs, and
emits the target's native separator - without touching the filesystem.

**Purely lexical is the contract, not a limitation.** Two spellings that clean to the
same bytes name the same path *as written*, which is the identity an editor overlay
needs: a compiler composes `<root>/./src/f.mach` from a manifest's `src = "./src"`
while the editor supplies `<root>/src/f.mach`, and the unsaved buffer is missed unless
those compare equal (briar-systems/mach#2998, briar-systems/mach-lsp#141). Resolving
symlinks is a different, I/O-bearing question.

The root is preserved and never climbed through - a POSIX `/`, a drive `C:\`, a UNC
`\\server\share` - so a `..` that would escape one is dropped. A **relative** path
keeps its leading `..`: there is nothing above it to cancel against, so `../a/../b`
cleans to `../b` rather than `b`.

Separators go in either way on Windows, where `/` and `\` both separate, and come out
native - which is what lets a compiler's forward-slash spelling and an editor's
backslash one meet at one canonical result.

An embedded NUL is not representable: `Path` is a null-terminated `str`, so a path
ends at its first NUL by construction and there is nothing to reject. Stated because
the question is a real one for a byte-oriented normalizer, and the answer is a
property of the type.

## [0.27.0] - 2026-08-20

### Added

#### data(toml): `dnit` releases a parsed table (#474)

`toml.parse` had no pairing. It allocates the table, its key copies, its string
values, and the backing arrays of every nested table and array, and nothing
returned any of it, so **every parse was a permanent allocation**. Invisible in a
one-shot process, unbounded in anything that parses twice: a retained compiler
session was growing ~7.4 MiB per manifest reload
(briar-systems/mach#3001), and the parsed table was 96% of it.

`dnit(a, t)` walks the tree once, releasing keys, value payloads, and both
parallel arrays, and resets the table to empty so a second call is a no-op rather
than a double free.

### Fixed

#### data(toml): table ownership is one rule instead of four (#474)

Three ownership defects sat behind the missing teardown, each of them a leak on
an ordinary successful parse.

**Growth stranded the buffer it replaced.** `table_set`, `array_push`, and
`keysegs_push` allocated a new array, copied into it, and reassigned the field
without releasing the old one, so every doubling leaked the previous array.

**Whether a key was adopted depended on the path taken.** `table_set` took
ownership of the caller's key when the key was new and stranded it on the
overwrite path; `table_ensure_subtable` stranded its key whenever the subtable
already existed. No caller could tell which had happened, so no caller could be
correct. **A table now stores a copy of its key**, which makes the rule sayable in
one sentence: the caller keeps and frees what it passed, always.

**The overwrite path stranded the value it displaced.** Setting an existing key
overwrote a `Value` that may own a string, a table, or an array, releasing none of
it.

`parse` and `parse_inline_table` are also restructured so the owned values live in
the caller and the walk below only reports failure. A parse that fails partway now
releases the partial tree on every error return rather than each new return having
to remember to - which matters for an editor, where a file being typed into is
invalid for most keystrokes.

The four new tests assert a **balance** rather than any particular call: parse and
tear down through a counting allocator and the allocator must end exactly where it
started, across repeated cycles, on a failed parse, and over a document that
overwrites the same key with each value kind.

### Added

#### process: spawned children can be force-stopped without being reaped (#470)

`std.process.exec.terminate_child()` forcefully stops one `Child` while leaving
its status available to `wait()` / `wait_any()`. The portable OS primitive uses
`SIGKILL` after a non-reaping child-ownership check on Linux and Darwin, and
`TerminateProcess` through the retained child handle on Windows. Unknown and
already-reaped children return `ECHILD` instead of falling through to a raw PID
operation that could affect a reused process ID. Termination and reaping of the
same child must be serialized; a concurrent wait could release that numeric ID
between POSIX's ownership check and signal delivery.

#### os: pipe writers can opt out of SIGPIPE termination (#468)

`std.system.os.ignore_sigpipe()` installs the process-wide ignored disposition
on Linux and Darwin, so subsequent broken-pipe writes from every thread return
`EPIPE` instead of terminating the process. Windows exposes the same portable
call as a successful no-op because its writes already report broken pipes as
ordinary errors.

## [0.26.1] - 2026-08-10

### Changed

#### log: lines carry an RFC 3339 timestamp, and the level loses its brackets

A log line was `[INFO] message`, which said when nothing about *when*. It is now `2026-08-10T14:03:21Z INFO message`: an RFC 3339 UTC timestamp from `std.chrono.time.now()`, then the bare level tag, then the message. The brackets are gone because the timestamp already gives the eye a fixed-width column to stop at, and two bracketed fields would fight it.

The timestamp is formatted through `std.chrono.format.rfc3339` rather than a private formatter, so the wire format tracks that one definition. If the clock read or the format call fails, the line still prints — level and message first, timestamp dropped — because a log line missing its timestamp is worth more than no log line.

## [0.26.0] - 2026-08-08

### Changed

#### darwin: the clocks and `sleep` go through libSystem (#415)

**darwin has no `clock_gettime` trap at all.** The backend called syscall 427 and read the result as a time; whatever that number is on current macOS, it is not one — `now()` came back *below the unix epoch*. The three `std.chrono.time` tests had been failing for as long as nothing was running them. `clock_gettime(3)` is public, has shipped since macOS 10.12, and is implemented in userspace over `mach_absolute_time()` and the commpage rather than as a trap, which is why hunting for a syscall number was never going to work. 10.12 is older than any macOS running on hardware these targets support, so this moves no deployment floor — unlike `os_sync_wait_on_address`, which is why the thread layer went a different way.

The `CLOCK_REALTIME` / `CLOCK_MONOTONIC` constants needed no change: they were always written against darwin's own `<time.h>` values, even while the call underneath did not exist.

**`sleep` moves to `nanosleep(3)`.** The note it carried — "darwin has no nanosleep syscall" — was true of the trap table and false of libSystem, so it went through `select` with a `timeval` timeout and lost sub-microsecond resolution on the way. It now also handles `EINTR` by resuming with the *remaining* time, so an interrupted sleep ends at about the requested moment instead of stretching towards double it. `rec timeval` and three more `SYS_*` constants go with it.

**A broken clock is not a clock that errors — it is one that returns a plausible-looking number**, so none of the seven new tests checks a return code. Each pins the clock against something independent: the epoch against a timestamp the *filesystem* just wrote (same kernel clock, completely different path), the unit against a measured 50ms sleep (which is what catches microseconds, milliseconds, or raw mach ticks), and `tv_nsec` against its documented range. Monotonicity is checked across 200 reads, and an unknown clock id is provoked for `EINVAL`.



#### darwin: threads are pthreads, not bsdthreads (#415)

`bsdthread_create` / `bsdthread_register` was never an ABI. `bsdthread_register` publishes a workqueue callback the kernel invokes, versioned against the libpthread that shipped with the OS — an internal kernel↔libpthread protocol this backend was impersonating. It is what #415 singles out as the most fragile code on the least stable part of the surface, and on current macOS it does not work: all three `std.sync.thread` tests were failing before this change, and had been failing unnoticed because nothing had ever run this suite on darwin.

**This had to come before the rest of the migration, not after it.** libSystem reaches errno through `__error()`, a thread-local resolved against the pthread structure libpthread installs for threads it created. A raw bsdthread never had one, because the start routine never performed libpthread's own `_pthread_set_self` handshake. Every libSystem call already migrated would therefore have carried an unvalidated errno path the moment it ran off the main thread. `pthread_create` makes every thread a real pthread and the question stops existing.

**pthread does not use errno, and that is the trap.** Every other libSystem entry point reports failure as `-1` and leaves the reason in errno. The pthread family returns the error number *directly* and leaves errno untouched, so the `if (rc < 0) { ret fail_errno(); }` shape used everywhere else is wrong twice over — the branch never fires, and if it did it would report an unrelated stale errno. The pthread wrappers negate `rc` itself and never call `fail_errno`.

**The OS-layer contract is unchanged; stack ownership moved.** `thread_spawn` still takes a caller-allocated region and a completion flag, and `thread_wait`/`thread_wake` are still address-keyed. The caller's region is now a *context block* only — pthread allocates and frees the real stack — which is exactly how the windows backend has always used it. The block is released by the new thread itself, so an unjoined thread still reclaims it, matching what `bsdthread_terminate` did. Threads are created **detached**, because joining waits on the completion flag rather than calling `pthread_join`, and a joinable pthread would leave its descriptor unreaped.

**The address-keyed wait is a table of condition variables.** darwin's futex equivalent, `__ulock_wait`, is as private as the bsdthread traps; the public replacement `os_sync_wait_on_address` is macOS 14.4+ and adopting it would quietly raise this library's deployment floor. So the wait is built from pthread condition variables in a fixed table hashed by address. Buckets are genuinely shared, and the consequences are handled rather than hoped away: `thread_wake` **broadcasts**, because a signal could hand the one wakeup to a waiter on an unrelated address; and the lost-wakeup race is closed by lock discipline, since the waiter re-reads the address under the bucket mutex that `pthread_cond_wait` releases atomically and that `thread_wake` must hold to broadcast.

Deleted with it: both hand-written `asm` trampolines (including the x86_64 stack-realignment fixup that existed only because the kernel *jumped* to the entry rather than calling it), the workqueue callback, and six `SYS_*` constants.



#### darwin: the filesystem layer calls libSystem instead of raw BSD traps (#415)

Apple does not guarantee syscall-number stability. `svc 0x80` / `syscall` works today and has been broken across macOS releases before, and libSystem is the only interface Apple supports. This moves the **filesystem and descriptor** primitives of the darwin backend onto it. Memory, time, process, sockets, threads, `read_dir`, and `terminal` still issue raw traps; see "what is deliberately left" below.

**The errno contract inverts, so every error path was re-derived rather than re-pointed.** A raw BSD trap sets the carry flag and returns the *positive* errno in the result register. libSystem returns `-1` (or `nil`) and leaves the errno in thread-local storage, reached through `__error()`. Two facts follow that the old code never had to encode:

- **errno is not cleared on success.** It may only be read once the return value has already reported failure. `fail_errno` is the single place the conversion happens and is only ever reached from inside a test of the documented sentinel.
- **the sentinel is per-function, not "negative".** `lseek` returns a file offset, and its failure value is exactly `-1`; testing the sign would be a different predicate that happens to agree today.

The layer's outward contract is unchanged — a count or descriptor on success, a negative errno on failure — so nothing above `std.system.os.darwin` moved.

**`open`, `fcntl`, and the apple arm64 variadic ABI.** `openat` and `fcntl` are C-variadic, and apple arm64 passes *every* variadic argument on the stack with no register phase. A fixed-arity declaration lowers `mode` into `x2` while libSystem reads it off the stack — which links, runs, and creates a file with the wrong permission bits. They are declared with mach's C-variadic `ext fun` form (briar-systems/mach#2575) and, where a call needs no tail, called with none: two-argument `openat` without `O_CREAT`, and `F_GETFD` / `F_GETFL`. Passing a dummy zero would not be an equivalent spelling on that target. Every tail this layer passes is an int, never a float, which keeps `AL` at zero on the SysV x86_64 leg.

**The stat family is arch-gated on `$INODE64`.** On x86_64 the plain `_fstat` is still the legacy 32-bit-`st_ino` struct and the 64-bit layout — the one `stat_t` describes — is reached through the `$INODE64` variant symbol. arm64 has only the plain name. Binding the plain name on x86_64 would link and run and quietly fill `stat_t` from a different field order, so the suffix is applied by an explicit gate and asserted in CI per architecture.

**Cancellation: the plain entry points, deliberately.** libSystem exports a `$NOCANCEL` twin for every cancellation point. std has no cancellation model, never calls `pthread_cancel`, and exposes no way to, so a cancellation point never acts and the plain entry point does exactly what its twin does — while remaining the public symbol. The decision is recorded in one place rather than left to whatever the linker resolves.

**Deletions.** `getcwd` was an `open(".")` + `fcntl(F_GETPATH)` dance with a `MAXPATHLEN` bounce buffer, because `F_GETPATH` carries no capacity and XNU writes up to `MAXPATHLEN` bytes whatever the caller sized its destination. `getcwd(3)` takes the capacity, so the scratch buffer, the copy loop, the `F_GETPATH` constant and `MAXPATHLEN` all go (#409, #413). The hand-written `pipe` asm in both arch modules — which existed only because the raw trap returns two descriptors in `x0`/`x1` and signals through the carry flag — collapses to one line, identical on both architectures. Fifteen `SYS_*` constants are gone.

### Added

#### CI runs the suite natively on both darwin architectures

There was no darwin execution anywhere in this repo's CI: `cross-backends` compiles the darwin backends from linux and runs nothing. The suite now runs natively on `macos-15` (arm64) and `macos-15-intel`, matching the reasoning already applied to the arm64 linux job — a psABI fact is exactly what an emulator or a cross-build can be wrong about.

The two rows are not interchangeable. The stack-passed variadic tail exists on apple arm64 and nowhere else, and the `$INODE64` suffix exists on x86_64 and nowhere else, so each divergence is invisible on the other row. CI additionally asserts that a linked darwin image names **exactly one** libSystem, at its install path — the implicit platform dependency plus a manifest entry spelled differently enough not to match it produces two `LC_LOAD_DYLIB` commands, which loads and runs and would otherwise go unnoticed.

Tests assert observable effects, not return codes: a file created with `O_CREAT` is stat'd back and its mode compared **exactly** (with the umask pinned to zero, so a dropped variadic argument cannot pass), `FD_CLOEXEC` is set and read back and cleared and read back, a pipe carries bytes end to end, `lseek` reports the size the writes produced, and the claimed error paths are provoked for their **specific** errno — `EEXIST`, `ENOENT`, `EBADF`.

### What is deliberately left, and why

This is a partial migration and the mixed state is intentional. `read_dir` needs `getdirentries64`, which is not public API on darwin; replacing it means an `opendir`/`readdir` redesign that changes the primitive's shape rather than just its callee. The thread layer's `bsdthread_create` / `__ulock_*` is the highest-value part of this issue and carries its own risk, and it interacts with everything else here — see the follow-up issue for the ordering question it raises.

## [0.25.1] - 2026-08-07

**Requires mach 4.14.0 or newer, and 4.13.0 will NOT build this.** `eq[f.type]` — the walk re-entering itself at a field's type — is a spelling mach did not accept before briar-systems/mach#2691, which landed on mach `dev` after 4.13.0 was tagged. On an older toolchain this is a **parse** error ("expected a module alias before `.`") reported against `src/derive.mach`, and because parsing precedes comptime evaluation the module's own `$mach.version` gate cannot fire ahead of it. That capability now exists: briar-systems/mach#2714 landed and shipped in mach 4.15.0, so `[project].mach` takes a semver minimum and is checked when the manifest is read, before any source is parsed.

**It is not adopted here yet, and the reason is the bootstrap.** The key is only understood by 4.15.0 and newer, so declaring it would move this library's floor to 4.15.0 in order to diagnose a 4.14.0 requirement, which trades a clear error on one old toolchain for a hard failure on a newer one. It becomes the right move once the floor rises to 4.15.0 for an unrelated reason. Until then the `$mach.version` gate states the requirement where `mach doc` finds it, and this note is what makes an old toolchain diagnosable.

### Changed

#### derive: the depth cap is gone, and the walk is recursion rather than a ladder (#449)

`std.derive` shipped as bounded structural descent four levels deep, with a comptime `$error` past the bound. That bound was never a design choice — mach could not re-enter a generic at a field's type, so the descent had to be a hand-written ladder, one nested `$each` per level per derive.

briar-systems/mach#2691 makes the recursive form spellable, and each of the five walks collapses to its own outermost level with the descent arm calling itself:

```mach
pub fun eq[T](a: *T, b: *T) bool {
    check[T]();
    $each f in $fields(T) {
        $if ($is_record(f.type)) {
            if (!eq[f.type](?a.[f], ?b.[f])) { ret false; }
        }
        $or (SCALARS) { if (a.[f] != b.[f]) { ret false; } }
        $or { }
    }
    ret true;
}
```

**This was a deletion, not a rewrite**, which is how the ladder was shaped: every level was the same arms over the same projection, so levels 2 through 4 came out of five functions and nothing else moved. `check[T]` recurses alongside the walk it guards.

**Behaviour is unchanged, and that is the evidence rather than the claim.** All 784 existing tests pass with **no edits**, including `fmt: four levels of nesting render every leaf` byte for byte. Four tests were added for six-level nesting, which was a comptime error before.

Two details preserve behaviour exactly:

- **`hash` threads its accumulator through the descent** (`fold_fields[T](h, v)`) rather than hashing each nested record on its own and combining. A nested field therefore contributes exactly the bytes a flattened one would, and the digest is identical to what the bounded walk produced. Hashing nested records separately would also have satisfied the eq/hash contract while silently changing every digest.
- **`fmt` splits the nested label from the nested value.** `write_label` writes `[, ]name=` and the recursive `fmt` call supplies `Type{...}`, which composes to the same `name=Type{...}` the per-level bracketing produced.

Termination is structural and needs no depth counter: a descent instantiates at a field's type, a record's fields are finite, and a record cannot contain itself by value. Note this does **not** extend to following references — `rec Grow[T] { p: *Grow[*T]; }` is legal and has unboundedly many instances reachable through its pointer, so a reference-following derive (briar-systems/mach#2693) needs a termination story this one gets for free.

### Fixed

#### derive: the module header described pre-4.13.0 behaviour (#449)

#450 corrected the four leaf `$error` messages for briar-systems/mach#2692 but not the prose above them, so the header still said the shape predicates strip `^`, still drew a contrast between type comparison and the predicates that no longer exists, and still described a `^`-wrapped record as "the one shape that escapes the classification" failing with a raw intrinsic error — which #450 had just made false. The header now states the rule once: **nothing strips `^`**, so `^u64` fails `f.type == u64` and `^Rec` fails `$is_record`, and both are refused by our own fallback.

#### os(windows): a symlink with a relative target was not traversable as a directory (#454)

`CreateSymbolicLink` stores the target verbatim as the reparse point's substitute name, and a **relative** substitute name is resolved by the kernel, which treats only `\` as a separator. Win32 path normalization, the layer that does accept `/`, never runs over reparse data. A `/`-separated relative target was therefore stored as one unresolvable component: creation reported success and every later read through the link failed, which is why `mach dep pull` looked fine and the next `mach build` did not. Paths are `/`-separated by contract above this layer, so `symlink` now rewrites the target to `\` at the syscall boundary. An over-long target is `ERANGE`, matching what this layer already does for a path too long.

The issue named a second candidate, the `SYMBOLIC_LINK_FLAG_DIRECTORY` flag going unset because the directory probe could not resolve a forward-slashed relative target. It is not live, and that is measured rather than argued: the rewrite reaches `CreateSymbolicLinkA` only, leaving the probe seeing the same `/`-separated target it always did, and the windows leg goes from failing to passing across exactly that change.

#### derive: the reference refusal blamed a compiler gap that has since closed

Three places said the walk stops at a reference because "mach has no `$pointee_of`". briar-systems/mach#2693 landed it, and mach 4.15.0 carries it. Checked against the release binary, `$pointee_of(f.type)` resolves inside a `$fields` walk. The refusal is unchanged and still correct, but the reason is now a semantic one and is stated as such: address semantics versus deep semantics is the caller's choice, and a deep walk allocates, so it needs an allocator argument and a failure mode these signatures do not have. Same for the note on the owning clone, which waits on a signature rather than on a capability.

Behaviour, refusal wording that `test/derive/verify.sh` pins, and the minimum toolchain are all unchanged.

### Tests

- `test/symlink` links a directory through a relative, `/`-separated target and reads a file **through** the link, and asserts `fs.is_dir` on the link. Creation succeeding is not the property: `fs.symlink` reported success on the bug, which is what made this look fine.
- A `windows-symlink` CI leg runs that probe on `windows-latest`. It is the first job in the family to create a symlink on a windows host, and every existing windows job is a cross-build hosted on linux, which is why this went unseen. Wine cannot stand in either: its filesystem is unix-backed, so it creates a genuine unix symlink and reports a false pass on precisely this bug.
- Six-level `eq` / `hash` / `clone` / `fmt` cases, each perturbing one leaf at a time at every depth, so a walk that stops short reports two different values equal.
- `test/derive/verify.sh` loses its depth-cap case, because the cap it pinned no longer exists, and its positive control now nests six deep rather than four. The other nine refusals are unchanged and still pass.

## [0.25.0] - 2026-08-07

**Requires mach 4.13.0 or newer.** `std.derive`'s recursive tier uses reflection primitives first shipped in 4.12.0, and its `^` handling tracks the shape-predicate change in 4.13.0 (briar-systems/mach#2692). The module checks `$mach.version` and says so, since `mach.lock` records dependency commits and cannot pin a toolchain.

### Added

#### `exec.resolve` / `exec.resolve_in` - one shared PATH lookup (#425)
No spawn entry point searches PATH: `execve` resolves nothing, and the windows layer passes a non-NULL `lpApplicationName`. Every caller spawning a program the *user* names had to hand-roll the same walk, and briar-systems/mach carried three copies of it.

`resolve` reads PATH; `resolve_in` takes the search list. The split keeps the policy pure, gives callers with their own list a way in, and makes the search testable at all - there is no way to set an environment variable in-process, so a test against the real PATH could only assert that some program somewhere resolved.

**The current directory is never searched.** An empty entry means cwd on both posix and windows and is skipped, which is the whole reason this is written rather than delegated to the OS: `CreateProcess` with a NULL `lpApplicationName` searches the working directory ahead of System32.

**Windows resolves a bare name through PATHEXT.** `git` is not a file, `git.exe` is, so a lookup that only joined the name would resolve nothing there.

- derive: **the walk descends into nested records** (#412). `eq`, `hash` and `fmt` used to refuse any field that was not a scalar numeric, so a record holding a `Vec3` could not be derived at all. They now walk a record-typed field's own fields, four levels deep, and `clone[T]` joins them. Requires mach 4.12.0, which first shipped `$fields(f.type)`, `$is_record` / `$is_union` / `$is_pointer`, and `$type_name`; the module checks `$mach.version` and says so, since `mach.lock` records dependency commits and cannot pin a toolchain.
- derive: **`check[T]` is the classification contract, written once and `pub`** (#412). Every derive calls it before its own ladder, so all four share one set of refusals and one set of messages, and a hand-written derive can hold itself to the same rule. Adding a derivable trait is now a ladder plus a leaf action, not a fresh set of refusals to get right.
- derive: **`clone[T](dst, src)`** (#412), a memberwise structural copy. The value of it over `dst = src` is the refusal rather than the copy: a field that a shallow copy would only alias does not classify, so `clone[T]` compiling is the proof that a structural copy is a whole copy.

### Changed
- derive: **`fmt` now prints the record's type name**, so `{x=1, y=2}` becomes `DV2{x=1, y=2}` and a nested field renders as `pos=Vec3{x=1, y=2, z=3}`. The spelling comes from `$type_name`, which is sema's own diagnostic authority, so a printed name and an error's name cannot drift.

### Known limits
- **This is bounded structural descent, not recursion, and the bound is four levels.** mach cannot re-enter a generic at a field's type — `eq[f.type]` does not parse, there is no inference from the argument, and `$type_of` is not a type operand — so each level of descent is a `$each` block someone wrote. Four is measured rather than rounded: across the 500 records in mach-std and the mach compiler the deepest by-value nesting is exactly four, reached only by `Loop` (`iv: InductionVar` → `init: Value` → `bytes: ValueBytes`) and `PcgWorker` (`sess: Session` → `registry: TargetRegistry` → `isa: IsaRegistry`); mach-std's own deepest is three. So the bound covers every record either codebase has, with the deepest sitting exactly on it. A deeper record is a comptime `$error` naming the bound and what to do about it. briar-systems/mach#2691 removes this, and lands as a deletion rather than a rewrite: each ladder collapses to its own outermost level with the descent arm calling itself.
- **Nothing here is secrecy-aware, and nothing can be**: the shape predicates strip `^` before answering, so no comptime surface can tell a walk that a field is secret (briar-systems/mach#2694). What keeps that from being silent is the scalar gate — type comparison does *not* strip `^`, so a `^u64` field fails `f.type == u64` and is refused at comptime rather than printed. A `^`-wrapped *record* field is the one shape the classification cannot catch: `$is_record` strips `^` and answers true, then `$fields` refuses the same operand (briar-systems/mach#2692). It still fails the build, so no secret is walked, but with mach's message rather than ours.
- **References are detected, never followed.** `$is_pointer` sees a reference but there is no `$pointee_of` (briar-systems/mach#2693), and address semantics versus deep semantics is the caller's choice, so a reference field is refused. `str` is `def str: *char`, so a `str` field is refused with the rest. An owning clone waits on the same capability.

### Tests

#### The library suite runs on riscv64 (#443)
No part of this suite had ever executed on riscv64: the leg ran a runtime smoke test and the RELRO contract only, and `mach.toml` declared no `linux-riscv64` target so `mach test .` could not target it. The compiler blocker (briar-systems/mach#2654) is fixed, and all tests now build and pass there.

qemu-user is real coverage for logic and a weak signal for ABI constants, and riscv64 has no native runner, so a riscv64-only result stays provisional. It would still have caught #436, whose defect was a wrong constant producing a hard `EINVAL`.

- `test/derive/verify.sh` — every refusal is a `$error` that fires during instantiation, so the evidence is a build that fails with a written message, which the in-process suite cannot express: a test binary that does not compile cannot run. Ten cases, one per shape and one per derive entry point, plus a positive control so the harness cannot pass on a project that never compiles. Wired into CI.
- The nesting tests perturb one field at a time at each of the four depths and assert the derive notices. That is the case that separates a real descent from a walk that stops at the first record and reports two different values equal, and each was confirmed to fail against a ladder with that level removed.

#### A `^` record is refused by our own leaf arm (#448)
mach 4.13.0 makes the shape predicates answer about the outermost constructor, so `$is_record(^SInner)` is false and a secret record field falls to `std.derive`'s leaf arm rather than classifying as a record and dying on `$fields`. The user-visible message is now our written explanation instead of a raw intrinsic error.

The refusal harness had deliberately pinned mach's raw message so exactly this change would be caught here rather than in a program's output. It was, on the first release carrying it.

## [0.24.2] - 2026-08-07

Corrects a regression in 0.24.1 that broke directory listing on aarch64.

### Fixed
- system: **arm swaps `O_DIRECTORY` and `O_DIRECT` relative to asm-generic, so aarch64 keeps `0o40000`** (#441). 0.24.1 unified the flag to `0o200000` on every linux arch on the strength of `asm-generic/fcntl.h`. That header defines both under `#ifndef` precisely so an arch can override, and arm does: `O_DIRECTORY` `0o40000` and `O_DIRECT` `0o200000`, the reverse of everyone else, inherited by aarch64. So the original arch gate was right about aarch64 and wrong only about riscv64. Both values are now stated with the reason, and the comment warns against unifying them again.

  Getting this backwards is not a compile error and not a wrong result: the open is refused `EINVAL`, so directory listing simply stops working on the arch that was guessed wrong. Both directions have now been observed on real hardware.

### Changed
- #439 is closed as a non-defect. `fs.read_dir` works on aarch64 with the correct constant, so the aarch64 gate 0.24.1 put on `read_dir:lists_children` is removed and the test runs on every arch again.

### Note
The native aarch64 CI leg added in 0.24.1 is what caught this, one release after it was introduced rather than silently. qemu-aarch64 had also been reporting it correctly all along; it was discounted because qemu-riscv64 disagreed, and both were right about their own arch.


## [0.24.1] - 2026-08-07

A wrong flag constant that made directory listing impossible on two of three linux arches, and the CI change that found it.

### Fixed
- system: **`O_DIRECTORY` is `0o200000` on every linux arch mach targets, not `0x4000`.** It was arch-gated, with aarch64 and riscv64 given `0x4000`, which is `O_DIRECT`'s value. Opening a directory with `O_DIRECT` is refused `EINVAL`, so `fs.read_dir` could not list anything on either. x86_64, aarch64 and riscv64 all take this flag from `asm-generic/fcntl.h`, so the gate was both wrong and unnecessary. Found when a riscv64 self-host build first enumerated a source tree for briar-systems/mach#2539 and reported `error: invalid argument` (#436).

### Changed
- ci: **the aarch64 leg runs natively on `ubuntu-24.04-arm` instead of under qemu-user** (#438). qemu-user does not faithfully model the kernel ABI here: its aarch64 target accepts `0x4000` as `O_DIRECTORY` and refuses `0o200000`, while its riscv64 target does the opposite and agrees with the kernel header. The two disagree with each other, so a qemu leg cannot be what decides whether the syscall surface is correct. mach's own int harness keeps its aarch64 leg native for the same class of reason (briar-systems/mach#1885).

### Tests
- `std.filesystem.read_dir:lists_children` — there was **no `read_dir` test at all**, which is the actual reason a broken directory listing on two of three linux arches survived. It asserts the children are listed and that `.` and `..` are not reported as children, so it checks the listing rather than that the call returned.

### Known broken
- **`fs.read_dir` does not work on aarch64** (#439). With the corrected flag the directory open is still refused `EINVAL` on real hardware, so the platform is broken independently of the constant. The new test carries an explicit aarch64 gate naming that issue; removing the gate is how the fix is verified. `os.read_dir`'s getdents64 handling is unverified on aarch64, since the open never succeeds and the loop has never executed there.


## [0.24.0] - 2026-08-07

Settles the OS-layer filesystem contracts that differed silently between backends. Every fix here is a case where the public docstring described one behaviour and at least one backend did another, and no caller in tree happened to notice.

### Fixed
- system: **`os.rename` on windows now replaces an existing destination.** It wrapped `MoveFileA`, which fails with `ERROR_ALREADY_EXISTS` whenever the destination exists, contradicting `fs.rename`'s own docstring and diverging from linux and darwin, which both call POSIX `rename(2)`. That broke the write-a-temp-then-rename-into-place pattern in exactly the case it is used in, and mach#2475 hit it across every writer that rebuilds an existing output. Now `MoveFileExA` with `MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH`. `MOVEFILE_COPY_ALLOWED` is deliberately not set, because POSIX `rename` fails across devices rather than silently copying and so should this. One divergence remains and is now documented rather than implied: `REPLACE_EXISTING` does not apply to a directory destination, so renaming a directory onto an existing empty directory still fails on windows where POSIX succeeds (#414).
- system: **`os.getcwd` on darwin no longer overruns a caller buffer.** It called `fcntl(F_GETPATH, buf)` and never looked at `size`. XNU receives no capacity for `F_GETPATH` and writes up to `MAXPATHLEN` bytes into the destination regardless, so any caller supplying a smaller buffer could be overrun even though the signature documents `size` as the capacity. The path is now read into a `MAXPATHLEN` scratch and copied out only when it fits, with a path too long for the destination reported as `ERANGE` the way linux reports it. `std.process.env.current_dir` supplies 4096 bytes, so nothing in tree was reaching it (#409).
- system: **`os.getcwd`'s return value meant two different things.** Linux passed the raw syscall's length through, which includes the terminator, while darwin and windows reported the string length. The docstring said "length of path" on all three. Linux now reports the path length, matching the other two and the wording. `current_dir` only tested `n <= 0 || n >= cap`, which is why an off-by-one in a documented length went unnoticed (#432).
- system: **`os.getcwd` on windows reported success for a call that wrote nothing.** `GetCurrentDirectoryA` overloads its return with the size *required* when the destination is too small, writing nothing, and the wrapper passed that through as a non-negative result. A caller that did not separately compare the result against its own capacity would read an untouched buffer and believe it held a path. It is now `ERANGE`, matching linux and darwin (#433).

### Changed
- `ERANGE` is now defined in the darwin and windows errno blocks, alongside linux's.
- `fs.rename`'s docstring states that an existing destination file is replaced, and that replacing an existing *directory* is not portable.

### Tests
- The `getcwd` capacity and length assertions are carried by **all three backends** rather than only the one they were written against. The os layer is target-gated, so each backend's tests run on its own CI leg; stating the same rule three times is what stops the three implementations diverging again, which is how every defect in this release arose.
- `fs.rename:replaces_existing_destination` asserts the destination carries the **source's** bytes rather than merely existing, so it cannot pass against a rename that quietly did nothing.

## [0.23.0] - 2026-08-07

Adds the shell-execution and working-directory half of the process surface, so a consumer never hand-assembles a shell invocation again, and fixes the darwin x86_64 entry under `--pie`.

### Added
- process: `std.process.exec.run_shell(command, cwd, envp)` — run a command through the host interpreter in a caller-supplied directory. **A command line's encoding is a property of the program being spawned**, so an argv-taking API has to pick a convention, and the CRT convention that `build_cmdline` picks is not the one `cmd.exe` implements: an embedded `"` becomes `\"` and cmd takes those bytes literally. Any caller assembling its own shell invocation therefore corrupts commands carrying quotes, which is how anyone writes a path containing a space. posix hands `sh -c <command>` straight to `execve`, so argv passes through with no encoding step to get wrong. windows resolves the interpreter from `%ComSpec%` and emits `"<comspec>" /s /c "<command verbatim>"`, where `/s` makes cmd strip exactly the first and last quote and keep everything between, so the caller escapes nothing (#424, PR #423).
- system: `os.spawn_in`, `os.spawn_redirected_in`, and `os.spawn_shell` on all three backends — spawn with an explicit child working directory. The chdir happens **in the child**, so the parent's cwd is untouched and the directory never enters the command line, which is what let a `cd <dir> &&` prefix corrupt it before. linux relies on `SPAWN_CLONE_FLAGS` omitting `CLONE_FS` so the child holds its own filesystem context; darwin forks, which copies it; windows passes `lpCurrentDirectory` (#422, PR #423).

### Fixed
- runtime: `std.runtime.darwin.x86_64` — the entry now selects its argument-block contract at compile time on `$mach.build.pie`, because **darwin x86_64 has two entry contracts and the image's load command picks which one is used**. A `--pie` image is emitted with `LC_MAIN`, which dyld CALLs like a C `main` (argc/argv/envp in `rdi`/`rsi`/`rdx`, `[rsp]` holding dyld's return address); a non-PIE image is still entered by the kernel with `LC_UNIXTHREAD` and the block on the stack. The entry only ever implemented the stack form, so under `--pie` it captured dyld's return address as `argc`, pointed `argv` one slot past it, and corrupted every `std.process.env` read. The selector is the same request bit the Mach-O writer gates `LC_MAIN` on, so the entry command in the image and the code at the entry cannot disagree. `aarch64` is untouched — arm64 darwin is always PIE and was already on the register convention (mach#2576, PR #421).
- README pointed at a `docs` directory that does not exist; the documentation lives in `doc` (external contribution, PR #413).

### Changed
- system: `std.system.os.darwin.shared.FCNTL_GETPATH` is now **`F_GETPATH`**, matching the name every other library uses for fcntl 50. A **breaking rename** for anything referencing the constant directly; `os.getcwd` is unaffected (external contribution, PR #413).
- The interpreter for `run_shell` is resolved explicitly and must stay that way. Passing the program through `lpCommandLine` with a NULL `lpApplicationName` would let `CreateProcess` search **the current directory before System32**, so a `cmd.exe` committed into a repository would win over the real one — binary planting via a hostile checkout, on tools whose job is building untrusted source. It would also make windows the only backend that searches at all, since `execve` resolves nothing. Callers needing a PATH lookup for a user-named program should do it explicitly and PATH-only (#425).

### CI
- The backend matrix now **cross-compiles the windows and darwin backends**, which were previously never built by CI — only linux was, so a target-gated module could break without any job going red. `test/backends/verify.sh` asserts the gated modules were genuinely compiled rather than silently skipped, so the job cannot pass vacuously (#426, PR #427).

### Verification
- 761/761 linux-x86_64 tests.
- CI green on build, cross-arm64, cross-riscv64, and the new cross-backends job.
- `run_shell` was **run**, not merely compiled, on windows: the child started in the requested directory, a quoted command round-tripped intact, and the parent's cwd was byte-identical after. Sabotaging the cwd path to pass `nil` fails the cwd test, and routing the identical quoted command through the CRT-convention encoder instead of `run_shell` fails where `run_shell` passes — a direct A/B on the defect.
- **Caveat:** that windows run was under **Wine 11.14, not real Windows**. A genuine-runner fixture is tracked on the mach side (mach#2587).
- The darwin entry fix was re-verified independently of its PR by building the backend smoke test both ways and reading the emitted image: `--pie` yields `cmd LC_MAIN` with a prologue that stores `rdi`/`rsi`/`rdx` RIP-relative, and no flags yields `cmd LC_UNIXTHREAD`. This release is the first in which CI compiled the darwin backends at all, via the new cross-backends job.
- **Caveat:** the non-PIE darwin x86_64 image is malformed in ways unrelated to this release — short `__PAGEZERO`, base one page low, and no section commands (mach#2599). The `--pie` path, which is what arm64 darwin and every `--pie` x86_64 build use, is unaffected.

## [0.22.0] - 2026-08-05

### Added
- compress: `std.compress.inflate` — DEFLATE decompression (RFC 1951) covering stored, fixed-huffman, and dynamic-huffman blocks. The decoder is a **resumable state machine** rather than a one-pass loop: every point at which it can run out of input or output is a state, so a huffman symbol, a match, or a code-length table may straddle a chunk boundary and resume on the next call. That is what lets a caller feed PNG IDAT chunks one at a time without concatenating them first. Back-references always resolve through a 32 KiB circular window rather than through the caller's output buffer, so output can be drained in pieces of any size; the window is the only allocation and comes from the caller's allocator. `decompress` drives the stream and reports `NEED_INPUT` / `OUTPUT_FULL` / `DONE` with bytes consumed and written; `finish` distinguishes a stream that ended from one that was cut short. `decompress_into` and `decompress_alloc` are one-shot conveniences over the same core (#416).
- compress: `std.compress.zlib` — RFC 1950 framing over the inflate core, validating the header and verifying the adler32 trailer. Preset dictionaries (`FDICT`) are rejected rather than silently ignored (#416).
- compress: `std.compress.gzip` — RFC 1952 framing over the inflate core, parsing the optional `FEXTRA` / `FNAME` / `FCOMMENT` / `FHCRC` header fields and verifying the header checksum when present, plus the crc32 and length trailer. One member is decoded; bytes after the first member's trailer are left unconsumed (#416).
- crypto: `std.crypto.hash.crc32` and `std.crypto.hash.adler32` — the checksums the wrappers need, both with a one-shot and an incremental surface. They sit beside `fnv1a` as non-cryptographic digests and are documented as error-detecting only. CRC-32 is a general module rather than a gzip-private helper because PNG chunk integrity needs it independently of gzip (#416).

Compression (deflate encoding) is deliberately not included.

## [0.21.0] - 2026-08-03

### Removed
- bmos: the `std.system.bmos` kernel API, `std.runtime.bmos` entry point, and the `std.system.panic` bmos arm (all added in 0.20.0). bmos support now lives in the external `mach-bmos` package, selected by the platform tag (`os=freestanding` + `platform="bmos"`, mach 4.4.0), so std no longer carries a parallel bmos arm. Unblocks removing `OS_BMOS` / `$mach.os.bmos` from the compiler (mach#2426).

## [0.20.2] - 2026-07-28

### Fixed
- system: `std.system.os.darwin.shared.getcwd` — replace the bogus `SYS___GETCWD` (304, which is actually `psynch_cvsignal` on XNU) with the correct libc-free approach: `open(".")` + `fcntl(F_GETPATH)` + `close()`. The previous implementation never worked on darwin; the buffer was never written to (#406, #2327).

## [0.20.1] - 2026-07-27

### Fixed
- system: `std.system.os.darwin.shared.getcwd` — return string length on success instead of 0 to match the cross-platform `os.getcwd` contract (#2327).

## [0.20.0] - 2026-07-26

Adds the `bmos` arm — support for [ReturnInfinity's BareMetal](https://github.com/ReturnInfinity/BareMetal) exokernel, whose compiler-side target shipped in mach 4.3.0.

### Added
- system: `std.system.bmos` — the BareMetal kernel API. BareMetal exposes no syscalls; its entire interface is a table of **fixed absolute addresses** called through indirectly (`b_output` at `0x100018`, and six siblings at an 8-byte stride). This module wraps all seven as named constants rather than raw bytes, which mach 4.3.0's `call [imm]` form (mach#2398) made expressible, plus the `b_system` sub-functions: `output`, `input`, `system`, `timecounter`, `shutdown`, `nvs_read`, `nvs_write`, `net_tx`, `net_rx`. The register moves follow `libBareMetal.c`; the convention is **not** SysV (PR #400, mach#2396).
- runtime: `std.runtime.bmos` — the `x86_64` entry point. BareMetal enters a program at the **first byte of a flat image** and expects it to `ret`, and it does two things a hosted loader would do that this kernel does not: it neither guarantees a 16-byte-aligned `RSP` nor zeroes `.bss`. `_start` is `#[naked]` (a compiler frame would sit between the alignment and the callee), parks the entry `RSP`, aligns it, calls `main(0, nil)`, restores and returns. The `.bss` half is handled in the compiler instead, by storing the flat image's zero-fill (mach#2402) (PR #400).
- panic: a `bmos` arm — writes the message through `b_output`, then enters a **halt loop**. Deliberately neither of the obvious alternatives: a plain `ret` would make this the only panic arm on any platform that *does not terminate*, returning into the failed program and looking to an operator exactly like a clean exit; `b_system`'s `SHUTDOWN` terminates but powers the machine off, taking the message with it. The loop rather than a bare `hlt` is required because interrupts are enabled and `hlt` resumes on the next timer tick (PR #400).

### Changed
- Both new modules gate their **declarations**, not merely their imports. `mach test` compiles every module on a linux build even where nothing imports them, so an ungated `_start` is a second definition of linux's — `multiple definition of '_start'`. darwin and windows avoid this only by spelling their entry `start` / `mainCRTStartup`; `bmos` shares linux's spelling (PR #400).

## [0.19.0] - 2026-07-25

Adds the constant-time crypto substrate, SHA-3, derive helpers, terminal/line input and the SIMD/float math follow-ups, and overhauls the string, io, filesystem, path and process surfaces. Panics now terminate deliberately on every supported OS instead of dying by trap.

### Added
- crypto: `std.crypto.ct` — constant-time primitives over `^` secrets, each `#[oblivious]`: `mask_*`/`select_*` masked branchless merge, `is_zero_*`/`eq_*`/`lt_*`/`gt_*` comparisons returning a secret 0/1 flag, `eq_bytes` whole-buffer compare with no early exit, `lookup_*` masked full-table scan replacing a secret index, `zeroize`, and `begin`/`end` for the hardware data-independent-timing mode. Comparisons use the language's own operators, which mach lowers branch-free on all three machine ISAs; the merges are masked arithmetic because no operator selects without branching. `begin` reports `false` on every target today — aarch64's `msr DIT` is not yet in mach's inline-asm surface (mach#2352), x86_64's DOITM is ring-0 only, and riscv64's Zkt has no mode bit (PR #391, mach-std#304, mach#1643).
- math: `std.math.float` — scalar floating-point roots and transcendentals in plain Mach: `sqrt_f32`/`rsqrt_f32` (Newton refinement) and `sin_f32`/`cos_f32`/`asin_f32`/`acos_f32` (range-reduced minimax/Taylor). Each public f32 entry evaluates in f64 and narrows, so the result is accurate to under one f32 ulp; no hardware sqrt/transcendental instruction is used, pending SIMD-capable inline-asm encoders (PR #389, mach-std#376).
- math: `quat_slerp` — true spherical linear interpolation over the shortest great-circle arc at constant angular velocity, on the new `acos_f32`/`sin_f32`; falls back to the normalized lerp for near-parallel inputs. `quat` now consumes the shared `std.math.float` roots instead of its private bit-seed `rsqrt` (PR #389, mach-std#376).
- simd: signed saturating add/sub — `adds_i8x16`/`subs_i8x16`/`adds_i16x8`/`subs_i16x8` in `std.simd.saturate` clamp to the type's `[MIN, MAX]`, detecting overflow in the mask domain and blending the saturated lanes with `select`. Adds `splat_i8x16`/`splat_i16x8` to `std.simd.shuffle` (PR #389, mach-std#376).
- derive: generic, macro-free derive helpers over `$fields` — `eq[T]` (structural equality), `hash[T]` (FNV-1a fold, `eq`-consistent), and `fmt[T]` (debug `{name=value, ...}`), each walking a record's fields at comptime via `$each`/`v.[f]`. Eligible fields are scalar numerics (integers of any width and floats, plus defs like `bool`/`char`); any other field type is rejected at comptime with a clear `$error` (PR #388, mach-std#285).
- terminal: raw single-key keyboard input for game loops — `enable_raw`/`disable_raw`/`is_raw`/`flush_input` mode control and `poll_key`/`poll_key_decoded` per-frame polling over a tagged `Key` type, with linux, darwin, and windows backends (PR #379).
- input: canonical stdin line input — `read_line`/`read_line_from` strip a trailing newline, null-terminate, and error on overflow rather than truncating silently (PR #379).
- crypto: SHA-3 family (FIPS 202) — Keccak-f[1600] permutation and byte-oriented sponge (`crypto/hash/keccak`), plus SHA3-256, SHA3-512, and the SHAKE128/SHAKE256 XOFs, each pinned to NIST known-answer vectors (PR #385).
- filesystem: the surface completed around the `std.io` reader/writer API, including `remove_dir` and a test suite (PR #380).
- format: `sprint` — an allocating formatter, which frees its buffer on a fill-pass error rather than leaking it (PR #380).
- encoding: an explicit-endianness binary encoder (PR #380).
- types: the `view` module (PR #380).
- path: `has_separator` and `seg_count` (PR #380).
- allocator: a fixed-buffer allocator (PR #380).
- net: TCP read timeout via `SO_RCVTIMEO` (PR #380).
- json: float members emitted through `field_f64` / `value_f64` (PR #380).

### Changed
- manifest: Re-touched the self-manifest to RFC-exact totality per mach#1964/mach#1979.
- **BREAKING** sync: thread userdata is threaded via `spawn_with`; callers passing userdata must move to the new entry point (PR #380).
- string: the module was overhauled for performance and a cleaner surface (PR #380).
- process: the env and exec layers are now allocating (PR #380).
- io: consumers realigned with the reader/writer API; the entry point moved to `src/lib/libstd.mach` and `io.buffer` was dropped (PR #380).
- memory: word-wide `raw_copy` / `raw_fill` / `raw_equal` (PR #380).

### Fixed
- panic: a panic terminated by executing `hlt`, a **privileged** instruction — in user mode that raises #GP, which the kernel delivers as SIGSEGV, so every internal error exited **139** and was indistinguishable from memory corruption at the shell. The three architectures did not even agree (aarch64 and riscv64 trapped to SIGTRAP, 133). Panics now `exit_group` with **255**, matching `std.system.os.abort()`, on linux x86_64 / aarch64 / riscv64 (PR #394, mach#2369).
- panic: `std.system.panic` dispatched as `$if linux { ... } $or { ...darwin... }`, so **"not linux" meant "darwin"** and a Windows build compiled darwin syscall numbers into the message write — a panic there printed nothing at all. The trailing terminator block was arch-gated with **no OS gate whatsoever**, applying `hlt`/`brk`/`ebreak` to every OS. Each OS now owns an explicit arm with a real Windows path over `GetStdHandle`/`WriteFile`/`ExitProcess`, and an unknown OS is refused at compile time instead of silently inheriting another platform's syscalls (PR #398, mach-std#397).
- os/darwin: the x86_64 `bsdthread` stack is aligned at the kernel entry point, establishing the stack-entry ABI contract (PR #377, mach#2104).
- string: `str_region_equals` no longer measures the haystack (PR #380).
- fs: `stat` mode width is normalized across platforms (PR #380).

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
