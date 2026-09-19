# Mach Standard Library

The standard library for the Mach programming language.

## Installation

Add std as a dependency in your project's `mach.toml`:

```toml
[dep.std]
git = "https://github.com/briar-systems/mach-std"
ref = "tag/v5.7.1"
```

Or with the dependency manager:

```bash
mach dep add . std --git https://github.com/briar-systems/mach-std --ref tag/v5.7.1
```

## Support

std 5.x requires mach 5.5.2 or later. It is tested on linux (x86_64, arm64, riscv64), darwin (x86_64, aarch64) and windows (x86_64). Its OS-free core also builds for freestanding targets.

std follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See the [changelog](./CHANGELOG.md).

## API surface

The semantic versioning promise covers the driver and library modules, such as `std.net.async` and `std.net.async.local`. Code that uses only those keeps building across minor and patch releases.

std is designed so that callers can reach past a driver when it does not give them what they need, and doing so is expected. The only thing to know is what the version number covers. The `net.async` backend modules are outside the promise:

- `std.net.async.linux` (`src/net/async/linux.mach`)
- `std.net.async.darwin` (`src/net/async/darwin.mach`)
- `std.net.async.windows` (`src/net/async/windows.mach`)
- `std.net.async.iocp` (`src/net/async/iocp.mach`)
- `std.net.async.iocp.port` (`src/net/async/iocp/port.mach`)
- `std.net.async.local.unix` (`src/net/async/local/unix.mach`)
- `std.net.async.local.windows` (`src/net/async/local/windows.mach`)

Their signatures may change in a minor release. If you call one directly, check the CHANGELOG when you upgrade.

The reason: each backend is compiled for its own target only, so exactly one backend exists in any build, and the driver above it owns the portable contract. This list is exactly what was ruled on and says nothing about other modules.

std 5.3.0 is the release that raised the question: #793 changed the backend `cancel` signatures and shipped as a minor release, with the change named in its own CHANGELOG entry. The owner then approved this rule.

## Documentation

- API documentation lives in the module doc comments under [src](./src). Run `mach doc` to render it.
- [CHANGELOG.md](./CHANGELOG.md): release changes.
- [MIGRATION.md](./MIGRATION.md): upgrading across major versions.
- [OS-CONTRACT.md](./OS-CONTRACT.md): the `std.system.os` primitive contract.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
