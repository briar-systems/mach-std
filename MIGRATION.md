# std 2.0.0 migration inventory: v5 `res`, `opt` and `err`

This is the retained-surface inventory for mach-std #617 (representation) and
#618 (ownership), S1 of the Mach v5 program. It records, for every public
module and every outcome-bearing public API, the deliberate representation
the API has or will have in std 2.0.0, which lane executes it, and which
signatures are frozen now so that S2 to S8 can start against them. It lives at
the repository root because `doc/` is the gitignored output of `mach doc`.

The per-function ledger is the S0 census in the compiler repository,
`doc/design/std-outcome-inventory.md` with `std-outcome-census.json`, taken at
std `ad7add30`. This document does not repeat those 1,806 rows. It fixes what
S1 executed, where S1's executed form corrects a census row and why, and what
each later lane owes against the frozen foundations. The language contract is
mach `doc/design/tagged-values.md`; the compiler pin is
`doc/design/migration-compiler-3218.md`.

## Pins

| | |
| --- | --- |
| migration compiler | mach `dev` `b4ab85122e30bb24d733a024d549a9a05ef1a2c2`, built by the 4.30.0 seed (generation A `a881f3c2`) or through std's own bootstrap chain (fixpoint `b1fe8a87`) |
| std base | `origin/dev` `c373e56` (std 1.0.2) |
| bootstrap chain | `.github/actions/setup-mach/bootstrap.py`: published 4.26.5, bridge `878a8f66` single, audited `b65afb97` fixpoint, v5 `8464568d` fixpoint (std pin `168a9f76` at every stage). `8464568d` is `9a15ac3a6` plus the seeding removal (mach PR #3278: the compiler no longer seeds `res`, `opt` and `err` and no longer refuses a module that declares them); `9a15ac3a6` is `b4ab85122` plus the darwin build fix (mach PR #3277, the pinned std does not forward `O_NONBLOCK` on darwin) and is language-identical |
| suite at this phase | 1216 passed, 0 failed under the v5 compiler `8464568d` on linux-x86_64 after S3b (1199 after S3a, 1208 after the two `feat/618` filesystem producer fixes landed, 1185 at S1 phase 2, 1182 at S1 phase 1 under `9a15ac3a6`, 1157 on the base under both the 4.30.0 seed and the v5 compiler) |

## Compiler facts every lane must know

- **The declarations of `res`, `opt` and `err` are std's; the compiler has
  none.** mach `8464568d` (PR #3278, mach #3226) seeds nothing and no longer
  refuses a module that declares the three names. `std.types.canonical`
  declares them `pub` exactly as the contract spells them and pins the shapes
  by test, and every consuming module has `use std.types.canonical.res;` and
  friends (`std.data.toml` and `std.net.resolve` also import the
  `std.types.result.err` helper, so they spell the tag `canonical.err[E]`
  until C5 deletes that helper). A module that names a canonical tag without
  the `use` fails to compile with `unresolved type name`, and a local binding
  named `res`, `opt` or `err` now shadows the tag in type position, which the
  seeded compiler hid.
- **A user generic instantiates over a canonical tag like over any other
  declared type.** `Vector[res[T, E]]`, `Map[K, opt[V]]`, `Holder[opt[T]]`
  and the like build and behave (the mangler defect noted on mach #3218 had
  a nil owner module because the tags were seeded; declared in std they have
  one). Tests pin it: `vector: elements of canonical tag type round-trip`,
  `map: values of canonical tag type round-trip` and
  `std.types.canonical: user generics instantiate over the canonical tags`.
  Nesting the canonical tags in each other works (`res[opt[T], E]`,
  `opt[res[T, E]]`), and a record field of canonical type works.
- Guards are lexical (contract "Payload places and guards"). The forms that
  bite during migration: an `or` arm is never guarded by the `if` arm's test,
  so `if (sel r.err) {...} or { r.ok }` is rejected, write
  `if (sel r.ok) { r.ok } or {...}`; `||` opens no guard; after an exiting
  chain the tested place is guarded for the rest of the block and **cannot be
  whole-assigned**, so a `var r` reused across a loop of pops must become a
  fresh `val` per iteration.
- `$is_tag` is comptime-only (a `$if` gate), and `$if` cannot appear inside a
  runtime `if` body.
- `sel` takes a place, never a call: `if (sel make(?r).err)` does not parse.
  Bind the outcome (`val made: err[E] = make(?r);`) or, in a test that only
  wants the yes/no, pass the value to a one-line predicate
  (`fun ok_err(r: err[E]) bool { ret sel r.ok; }`), which S3a does in
  `io.runtime`, `io.file.tests` and the runtime consumers. `||` opens no guard,
  so `if (sel r.err || r.ok != 1) { ret 1; }` is rejected even though every
  arm exits; split it into one `if` per term. A module that imports the
  `std.types.result.err` helper spells the tag `canonical.err[E]`
  (`use canonical: std.types.canonical;`).

## Representation rules

The contract and the S0 census fix the rules; this phase applied them to the
foundations. Later lanes apply the same rules to their modules.

| outcome | representation |
| --- | --- |
| fallible operation with a value | `res[T, E]`, `E` a closed domain tag, never `str` |
| fallible operation with no value (unit success, "optional error" today) | `err[E]` |
| genuine absence (empty container, no match, no element at an index, unset variable) | `opt[T]` |
| closed set of alternatives that are not failures | a named `tag` (`SearchPosition`) |
| an answer that is a real yes/no (predicate, changed/unchanged, inserted/updated) | `bool`, or `res[bool, E]` when the question can also fail |
| combinable flags, native constants, foreign status integers at a native boundary | unchanged integer or nominal scalar |
| owners | explicit manual ownership: the caller releases what it received; a container never destroys elements; a refused growth leaves the container as it was |
| address-bound owners (allocator state, cancellation scopes, lifecycle attachments, queued sinks, runtime registrations) | in-place `init(*T, ...) err[E]` into caller-owned final storage; never returned by value inside `res` |
| owned text whose extent may exceed its length | `std.types.string.OwnedString` |

A nil receiver pointer (`*Vector`, `*Map`, `*Allocator` inside a container) is
a contract violation of the same class as any nil dereference and is not an
outcome. The one place std reports it is the allocator interface itself
(`allocator.Error.invalid`), because that is the boundary every owner passes
through.

## S1 corrections to the S0 census

Each row was executed as written here. The census proposal is quoted so the
owner can rule; converting any row back to the census form is mechanical.

| census row | census target | executed | why |
| --- | --- | --- | --- |
| `allocator.zallocate` | `res[*T, *u8]` | `res[*T, allocator.Error]` | census slip, `allocate` in the same row set is `res[*T, allocator.Error]` |
| `allocator.deallocate_raw` | `err[allocator.Error]` | `err[allocator.Error]` | as proposed, with a nil pointer as ok and the backend status as `release` |
| collection growth (`vector.reserve/ensure/push`, `deque.push_*`, `heap.push`, `map.insert`, `set.insert`) | `res[usize\|bool, str]` | `res[usize\|bool, allocator.Error]` | the only failures are allocation and extent overflow, both cases of `allocator.Error`; a message string is the erasure the census prose forbids |
| `vector.pop`, `deque.pop_*`, `map.get` | `res[opt[T], str]` (invalid owner kept) | `opt[T]`, `opt[*V]` | a nil receiver is invalid use under the raw-memory rules, not an outcome; `heap.pop` in the same census is already `opt` for the same operation |
| `vector.get`, `deque.get`, `slice.get` | `res[*T, str]` (bounds failure kept) | `opt[*T]` | no element at an index is absence, the same class as an empty pop |
| `slice.set` | `err[str]` | `bool` | stored or out of range is the one condition and a real yes/no |
| `map.remove`, `set.remove` | `res[bool, str]` | `bool` | removal never allocates; the only error was the nil receiver |
| `bitset.init` | `res[Bitset, str]` | `res[Bitset, allocator.Error]` | by value as proposed (a Bitset is relocatable, not address-bound); the error is typed |
| `types.string` constructors | `res[str, str]` | `res[str, StrError]` with `StrError { alloc: allocator.Error; bounds; }` | a slice outside its string is distinct from the allocator's refusal |
| `types.path` constructors | `res[Path, str]` | `res[Path, allocator.Error]` | allocation is the only failure |
| `types.semver.semver_parse` | `res[Semver, str]` | `res[Semver, SemverError]` with `SemverError { empty; syntax: usize; alloc: allocator.Error; }` | the census prose asks parsers to keep invalid syntax, overflow and allocation distinct; `syntax` carries the byte offset |
| `collections.sort.binary_search` | `tag SearchPosition { found; insertion }` | `tag SearchPosition { insertion: usize; found: usize; }` | `insertion` is declared first so a zero-initialized position reads as absent at index zero, not as a match at zero |
| `text.string.str_free` | `err[allocator.Error]` | `err[allocator.Error]` | as proposed; `str_dup` returns `res[str, allocator.Error]` (the census says `res[str, str]`, the same erasure correction) |
| `OwnedString` | "S1 provides" | `std.types.string.OwnedString` with `owned_adopt`, `owned_dup`, `owned_release` | placed beside `str` and `StrError` in the S1 types module rather than in S2's `text.string` |

S3a executed its rows as tabled with these corrections:

| table row | table target | executed | why |
| --- | --- | --- | --- |
| `io.file.root_open` | `res[Root, io_error.Error]` | `root_open(root: *Root, path: Path) err[io_error.Error]` | a `Root` is address-bound: watches borrow `*Root` and admitted handle-relative work waits on its condition, so it is initialized in place like every other address-bound owner in the rules table |
| `io.reader.read` at the end of the stream | "EOF distinct" | `err{ReadError.eof{0}}`, never `ok{0}` for a nonzero request | a source still reports the end as zero bytes (the POSIX shape); `read` classifies it once, so no consumer branches on `ok{0}` |
| `io.writer.write` when the sink accepts nothing | not tabled | `err{WriteError.stalled{0}}` | the same classification for sinks; `write_all` no longer has to special-case a zero count |
| `io.runtime.destroy` refusals | "retained facts in the error" | `EINVAL` when the runtime is not closed or already destroyed, `EBUSY` when live operations, queued completions, a native controller or a registered source remain | the two refusals were both `EINVAL`; a caller that must drain before destroying can now tell them apart |
| `io.file.watch_close` | `err[io_error.Error]` | as tabled (was `bool`) | a never-opened watch is `EINVAL` on `OP_CLOSE` |

S3b executed its rows as tabled with these corrections:

| table row | table target | executed | why |
| --- | --- | --- | --- |
| `filesystem.create_dir`, `remove_file`, `remove_dir`, `rename`, `symlink`, `temp_close`, `temp_remove`, `temp_close_and_remove` | `err[FsError]` | `err[io_error.Error]` | one native effect has one cause; wrapping it in the composite tag adds a layer no caller can use (the `types.path` constructors set the precedent: allocation is the only failure, so `allocator.Error` is the type). `temp_close_and_remove` runs both effects and reports the close failure with the removal's code in `cleanup_code` |
| `filesystem.metadata`, `metadata_link`, `stat_of` | `res[T, io_error.Error\|FsError]` | `res[Metadata, io_error.Error]` | nothing allocates; `stat_of_error`, the typed twin of `stat_of`, is removed rather than kept as a second spelling |
| `filesystem.exists`, `is_file`, `is_dir`, `is_symlink` | `res[bool, io_error.Error]` | as tabled, with `ENOTDIR` a successful false beside `ENOENT` | a path through a regular file names nothing, which is the question asked; `EACCES` and `ELOOP` are refusals |
| `filesystem.Metadata.created` | not tabled | `opt[Time]` | the record's absence field is spelled canonically with the module |
| `filesystem.read_dir`, `read_string`, `read_bytes`, `write_bytes` after a complete transfer | not tabled | a close failure is the outcome (`io` on `OP_CLOSE`) and owns nothing | the bytes are not known to have reached the file; before, `write_bytes` and `read_bytes` discarded it |
| `filesystem.create_dir_all` | "cannot create directory" | the last creation's `io_error.Error` | the refusal exists and was being erased |
| `filesystem.transaction.prepare` `write_cb` | `R.Result[R.Void, str]` | `fun(*W, *m_writer.Writer) err[WriteError]` | a producer writes through the writer and its outcome is the writer's frozen tag (`format` and `derive` produce the same, S2); the transaction folds any error into `REJECTED` and reads the sink's own native code first, exactly as before |
| `filesystem.transaction.validate` `validator` | `R.Result[bool, str]` | `fun(*V, *u8, usize) bool` | false or an error were both `REJECTED`; the answer is a real yes/no |
| `filesystem.transaction.BackupOutcome.failure`, `cleanup_failure` | not tabled | `err[Error]` fields | the report's two independent outcomes, spelled as the module's unit outcome |
| `filesystem.transaction.ownership.initialize_claims` | unchanged `i64` | `err[removal.Error]` | `feat/618` `dac63cd` typed it (cursor and cleanup failures are two facts); landed as the canonical spelling. The other ownership operations stay native `i64` |
| `io.error.Error` | unchanged record | gains `cleanup_code: i64` | `feat/618` `dac63cd`: the first cleanup failure observed beside a primary refusal, zero when none; every existing construction stays valid and S3a's frozen consumers are untouched |

## S4a corrections to the S0 census

| census row | census target | executed | why |
| --- | --- | --- | --- |
| `sync.thread.join_result` | `err[ThreadError]` beside `join` | removed, `join` is the checked operation | two names for one operation once both are checked |
| `sync.once.run` | `err[InitError]` | `res[bool, InitError]` | the S1 table's form; the real "this call initialized" boolean is kept |
| `sync.once.InitFun` | (not in the census) | `fun(ptr) err[i64]` | the census prose requires the initializer's actual failure retained, which a bool cannot carry |
| `sync.cancel.finish`, `unregister` | `res[bool, StateError]` | as proposed, `ok{false}` meaning the completion hook owns the registration | the S1 table listed them under `err[StateError]`; the census row is the one with the real boolean |
| `sync.cancel.expire` | `res[bool, StateError]` | as proposed; a `destroyed` scope is the error, a scope with no deadline or a deadline not yet reached is `ok{false}` | |
| `sync.channel.Status` | a closed tag | `Status[T]`, generic over the element | the received element rides on the `received` case |
| `sync.worker_pool.Status` | a closed tag | as proposed, `spawn_failed` and `join_failed` carry the `ThreadError` | the census prose asks the pool to preserve native refusals; `last_thread_error` still returns the `i64` code, 0 when none |
| `sync.condition.WaitStatus` | a closed tag | `{ invalid; failed: i64; timed_out; notified; }` | a refused native wait keeps its code instead of collapsing into one failure case |
| `chrono.time.now`, `monotonic` | `res[Time, io_error.Error]` | as proposed, spelled `time.Clock`; the error is `from_code(code, OP_READ)` | |

## Frozen core signatures

"Frozen" means S2 to S8 code against exactly this and C1 pins the compiler's
consumers to it. Anything not in this table is a lane's to shape within the
rules above.

### `std.allocator`

| API | signature | frozen |
| --- | --- | --- |
| `Error` | `pub tag Error: u8 { exhausted; overflow; invalid; release: i64; }` | yes |
| `Allocator` | `rec { ctx: ptr; fn_allocate: fun(ptr, usize, usize) opt[ptr]; fn_reallocate: fun(ptr, ptr, usize, usize, usize) opt[ptr]; fn_deallocate: fun(ptr, ptr, usize, usize) i64; }` | yes |
| `allocate_raw` | `fun(a: *Allocator, size: usize, align: usize) res[ptr, Error]` | yes |
| `reallocate_raw` | `fun(a: *Allocator, p: ptr, old_size: usize, new_size: usize, align: usize) res[ptr, Error]` | yes |
| `deallocate_raw` | `fun(a: *Allocator, p: ptr, size: usize, align: usize) err[Error]` | yes |
| `allocate[T]`, `zallocate[T]` | `fun(a: *Allocator, count: usize) res[*T, Error]` | yes |
| `reallocate[T]` | `fun(a: *Allocator, p: *T, old_count: usize, new_count: usize) res[*T, Error]` | yes |
| `deallocate[T]` | `fun(a: *Allocator, p: *T, count: usize) err[Error]` | yes |

Contract: zero-size success is `ok{nil}` and asks no backend; a byte count that
does not fit `usize` is `overflow` before the backend is asked; a nil allocator
or an alignment that is zero or not a power of two is `invalid`; a refused
request is `exhausted` and changes nothing; a refused resize leaves the old
allocation owned by the caller; a release the backend refuses carries the
backend's negative status in `release`. The callbacks are the backend's
`some{ptr}` or `none{}`; the portable producer turns them into `Error`.

### Allocator backends

| API | signature | frozen |
| --- | --- | --- |
| `arena.init` | `fun(ar: *Arena, backing: *Allocator, cap: usize) err[allocator.Error]` | yes |
| `arena.make` | `fun(a: *Allocator, ar: *Arena) err[allocator.Error]` | yes |
| `arena.dnit` | `fun(ar: *Arena) err[allocator.Error]` (every chunk released, first refusal reported) | yes |
| `arena.reset` | unchanged | yes |
| `bump.make` | `fun(a: *Allocator, state: *BumpState) err[A.Error]` | yes |
| `fixed.make` | `fun(a: *Allocator, state: *FixedState, buf: *u8, cap: usize) err[A.Error]` | yes |
| `fixed.reset`, `fixed.remaining` | unchanged | yes |
| `page.make` | `fun(a: *Allocator) err[allocator.Error]` | yes |
| `testing.make` | `fun(t: *Testing) err[allocator.Error]` | yes |
| `testing.dnit`, counters, `fail_at_ordinal`, `clear_failure`, `leaked`, `tracking_exhausted` | unchanged (`dnit` returns the reclaimed count) | yes |

All backend initializers are in-place into caller-owned storage: the arena,
bump and fixed states are address-bound (the interface points at them).

### Collections

| API | signature | frozen |
| --- | --- | --- |
| `vector.init[T]` | `fun(a: *A.Allocator) Vector[T]` | yes |
| `vector.dnit[T]` | `fun(vec: *Vector[T]) err[A.Error]` | yes |
| `vector.reserve[T]`, `ensure[T]` | `fun(vec: *Vector[T], n: usize) res[usize, A.Error]` | yes |
| `vector.push[T]` | `fun(vec: *Vector[T], value: T) res[usize, A.Error]` | yes |
| `vector.pop[T]` | `fun(vec: *Vector[T]) opt[T]` | yes |
| `vector.get[T]` | `fun(vec: *Vector[T], index: usize) opt[*T]` | yes |
| `vector.is_empty[T]`, `clear[T]` | unchanged | yes |
| `map.init[K, V]` | unchanged | yes |
| `map.dnit[K, V]` | `fun(m: *Map[K, V]) err[allocator.Error]` (all three buffers released, first refusal reported) | yes |
| `map.insert[K, V]` | `fun(m: *Map[K, V], key: K, value: V) res[bool, allocator.Error]` (true inserted, false updated in place) | yes |
| `map.get[K, V]` | `fun(m: *Map[K, V], key: *K) opt[*V]` | yes |
| `map.remove[K, V]` | `fun(m: *Map[K, V], key: *K) bool` | yes |
| `map.contains`, `is_empty`, `length`, `capacity`, `clear`, hash and eq functions | unchanged | yes |
| `set.*` | mirrors `map`: `dnit` `err[allocator.Error]`, `insert` `res[bool, allocator.Error]`, `remove` `bool` | yes |
| `deque.dnit[T]` | `fun(dq: *Deque[T]) err[allocator.Error]` | yes |
| `deque.push_back[T]`, `push_front[T]` | `fun(dq: *Deque[T], value: T) res[usize, allocator.Error]` | yes |
| `deque.pop_back[T]`, `pop_front[T]` | `fun(dq: *Deque[T]) opt[T]` | yes |
| `deque.get[T]` | `fun(dq: *Deque[T], index: usize) opt[*T]` | yes |
| `heap.dnit[T]` | `fun(h: *Heap[T]) err[allocator.Error]` | yes |
| `heap.push[T]` | `fun(h: *Heap[T], value: T) res[usize, allocator.Error]` | yes |
| `heap.pop[T]` | `fun(h: *Heap[T]) opt[T]` | yes |
| `heap.peek[T]` | `fun(h: *Heap[T]) opt[*T]` | yes |
| `bitset.init` | `fun(alloc: *allocator.Allocator, nbits: usize) res[Bitset, allocator.Error]` | yes |
| `bitset.dnit` | `fun(bs: *Bitset) err[allocator.Error]` | yes |
| `bitset.set/clear/get/toggle/count/clear_all/set_all` | unchanged | yes |
| `slice.get[T]` | `fun(s: Slice[T], index: usize) opt[*T]` | yes |
| `slice.set[T]` | `fun(s: Slice[T], index: usize, value: T) bool` | yes |
| `sort.SearchPosition` | `pub tag SearchPosition: u8 { insertion: usize; found: usize; }` | yes |
| `sort.binary_search[T]` | `fun(data: *T, len: usize, target: *T, cmp: fun(*T, *T) i64) SearchPosition` | yes |
| `sort.swap/reverse/sort/is_sorted` | unchanged | yes |

Ownership: a pushed value is copied in and stays the caller's on refusal; a
popped value is copied out and its storage (if it owns any) is the caller's to
release; `get` borrows container storage and expires on growth, removal or
`dnit`; `dnit` releases the container's buffers only and never visits
elements; replacing an owning value in a map is `get`, release the old owner,
`insert`. A refused growth leaves the container exactly as it was, and a map
growth that is refused part way releases the buffers it acquired.

### Types

| API | signature | frozen |
| --- | --- | --- |
| `types.string.StrError` | `pub tag StrError: u8 { alloc: A.Error; bounds; }` | yes |
| `types.string.OwnedString` | `pub rec OwnedString { data: str; len: usize; extent: usize; a: *A.Allocator; }` | yes |
| `types.string.owned_adopt` | `fun(a: *A.Allocator, data: str, len: usize, extent: usize) OwnedString` | yes |
| `types.string.owned_dup` | `fun(a: *A.Allocator, s: str) res[OwnedString, A.Error]` | yes |
| `types.string.owned_release` | `fun(o: *OwnedString) err[A.Error]` (record owns nothing afterwards; a refused release leaves it owning) | yes |
| `str_copy`, `str_join`, `str_trim`, `str_trim_left`, `str_trim_right`, `str_to_lower`, `str_to_upper`, `str_repeat`, `str_replace` | `... res[str, StrError]` (extent is `str_len + 1`, released with `text.string.str_free`) | yes |
| `str_copy_slice` | `fun(a, s, start, len) res[str, StrError]` (`bounds` when the slice is outside `s`) | yes |
| `str_index_of`, `str_index_of_from`, `str_last_index_of`, `str_index_char`, `str_last_index_char` | `... opt[usize]` | yes |
| `str_find`, `str_find_last`, `str_find_char`, `str_find_last_char` | `... opt[str]` | yes |
| `str_len`, `str_empty`, `str_equals`, `str_region_equals`, `str_compare`, `str_starts_with`, `str_ends_with`, `str_contains`, `str_contains_char` | unchanged | yes |
| `types.view.view_index_char` | `fun(v: View, c: char) opt[usize]` | yes |
| `types.view.view`, `view_eq_str`, `view_contains_char` | unchanged | yes |
| `types.path.stem/clone/join/parent/resolve/clean` | `... res[Path, allocator.Error]` (extent is `str_len + 1`; `clean` shrinks to that extent and releases the working buffer on a refused shrink) | yes |
| `types.path` predicates and views (`separator`, `is_separator`, `root`, `has_separator`, `is_empty`, `is_abs`, `is_root`, `seg_count`, `filename`, `extension`) | unchanged | yes |
| `types.semver.SemverError` | `pub tag SemverError: u8 { empty; syntax: usize; alloc: allocator.Error; }` | yes |
| `types.semver.semver_parse` | `fun(input: str, a: *allocator.Allocator) res[Semver, SemverError]` (a prerelease copied before a refused build copy is released) | yes |
| `types.semver` predicates and `semver_compare` | unchanged | yes |
| `types.char`, `types.bool`, `types.size` | unchanged | yes |
| `text.string.str_dup`, `str_dup_range` | `... res[str, allocator.Error]` | yes |
| `text.string.str_free` | `fun(a: *Allocator, s: str) err[allocator.Error]` | yes |
| `memory.*` | unchanged (predicates and infallible effects) | yes |
| `types.canonical` | tests only until the compiler stops seeding; then the three declarations | yes |
| `types.result`, `types.option` (`Result`, `Option`, `Void`, `ok`, `err`, `ok_void`, `void_of`, `some`, `none`, `is_*`, `unwrap*`) | retained on the migration branch only; removed by C5 after S2 to S8 and mach #3226 | removal owed |

### I/O (S3a)

| API | signature | frozen |
| --- | --- | --- |
| `io.reader.ReadFailure` | `pub rec ReadFailure { delivered: usize; error: io_error.Error; }` | yes |
| `io.reader.ReadError` | `pub tag ReadError: u8 { eof: usize; would_block: usize; native: ReadFailure; alloc: A.Error; }` (every payload but `alloc` is the bytes delivered before the outcome) | yes |
| `io.reader.ReadFun` | `fun(ptr, *u8, usize) res[usize, ReadError]` (a source returns the bytes it delivered, `ok{0}` at the end of the stream, or its native failure; `read` classifies) | yes |
| `io.reader.read` | `fun(r: *Reader, buf: *u8, len: usize) res[usize, ReadError]` (`ok{0}` only for `len == 0`; the end of the stream is `eof{0}`; a native `WOULD_BLOCK` is `would_block{0}`) | yes |
| `io.reader.read_exact` | `fun(r: *Reader, buf: *u8, len: usize) err[ReadError]` (the payload carries the bytes delivered before the outcome) | yes |
| `io.reader.read_all` | `fun(a: *A.Allocator, r: *Reader) res[Vector[u8], ReadError]` (the caller owns the vector; on failure it is already released) | yes |
| `io.reader.read_str` | `fun(a: *A.Allocator, r: *Reader) res[OwnedString, ReadError]` (extent is the buffer's capacity, released whole by `owned_release`) | yes |
| `io.reader.native_failure` | `fun(delivered: usize, error: io_error.Error) ReadError` | yes |
| `io.writer.WriteFailure` | `pub rec WriteFailure { written: usize; error: io_error.Error; }` | yes |
| `io.writer.WriteError` | `pub tag WriteError: u8 { stalled: usize; would_block: usize; native: WriteFailure; }` (every payload is the persisted prefix) | yes |
| `io.writer.WriteFun` | `fun(ptr, *u8, usize) res[usize, WriteError]` (a sink returns the bytes it accepted, `ok{0}` when it accepts nothing, or its native failure; `write` classifies) | yes |
| `io.writer.write` | `fun(w: *Writer, buf: *u8, len: usize) res[usize, WriteError]` (`ok{0}` only for `len == 0`; nothing accepted is `stalled{0}`; a native `WOULD_BLOCK` is `would_block{0}`) | yes |
| `io.writer.write_all`, `write_str` | `... err[WriteError]` (the payload carries the persisted prefix) | yes |
| `io.writer.persisted` | `fun(error: WriteError) usize` | yes |
| `io.writer.native_failure` | `fun(written: usize, error: io_error.Error) WriteError` | yes |
| `io.lifecycle.StateError` | `pub tag StateError: u8 { invalid; closed; exhausted; active; inactive; stale; busy; }` (the state-machine domain tag: `sync.channel`, `sync.worker_pool`, `net.resolve.cancel` and `log.sink` import it; a lane needing a new fact appends a case) | yes |
| `io.lifecycle.make` | `fun(lifecycle: *Lifecycle) err[StateError]` (in place) | yes |
| `io.lifecycle.attach` | `fun(lifecycle: *Lifecycle, attachment: *Attachment) err[StateError]` (in place; `active` when already attached, `closed` past OPEN, `exhausted` at the counter's limit) | yes |
| `io.lifecycle.settle` | `fun(attachment: *Attachment) res[bool, StateError]` (true when this settlement completed the owner's close; `inactive`, `stale`) | yes |
| `io.lifecycle.settle_closed_child` | `fun(attachment: *Attachment, child: *Lifecycle) res[bool, StateError]` (`busy` while the child is not CLOSED) | yes |
| `io.lifecycle.begin_close`, `begin_process_drain`, `fail`, `snapshot` | unchanged | yes |
| `io.handle` | unchanged predicates | yes |
| `io.runtime.make`, `release_source`, `unregister_source`, `complete`, `complete_copy`, `complete_batch`, `fail`, `complete_cancellation`, `cancel_timer`, `begin_native_control`, `wake`, `destroy` | `... err[io_error.Error]` | yes |
| `io.runtime.retire_source`, `close` | `... res[bool, io_error.Error]` (already retired, already closed) | yes |
| `io.runtime.register_source` | `... res[SourceToken, io_error.Error]`; `submit*`, `submit_timer*` `... res[Token, io_error.Error]`; `poll`, `wait` `... res[usize, io_error.Error]`; `prepare_wait` `res[WaitPlan, io_error.Error]`; `begin_close` `res[lifecycle.CloseResult, io_error.Error]` | yes |
| `io.file.root_open` | `fun(root: *Root, path: Path) err[io_error.Error]` (in place) | yes |
| `io.file.root_close`, `replace_confined`, `mapping_sync`, `mapping_close`, `watch_close` | `... err[io_error.Error]` | yes |
| `io.file.open_confined`, `read_at`, `write_at`, `map`, `transfer`, `watch_open`, `watch_scan` | `... res[T, io_error.Error]` (`watch_open` answers whether the path exists) | yes |
| `io.file.adapter.make`, `destroy` | `... err[io_error.Error]` (in place; `destroy` is `EBUSY` with active requests) | yes |
| `io.file.adapter.submit_read`, `submit_write` | `... res[io_runtime.Token, io_error.Error]`; `shutdown_drain` `res[bool, io_error.Error]`; `shutdown_abort` `res[usize, io_error.Error]` | yes |
| `io.error.Error` | `pub rec Error { kind: Kind; code: i64; operation: Operation; cleanup_code: i64; }` (`cleanup_code` added by S3b from `feat/618`, zero when no cleanup failed) | yes |

Contract: a reader source or writer sink never spells `eof`, `stalled` or
`would_block` itself unless it wants to; it hands over bytes or a native
failure and `read`/`write` classify. A composite operation's error payload is
the whole prefix (`read_exact` after two partial reads reports the sum).
`read_all` releases its vector before reporting; `read_str` adopts the vector's
buffer whole. `WriteError` and `ReadError` are the domain tags the S2 and S4
consumers (`format`, `print`, `input`, `terminal`, `log`, `data.json`) import;
their shapes are frozen by this phase.

### Filesystem (S3b)

| API | signature | frozen |
| --- | --- | --- |
| `filesystem.FsError` | `pub tag FsError: u8 { io: io_error.Error; alloc: A.Error; read: ReadError; write: WriteError; removal: removal.Error; exhausted; published: io_error.Error; }` | yes |
| `filesystem.Metadata` | `pub rec Metadata { kind: Kind; size: usize; mode: u32; modified: Time; accessed: Time; created: opt[Time]; }` | yes |
| `filesystem.open`, `create` | `... res[File, io_error.Error]` | yes |
| `filesystem.close` | `fun(f: *File) err[io_error.Error]` (the handle is invalid afterwards whatever the outcome; a closed handle is `EBADF`) | yes |
| `filesystem.sync` | `fun(f: File) err[io_error.Error]` | yes |
| `filesystem.read`, `write` | `... res[usize, io_error.Error]`; `seek` `res[i64, io_error.Error]` | yes |
| `filesystem.identity_of`, `identity_link` | `... res[Identity, io_error.Error]`; `stat_of`, `metadata`, `metadata_link` `res[Metadata, io_error.Error]` | yes |
| `filesystem.exists`, `is_file`, `is_dir`, `is_symlink` | `fun(p: Path) res[bool, io_error.Error]` (`ENOENT` and `ENOTDIR` are `ok{false}`) | yes |
| `filesystem.create_dir`, `remove_file`, `remove_dir`, `rename`, `symlink` | `... err[io_error.Error]` | yes |
| `filesystem.read_bytes` | `fun(a, p) res[Vector[u8], FsError]`; `read_string` `res[str, FsError]` (extent `size + 1`; a shrunk file is `read{eof{delivered}}`) | yes |
| `filesystem.read_dir` | `fun(a, p) res[Vector[str], FsError]` (names owned by the caller, released whole on failure) | yes |
| `filesystem.write_bytes` | `fun(p, data, len, mode) err[FsError]` (`write` carries the persisted prefix) | yes |
| `filesystem.replace_bytes_atomic` | `fun(a, p, data, len, file_mode, dir_mode) err[FsError]` (`published{flush}` after the rename, every other case before it with the destination untouched) | yes |
| `filesystem.create_dir_all`, `remove_all` | `... err[FsError]` (`remove_all` refuses roots and dot names as `removal` with `containment`) | yes |
| `filesystem.temp_create` | `fun(a, prefix) res[TempFile, FsError]` (`exhausted` after `TEMP_MAX_ATTEMPTS`) | yes |
| `filesystem.temp_close`, `temp_remove`, `temp_close_and_remove` | `... err[io_error.Error]` (`temp_close_and_remove` runs both, close first, the removal's code in `cleanup_code`) | yes |
| `filesystem.reader`, `writer`, `temp_path`, `meta_*`, `identity_equal` | unchanged | yes |
| `filesystem.removal.Error` | `pub rec Error { code: i64; containment: bool; cleanup_code: i64; }` | yes |
| `filesystem.removal.tree`, `private_tree` | `fun(dirfd: i32, name: str, removed: *usize, max_depth: usize) err[Error]`; `with_cleanup` `fun(result: err[Error], code: i64) err[Error]` | yes |
| `filesystem.transaction.Error` | unchanged record (`kind`, `op`, `code`, `cleanup_code`) | yes |
| `filesystem.transaction` unit effects (`root_open`, `root_open_child`, `root_dnit`, `entry_rename`, `entry_rename_alias`, `entry_unlink`, `entry_rmdir_if_empty`, `lock`, `unlock`, `borrow_worker`, `release_worker`, `claim`, `release_claim`, `inventory_push`, `prepare*`, `validate`, `abort`, `descent_dnit`) | `... err[Error]` (owners initialized in place, as before) | yes |
| `filesystem.transaction` producers (`root_identity`, `entry_probe`, `root_remove_tree`, `entry_make_dir`, `transaction_staged_identity`, `transaction_staged_child_identity`, `commit`, `commit_replacing_owned`, `recover`, `descend`) | `... res[T, Error]` | yes |
| `filesystem.transaction.entry_identity` | `res[opt[Identity], Error]`; `entry_read_all` `res[opt[usize], Error]` | yes |
| `filesystem.transaction.inventory_dnit` | `fun(inv: *Inventory) err[allocator.Error]` | yes |
| `filesystem.transaction.prepare[W]` | `write_cb: fun(*W, *m_writer.Writer) err[WriteError]`; `validate[V]` `validator: fun(*V, *u8, usize) bool` | yes |
| `filesystem.transaction.BackupOutcome` | `failure: err[Error]; cleanup_failure: err[Error]` (other fields unchanged) | yes |
| `filesystem.transaction.commit_with_backup` | unchanged (`BackupOutcome` by value) | yes |
| `filesystem.transaction.ownership.initialize_claims` | `fun(held: *Lock) err[removal.Error]`; every other ownership operation native `i64` | yes |

Contract: a composite filesystem operation names the step that refused and
owns nothing on failure; a single native effect reports the native refusal
with its operation. A cleanup failure never replaces the primary refusal: it
rides in `io_error.Error.cleanup_code` (or `removal.Error.cleanup_code`) and
becomes the outcome only when nothing else failed. The transaction's lifetime
contracts (address-bound roots, locks, claims and workers; consumption of
every valid prepared transaction by commit or abort; recovery only under the
coordinator lock with no live claims) are unchanged; only the spelling of the
outcomes moved.

### Synchronization and clocks (S4a)

| API | signature | frozen |
| --- | --- | --- |
| `sync.thread.ThreadError` | `pub tag ThreadError: u8 { invalid; exhausted; unsupported; native: i64; }` | yes |
| `sync.thread.code` | `fun(e: ThreadError) i64` (`ERROR_INVALID`, `ERROR_NO_MEMORY`, `ERROR_UNSUPPORTED` or the native code) | yes |
| `sync.thread.spawn*`, `join`, `detach` | `... err[ThreadError]` (`Operation`) | yes |
| `sync.cancel.Reason` | `pub tag Reason: u8 { active; cancelled; timed_out; destroyed; invalid; }` | yes |
| `sync.cancel.StateError` | `pub tag StateError: u8 { invalid; destroyed; busy; }` | yes |
| `sync.cancel.Deadline` | `pub rec Deadline { at: time.Time; owner: *Scope; }` | yes |
| `sync.cancel.make_root`, `make_child`, `init_registration`, `destroy` | `... err[StateError]` (`Operation`) in place | yes |
| `sync.cancel.finish`, `unregister`, `cancel`, `timeout`, `expire` | `... res[bool, StateError]` (`Transition`, true when this call made the change) | yes |
| `sync.cancel.get_deadline` | `fun(scope: *Scope) res[opt[Deadline], StateError]` (`DeadlineQuery`) | yes |
| `sync.channel.Status[T]` | `pub tag Status[T]: u8 { invalid; sent; received: T; full; empty; closed; timed_out; cancelled; aborted; }` | yes |
| `sync.channel.StateError` | `pub tag StateError: u8 { invalid; destroyed; open; busy; }` | yes |
| `sync.channel.make[T]`, `destroy[T]` | `... err[StateError]` (`Operation`) in place | yes |
| `sync.channel.close[T]` | `fun(channel: *Channel[T]) res[bool, StateError]` (`Transition`) | yes |
| `sync.channel.try_receive[T]`, `receive[T]`, `receive_until[T]`, `receive_scoped[T]` | `fun(channel: *Channel[T], ...) Status[T]` (no output pointer) | yes |
| `sync.worker_pool.Status` | `pub tag Status: u8 { invalid; accepted; queue_full; pool_closed; timed_out; cancelled; spawn_failed: thread.ThreadError; draining; aborting; joined; join_failed: thread.ThreadError; joining; }` | yes |
| `sync.worker_pool.StateError` | `pub tag StateError: u8 { invalid; unjoined; busy; queue: channel.StateError; }` | yes |
| `sync.worker_pool.destroy` | `fun(pool: *Pool) err[StateError]` (`Operation`) | yes |
| `sync.condition.WaitStatus` | `pub tag WaitStatus: u8 { invalid; failed: i64; timed_out; notified; }` | yes |
| `sync.once.InitFun`, `InitError`, `run` | `pub def InitFun: fun(ptr) err[i64];` `pub tag InitError: u8 { invalid; failed: i64; }` `fun(o: *Once, ctx: ptr, init: InitFun) res[bool, InitError]` (`Outcome`) | yes |
| `sync.semaphore.StateError`, `init`, `release` | `pub tag StateError: u8 { invalid; overflow; }` `... err[StateError]` (`Operation`) | yes |
| `chrono.time.Clock`, `now`, `monotonic` | `pub def Clock: res[Time, io_error.Error];` `fun() Clock` | yes |
| `chrono.time.Elapsed`, `since`, `until` | `pub def Elapsed: res[Duration, io_error.Error];` `fun(t: Time) Elapsed` | yes |
| `crypto.rand.fill` | `fun(buf: *u8, len: usize) err[io_error.Error]` | yes |
| `EnvError` | owed by the lane that migrates `process.env` (the S3 table); S4a did not touch `process.env` | owed |

Every state-bound object (scope, registration, channel, pool, semaphore) is
initialized in place into caller-owned storage and never returned by value;
the operation's outcome is the only return. A refused transition leaves the
object exactly as it was, and the change/no-change boolean of a transition is
carried in `res[bool, E]` with the invalid-state refusals kept apart in `E`.

## Domain inventory

Lanes are the roadmap's: S2 value/text/codec, S3 I/O, filesystem, process,
network, S4 crypto/random, sync, clocks, terminal, runtime/OS, S5 to S8 the
Darwin, ancillary-rights, welded-secret-I/O and gzip programs. "S0 rule" names
the census rule that fixes the per-function target. "translation shim" marks a
call site where this phase converted a foundation refusal into the module's
legacy string (`"out of memory"`); the owning lane removes every one when it
migrates the module's own return types.

### Allocator (S1, done)

`allocator`, `allocator.arena`, `allocator.bump`, `allocator.fixed`,
`allocator.page`, `allocator.testing`: frozen above. Tests exercise both cases,
empty success, overflow before the backend, invalid use (nil allocator, bad
alignment), transfer by reallocate, replacement of an owning map value, a
failed release carrying the backend status, and cleanup (`leaked` after the
last release).

### Collections (S1, done)

`collections.vector`, `map`, `set`, `deque`, `heap`, `bitset`, `slice`,
`sort`: frozen above. Partial initialization is covered by the map growth test
(each of the three acquisitions refused in turn, nothing leaked, map unchanged)
and the bitset refusal test.

### Types (S1, done)

`types.string`, `view`, `path`, `semver`, `char`, `bool`, `size`,
`canonical`, plus `text.string` (owned `str` helpers) and `memory`: frozen
above. `types.result` and `types.option` remain for the unmigrated consumers.

### Text and encoding (S2)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `text.parse` | `parse_u64`, `parse_u64_exact`, `parse_i64`, `parse_i64_exact`, `parse_f64`, `parse_f64_len`, `parse_f64_exact` | `res[T, ParseError]` with invalid syntax and overflow distinct; no allocation | result-payload |
| `text.utf8` | `validate`, `is_continuation`, decoders | unchanged predicates and values | value-or-effect |
| `format` | `write_*`, `vformat`, `format` | `res[usize, WriteError]` carrying committed bytes and the writer cause (shared with `io.writer`, S3 owns the writer error type) | result-payload |
| `format.sprint` | | `res[OwnedString, FormatError]` or `res[str, FormatError]` with `alloc: allocator.Error` (translation shim at the `A.allocate` site) | result-payload |
| `print` | `print`, `println`, `eprint*`, `printf` family, `u64`, `eu64` | `res[usize, WriteError]` (checked printing stays checked) | result-payload |
| `input` | `read_line`, `read_line_from` | `res[usize, ReadError]` with EOF distinct from failure | result-payload |
| `encoding.binary` | `reserve`, `write_*`, `patch_*`, `align`, builder and reservation operations | `res[usize, EncodeError]` with `alloc: allocator.Error` and invalid-encoder distinct (translation shim at the `A.reallocate` site) | result-payload |
| `encoding.binary` | `read_*`, `skip`, `align_read`, `read_subview`, checkpoints and rollbacks | `res[T, DecodeError]` with short input distinct from malformed | result-payload |
| `encoding.binary.encoder_dnit` | | `err[allocator.Error]` | allocator-release |
| `encoding.base64`, `encoding.hex` | | unchanged (values and lengths) | value-or-effect |
| `data.json` | `parse`, `value_string_decode`, children/keys growth | `res[Value, JsonError]` with `alloc: allocator.Error`, syntax with position, and depth distinct; `value_*` predicates and numbers unchanged; a partial parse releases what it acquired (translation shims at the two growth sites) | result-payload |
| `data.json` streaming writer helpers | | `err[WriteError]` with the emitted prefix and writer cause | streaming-output |
| `data.toml` | `parse`, key and array growth, string decoding | `res[Table, TomlError]` with `alloc: allocator.Error` and positioned syntax distinct (translation shims at the growth and decode sites); `get_int`, `get_float`, `get_bool` stay `opt[T]` as absence-or-type-mismatch unless a checked accessor is added; `dnit` becomes `err[allocator.Error]` | result-payload, optional-value, allocator-release |
| `derive` | `eq[T]` unchanged; `fmt[T]` | `res[usize, WriteError]` | result-payload |

### Compression (S2 types, S8 lifecycle)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `compress.inflate`, `zlib`, `gzip` | `init` | `res[Inflater\|Decompressor, allocator.Error]` (the window is the only acquisition; translation shim at the window allocation) | result-payload |
| | `dnit` | `err[allocator.Error]` | allocator-release |
| | `decompress`, `finish`, `decompress_into`, `decompress_alloc` | `res[Progress, InflateError]` where a failure after progress carries the committed input and output counts; concatenated members, explicit EOF, sticky failure, truncation and CRC verdicts are S8's to preserve (translation shims at the `V.ensure` growth sites) | result-payload |
| | `is_done` | unchanged predicate | predicate-or-transition |

### Crypto and random (S4a, done)

| module | representation |
| --- | --- |
| `crypto.hash.*` (sha256, sha512, sha3, keccak, shake, crc32, adler32, fnv1a) | unchanged (S4a, not touched): values, states and digests |
| `crypto.ct` | unchanged (S4a, not touched): constant-time predicates and values; `begin` stays a bool meaning a hardware mode was engaged |
| `crypto.rand.fill` | done (S4a): `err[io_error.Error]` in place of the negative errno (`OP_READ`, the native code kept); the bytes written before the refusal stay in the buffer |
| `rand` | unchanged (S4a, not touched) values |

### Filesystem and I/O (S3)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `io.error` | `Error { kind; code; operation }` | unchanged record (done, S3a) | retained |
| `io.reader` | `read` | done (S3a): `res[usize, ReadError]` with EOF, would-block and native failure distinct | result-payload |
| | `read_exact` | done (S3a): `err[ReadError]` reporting the delivered count | optional-error |
| | `read_all`, `read_str` | done (S3a): `res[Vector[u8]\|OwnedString, ReadError]` with `alloc: allocator.Error`; the two `vector.reserve` shims are gone | result-payload |
| `io.writer` | `write` | done (S3a): `res[usize, WriteError]`; `write_all`, `write_str` `err[WriteError]` carrying the persisted prefix | result-payload, optional-error |
| `io.handle`, `io.lifecycle` | predicates unchanged; `make`, `attach`, `settle`, `settle_closed_child` | done (S3a): `err[StateError]` or `res[bool, StateError]` per the state-transition rule, address-bound attachments initialized in place | state-operation |
| `io.file` | `root_open`, `open_confined`, `map`, `transfer`, `watch_*`, `read_at`, `write_at` | done (S3a): `res[T, io_error.Error]` and `err[io_error.Error]` for unit successes; `root_open` in place (correction above); `watch_close` `err[io_error.Error]` | result-payload |
| `io.file.adapter`, `io.runtime` | every `Result[bool, io_error.Error]` | done (S3a): `err[io_error.Error]`; token-returning submits `res[Token, io_error.Error]`; `close`, `destroy` keep retained-descriptor and queued-completion facts in the error (`EINVAL` versus `EBUSY`) | result-payload |
| `io.file.posix`, `io.file.windows` | native `i64` | unchanged native boundary (done, S3a) | native-boundary |
| `filesystem` | `open`, `create`, `read`, `write`, `seek`, `identity_of`, `identity_link`, `stat_of` | done (S3b): `res[T, io_error.Error]` (`stat_of_error` removed, correction above) | result-payload |
| | `close`, `sync` | done (S3b): `err[io_error.Error]` | optional-error |
| | `read_bytes`, `read_string`, `read_dir`, `temp_create` | done (S3b): `res[T, FsError]` with `alloc: allocator.Error` distinct; `stat_of`, `metadata`, `metadata_link` `res[Metadata, io_error.Error]` (correction above); the 16 translation shims are gone | result-payload |
| | `write_bytes`, `replace_bytes_atomic`, `create_dir_all`, `remove_all` | done (S3b): `err[FsError]`; a failure after publication is `published` (the directory flush after the rename is the separate effect) | optional-error |
| | `create_dir`, `remove_file`, `remove_dir`, `rename`, `symlink`, `temp_close`, `temp_remove`, `temp_close_and_remove` | done (S3b): `err[io_error.Error]` (correction above) | optional-error |
| | `exists`, `is_file`, `is_dir`, `is_symlink` | done (S3b): `res[bool, io_error.Error]`: a path that names nothing (`ENOENT`, `ENOTDIR`) is a successful false, a native failure is the error | filesystem-query |
| `filesystem.removal` | `tree`, `private_tree` | done (S3b): `err[Error]`; `with_cleanup` folds a cleanup failure beside the primary | optional-error |
| `filesystem.transaction` | every `O.Option[Error]` | done (S3b): `err[Error]`; `root_identity`, `entry_probe`, `commit`, `commit_replacing_owned`, `recover`, `root_remove_tree`, `descend`, `entry_make_dir`, the staged identities `res[T, Error]`; `entry_identity`, `entry_read_all` `res[opt[T], Error]`; `inventory_dnit` `err[allocator.Error]`; the writer callback `err[WriteError]` and the validator `bool` (corrections above); Roots, Locks, Claims, Workers keep their stronger lifetime contracts; the two translation shims are gone | result-payload, optional-error |
| `filesystem.transaction.ownership` | native `i64` | done (S3b): unchanged except `initialize_claims` `err[removal.Error]` (correction above) | native-boundary |

### Process and network (S3)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `process.env` | `get` | `res[opt[usize], EnvError]`: missing is `none`, the length excludes the terminator | environment-buffer |
| | `value` | `res[opt[OwnedString], EnvError]` with the read-again race bounded and reported (`changed`) and the owned extent preserved (translation shims at the `A.allocate` and `str_copy` sites) | environment-owned |
| | `current_dir` | `res[OwnedString, EnvError]` with native and allocation failure distinct | environment-owned |
| | `compare_names` | `res[i32, EnvError]` keeping native Unicode comparison failure | environment-order |
| `process.exec` | `run`, `run_shell`, `output`, `spawn*`, `wait`, `wait_any`, `wait_within`, `resolve`, `resolve_in` | `res[T, Error]` where `Error` is `feat/618`'s typed record (unreaped child, detail, native code, operation, secondary wait failure); `try_wait` `res[opt[ExitStatus], Error]`; `terminate_child`, `terminate_group` `err[Error]`; `ExitStatus` keeps the full 32-bit Windows code and POSIX exit/signal/stop distinctions (translation shims at the `str_copy`, `str_join`, `str_copy_slice` and `path.join` sites) | result-payload, process-poll |
| `process.events` | `next` | `res[opt[Event], io_error.Error]`; `wait` `res[bool, io_error.Error]`; `make`, `make_runtime`, `close` `err[io_error.Error]` | event-poll, event-ready |
| `net.ip` | `ipv4_parse`, `ipv6_parse`, `addr_parse`, `endpoint_parse` | `res[T, ParseError]`; predicates unchanged | result-payload |
| `net.socket`, `net.tcp`, `net.udp`, `net.local`, `net.local.endpoint`, `net.async`, `net.async.local` | every `Result[bool, io_error.Error]` | `err[io_error.Error]`; value results stay `res[T, io_error.Error]`; completion lifetimes and retained descriptors survive in the error | result-payload |
| `net.async.linux`, `darwin`, `windows`, `net.async.local.unix`, `net.async.local.windows`, `net.local.unix`, `net.local.windows` | native `i64` | unchanged native boundary | native-boundary |
| `net.resolve` | `make*` | `err[types.Error]`; `submit`, `submit_runtime` `res[Token, types.Error]`; `cancel` `res[bool, StateError]` (whether it changed the reason); `close`, `destroy`, `resolution_destroy` `err[types.Error]` keeping live resolution storage on failure | resolver-operation |
| `net.resolve.shared` | `destroy`, `allocate_endpoints`, `set_canonical`, `append_unique`, `deduplicate` | `err[types.Error]` with `alloc: allocator.Error` distinct; `error` still constructs an error value; `valid`, `within_limits`, `canonical_fits` unchanged predicates | resolver-operation |
| `net.resolve.lines` | `open` `err[io_error.Error]`; `next` `res[opt[usize], io_error.Error]` (EOF is `none`, the full line length on success); `close` surfaces cleanup failure | resolver-lines |
| `net.resolve.service.lookup` | `res[opt[u16], types.Error]`, output pointer removed; `numeric`, `scan_line` unchanged | service-lookup |
| `net.dns` | `lookup_hosts`, `query`, `resolve` | `res[bool, types.Error]` with the existing output pointer | resolver-query |
| `net.resolve.conf`, `hosts`, `linux`, `darwin`, `windows`, `wire`, `lookup`, `order` | | per the census: `Outcome` becomes a tag, wire parsing stays a predicate with `Parsed` status, config loading surfaces read/close failure | closed-value, retained |

### Synchronization (S4a, done)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `sync.atomic` | `load`, `store`, `cas`, `fetch_add`, `fetch_sub`, `exchange`, `fence`, `spin_hint` | done (S4a): unchanged values; the eight `#[inline]` annotations landed (`ad7add3` cherry-picked); elimination proven below | atomic-inline |
| `sync.mutex` | `try_lock`, `is_locked` | done (S4a): unchanged predicates | predicate-or-transition |
| `sync.channel` | `Status[T]` | done (S4a): a closed tag generic over the element; `send*`/`receive*`/`close_abort` return it with the element on `received` and the output pointer removed; `make`, `destroy` `err[StateError]` in place; `close` `res[bool, StateError]` (true closed it now) | closed-value, state-transition |
| `sync.worker_pool` | `Status` | done (S4a): a closed tag; `make*`, `submit*`, `close_*`, `join`, `shutdown_*`, `state` return it, `spawn_failed` and `join_failed` carry the `ThreadError`; `destroy` `err[StateError]` nesting the queue's refusal; `last_thread_error` keeps the `i64` code (0 when none) | closed-value |
| `sync.cancel` | `Reason` | done (S4a): a closed tag; `make_root`, `make_child`, `init_registration`, `destroy` `err[StateError]` in place (scopes and registrations are address-bound); `finish`, `unregister`, `cancel`, `timeout`, `expire` `res[bool, StateError]` (the real changed boolean, `destroyed` kept apart); `get_deadline` `res[opt[Deadline], StateError]` with the output pointers removed | deadline-query, state-transition |
| `sync.condition` | `WaitStatus` | done (S4a): a closed tag, `failed` carries the native code | closed-value |
| `sync.once` | `run` | done (S4a): `res[bool, InitError]` (true ran the initializer, false already complete) retaining the initializer's failure code; `InitFun` returns `err[i64]` | state-transition |
| `sync.semaphore` | `init`, `release` | done (S4a): `err[StateError]` (`invalid`, `overflow`); `try_wait` unchanged predicate; counts unchanged | state-operation |
| `sync.thread` | `spawn*`, `join`, `detach` | done (S4a): `err[ThreadError]` decoding native errors without narrowing (`native: i64` keeps the code, `code()` round-trips it); `spawn`, `spawn_with` and `join` are checked, `join_result` is removed; `Thread.tid` still carries the failure code so a moved handle stays diagnosable; `diagnostic_id`, `is_done` unchanged | thread-operation |

### Clocks (S4a, done)

| module | representation |
| --- | --- |
| `chrono.time.now`, `monotonic` | done (S4a): `time.Clock` = `res[Time, io_error.Error]`; `since`, `until` `time.Elapsed` = `res[Duration, io_error.Error]`; a failed clock is never zero time. Consumers with an error channel propagate the clock's `io_error.Error`; a deadline pre-check with no channel skips the check on failure and leaves the deadline to the native timed wait |
| `chrono.time` comparisons and components, `chrono.duration`, `chrono.date`, `chrono.format` | done (S4a): unchanged values and predicates |

### Terminal (S4)

| module | representation |
| --- | --- |
| `terminal`, `terminal.linux`, `terminal.darwin`, `terminal.windows` | `enable_raw`, `disable_raw`, `flush_input` `err[TermError]`; `poll_key` `res[opt[Key], TermError]` (no key is absence, native read failure is the error); `is_raw` unchanged |
| `terminal.key` | unchanged predicates and `Key` |

### Logging (S4)

| module | representation |
| --- | --- |
| `log`, `log.sink` | `WriteReport` retained with offered, persisted, suppression, truncation and failure; convenience functions return it; `logger`, `make`, `custom`, `from_writer`, `console`, `file`, `pipe`, `queued*` `res[Sink\|Logger, SinkError]` with queued sinks initialized in place (address-bound); `queued_close_*`, `queued_join`, `queued_destroy` `err[SinkError]` preserving undelivered records and thread failure |
| `log.record` | unchanged values; `EncodeStatus` becomes a closed tag. S4a touched only the clock consumers: `system_now` reads `time.now()` and keeps the log clock's existing zero-time convention for an unreadable clock (the same one `clock_now` applies to an invalid clock), and `log.log_msg` stamps through `record.clock_now`; S4b decides whether `NowFun` reports the clock's refusal |

### Runtime and OS (S4a portable done, S5 Darwin)

| module | representation |
| --- | --- |
| `system.os`, `system.os.linux.*`, `system.os.darwin.*`, `system.os.windows.*`, `system.os.shared`, `system.os.secret`, `system.os.darwin.libsystem` | done (S4a, not touched): unchanged native boundary: foreign ABI widths, native constants, negative errno and raw calling conventions; the portable producers above decode them. `allocate`, `deallocate`, `reallocate`, `secret_allocate`, `secret_deallocate` keep nil and `i64` |
| `system.file_identity` | done (S4a, not touched): unchanged predicates and values |
| `system.panic` | done (S4a, not touched): unchanged |
| `runtime`, `runtime.linux.*`, `runtime.darwin.*`, `runtime.windows.*` | done (S4a, not touched): unchanged native entry and relocation boundary |
| `system.os.tests` | done (S4a): in-tree census tests; no call site needed migration |

### Math and SIMD (S2)

| module | representation |
| --- | --- |
| `math`, `math.bits`, `math.float`, `math.quat`, `math.bignum` | unchanged values and predicates |
| `math.mat4.mat4_inverse` | `opt[Mat4]` (a singular matrix is mathematical absence) |
| `simd.select`, `reduce`, `shuffle`, `saturate`, `gather` | unchanged values |

## Translation shims left by this phase

Every site where a foundation refusal is turned into a module's legacy
message. The owning lane removes them when it migrates the module's own return
types; none is a final form. Counted by `"out of memory"` strings added in this
phase (33 sites over 15 modules):

| module | sites | lane |
| --- | ---: | --- |
| `filesystem` | 0 (16 removed by S3b) | S3 |
| `data.toml` | 8 | S2 |
| `data.json` | 4 | S2 |
| `compress.inflate` | 3 | S2/S8 |
| `process.exec` | 2 | S3 |
| `process.env` | 2 | S3 |
| `format` | 2 | S2 |
| `filesystem.transaction` | 0 (2 removed by S3b) | S3 |
| `encoding.binary` | 1 | S2 |
| `compress.zlib`, `compress.gzip` | 1 each | S2/S8 |
| `net.resolve`, `net.resolve.shared` | 0 (typed `types.Error` and `bool` already) | S3 |

The `system.os.*` hits of that string are the OS layer's own native
messages, not shims.

S3a removed `io.reader`'s two and, because the reader, writer, lifecycle and
runtime signatures changed under their consumers, left typed-outcome shims of
the same class: each consumer keeps its legacy carrier and spells the typed
outcome as its old message or status. The owning lane removes them with the
module's own return types:

| module | shim | lane |
| --- | --- | --- |
| `filesystem`, `filesystem.transaction` | removed by S3b (`FsError.read`/`write` carry the reader and writer tags whole; the transaction's writer callback returns `err[WriteError]`) | done |
| `process.exec` | `file_exists` around `filesystem.is_file` (a query the platform cannot answer reads as absent) | S3c |
| `process.exec` | `read_error_text` around `read_all` in `output` | S3c |
| `process.events`, `net.async`, `net.async.local`, `net.resolve` | `runtime_ok_*` predicates and `res`/`canonical.err` bindings at every `io_runtime` call; `net.async.wait` and `process.events.begin_runtime_drain` re-wrap the runtime's `res` in their `Result` | S3c |
| `input` | `ERR_EOF`, `read_error_text` in `read_line_from` | S4 |
| `format` | `ERR_SHORT_WRITE`, `write_error_text`, `capacity_exhausted` (the span, measure and test writers report `ENOSPC` natively) | S2 |
| `derive`, `data.json` | writer callbacks return the typed outcome; no message shim | S2 |
| `log.sink`, `log` | `ERR_SHORT_WRITE`, `report_write` folding a `WriteError` into a `WriteReport` | S4 |

## Prepared branches

- `origin/feat/618` (four commits): `dac63cd` directory cursors across native
  backends and `a230488` byte-socket and directory-root ownership are landed
  by S3b on the frozen signatures (the directory batch test seeks before its
  first scan because btrfs hides entries created after the descriptor was
  opened until a seek; `a230488`'s changelog line for process waits belongs
  to `9dd151d` and was not taken). `9dd151d` process status and wait
  ownership (typed `exec.Error`, full Windows exit codes) is S3c's. `66d545c`
  is superseded: std 1.0.2 on `dev` already declares both profiles (and
  `{artifact.suffix}` landed with mach #3222). When rebased, `9dd151d` adopts
  the frozen signatures above and spells its carriers as `res`, `opt` and
  `err` (`R.Result[ExitStatus, Error]` becomes `res[ExitStatus, Error]`,
  `O.Option[ExitStatus]` becomes `opt[ExitStatus]`).
- `origin/feat/mach-3110` (`ad7add3` on top of feat/618): the eight
  `sync.atomic` inline annotations. Landed by S4a (cherry-picked onto `dev`,
  the feat/618 CHANGELOG line dropped); see "Atomic inlining" below.

## Atomic inlining (mach #3110, std half of phase 2)

Proof under the v5 compiler `8464568d` on linux-x86_64 with a program that
calls each of the eight wrappers once cross-module (`use std.sync.atomic;`,
`store`, `load`, `cas`, `fetch_add`, `fetch_sub`, `fence`, `exchange`,
`spin_hint`, then a checking `load`), built with `--emit-asm`:

| profile | `call` instructions in `main.s` | atomic instructions in `main.s`, in source order | exit |
| --- | ---: | --- | ---: |
| release (`-O2`) | 0 | `xchg` (store), `mov` load, `lock cmpxchg`, `lock xadd`, `neg` + `lock xadd`, `mfence`, `xchg` (exchange), `pause`, `mov` load | 0 |
| debug (`-O0`, control) | 9 (one per wrapper call, `std.sync.atomic.*`) | none in `main.s` (all inside the callees) | 0 |

The release stream keeps the wrappers' instruction sequences and their order,
`fence` stays an `mfence`, and the program's checks on the observed values
pass. The mach half (linking and running the wrappers on three native
targets) is the compiler repository's.

Control (same program, same compiler, mach 4.30.0): with all eight
annotations stripped from the copied `std.sync.atomic` the release `main.s`
also carries zero `call` instructions and the same atomic sequence. The
compiler's release policy (`doc/design/inline-acceptance-3110.md` in mach)
already flows every small cross-module body, and the wrappers clear its
25-instruction bar. The annotations therefore pin the decision rather than
create it: they are the wrappers' declared contract, independent of the size
heuristic and of any future growth of a wrapper body. `#[inline]` has no
effect at `-O0`, by that policy.

## What the lanes owe

- S2 to S4: migrate the modules in their domain tables to the representations
  recorded here and in the S0 census, remove the translation shims listed
  above, and declare the domain error tags named in the tables (`ParseError`,
  `WriteError`, `EncodeError`, `JsonError`, `TomlError`, `InflateError`,
  `FsError` (declared by S3b), `EnvError`, `StateError`, `ThreadError`,
  `SinkError`, `TermError`), each nesting `allocator.Error` where allocation
  is one of its causes.
- S3 owns the operation and error contracts S5 to S7 consume, and lands
  `feat/618`'s three producer fixes on the frozen foundations (two landed by
  S3b, `9dd151d` owed by S3c).
- S5 to S8: behavior programs on top of S3's contracts (Darwin boundaries,
  ancillary rights, welded secret I/O, gzip lifecycle); no foundation change.
- C5: the compiler side is done (mach #3226, `8464568d` seeds nothing) and
  std declares the three tags in `std.types.canonical` with the `use` sweep
  (std #617, S1 phase 2). What remains: `std.types.result` and
  `std.types.option` (`Result`, `Option`, `Void`, `ok`, `err`, `ok_void`,
  `void_of`, `some`, `none`, `is_*`, `unwrap*`) are deleted after the last
  consumer migrates, `mach.toml` moves to 2.0.0 and the CHANGELOG records
  the breaking surface. Generics over the canonical tags need no follow-up.
