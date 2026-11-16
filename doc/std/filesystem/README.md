[std](../README.md) / **filesystem**

# std.filesystem

filesystem access over the platform namespace

three layers: handle operations on an open File; whole-file convenience
composing std.io (a File adapts to a Reader/Writer, so content flows through
io.read_all/read_exact/write_all rather than hand-rolled loops); and
namespace operations on a Path.

outcomes are the canonical tags. a handle operation and a single native
namespace effect report io_error.Error; a composite operation reports
FsError, which names the step that refused; the existence queries answer
res[bool, io_error.Error], where a missing path is a successful false.

a Path is UTF-8. the *_native calls take a name in std.runtime.native units
instead, UTF-16 on windows and bytes on linux and darwin, such as an
argument from std.runtime.native, and hand it to the OS unchanged. on
windows a name that is not valid UTF-8, one holding an unpaired surrogate,
is reached only through them. a Path is already the native name on linux
and darwin, and on windows it is converted once and then takes the native
call's path to the kernel.

The directory's root module is [`std.filesystem`](../filesystem.md).

| Module | |
| :--- | :--- |
| [`native`](native.md) | filesystem helpers built on the os contract's stat, unlink and environment |
| [`removal`](removal.md) | descriptor-relative recursive removal shared by namespace and transaction callers |
| [`transaction`](transaction.md) | cooperative filesystem publication with explicit session ownership |

| Directory | |
| :--- | :--- |
| [`transaction/`](transaction/README.md) | cooperative filesystem publication with explicit session ownership |

