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
| suite at this phase | 1224 passed, 0 failed under the v5 compiler `8464568d` on linux-x86_64 and linux-riscv64 (qemu) after S2 (1199 after S3a, 1185 at S1 phase 2, 1182 at S1 phase 1 under `9a15ac3a6`, 1157 on the base under both the 4.30.0 seed and the v5 compiler) |

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

S2 executed its rows as tabled with these corrections:

| table or census row | tabled target | executed | why |
| --- | --- | --- | --- |
| `format.vformat`, `format.format` | `res[usize, WriteError]` | `res[usize, FormatError]` with `FormatError { syntax: usize; few_holes: usize; many_holes: usize; write: WriteError; alloc: A.Error; }` | a malformed format string and an argument-count mismatch are the format's own failures, distinct from the sink's; the sink's outcome nests as `write` with its persisted prefix. `write_*` and `write_value` take no format string and stay `res[usize, WriteError]` |
| `format.sprint` | `res[OwnedString\|str, FormatError]` | `res[str, FormatError]` (extent `str_len + 1`, released with `text.string.str_free`) | the result is measured exactly before it is allocated, so there is no spare extent to keep; `alloc` is the tag's own case, not a shim |
| `format.capacity_exhausted` | listed as a translation shim | retained as the span sink's native `ENOSPC` `WriteError` | it is the bounded sink reporting its own refusal through the frozen `WriteError`, not a message spelled over a typed outcome; `ERR_SHORT_WRITE` and `write_error_text` are gone |
| `print.printf`, `eprintf`, `printlnf`, `eprintlnf` | `res[usize, WriteError]` | `res[usize, FormatError]` | they format, so they can fail the way `format` does; `print`, `println`, `eprint`, `eprintln`, `u64`, `eu64` are `res[usize, WriteError]` as tabled |
| `input.read_line`, `read_line_from` | `res[usize, ReadError]` | `res[usize, InputError]` with `InputError { read: ReadError; too_long: usize; }` | a line that does not fit the buffer is not a reader failure; it carries the bytes buffered, the overflowing byte is consumed and dropped, and the next call continues. `read{eof{0}}` is the end of input with nothing buffered, distinct from an empty line `ok{0}` |
| `text.parse.ParseError` | "invalid syntax and overflow distinct" | `ParseError { empty; syntax: usize; overflow: usize; base: u8; }` | an empty input and a base outside 2..36 are distinct from a bad byte; `syntax` and `overflow` carry the byte offset |
| `data.json.dnit` | not tabled | `err[allocator.Error]` (every child released, first refusal reported) | allocator-release, the same shape as every container `dnit` |
| `data.json.value_get`, `value_find` | not tabled (census `opt[*Value]`) | `opt[*Value]` | no child at an index and no entry with a key are absence; the pointer borrows the tree |
| `data.json.value_key` | not tabled (census `opt[str]`) | `opt[str]` (`value_key_len` unchanged) | the same absence |
| `data.toml.get`, `get_table`, `get_array`, `array_get`, `table_value` | not tabled (census `opt[*T]`) | `opt[*Value]`, `opt[*Table]`, `opt[*Array]` | absence and wrong shape were a nil pointer, the last pointer-as-option in the module; nil receivers are contract violations and no longer special-cased (`table_len`, `array_len` included) |
| `data.toml.get_str`, `table_key` | not tabled (census `opt[str]`) | `opt[str]` | the same absence |
| `data.toml.TomlError` | "positioned syntax distinct" | `TomlError { syntax: usize; overflow: usize; depth: usize; conflict: usize; alloc: Error; }` | an integer that does not fit, nesting past the bound and a key colliding with a value of another shape each carry their offset |
| `encoding.binary.EncodeError` | "alloc and invalid-encoder distinct" | `EncodeError { alloc: A.Error; overflow; invalid; full: usize; alignment: usize; reserved; bounds; inactive; stale; busy; }` | the builder and reservation refusals were each a distinct message; each is a case now |
| `encoding.binary.DecodeError` | "short input distinct from malformed" | `DecodeError { short: usize; invalid; alignment: usize; bounds; unterminated; }` | `short` carries the bytes remaining; the malformed cases are named |
| `compress.*.finish` (inflate, zlib) | `res[Progress, InflateError]` | `err[InflateError]` | a completed stream has no value; `truncated{0, 0}` when the stream did not reach its end, `closed` after `dnit`. `gzip.finish` keeps `res[Progress, InflateError]` because it drains output |
| `compress.*` nil arguments | `"inflater is nil"`, `"gzip input is nil"` | no check | a nil decoder, or a nil buffer with a nonzero length, is a contract violation under the raw-memory rules, not an outcome |
| `io.reader.advance`, `io.writer.advance` | private | `pub` | a composite consumer (`input`, `format`, `data.json`) rebases a prefix the same way the reader and writer do; additive, no frozen row changes |

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

