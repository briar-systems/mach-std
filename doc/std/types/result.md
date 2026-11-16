[std](../README.md) / [types](README.md) / **result**

# std.types.result

the canonical result tag: res[T, E]

a fallible operation with a value is spelled `res[T, E]`. it is an ordinary
std declaration (mach doc/design/tagged-values.md fixes the language
contract; the compiler seeds nothing and treats it like any other tag). a
consuming module gains `use std.types.result.res;` and spells the bare name.
the sibling tags live in `std.types.option` (`opt[T]`) and
`std.types.error` (`err[E]`).

res[T, E]: `err: E` is case 0 and `ok: T` is case 1; `E` is the producing
module's closed domain tag, never a string. the zero value reads as `err`
with a zero error, so uninitialized storage never reads as success.

the discriminator is a u8 at offset zero and the payload follows at its
natural alignment. the three canonical tags nest freely (`res[opt[T], E]`,
`res[T, Tag]`) and instantiate user generics like any declared type.

reading: `sel place.case` is the test, and the guarded payload place is the
read. an `if (!sel r.ok) { ret ...; }` chain guards `r.ok` for the rest of
the block; `||` opens no guard, so one term per `if`. construction is
`Type.case{...}` only. no helper functions are provided on purpose: a
by-value `unwrap` would copy owning payloads out of the ownership rules,
and a constructor function would be a second spelling of a form the
language already has. the test below pins the shape: case order, case
codes, zero defaults, layout and reflection.

Source: [`src/types/result.mach`](../../../src/types/result.mach)

| Type | | |
| :--- | :--- | :--- |
| [`res`](#res) | `tag` |  |

---

## res

```mach
pub tag res[T, E]: u8 { err: E; ok: T; }
```

