# Freestanding build ratchet

`verify.sh` builds every std module (depth one and two under `src/`, excluding
`lib/`) for `freestanding-x86_64` (`os = "freestanding"`, `of = "elf"`) from a
probe that only imports it. It then compares the modules that build with
`expected-pass.txt`, which must match exactly.

The check fails when:

- a listed module no longer builds, and the first errors are printed
- a module builds but is not listed
- a listed module does not exist
- a module that does not build fails with anything other than exactly one
  `error:` line saying what it `needs` (a capability from
  `std.system.capability`, or a target)

```sh
bash test/freestanding/verify.sh [mach]
```

An OS-bound module gates its OS-bound imports on the capability flags it uses
directly and refuses in the `$or` branch, for example:

```mach
$if (capability.HAS_FILES) {
    use std.system.os;
}
$or {
    $error("std.filesystem needs the files capability (std.system.capability.HAS_FILES)");
}
```

When a change makes more modules build, add them to `expected-pass.txt` in the
same change. The steps of the std OS layering epic (#697) grow this list. A
module leaves it only through a deliberate, reviewed change.

`FREESTANDING_JOBS` sets how many builds run in parallel (default `nproc`,
capped at 4).
