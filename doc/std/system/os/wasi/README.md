[std](../../../README.md) / [system](../../README.md) / [os](../README.md) / **wasi**

# std.system.os.wasi

wasi OS interface with one implementation per preview

forwards the complete surface of the selected row. mach names one environment
of the wasi system, preview1, so one row is selected here, and a later preview
is its own module beside std.system.os.wasi.preview1 exporting this surface,
selected on this line and given its capability row in std.system.capability.

The directory's root module is [`std.system.os.wasi`](../wasi.md).

| Module | |
| :--- | :--- |
| [`preview1`](preview1.md) | the os contract over wasi preview 1 |
| [`shared`](shared.md) | what every wasi row shares: the contract's constants, the native codes and the pages of linear memory |

