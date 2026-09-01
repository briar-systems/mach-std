# Mach Standard Library

This repository contains the canonical standard library for the Mach programming language.

## Installation

To use the standard library in your Mach project, you can include it as a dependency in your project's configuration file:

```toml
[deps.mach-std]
git = "https://github.com/briar-systems/mach-std"
ref = "tag/v0.34.0"
```

You can also use the Mach dependency manager to add it to your project:

```bash
mach dep add mach-std --git https://github.com/briar-systems/mach-std --ref tag/v0.34.0
```

## Documentation

The documentation for the Mach Standard Library can be found in the [doc](./doc) directory.

> NOTE: The documentation is currently a work in progress and the API is rapidly changing.
> Please refer to the source code for the most up-to-date information.

### I/O ownership queries

`std.io.runtime.aliases`, `std.net.async.aliases`, and
`std.net.async.local.aliases` report whether a public byte range overlaps an
owner descriptor or any backing storage reachable through it. Network driver
queries include the selected platform backend and the borrowed runtime.

The queries are read-only and allocation-free. Ownership-defining pointers and
capacities, plus the queried range descriptor, must remain immutable for the
duration of a query. A caller may query while ordinary operations are active
because those fields do not change, but must synchronize initialization and
destruction.

A non-empty malformed range, uninitialized owner, partially initialized owner,
partially torn-down owner, or destroyed owner reports overlap. An empty range
owns no bytes and reports no overlap. Range validation uses inclusive endpoints,
so a one-byte range at `usize::MAX` is valid while any range extending beyond it
is malformed and reports overlap.

### Secret-welded operating-system storage

`std.system.os.secret_allocate`, `secret_deallocate`, and
`secret_random_fill` keep storage typed as `*^u8` across the complete native
boundary. They never create a public pointer or integer alias to the secret
bytes. `secret_allocate_typed[T]` and `secret_deallocate_typed[T]` preserve the
exact `*T` shape for records with deeply secret fields. Linux uses direct
syscalls without libc, Darwin uses libSystem, and Windows uses the stable
virtual-memory and system-entropy APIs.
The Windows entropy boundary requires Vista SP2 or later for
`BCRYPT_USE_SYSTEM_PREFERRED_RNG`.

Allocation returns zero-initialized storage, or nil for zero bytes or failure.
Deallocation wipes the complete logical span before native release and returns
zero only after releasing the original allocation, except that `(nil, 0)` is a
successful no-op. A failed release leaves zeroed storage owned by the caller.
Random fill returns zero only after initializing the complete requested range
and wipes that complete range before returning any error.

Typed allocation checks the complete `count * $size_of(T)` geometry and honors
`$align_of(T)`, including over-aligned records. Typed deallocation requires the
original element count, validates the stored allocation geometry, and wipes all
bytes in every element, including padding, before native release.

The `^` qualifier enforces secret data flow. These primitives do not lock pages,
exclude them from swap or process dumps, isolate them across process creation,
add guard pages, or resist a debugger with process access.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.