### Text, encoding, data and compression (S2)

| API | signature | frozen |
| --- | --- | --- |
| `text.parse.ParseError` | `pub tag ParseError: u8 { empty; syntax: usize; overflow: usize; base: u8; }` | yes |
| `text.parse.parse_u64`, `parse_u64_exact`, `parse_i64`, `parse_i64_exact` | `fun(s: str, base: u8) res[u64\|i64, ParseError]` | yes |
| `text.parse.parse_f64`, `parse_f64_exact` | `fun(s: str) res[f64, ParseError]`; `parse_f64_len` `fun(s: str, len: usize) res[f64, ParseError]` | yes |
| `format.FormatError` | `pub tag FormatError: u8 { syntax: usize; few_holes: usize; many_holes: usize; write: WriteError; alloc: A.Error; }` | yes |
| `format.write_bytes`, `write_str`, `write_byte`, `write_newline`, `write_u64`, `write_i64`, `write_hex_u64`, `write_ptr`, `write_f64`, `write_value` | `... res[usize, WriteError]` (the payload is the persisted prefix) | yes |
| `format.vformat`, `format` | `fun(w: *writer.Writer, fmt: str, va: ...) res[usize, FormatError]` | yes |
| `format.sprint` | `fun(a: *A.Allocator, fmt: str, va: ...) res[str, FormatError]` (extent `str_len + 1`, released with `text.string.str_free`; a format failure is reported before any allocation) | yes |
| `print.print`, `println`, `eprint`, `eprintln`, `u64`, `eu64` | `... res[usize, WriteError]` | yes |
| `print.printf`, `eprintf`, `printlnf`, `eprintlnf` | `... res[usize, FormatError]` | yes |
| `input.InputError` | `pub tag InputError: u8 { read: ReadError; too_long: usize; }` | yes |
| `input.read_line_from` | `fun(r: *reader.Reader, buf: *u8, cap: usize) res[usize, InputError]`; `read_line` `fun(buf: *u8, cap: usize) res[usize, InputError]` | yes |
| `encoding.binary.EncodeError` | `pub tag EncodeError: u8 { alloc: A.Error; overflow; invalid; full: usize; alignment: usize; reserved; bounds; inactive; stale; busy; }` | yes |
| `encoding.binary.DecodeError` | `pub tag DecodeError: u8 { short: usize; invalid; alignment: usize; bounds; unterminated; }` | yes |
| `encoding.binary.encoder_dnit` | `fun(e: *Encoder) err[A.Error]` | yes |
| `encoding.binary.reserve`, `write_*`, `patch_*`, `align`, `builder_write_*`, `builder_patch_*`, `builder_align`, `builder_rollback`, `builder_commit`, `reservation_rollback` | `... res[usize, EncodeError]`; `builder_checkpoint` `res[Checkpoint, EncodeError]`; `builder_reserve` `res[Reservation, EncodeError]` | yes |
| `encoding.binary.read_u8/u16/u32/u64` | `... res[uN, DecodeError]`; `read_bytes` `res[*u8, DecodeError]`; `read_str` `res[str, DecodeError]`; `skip`, `align_read`, `cursor_rollback` `res[usize, DecodeError]`; `read_subview` `res[Cursor, DecodeError]`; `cursor_checkpoint` `res[Checkpoint, DecodeError]` | yes |
| `encoding.base64`, `encoding.hex`, `text.utf8` | unchanged | yes |
| `data.json.JsonError` | `pub tag JsonError: u8 { syntax: usize; depth: usize; alloc: allocator.Error; }` | yes |
| `data.json.parse` | `fun(src: *u8, src_len: usize, alloc: *allocator.Allocator) res[Value, JsonError]` (a partial parse releases what it acquired before reporting) | yes |
| `data.json.dnit` | `fun(alloc: *allocator.Allocator, v: *Value) err[allocator.Error]` | yes |
| `data.json.value_string_decode` | `fun(v: *Value, buf: *u8, len: usize) res[usize, JsonError]` | yes |
| `data.json.value_get`, `value_find` | `... opt[*Value]`; `value_key` `opt[str]` (borrow the tree; `value_key_len`, `value_count`, predicates and numbers unchanged) | yes |
| `data.json.write_value`, `object_begin`, `object_end`, `object_end_value`, `field_*`, `array_*`, `value_f64`, `write_json_string` | `... err[WriteError]` (the payload is the emitted prefix) | yes |
| `data.toml.TomlError` | `pub tag TomlError: u8 { syntax: usize; overflow: usize; depth: usize; conflict: usize; alloc: Error; }` | yes |
| `data.toml.parse` | `fun(a: *Allocator, src: str) res[Table, TomlError]` (nothing a failed parse built survives) | yes |
| `data.toml.dnit` | `fun(a: *Allocator, t: *Table) err[Error]` | yes |
| `data.toml.get`, `array_get`, `table_value` | `... opt[*Value]`; `get_table` `opt[*Table]`; `get_array` `opt[*Array]`; `get_str`, `table_key` `opt[str]`; `get_int` `opt[i64]`; `get_float` `opt[f64]`; `get_bool` `opt[bool]` (absence or wrong shape is `none`) | yes |
| `derive.fmt[T]` | `fun(w: *writer.Writer, v: *T) res[usize, WriteError]`; `eq`, `hash`, `clone`, `check` unchanged | yes |
| `compress.inflate.Defect` | `pub tag Defect: u8 { block_type; stored_length; code_count; length_code_set; length_code; repeat_no_previous; repeat_overrun; oversubscribed_literals; incomplete_literals; oversubscribed_distances; incomplete_distances; literal_code; distance_code; distance_range; method; window; header_check; dictionary; magic; flags; header_checksum; checksum; length; }` (the deflate cases are inflate's, the framing cases the wrappers'; one tag describes a whole stream) | yes |
| `compress.inflate.Committed`, `Fault` | `pub rec Committed { consumed: usize; written: usize; }`, `pub rec Fault { defect: Defect; consumed: usize; written: usize; }` | yes |
| `compress.inflate.InflateError` | `pub tag InflateError: u8 { alloc: A.Error; malformed: Fault; truncated: Committed; full: Committed; closed; finished; invalid; }` (re-exported by `zlib` and `gzip`) | yes |
| `compress.inflate.advance`, `settled`, `malformed`, `truncated` | `fun(e: InflateError, consumed: usize, written: usize) InflateError`, `fun(e: InflateError) InflateError`, `fun(defect: Defect, consumed: usize, written: usize) InflateError`, `fun(consumed: usize, written: usize) InflateError` | yes |
| `compress.{inflate,zlib,gzip}.init` | `fun(a: *A.Allocator) res[Inflater\|Decompressor, InflateError]` (`alloc` is the only failure; a decoder is relocatable, not address-bound) | yes |
| `compress.{inflate,zlib,gzip}.dnit` | `fun(z: *T) err[A.Error]` (a decoder holding no window is already released; a refused release leaves it owning) | yes |
| `compress.{inflate,zlib,gzip}.decompress` | `fun(z: *T, src: *u8, src_len: usize, dst: *u8, dst_len: usize) res[Progress, InflateError]` (a failure carries the counts this call committed; `closed` after `dnit`) | yes |
| `compress.{inflate,zlib}.finish` | `fun(z: *T) err[InflateError]`; `compress.gzip.finish` `fun(z: *Decompressor, dst: *u8, dst_len: usize) res[Progress, InflateError]` (`finished` on input after it) | yes |
| `compress.{inflate,zlib,gzip}.decompress_into` | `fun(a, src, src_len, dst, dst_len) res[usize, InflateError]` (`malformed`, `truncated` and `full` carry the counts over the whole call) | yes |
| `compress.{inflate,zlib,gzip}.decompress_alloc` | `fun(a, src, src_len) res[Vector[u8], InflateError]` (on failure the vector is already released) | yes |
| `compress.*.is_done`, `reset`, `Progress`, status constants, `WINDOW` | unchanged | yes |
| `math.mat4.mat4_inverse` | `fun(m: Mat4) opt[Mat4]` | yes |
| `io.reader.advance`, `io.writer.advance` | `pub fun(error: ReadError\|WriteError, delivered\|written: usize) ReadError\|WriteError` (additive) | yes |

