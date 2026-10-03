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

CI installs the mach release named by `MACH_VERSION` in `.github/workflows/ci.yml` and runs `mach fmt --check .` and `mach test . --all` on linux. A release tag runs `.github/workflows/cd.yml`, which tests every host std ships to and publishes the release. The suites under `test/` run locally, not in CI. std and compiler version numbers are independent.

## Tests

`mach test .` runs the tests of every module the library reaches. `mach test . -a tests` runs the rest, from the modules `src/lib/tests.mach` reaches. `mach test . --all` runs both. A new module that holds tests and that the library does not reach on some target goes in `src/lib/tests.mach`. `test/selections/verify.sh` fails until it does.
