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
| suite at this phase | 1185 passed, 0 failed under the v5 compiler `8464568d` on linux-x86_64 (1182 at S1 phase 1 under `9a15ac3a6`, 1157 on the base under both the 4.30.0 seed and the v5 compiler) |

## Compiler facts every lane must know

- **The compiler still seeds `res`, `opt` and `err` and rejects a module that
  declares them** (`reject_builtin_named_type`: "a canonical tag name cannot
  also name a declared type"). std therefore spells the three bare names
  everywhere and declares nothing. `std.types.canonical` carries the contract
  text and pins the seeded shapes by test. When the compiler drops the seeding
  (mach #3218 follow-up, C5), the three `pub tag` lines move into that module
  and every consuming module gains `use std.types.canonical.res;` and friends.
  That is a one-line-per-module sweep, not a redesign, and it must land with
  the compiler change as one pinned pair.
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

### Crypto and random (S4)

| module | representation |
| --- | --- |
| `crypto.hash.*` (sha256, sha512, sha3, keccak, shake, crc32, adler32, fnv1a) | unchanged: values, states and digests |
| `crypto.ct` | unchanged: constant-time predicates and values; `begin` stays a bool meaning a hardware mode was engaged |
| `crypto.rand.fill` | `err[io_error.Error]` in place of the negative errno; the completed prefix on failure stays observable |
| `rand` | unchanged values |

### Filesystem and I/O (S3)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `io.error` | `Error { kind; code; operation; cleanup_code }` | unchanged record; primary and cleanup causes stay separate fields | retained |
| `io.reader` | `read` | `res[usize, ReadError]` with EOF, would-block and native failure distinct | result-payload |
| | `read_exact` | `err[ReadError]` reporting incomplete progress | optional-error |
| | `read_all`, `read_str` | `res[Vector[u8]\|OwnedString, ReadError]` with `alloc: allocator.Error` (translation shims at the two `vector.reserve` sites) | result-payload |
| `io.writer` | `write` | `res[usize, WriteError]`; `write_all`, `write_str` `err[WriteError]` carrying the persisted prefix | result-payload, optional-error |
| `io.handle`, `io.lifecycle` | predicates unchanged; `make`, `attach`, `settle`, `settle_closed_child` | `err[StateError]` or `res[bool, StateError]` per the state-transition rule, address-bound attachments initialized in place | state-operation |
| `io.file` | `root_open`, `open_confined`, `map`, `transfer`, `watch_*`, `read_at`, `write_at` | `res[T, io_error.Error]` and `err[io_error.Error]` for unit successes; `watch_close` `err[io_error.Error]` | result-payload |
| `io.file.adapter`, `io.runtime` | every `Result[bool, io_error.Error]` | `err[io_error.Error]`; token-returning submits `res[Token, io_error.Error]`; `close`, `destroy` keep retained-descriptor and queued-completion facts in the error | result-payload |
| `io.file.posix`, `io.file.windows` | native `i64` | unchanged native boundary | native-boundary |
| `filesystem` | `open`, `create`, `read`, `write`, `seek`, `identity_of`, `identity_link`, `stat_of_error` | `res[T, io_error.Error]` (already typed) | result-payload |
| | `close`, `sync` | `err[io_error.Error]` | optional-error |
| | `read_bytes`, `read_string`, `read_dir`, `stat_of`, `metadata`, `metadata_link`, `temp_create` | `res[T, io_error.Error\|FsError]` with `alloc: allocator.Error` distinct (translation shims at the `A.allocate`, `str_copy`, `vector.push` and `path.*` sites, 16 in this module) | result-payload |
| | `write_bytes`, `replace_bytes_atomic`, `create_dir`, `remove_file`, `remove_dir`, `rename`, `symlink`, `create_dir_all`, `remove_all`, `temp_close`, `temp_remove`, `temp_close_and_remove` | `err[FsError]`; a failure after publication says so (sync after rename is a separate effect) | optional-error |
| | `exists`, `is_file`, `is_dir`, `is_symlink` | `res[bool, io_error.Error]`: missing is a successful false, a native failure is the error | filesystem-query |
| `filesystem.removal` | `tree`, `private_tree` | `err[Error]` | optional-error |
| `filesystem.transaction` | every `O.Option[Error]` | `err[Error]`; `root_identity`, `entry_probe`, `commit`, `recover`, `root_remove_tree`, `descend`, `entry_make_dir` `res[T, Error]`; `entry_identity`, `entry_read_all` keep `res[opt[T], Error]`; `inventory_dnit` `err[allocator.Error]`; Roots, Locks, Claims, Workers keep their stronger lifetime contracts (translation shims at two `str_dup`/`str_copy_slice` sites) | result-payload, optional-error |
| `filesystem.transaction.ownership` | native `i64` | unchanged (native status decoded by `transaction`) | native-boundary |

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

### Synchronization (S4)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `sync.atomic` | `load`, `store`, `cas`, `fetch_add`, `fetch_sub`, `exchange`, `fence`, `spin_hint` | unchanged values; the eight N6 inline annotations land with `feat/mach-3110` | atomic-inline |
| `sync.mutex` | `try_lock`, `is_locked` | unchanged predicates | predicate-or-transition |
| `sync.channel` | `Status` | a closed tag; `send*`/`receive*` return the tag with the received element on the received case and the output pointer removed; `make`, `close`, `destroy` `err[StateError]` or `res[bool, StateError]` | closed-value, state-transition |
| `sync.worker_pool` | `Status` | a closed tag; `make*`, `submit*`, `close_*`, `join`, `shutdown_*` return it; `destroy` `err[StateError]`; `last_thread_error` keeps the native code | closed-value |
| `sync.cancel` | `Reason` | a closed tag; `make_root`, `make_child`, `init_registration`, `finish`, `unregister`, `destroy` `err[StateError]` in place (scopes and registrations are address-bound); `cancel`, `timeout`, `expire` `res[bool, StateError]`; `get_deadline` `res[opt[Deadline], StateError]` | deadline-query, state-transition |
| `sync.condition` | `WaitStatus` | a closed tag | closed-value |
| `sync.once` | `run` | `res[bool, InitError]` retaining the initializer's failure | state-transition |
| `sync.semaphore` | `init`, `release` | `err[StateError]`; `try_wait` unchanged predicate; counts unchanged | state-operation |
| `sync.thread` | `spawn*`, `join*`, `detach` | `err[ThreadError]`/`res[i64, ThreadError]` decoding native errors without narrowing; error-hiding `spawn`, `spawn_with`, `join` become checked or are removed; `diagnostic_id`, `is_done` unchanged | thread-operation |

### Clocks (S4)

| module | representation |
| --- | --- |
| `chrono.time.now`, `monotonic` | `res[Time, io_error.Error]`; `since`, `until` `res[Duration, io_error.Error]`; a failed clock is never zero time |
| `chrono.time` comparisons and components, `chrono.duration`, `chrono.date`, `chrono.format` | unchanged values and predicates |

### Terminal (S4)

| module | representation |
| --- | --- |
| `terminal`, `terminal.linux`, `terminal.darwin`, `terminal.windows` | `enable_raw`, `disable_raw`, `flush_input` `err[TermError]`; `poll_key` `res[opt[Key], TermError]` (no key is absence, native read failure is the error); `is_raw` unchanged |
| `terminal.key` | unchanged predicates and `Key` |

### Logging (S4)

| module | representation |
| --- | --- |
| `log`, `log.sink` | `WriteReport` retained with offered, persisted, suppression, truncation and failure; convenience functions return it; `logger`, `make`, `custom`, `from_writer`, `console`, `file`, `pipe`, `queued*` `res[Sink\|Logger, SinkError]` with queued sinks initialized in place (address-bound); `queued_close_*`, `queued_join`, `queued_destroy` `err[SinkError]` preserving undelivered records and thread failure |
| `log.record` | unchanged values; `EncodeStatus` becomes a closed tag |

### Runtime and OS (S4 portable, S5 Darwin)

| module | representation |
| --- | --- |
| `system.os`, `system.os.linux.*`, `system.os.darwin.*`, `system.os.windows.*`, `system.os.shared`, `system.os.secret`, `system.os.darwin.libsystem` | unchanged native boundary: foreign ABI widths, native constants, negative errno and raw calling conventions; the portable producers above decode them. `allocate`, `deallocate`, `reallocate`, `secret_allocate`, `secret_deallocate` keep nil and `i64` |
| `system.file_identity` | unchanged predicates and values |
| `system.panic` | unchanged |
| `runtime`, `runtime.linux.*`, `runtime.darwin.*`, `runtime.windows.*` | unchanged native entry and relocation boundary |
| `system.os.tests` | in-tree census tests; migrated call sites only |

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
| `filesystem` | 16 | S3 |
| `data.toml` | 8 | S2 |
| `data.json` | 4 | S2 |
| `compress.inflate` | 3 | S2/S8 |
| `process.exec` | 2 | S3 |
| `process.env` | 2 | S3 |
| `io.reader` | 2 | S3 |
| `format` | 2 | S2 |
| `filesystem.transaction` | 2 | S3 |
| `encoding.binary` | 1 | S2 |
| `compress.zlib`, `compress.gzip` | 1 each | S2/S8 |
| `net.resolve`, `net.resolve.shared` | 0 (typed `types.Error` and `bool` already) | S3 |

The `system.os.*` hits of that string are the OS layer's own native
messages, not shims.

## Prepared branches

- `origin/feat/618` (four commits): `dac63cd` directory cursors across native
  backends, `9dd151d` process status and wait ownership (typed `exec.Error`,
  full Windows exit codes), `66d545c` complete manifest profiles, `a230488`
  byte-socket and directory-root ownership. `66d545c` is superseded: std 1.0.2
  on `dev` already declares both profiles (and `{artifact.suffix}` landed with
  mach #3222). The other three are S3's producer contracts (`exec.Error`,
  `RemovalError`, typed `read_dir`); nothing in S1 depends on them. When
  rebased they adopt the frozen signatures above (`vector.push`,
  `A.allocate`, `str_dup`, `path.*`) and spell their carriers as `res`, `opt`
  and `err` (`R.Result[ExitStatus, Error]` becomes `res[ExitStatus, Error]`,
  `O.Option[ExitStatus]` becomes `opt[ExitStatus]`).
- `origin/feat/mach-3110` (`ad7add3` on top of feat/618): the eight
  `sync.atomic` inline annotations. Orthogonal to S1; lands with N6 under S4.
  Its base is feat/618, so it rebases after that branch.

## What the lanes owe

- S2 to S4: migrate the modules in their domain tables to the representations
  recorded here and in the S0 census, remove the translation shims listed
  above, and declare the domain error tags named in the tables (`ParseError`,
  `WriteError`, `EncodeError`, `JsonError`, `TomlError`, `InflateError`,
  `FsError`, `EnvError`, `StateError`, `ThreadError`, `SinkError`,
  `TermError`), each nesting `allocator.Error` where allocation is one of its
  causes.
- S3 owns the operation and error contracts S5 to S7 consume, and lands
  `feat/618`'s three producer fixes on the frozen foundations.
- S5 to S8: behavior programs on top of S3's contracts (Darwin boundaries,
  ancillary rights, welded secret I/O, gzip lifecycle); no foundation change.
- C5 (with mach #3226): the compiler stops seeding the canonical tags and std
  moves the three declarations into `std.types.canonical` with the `use`
  sweep; `std.types.result` and `std.types.option` (`Result`, `Option`,
  `Void`, `ok`, `err`, `ok_void`, `void_of`, `some`, `none`, `is_*`,
  `unwrap*`) are deleted after the last consumer migrates; the mangler defect
  for generics over canonical tags is fixed or the collections stay documented
  as unable to hold `res`/`opt`/`err` elements; `mach.toml` moves to 2.0.0
  and the CHANGELOG records the breaking surface.
