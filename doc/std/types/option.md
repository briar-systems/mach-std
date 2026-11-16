[std](../README.md) / [types](README.md) / **option**

# std.types.option

the canonical option tag: opt[T]

genuine absence is spelled `opt[T]`: an empty container, no match, no
element at an index, an unset variable. it is an ordinary std declaration
(mach doc/design/tagged-values.md fixes the language contract; the compiler
seeds nothing and treats it like any other tag). a consuming module gains
`use std.types.option.opt;` and spells the bare name. the sibling tags live
in `std.types.result` (`res[T, E]`) and `std.types.error` (`err[E]`).

opt[T]: `none` is case 0 and `some: T` is case 1; the zero value reads as
`none`.

the discriminator is a u8 at offset zero and the payload follows at its
natural alignment. the three canonical tags nest freely (`res[opt[T], E]`,
`opt[res[T, E]]`) and instantiate user generics like any declared type.

reading: `sel place.case` is the test, and the guarded payload place is the
read. an `if (!sel o.some) { ret ...; }` chain guards `o.some` for the rest
of the block; `||` opens no guard, so one term per `if`. construction is
`Type.case{...}` only. no helper functions are provided on purpose: a
by-value `unwrap` would copy owning payloads out of the ownership rules,
and a constructor function would be a second spelling of a form the
language already has. the test below pins the shape: case order, case
codes, zero defaults, layout and reflection.

Source: [`src/types/option.mach`](../../../src/types/option.mach)

| Type | | |
| :--- | :--- | :--- |
| [`opt`](#opt) | `tag` |  |

---

## opt

```mach
pub tag opt[T]: u8 { none; some: T; }
```

