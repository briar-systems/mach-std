# Mach Standard Library

This repository contains the cannonical standard library for the Mach programming language.

## Installation

To use the standard library in your Mach project, you can include it as a dependency in your project's configuration file:

```toml
[deps.mach-std]
git = "https://github.com/briar-systems/mach-std"
ref = "branch/main"
```

You can also use the Mach dependency manager to add it to your project:

```bash
mach dep add mach-std --git https://github.com/briar-systems/mach-std --ref branch/main
```

## Documentation

The documentation for the Mach Standard Library can be found in the [docs](./doc) directory.
```zsh
mach doc .
```

> NOTE: The documentation is currently a work in progress and the API is rapidly changing.
> Please refer to the source code for the most up-to-date information.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.
