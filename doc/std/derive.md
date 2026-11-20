[std](README.md) / **derive**

# std.derive

generic derive helpers over a record's fields

these are macro-free, generic functions that walk a record type's fields at
comptime with `$each f in $fields(T)` and act on each field through the
projection `v.[f]`. one definition serves every record shape: the `$each`
unroll is deferred to instantiation, so `T` is a concrete record by the time a
field descriptor's type gates fold.

the walk descends. a field whose own type is a record is walked in turn, so a
derive over `Player { pos: Vec3 { x, y, z } }` reaches the three floats rather
than refusing at `pos`, at any nesting depth.

## the classification contract

every derive here classifies each field the same way, and `check[T]` is that
classification written once. a derive's own walk carries only its leaf action
and relies on `check[T]` for every refusal, which is why each walk's trailing
`$or { }` is empty rather than defensive: a field that reaches it has already
failed the build. `check[T]` recurses alongside the walk it guards, so a nested
record is classified at every depth.

| field shape    | gate                       | what happens                    |
|----------------|----------------------------|---------------------------------|
| union          | `$is_union`                | refused, with a written message |
| reference      | `$is_pointer`              | detected, never followed        |
| record         | `$is_record`               | descended into                  |
| scalar numeric | `$is_integer`, `$is_float` | the derive's leaf action        |
| anything else  | the `$or` fallback         | refused, with a written message |

a scalar numeric is a signed or unsigned integer of any width, or a float. a
`def` over such a scalar counts (its underlying type is what the predicate
sees), so `bool` and `char` fields qualify. the fallback catches arrays,
vectors, and `^` secrets.

adding a derive is the drop-in this shape is for: write the walk with your own
leaf action, call `check[T]` first, and every refusal and message comes with
it. the leaf action is free to allocate or to fail -- `fmt` already
returns a `res` and returns early from any depth -- so a fallible or
allocating member takes its extra parameters and its return type as it needs
them, without the contract changing.

## the descent is recursion, and it terminates structurally

each derive walks one level and re-enters itself at a record field's own type
(`eq[f.type](?a.[f], ?b.[f])`). there is no depth limit and none is needed: a
descent instantiates at a field's type, a record's fields are finite, and a
record cannot contain itself by value -- the compiler refuses that as a
recursive type of infinite size. a self-reference has to go through a pointer,
which is a different type and which `$is_record` does not select.

this replaces a hand-written ladder four levels deep. that bound was never a
design choice, only what could be spelled: mach could not re-enter a generic at
a field's type until briar-systems/mach#2691.

the property does NOT extend to following references. `rec Grow[T] { p:
*Grow[*T]; }` is legal and has unboundedly many distinct instances reachable
through its pointer, so a reference-following derive needs a termination story
this one gets for free. see briar-systems/mach#2693.

## secrets are refused, not skipped

none of these helpers is secrecy-aware. `$is_secret` reports a `^` field, so
a secrecy-aware derive (skip in `fmt`, refuse in `hash`, constant-time compare
in `eq`) can be written, but the derives here never test for one.

what makes that safe rather than silent is that **nothing strips `^`**. type
comparison never did, and since briar-systems/mach#2692 the shape predicates do
not either, so `^u64` fails `$is_integer` and `^Rec` fails `$is_record`.
both fall to the fallback and are refused at comptime, with our message rather
than a raw intrinsic error.

that is why the leaf is a positive classification and the fallback is an `$error`.
under the current predicate rule a walk that ACTED on its fallback would
silently skip a secret instead of refusing it, so the refusal is what makes
"nothing classifies it" a safe answer rather than a dangerous one. inverting
either gate would let secrets through, and `fmt` would print them.

## references are detected, never followed

`$is_pointer` sees a reference, and since briar-systems/mach#2693 (mach 4.15.0)
`$pointee_of` reaches the pointee's shape, so the walk could follow one. it does
not, and that is now a semantic choice rather than a toolchain limit: address
semantics versus deep semantics is the caller's to make, and a deep `clone`
allocates, which means an allocator argument and a failure mode these signatures
do not have. a reference field is refused. note that `str` is `def str: *char`,
so a `str` field is a reference field and is refused with the rest.

## value semantics

equality and hashing follow IEEE-754 through `!=` and a canonical bit fold:
`-0.0` and `+0.0` are equal and hash alike, while a field holding NaN makes a
record never equal to itself (NaN compares unequal to everything).

