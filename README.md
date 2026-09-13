# Mach Standard Library

This repository contains the canonical standard library for the Mach programming language.

## Installation

To use the standard library in your Mach project, you can include it as a dependency in your project's configuration file:

```toml
[dep.std]
git = "https://github.com/briar-systems/mach-std"
ref = "tag/v1.0.0"
```

You can also use the Mach dependency manager to add it to your project:

```bash
mach dep add std --git https://github.com/briar-systems/mach-std --ref tag/v1.0.0
```

## Versioning

Starting with 1.0.0, releases follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).
The public API consists of public declarations in shipped modules under `src`,
including their signatures, exposed type layouts, documented behavior, ownership,
lifetimes and error contracts on supported targets. Test-only modules and private
implementation helpers are excluded.

- Incompatible public API changes increment the major version.
- Compatible additions and public API deprecations increment the minor version.
- Compatible bug fixes increment the patch version.

A published version's source and tag are immutable. Release tags must match
`mach.toml`. Each release documents its supported compiler and target combinations.
Changes that invalidate an existing supported combination require a major release.
Version compatibility does not silently move an application's dependency pin.

Std 1.0.1 is the audited dependency for the Mach 4.30.0 implementation. Its
compiler release was withdrawn. CI builds that implementation from published
4.26.5 and fixed source commits reachable from main, then requires identical
final self-builds. See the [source bootstrap recipe](https://github.com/briar-systems/mach/blob/dev/doc/tooling/bootstrap.md). The breaking language and API
migration for Mach v5 is planned as std 2.0.0. Compiler and std version numbers
are independent.

## Documentation

API documentation lives alongside the implementation in [src](./src).

See the [changelog](./CHANGELOG.md) for release changes and migration requirements.

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

### Local byte-stream receive ownership

A local Stream has one closing owner. Its receive queue must be exclusively
borrowed across each read, including any raw or duplicated handle aliases.
Concurrent receive, receive shutdown or close through another alias is invalid.
Peer writes and operations on unrelated descriptors may run concurrently.

`net.local.stream_read` and the local async backend's reads deliver bytes only.
A peer may attach descriptor rights to those bytes; the stream never hands them
to the caller, and each platform has its own way of making sure they cannot
occupy the caller's descriptor table:

- Linux receives through `recvmsg(MSG_CMSG_CLOEXEC)` with control storage sized
  for the kernel's descriptor bound (`SCM_MAX_FD`, 253, plus the credential
  records `SO_PASSCRED` and `SO_PASSPIDFD` can prepend) and closes every
  `SCM_RIGHTS` and `SCM_PIDFD` descriptor the storage reports. The bytes arrive
  and the count is the outcome. A native failure after the kernel installed
  rights is still walked, because the storage is zero-filled before the call and
  the kernel writes records before it fails. `MSG_CTRUNC` means the kernel dropped
  records it could not report, and it installs no descriptor it does not report,
  so the walk over the reported ones is complete. `std.system.os.linux.
  sock_recv_close_rights` is that primitive with caller-supplied storage;
  `local_stream_recv` supplies the bound.
- Darwin inspects without consuming (`MSG_PEEK` with one control header), refuses
  any ancillary data or truncation with `UNSUPPORTED`, and otherwise consumes at
  most the inspected byte count. Zero-length reads do not inspect the queue. A
  refusal leaves the socket open and its queued rights owned by that socket; the
  caller must still close the stream, which releases them. Native failures retain
  their cause. Buffer contents on failure are unspecified.
- Windows has no descriptor rights on local sockets; reads are plain.

The local async backend reads under its existing read lane ownership with the
same platform mechanism. Its buffer remains borrowed until completion. A Darwin
refusal completes with zero delivered bytes and does not close the stream. The
generic Linux and Darwin async backends accept only IPv4/IPv6 socket handles,
checked before registration, so a local handle cannot reach a byte path that
does not own rights. Use the local backend for local streams. Raw OS `sock_recv`
and `sock_receive_message` retain native ancillary behavior and do not provide
this byte-only contract.

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
