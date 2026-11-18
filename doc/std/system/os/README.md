[std](../../README.md) / [system](../README.md) / **os**

# std.system.os

the OS contract: a small set of primitives, one implementation per OS

the primitives fall into capability groups (core, pages, clock, entropy,
threads, files, io queue, sockets, process). std.system.capability says which
groups a target provides, and a target that claims a group exports every
member of it. OS-CONTRACT.md lists the members and the assumptions the
contract holds. for platform-specific functionality, import the target module
directly (e.g. std.system.os.linux).

The directory's root module is [`std.system.os`](../os.md).

| Module | |
| :--- | :--- |
| [`darwin`](darwin.md) | darwin OS interface with ISA dispatch |
| [`errors`](errors.md) | the portable reading of a native code, written once over the selected OS's codes |
| [`linux`](linux.md) | linux OS interface with ISA dispatch |
| [`secret`](secret.md) | native primitives for secret-welded storage |
| [`shared`](shared.md) | abstract types and constants for the OS interface |
| [`tests`](tests.md) | import-attribution census for the two-level-namespace targets |
| [`wasi`](wasi.md) | wasi OS interface with one implementation per preview |
| [`windows`](windows.md) | windows OS interface with ISA dispatch |

| Directory | |
| :--- | :--- |
| [`darwin/`](darwin/README.md) | darwin OS interface with ISA dispatch |
| [`linux/`](linux/README.md) | linux OS interface with ISA dispatch |
| [`wasi/`](wasi/README.md) | wasi OS interface with one implementation per preview |
| [`windows/`](windows/README.md) | windows OS interface with ISA dispatch |

