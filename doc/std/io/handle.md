[std](../README.md) / [io](README.md) / **handle**

# std.io.handle

opaque native-width resource handles

Source: [`src/io/handle.mach`](../../../src/io/handle.mach)

| Type | | |
| :--- | :--- | :--- |
| [`FileHandle`](#filehandle) | `rec` | file handle owned by the filesystem layer |
| [`SocketHandle`](#sockethandle) | `rec` | socket handle owned by the networking layer |

| On `FileHandle` | |
| :--- | :--- |
| [`invalid_file`](#invalid_file), [`file_is_valid`](#file_is_valid) | |

| On `SocketHandle` | |
| :--- | :--- |
| [`invalid_socket`](#invalid_socket) | |
| [`socket`](#socket) | a handle for a native socket this process has just opened or accepted |
| [`socket_is_valid`](#socket_is_valid) | |

| Constants | |
| :--- | :--- |
| [`INVALID_VALUE`](#constants) | |

---

## FileHandle

```mach
pub rec FileHandle {
    value: usize;
}
```

file handle owned by the filesystem layer

### invalid_file

```mach
pub fun invalid_file() FileHandle
```

### file_is_valid

```mach
pub fun file_is_valid(handle: FileHandle) bool
```

## SocketHandle

```mach
pub rec SocketHandle {
    value:   usize;
    opening: u64;
}
```

socket handle owned by the networking layer

opening tells one socket from another that later reuses its native value.
the networking layer stamps it once, when it opens or accepts the socket,
and every copy of the handle carries the same stamp. an async driver keys
its state by value and opening together, so a socket closed outside its
driver is detected on the next submission rather than mistaken for the
socket that took over its value

### invalid_socket

```mach
pub fun invalid_socket() SocketHandle
```

### socket

```mach
pub fun socket(value: usize) SocketHandle
```

a handle for a native socket this process has just opened or accepted

each call stamps a new opening, so wrap a native socket exactly once and pass
the handle around. two handles made from one live socket look like two
sockets, and an async driver treats the older one as closed

| Parameter | |
| :--- | :--- |
| `value` | the native socket |
| **returns** | the handle, with an opening no other handle in this process shares |

### socket_is_valid

```mach
pub fun socket_is_valid(handle: SocketHandle) bool
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `INVALID_VALUE` | `usize` | `(-1)::isize::usize` |  |

