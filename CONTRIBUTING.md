# Contributing

Bug reports and feature requests are welcome as GitHub issues. To contribute code, fork the repository and open a pull request against `dev`.

## Versioning

Releases follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

The public API is every public declaration in the shipped modules under `src`. That covers their signatures, the type layouts they expose, and their documented behaviour, ownership, lifetimes and error contracts on supported targets. Test-only modules and private implementation helpers are not part of it.

- An incompatible public API change increments the major version.
- A compatible addition or public API deprecation increments the minor version.
- A compatible bug fix increments the patch version.

A published version's source and tag are immutable, and a release tag must match `mach.toml`. Each release documents the compiler and targets it supports. A change that invalidates an existing supported combination needs a major release. Version compatibility never silently moves an application's dependency pin.

## Compiler and CI

CI builds and tests std with the mach release pinned for the whole family in [briar-systems/.github](https://github.com/briar-systems/.github), downloaded and verified against its `SHA256SUMS`. Releases run through that repository's shared release workflow. std and compiler version numbers are independent.