Source: [`src/derive.mach`](../../src/derive.mach)

Uses types from [`std.io.writer`](io/writer.md).

| Functions | |
| :--- | :--- |
| [`check`](#check) | refuse every field shape the derives here do not walk |
| [`eq`](#eq) | structural equality over a record's fields |
| [`hash`](#hash) | FNV-1a hash over a record's fields |
| [`clone`](#clone) | copy `src` onto `dst` field by field |
| [`fmt`](#fmt) | write a record as `Type{field=value, ...}` to a writer |

---

## Functions

### check

```mach
pub fun check[T]()
```

refuse every field shape the derives here do not walk

this is the classification contract in one place. each derive calls it before
its own walk, so a rejected record fails the build with a message written
against the field shape rather than through whichever intrinsic the leaf action
happened to reach first. it is `pub` so a hand-written derive can hold itself
to the same rule.

the body is entirely comptime: every arm is empty or an `$error`, so an
accepted `T` compiles to an empty function. the release pipeline eliminates the
call; at `-O0` a derive pays one call into it.

| Parameter | |
| :--- | :--- |
| `[T]` | the record type to classify |

### eq

```mach
pub fun eq[T](a: *T, b: *T) bool
```

structural equality over a record's fields

compares `a` and `b` field by field, descending into nested records, and
returns false at the first mismatch. a record with no fields compares equal.
every field must classify (see `check`); a union, a reference, an array, or a
`^` secret is a comptime `$error`.

| Parameter | |
| :--- | :--- |
| `[T]` | the record type to compare |
| `a` | first record |
| `b` | second record |
| **returns** | true when every field, at every depth, compares equal |

### hash

```mach
pub fun hash[T](v: *T) u64
```

FNV-1a hash over a record's fields

folds each field's value into a 64-bit accumulator in declaration order,
descending into nested records so a nested field contributes exactly as a
flattened one would. two records that compare `eq` hash alike, since both walk
the same fields in the same order. eligibility matches `eq`.

| Parameter | |
| :--- | :--- |
| `[T]` | the record type to hash |
| `v` | the record to hash |
| **returns** | the 64-bit hash |

### clone

```mach
pub fun clone[T](dst: *T, src: *T)
```

copy `src` onto `dst` field by field

the value of this over `dst = src` is the refusal, not the copy: a record whose
every field classifies has no field a memberwise copy could get wrong, so
`clone[T]` compiling is the proof that a structural copy is a whole copy.
a field the copy would only shallowly duplicate -- a reference to owned storage
-- does not classify, and the build fails rather than handing back a second
record aliasing the first's memory.

an owning clone, which follows references and therefore allocates and can fail,
is a separate member. briar-systems/mach#2693 (mach 4.15.0) supplies the
traversal it needs, so what it still waits on is a signature carrying an
allocator and an error, not a compiler capability.

| Parameter | |
| :--- | :--- |
| `[T]` | the record type to copy |
| `dst` | destination record, overwritten field by field |
| `src` | source record |

### fmt

```mach
pub fun fmt[T](w: *std.io.writer.Writer, v: *T) res[usize, WriteError]
```

write a record as `Type{field=value, ...}` to a writer

renders each field as `name=value` in declaration order, separated by `, `,
delegating value formatting to `format.write_value`. a nested record renders
as `name=Type{...}`, so `Player{pos=Vec3{x=1, y=2, z=3}, id=7}` is one call.
the type spelling comes from `$type_name`, which is sema's own diagnostic
authority, so a printed name and an error's name cannot drift.

the outcome is the writer's: a failure at any depth returns at once and
carries the bytes this call persisted before it.

**this formatter prints `^` secret fields as ordinary values, and it is not
able to do otherwise.** what saves it today is that a secret field does not
classify, so `check[T]` fails the build rather than letting one through -- see
the module note on secrets. do not read that as a redaction: nothing here
recognizes a secret, and a secrecy-aware `fmt` would have to test
`$is_secret` itself.

eligibility matches `eq` and `hash`.

| Parameter | |
| :--- | :--- |
| `[T]` | the record type to render |
| `w` | target writer |
| `v` | the record to render |
| **returns** | total bytes written, or the writer's failure with the persisted prefix |

