[std](../README.md) / [io](README.md) / **file**

# std.io.file

bounded asynchronous and handle-relative file operations

Source: [`src/io/file.mach`](../../../src/io/file.mach)

Uses types from [`std.filesystem`](../filesystem.md), [`std.io.error`](error.md), [`std.sync.mutex`](../sync/mutex.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Access`](#access) | `def` |  |
| [`OpenOptions`](#openoptions) | `rec` |  |
| [`Root`](#root) | `rec` |  |
| [`Capabilities`](#capabilities) | `rec` |  |
| [`Mapping`](#mapping) | `rec` |  |
| [`TransferReport`](#transferreport) | `rec` |  |
| [`WatchCapabilities`](#watchcapabilities) | `rec` |  |
| [`WatchEvent`](#watchevent) | `def` |  |
| [`Watch`](#watch) | `rec` | path: the UTF-8 path watch_init borrowed, nil for watch_init_native name: the watched name in native units, which every scan opens |

| On `Access` | |
| :--- | :--- |
| [`READ_ONLY`](#access), [`WRITE_ONLY`](#access), [`READ_WRITE`](#access) | |

| On `OpenOptions` | |
| :--- | :--- |
| [`read_options`](#read_options), [`write_options`](#write_options) | |

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
| [`capabilities`](#capabilities-1) | |

| On `Mapping` | |
| :--- | :--- |
| [`map`](#map) | mappings own their virtual region independently of the file handle |
| [`mapping_sync`](#mapping_sync), [`mapping_close`](#mapping_close) | |

| On `TransferReport` | |
| :--- | :--- |
| [`transfer`](#transfer) | the portable transfer uses fixed stack storage and preserves both file offsets |

| On `WatchCapabilities` | |
| :--- | :--- |
| [`watch_capabilities`](#watch_capabilities) | |

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
| [`read_at`](#read_at), [`write_at`](#write_at) | |

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

### read_options

```mach
pub fun read_options() OpenOptions
```

### write_options

```mach
pub fun write_options(mode: i32) OpenOptions
```

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

### capabilities

```mach
pub fun capabilities() Capabilities
```

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

### map

```mach
pub fun map(file: std.filesystem.File, offset: u64, length: usize, writable: bool) res[Mapping, std.io.error.Error]
```

mappings own their virtual region independently of the file handle

### mapping_sync

```mach
pub fun mapping_sync(mapping: *Mapping) err[std.io.error.Error]
```

### mapping_close

```mach
pub fun mapping_close(mapping: *Mapping) err[std.io.error.Error]
```

## TransferReport

```mach
pub rec TransferReport {
    bytes:       usize;
    end_of_file: bool;
    accelerated: bool;
}
```

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

### watch_capabilities

```mach
pub fun watch_capabilities() WatchCapabilities
```

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

### write_at

```mach
pub fun write_at(file: std.filesystem.File, buffer: *u8, length: usize, offset: u64) res[usize, std.io.error.Error]
```

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

