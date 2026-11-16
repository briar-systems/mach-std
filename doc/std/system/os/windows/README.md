[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / **windows**

# std.system.os.windows

windows OS interface with ISA dispatch

forwards the complete surface from the selected ISA backend.
consumers who need windows-specific functionality import this module
directly rather than going through std.system.os.

The directory's root module is [`std.system.os.windows`](../windows.md).

| Module | |
| :--- | :--- |
| [`aarch64`](aarch64.md) | aarch64-specific windows OS primitives |
| [`shared`](shared.md) | code shared across all windows ISA implementations |
| [`x86_64`](x86_64.md) | x86_64-specific windows OS primitives |

