[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / **darwin**

# std.system.os.darwin

darwin OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need darwin-specific functionality import this module
directly rather than going through std.system.os.

The directory's root module is [`std.system.os.darwin`](../darwin.md).

| Module | |
| :--- | :--- |
| [`aarch64`](aarch64.md) | aarch64-specific darwin OS primitives |
| [`libsystem`](libsystem.md) | libSystem imports for the darwin backend |
| [`shared`](shared.md) | code shared across all darwin ISA implementations |
| [`x86_64`](x86_64.md) | x86_64-specific darwin OS primitives |

