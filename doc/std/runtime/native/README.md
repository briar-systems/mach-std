[std](../../README.md) / [runtime](../README.md) / **native**

# std.runtime.native

the process arguments as the host passed them, before any conversion

main's argv is UTF-8 on every host. on linux, darwin and wasi it is the bytes the
host passed, so the native view holds the same arguments. on windows argv is
converted from the wide command line and an unpaired surrogate, which a file
name may hold, becomes U+FFFD, so such a name does not survive in argv. the
native view there holds each argument as the UTF-16 code units the command
line held, split by the same walker as argv (std.runtime.windows.cmdline), so
both views have the same count and each index names the same argument.

a program that must reopen a name exactly as it was given reads it here, in
the host's own units, through one shape on every host. the runtime that owns
the arguments keeps the view and is its only writer, so it is read only here
and lives as long as the process.

The directory's root module is [`std.runtime.native`](../native.md).

| Module | |
| :--- | :--- |
| [`view`](view.md) | the shape of the native argument view, shared by std.runtime.native and the runtimes that own the arguments |

