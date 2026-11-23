[std](../README.md) / [io](README.md) / **file**

# std.io.file

bounded asynchronous and handle-relative file operations

Source: [`src/io/file.mach`](../../../src/io/file.mach)

Uses types from [`std.filesystem`](../filesystem.md), [`std.io.error`](error.md), [`std.sync.mutex`](../sync/mutex.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Access`](#access) | `def` |  |
| [`OpenOptions`](#openoptions) | `rec` | how open_confined opens a file |
| [`Root`](#root) | `rec` | a directory every confined operation resolves beneath |
| [`Capabilities`](#capabilities) | `rec` | what the file layer provides on this target |
| [`Mapping`](#mapping) | `rec` | a file region mapped into memory |
| [`TransferReport`](#transferreport) | `rec` | what transfer copied |
| [`WatchCapabilities`](#watchcapabilities) | `rec` | what watching provides on this target |
| [`WatchEvent`](#watchevent) | `def` |  |
| [`Watch`](#watch) | `rec` | path: the UTF-8 path watch_init borrowed, nil for watch_init_native name: the watched name in native units, which every scan opens |

| On `Access` | |
| :--- | :--- |
| [`READ_ONLY`](#access), [`WRITE_ONLY`](#access), [`READ_WRITE`](#access) | |

| On `OpenOptions` | |
| :--- | :--- |
| [`read_options`](#read_options) | options that open an existing file read-only |
| [`write_options`](#write_options) | options that open a file write-only, creating it when missing |

| On `Root` | |
| :--- | :--- |
| [`root_open`](#root_open) | the root path is trusted once and every later resolution starts from its handle the root is initialized in place: watches borrow its address and admitted work waits on its condition, so it never moves after this call succeeds |
| [`root_open_native`](#root_open_native) | root_open for a directory named in native units |
| [`root_close`](#root_close) | close rejects new resolution and waits for admitted handle-relative work |
| [`open_confined`](#open_confined) | relative components are opened one at a time from pinned directory handles |
| [`open_confined_native`](#open_confined_native) | open_confined for a relative name in native units, split into components in those units |
| [`replace_confined`](#replace_confined) | success confirms os data and namespace flush requests, not media persistence |
| [`replace_confined_native`](#replace_confined_native) | replace_confined for relative names in native units |

| On `Capabilities` | |
| :--- | :--- |
| [`capabilities`](#capabilities-1) | the file layer's capabilities on this target |

| On `Mapping` | |
| :--- | :--- |
| [`map`](#map) | mappings own their virtual region independently of the file handle |
| [`mapping_sync`](#mapping_sync) | flushes a writable mapping's changes to the file |
| [`mapping_close`](#mapping_close) | unmaps a mapping and clears it |

| On `TransferReport` | |
| :--- | :--- |
| [`transfer`](#transfer) | the portable transfer uses fixed stack storage and preserves both file offsets |

| On `WatchCapabilities` | |
| :--- | :--- |
| [`watch_capabilities`](#watch_capabilities) | watching's capabilities on this target |

| On `WatchEvent` | |
| :--- | :--- |
| [`WATCH_UNCHANGED`](#watchevent), [`WATCH_CREATED`](#watchevent), [`WATCH_REMOVED`](#watchevent), [`WATCH_REPLACED`](#watchevent), [`WATCH_MODIFIED`](#watchevent), [`WATCH_METADATA`](#watchevent) | |

| On `Watch` | |
| :--- | :--- |
| [`watch_init`](#watch_init) | the root and path remain borrowed until watch_dnit |
| [`watch_init_native`](#watch_init_native) | watch_init for a relative name in native units; the root and name remain borrowed until watch_dnit |
| [`watch_scan`](#watch_scan) | scans observe identity without pinning it between calls or detecting every intervening write |
| [`watch_dnit`](#watch_dnit) | releases the borrowed root and path and the converted name; a watch that was never opened is INVALID |

| Functions | |
| :--- | :--- |
| [`read_at`](#read_at) | reads at an offset without using the file position |
| [`write_at`](#write_at) | writes at an offset without using the file position |

| Forwards | |
| :--- | :--- |
| [`Request`](#request) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`Adapter`](#adapter) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`init`](#init) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`submit_read`](#submit_read) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`submit_write`](#submit_write) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`attach_secret_scratch`](#attach_secret_scratch) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`submit_secret_read`](#submit_secret_read) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`submit_secret_write`](#submit_secret_write) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`shutdown_drain`](#shutdown_drain) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`shutdown_abort`](#shutdown_abort) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`active`](#active) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |
| [`dnit`](#dnit) | the background request adapter runs on threads, and a thread is what a root's close waits for, so a threadless target has neither |

---

## Access

```mach
pub def Access: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `READ_ONLY` | `0` |  |
| `WRITE_ONLY` | `1` |  |
| `READ_WRITE` | `2` |  |

## OpenOptions

```mach
pub rec OpenOptions {
    access:    Access;
    create:    bool;
    exclusive: bool;
    truncate:  bool;
    directory: bool;
    mode:      i32;
}
```

how open_confined opens a file

| Field | Type | |
| :--- | :--- | :--- |
| `access` | `Access` | the access the opened file grants |
| `create` | `bool` | create the file when it is missing |
| `exclusive` | `bool` | refuse a file that already exists, valid only with create |
| `truncate` | `bool` | empty an existing file |
| `directory` | `bool` | open a directory, valid only read-only without create or truncate |
| `mode` | `i32` | permission bits for a created file |

### read_options

```mach
pub fun read_options() OpenOptions
```

options that open an existing file read-only

| Parameter | |
| :--- | :--- |
| **returns** | READ_ONLY access with every flag off |

### write_options

```mach
pub fun write_options(mode: i32) OpenOptions
```

options that open a file write-only, creating it when missing

| Parameter | |
| :--- | :--- |
| `mode` | permission bits for a created file |
| **returns** | WRITE_ONLY access with create set, not exclusive and not truncating |

## Root

```mach
pub rec Root {
    directory:   std.filesystem.File;
    active:      usize;
    initialized: bool;
    closing:     bool;
    lock:        std.sync.mutex.Mutex;
    idle:        Idle;
}
```

a directory every confined operation resolves beneath

opened in place by root_open and closed by root_close. it never moves while open

| Field | Type | |
| :--- | :--- | :--- |
| `directory` | `std.filesystem.File` | the pinned directory handle |
| `active` | `usize` | operations admitted and not yet finished |
| `initialized` | `bool` | true between a successful open and close |
| `closing` | `bool` | true while root_close waits for admitted work |
| `lock` | `std.sync.mutex.Mutex` | guards active, initialized and closing |
| `idle` | `Idle` | signalled when active drops to zero |

### root_open

```mach
pub fun root_open(root: *Root, path: Path) err[std.io.error.Error]
```

the root path is trusted once and every later resolution starts from its handle
the root is initialized in place: watches borrow its address and admitted work
waits on its condition, so it never moves after this call succeeds

### root_open_native

```mach
pub fun root_open_native(root: *Root, name: *Unit) err[std.io.error.Error]
```

root_open for a directory named in native units

### root_close

```mach
pub fun root_close(root: *Root) err[std.io.error.Error]
```

close rejects new resolution and waits for admitted handle-relative work

| Parameter | |
| :--- | :--- |
| `root` | the root to close |
| **returns** | the directory close failure, or CLOSED when root is nil, not open or already closing |

### open_confined

```mach
pub fun open_confined(root: *Root, path: Path, options: OpenOptions) res[std.filesystem.File, std.io.error.Error]
```

relative components are opened one at a time from pinned directory handles

### open_confined_native

```mach
pub fun open_confined_native(root: *Root, name: *Unit, options: OpenOptions) res[std.filesystem.File, std.io.error.Error]
```

open_confined for a relative name in native units, split into components
in those units

### replace_confined

```mach
pub fun replace_confined(root: *Root, temporary: Path, destination: Path) err[std.io.error.Error]
```

success confirms os data and namespace flush requests, not media persistence

both names are converted once before anything is flushed, so a name that
cannot be converted leaves the temporary untouched

### replace_confined_native

```mach
pub fun replace_confined_native(root: *Root, temporary: *Unit, destination: *Unit) err[std.io.error.Error]
```

replace_confined for relative names in native units

## Capabilities

```mach
pub rec Capabilities {
    positioned_io:                      bool;
    native_async:                       bool;
    bounded_workers:                    bool;
    confined_open:                      bool;
    replacement_flush_request:          bool;
    replacement_persistence_guaranteed: bool;
    mapping:                            bool;
    watching:                           bool;
    accelerated_transfer:               bool;
}
```

what the file layer provides on this target

| Field | Type | |
| :--- | :--- | :--- |
| `positioned_io` | `bool` | reads and writes at an offset are available |
| `native_async` | `bool` | the host completes file requests asynchronously |
| `bounded_workers` | `bool` | async requests run on a bounded worker adapter |
| `confined_open` | `bool` | opens resolve beneath a root without escaping it |
| `replacement_flush_request` | `bool` | replace_confined requests a flush before renaming |
| `replacement_persistence_guaranteed` | `bool` | a replacement is guaranteed to reach the media |
| `mapping` | `bool` | files can be mapped into memory |
| `watching` | `bool` | a path can be watched for changes |
| `accelerated_transfer` | `bool` | transfer uses a native copy path |

### capabilities

```mach
pub fun capabilities() Capabilities
```

the file layer's capabilities on this target

| Parameter | |
| :--- | :--- |
| **returns** | the capabilities, the same on every target that builds this module |

## Mapping

```mach
pub rec Mapping {
    data:        ptr;
    length:      usize;
    offset:      u64;
    writable:    bool;
    initialized: bool;
}
```

a file region mapped into memory

| Field | Type | |
| :--- | :--- | :--- |
| `data` | `ptr` | the first mapped byte |
| `length` | `usize` | the mapped length in bytes |
| `offset` | `u64` | the file offset the mapping starts at |
| `writable` | `bool` | true when writes reach the file |
| `initialized` | `bool` | true until mapping_close |

### map

```mach
pub fun map(file: std.filesystem.File, offset: u64, length: usize, writable: bool) res[Mapping, std.io.error.Error]
```

mappings own their virtual region independently of the file handle

### mapping_sync

```mach
pub fun mapping_sync(mapping: *Mapping) err[std.io.error.Error]
```

flushes a writable mapping's changes to the file

| Parameter | |
| :--- | :--- |
| `mapping` | the mapping to flush |
| **returns** | the failure, INVALID for a nil, closed or read-only mapping |

### mapping_close

```mach
pub fun mapping_close(mapping: *Mapping) err[std.io.error.Error]
```

unmaps a mapping and clears it

| Parameter | |
| :--- | :--- |
| `mapping` | the mapping to release |
| **returns** | the failure, INVALID for a nil or closed mapping |

## TransferReport

```mach
pub rec TransferReport {
    bytes:       usize;
    end_of_file: bool;
    accelerated: bool;
}
```

what transfer copied

| Field | Type | |
| :--- | :--- | :--- |
| `bytes` | `usize` | bytes copied |
| `end_of_file` | `bool` | true when the source ended before length bytes were copied |
| `accelerated` | `bool` | true when a native copy path was used |

### transfer

```mach
pub fun transfer(source: std.filesystem.File, destination: std.filesystem.File, source_offset: u64, destination_offset: u64, length: usize) res[TransferReport, std.io.error.Error]
```

the portable transfer uses fixed stack storage and preserves both file offsets

## WatchCapabilities

```mach
pub rec WatchCapabilities {
    supported:     bool;
    recursive:     bool;
    native:        bool;
    requires_scan: bool;
}
```

what watching provides on this target

| Field | Type | |
| :--- | :--- | :--- |
| `supported` | `bool` | a path can be watched |
| `recursive` | `bool` | a watch covers a directory's descendants |
| `native` | `bool` | the host reports changes itself |
| `requires_scan` | `bool` | changes are found only by calling watch_scan |

### watch_capabilities

```mach
pub fun watch_capabilities() WatchCapabilities
```

watching's capabilities on this target

| Parameter | |
| :--- | :--- |
| **returns** | supported and scan-driven, neither recursive nor native |

## WatchEvent

```mach
pub def WatchEvent: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `WATCH_UNCHANGED` | `0` |  |
| `WATCH_CREATED` | `1` |  |
| `WATCH_REMOVED` | `2` |  |
| `WATCH_REPLACED` | `3` |  |
| `WATCH_MODIFIED` | `4` |  |
| `WATCH_METADATA` | `5` |  |

## Watch

```mach
pub rec Watch {
    root:        *Root;
    path:        Path;
    name:        std.system.os.NativePath;
    metadata:    std.filesystem.Metadata;
    identity:    std.filesystem.Identity;
    exists:      bool;
    initialized: bool;
}
```

path: the UTF-8 path watch_init borrowed, nil for watch_init_native
name: the watched name in native units, which every scan opens

### watch_init

```mach
pub fun watch_init(watch: *Watch, root: *Root, path: Path) res[bool, std.io.error.Error]
```

the root and path remain borrowed until watch_dnit. the path is converted
once here, and every scan opens the converted name

### watch_init_native

```mach
pub fun watch_init_native(watch: *Watch, root: *Root, name: *Unit) res[bool, std.io.error.Error]
```

watch_init for a relative name in native units; the root and name remain
borrowed until watch_dnit

### watch_scan

```mach
pub fun watch_scan(watch: *Watch) res[WatchEvent, std.io.error.Error]
```

scans observe identity without pinning it between calls or detecting every intervening write

### watch_dnit

```mach
pub fun watch_dnit(watch: *Watch) err[std.io.error.Error]
```

releases the borrowed root and path and the converted name; a watch that
was never opened is INVALID

## Functions

### read_at

```mach
pub fun read_at(file: std.filesystem.File, buffer: *u8, length: usize, offset: u64) res[usize, std.io.error.Error]
```

reads at an offset without using the file position

| Parameter | |
| :--- | :--- |
| `file` | the file to read |
| `buffer` | receives the bytes, may be nil only when length is 0 |
| `length` | the most bytes to read |
| `offset` | the file offset to read from |
| **returns** | bytes read, 0 at end of file, or the failure. an invalid handle, nil buffer or offset past the largest file offset is INVALID |

### write_at

```mach
pub fun write_at(file: std.filesystem.File, buffer: *u8, length: usize, offset: u64) res[usize, std.io.error.Error]
```

writes at an offset without using the file position

| Parameter | |
| :--- | :--- |
| `file` | the file to write |
| `buffer` | the bytes to write, may be nil only when length is 0 |
| `length` | the number of bytes to write |
| `offset` | the file offset to write at |
| **returns** | bytes written, which may be short, or the failure. an invalid handle, nil buffer or offset past the largest file offset is INVALID |

## Forwards

### Request

Forwards [`std.io.file.adapter.Request`](file/adapter.md#request), only where `capability.HAS_THREADS`.

```mach
pub rec Request {
    adapter:        *Adapter;
    state:          i64;
    kind:           std.io.runtime.Kind;
    file:           std.filesystem.File;
    length:         usize;
    offset:         u64;
    scratch:        *u8;
    token:          std.io.runtime.Token;
    secret:         bool;
    scratch_offset: usize;
    arrivals:       usize;
    borrow:         std.memory.secret.Borrow;
}
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### Adapter

Forwards [`std.io.file.adapter.Adapter`](file/adapter.md#adapter), only where `capability.HAS_THREADS`.

```mach
pub rec Adapter {
    runtime:          *std.io.runtime.Runtime;
    source:           std.io.runtime.SourceToken;
    requests:         *Request;
    request_capacity: usize;
    scratch:          *u8;
    scratch_length:   usize;
    max_transfer:     usize;
    secret_scratch:   std.memory.secret.Borrow;
    secret_attached:  bool;
    tasks:            *std.sync.worker_pool.Task;
    abort_tasks:      *std.sync.worker_pool.Task;
    threads:          *std.sync.thread.Thread;
    workers:          *std.sync.worker_pool.Worker;
    worker_count:     usize;
    pool:             std.sync.worker_pool.Pool;
    next_request:     usize;
    active:           usize;
    state:            u8;
    initialized:      bool;
    lock:             std.sync.mutex.Mutex;
}
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### init

Forwards [`std.io.file.adapter.init`](file/adapter.md#init), only where `capability.HAS_THREADS`.

```mach
pub fun init(
    adapter: *Adapter,
    runtime: *std.io.runtime.Runtime,
    requests: *Request,
    request_capacity: usize,
    scratch: *u8,
    scratch_length: usize,
    max_transfer: usize,
    tasks: *std.sync.worker_pool.Task,
    abort_tasks: *std.sync.worker_pool.Task,
    threads: *std.sync.thread.Thread,
    workers: *std.sync.worker_pool.Worker,
    worker_count: usize,
) err[std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### submit_read

Forwards [`std.io.file.adapter.submit_read`](file/adapter.md#submit_read), only where `capability.HAS_THREADS`.

```mach
pub fun submit_read(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### submit_write

Forwards [`std.io.file.adapter.submit_write`](file/adapter.md#submit_write), only where `capability.HAS_THREADS`.

```mach
pub fun submit_write(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### attach_secret_scratch

Forwards [`std.io.file.adapter.attach_secret_scratch`](file/adapter.md#attach_secret_scratch), only where `capability.HAS_THREADS`.

```mach
pub fun attach_secret_scratch(adapter: *Adapter, scratch: *^u8, scratch_length: usize) err[std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### submit_secret_read

Forwards [`std.io.file.adapter.submit_secret_read`](file/adapter.md#submit_secret_read), only where `capability.HAS_THREADS`.

```mach
pub fun submit_secret_read(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *^u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### submit_secret_write

Forwards [`std.io.file.adapter.submit_secret_write`](file/adapter.md#submit_secret_write), only where `capability.HAS_THREADS`.

```mach
pub fun submit_secret_write(adapter: *Adapter, scope: *std.sync.cancel.Scope, file: *std.filesystem.File, buffer: *^u8, length: usize, offset: u64, context: usize) res[std.io.runtime.Token, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### shutdown_drain

Forwards [`std.io.file.adapter.shutdown_drain`](file/adapter.md#shutdown_drain), only where `capability.HAS_THREADS`.

```mach
pub fun shutdown_drain(adapter: *Adapter) res[bool, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### shutdown_abort

Forwards [`std.io.file.adapter.shutdown_abort`](file/adapter.md#shutdown_abort), only where `capability.HAS_THREADS`.

```mach
pub fun shutdown_abort(adapter: *Adapter) res[usize, std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### active

Forwards [`std.io.file.adapter.active`](file/adapter.md#active), only where `capability.HAS_THREADS`.

```mach
pub fun active(adapter: *Adapter) usize
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

### dnit

Forwards [`std.io.file.adapter.dnit`](file/adapter.md#dnit), only where `capability.HAS_THREADS`.

```mach
pub fun dnit(adapter: *Adapter) err[std.io.error.Error]
```

the background request adapter runs on threads, and a thread is what a root's
close waits for, so a threadless target has neither

