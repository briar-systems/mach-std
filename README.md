# Mach Standard Library

The standard library for the Mach programming language.

## Installation

Add std as a dependency in your project's `mach.toml`:

```toml
[dep.std]
git = "https://github.com/briar-systems/mach-std"
ref = "tag/v5.3.0"
```

Or with the dependency manager:

```bash
mach dep add . std --git https://github.com/briar-systems/mach-std --ref tag/v5.3.0
```

## Support

std 5.x requires mach 5.3.0 or later. It is tested on linux (x86_64, arm64, riscv64), darwin (x86_64, aarch64) and windows (x86_64). Its OS-free core also builds for freestanding targets.

std follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See the [changelog](./CHANGELOG.md).

## API surface

The semantic versioning promise covers std's public API: the driver and library modules that callers are expected to use, such as `std.net.async` and `std.net.async.local`. Code that uses those modules keeps building across minor and patch releases.

The `net.async` backend modules are implementation, not API:

- `std.net.async.linux` (`src/net/async/linux.mach`)
- `std.net.async.darwin` (`src/net/async/darwin.mach`)
- `std.net.async.windows` (`src/net/async/windows.mach`)
- `std.net.async.iocp` (`src/net/async/iocp.mach`)
- `std.net.async.iocp.port` (`src/net/async/iocp/port.mach`)
- `std.net.async.local.unix` (`src/net/async/local/unix.mach`)
- `std.net.async.local.windows` (`src/net/async/local/windows.mach`)

They are `pub` only because a driver has to reach them and Mach has no narrower visibility, not because they are a supported entry point. Their signatures may change in a minor release. Code that calls a backend directly is not covered by the promise.

The reason is structural. Each backend is compiled for its own target only, so exactly one backend exists in any build, and the driver above it owns the portable contract that callers rely on. A backend's signature is the driver's private arrangement with that one target. To decide whether a module not listed here falls under the same rule, ask whether it exists only to serve a driver that owns a portable contract, and whether only one variant of it is ever built for a target. This list is exactly what was ruled on. Other modules are not covered by it until they are ruled on.

std 5.3.0 is the release that raised the question: #793 changed the backend `cancel` signatures and shipped as a minor release, with the change named in its own CHANGELOG entry. The owner then approved this rule.

## Documentation

- API documentation lives in the module doc comments under [src](./src). Run `mach doc` to render it.
- [CHANGELOG.md](./CHANGELOG.md): release changes.
- [MIGRATION.md](./MIGRATION.md): upgrading across major versions.
- [OS-CONTRACT.md](./OS-CONTRACT.md): the `std.system.os` primitive contract.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
