[std](../README.md) / [system](README.md) / **file_identity**

# std.system.file_identity

observational identity within one host and its current mounted namespace

Source: [`src/system/file_identity.mach`](../../../src/system/file_identity.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Access`](#access) | `def` | maximum access authorized while retaining identity, never a required upgrade |
| [`Identity`](#identity) | `rec` | opaque to filesystem callers, native producers initialize every byte |

| On `Access` | |
| :--- | :--- |
| [`METADATA_ONLY`](#access), [`READ_AUTHORIZED`](#access) | |

| On `Identity` | |
| :--- | :--- |
| [`equal`](#equal) | |
| [`encode`](#encode) | failure leaves the output untouched |
| [`decode`](#decode) | only the complete current representation is accepted |
| [`native`](#native) | |

| Constants | |
| :--- | :--- |
| [`LINUX_LOCAL`](#constants), [`DARWIN_LOCAL`](#constants), [`WINDOWS_LOCAL`](#constants), [`WASI_LOCAL`](#constants), [`TEXT_CAPACITY`](#constants) | |

---

## Access

```mach
pub def Access: u8
```

maximum access authorized while retaining identity, never a required upgrade

| Name | Value | |
| :--- | :--- | :--- |
| `METADATA_ONLY` | `0` |  |
| `READ_AUTHORIZED` | `1` |  |

## Identity

```mach
pub rec Identity {
    representation: [41]u8;
}
```

opaque to filesystem callers, native producers initialize every byte

### equal

```mach
pub fun equal(a: Identity, b: Identity) bool
```

### encode

```mach
pub fun encode(value: Identity, out: *u8, capacity: usize) bool
```

failure leaves the output untouched

### decode

```mach
pub fun decode(text: str, out: *Identity) bool
```

only the complete current representation is accepted

### native

```mach
pub fun native(backend: u8, volume: u64, file: u64) Identity
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `LINUX_LOCAL` | `u8` | `1` |  |
| `DARWIN_LOCAL` | `u8` | `2` |  |
| `WINDOWS_LOCAL` | `u8` | `3` |  |
| `WASI_LOCAL` | `u8` | `4` |  |
| `TEXT_CAPACITY` | `usize` | `83` |  |

