[std](../README.md) / [crypto](README.md) / **ct**

# std.crypto.ct

constant-time primitives over `^` secrets

the operations that replace the ones a leakage model observes. sema rejects a
secret branch condition, a secret memory index, and a secret operand of a
variable-latency instruction; these are what one writes instead. every
computational primitive here is `#[constant_time("soft")]`, so the backend may not
reintroduce a branch or select a variable-latency instruction on a secret
operand. `zeroize` holds the wipe that no pass deletes.

TWO KINDS OF PRIMITIVE, FOR TWO DIFFERENT REASONS.

the comparisons are the language's own `==` / `<` / `>` on secret operands.
a comparison is not a branch: mach lowers one to a flag-setting compare and a
materialize (`cmp`/`setb` on x86_64, `cmp`/`cset` on aarch64, `sltu` on
riscv64), all branch-free, and each lowering zero-extends a narrow operand
before comparing. what keeps it that way is `#[constant_time("soft")]`: inside it the
backend may not turn a secret comparison into a branch, and the translation
validator re-checks the lowered MIR. writing the bit-twiddling equivalent by
hand would buy nothing the contract does not already give, and would cost the
operand cleanup the compare gets for free.

the merges are masked arithmetic, and/or/xor/not over an all-ones mask,
because there is no operator that selects without branching. that set is
branch-free on every architecture mach targets, including base RISC-V, which
has no conditional move at all, and it needs no per-arch assembly. multiply is
deliberately absent: it is variable-latency on some cores, and sema admits it
on a secret operand only where the target declares its multiply constant-time
(the compiler's `doc/language/secrecy.md`), so a primitive built on it would
not be portable.

THE FLAG CONVENTION. comparisons return a secret `^u8` holding 0 or 1, and
`mask_*` lifts that flag to an all-ones mask of a chosen width. one flag type
across every width is what lets a comparison at one width drive a select at
another (`select_u32(eq[u8](x, y), a, b)`) with no conversion at the call site.
`select_*` takes the flag directly and widens internally.

THE COMPARISONS ARE GENERIC. `is_zero`, `eq`, `lt` and `gt` are one generic
each over the width, spelled `eq[u32](a, b)` at the call site. an instance is
the readable unit for auditing emitted code: it is a monomorphic symbol whose
release lowering is pinned instruction for instruction against the
hand-written per-width bodies it replaced (x86_64 and aarch64, #660, #839).
an instance carries `#[constant_time("soft")]` exactly as a hand-written function does
(the lowering sets the flag per instance, so the translation validator
re-checks every width), and the flow typing checks the body against the
instance's types, so a secret misuse is refused at the width that asked for
it. `mask_*`, `select_*` and `lookup_*` are still spelled out per width
because their bodies differ by the cast they widen through.

> **Experimental preview.** mach's constant-time support is unaudited and has
> known open holes. see the compiler's `doc/language/secrecy.md`. do not build
> production cryptography on this version.

Source: [`src/crypto/ct.mach`](../../../src/crypto/ct.mach)

| Functions | |
| :--- | :--- |
| [`mask_u8`](#mask_u8) | lift a secret 0/1 flag to an all-ones 8-bit mask |
| [`mask_u16`](#mask_u16) | lift a secret 0/1 flag to an all-ones 16-bit mask |
| [`mask_u32`](#mask_u32) | lift a secret 0/1 flag to an all-ones 32-bit mask |
| [`mask_u64`](#mask_u64) | lift a secret 0/1 flag to an all-ones 64-bit mask |
| [`mask_usize`](#mask_usize) | lift a secret 0/1 flag to an all-ones usize mask |
| [`select_u8`](#select_u8) | branchless select between two secret bytes |
| [`select_u16`](#select_u16) | branchless select between two secret 16-bit words |
| [`select_u32`](#select_u32) | branchless select between two secret 32-bit words |
| [`select_u64`](#select_u64) | branchless select between two secret 64-bit words |
| [`select_usize`](#select_usize) | branchless select between two secret usize words |
| [`is_zero`](#is_zero) | branchless test of a secret word against zero |
| [`eq`](#eq) | branchless equality of two secret words |
| [`lt`](#lt) | branchless unsigned less-than of two secret words |
| [`gt`](#gt) | branchless unsigned greater-than of two secret words |
| [`eq_bytes`](#eq_bytes) | branchless equality of two secret byte buffers |
| [`lookup_u8`](#lookup_u8) | read a secret-indexed byte without a secret memory address |
| [`lookup_u32`](#lookup_u32) | read a secret-indexed 32-bit word without a secret memory address |
| [`lookup_u64`](#lookup_u64) | read a secret-indexed 64-bit word without a secret memory address |
| [`zeroize`](#zeroize) | wipe secret memory |
| [`zeroize_plain`](#zeroize_plain) | wipe memory whose type is not secret but which may hold secrets |
| [`copy_bytes`](#copy_bytes) | copy secret bytes without declassifying them |
| [`move_bytes`](#move_bytes) | copy secret bytes between regions that may overlap |
| [`begin`](#begin) | engage the hardware data-independent-timing mode, if the target has one |
| [`end`](#end) | release the hardware data-independent-timing mode engaged by `begin` |

---

## Functions

### mask_u8

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun mask_u8(c: ^u8) ^u8
```

lift a secret 0/1 flag to an all-ones 8-bit mask

`0` maps to `0x00` and `1` to `0xFF`. the low bit is taken first, so a flag
outside {0, 1} selects on its low bit rather than blending the two operands'
bits together.

| Parameter | |
| :--- | :--- |
| `c` | secret flag, 0 or 1 |
| **returns** | 0x00 or 0xFF |

### mask_u16

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun mask_u16(c: ^u8) ^u16
```

lift a secret 0/1 flag to an all-ones 16-bit mask

THE WIDENING CAST AND THE `& 1` DO DIFFERENT JOBS, stated once for the four
`mask_*` that widen (u16/u32/u64/usize).

`::^uN` zero-extends: it takes the low 8 bits of the flag and nothing else, so a
caller's stray high bits cannot reach the subtraction. that is worth naming
because it was NOT true until briar-systems/mach#2373: a secret-to-secret `::`
used to lower to a width-changing `bitcast`, a reinterpret that cleaned nothing,
and these four were correct only because the `& 1` happened to be emitted at
machine-register width. they are now correct because the cast converts.

the `& 1` is the flag's normalization, not the cleanup: it reduces a flag outside
{0, 1} to its low bit, which is what lets `0 - one` be all-ones or all-zeros
rather than a partial blend. it is load-bearing for that reason alone, and
dropping it is caught by `ct__mask_lifts_the_flag_low_bit_at_every_width`.

`ct__mask_answers_for_the_value_under_a_dirty_flag` pins the pair: the masks must
answer for the 8-bit VALUE of the flag whatever the register around it holds. a
caller can still hand over stray high bits: a narrow `0 - x` is not truncated,
as #2357 canonicalized the shift consumers rather than the producers, so this stays
a live property to guard, not a historical one.

| Parameter | |
| :--- | :--- |
| `c` | secret flag, 0 or 1 |
| **returns** | 0x0000 or 0xFFFF |

### mask_u32

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun mask_u32(c: ^u8) ^u32
```

lift a secret 0/1 flag to an all-ones 32-bit mask

the cast zero-extends; the `& 1` normalizes the flag, as `mask_u16` explains.

| Parameter | |
| :--- | :--- |
| `c` | secret flag, 0 or 1 |
| **returns** | 0x00000000 or 0xFFFFFFFF |

### mask_u64

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun mask_u64(c: ^u8) ^u64
```

lift a secret 0/1 flag to an all-ones 64-bit mask

the cast zero-extends; the `& 1` normalizes the flag, as `mask_u16` explains.

| Parameter | |
| :--- | :--- |
| `c` | secret flag, 0 or 1 |
| **returns** | 0 or 0xFFFFFFFFFFFFFFFF |

### mask_usize

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun mask_usize(c: ^u8) ^usize
```

lift a secret 0/1 flag to an all-ones usize mask

the cast zero-extends; the `& 1` normalizes the flag, as `mask_u16` explains.

| Parameter | |
| :--- | :--- |
| `c` | secret flag, 0 or 1 |
| **returns** | 0 or the all-ones usize |

### select_u8

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun select_u8(cond: ^u8, a: ^u8, b: ^u8) ^u8
```

branchless select between two secret bytes

yields `a` when the flag is 1 and `b` when it is 0, as a bitwise blend under
the widened mask. both operands are always read, so the choice leaves no trace
in the control-flow or memory-address stream.

| Parameter | |
| :--- | :--- |
| `cond` | secret flag, 0 or 1 |
| `a` | value chosen when the flag is 1 |
| `b` | value chosen when the flag is 0 |
| **returns** | the chosen value |

### select_u16

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun select_u16(cond: ^u8, a: ^u16, b: ^u16) ^u16
```

branchless select between two secret 16-bit words

| Parameter | |
| :--- | :--- |
| `cond` | secret flag, 0 or 1 |
| `a` | value chosen when the flag is 1 |
| `b` | value chosen when the flag is 0 |
| **returns** | the chosen value |

### select_u32

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun select_u32(cond: ^u8, a: ^u32, b: ^u32) ^u32
```

branchless select between two secret 32-bit words

| Parameter | |
| :--- | :--- |
| `cond` | secret flag, 0 or 1 |
| `a` | value chosen when the flag is 1 |
| `b` | value chosen when the flag is 0 |
| **returns** | the chosen value |

### select_u64

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun select_u64(cond: ^u8, a: ^u64, b: ^u64) ^u64
```

branchless select between two secret 64-bit words

| Parameter | |
| :--- | :--- |
| `cond` | secret flag, 0 or 1 |
| `a` | value chosen when the flag is 1 |
| `b` | value chosen when the flag is 0 |
| **returns** | the chosen value |

### select_usize

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun select_usize(cond: ^u8, a: ^usize, b: ^usize) ^usize
```

branchless select between two secret usize words

| Parameter | |
| :--- | :--- |
| `cond` | secret flag, 0 or 1 |
| `a` | value chosen when the flag is 1 |
| `b` | value chosen when the flag is 0 |
| **returns** | the chosen value |

### is_zero

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun is_zero[T](a: ^T) ^u8
```

branchless test of a secret word against zero

one generic per family, instantiated per width. `#[constant_time("soft")]` validates each
instance's lowering, not the template: the template is never emitted, and the
instance is what the translation validator re-checks.

| Parameter | |
| :--- | :--- |
| `[T]` | unsigned integer width |
| `a` | value to test |
| **returns** | secret flag, 1 when `a` is zero |

### eq

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun eq[T](a: ^T, b: ^T) ^u8
```

branchless equality of two secret words

| Parameter | |
| :--- | :--- |
| `[T]` | unsigned integer width |
| `a` | left operand |
| `b` | right operand |
| **returns** | secret flag, 1 when equal |

### lt

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun lt[T](a: ^T, b: ^T) ^u8
```

branchless unsigned less-than of two secret words

| Parameter | |
| :--- | :--- |
| `[T]` | unsigned integer width |
| `a` | left operand |
| `b` | right operand |
| **returns** | secret flag, 1 when `a < b` |

### gt

```mach
#[constant_time("soft")]
#[inline("always")]
pub fun gt[T](a: ^T, b: ^T) ^u8
```

branchless unsigned greater-than of two secret words

| Parameter | |
| :--- | :--- |
| `[T]` | unsigned integer width |
| `a` | left operand |
| `b` | right operand |
| **returns** | secret flag, 1 when `a > b` |

### eq_bytes

```mach
#[constant_time("soft")]
pub fun eq_bytes(a: *^u8, b: *^u8, len: usize) ^u8
```

branchless equality of two secret byte buffers

folds every byte of both buffers whatever they hold, so the running time
depends only on `len`, which is public. the accumulator is the running
difference: zero exactly when every byte agreed.

| Parameter | |
| :--- | :--- |
| `a` | left buffer |
| `b` | right buffer |
| `len` | length of both buffers in bytes |
| **returns** | secret flag, 1 when the buffers are equal |

### lookup_u8

```mach
#[constant_time("soft")]
pub fun lookup_u8(table: *^u8, len: usize, idx: ^usize) ^u8
```

read a secret-indexed byte without a secret memory address

scans the whole table and merges the element whose public position matches the
secret index, so the address trace is the same for every index. that is what
replaces `table[idx]`, which sema rejects. cost is linear in `len`.

an index at or beyond `len` matches nothing and yields 0. that is the defined
result of the scan, not a bounds check: no comparison against `len` reaches
the control flow, so an out-of-range index costs exactly what an in-range one
does.

| Parameter | |
| :--- | :--- |
| `table` | base of the table |
| `len` | number of elements, public |
| `idx` | secret element index |
| **returns** | the selected element, or 0 if the index is out of range |

### lookup_u32

```mach
#[constant_time("soft")]
pub fun lookup_u32(table: *^u32, len: usize, idx: ^usize) ^u32
```

read a secret-indexed 32-bit word without a secret memory address

| Parameter | |
| :--- | :--- |
| `table` | base of the table |
| `len` | number of elements, public |
| `idx` | secret element index |
| **returns** | the selected element, or 0 if the index is out of range |

### lookup_u64

```mach
#[constant_time("soft")]
pub fun lookup_u64(table: *^u64, len: usize, idx: ^usize) ^u64
```

read a secret-indexed 64-bit word without a secret memory address

| Parameter | |
| :--- | :--- |
| `table` | base of the table |
| `len` | number of elements, public |
| `idx` | secret element index |
| **returns** | the selected element, or 0 if the index is out of range |

### zeroize

```mach
#[constant_time("soft")]
pub fun zeroize(p: *^u8, n: usize)
```

wipe secret memory

a zeroing loop over storage that is never read again is dead by every ordinary
rule, and an optimizer may delete, merge or sink it past the release that
follows, leaving key material in memory behind code that reads as if it had
been erased. `$zeroize` is the language's own answer: a kept fill no pass drops,
narrows or merges, whose length and timing rest on the size alone. it does not
cover a secret in a REGISTER: a register-promoted `var x: ^u8 = k; x = 0;` is
outside the memory-address leakage model. this wipes memory.

a span of another type wipes with `$zeroize` itself, which takes any `*T`, and so
does constant-time code with secrets still live in its registers, since the
intrinsic is no call for them to reach.

| Parameter | |
| :--- | :--- |
| `p` | base of the region to wipe |
| `n` | number of bytes |

### zeroize_plain

```mach
pub fun zeroize_plain(p: *u8, n: usize)
```

wipe memory whose type is not secret but which may hold secrets

a thread's thread-local block is plain memory to the type system, yet the
variables in it may be secret.

| Parameter | |
| :--- | :--- |
| `p` | base of the region to wipe |
| `n` | number of bytes |

### copy_bytes

```mach
#[constant_time("soft")]
pub fun copy_bytes(dst: *^u8, src: *^u8, n: usize)
```

copy secret bytes without declassifying them

the regions must not overlap, `move_bytes` is the overlap-safe copy. the
running time depends on `n` and the two addresses alone: every load and store
is at a public offset from a public base, every loop runs on `n`, and the
`constant_time` contract has the build prove that no secret reaches a branch,
an address or a variable-time instruction. see the kernels below for how the
bytes are moved.

| Parameter | |
| :--- | :--- |
| `dst` | base of the destination |
| `src` | base of the source |
| `n` | number of bytes |

### move_bytes

```mach
#[constant_time("soft")]
pub fun move_bytes(dst: *^u8, src: *^u8, n: usize)
```

copy secret bytes between regions that may overlap

the direction is picked from the two public addresses alone: forward when the
destination starts below the source, backward otherwise. see the kernels below
for why each direction is safe for its case.

| Parameter | |
| :--- | :--- |
| `dst` | base of the destination |
| `src` | base of the source |
| `n` | number of bytes |

### begin

```mach
pub fun begin() bool
```

engage the hardware data-independent-timing mode, if the target has one

the timing guarantee the type system enforces is about the instructions
emitted. whether a given instruction's latency is data-independent is the
silicon's business. some architectures expose a mode that promises it, and
this is where a caller asks for it around secret work.

  * aarch64 linux, darwin and freestanding: `PSTATE.DIT`, set for the calling thread with
    `msr dit, 1` through std.system.dit where the processor and kernel
    provide FEAT_DIT. each soft constant-time function already switches it
    for itself, so this is for a thread that wants it across code that is
    not. std.system.timing reports whether the processor provides it.
  * x86_64: DOITM lives in the `IA32_UARCH_MISC_CTL` MSR, writable only at
    ring 0. no user-mode program sets it on any OS. it is the kernel's to
    configure.
  * riscv64: the Zkt extension states data-independent latency for its
    instruction list as an architectural property. there is no mode bit,
    so there is nothing to engage.

| Parameter | |
| :--- | :--- |
| **returns** | whether a hardware data-independent-timing mode is engaged for the calling thread |

### end

```mach
#[constant_time("soft")]
pub fun end()
```

release the hardware data-independent-timing mode engaged by `begin`

the mode is left on: it only removes a timing channel, and an enclosing
`begin` may rely on it for the same thread. it does nothing, so constant-time
code holding a secret may call it

