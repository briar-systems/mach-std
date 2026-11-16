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
| [`Linger`](#linger) | `rec` |  |
| [`BindOptions`](#bindoptions) | `rec` | socket options applied between creation and bind |

| On `Flags` | |
| :--- | :--- |
| [`blocking_flags`](#blocking_flags), [`async_flags`](#async_flags), [`create`](#create), [`accept`](#accept) | |

| On `BoolOption` | |
| :--- | :--- |
| [`REUSE_ADDRESS`](#booloption), [`REUSE_PORT`](#booloption), [`EXCLUSIVE_ADDRESS`](#booloption), [`NO_DELAY`](#booloption), [`KEEP_ALIVE`](#booloption), [`IPV6_ONLY`](#booloption), [`FAST_OPEN`](#booloption), [`bool_option_supported`](#bool_option_supported), [`set_bool`](#set_bool), [`get_bool`](#get_bool) | |

| On `ValueOption` | |
| :--- | :--- |
| [`KEEP_IDLE_SECONDS`](#valueoption), [`KEEP_INTERVAL_SECONDS`](#valueoption), [`KEEP_PROBE_COUNT`](#valueoption), [`SEND_BUFFER_BYTES`](#valueoption), [`RECEIVE_BUFFER_BYTES`](#valueoption), [`TRAFFIC_CLASS_IPV4`](#valueoption), [`TRAFFIC_CLASS_IPV6`](#valueoption), [`value_option_supported`](#value_option_supported) | |
| [`set_value`](#set_value) | setters copy values immediately and retain no caller storage units are seconds, probe count, requested bytes, or an 8-bit traffic class |
| [`get_value`](#get_value) | |

| On `Linger` | |
| :--- | :--- |
| [`set_linger`](#set_linger), [`get_linger`](#get_linger) | |

| On `BindOptions` | |
| :--- | :--- |
| [`bind_options`](#bind_options) | the options the plain bind and listen functions use |
| [`check_bind_options`](#check_bind_options) | refuses options the target cannot apply, before any socket exists |
| [`apply_bind_options`](#apply_bind_options) | applies bind options to a freshly created socket |

| Functions | |
| :--- | :--- |
| [`local_endpoint`](#local_endpoint), [`remote_endpoint`](#remote_endpoint), [`inheritable`](#inheritable) | |

---

## Flags

```mach
pub rec Flags {
    nonblocking:     bool;
    non_inheritable: bool;
}
```

creation state is established before a handle reaches application code

### blocking_flags

```mach
pub fun blocking_flags() Flags
```

### async_flags

```mach
pub fun async_flags() Flags
```

### create

```mach
pub fun create(family: i32, typ: i32, protocol: i32, flags: Flags) res[std.io.handle.SocketHandle, std.io.error.Error]
```

### accept

```mach
pub fun accept(handle: std.io.handle.SocketHandle, flags: Flags, peer: *std.net.ip.Endpoint) res[std.io.handle.SocketHandle, std.io.error.Error]
```

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

### set_bool

```mach
pub fun set_bool(handle: std.io.handle.SocketHandle, option: BoolOption, enabled: bool) err[std.io.error.Error]
```

### get_bool

```mach
pub fun get_bool(handle: std.io.handle.SocketHandle, option: BoolOption) res[bool, std.io.error.Error]
```

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

## Linger

```mach
pub rec Linger {
    enabled: bool;
    seconds: u32;
}
```

### set_linger

```mach
pub fun set_linger(handle: std.io.handle.SocketHandle, value: Linger) err[std.io.error.Error]
```

### get_linger

```mach
pub fun get_linger(handle: std.io.handle.SocketHandle) res[Linger, std.io.error.Error]
```

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

### remote_endpoint

```mach
pub fun remote_endpoint(handle: std.io.handle.SocketHandle) res[std.net.ip.Endpoint, std.io.error.Error]
```

### inheritable

```mach
pub fun inheritable(handle: std.io.handle.SocketHandle) res[bool, std.io.error.Error]
```

