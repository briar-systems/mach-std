[std](README.md) / **filesystem**

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

Source: [`src/filesystem.mach`](../../src/filesystem.mach)

Uses types from [`std.allocator`](allocator.md), [`std.filesystem.removal`](filesystem/removal.md), [`std.io.error`](io/error.md), [`std.io.handle`](io/handle.md), [`std.io.reader`](io/reader.md), [`std.io.writer`](io/writer.md).

| Type | | |
| :--- | :--- | :--- |
| [`File`](#file) | `rec` | an open file with a native-width opaque handle |
| [`FsError`](#fserror) | `tag` | why a composite filesystem operation refused |
| [`Kind`](#kind) | `def` | what a path resolves to |
| [`Metadata`](#metadata) | `rec` | portable file metadata |
| [`SecretBytes`](#secretbytes) | `rec` | a file's bytes in secret-welded storage |
| [`Listed`](#listed) | `tag` | one read_dir entry: its name in UTF-8, or, for an entry with no UTF-8 spelling, which only a windows directory can hold, its name in native units (std.runtime.native.view.NativeName) so the native forms can reach it |
| [`TempFile`](#tempfile) | `rec` | a created temporary file and its path |
| [`NativeTempFile`](#nativetempfile) | `rec` | a created temporary file named in native units |

| On `File` | |
| :--- | :--- |
| [`STDIN`](#file) | the standard streams, as already-open files |
| [`STDOUT`](#file), [`STDERR`](#file) | |
| [`open`](#open) | open a file for reading |
| [`open_native`](#open_native) | open a file for reading by a name in native units |
| [`create`](#create) | create or truncate a file for writing |
| [`create_native`](#create_native) | create or truncate a file for writing by a name in native units |
| [`close`](#close) | close an open file; the handle is invalid afterwards whatever the outcome |
| [`sync`](#sync) | flush an open file's data and metadata to its backing storage |
| [`read`](#read) | read up to len bytes into buf |
| [`write`](#write) | write up to len bytes from buf |
| [`seek`](#seek) | reposition the file offset |
| [`reader`](#reader) | adapt a file to an io.Reader (the file must outlive the reader) |
| [`writer`](#writer) | adapt a file to an io.Writer (the file must outlive the writer) |
| [`read_secret_of`](#read_secret_of) | read an entire open file straight into secret-welded storage |
| [`identity_of`](#identity_of) | observations do not retain an object or imply unchanged contents |
| [`stat_of`](#stat_of) | metadata for an open file |

| On `FsError` | |
| :--- | :--- |
| [`read_bytes`](#read_bytes) | read an entire file into an allocated byte buffer |
| [`read_bytes_native`](#read_bytes_native) | read_bytes for a name in native units |
| [`read_string`](#read_string) | read an entire file into an allocated, null-terminated string |
| [`read_string_native`](#read_string_native) | read_string for a name in native units |
| [`write_bytes`](#write_bytes) | write bytes to a file, creating or truncating it |
| [`write_bytes_native`](#write_bytes_native) | write_bytes for a name in native units |
| [`replace_bytes_atomic`](#replace_bytes_atomic) | replace a file with complete bytes through a durable sibling temporary |
| [`replace_bytes_atomic_native`](#replace_bytes_atomic_native) | replace_bytes_atomic for a name in native units |
| [`read_dir`](#read_dir) | list the entries of a directory, excluding "." and ".." |
| [`read_dir_native`](#read_dir_native) | read_dir for a directory named in native units, every entry named in them |
| [`create_dir_all`](#create_dir_all) | create a directory and every missing parent (mkdir -p) |
| [`create_dir_all_native`](#create_dir_all_native) | create_dir_all for a name in native units, its parents walked in the same units |
| [`remove_all`](#remove_all) | recursively remove a file, directory tree, or symbolic link (rm -rf) |
| [`remove_all_native`](#remove_all_native) | remove_all for a name in native units |

| On `Kind` | |
| :--- | :--- |
| [`KIND_OTHER`](#kind), [`KIND_FILE`](#kind), [`KIND_DIR`](#kind), [`KIND_SYMLINK`](#kind) | |

| On `Metadata` | |
| :--- | :--- |
| [`metadata`](#metadata-1) | metadata for a path, following a final symbolic link |
| [`metadata_native`](#metadata_native) | metadata for a name in native units, following a final symbolic link |
| [`metadata_link`](#metadata_link) | metadata for a path without following a final symbolic link |
| [`metadata_link_native`](#metadata_link_native) | metadata_link for a name in native units |
| [`meta_is_dir`](#meta_is_dir) | check whether metadata describes a directory |
| [`meta_is_file`](#meta_is_file) | check whether metadata describes a regular file |
| [`meta_is_symlink`](#meta_is_symlink) | check whether metadata describes a symbolic link |

| On `SecretBytes` | |
| :--- | :--- |
| [`read_secret`](#read_secret) | read an entire file by path straight into secret-welded storage |
| [`read_secret_native`](#read_secret_native) | read_secret for a name in native units |

| On `Listed` | |
| :--- | :--- |
| [`listed_dnit`](#listed_dnit) | release a read_dir result: every name, then the vector |

| On `TempFile` | |
| :--- | :--- |
| [`temp_create`](#temp_create) | create a uniquely named temporary file under the OS temp directory |
| [`temp_path`](#temp_path) | the path of a temporary file |
| [`temp_close`](#temp_close) | close a temporary file without removing it |
| [`temp_remove`](#temp_remove) | remove a temporary file from disk |
| [`temp_close_and_remove`](#temp_close_and_remove) | close and remove a temporary file; both effects run, and a close failure is reported first with the removal's refusal beside it |

| On `NativeTempFile` | |
| :--- | :--- |
| [`temp_create_native`](#temp_create_native) | create a uniquely named temporary file under the OS temp directory, named in native units from temp_dir_native, so a temp directory whose path has no UTF-8 spelling still holds it |
| [`temp_remove_native`](#temp_remove_native) | remove a native temporary file from disk |
| [`temp_close_and_remove_native`](#temp_close_and_remove_native) | close and remove a native temporary file, as temp_close_and_remove does |

| Functions | |
| :--- | :--- |
| [`identity_equal`](#identity_equal) | |
| [`identity_link`](#identity_link) | the final symlink itself is observed and unsupported domains remain explicit |
| [`identity_link_native`](#identity_link_native) | identity_link for a name in native units |
| [`exists`](#exists) | check whether a path exists (as any entry, including a broken symlink) |
| [`exists_native`](#exists_native) | exists for a name in native units |
| [`is_file`](#is_file) | check whether a path is an existing regular file (following symlinks) |
| [`is_file_native`](#is_file_native) | is_file for a name in native units |
| [`is_dir`](#is_dir) | check whether a path is an existing directory (following symlinks) |
| [`is_dir_native`](#is_dir_native) | is_dir for a name in native units |
| [`is_symlink`](#is_symlink) | check whether a path is a symbolic link (not following it) |
| [`is_symlink_native`](#is_symlink_native) | is_symlink for a name in native units |
| [`create_dir`](#create_dir) | create a single directory |
| [`create_dir_native`](#create_dir_native) | create a single directory by a name in native units |
| [`remove_file`](#remove_file) | remove a single file or symbolic link |
| [`remove_file_native`](#remove_file_native) | remove a single file or symbolic link by a name in native units |
| [`remove_dir`](#remove_dir) | remove an empty directory |
| [`remove_dir_native`](#remove_dir_native) | remove an empty directory by a name in native units |
| [`rename`](#rename) | rename or move a file or directory |
| [`rename_native`](#rename_native) | rename or move by names in native units, as rename does |
| [`symlink`](#symlink) | create a symbolic link at linkpath pointing to target |
| [`symlink_native`](#symlink_native) | create a symbolic link by names in native units, as symlink does |
| [`native_names_dnit`](#native_names_dnit) | release a read_dir_native result: every name, then the vector |

| Forwards | |
| :--- | :--- |
| [`Identity`](#identity) | |
| [`SEEK_SET`](#seek_set) | seek anchors for `seek` |
| [`SEEK_CUR`](#seek_cur), [`SEEK_END`](#seek_end) | |

---

## File

```mach
pub rec File {
    handle: std.io.handle.FileHandle;
}
```

an open file with a native-width opaque handle

| Name | Value | |
| :--- | :--- | :--- |
| `STDIN` | `File{handle: io_handle.FileHandle{value: 0}}` | the standard streams, as already-open files |
| `STDOUT` | `File{handle: io_handle.FileHandle{value: 1}}` |  |
| `STDERR` | `File{handle: io_handle.FileHandle{value: 2}}` |  |

### open

```mach
pub fun open(p: Path) res[File, std.io.error.Error]
```

open a file for reading

| Parameter | |
| :--- | :--- |
| `p` | file path |
| **returns** | the open file, or the native refusal |

### open_native

```mach
pub fun open_native(name: *Unit) res[File, std.io.error.Error]
```

open a file for reading by a name in native units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name, as std.runtime.native gives an argument |
| **returns** | the open file, or the native refusal |

### create

```mach
pub fun create(p: Path, mode: i32) res[File, std.io.error.Error]
```

create or truncate a file for writing

| Parameter | |
| :--- | :--- |
| `p` | file path |
| `mode` | permission bits for a newly created file |
| **returns** | the open file, or the native refusal |

### create_native

```mach
pub fun create_native(name: *Unit, mode: i32) res[File, std.io.error.Error]
```

create or truncate a file for writing by a name in native units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name in native units |
| `mode` | permission bits for a newly created file |
| **returns** | the open file, or the native refusal |

### close

```mach
pub fun close(f: *File) err[std.io.error.Error]
```

close an open file; the handle is invalid afterwards whatever the outcome

| Parameter | |
| :--- | :--- |
| `f` | file to close |
| **returns** | ok, or the native refusal (a closed handle is EBADF) |

### sync

```mach
pub fun sync(f: File) err[std.io.error.Error]
```

flush an open file's data and metadata to its backing storage

| Parameter | |
| :--- | :--- |
| `f` | file to flush |
| **returns** | ok, or the native refusal |

### read

```mach
pub fun read(f: File, buf: *u8, len: usize) res[usize, std.io.error.Error]
```

read up to len bytes into buf

| Parameter | |
| :--- | :--- |
| `f` | file to read from |
| `buf` | destination buffer |
| `len` | maximum bytes to read |
| **returns** | bytes read (0 at end of file), or the native refusal |

### write

```mach
pub fun write(f: File, buf: *u8, len: usize) res[usize, std.io.error.Error]
```

write up to len bytes from buf

| Parameter | |
| :--- | :--- |
| `f` | file to write to |
| `buf` | source buffer |
| `len` | bytes to write |
| **returns** | bytes written, or the native refusal |

### seek

```mach
pub fun seek(f: File, offset: i64, whence: i32) res[i64, std.io.error.Error]
```

reposition the file offset

| Parameter | |
| :--- | :--- |
| `f` | file to seek |
| `offset` | byte offset relative to whence |
| `whence` | SEEK_SET, SEEK_CUR, or SEEK_END |
| **returns** | the resulting absolute offset, or the native refusal |

### reader

```mach
pub fun reader(f: File) std.io.reader.Reader
```

adapt a file to an io.Reader (the file must outlive the reader)

| Parameter | |
| :--- | :--- |
| `f` | file to read from |
| **returns** | a Reader drawing from f |

### writer

```mach
pub fun writer(f: File) std.io.writer.Writer
```

adapt a file to an io.Writer (the file must outlive the writer)

| Parameter | |
| :--- | :--- |
| `f` | file to write to |
| **returns** | a Writer feeding f |

### read_secret_of

Only where `capability.HAS_ENTROPY && capability.HAS_PAGES`.

```mach
pub fun read_secret_of(f: File) res[SecretBytes, FsError]
```

read an entire open file straight into secret-welded storage

stats the handle for its size, allocates welded storage once, and has the
kernel read into it through std.memory.secret.read_at, so the bytes never
pass through public memory. reads are positioned from offset zero, so the
handle's position neither matters nor moves, and the handle stays open
for the caller to close. a caller that checks the file before trusting it
checks and reads this one handle. the caller owns the result and releases
it with std.memory.secret.deallocate(data, size). the file must support
positioned reads. a file that shrinks between the stat and the read is
reported as read{eof} with the bytes that were delivered, and the storage
is wiped and released before any error returns.

| Parameter | |
| :--- | :--- |
| `f` | open file to read |
| **returns** | the file contents in welded storage, or why they could not be read |

### identity_of

```mach
pub fun identity_of(f: File) res[Identity, std.io.error.Error]
```

observations do not retain an object or imply unchanged contents

### stat_of

```mach
pub fun stat_of(f: File) res[Metadata, std.io.error.Error]
```

metadata for an open file

## FsError

```mach
pub tag FsError: u8 {
    io:      std.io.error.Error;
    alloc:   std.allocator.Error;
    read:    ReadError;
    write:   WriteError;
    removal: std.filesystem.removal.Error;
    exhausted;
    published: std.io.error.Error;
}
```

why a composite filesystem operation refused

| Case | Payload | |
| :--- | :--- | :--- |
| `io` | `std.io.error.Error` | a native refusal, with its operation and any cleanup failure |
| `alloc` | `std.allocator.Error` | the allocator refused |
| `read` | `ReadError` | the content read failed; eof is a file shorter than its size said |
| `write` | `WriteError` | the content write failed; the payload is the persisted prefix |
| `removal` | `std.filesystem.removal.Error` | a recursive removal refused, by containment or natively |
| `exhausted` |  | every candidate temporary name was taken |
| `published` | `std.io.error.Error` | the replacement is visible, but the directory flush after it failed |

### read_bytes

```mach
pub fun read_bytes(a: *std.allocator.Allocator, p: Path) res[Vector[u8], FsError]
```

read an entire file into an allocated byte buffer

a regular file with a nonzero size is stat'ed and read through io.read_exact
into one buffer of exactly that size, keeping embedded NUL bytes and the
length. a file that shrinks between the stat and the read is reported as
read{eof} with the bytes that were delivered, and nothing stays allocated.
anything else (pipes, special files, files that report no size) composes
io.read_all, which grows as it reads. a refused allocation is read{alloc}
on either path. the caller owns the returned vector; on failure nothing is
owned.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `p` | file path |
| **returns** | the file contents, or why they could not be read |

### read_bytes_native

```mach
pub fun read_bytes_native(a: *std.allocator.Allocator, name: *Unit) res[Vector[u8], FsError]
```

read_bytes for a name in native units

### read_string

```mach
pub fun read_string(a: *std.allocator.Allocator, p: Path) res[str, FsError]
```

read an entire file into an allocated, null-terminated string

stats the file for its size and composes io.read_exact into an exact buffer,
allocating once with no growth. for text; binary content with embedded NUL
bytes loses its length to the first NUL when read through str_len. a file
that shrinks between the stat and the read is reported as read{eof} with the
bytes that were delivered, and nothing stays allocated.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `p` | file path |
| **returns** | the file contents, or why they could not be read |

### read_string_native

```mach
pub fun read_string_native(a: *std.allocator.Allocator, name: *Unit) res[str, FsError]
```

read_string for a name in native units

### write_bytes

```mach
pub fun write_bytes(p: Path, data: *u8, len: usize, mode: i32) err[FsError]
```

write bytes to a file, creating or truncating it

composes io.write_all over the file's Writer. a write failure carries the
persisted prefix; a close failure after a complete write is reported as io,
because the bytes are not known to have reached the file.

| Parameter | |
| :--- | :--- |
| `p` | file path |
| `data` | bytes to write |
| `len` | number of bytes |
| `mode` | permission bits for a newly created file |
| **returns** | ok, or why the bytes are not all in the file |

### write_bytes_native

```mach
pub fun write_bytes_native(name: *Unit, data: *u8, len: usize, mode: i32) err[FsError]
```

write_bytes for a name in native units

### replace_bytes_atomic

```mach
pub fun replace_bytes_atomic(a: *std.allocator.Allocator, p: Path, data: *u8, len: usize, file_mode: i32, dir_mode: i32) err[FsError]
```

replace a file with complete bytes through a durable sibling temporary

missing parent directories are created before the temporary. the temporary is
created beside the destination with O_EXCL, flushed, and closed before rename,
so readers see either the old file or the complete replacement and a
cross-device rename cannot occur. after rename, the parent directory is
flushed through the platform durability contract. if that final flush
fails, the replacement is already visible: the outcome is `published` with
the flush failure, distinct from every refusal before the rename, after
which the destination is untouched and the temporary is removed.

| Parameter | |
| :--- | :--- |
| `a` | allocator for temporary paths |
| `p` | destination path |
| `data` | bytes to write |
| `len` | number of bytes |
| `file_mode` | permission bits for the replacement file |
| `dir_mode` | permission bits for newly created parent directories |
| **returns** | ok, or why the replacement is not complete and durable |

### replace_bytes_atomic_native

```mach
pub fun replace_bytes_atomic_native(a: *std.allocator.Allocator, name: *Unit, data: *u8, len: usize, file_mode: i32, dir_mode: i32) err[FsError]
```

replace_bytes_atomic for a name in native units. the parent walk and the
sibling temporary are in the same units, so the temporary sits beside a
destination whose name has no UTF-8 spelling

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated destination name in native units |

### read_dir

```mach
pub fun read_dir(a: *std.allocator.Allocator, p: Path) res[Vector[Listed], FsError]
```

list the entries of a directory, excluding "." and ".."

every entry is listed in directory order. an entry with no UTF-8 spelling
is listed in sequence as unspellable, with its native name, and the listing
goes on. only a fault of the directory itself fails the listing. the vector
and every name are owned by the caller and released with listed_dnit, or
with the whole arena. a failure releases every partial result and reports
the first refusal, with a cursor or descriptor cleanup failure kept beside it.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the vector and each name |
| `p` | directory path |
| **returns** | the child entries, or why they could not be listed |

### read_dir_native

```mach
pub fun read_dir_native(a: *std.allocator.Allocator, p: *Unit) res[Vector[NativeName], FsError]
```

read_dir for a directory named in native units, every entry named in them

| Parameter | |
| :--- | :--- |
| **returns** | the child names, released with native_names_dnit |

### create_dir_all

```mach
pub fun create_dir_all(a: *std.allocator.Allocator, p: Path, mode: i32) err[FsError]
```

create a directory and every missing parent (mkdir -p)

a directory that already exists is success. when the final creation fails
and the path is still not a directory, the creation's refusal is reported.

| Parameter | |
| :--- | :--- |
| `a` | allocator for transient parent paths |
| `p` | directory path |
| `mode` | permission bits for created directories |
| **returns** | ok, or why the directory does not exist |

### create_dir_all_native

```mach
pub fun create_dir_all_native(a: *std.allocator.Allocator, name: *Unit, mode: i32) err[FsError]
```

create_dir_all for a name in native units, its parents walked in the same units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated directory name in native units |

### remove_all

```mach
pub fun remove_all(a: *std.allocator.Allocator, p: Path) err[FsError]
```

recursively remove a file, directory tree, or symbolic link (rm -rf)

directories are removed depth-first. symbolic links are removed as links and
never followed, so a link pointing outside the tree leaves its target intact.
a missing path succeeds, making the operation idempotent.
windows force deletion preserves alias attributes and reports unsupported
for read-only entries on filesystems without native posix deletion.
roots and dot entries are refused before mutation, as a removal containment
refusal.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the owned input and parent paths |
| `p` | path naming the child entry to remove |
| **returns** | ok, or why the entry may still exist |

### remove_all_native

```mach
pub fun remove_all_native(a: *std.allocator.Allocator, name: *Unit) err[FsError]
```

remove_all for a name in native units. the parent walk and every name below
the entry are handled in native units, so a tree holding names with no UTF-8
spelling is removed whole

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name in native units of the child entry to remove |

## Kind

```mach
pub def Kind: u8
```

what a path resolves to

| Name | Value | |
| :--- | :--- | :--- |
| `KIND_OTHER` | `0` |  |
| `KIND_FILE` | `1` |  |
| `KIND_DIR` | `2` |  |
| `KIND_SYMLINK` | `3` |  |

## Metadata

```mach
pub rec Metadata {
    kind:     Kind;
    size:     usize;
    mode:     u32;
    modified: Time;
    accessed: Time;
    created:  opt[Time];
}
```

portable file metadata

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `Kind` | file, directory, symlink, or other |
| `size` | `usize` | size in bytes |
| `mode` | `u32` | raw permission/type bits (POSIX; synthesized elsewhere) |
| `modified` | `Time` | last modification time |
| `accessed` | `Time` | last access time |
| `created` | `opt[Time]` | birth time when the platform provides it, else none |

### metadata

```mach
pub fun metadata(p: Path) res[Metadata, std.io.error.Error]
```

metadata for a path, following a final symbolic link

| Parameter | |
| :--- | :--- |
| `p` | path to query |
| **returns** | the metadata, or the native refusal |

### metadata_native

```mach
pub fun metadata_native(name: *Unit) res[Metadata, std.io.error.Error]
```

metadata for a name in native units, following a final symbolic link

### metadata_link

```mach
pub fun metadata_link(p: Path) res[Metadata, std.io.error.Error]
```

metadata for a path without following a final symbolic link

| Parameter | |
| :--- | :--- |
| `p` | path to query |
| **returns** | the metadata (a symlink reports itself), or the native refusal |

### metadata_link_native

```mach
pub fun metadata_link_native(name: *Unit) res[Metadata, std.io.error.Error]
```

metadata_link for a name in native units

### meta_is_dir

```mach
pub fun meta_is_dir(m: *Metadata) bool
```

check whether metadata describes a directory

### meta_is_file

```mach
pub fun meta_is_file(m: *Metadata) bool
```

check whether metadata describes a regular file

### meta_is_symlink

```mach
pub fun meta_is_symlink(m: *Metadata) bool
```

check whether metadata describes a symbolic link

## SecretBytes

Only where `capability.HAS_ENTROPY && capability.HAS_PAGES`.

```mach
pub rec SecretBytes {
    data: *^u8;
    size: usize;
}
```

a file's bytes in secret-welded storage

| Field | Type | |
| :--- | :--- | :--- |
| `data` | `*^u8` | allocation from std.memory.secret, nil for an empty file |
| `size` | `usize` | byte count, and the size to release with secret.deallocate |

### read_secret

Only where `capability.HAS_ENTROPY && capability.HAS_PAGES`.

```mach
pub fun read_secret(p: Path) res[SecretBytes, FsError]
```

read an entire file by path straight into secret-welded storage

opens the path, reads it through read_secret_of and closes it. a native
refusal carries any close failure beside it, and a close failure after a
complete read releases the storage and is reported as io.

| Parameter | |
| :--- | :--- |
| `p` | file path |
| **returns** | the file contents in welded storage, or why they could not be read |

### read_secret_native

Only where `capability.HAS_ENTROPY && capability.HAS_PAGES`.

```mach
pub fun read_secret_native(name: *Unit) res[SecretBytes, FsError]
```

read_secret for a name in native units

## Listed

```mach
pub tag Listed: u8 {
    name:        str;
    unspellable: NativeName;
}
```

one read_dir entry: its name in UTF-8, or, for an entry with no UTF-8
spelling, which only a windows directory can hold, its name in native units
(std.runtime.native.view.NativeName) so the native forms can reach it. each
is owned by the caller's allocator

### listed_dnit

```mach
pub fun listed_dnit(entries: *Vector[Listed])
```

release a read_dir result: every name, then the vector

## TempFile

```mach
pub rec TempFile {
    file: File;
    path: Path;
}
```

a created temporary file and its path

| Field | Type | |
| :--- | :--- | :--- |
| `file` | `File` | the open handle |
| `path` | `Path` | the allocated path (freed with the caller's allocator) |

### temp_create

```mach
pub fun temp_create(a: *std.allocator.Allocator, prefix: str) res[TempFile, FsError]
```

create a uniquely named temporary file under the OS temp directory

the file is opened O_CREAT|O_EXCL, so the returned path is exclusively owned.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the path |
| `prefix` | name prefix (e.g. "build" -> "\<tmp>/build_\<hex>") |
| **returns** | the created temporary file, or why none could be created |

### temp_path

```mach
pub fun temp_path(tf: *TempFile) Path
```

the path of a temporary file

### temp_close

```mach
pub fun temp_close(tf: *TempFile) err[std.io.error.Error]
```

close a temporary file without removing it

### temp_remove

```mach
pub fun temp_remove(tf: *TempFile) err[std.io.error.Error]
```

remove a temporary file from disk

### temp_close_and_remove

```mach
pub fun temp_close_and_remove(tf: *TempFile) err[std.io.error.Error]
```

close and remove a temporary file; both effects run, and a close failure is
reported first with the removal's refusal beside it

## NativeTempFile

```mach
pub rec NativeTempFile {
    file: File;
    name: *Unit;
}
```

a created temporary file named in native units

| Field | Type | |
| :--- | :--- | :--- |
| `file` | `File` | the open handle |
| `name` | `*Unit` | the allocated nul-terminated name, freed with the caller's allocator as path.native_len(name) + 1 units |

### temp_create_native

```mach
pub fun temp_create_native(a: *std.allocator.Allocator, prefix: str) res[NativeTempFile, FsError]
```

create a uniquely named temporary file under the OS temp directory, named in
native units from temp_dir_native, so a temp directory whose path has no
UTF-8 spelling still holds it. the file is opened O_CREAT|O_EXCL

| Parameter | |
| :--- | :--- |
| `a` | allocator for the name |
| `prefix` | name prefix (e.g. "build" -> "\<tmp>/build_\<hex>") |
| **returns** | the created temporary file, or why none could be created |

### temp_remove_native

```mach
pub fun temp_remove_native(tf: *NativeTempFile) err[std.io.error.Error]
```

remove a native temporary file from disk

### temp_close_and_remove_native

```mach
pub fun temp_close_and_remove_native(tf: *NativeTempFile) err[std.io.error.Error]
```

close and remove a native temporary file, as temp_close_and_remove does

## Functions

### identity_equal

```mach
pub fun identity_equal(a: Identity, b: Identity) bool
```

### identity_link

```mach
pub fun identity_link(p: Path) res[Identity, std.io.error.Error]
```

the final symlink itself is observed and unsupported domains remain explicit

### identity_link_native

```mach
pub fun identity_link_native(name: *Unit) res[Identity, std.io.error.Error]
```

identity_link for a name in native units

### exists

```mach
pub fun exists(p: Path) res[bool, std.io.error.Error]
```

check whether a path exists (as any entry, including a broken symlink)

| Parameter | |
| :--- | :--- |
| **returns** | true or false when the question could be answered, or the native refusal (permission denied, a symlink loop) when it could not |

### exists_native

```mach
pub fun exists_native(name: *Unit) res[bool, std.io.error.Error]
```

exists for a name in native units

### is_file

```mach
pub fun is_file(p: Path) res[bool, std.io.error.Error]
```

check whether a path is an existing regular file (following symlinks)

### is_file_native

```mach
pub fun is_file_native(name: *Unit) res[bool, std.io.error.Error]
```

is_file for a name in native units

### is_dir

```mach
pub fun is_dir(p: Path) res[bool, std.io.error.Error]
```

check whether a path is an existing directory (following symlinks)

### is_dir_native

```mach
pub fun is_dir_native(name: *Unit) res[bool, std.io.error.Error]
```

is_dir for a name in native units

### is_symlink

```mach
pub fun is_symlink(p: Path) res[bool, std.io.error.Error]
```

check whether a path is a symbolic link (not following it)

### is_symlink_native

```mach
pub fun is_symlink_native(name: *Unit) res[bool, std.io.error.Error]
```

is_symlink for a name in native units

### create_dir

```mach
pub fun create_dir(p: Path, mode: i32) err[std.io.error.Error]
```

create a single directory

| Parameter | |
| :--- | :--- |
| `p` | directory path |
| `mode` | permission bits |
| **returns** | ok, or the native refusal |

### create_dir_native

```mach
pub fun create_dir_native(name: *Unit, mode: i32) err[std.io.error.Error]
```

create a single directory by a name in native units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name in native units |
| `mode` | permission bits |
| **returns** | ok, or the native refusal |

### remove_file

```mach
pub fun remove_file(p: Path) err[std.io.error.Error]
```

remove a single file or symbolic link

| Parameter | |
| :--- | :--- |
| `p` | path to remove |
| **returns** | ok, or the native refusal |

### remove_file_native

```mach
pub fun remove_file_native(name: *Unit) err[std.io.error.Error]
```

remove a single file or symbolic link by a name in native units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name in native units |
| **returns** | ok, or the native refusal |

### remove_dir

```mach
pub fun remove_dir(p: Path) err[std.io.error.Error]
```

remove an empty directory

| Parameter | |
| :--- | :--- |
| `p` | directory path to remove |
| **returns** | ok, or the native refusal |

### remove_dir_native

```mach
pub fun remove_dir_native(name: *Unit) err[std.io.error.Error]
```

remove an empty directory by a name in native units

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated name in native units |
| **returns** | ok, or the native refusal |

### rename

```mach
pub fun rename(from: Path, to: Path) err[std.io.error.Error]
```

rename or move a file or directory

An existing destination file is replaced, as POSIX rename does. Replacing an
existing *directory* is not portable: POSIX allows it when the destination is
an empty directory and windows refuses it outright, so callers should not rely
on it.
windows retains open destination handles on supporting local filesystems,
while smb refuses replacement until destination handles close.

| Parameter | |
| :--- | :--- |
| `from` | source path |
| `to` | destination path |
| **returns** | ok, or the native refusal |

### rename_native

```mach
pub fun rename_native(from: *Unit, to: *Unit) err[std.io.error.Error]
```

rename or move by names in native units, as rename does

| Parameter | |
| :--- | :--- |
| `from` | nul-terminated source name in native units |
| `to` | nul-terminated destination name in native units |
| **returns** | ok, or the native refusal |

### symlink

```mach
pub fun symlink(target: Path, linkpath: Path) err[std.io.error.Error]
```

create a symbolic link at linkpath pointing to target

| Parameter | |
| :--- | :--- |
| `target` | path the link points to (stored verbatim) |
| `linkpath` | path of the link to create |
| **returns** | ok, or the native refusal |

### symlink_native

```mach
pub fun symlink_native(target: *Unit, linkpath: *Unit) err[std.io.error.Error]
```

create a symbolic link by names in native units, as symlink does

| Parameter | |
| :--- | :--- |
| `target` | nul-terminated target in native units (stored verbatim) |
| `linkpath` | nul-terminated name of the link in native units |
| **returns** | ok, or the native refusal |

### native_names_dnit

```mach
pub fun native_names_dnit(names: *Vector[NativeName])
```

release a read_dir_native result: every name, then the vector

## Forwards

### Identity

Forwards [`std.system.file_identity.Identity`](system/file_identity.md#identity).

```mach
pub rec Identity {
    representation: [41]u8;
}
```

opaque to filesystem callers, native producers initialize every byte

### SEEK_SET

Forwards [`std.system.os.SEEK_SET`](system/os.md#seek_set), only where `capability.HAS_FILES`.

```mach
pub val SEEK_SET: i32 = 0
```

seek anchors for `seek`

### SEEK_CUR

Forwards [`std.system.os.SEEK_CUR`](system/os.md#seek_cur), only where `capability.HAS_FILES`.

```mach
pub val SEEK_CUR: i32 = 1
```

### SEEK_END

Forwards [`std.system.os.SEEK_END`](system/os.md#seek_end), only where `capability.HAS_FILES`.

```mach
pub val SEEK_END: i32 = 2
```

