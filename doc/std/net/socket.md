[std](../README.md) / [net](README.md) / **socket**

# std.net.socket

portable socket creation, options, and endpoint queries

Source: [`src/net/socket.mach`](../../../src/net/socket.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.io.handle`](../io/handle.md), [`std.net.ip`](ip.md).

| Type | | |
| :--- | :--- | :--- |
| [`Flags`](#flags) | `rec` | creation state is established before a handle reaches application code |
| [`BoolOption`](#booloption) | `def` |  |
| [`ValueOption`](#valueoption) | `def` |  |
| [`Linger`](#linger) | `rec` | the SO_LINGER setting of a socket |
| [`BindOptions`](#bindoptions) | `rec` | socket options applied between creation and bind |

| On `Flags` | |
| :--- | :--- |
| [`blocking_flags`](#blocking_flags) | the flags for a blocking socket that child processes do not inherit |
| [`async_flags`](#async_flags) | the flags for a nonblocking socket that child processes do not inherit |
| [`create`](#create) | create a socket |
| [`accept`](#accept) | accept a pending connection on a listening socket |

| On `BoolOption` | |
| :--- | :--- |
| [`REUSE_ADDRESS`](#booloption), [`REUSE_PORT`](#booloption), [`EXCLUSIVE_ADDRESS`](#booloption), [`NO_DELAY`](#booloption), [`KEEP_ALIVE`](#booloption), [`IPV6_ONLY`](#booloption), [`FAST_OPEN`](#booloption) | |
| [`bool_option_supported`](#bool_option_supported) | whether the target supports a boolean option |
| [`set_bool`](#set_bool) | turn a boolean option on or off |
| [`get_bool`](#get_bool) | read a boolean option |

| On `ValueOption` | |
| :--- | :--- |
| [`KEEP_IDLE_SECONDS`](#valueoption), [`KEEP_INTERVAL_SECONDS`](#valueoption), [`KEEP_PROBE_COUNT`](#valueoption), [`SEND_BUFFER_BYTES`](#valueoption), [`RECEIVE_BUFFER_BYTES`](#valueoption), [`TRAFFIC_CLASS_IPV4`](#valueoption), [`TRAFFIC_CLASS_IPV6`](#valueoption) | |
| [`value_option_supported`](#value_option_supported) | whether the target supports a value option |
| [`set_value`](#set_value) | setters copy values immediately and retain no caller storage units are seconds, probe count, requested bytes, or an 8-bit traffic class |
| [`get_value`](#get_value) | read a value option |

| On `Linger` | |
| :--- | :--- |
| [`set_linger`](#set_linger) | set a socket's SO_LINGER |
| [`get_linger`](#get_linger) | read a socket's SO_LINGER |

| On `BindOptions` | |
| :--- | :--- |
| [`bind_options`](#bind_options) | the options the plain bind and listen functions use |
| [`check_bind_options`](#check_bind_options) | refuses options the target cannot apply, before any socket exists |
| [`apply_bind_options`](#apply_bind_options) | applies bind options to a freshly created socket |

| Functions | |
| :--- | :--- |
| [`local_endpoint`](#local_endpoint) | the local endpoint a socket is bound to |
| [`remote_endpoint`](#remote_endpoint) | the remote endpoint a socket is connected to |
| [`inheritable`](#inheritable) | whether child processes inherit a socket |

---

## Flags

```mach
pub rec Flags {
    nonblocking:     bool;
    non_inheritable: bool;
}
```

creation state is established before a handle reaches application code

| Field | Type | |
| :--- | :--- | :--- |
| `nonblocking` | `bool` | the socket is created in nonblocking mode |
| `non_inheritable` | `bool` | child processes do not inherit the socket |

### blocking_flags

```mach
pub fun blocking_flags() Flags
```

the flags for a blocking socket that child processes do not inherit

### async_flags

```mach
pub fun async_flags() Flags
```

the flags for a nonblocking socket that child processes do not inherit

### create

```mach
pub fun create(family: i32, typ: i32, protocol: i32, flags: Flags) res[std.io.handle.SocketHandle, std.io.error.Error]
```

create a socket

| Parameter | |
| :--- | :--- |
| `family` | the address family, such as AF_INET or AF_INET6 |
| `typ` | the socket type, such as SOCK_STREAM or SOCK_DGRAM |
| `protocol` | the protocol, 0 for the type's default |
| `flags` | the creation state the handle starts with |
| **returns** | the handle, which the caller owns and closes, or the failure |

### accept

```mach
pub fun accept(handle: std.io.handle.SocketHandle, flags: Flags, peer: *std.net.ip.Endpoint) res[std.io.handle.SocketHandle, std.io.error.Error]
```

accept a pending connection on a listening socket

| Parameter | |
| :--- | :--- |
| `handle` | the listening socket |
| `flags` | the creation state the accepted handle starts with |
| `peer` | filled with the peer's endpoint, or nil |
| **returns** | the accepted handle, which the caller owns and closes, or the failure. UNSUPPORTED when the peer address cannot be read as an IP endpoint, and the accepted socket is then closed |

## BoolOption

```mach
pub def BoolOption: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `REUSE_ADDRESS` | `0` |  |
| `REUSE_PORT` | `1` |  |
| `EXCLUSIVE_ADDRESS` | `2` |  |
| `NO_DELAY` | `3` |  |
| `KEEP_ALIVE` | `4` |  |
| `IPV6_ONLY` | `5` |  |
| `FAST_OPEN` | `6` |  |

### bool_option_supported

```mach
pub fun bool_option_supported(option: BoolOption) bool
```

whether the target supports a boolean option

| Parameter | |
| :--- | :--- |
| `option` | the option |
| **returns** | true when set_bool and get_bool can reach it |

### set_bool

```mach
pub fun set_bool(handle: std.io.handle.SocketHandle, option: BoolOption, enabled: bool) err[std.io.error.Error]
```

turn a boolean option on or off

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| `option` | the option |
| `enabled` | whether to turn it on |
| **returns** | ok, or the failure. UNSUPPORTED where the target lacks the option |

### get_bool

```mach
pub fun get_bool(handle: std.io.handle.SocketHandle, option: BoolOption) res[bool, std.io.error.Error]
```

read a boolean option

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| `option` | the option |
| **returns** | whether it is on, or the failure. UNSUPPORTED where the target lacks the option |

## ValueOption

```mach
pub def ValueOption: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `KEEP_IDLE_SECONDS` | `0` |  |
| `KEEP_INTERVAL_SECONDS` | `1` |  |
| `KEEP_PROBE_COUNT` | `2` |  |
| `SEND_BUFFER_BYTES` | `3` |  |
| `RECEIVE_BUFFER_BYTES` | `4` |  |
| `TRAFFIC_CLASS_IPV4` | `5` |  |
| `TRAFFIC_CLASS_IPV6` | `6` |  |

### value_option_supported

```mach
pub fun value_option_supported(option: ValueOption) bool
```

whether the target supports a value option

| Parameter | |
| :--- | :--- |
| `option` | the option |
| **returns** | true when set_value and get_value can reach it |

### set_value

```mach
pub fun set_value(handle: std.io.handle.SocketHandle, option: ValueOption, value: u32) err[std.io.error.Error]
```

setters copy values immediately and retain no caller storage
units are seconds, probe count, requested bytes, or an 8-bit traffic class

### get_value

```mach
pub fun get_value(handle: std.io.handle.SocketHandle, option: ValueOption) res[u32, std.io.error.Error]
```

read a value option

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| `option` | the option |
| **returns** | the value, or the failure. UNSUPPORTED where the target lacks the option, INVALID when the native value is negative |

## Linger

```mach
pub rec Linger {
    enabled: bool;
    seconds: u32;
}
```

the SO_LINGER setting of a socket

| Field | Type | |
| :--- | :--- | :--- |
| `enabled` | `bool` | close waits for unsent data, up to seconds |
| `seconds` | `u32` | how long close waits |

### set_linger

```mach
pub fun set_linger(handle: std.io.handle.SocketHandle, value: Linger) err[std.io.error.Error]
```

set a socket's SO_LINGER

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| `value` | the linger setting |
| **returns** | ok, or the failure. INVALID when seconds exceeds what the target stores, 65535 on windows and 0x7fffffff elsewhere |

### get_linger

```mach
pub fun get_linger(handle: std.io.handle.SocketHandle) res[Linger, std.io.error.Error]
```

read a socket's SO_LINGER

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| **returns** | the linger setting, or the failure |

## BindOptions

```mach
pub rec BindOptions {
    reuse_address: bool;
    reuse_port:    bool;
}
```

socket options applied between creation and bind

| Field | Type | |
| :--- | :--- | :--- |
| `reuse_address` | `bool` | rebind an address whose closed connections still linger, set by default as the plain bind functions do. SO_REUSEADDR does this on posix. windows does it without an option, and its SO_REUSEADDR would let the socket take an address another socket is using, so nothing is set there |
| `reuse_port` | `bool` | SO_REUSEPORT, so several sockets can bind one address. linux spreads the traffic across them, and only linux does, which std.system.capability.REUSE_PORT_BALANCES answers per target. darwin binds them all but delivers everything to the last one bound, which still serves a fast restart and not a multi-worker server. windows refuses with UNSUPPORTED |

### bind_options

```mach
pub fun bind_options() BindOptions
```

the options the plain bind and listen functions use

### check_bind_options

```mach
pub fun check_bind_options(options: BindOptions, op: std.io.error.Operation) err[std.io.error.Error]
```

refuses options the target cannot apply, before any socket exists

| Parameter | |
| :--- | :--- |
| `options` | the requested options |
| `op` | the operation a refusal is reported for |
| **returns** | ok, or UNSUPPORTED |

### apply_bind_options

```mach
pub fun apply_bind_options(handle: std.io.handle.SocketHandle, options: BindOptions) err[std.io.error.Error]
```

applies bind options to a freshly created socket

| Parameter | |
| :--- | :--- |
| `handle` | the socket, not yet bound |
| `options` | the options to apply |
| **returns** | ok, or the native refusal |

## Functions

### local_endpoint

```mach
pub fun local_endpoint(handle: std.io.handle.SocketHandle) res[std.net.ip.Endpoint, std.io.error.Error]
```

the local endpoint a socket is bound to

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| **returns** | the endpoint, or the failure. UNSUPPORTED when the address is not IP |

### remote_endpoint

```mach
pub fun remote_endpoint(handle: std.io.handle.SocketHandle) res[std.net.ip.Endpoint, std.io.error.Error]
```

the remote endpoint a socket is connected to

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| **returns** | the endpoint, or the failure. UNSUPPORTED when the address is not IP |

### inheritable

```mach
pub fun inheritable(handle: std.io.handle.SocketHandle) res[bool, std.io.error.Error]
```

whether child processes inherit a socket

| Parameter | |
| :--- | :--- |
| `handle` | the socket |
| **returns** | true when the socket is inherited, or the failure |

