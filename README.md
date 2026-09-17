# Mach Standard Library

The standard library for the Mach programming language.

## Installation

Add std as a dependency in your project's `mach.toml`:

```toml
[dep.std]
git = "https://github.com/briar-systems/mach-std"
ref = "tag/v4.0.1"
```

Or with the dependency manager:

```bash
mach dep add . std --git https://github.com/briar-systems/mach-std --ref tag/v4.0.1
```

## Support

std 4.x requires mach 5.2.0 or later. It is tested on linux (x86_64, arm64, riscv64), darwin (x86_64, aarch64) and windows (x86_64). Its OS-free core also builds for freestanding targets.

std follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See the [changelog](./CHANGELOG.md).

## Documentation

- API documentation lives in the module doc comments under [src](./src). Run `mach doc` to render it.
- [CHANGELOG.md](./CHANGELOG.md): release changes.
- [MIGRATION.md](./MIGRATION.md): upgrading across major versions.
- [OS-CONTRACT.md](./OS-CONTRACT.md): the `std.system.os` primitive contract.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