Contract: a composite operation's error payload is the whole prefix the call
committed, never the whole stream's (a gzip call that fails in its second
member reports that call's consumed and written; the sticky failure it stores
is re-reported `settled`, with nothing committed). Every parser releases what
it acquired before reporting `alloc`; every emitter's `WriteError` payload is
the prefix persisted.

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
| `io.error.Error` | unchanged record | yes |

Contract: a reader source or writer sink never spells `eof`, `stalled` or
`would_block` itself unless it wants to; it hands over bytes or a native
failure and `read`/`write` classify. A composite operation's error payload is
the whole prefix (`read_exact` after two partial reads reports the sum).
`read_all` releases its vector before reporting; `read_str` adopts the vector's
buffer whole. `WriteError` and `ReadError` are the domain tags the S2 and S4
consumers (`format`, `print`, `input`, `terminal`, `log`, `data.json`) import;
their shapes are frozen by this phase.

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

### Text and encoding (S2, done)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `text.parse` | `parse_u64`, `parse_u64_exact`, `parse_i64`, `parse_i64_exact`, `parse_f64`, `parse_f64_len`, `parse_f64_exact` | done (S2): `res[T, ParseError]` with `empty`, `syntax`, `overflow` and `base` distinct; no allocation | result-payload |
| `text.utf8` | `validate`, `is_continuation`, decoders | unchanged predicates and values | value-or-effect |
| `format` | `write_*`, `write_value` | done (S2): `res[usize, WriteError]` carrying committed bytes and the writer cause (shared with `io.writer`, S3 owns the writer error type) | result-payload |
| `format` | `vformat`, `format` | done (S2): `res[usize, FormatError]` (correction above: the format string's own failures are distinct from the sink's, which nests as `write`) | result-payload |
| `format.sprint` | | done (S2): `res[str, FormatError]` with `alloc: allocator.Error`; the shim at the `A.allocate` site is gone | result-payload |
| `print` | `print`, `println`, `eprint*`, `u64`, `eu64` | done (S2): `res[usize, WriteError]` (checked printing stays checked) | result-payload |
| `print` | `printf` family | done (S2): `res[usize, FormatError]` (correction above) | result-payload |
| `input` | `read_line`, `read_line_from` | done (S2): `res[usize, InputError]` with `read: ReadError` (EOF distinct inside it) and `too_long` (correction above); `ERR_EOF` and `read_error_text` are gone | result-payload |
| `encoding.binary` | `reserve`, `write_*`, `patch_*`, `align`, builder and reservation operations | done (S2): `res[usize, EncodeError]` with `alloc: allocator.Error` and `invalid` distinct; the shim at the `A.reallocate` site is gone | result-payload |
| `encoding.binary` | `read_*`, `skip`, `align_read`, `read_subview`, checkpoints and rollbacks | done (S2): `res[T, DecodeError]` with `short` distinct from the malformed cases | result-payload |
| `encoding.binary.encoder_dnit` | | done (S2): `err[allocator.Error]` | allocator-release |
| `encoding.base64`, `encoding.hex` | | unchanged (values and lengths) | value-or-effect |
| `data.json` | `parse`, `value_string_decode`, children/keys growth | done (S2): `res[Value, JsonError]` with `alloc: allocator.Error`, `syntax` with position and `depth` distinct; `value_*` predicates and numbers unchanged; a partial parse releases what it acquired; the two growth shims are gone; `dnit` `err[allocator.Error]` | result-payload |
| `data.json` | `value_get`, `value_key`, `value_find` | done (S2): `opt[*Value]`, `opt[str]`, `opt[*Value]` (census rows, correction above) | optional-value |
| `data.json` streaming writer helpers | | done (S2): `err[WriteError]` with the emitted prefix and writer cause | streaming-output |
| `data.toml` | `parse`, key and array growth, string decoding | done (S2): `res[Table, TomlError]` with `alloc: allocator.Error` and positioned `syntax`, `overflow`, `depth` and `conflict` distinct; the eight growth and decode shims are gone; `get_int`, `get_float`, `get_bool` `opt[T]` as absence-or-type-mismatch; `dnit` `err[allocator.Error]` | result-payload, optional-value, allocator-release |
| `data.toml` | `get`, `get_str`, `get_table`, `get_array`, `array_get`, `table_key`, `table_value` | done (S2): `opt[*Value]`, `opt[str]`, `opt[*Table]`, `opt[*Array]`, `opt[*Value]`, `opt[str]`, `opt[*Value]` (census rows, correction above) | optional-value |
| `derive` | `eq[T]` unchanged; `fmt[T]` | done (S2): `res[usize, WriteError]` | result-payload |

