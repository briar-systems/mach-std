[std](../../README.md) / [runtime](../README.md) / [linux](README.md) / **reloc**

# std.runtime.linux.reloc

static-PIE self-relocation

Source: [`src/runtime/linux/reloc.mach`](../../../../src/runtime/linux/reloc.mach)

| Functions | |
| :--- | :--- |
| [`_rt_relocate`](#_rt_relocate) | apply the image's ELF RELATIVE relocations, sliding each by the load bias recovered from the kernel auxiliary vector |
| [`relro_reprotect`](#relro_reprotect) | re-protect the RELRO region read-only, or abort naming the violated invariant |

---

## Functions

### _rt_relocate

```mach
#[symbol("_rt_relocate")]
pub fun _rt_relocate(envp: *usize)
```

apply the image's ELF RELATIVE relocations, sliding each by the load bias recovered
from the kernel auxiliary vector

`envp` points at the program's environment vector: envp[0..] then a NULL, immediately
after which the kernel placed the auxv (type/value word pairs terminated by AT_NULL).
PIC by construction - only `envp`, the region it points into, and computed addresses
are touched - so it runs correctly before any relocation is applied.

| Parameter | |
| :--- | :--- |
| `envp` | the program's envp pointer (the value `_start` stored into `_rt_envp`) |

### relro_reprotect

```mach
pub fun relro_reprotect(relro_start: u64, relro_sz: u64, at_pagesz: u64)
```

re-protect the RELRO region read-only, or abort naming the violated invariant

The region holds the relocated constants (`.data.rel.ro`: vtables, `val` pointer
globals, `str` literals) mapped writable for the relocation pass; once the RELATIVE
slots are slid it must be restored read-only before `main`. `relro_sz` is the region's
actual mapped extent from its first page; this function rounds it
UP to the runtime page - the pages the kernel mapped - and mprotects exactly those. The
rounding lives here, against AT_PAGESZ, rather than at the writer against the image
max-page: a build-time max-page larger than the runtime page would otherwise overshoot
the mapping and fault ENOMEM (briar-systems/mach#1885).

Re-protection is fatal on any failure (the glibc stance, matching
`std.system.os.page_size`'s AT_PAGESZ precedent, #336/#343): an absent AT_PAGESZ, a
region with no mapped extent, a non-page-aligned start, or an mprotect failure is a
broken environment or a violated layout contract, and running unhardened would silently
mask it. No silent-unhardened path remains.

Reached only after relocation (it uses panic + the syscall path), so its message
pointers are already slid; `_rt_relocate` invokes it once the RELATIVE slots are applied.

| Parameter | |
| :--- | :--- |
| `relro_start` | the runtime start of the region's first page |
| `relro_sz` | the region's mapped extent from `relro_start` |
| `at_pagesz` | the runtime page size from AT_PAGESZ (0 when the auxv lacked it) |

