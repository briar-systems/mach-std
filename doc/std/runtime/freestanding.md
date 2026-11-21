[std](../README.md) / [runtime](README.md) / **freestanding**

# std.runtime.freestanding

freestanding program entrypoint, dispatched by architecture

bare metal has no loader to set a stack, place data or pass arguments, so the
one `_start` of each architecture does that work in asm before any mach code
runs: it points the stack at `__run_stop_.stack`, copies `.data` from where it
loads to where it runs, zeroes `.bss`, calls `main(0, nil)`, and parks the core
when main returns, since there is no process to exit.

a wasm module is the exception: its host instantiates it with the stack and
data the link laid out, so std.runtime.freestanding.wasm32's `_start` is plain
mach that calls main, and a module that uses no std.runtime has no entry.

`_start` lies in a section of its own, `.start`, so a manifest that names it
first in an artifact's `sections` or a region's `run` lays it at the image's
first byte, where a loader of a flat image, which records no entry, enters.

the linker defines the section boundaries the entry reads (mink#526): for an
output section named `S`, `__run_start_S` and `__run_stop_S` bound where it
runs and `__load_start_S` names where its bytes load. the manifest places
`.data` and `.bss`, and mink lays out the `.stack` region at the size the
artifact's stack keys state, so std states no stack size of its own.

Source: [`src/runtime/freestanding.mach`](../../../src/runtime/freestanding.mach)