### Compression (S2 types done, S8 lifecycle)

| module | outcome-bearing APIs | representation | S0 rule |
| --- | --- | --- | --- |
| `compress.inflate`, `zlib`, `gzip` | `init` | done (S2): `res[Inflater\|Decompressor, InflateError]` with `alloc` the only case raised (the window is the only acquisition; the shim at the window allocation is gone) | result-payload |
| | `dnit` | done (S2): `err[allocator.Error]` | allocator-release |
| | `decompress`, `finish`, `decompress_into`, `decompress_alloc` | done (S2): `res[Progress, InflateError]` where a failure after progress carries the committed input and output counts; `finish` is `err[InflateError]` on inflate and zlib (correction above); concatenated members, explicit EOF, sticky failure (`opt[InflateError]`, re-reported `settled`), truncation and CRC verdicts are preserved for S8 with their tests passing unchanged in form; the `V.ensure` growth shims are gone | result-payload |
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
| `io.error` | `Error { kind; code; operation }` | unchanged record (done, S3a) | retained |
| `io.reader` | `read` | done (S3a): `res[usize, ReadError]` with EOF, would-block and native failure distinct | result-payload |
| | `read_exact` | done (S3a): `err[ReadError]` reporting the delivered count | optional-error |
| | `read_all`, `read_str` | done (S3a): `res[Vector[u8]\|OwnedString, ReadError]` with `alloc: allocator.Error`; the two `vector.reserve` shims are gone | result-payload |
| `io.writer` | `write` | done (S3a): `res[usize, WriteError]`; `write_all`, `write_str` `err[WriteError]` carrying the persisted prefix | result-payload, optional-error |
| `io.handle`, `io.lifecycle` | predicates unchanged; `make`, `attach`, `settle`, `settle_closed_child` | done (S3a): `err[StateError]` or `res[bool, StateError]` per the state-transition rule, address-bound attachments initialized in place | state-operation |
| `io.file` | `root_open`, `open_confined`, `map`, `transfer`, `watch_*`, `read_at`, `write_at` | done (S3a): `res[T, io_error.Error]` and `err[io_error.Error]` for unit successes; `root_open` in place (correction above); `watch_close` `err[io_error.Error]` | result-payload |
| `io.file.adapter`, `io.runtime` | every `Result[bool, io_error.Error]` | done (S3a): `err[io_error.Error]`; token-returning submits `res[Token, io_error.Error]`; `close`, `destroy` keep retained-descriptor and queued-completion facts in the error (`EINVAL` versus `EBUSY`) | result-payload |
| `io.file.posix`, `io.file.windows` | native `i64` | unchanged native boundary (done, S3a) | native-boundary |
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

### Math and SIMD (S2, done)

| module | representation |
| --- | --- |
| `math`, `math.bits`, `math.float`, `math.quat`, `math.bignum` | unchanged values and predicates |
| `math.mat4.mat4_inverse` | done (S2): `opt[Mat4]` (a singular matrix is mathematical absence) |
| `simd.select`, `reduce`, `shuffle`, `saturate`, `gather` | unchanged values |

## Translation shims left by this phase

Every site where a foundation refusal is turned into a module's legacy
message. The owning lane removes them when it migrates the module's own return
types; none is a final form. Counted by `"out of memory"` strings added in this
phase (33 sites over 15 modules):

| module | sites | lane |
| --- | ---: | --- |
| `filesystem` | 16 | S3 |
| `data.toml` | 8, removed | S2 (done) |
| `data.json` | 4, removed | S2 (done) |
| `compress.inflate` | 3, removed | S2 (done) |
| `process.exec` | 2 | S3 |
| `process.env` | 2 | S3 |
| `format` | 2, removed | S2 (done) |
| `filesystem.transaction` | 2, plus `sprint_text` around `format.sprint` (7 call sites, added by S2) | S3 |
| `encoding.binary` | 1, removed | S2 (done) |
| `compress.zlib`, `compress.gzip` | 1 each, removed | S2 (done) |
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
| `filesystem` | `ERR_EOF`, `read_error_text`, `write_error_text` (the reader/writer callbacks now return the typed outcome; `read_bytes`, `read_string`, `write_bytes`, `replace_bytes_atomic` translate) | S3b |
| `filesystem.transaction` | `write_error_text` around `sink_write`, `bytes_write_cb`, `write_subtree_file` | S3b |
| `process.exec` | `read_error_text` around `read_all` in `output` | S3c |
| `process.events`, `net.async`, `net.async.local`, `net.resolve` | `runtime_ok_*` predicates and `res`/`canonical.err` bindings at every `io_runtime` call; `net.async.wait` and `process.events.begin_runtime_drain` re-wrap the runtime's `res` in their `Result` | S3c |
| `input` | `ERR_EOF`, `read_error_text` in `read_line_from` | removed (S2): `InputError` nests the `ReadError` |
| `format` | `ERR_SHORT_WRITE`, `write_error_text` | removed (S2): `WriteError` is the outcome; `capacity_exhausted` stays as the span sink's native `ENOSPC` report (correction above) |
| `derive`, `data.json` | writer callbacks return the typed outcome; no message shim | done (S2) |
| `filesystem.transaction` | `sprint_text` spelling `format.sprint`'s `FormatError` as `R.Result[str, str]` (`"out of memory"`) at seven call sites | S3b |
| `log.sink`, `log` | `ERR_SHORT_WRITE`, `report_write` folding a `WriteError` into a `WriteReport` | S4 |

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
  causes. S2 is done: `ParseError`, `FormatError`, `InputError`,
  `EncodeError`, `DecodeError`, `JsonError`, `TomlError`, `InflateError` and
  `Defect` are frozen above, and S8 inherits the compression lifecycle on
  those shapes.
- S3 owns the operation and error contracts S5 to S7 consume, and lands
  `feat/618`'s three producer fixes on the frozen foundations.
- S5 to S8: behavior programs on top of S3's contracts (Darwin boundaries,
  ancillary rights, welded secret I/O, gzip lifecycle); no foundation change.
- C5: the compiler side is done (mach #3226, `8464568d` seeds nothing) and
  std declares the three tags in `std.types.canonical` with the `use` sweep
  (std #617, S1 phase 2). What remains: `std.types.result` and
  `std.types.option` (`Result`, `Option`, `Void`, `ok`, `err`, `ok_void`,
  `void_of`, `some`, `none`, `is_*`, `unwrap*`) are deleted after the last
  consumer migrates, `mach.toml` moves to 2.0.0 and the CHANGELOG records
  the breaking surface. Generics over the canonical tags need no follow-up.
